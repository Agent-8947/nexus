#!/usr/bin/env python3
"""
NEXUS DNA OSINT Agent: TECHNOLOGY_PROFILER
Tier: S-Target (Production-Hardened)
Spec Hash: 7b36088d1412a0ea

Detect web technologies, frameworks, and CMS used by a target website via Wappalyzer logic.
"""

import json
import logging
import sqlite3
import hashlib
import sys
import time
import re
from dataclasses import dataclass, field, asdict
from typing import Optional, List

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("TECHNOLOGY_PROFILER")

MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

@dataclass
class TechRecord:
    target_url: str
    technology: str
    category: str
    version: str = ""
    confidence: int = 100

@dataclass
class TechProfileReport:
    target_url: str
    technologies: List[TechRecord] = field(default_factory=list)
    scanned_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    errors: List[str] = field(default_factory=list)

class TechnologyProfilerAgent:
    """Agent for HTTP header + HTML meta + script fingerprinting of web techs."""
    
    def __init__(self, db_path: str = "nexus_osint.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NEXUS-OSINT/1.0"})
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS technology_profiler (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        target_url TEXT NOT NULL,
                        technology TEXT,
                        category TEXT,
                        version TEXT,
                        confidence INTEGER,
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

    def _analyze_headers(self, headers: dict) -> List[TechRecord]:
        found = []
        # X-Powered-By check
        powered_by = headers.get("X-Powered-By", "")
        if powered_by:
            found.append(TechRecord(target_url="", technology=powered_by, category="Backend Framework"))
        
        server = headers.get("Server", "")
        if server:
            found.append(TechRecord(target_url="", technology=server, category="Web Server"))
            
        return found

    def _analyze_body(self, html: str) -> List[TechRecord]:
        found = []
        # Meta generator check
        match = re.search(r'<meta name="generator" content="([^"]+)"', html, re.I)
        if match:
            found.append(TechRecord(target_url="", technology=match.group(1), category="CMS"))
        
        # Script tags for frameworks
        if "wp-content" in html:
            found.append(TechRecord(target_url="", technology="WordPress", category="CMS"))
        if "react" in html.lower():
            found.append(TechRecord(target_url="", technology="React", category="Frontend Framework"))
        if "jquery" in html.lower():
            found.append(TechRecord(target_url="", technology="jQuery", category="JavaScript Library"))
            
        return found

    def execute_scan(self, url: str) -> TechProfileReport:
        if not url.startswith("http"):
            url = f"http://{url}"
            
        logger.info("Profiling web technology for target: %s", url)
        report = TechProfileReport(target_url=url)

        try:
            resp = self.session.get(url, timeout=15)
            # Analyze headers
            report.technologies.extend(self._analyze_headers(resp.headers))
            # Analyze HTML
            report.technologies.extend(self._analyze_body(resp.text))
            
            # Persist
            with sqlite3.connect(self.db_path) as conn:
                for tech in report.technologies:
                    tech.target_url = url
                    snap_blob = f"{url}:{tech.technology}"
                    conn.execute(
                        """INSERT OR IGNORE INTO technology_profiler
                           (target_url, technology, category, version, confidence, data_hash)
                           VALUES (?,?,?,?,?,?)""",
                        (url, tech.technology, tech.category, tech.version, 
                         tech.confidence, self._hash(snap_blob)),
                    )
                conn.commit()
            logger.info("Detected %d technologies for %s", len(report.technologies), url)
            
        except Exception as exc:
            logger.error("Scan failed for %s: %s", url, exc)
            report.errors.append(str(exc))

        return report

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 75_TECHNOLOGY_PROFILER_synthesized_agent.py <url>")
        sys.exit(1)

    agent = TechnologyProfilerAgent()
    result = agent.execute_scan(sys.argv[1])
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
