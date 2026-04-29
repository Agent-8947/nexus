#!/usr/bin/env python3
"""
NEXUS DNA OSINT Agent: THREAT_INTEL_FEED
Tier: S-Target (Production-Hardened)
Spec Hash: 6ae79175b1138c31

Aggregate indicators of compromise (IoCs) from AlienVault OTX and URLhaus.
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
logger = logging.getLogger("THREAT_INTEL_FEED")

OTX_API_URL = "https://otx.alienvault.com/api/v1/indicators/IPv4/{target}/general"
URLHAUS_API_URL = "https://urlhaus-api.abuse.ch/v1/host/"
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

@dataclass
class IoCRecord:
    indicator: str
    indicator_type: str
    source: str
    pulse_count: int = 0
    threat_score: float = 0.0
    tags: str = ""

@dataclass
class ThreatIntelReport:
    target: str
    iocs: List[IoCRecord] = field(default_factory=list)
    scanned_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    errors: List[str] = field(default_factory=list)

class ThreatIntelFeedAgent:
    """Multi-source IoC correlation (AlienVault OTX + URLhaus)."""
    
    def __init__(self, db_path: str = "nexus_osint.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NEXUS-OSINT/1.0"})
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS threat_intel_feed (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        indicator TEXT NOT NULL,
                        indicator_type TEXT,
                        source TEXT,
                        pulse_count INTEGER,
                        threat_score REAL,
                        tags TEXT,
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

    def _query_otx(self, target: str) -> Optional[dict]:
        url = OTX_API_URL.format(target=target)
        try:
            resp = self.session.get(url, timeout=15)
            if resp.status_code == 200:
                return resp.json()
        except requests.exceptions.RequestException as exc:
            logger.error("OTX query error: %s", exc)
        return None

    def _query_urlhaus(self, target: str) -> Optional[dict]:
        try:
            resp = self.session.post(URLHAUS_API_URL, data={"host": target}, timeout=15)
            if resp.status_code == 200:
                return resp.json()
        except requests.exceptions.RequestException as exc:
            logger.error("URLhaus query error: %s", exc)
        return None

    def execute_scan(self, target: str) -> ThreatIntelReport:
        logger.info("Aggregating threat intel for: %s", target)
        report = ThreatIntelReport(target=target)

        # 1. AlienVault OTX
        otx_data = self._query_otx(target)
        if otx_data:
            pulse_info = otx_data.get("pulse_info", {})
            pulses = pulse_info.get("pulses", [])
            pulse_count = len(pulses)
            tags = ",".join(set([t for p in pulses for t in p.get("tags", [])]))
            
            record = IoCRecord(
                indicator=target,
                indicator_type="IPv4",
                source="otx.alienvault.com",
                pulse_count=pulse_count,
                threat_score=min(pulse_count / 10.0, 1.0),
                tags=tags[:1000]
            )
            report.iocs.append(record)

        # 2. URLhaus
        uh_data = self._query_urlhaus(target)
        if uh_data and uh_data.get("query_status") == "ok":
            url_count = uh_data.get("url_count", 0)
            record = IoCRecord(
                indicator=target,
                indicator_type="URL/Host",
                source="urlhaus-api.abuse.ch",
                pulse_count=url_count,
                threat_score=1.0 if url_count > 0 else 0.0,
                tags=f"blacklisted_urls:{url_count}"
            )
            report.iocs.append(record)

        # Persist
        try:
            with sqlite3.connect(self.db_path) as conn:
                for rec in report.iocs:
                    snap_blob = f"{rec.indicator}:{rec.source}:{rec.pulse_count}"
                    conn.execute(
                        """INSERT OR IGNORE INTO threat_intel_feed
                           (indicator, indicator_type, source, pulse_count, threat_score, tags, data_hash)
                           VALUES (?,?,?,?,?,?,?)""",
                        (rec.indicator, rec.indicator_type, rec.source, rec.pulse_count, 
                         rec.threat_score, rec.tags, self._hash(snap_blob)),
                    )
                conn.commit()
            logger.info("Persisted %d intelligence records", len(report.iocs))
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)
            report.errors.append(str(exc))

        return report

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 73_THREAT_INTEL_FEED_synthesized_agent.py <target_ip>")
        sys.exit(1)

    agent = ThreatIntelFeedAgent()
    result = agent.execute_scan(sys.argv[1])
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
