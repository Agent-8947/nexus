#!/usr/bin/env python3
"""
NEXUS DNA Web Agent: BROKEN_IMAGE_HUNTER
Tier: A-Target (Production-Hardened)
Spec Hash: 42524f4b454e5f49

Scan page HTML for broken <img> tags.
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
logger = logging.getLogger("BROKEN_IMAGE_HUNTER")

MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

@dataclass
class BrokenImageRecord:
    src: str
    status: int
    error: str

@dataclass
class BrokenImageReport:
    page_url: str
    img_count: int = 0
    broken_images: List[BrokenImageRecord] = field(default_factory=list)
    scanned_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    errors: List[str] = field(default_factory=list)

class BrokenImageHunterAgent:
    def __init__(self, db_path: str = "nexus_web.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NEXUS-WEB/1.0"})
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""CREATE TABLE IF NOT EXISTS broken_image_hunter 
                                (id INTEGER PRIMARY KEY, page_url TEXT, src TEXT, status INTEGER, error TEXT, data_hash TEXT UNIQUE, ts DATETIME DEFAULT CURRENT_TIMESTAMP)""")
                conn.commit()
            logger.info("Storage ready.")
        except sqlite3.Error as exc:
            logger.critical("DB init failed: %s", exc)
            raise SystemExit(1) from exc

    @staticmethod
    def _hash(payload: str) -> str:
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def execute_scan(self, url: str) -> BrokenImageReport:
        logger.info("Hunting broken images on %s", url)
        report = BrokenImageReport(page_url=url)
        
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self.session.get(url, timeout=10)
                resp.raise_for_status()
                img_srcs = re.findall(r'<img [^>]*src="([^"]+)"', resp.text)
                
                report.img_count = len(img_srcs)
                logger.info("Found %d images. Validating...", len(img_srcs))
                
                for src in img_srcs:
                    full_src = src if src.startswith("http") else f"{url.rstrip('/')}/{src.lstrip('/')}"
                    try:
                        head = self.session.head(full_src, timeout=5)
                        if head.status_code >= 400:
                            record = BrokenImageRecord(src=src, status=head.status_code, error="")
                            report.broken_images.append(record)
                            self._persist(url, record)
                    except Exception as e:
                        record = BrokenImageRecord(src=src, status=0, error="Unreachable")
                        report.broken_images.append(record)
                        self._persist(url, record)
                break
            except Exception as e:
                logger.error("Failed to crawl page on attempt %d: %s", attempt, e)
                time.sleep(attempt * RETRY_BACKOFF)
                if attempt == MAX_RETRIES:
                    report.errors.append(f"Crawl failed: {e}")
                    
        return report

    def _persist(self, url: str, m: BrokenImageRecord) -> None:
        h = self._hash(f"{url}:{m.src}")
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT OR IGNORE INTO broken_image_hunter (page_url, src, status, error, data_hash) VALUES (?,?,?,?,?)",
                             (url, m.src, m.status, m.error, h))
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)

if __name__ == "__main__":
    if len(sys.argv) < 2: 
        print("Usage: python 42_BROKEN_IMAGE_HUNTER_synthesized_agent.py <url>")
        sys.exit(1)
    print(json.dumps(asdict(BrokenImageHunterAgent().execute_scan(sys.argv[1])), indent=2))
