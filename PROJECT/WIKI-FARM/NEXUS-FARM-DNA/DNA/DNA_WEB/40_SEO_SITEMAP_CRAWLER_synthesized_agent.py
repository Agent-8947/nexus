#!/usr/bin/env python3
"""
NEXUS DNA Web Agent: SEO_SITEMAP_CRAWLER
Tier: A-Target (Production-Hardened)
Spec Hash: 53454f5f53495445

Crawl website sitemaps and audit for status codes and structure.
"""

import xml.etree.ElementTree as ET
import logging
import requests
import json
import sqlite3
import hashlib
import sys
import time
from dataclasses import dataclass, field, asdict
from typing import List

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("SEO_SITEMAP_CRAWLER")

MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

@dataclass
class SitemapUrlRecord:
    url: str
    status_code: int
    is_broken: int

@dataclass
class SitemapCrawlerReport:
    sitemap_url: str
    total_urls: int = 0
    checks: List[SitemapUrlRecord] = field(default_factory=list)
    scanned_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    errors: List[str] = field(default_factory=list)

class SeoSitemapCrawlerAgent:
    """Agent to crawl sitemap XML and check link health."""
    
    def __init__(self, db_path: str = "nexus_web.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NEXUS-WEB/1.0"})
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS seo_sitemap_urls (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sitemap_url TEXT NOT NULL,
                        url TEXT NOT NULL,
                        status_code INTEGER,
                        is_broken INTEGER,
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

    def execute_audit(self, sitemap_url: str) -> SitemapCrawlerReport:
        logger.info("Crawling sitemap: %s", sitemap_url)
        report = SitemapCrawlerReport(sitemap_url=sitemap_url)
        
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self.session.get(sitemap_url, timeout=20)
                resp.raise_for_status()
                root = ET.fromstring(resp.content)
                ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
                urls = [loc.text for loc in root.findall('.//ns:loc', ns)]
                
                report.total_urls = len(urls)
                logger.info("Found %d URLs. Sampling up to 10...", len(urls))
                
                for url in urls[:10]: # Sample check
                    try:
                        sub_resp = self.session.head(url, timeout=5)
                        is_broken = 1 if sub_resp.status_code >= 400 else 0
                        rec = SitemapUrlRecord(url=url, status_code=sub_resp.status_code, is_broken=is_broken)
                        report.checks.append(rec)
                        
                        with sqlite3.connect(self.db_path) as conn:
                            snap_blob = f"{sitemap_url}:{url}:{sub_resp.status_code}"
                            conn.execute(
                                """INSERT OR IGNORE INTO seo_sitemap_urls
                                   (sitemap_url, url, status_code, is_broken, data_hash)
                                   VALUES (?,?,?,?,?)""",
                                (sitemap_url, url, sub_resp.status_code, is_broken, self._hash(snap_blob)),
                            )
                            conn.commit()
                    except requests.exceptions.RequestException as e:
                        logger.error("Failed to check url %s: %s", url, e)
                        report.errors.append(f"Broken check for {url}")
                
                return report
                
            except Exception as exc:
                logger.error("Sitemap fetch failed: %s", exc)
                time.sleep(RETRY_BACKOFF * attempt)
                if attempt == MAX_RETRIES:
                    report.errors.append(str(exc))

        return report

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 40_SEO_SITEMAP_CRAWLER_synthesized_agent.py <sitemap_url>")
        sys.exit(1)

    agent = SeoSitemapCrawlerAgent()
    result = agent.execute_audit(sys.argv[1])
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
