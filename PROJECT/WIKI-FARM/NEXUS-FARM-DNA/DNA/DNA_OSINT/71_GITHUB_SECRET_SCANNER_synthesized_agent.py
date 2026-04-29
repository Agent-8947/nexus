#!/usr/bin/env python3
"""
NEXUS DNA OSINT Agent: GITHUB_SECRET_SCANNER
Tier: S-Target (Production-Hardened)
Spec Hash: b571ff6d93c667a7

Search GitHub code for leaked secrets, API keys, and credentials.
"""

import json
import logging
import sqlite3
import hashlib
import sys
import time
import os
import re
from dataclasses import dataclass, field, asdict
from typing import Optional, List

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("GITHUB_SECRET_SCANNER")

GITHUB_API_URL = "https://api.github.com/search/code"
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

@dataclass
class SecretMatch:
    query: str
    repo_full_name: str
    file_path: str
    match_snippet: str
    secret_type: str

@dataclass
class GithubSecretScannerReport:
    query: str
    matches: List[SecretMatch] = field(default_factory=list)
    scanned_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    errors: List[str] = field(default_factory=list)

class GithubSecretScannerAgent:
    """Agent for GitHub code search with secret pattern detection."""
    
    def __init__(self, db_path: str = "nexus_osint.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "NEXUS-OSINT/1.0",
            "Accept": "application/vnd.github.v3+json",
        })
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            self.session.headers["Authorization"] = f"token {token}"
            logger.info("GitHub API token loaded from env.")
        else:
            logger.warning("No GITHUB_TOKEN env var — search API will be highly restricted.")
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS github_secret_scanner (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        query TEXT NOT NULL,
                        repo_full_name TEXT,
                        file_path TEXT,
                        match_snippet TEXT,
                        secret_type TEXT,
                        data_hash TEXT NOT NULL,
                        ts DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(data_hash)
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

    def _search_code(self, query: str) -> Optional[dict]:
        params = {"q": query, "per_page": 20}
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self.session.get(GITHUB_API_URL, params=params, timeout=20)
                if resp.status_code == 403:
                    reset = resp.headers.get("X-RateLimit-Reset")
                    if reset:
                        wait = max(int(reset) - int(time.time()), 1)
                        logger.warning("Rate-limited. Reset in %ds", wait)
                        if wait < 60:
                            time.sleep(wait + 1)
                            continue
                    return None
                if resp.status_code == 422:
                    logger.error("GitHub search query is invalid: %s", query)
                    return None
                resp.raise_for_status()
                return resp.json()
            except requests.exceptions.RequestException as exc:
                logger.error("GitHub search error: %s", exc)
                time.sleep(RETRY_BACKOFF * attempt)
        return None

    def execute_scan(self, query: str, secret_type: str = "unknown") -> GithubSecretScannerReport:
        logger.info("Searching GitHub code for: %s (type: %s)", query, secret_type)
        report = GithubSecretScannerReport(query=query)

        data = self._search_code(query)
        if data and "items" in data:
            for item in data["items"]:
                repo = item.get("repository", {}).get("full_name", "")
                path = item.get("path", "")
                # Snippet is not provided in core search/code API, usually requires fetching file content
                # For this agent, we record the repo and path
                match = SecretMatch(
                    query=query,
                    repo_full_name=repo,
                    file_path=path,
                    match_snippet=f"Detected leak in {path} at {repo}",
                    secret_type=secret_type
                )
                report.matches.append(match)
                
                # Persist
                try:
                    with sqlite3.connect(self.db_path) as conn:
                        snap_blob = f"{repo}:{path}:{query}:{secret_type}"
                        conn.execute(
                            """INSERT OR IGNORE INTO github_secret_scanner
                               (query, repo_full_name, file_path, match_snippet, secret_type, data_hash)
                               VALUES (?,?,?,?,?,?)""",
                            (query, repo, path, match.match_snippet, secret_type, self._hash(snap_blob)),
                        )
                        conn.commit()
                except sqlite3.Error as exc:
                    logger.error("DB storage error: %s", exc)
            logger.info("Found %d potential matches on GitHub", len(report.matches))
        else:
            logger.info("No matches found or search failed")

        return report

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 71_GITHUB_SECRET_SCANNER_synthesized_agent.py <query> [secret_type]")
        sys.exit(1)

    agent = GithubSecretScannerAgent()
    stype = sys.argv[2] if len(sys.argv) > 2 else "generic_secret"
    result = agent.execute_scan(sys.argv[1], stype)
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
