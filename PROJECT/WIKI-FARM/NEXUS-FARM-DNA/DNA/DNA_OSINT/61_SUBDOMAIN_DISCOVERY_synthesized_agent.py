#!/usr/bin/env python3
"""
NEXUS DNA OSINT Agent: SUBDOMAIN_DISCOVERY
Tier: S-Target (Production-Hardened)

Discovers subdomains via Certificate Transparency logs (crt.sh),
deduplicates, resolves live hosts, and persists results.
"""

import json
import logging
import sqlite3
import hashlib
import socket
import sys
import time
from dataclasses import dataclass, field, asdict
from typing import Optional

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("SUBDOMAIN_DISCOVERY")

MAX_RETRIES = 3
RETRY_BACKOFF = 2.0
CRT_SH_URL = "https://crt.sh/"


@dataclass
class SubdomainRecord:
    subdomain: str
    resolved_ip: Optional[str] = None
    is_live: bool = False
    source: str = "crt.sh"


@dataclass
class SubdomainReport:
    target: str
    total_found: int = 0
    live_count: int = 0
    subdomains: list[SubdomainRecord] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class SubdomainDiscoveryAgent:
    """Subdomain enumeration via CT logs with live-host resolution."""

    def __init__(self, db_path: str = "nexus_osint.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NEXUS-OSINT/1.0"})
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS subdomains (
                        id         INTEGER PRIMARY KEY AUTOINCREMENT,
                        target     TEXT NOT NULL,
                        subdomain  TEXT NOT NULL,
                        resolved_ip TEXT,
                        is_live    INTEGER DEFAULT 0,
                        data_hash  TEXT NOT NULL,
                        ts         DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(target, subdomain)
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

    def _fetch_ct_logs(self, domain: str) -> Optional[list[dict]]:
        """Fetch certificate transparency data from crt.sh with retry."""
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self.session.get(
                    CRT_SH_URL,
                    params={"q": f"%.{domain}", "output": "json"},
                    timeout=20,
                )
                if resp.status_code == 429:
                    wait = RETRY_BACKOFF * attempt
                    logger.warning("Rate-limited, backing off %.1fs", wait)
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                return resp.json()
            except requests.exceptions.Timeout:
                logger.warning("Timeout attempt %d/%d", attempt, MAX_RETRIES)
                time.sleep(RETRY_BACKOFF * attempt)
            except requests.exceptions.JSONDecodeError as exc:
                logger.error("Invalid JSON from crt.sh: %s", exc)
                return None
            except requests.exceptions.RequestException as exc:
                logger.error("Network error: %s", exc)
                time.sleep(RETRY_BACKOFF * attempt)
        return None

    @staticmethod
    def _extract_subdomains(ct_data: list[dict]) -> set[str]:
        """Deduplicate and normalize subdomains from CT log entries."""
        subs: set[str] = set()
        for entry in ct_data:
            name_value = entry.get("name_value", "")
            for line in name_value.strip().split("\n"):
                clean = line.strip().lower().lstrip("*.")
                if clean and not clean.startswith("."):
                    subs.add(clean)
        return subs

    @staticmethod
    def _resolve_host(hostname: str) -> Optional[str]:
        """Attempt DNS resolution to check if host is live."""
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            return None

    def execute_scan(self, target: str) -> SubdomainReport:
        logger.info("Starting subdomain discovery for: %s", target)
        report = SubdomainReport(target=target)

        ct_data = self._fetch_ct_logs(target)
        if ct_data is None:
            report.errors.append("Failed to fetch CT logs")
            return report

        unique_subs = self._extract_subdomains(ct_data)
        report.total_found = len(unique_subs)
        logger.info("Found %d unique subdomains", report.total_found)

        for sub in sorted(unique_subs):
            ip = self._resolve_host(sub)
            rec = SubdomainRecord(
                subdomain=sub,
                resolved_ip=ip,
                is_live=ip is not None,
            )
            report.subdomains.append(rec)
            if rec.is_live:
                report.live_count += 1

        # Persist
        try:
            with sqlite3.connect(self.db_path) as conn:
                for rec in report.subdomains:
                    conn.execute(
                        """INSERT OR IGNORE INTO subdomains
                           (target, subdomain, resolved_ip, is_live, data_hash)
                           VALUES (?,?,?,?,?)""",
                        (target, rec.subdomain, rec.resolved_ip, int(rec.is_live),
                         self._hash(rec.subdomain)),
                    )
                conn.commit()
            logger.info("Persisted %d subdomains (%d live)", report.total_found, report.live_count)
        except sqlite3.Error as exc:
            logger.error("DB persist error: %s", exc)
            report.errors.append(str(exc))

        return report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 61_SUBDOMAIN_DISCOVERY_synthesized_agent.py <domain>")
        sys.exit(1)

    agent = SubdomainDiscoveryAgent()
    result = agent.execute_scan(sys.argv[1])
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
