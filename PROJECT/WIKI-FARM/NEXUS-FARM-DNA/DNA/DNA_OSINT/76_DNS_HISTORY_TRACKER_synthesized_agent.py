#!/usr/bin/env python3
"""
NEXUS DNA OSINT Agent: DNS_HISTORY_TRACKER
Tier: S-Target (Production-Hardened)
Spec Hash: e71baa099235077c

Track historical DNS record changes for a domain via SecurityTrails.
"""

import json
import logging
import sqlite3
import hashlib
import sys
import time
import os
from dataclasses import dataclass, field, asdict
from typing import Optional, List

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("DNS_HISTORY_TRACKER")

ST_API_URL = "https://api.securitytrails.com/v1/domain/{domain}/dns/a/history"
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

@dataclass
class DnsHistoryRecord:
    domain: str
    record_type: str
    old_value: str = ""
    new_value: str = ""
    first_seen: str = ""
    last_seen: str = ""

@dataclass
class DnsHistoryReport:
    domain: str
    records: List[DnsHistoryRecord] = field(default_factory=list)
    scanned_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    errors: List[str] = field(default_factory=list)

class DnsHistoryTrackerAgent:
    """Agent for DNS history diffing with temporal correlation."""
    
    def __init__(self, db_path: str = "nexus_osint.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NEXUS-OSINT/1.0"})
        token = os.environ.get("SECURITYTRAILS_API_KEY")
        if token:
            self.session.headers["apikey"] = token
            logger.info("SecurityTrails API key loaded.")
        else:
            logger.warning("No SECURITYTRAILS_API_KEY env var.")
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS dns_history_tracker (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        domain TEXT NOT NULL,
                        record_type TEXT,
                        old_value TEXT,
                        new_value TEXT,
                        first_seen TEXT,
                        last_seen TEXT,
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

    def _get_history(self, domain: str) -> Optional[dict]:
        url = ST_API_URL.format(domain=domain)
        try:
            resp = self.session.get(url, timeout=15)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 403:
                logger.error("SecurityTrails API key invalid or restricted")
        except Exception as exc:
            logger.error("ST query error: %s", exc)
        return None

    def execute_scan(self, domain: str) -> DnsHistoryReport:
        logger.info("Tracking DNS history for: %s", domain)
        report = DnsHistoryReport(domain=domain)

        data = self._get_history(domain)
        if data and "records" in data:
            for rec in data["records"]:
                values = rec.get("values", [])
                val_str = ",".join(values)
                record = DnsHistoryRecord(
                    domain=domain,
                    record_type="A",
                    new_value=val_str,
                    first_seen=rec.get("first_seen", ""),
                    last_seen=rec.get("last_seen", "")
                )
                report.records.append(record)
                
                # Persist
                try:
                    with sqlite3.connect(self.db_path) as conn:
                        snap_blob = f"{domain}:A:{val_str}:{record.first_seen}"
                        conn.execute(
                            """INSERT OR IGNORE INTO dns_history_tracker
                               (domain, record_type, new_value, first_seen, last_seen, data_hash)
                               VALUES (?,?,?,?,?,?)""",
                            (domain, "A", val_str, record.first_seen, record.last_seen, self._hash(snap_blob)),
                        )
                        conn.commit()
                except sqlite3.Error as exc:
                    logger.error("DB error: %s", exc)
            logger.info("Found %d historical DNS records", len(report.records))
        else:
            logger.info("No records found or API unavailable")

        return report

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 76_DNS_HISTORY_TRACKER_synthesized_agent.py <domain>")
        sys.exit(1)

    agent = DnsHistoryTrackerAgent()
    result = agent.execute_scan(sys.argv[1])
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
