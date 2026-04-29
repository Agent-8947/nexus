#!/usr/bin/env python3
"""
NEXUS DNA Infra Agent: SSH_BRUTEFORCE_LOG_ANALYZER
Tier: A-Target (Production-Hardened)
Spec Hash: 5353485f42525554

Analyze auth.log for SSH bruteforce attempts.
"""

import re
import logging
import sqlite3
import hashlib
import sys
import time
import json
from collections import Counter
from dataclasses import dataclass, field, asdict
from typing import List

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("SSH_BRUTEFORCE_LOG_ANALYZER")

@dataclass
class AttackerRecord:
    ip: str
    count: int
    usernames: str
    risk: str

@dataclass
class SshBruteforceReport:
    log_path: str
    top_attackers: List[AttackerRecord] = field(default_factory=list)
    scanned_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    errors: List[str] = field(default_factory=list)

class SshBruteforceLogAnalyzerAgent:
    def __init__(self, db_path: str = "nexus_infra.db"):
        self.db_path = db_path
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""CREATE TABLE IF NOT EXISTS ssh_bruteforce_analyzer 
                                (id INTEGER PRIMARY KEY, ip TEXT, count INTEGER, usernames TEXT, risk TEXT, data_hash TEXT UNIQUE, ts DATETIME DEFAULT CURRENT_TIMESTAMP)""")
                conn.commit()
            logger.info("Storage ready.")
        except sqlite3.Error as exc:
            logger.critical("DB init failed: %s", exc)
            raise SystemExit(1) from exc

    @staticmethod
    def _hash(payload: str) -> str:
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def execute_analysis(self, log_path: str) -> SshBruteforceReport:
        logger.info("Analyzing auth log: %s", log_path)
        report = SshBruteforceReport(log_path=log_path)
        pattern = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\d+\.\d+\.\d+\.\d+) port")
        attempts = Counter()
        users = {}
        
        try:
            with open(log_path, 'r') as f:
                for line in f:
                    match = pattern.search(line)
                    if match:
                        user, ip = match.groups()
                        attempts[ip] += 1
                        if ip not in users: users[ip] = set()
                        users[ip].add(user)
                        
            for ip, count in attempts.most_common(10):
                record = AttackerRecord(
                    ip=ip, 
                    count=count, 
                    usernames=",".join(list(users[ip])[:5]), 
                    risk="High" if count > 50 else "Medium"
                )
                report.top_attackers.append(record)
                self._persist(record)
                
        except Exception as e:
            logger.error("Log analysis failed: %s", e)
            report.errors.append(f"Could not read log file: {e}")
            
        return report

    def _persist(self, m: AttackerRecord) -> None:
        h = self._hash(f"{m.ip}:{m.count}")
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT OR IGNORE INTO ssh_bruteforce_analyzer (ip, count, usernames, risk, data_hash) VALUES (?,?,?,?,?)",
                             (m.ip, m.count, m.usernames, m.risk, h))
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)

if __name__ == "__main__":
    if len(sys.argv) < 2: 
        print("Usage: python 18_SSH_BRUTEFORCE_LOG_ANALYZER_synthesized_agent.py <log_path>")
        sys.exit(1)
    print(json.dumps(asdict(SshBruteforceLogAnalyzerAgent().execute_analysis(sys.argv[1])), indent=2))
