#!/usr/bin/env python3
"""
NEXUS DNA AI Agent: HF_MODEL_METADATA_SCRAPER
Tier: A-Target (Production-Hardened)
Spec Hash: 48465f4d4f44454c

Fetch metadata, architectures, and performance metrics from HuggingFace.
"""

import json
import logging
import requests
import sqlite3
import hashlib
import sys
import time
from dataclasses import dataclass, field, asdict
from typing import List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("HF_MODEL_METADATA_SCRAPER")

HF_API_URL = "https://huggingface.co/api/models/{model_id}"
MAX_RETRIES = 3
RETRY_BACKOFF = 3.0

@dataclass
class HfModelRecord:
    model_id: str
    architecture: str
    downloads: int
    likes: int
    tags: str

@dataclass
class HfScraperReport:
    model_id: str
    record: Optional[HfModelRecord] = None
    scanned_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    errors: List[str] = field(default_factory=list)

class HfModelMetadataScraperAgent:
    def __init__(self, db_path: str = "nexus_ai_ml.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NEXUS-AI/1.0"})
        self._init_storage()

    def _init_storage(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""CREATE TABLE IF NOT EXISTS hf_model_metadata 
                                (id INTEGER PRIMARY KEY, model_id TEXT, architecture TEXT, downloads INTEGER, likes INTEGER, tags TEXT, data_hash TEXT UNIQUE, ts DATETIME DEFAULT CURRENT_TIMESTAMP)""")
                conn.commit()
            logger.info("Storage ready.")
        except sqlite3.Error as exc:
            logger.critical("DB init failed: %s", exc)
            raise SystemExit(1) from exc

    @staticmethod
    def _hash(payload: str) -> str:
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def execute_scan(self, model_id: str) -> HfScraperReport:
        logger.info("Scraping HF metadata for: %s", model_id)
        report = HfScraperReport(model_id=model_id)
        
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self.session.get(HF_API_URL.format(model_id=model_id), timeout=15)
                resp.raise_for_status()
                
                data = resp.json()
                archs = data.get("config", {}).get("architectures", ["unknown"])
                arch_str = archs[0] if archs else "unknown"
                
                record = HfModelRecord(
                    model_id=data.get("id"),
                    architecture=arch_str,
                    downloads=data.get("downloads", 0),
                    likes=data.get("likes", 0),
                    tags=",".join(data.get("tags", [])[:10])
                )
                report.record = record
                self._persist(record)
                break
                
            except Exception as e:
                logger.error("HF API error on attempt %d: %s", attempt, e)
                time.sleep(attempt * RETRY_BACKOFF)
                if attempt == MAX_RETRIES:
                    report.errors.append(str(e))
                    
        return report

    def _persist(self, m: HfModelRecord) -> None:
        h = self._hash(f"{m.model_id}:{m.downloads}:{m.likes}")
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT OR IGNORE INTO hf_model_metadata (model_id, architecture, downloads, likes, tags, data_hash) VALUES (?,?,?,?,?,?)",
                             (m.model_id, m.architecture, m.downloads, m.likes, m.tags, h))
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)

if __name__ == "__main__":
    if len(sys.argv) < 2: 
        print("Usage: python 25_HF_MODEL_METADATA_SCRAPER_synthesized_agent.py <model_id>")
        sys.exit(1)
    print(json.dumps(asdict(HfModelMetadataScraperAgent().execute_scan(sys.argv[1])), indent=2))
