#!/usr/bin/env python3
"""
NEXUS DNA OSINT Agent: EMAIL_REPUTATION_PROFILER
Tier: S-Target (Production-Hardened)
Spec Hash: d34d11de12d3a297

Build reputation profile for email addresses using Disify and EmailRep APIs.
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
logger = logging.getLogger("EMAIL_REPUTATION_PROFILER")

DISIFY_API_URL = "https://disify.com/api/email/{email}"
EMAILREP_API_URL = "https://emailrep.io/{email}"
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

@dataclass
class EmailReputationRecord:
    email: str
    is_disposable: int = 0
    domain_age_days: int = 0
    reputation: str = "unknown"
    suspicious: int = 0
    profiles_found: str = ""

@dataclass
class EmailReputationReport:
    email: str
    profile: Optional[EmailReputationRecord] = None
    scanned_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    errors: List[str] = field(default_factory=list)

class EmailReputationProfilerAgent:
    """Multi-source email reputation scoring (Disify disposable check + EmailRep profile)."""
    
    def __init__(self, db_path: str = "nexus_osint.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NEXUS-OSINT/1.0"})
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS email_reputation_profiler (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT NOT NULL,
                        is_disposable INTEGER,
                        domain_age_days INTEGER,
                        reputation TEXT,
                        suspicious INTEGER,
                        profiles_found TEXT,
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

    def _query_disify(self, email: str) -> Optional[dict]:
        url = DISIFY_API_URL.format(email=email)
        try:
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                return resp.json()
        except requests.exceptions.RequestException as exc:
            logger.error("Disify query error: %s", exc)
        return None

    def _query_emailrep(self, email: str) -> Optional[dict]:
        url = EMAILREP_API_URL.format(email=email)
        try:
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                return resp.json()
        except requests.exceptions.RequestException as exc:
            logger.error("EmailRep query error: %s", exc)
        return None

    def execute_scan(self, email: str) -> EmailReputationReport:
        logger.info("Profiling email reputation for: %s", email)
        report = EmailReputationReport(email=email)
        record = EmailReputationRecord(email=email)

        # 1. Disify (disposable check)
        disify_data = self._query_disify(email)
        if disify_data:
            record.is_disposable = 1 if disify_data.get("disposable") else 0

        # 2. EmailRep
        rep_data = self._query_emailrep(email)
        if rep_data:
            record.reputation = rep_data.get("reputation", "unknown")
            record.suspicious = 1 if rep_data.get("suspicious") else 0
            details = rep_data.get("details", {})
            record.domain_age_days = details.get("days_since_domain_creation", 0)
            record.profiles_found = ",".join(details.get("profiles", []))

        report.profile = record

        # Persist
        try:
            with sqlite3.connect(self.db_path) as conn:
                snap_blob = f"{email}:{record.reputation}:{record.is_disposable}"
                conn.execute(
                    """INSERT OR IGNORE INTO email_reputation_profiler
                       (email, is_disposable, domain_age_days, reputation, suspicious, profiles_found, data_hash)
                       VALUES (?,?,?,?,?,?,?)""",
                    (email, record.is_disposable, record.domain_age_days, record.reputation, 
                     record.suspicious, record.profiles_found, self._hash(snap_blob)),
                )
                conn.commit()
            logger.info("Persisted reputation profile for %s", email)
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)
            report.errors.append(str(exc))

        return report

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 74_EMAIL_REPUTATION_PROFILER_synthesized_agent.py <email>")
        sys.exit(1)

    agent = EmailReputationProfilerAgent()
    result = agent.execute_scan(sys.argv[1])
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
