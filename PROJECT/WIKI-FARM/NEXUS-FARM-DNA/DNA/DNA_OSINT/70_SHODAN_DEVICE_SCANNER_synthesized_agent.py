#!/usr/bin/env python3
"""
NEXUS DNA OSINT Agent: SHODAN_DEVICE_SCANNER
Tier: S-Target (Production-Hardened)
Spec Hash: c321b3d8dabaf87c

Discover internet-connected devices and open ports via Shodan InternetDB.
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
logger = logging.getLogger("SHODAN_DEVICE_SCANNER")

SHODAN_INTERNET_DB_URL = "https://internetdb.shodan.io/{ip}"
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

@dataclass
class ShodanDeviceRecord:
    ip: str
    ports: List[int] = field(default_factory=list)
    hostnames: List[str] = field(default_factory=list)
    cpes: List[str] = field(default_factory=list)
    vulns: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

@dataclass
class ShodanDeviceScannerReport:
    target_ip: str
    device_info: Optional[ShodanDeviceRecord] = None
    scanned_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    errors: List[str] = field(default_factory=list)

class ShodanDeviceScannerAgent:
    """Agent for Shodan InternetDB passive reconnaissance."""
    
    def __init__(self, db_path: str = "nexus_osint.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NEXUS-OSINT/1.0"})
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS shodan_device_scanner (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ip TEXT NOT NULL,
                        ports TEXT,
                        hostnames TEXT,
                        cpes TEXT,
                        vulns TEXT,
                        tags TEXT,
                        data_hash TEXT NOT NULL,
                        ts DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(ip, data_hash)
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

    def _fetch_internet_db(self, ip: str) -> Optional[dict]:
        url = SHODAN_INTERNET_DB_URL.format(ip=ip)
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self.session.get(url, timeout=15)
                if resp.status_code == 429:
                    wait = RETRY_BACKOFF * attempt
                    logger.warning("Rate-limited, backing off %.1fs", wait)
                    time.sleep(wait)
                    continue
                if resp.status_code == 404:
                    logger.info("No data found for IP: %s", ip)
                    return None
                resp.raise_for_status()
                return resp.json()
            except requests.exceptions.RequestException as exc:
                logger.error("Request error for %s: %s", url, exc)
                time.sleep(RETRY_BACKOFF * attempt)
        return None

    def execute_scan(self, ip: str) -> ShodanDeviceScannerReport:
        logger.info("Scanning IP via Shodan InternetDB: %s", ip)
        report = ShodanDeviceScannerReport(target_ip=ip)

        data = self._fetch_internet_db(ip)
        if data:
            record = ShodanDeviceRecord(
                ip=data.get("ip", ip),
                ports=data.get("ports", []),
                hostnames=data.get("hostnames", []),
                cpes=data.get("cpes", []),
                vulns=data.get("vulns", []),
                tags=data.get("tags", []),
            )
            report.device_info = record
            
            # Persist
            try:
                with sqlite3.connect(self.db_path) as conn:
                    snapshot = json.dumps(asdict(record), sort_keys=True)
                    conn.execute(
                        """INSERT OR IGNORE INTO shodan_device_scanner
                           (ip, ports, hostnames, cpes, vulns, tags, data_hash)
                           VALUES (?,?,?,?,?,?,?)""",
                        (record.ip, json.dumps(record.ports), json.dumps(record.hostnames),
                         json.dumps(record.cpes), json.dumps(record.vulns), json.dumps(record.tags),
                         self._hash(snapshot)),
                    )
                    conn.commit()
                logger.info("Persisted device info for %s", ip)
            except sqlite3.Error as exc:
                logger.error("DB error: %s", exc)
                report.errors.append(str(exc))
        else:
            report.errors.append("No InternetDB data available for this IP")

        return report

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 70_SHODAN_DEVICE_SCANNER_synthesized_agent.py <ip>")
        sys.exit(1)

    agent = ShodanDeviceScannerAgent()
    result = agent.execute_scan(sys.argv[1])
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
