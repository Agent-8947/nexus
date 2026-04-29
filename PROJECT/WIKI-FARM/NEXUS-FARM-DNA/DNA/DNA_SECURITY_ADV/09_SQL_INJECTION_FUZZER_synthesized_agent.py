#!/usr/bin/env python3
"""
NEXUS DNA Security Agent: SQL_INJECTION_FUZZER
Tier: A-Target (Production-Hardened)
Spec Hash: 53514c495f46555a

Identify potential SQL injection points via error-based and boolean-based fuzzing.
"""

import json
import logging
import sqlite3
import hashlib
import time
import sys
import requests
from dataclasses import dataclass, field, asdict
from typing import List

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("SQL_INJECTION_FUZZER")

PAYLOADS = ["'", "''", "\" OR 1=1 --", "' OR '1'='1", "') OR ('1'='1"]
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

@dataclass
class SqlFinding:
    url: str
    parameter: str
    payload: str
    response_diff: float
    is_vulnerable: int

@dataclass
class SqlFuzzerReport:
    target_url: str
    findings: List[SqlFinding] = field(default_factory=list)
    scanned_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    errors: List[str] = field(default_factory=list)

class SqlInjectionFuzzerAgent:
    def __init__(self, db_path: str = "nexus_security.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NEXUS-SEC/1.0"})
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""CREATE TABLE IF NOT EXISTS sql_injection_fuzzer 
                                (id INTEGER PRIMARY KEY, url TEXT, parameter TEXT, payload TEXT, response_diff REAL, is_vulnerable INTEGER, data_hash TEXT UNIQUE, ts DATETIME DEFAULT CURRENT_TIMESTAMP)""")
                conn.commit()
            logger.info("Storage ready.")
        except sqlite3.Error as exc:
            logger.critical("DB init failed: %s", exc)
            raise SystemExit(1) from exc

    @staticmethod
    def _hash(payload: str) -> str:
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def execute_scan(self, url: str) -> SqlFuzzerReport:
        logger.info("Fuzzing URL for SQLi: %s", url)
        report = SqlFuzzerReport(target_url=url)
        
        try:
            base_resp = self.session.get(url, timeout=10)
            base_len = len(base_resp.text)
            
            for p in PAYLOADS:
                test_url = f"{url}?id={p}" if "?" not in url else f"{url}&id={p}"
                
                for attempt in range(1, MAX_RETRIES + 1):
                    try:
                        resp = self.session.get(test_url, timeout=10)
                        diff = abs(len(resp.text) - base_len) / (base_len or 1)
                        
                        if "sql" in resp.text.lower() or "syntax" in resp.text.lower() or diff > 0.2:
                            finding = SqlFinding(url, "id", p, float(diff), 1)
                            report.findings.append(finding)
                            self._persist(finding)
                        break
                    except Exception as e:
                        logger.error("Scan error: %s", e)
                        time.sleep(attempt * RETRY_BACKOFF)
                        if attempt == MAX_RETRIES:
                            report.errors.append(f"Failed to fetch {test_url}")
                    
        except Exception as e:
            logger.error("Base fetch error: %s", e)
            report.errors.append(str(e))
            
        return report

    def _persist(self, m: SqlFinding) -> None:
        h = self._hash(f"{m.url}:{m.parameter}:{m.payload}")
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT OR IGNORE INTO sql_injection_fuzzer (url, parameter, payload, response_diff, is_vulnerable, data_hash) VALUES (?,?,?,?,?,?)",
                             (m.url, m.parameter, m.payload, m.response_diff, m.is_vulnerable, h))
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)

if __name__ == "__main__":
    if len(sys.argv) < 2: 
        print("Usage: python 09_SQL_INJECTION_FUZZER_synthesized_agent.py <url>")
        sys.exit(1)
    print(json.dumps(asdict(SqlInjectionFuzzerAgent().execute_scan(sys.argv[1])), indent=2))
