#!/usr/bin/env python3
"""
NEXUS DNA OSINT Agent: SOCIAL_GRAPH_ANALYZER
Tier: S-Target (Production-Hardened)

Builds a social/professional graph from GitHub public API.
Maps: user → repos → contributors → organizations.
No API key required (unauthenticated: 60 req/hour).
"""

import json
import logging
import sqlite3
import hashlib
import sys
import time
from dataclasses import dataclass, field, asdict
from typing import Optional

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("SOCIAL_GRAPH_ANALYZER")

GITHUB_API = "https://api.github.com"
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0


@dataclass
class GraphNode:
    login: str
    node_type: str  # "user", "org", "repo"
    url: str
    name: Optional[str] = None


@dataclass
class GraphEdge:
    source: str
    target: str
    relation: str  # "owns", "contributes_to", "member_of"


@dataclass
class SocialGraphReport:
    seed_user: str
    nodes: list[GraphNode] = field(default_factory=list)
    edges: list[GraphEdge] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class SocialGraphAnalyzerAgent:
    """Build relationship graph from GitHub public data."""

    def __init__(self, db_path: str = "nexus_osint.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "NEXUS-OSINT/1.0",
            "Accept": "application/vnd.github.v3+json",
        })
        # Use token from env if available (raises limit to 5000/hr)
        token = __import__("os").environ.get("GITHUB_TOKEN")
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
            logger.info("Authenticated via GITHUB_TOKEN env var.")
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS social_nodes (
                        id        INTEGER PRIMARY KEY AUTOINCREMENT,
                        login     TEXT NOT NULL,
                        node_type TEXT NOT NULL,
                        url       TEXT,
                        name      TEXT,
                        data_hash TEXT NOT NULL,
                        ts        DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(login, node_type)
                    )
                """)
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS social_edges (
                        id       INTEGER PRIMARY KEY AUTOINCREMENT,
                        source   TEXT NOT NULL,
                        target   TEXT NOT NULL,
                        relation TEXT NOT NULL,
                        ts       DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(source, target, relation)
                    )
                """)
                conn.commit()
            logger.info("Storage ready.")
        except sqlite3.Error as exc:
            logger.critical("DB init failed: %s", exc)
            raise SystemExit(1) from exc

    @staticmethod
    def _hash(payload: str) -> str:
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def _api_get(self, path: str) -> Optional[list | dict]:
        """GitHub API GET with retry and rate-limit handling."""
        url = f"{GITHUB_API}{path}"
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self.session.get(url, timeout=15)
                if resp.status_code == 403:
                    reset = resp.headers.get("X-RateLimit-Reset")
                    if reset:
                        wait = max(int(reset) - int(time.time()), 1)
                        logger.warning("Rate-limited. Reset in %ds", wait)
                        if wait < 120:
                            time.sleep(wait + 1)
                            continue
                    return None
                if resp.status_code == 404:
                    return None
                resp.raise_for_status()
                return resp.json()
            except requests.exceptions.Timeout:
                logger.warning("Timeout attempt %d/%d for %s", attempt, MAX_RETRIES, path)
                time.sleep(RETRY_BACKOFF * attempt)
            except requests.exceptions.RequestException as exc:
                logger.error("Request error for %s: %s", path, exc)
                return None
        return None

    def execute_scan(self, username: str) -> SocialGraphReport:
        logger.info("Building social graph for: %s", username)
        report = SocialGraphReport(seed_user=username)
        seen_logins: set[str] = set()

        # 1. Fetch user profile
        user_data = self._api_get(f"/users/{username}")
        if user_data is None:
            report.errors.append(f"User '{username}' not found or API error")
            return report

        report.nodes.append(GraphNode(
            login=username,
            node_type="user",
            url=user_data.get("html_url", ""),
            name=user_data.get("name"),
        ))
        seen_logins.add(username)

        # 2. Fetch organizations
        orgs = self._api_get(f"/users/{username}/orgs") or []
        for org in orgs:
            login = org.get("login", "")
            if login:
                report.nodes.append(GraphNode(
                    login=login, node_type="org",
                    url=f"https://github.com/{login}",
                    name=org.get("description"),
                ))
                report.edges.append(GraphEdge(
                    source=username, target=login, relation="member_of",
                ))

        # 3. Fetch repos and top contributors
        repos = self._api_get(f"/users/{username}/repos?per_page=10&sort=updated") or []
        for repo in repos[:10]:
            repo_name = repo.get("full_name", "")
            report.nodes.append(GraphNode(
                login=repo_name, node_type="repo",
                url=repo.get("html_url", ""),
                name=repo.get("description"),
            ))
            report.edges.append(GraphEdge(
                source=username, target=repo_name, relation="owns",
            ))

            # Fetch contributors
            contribs = self._api_get(f"/repos/{repo_name}/contributors?per_page=5") or []
            for contrib in contribs:
                c_login = contrib.get("login", "")
                if c_login and c_login not in seen_logins:
                    seen_logins.add(c_login)
                    report.nodes.append(GraphNode(
                        login=c_login, node_type="user",
                        url=contrib.get("html_url", ""),
                    ))
                report.edges.append(GraphEdge(
                    source=c_login, target=repo_name, relation="contributes_to",
                ))

        # Persist
        try:
            with sqlite3.connect(self.db_path) as conn:
                for node in report.nodes:
                    conn.execute(
                        """INSERT OR IGNORE INTO social_nodes
                           (login, node_type, url, name, data_hash) VALUES (?,?,?,?,?)""",
                        (node.login, node.node_type, node.url, node.name,
                         self._hash(f"{node.login}:{node.node_type}")),
                    )
                for edge in report.edges:
                    conn.execute(
                        """INSERT OR IGNORE INTO social_edges
                           (source, target, relation) VALUES (?,?,?)""",
                        (edge.source, edge.target, edge.relation),
                    )
                conn.commit()
            logger.info("Persisted %d nodes, %d edges", len(report.nodes), len(report.edges))
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)
            report.errors.append(str(exc))

        return report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 63_SOCIAL_GRAPH_ANALYZER_synthesized_agent.py <github_username>")
        sys.exit(1)

    agent = SocialGraphAnalyzerAgent()
    result = agent.execute_scan(sys.argv[1])
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
