#!/usr/bin/env python3
"""
NEXUS DNA Infra Agent: SSL_CERT_EXPIRY_WATCHER
Tier: A-Target (Production-Hardened)
Spec Hash: 53534c5f43455254

Monitor SSL/TLS certificate expiry dates.
"""

import ssl
import socket
import logging
import sqlite3
import hashlib
import sys
import time
import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("SSL_CERT_EXPIRY_WATCHER")

MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

@dataclass
class SslCertRecord:
    domain: str
    expiry: str
    days_remaining: int
    is_expired: int

@dataclass
class SslCertReport:
    domain: str
    record: Optional[SslCertRecord] = None
    scanned_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    errors: List[str] = field(default_factory=list)

class SslCertExpiryWatcherAgent:
    def __init__(self, db_path: str = "nexus_infra.db"):
        self.db_path = db_path
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""CREATE TABLE IF NOT EXISTS ssl_cert_watcher 
                                (id INTEGER PRIMARY KEY, domain TEXT, expiry TEXT, days_remaining INTEGER, is_expired INTEGER, data_hash TEXT UNIQUE, ts DATETIME DEFAULT CURRENT_TIMESTAMP)""")
                conn.commit()
            logger.info("Storage ready.")
        except sqlite3.Error as exc:
            logger.critical("DB init failed: %s", exc)
            raise SystemExit(1) from exc

    @staticmethod
    def _hash(payload: str) -> str:
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def get_expiry(self, domain: str) -> SslCertReport:
        logger.info("Checking cert for %s", domain)
        report = SslCertReport(domain=domain)
        
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                context = ssl.create_default_context()
                with socket.create_connection((domain, 443), timeout=10) as sock:
                    with context.wrap_socket(sock, server_hostname=domain) as ssock:
                        cert = ssock.getpeercert()
                        expiry_str = cert.get('notAfter')
                        expiry_dt = datetime.datetime.strptime(expiry_str, '%b %d %H:%M:%S %Y %Z')
                        remaining = (expiry_dt - datetime.datetime.utcnow()).days
                        
                        record = SslCertRecord(
                            domain=domain,
                            expiry=expiry_str,
                            days_remaining=remaining,
                            is_expired=1 if remaining < 0 else 0
                        )
                        report.record = record
                        self._persist(record)
                        break
            except Exception as e:
                logger.error("Failed to check %s on attempt %d: %s", domain, attempt, e)
                time.sleep(attempt * RETRY_BACKOFF)
                if attempt == MAX_RETRIES:
                    report.errors.append(f"Handshake failed: {e}")
                    
        return report

    def _persist(self, m: SslCertRecord) -> None:
        h = self._hash(f"{m.domain}:{m.expiry}")
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT OR IGNORE INTO ssl_cert_watcher (domain, expiry, days_remaining, is_expired, data_hash) VALUES (?,?,?,?,?)",
                             (m.domain, m.expiry, m.days_remaining, m.is_expired, h))
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)

if __name__ == "__main__":
    if len(sys.argv) < 2: 
        print("Usage: python 16_SSL_CERT_EXPIRY_WATCHER_synthesized_agent.py <domain>")
        sys.exit(1)
    print(json.dumps(asdict(SslCertExpiryWatcherAgent().get_expiry(sys.argv[1])), indent=2))
