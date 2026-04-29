#!/usr/bin/env python3
"""
NEXUS DNA OSINT Agent: DARKWEB_MARKET_MONITOR
Tier: S-Target (Production-Hardened)

Monitors .onion services via Ahmia.fi clearnet search API.
Tracks keyword mentions, indexes results, and alerts on new findings.
No Tor required — uses Ahmia's public clearnet endpoint.
"""

import json
import logging
import sqlite3
import hashlib
import sys
import time
from dataclasses import dataclass, field, asdict
from typing import Optional
from urllib.parse import quote_plus

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("DARKWEB_MARKET_MONITOR")

AHMIA_SEARCH_URL = "https://ahmia.fi/search/"
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0


@dataclass
class DarkwebResult:
    title: str
    url: str
    snippet: str
    content_hash: str


@dataclass
class DarkwebReport:
    keyword: str
    total_results: int = 0
    new_findings: int = 0
    results: list[DarkwebResult] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class DarkwebMarketMonitorAgent:
    """Monitor darkweb mentions via Ahmia.fi clearnet search."""

    def __init__(self, db_path: str = "nexus_osint.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NEXUS-OSINT/1.0"})
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS darkweb_mentions (
                        id           INTEGER PRIMARY KEY AUTOINCREMENT,
                        keyword      TEXT NOT NULL,
                        title        TEXT,
                        url          TEXT NOT NULL,
                        snippet      TEXT,
                        content_hash TEXT NOT NULL,
                        ts           DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(content_hash)
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

    def _search_ahmia(self, keyword: str) -> Optional[str]:
        """Fetch search results HTML from Ahmia clearnet endpoint."""
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self.session.get(
                    AHMIA_SEARCH_URL,
                    params={"q": keyword},
                    timeout=20,
                )
                if resp.status_code == 429:
                    wait = RETRY_BACKOFF * attempt
                    logger.warning("Rate-limited, backing off %.1fs", wait)
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                return resp.text
            except requests.exceptions.Timeout:
                logger.warning("Timeout attempt %d/%d", attempt, MAX_RETRIES)
                time.sleep(RETRY_BACKOFF * attempt)
            except requests.exceptions.RequestException as exc:
                logger.error("Network error: %s", exc)
                time.sleep(RETRY_BACKOFF * attempt)
        return None

    @staticmethod
    def _parse_results(html: str) -> list[dict]:
        """Parse Ahmia search results from HTML without BeautifulSoup.
        Uses simple string parsing for zero-dependency operation."""
        results = []
        search_marker = 'class="result"'
        chunks = html.split(search_marker)

        for chunk in chunks[1:]:  # skip pre-results content
            title = ""
            url = ""
            snippet = ""

            # Extract href
            href_start = chunk.find('href="')
            if href_start != -1:
                href_start += 6
                href_end = chunk.find('"', href_start)
                url = chunk[href_start:href_end]

            # Extract title (text inside first <a>)
            a_close = chunk.find(">", href_start) if href_start != -1 else -1
            if a_close != -1:
                a_end = chunk.find("</a>", a_close)
                if a_end != -1:
                    title = chunk[a_close + 1:a_end].strip()

            # Extract snippet (text inside <p>)
            p_start = chunk.find("<p>")
            if p_start != -1:
                p_end = chunk.find("</p>", p_start)
                if p_end != -1:
                    snippet = chunk[p_start + 3:p_end].strip()

            if url:
                results.append({"title": title, "url": url, "snippet": snippet})

        return results

    def execute_scan(self, keyword: str) -> DarkwebReport:
        logger.info("Searching darkweb for keyword: %s", keyword)
        report = DarkwebReport(keyword=keyword)

        html = self._search_ahmia(keyword)
        if html is None:
            report.errors.append("Failed to fetch Ahmia results")
            return report

        parsed = self._parse_results(html)
        report.total_results = len(parsed)
        logger.info("Found %d results for '%s'", len(parsed), keyword)

        try:
            with sqlite3.connect(self.db_path) as conn:
                for item in parsed:
                    content = f"{item['url']}:{item['title']}"
                    h = self._hash(content)
                    rec = DarkwebResult(
                        title=item["title"],
                        url=item["url"],
                        snippet=item["snippet"],
                        content_hash=h,
                    )
                    report.results.append(rec)
                    try:
                        conn.execute(
                            """INSERT INTO darkweb_mentions
                               (keyword, title, url, snippet, content_hash)
                               VALUES (?,?,?,?,?)""",
                            (keyword, rec.title, rec.url, rec.snippet, h),
                        )
                        report.new_findings += 1
                    except sqlite3.IntegrityError:
                        pass  # already seen
                conn.commit()
            logger.info("New findings: %d / %d total", report.new_findings, report.total_results)
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)
            report.errors.append(str(exc))

        return report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 62_DARKWEB_MARKET_MONITOR_synthesized_agent.py <keyword>")
        sys.exit(1)

    agent = DarkwebMarketMonitorAgent()
    result = agent.execute_scan(sys.argv[1])
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
