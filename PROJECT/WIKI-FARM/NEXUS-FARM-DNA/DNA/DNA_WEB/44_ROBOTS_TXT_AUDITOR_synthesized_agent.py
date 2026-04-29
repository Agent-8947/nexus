#!/usr/bin/env python3
"""
NEXUS DNA Web Agent: ROBOTS_TXT_AUDITOR
Tier: A-Target (Production-Hardened)
Spec Hash: 524f424f54535f54

Audit robots.txt for sensitive paths.
"""

import re
import logging
import requests
import sqlite3
import hashlib
import sys
import time
import json
from dataclasses import dataclass, field, asdict
from typing import List

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("ROBOTS_TXT_AUDITOR")

SENSITIVE_PATTERNS = ["admin", "backup", "private", "config", "dev", "api/v1"]
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

@dataclass
class RobotsTxtFinding:
    path: str
    finding: str

@dataclass
class RobotsTxtReport:
    url: str
    disallows_count: int = 0
    security_findings: List[RobotsTxtFinding] = field(default_factory=list)
    scanned_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    errors: List[str] = field(default_factory=list)

class RobotsTxtAuditorAgent:
    def __init__(self, db_path: str = "nexus_web.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NEXUS-WEB/1.0"})
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""CREATE TABLE IF NOT EXISTS robots_txt_auditor 
                                (id INTEGER PRIMARY KEY, url TEXT, path TEXT, finding TEXT, data_hash TEXT UNIQUE, ts DATETIME DEFAULT CURRENT_TIMESTAMP)""")
                conn.commit()
            logger.info("Storage ready.")
        except sqlite3.Error as exc:
            logger.critical("DB init failed: %s", exc)
            raise SystemExit(1) from exc

    @staticmethod
    def _hash(payload: str) -> str:
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def execute_audit(self, domain: str) -> RobotsTxtReport:
        url = f"http://{domain}/robots.txt" if not domain.startswith("http") else domain
        logger.info("Auditing robots.txt: %s", url)
        report = RobotsTxtReport(url=url)
        
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self.session.get(url, timeout=10)
                resp.raise_for_status()
                
                disallows = re.findall(r"Disallow:\s*(\S+)", resp.text, re.I)
                report.disallows_count = len(disallows)
                
                for path in disallows:
                    if any(p in path.lower() for p in SENSITIVE_PATTERNS):
                        finding = RobotsTxtFinding(path=path, finding="Sensitive path exposed")
                        report.security_findings.append(finding)
                        self._persist(url, finding)
                break
            except Exception as e:
                logger.error("Audit failed on attempt %d: %s", attempt, e)
                time.sleep(attempt * RETRY_BACKOFF)
                if attempt == MAX_RETRIES:
                    report.errors.append(f"robots.txt not found or unreachable: {e}")
                    
        return report

    def _persist(self, url: str, m: RobotsTxtFinding) -> None:
        h = self._hash(f"{url}:{m.path}")
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT OR IGNORE INTO robots_txt_auditor (url, path, finding, data_hash) VALUES (?,?,?,?)",
                             (url, m.path, m.finding, h))
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)

if __name__ == "__main__":
    if len(sys.argv) < 2: 
        print("Usage: python 44_ROBOTS_TXT_AUDITOR_synthesized_agent.py <domain>")
        sys.exit(1)
    print(json.dumps(asdict(RobotsTxtAuditorAgent().execute_audit(sys.argv[1])), indent=2))
