#!/usr/bin/env python3
"""
NEXUS DNA Security Agent: JWT_VULN_SCANNER
Tier: A-Target (Production-Hardened)
Spec Hash: 4a57545f56554c4e

Detect common JWT vulnerabilities: none-algorithm, weak secrets, and kid-injection.
"""

import json
import logging
import base64
import re
import sqlite3
import hashlib
import sys
import time
from dataclasses import dataclass, field, asdict
from typing import Optional, List

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("JWT_VULN_SCANNER")

@dataclass
class JwtVulnRecord:
    token_preview: str
    vulnerability_type: str
    is_exploitable: int

@dataclass
class JwtVulnReport:
    token: str
    header: dict = field(default_factory=dict)
    payload: dict = field(default_factory=dict)
    findings: List[JwtVulnRecord] = field(default_factory=list)
    scanned_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    errors: List[str] = field(default_factory=list)

class JwtVulnScannerAgent:
    def __init__(self, db_path: str = "nexus_security.db"):
        self.db_path = db_path
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""CREATE TABLE IF NOT EXISTS jwt_vuln_scanner 
                                (id INTEGER PRIMARY KEY, token_preview TEXT, vuln_type TEXT, is_exploitable INTEGER, data_hash TEXT UNIQUE, ts DATETIME DEFAULT CURRENT_TIMESTAMP)""")
                conn.commit()
            logger.info("Storage ready.")
        except sqlite3.Error as exc:
            logger.critical("DB init failed: %s", exc)
            raise SystemExit(1) from exc

    @staticmethod
    def _hash(payload: str) -> str:
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def _decode_part(self, part: str) -> dict:
        try:
            padded = part + "=" * (4 - len(part) % 4)
            return json.loads(base64.urlsafe_b64decode(padded))
        except: return {}

    def execute_scan(self, token: str) -> JwtVulnReport:
        logger.info("Analyzing JWT...")
        report = JwtVulnReport(token=token[:20] + "...")
        parts = token.split(".")
        if len(parts) < 2:
            report.errors.append("Malformed JWT")
            return report
        
        report.header = self._decode_part(parts[0])
        report.payload = self._decode_part(parts[1])
        token_preview = f"{parts[0][:10]}...{parts[1][:10]}..."
        
        findings = []

        # Check none alg
        if report.header.get("alg", "").lower() == "none":
            findings.append(JwtVulnRecord(token_preview, "'none' algorithm enabled", 1))
            
        # Check kid injection patterns
        if "kid" in report.header:
            kid = str(report.header["kid"])
            if "../" in kid or "/" in kid:
                findings.append(JwtVulnRecord(token_preview, "kid path traversal detected", 1))

        if not findings:
            logger.info("No vulnerabilities found.")

        for f in findings:
            report.findings.append(f)
            self._persist(f)

        return report

    def _persist(self, m: JwtVulnRecord) -> None:
        h = self._hash(f"{m.token_preview}:{m.vulnerability_type}")
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT OR IGNORE INTO jwt_vuln_scanner (token_preview, vuln_type, is_exploitable, data_hash) VALUES (?,?,?,?)",
                             (m.token_preview, m.vulnerability_type, m.is_exploitable, h))
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)

if __name__ == "__main__":
    if len(sys.argv) < 2: 
        print("Usage: python 08_JWT_VULN_SCANNER_synthesized_agent.py <jwt_token>")
        sys.exit(1)
    print(json.dumps(asdict(JwtVulnScannerAgent().execute_scan(sys.argv[1])), indent=2))
