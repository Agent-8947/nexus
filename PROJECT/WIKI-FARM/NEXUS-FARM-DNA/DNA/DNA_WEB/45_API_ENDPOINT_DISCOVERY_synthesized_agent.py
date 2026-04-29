#!/usr/bin/env python3
"""
NEXUS DNA Web Agent: API_ENDPOINT_DISCOVERY
Tier: S-Target (Production-Hardened)
Spec Hash: 4150495f454e4450

Advanced logic for identifying hidden internal API endpoints within JS bundles.
Multi-Phase Execution: Recon (fetch JS) -> Analyze (Regex + Pattern Mapping) -> Validate (Probe endpoints).
"""

import re
import json
import logging
import sqlite3
import hashlib
import sys
import time
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass, field, asdict
from typing import List, Optional

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("API_ENDPOINT_DISCOVERY")

MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

@dataclass
class ApiDiscoveryRecord:
    api_url: str
    method_hint: str
    js_file: str
    is_live: int

@dataclass
class ApiDiscoveryReport:
    page_url: str
    discovered_endpoints: List[ApiDiscoveryRecord] = field(default_factory=list)
    scanned_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    errors: List[str] = field(default_factory=list)

class ApiEndpointDiscoveryAgent:
    def __init__(self, db_path: str = "nexus_web.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NEXUS/WEB-1.0",
            "Accept": "*/*"
        })
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""CREATE TABLE IF NOT EXISTS api_endpoint_discovery 
                                (id INTEGER PRIMARY KEY, page_url TEXT, api_url TEXT, method_hint TEXT, js_file TEXT, is_live INTEGER, data_hash TEXT UNIQUE, ts DATETIME DEFAULT CURRENT_TIMESTAMP)""")
                conn.commit()
            logger.info("Storage ready.")
        except sqlite3.Error as exc:
            logger.critical("DB init failed: %s", exc)
            raise SystemExit(1) from exc

    @staticmethod
    def _hash(payload: str) -> str:
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def _recon_extract_js_links(self, page_url: str) -> List[str]:
        """Phase 1: Fetch HTML and extract all referenced script sources."""
        js_links = set()
        try:
            resp = self.session.get(page_url, timeout=15)
            resp.raise_for_status()
            
            # Find script src attributes
            srcs = re.findall(r'<script[^>]+src=["\']([^"\']+\.js[^"\']*)["\']', resp.text, re.IGNORECASE)
            for src in srcs:
                full_url = urljoin(page_url, src)
                js_links.add(full_url)
                
            logger.info("Recon: Discovered %d JS files referenced on page.", len(js_links))
        except Exception as e:
            logger.error("Recon failed: %s", e)
        return list(js_links)

    def _analyze_js_for_endpoints(self, js_url: str) -> List[dict]:
        """Phase 2: Download JS blob and analyze for API patterns."""
        endpoints = []
        try:
            resp = self.session.get(js_url, timeout=15)
            if resp.status_code != 200:
                return endpoints
                
            js_content = resp.text
            
            # Logic markers: /api/v1/, /api/v2/, fetch(, axios.
            path_pattern = re.compile(r'["\'](/api/v[12]/[^"\']+)["\']', re.IGNORECASE)
            fetch_pattern = re.compile(r'(?:fetch|axios\.(?:get|post|put|delete))\s*\(\s*["\']([^"\']+)["\']', re.IGNORECASE)
            
            for path in path_pattern.findall(js_content):
                endpoints.append({"path": path, "method": "UNKNOWN"})
                
            for fetch_path in fetch_pattern.findall(js_content):
                # Try to infer method by nearby Axios calls
                method = "GET"
                if "axios.post" in js_content:
                    method = "POST" 
                endpoints.append({"path": fetch_path, "method": method})
                
        except Exception as e:
            logger.warning("Analyze failed for %s: %s", js_url, e)
            
        return endpoints

    def _validate_endpoint_alive(self, base_url: str, path: str) -> int:
        """Phase 3: Active validation - ping endpoint to see if it routes."""
        full_url = urljoin(base_url, path)
        try:
            # We use an OPTIONS request to avoid triggering actions while checking if path exists
            resp = self.session.options(full_url, timeout=5)
            if resp.status_code in (200, 204, 401, 403, 405, 500):
                return 1 # Exists but might be protected or require POST
        except:
            pass
        return 0

    def execute_scan(self, target_url: str) -> ApiDiscoveryReport:
        logger.info("Initiating API Discovery Scan on: %s", target_url)
        report = ApiDiscoveryReport(page_url=target_url)
        
        parsed = urlparse(target_url)
        base_domain = f"{parsed.scheme}://{parsed.netloc}"
        
        js_files = self._recon_extract_js_links(target_url)
        if not js_files:
            report.errors.append("No JS files found during recon.")
            return report
            
        for js_file in js_files:
            potential_endpoints = self._analyze_js_for_endpoints(js_file)
            
            for ep in potential_endpoints:
                path = ep["path"]
                is_alive = self._validate_endpoint_alive(base_domain, path)
                
                full_api_route = urljoin(base_domain, path) if not path.startswith("http") else path
                
                record = ApiDiscoveryRecord(
                    api_url=full_api_route,
                    method_hint=ep["method"],
                    js_file=js_file,
                    is_live=is_alive
                )
                
                report.discovered_endpoints.append(record)
                self._persist(target_url, record)
                
        return report

    def _persist(self, url: str, m: ApiDiscoveryRecord) -> None:
        h = self._hash(f"{url}:{m.api_url}:{m.js_file}")
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT OR IGNORE INTO api_endpoint_discovery (page_url, api_url, method_hint, js_file, is_live, data_hash) VALUES (?,?,?,?,?,?)",
                             (url, m.api_url, m.method_hint, m.js_file, m.is_live, h))
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)

if __name__ == "__main__":
    if len(sys.argv) < 2: 
        print("Usage: python API_ENDPOINT_DISCOVERY_synthesized_agent.py <target_page_url>")
        sys.exit(1)
        
    url = sys.argv[1]
    if not url.startswith("http"):
        url = "https://" + url
        
    print(json.dumps(asdict(ApiEndpointDiscoveryAgent().execute_scan(url)), indent=2))
