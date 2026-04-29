#!/usr/bin/env python3
"""
NEXUS DNA OSINT Agent: DNS_ENUMERATOR
Tier: S-Target (Production-Hardened)

Enumerate DNS records (A, AAAA, MX, NS, TXT, CNAME, SOA) for a target domain
using public DNS-over-HTTPS resolvers (Cloudflare, Google).
No external dependencies beyond stdlib + requests.
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
logger = logging.getLogger("DNS_ENUMERATOR")

DOH_ENDPOINTS = [
    "https://cloudflare-dns.com/dns-query",
    "https://dns.google/resolve",
]

RECORD_TYPES = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]

MAX_RETRIES = 3
RETRY_BACKOFF = 1.5


@dataclass
class DnsRecord:
    name: str
    rtype: str
    ttl: int
    data: str


@dataclass
class DnsReport:
    target: str
    records: list[DnsRecord] = field(default_factory=list)
    resolver_used: str = ""
    errors: list[str] = field(default_factory=list)


class DnsEnumeratorAgent:
    """Production-grade DNS enumeration via DoH (DNS-over-HTTPS)."""

    def __init__(self, db_path: str = "nexus_osint.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/dns-json"})
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS dns_records (
                        id       INTEGER PRIMARY KEY AUTOINCREMENT,
                        target   TEXT    NOT NULL,
                        rtype    TEXT    NOT NULL,
                        ttl      INTEGER,
                        data     TEXT    NOT NULL,
                        data_hash TEXT   NOT NULL,
                        ts       DATETIME DEFAULT CURRENT_TIMESTAMP
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

    def _query_doh(self, domain: str, rtype: str) -> Optional[list[dict]]:
        """Query DNS-over-HTTPS with retry + fallback resolvers."""
        for resolver in DOH_ENDPOINTS:
            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    resp = self.session.get(
                        resolver,
                        params={"name": domain, "type": rtype},
                        timeout=10,
                    )
                    if resp.status_code == 429:
                        wait = RETRY_BACKOFF * attempt
                        logger.warning("Rate-limited by %s, backing off %.1fs", resolver, wait)
                        time.sleep(wait)
                        continue
                    resp.raise_for_status()
                    data = resp.json()
                    return data.get("Answer", [])
                except requests.exceptions.Timeout:
                    logger.warning("Timeout on %s attempt %d/%d", resolver, attempt, MAX_RETRIES)
                    time.sleep(RETRY_BACKOFF * attempt)
                except requests.exceptions.RequestException as exc:
                    logger.warning("Request error on %s: %s", resolver, exc)
                    break  # try next resolver
        return None

    def execute_scan(self, target: str) -> DnsReport:
        logger.info("Starting DNS enumeration for: %s", target)
        report = DnsReport(target=target)

        for rtype in RECORD_TYPES:
            answers = self._query_doh(target, rtype)
            if answers is None:
                report.errors.append(f"Failed to resolve {rtype}")
                continue
            for ans in answers:
                rec = DnsRecord(
                    name=ans.get("name", target),
                    rtype=rtype,
                    ttl=ans.get("TTL", 0),
                    data=ans.get("data", ""),
                )
                report.records.append(rec)

        # Persist all discovered records
        try:
            with sqlite3.connect(self.db_path) as conn:
                for rec in report.records:
                    conn.execute(
                        "INSERT INTO dns_records (target, rtype, ttl, data, data_hash) VALUES (?,?,?,?,?)",
                        (target, rec.rtype, rec.ttl, rec.data, self._hash(rec.data)),
                    )
                conn.commit()
            logger.info("Persisted %d records for %s", len(report.records), target)
        except sqlite3.Error as exc:
            logger.error("DB persist error: %s", exc)
            report.errors.append(str(exc))

        return report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 60_DNS_ENUMERATOR_synthesized_agent.py <domain>")
        sys.exit(1)

    agent = DnsEnumeratorAgent()
    result = agent.execute_scan(sys.argv[1])
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
