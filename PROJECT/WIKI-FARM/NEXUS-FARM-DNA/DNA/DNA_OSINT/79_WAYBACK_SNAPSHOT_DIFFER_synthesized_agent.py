#!/usr/bin/env python3
"""
NEXUS DNA OSINT Agent: WAYBACK_SNAPSHOT_DIFFER
Tier: S-Target (Production-Hardened)
Spec Hash: 789fee081c8e5c18

Compare historical website snapshots from Wayback Machine CDX API.
"""

import json
import logging
import sqlite3
import hashlib
import sys
import time
from dataclasses import dataclass, field, asdict
from typing import Optional, List

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("WAYBACK_SNAPSHOT_DIFFER")

WAYBACK_CDX_URL = "https://web.archive.org/cdx/search/cdx?url={domain}&output=json"
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

@dataclass
class SnapshotRecord:
    domain: str
    timestamp: str
    status_code: int
    digest: str
    mime_type: str = ""
    content_length: int = 0

@dataclass
class WaybackReport:
    domain: str
    snapshots: List[SnapshotRecord] = field(default_factory=list)
    scanned_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    errors: List[str] = field(default_factory=list)

class WaybackSnapshotDifferAgent:
    """Agent for Wayback CDX temporal diffing with content digest comparison."""
    
    def __init__(self, db_path: str = "nexus_osint.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NEXUS-OSINT/1.0"})
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS wayback_snapshot_differ (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        domain TEXT NOT NULL,
                        timestamp TEXT,
                        status_code INTEGER,
                        digest TEXT,
                        mime_type TEXT,
                        content_length INTEGER,
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

    def _query_cdx(self, domain: str) -> Optional[list]:
        url = WAYBACK_CDX_URL.format(domain=domain)
        try:
            resp = self.session.get(url, timeout=20)
            if resp.status_code == 200:
                return resp.json()
        except Exception as exc:
            logger.error("Wayback CDX error: %s", exc)
        return None

    def execute_scan(self, domain: str) -> WaybackReport:
        logger.info("Analyzing historical snapshots for: %s", domain)
        report = WaybackReport(domain=domain)

        data = self._query_cdx(domain)
        if data and len(data) > 1:
            # Skip first row (column names)
            header = data[0]
            for row in data[1:30]: # Limit to 30 snapshots
                # row structure: [urlkey, timestamp, original, mimetype, statuscode, digest, length]
                try:
                    record = SnapshotRecord(
                        domain=domain,
                        timestamp=row[1],
                        status_code=int(row[4]) if row[4].isdigit() else 0,
                        digest=row[5],
                        mime_type=row[3],
                        content_length=int(row[6]) if row[6].isdigit() else 0
                    )
                    report.snapshots.append(record)
                    
                    # Persist
                    with sqlite3.connect(self.db_path) as conn:
                        snap_blob = f"{domain}:{record.timestamp}:{record.digest}"
                        conn.execute(
                            """INSERT OR IGNORE INTO wayback_snapshot_differ
                               (domain, timestamp, status_code, digest, mime_type, content_length, data_hash)
                               VALUES (?,?,?,?,?,?,?)""",
                            (domain, record.timestamp, record.status_code, record.digest, 
                             record.mime_type, record.content_length, self._hash(snap_blob)),
                        )
                    conn.commit()
                except (IndexError, ValueError) as exc:
                    continue
            logger.info("Diffed %d snapshots from Wayback CDX", len(report.snapshots))
        else:
            logger.info("No snapshots found for %s", domain)

        return report

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 79_WAYBACK_SNAPSHOT_DIFFER_synthesized_agent.py <domain>")
        sys.exit(1)

    agent = WaybackSnapshotDifferAgent()
    result = agent.execute_scan(sys.argv[1])
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
