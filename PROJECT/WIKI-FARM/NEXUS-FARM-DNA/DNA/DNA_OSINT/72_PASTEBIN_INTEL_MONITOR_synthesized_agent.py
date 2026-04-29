#!/usr/bin/env python3
"""
NEXUS DNA OSINT Agent: PASTEBIN_INTEL_MONITOR
Tier: S-Target (Production-Hardened)
Spec Hash: ac36e2e4e6d73962

Monitor public paste services for leaked data mentioning target keywords via PSBDMP.
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
logger = logging.getLogger("PASTEBIN_INTEL_MONITOR")

PSBDMP_API_URL = "https://psbdmp.ws/api/v3/search/{query}"
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

@dataclass
class PasteRecord:
    keyword: str
    paste_id: str
    paste_url: str
    content_preview: str
    source: str = "psbdmp.ws"

@dataclass
class PastebinIntelReport:
    keyword: str
    pastes: List[PasteRecord] = field(default_factory=list)
    scanned_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    errors: List[str] = field(default_factory=list)

class PastebinIntelMonitorAgent:
    """Agent for PSBDMP paste dump search with keyword correlation."""
    
    def __init__(self, db_path: str = "nexus_osint.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NEXUS-OSINT/1.0"})
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS pastebin_intel_monitor (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        keyword TEXT NOT NULL,
                        paste_id TEXT,
                        paste_url TEXT,
                        content_preview TEXT,
                        source TEXT,
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

    def _search_pastes(self, query: str) -> Optional[dict]:
        url = PSBDMP_API_URL.format(query=query)
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self.session.get(url, timeout=20)
                if resp.status_code == 429:
                    wait = RETRY_BACKOFF * attempt
                    logger.warning("Rate-limited, waiting %ds", wait)
                    time.sleep(wait)
                    continue
                if resp.status_code == 404:
                    return {"data": []}
                resp.raise_for_status()
                return resp.json()
            except requests.exceptions.RequestException as exc:
                logger.error("PSBDMP API error: %s", exc)
                time.sleep(RETRY_BACKOFF * attempt)
        return None

    def execute_scan(self, keyword: str) -> PastebinIntelReport:
        logger.info("Searching paste dumps for: %s", keyword)
        report = PastebinIntelReport(keyword=keyword)

        data = self._search_pastes(keyword)
        if data and "data" in data:
            for item in data["data"]:
                pid = item.get("id", "")
                preview = item.get("text", "")[:200]
                record = PasteRecord(
                    keyword=keyword,
                    paste_id=pid,
                    paste_url=f"https://pastebin.com/{pid}",
                    content_preview=preview,
                )
                report.pastes.append(record)
                
                # Persist
                try:
                    with sqlite3.connect(self.db_path) as conn:
                        snap_blob = f"{keyword}:{pid}:{preview}"
                        conn.execute(
                            """INSERT OR IGNORE INTO pastebin_intel_monitor
                               (keyword, paste_id, paste_url, content_preview, source, data_hash)
                               VALUES (?,?,?,?,?,?)""",
                            (keyword, record.paste_id, record.paste_url, record.content_preview, 
                             record.source, self._hash(snap_blob)),
                        )
                        conn.commit()
                except sqlite3.Error as exc:
                    logger.error("DB error: %s", exc)
            logger.info("Fetched %d pastes from PSBDMP", len(report.pastes))
        else:
            logger.info("No pastes found or search failed")

        return report

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 72_PASTEBIN_INTEL_MONITOR_synthesized_agent.py <keyword>")
        sys.exit(1)

    agent = PastebinIntelMonitorAgent()
    result = agent.execute_scan(sys.argv[1])
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
