#!/usr/bin/env python3
"""
CRAWL4AI__X__METASPLOIT [NEXUS SYNTHESIZED Gen-1]
Mission: Web Vulnerability Surface Reconnaissance Agent
Heritage: CRAWL4AI (web crawling/scraping) + METASPLOIT (vulnerability exploitation)
Role: collector | Security: high | Interface: cli | Domains: web & security

This agent crawls a target website, extracts technology fingerprints,
discovers exposed endpoints, and maps them to known CVE/exploit vectors.
It does NOT attack — it produces an intelligence report for human review.
"""

import sys
import os
import re
import json
import socket
import hashlib
import logging
import argparse
import urllib.request
import urllib.error
import ssl
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

__all__ = ["main", "WebReconAgent"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("CRAWL4AI_x_METASPLOIT")

# ── Technology Fingerprint Database ──────────────────────────────────────
# Maps HTTP headers, meta tags, and URL patterns to known technologies
TECH_SIGNATURES: Dict[str, Dict[str, str]] = {
    "headers": {
        "X-Powered-By": "server_framework",
        "Server": "web_server",
        "X-AspNet-Version": "aspnet",
        "X-Generator": "cms_generator",
        "X-Drupal-Cache": "drupal",
    },
    "body_patterns": {
        r"wp-content/|wp-includes/": "WordPress",
        r"Joomla!|/components/com_": "Joomla",
        r"drupal\.js|Drupal\.settings": "Drupal",
        r"Laravel|laravel_session": "Laravel",
        r"__next|_next/static": "Next.js",
        r"flask|Werkzeug": "Flask/Werkzeug",
        r"django|csrfmiddlewaretoken": "Django",
        r"phpmyadmin|phpMyAdmin": "phpMyAdmin",
        r"tomcat|Apache Tomcat": "Apache Tomcat",
        r"elasticsearch|kibana": "Elastic Stack",
    },
    "url_patterns": {
        r"/wp-admin|/wp-login\.php": "WordPress Admin",
        r"/administrator/|/admin/": "Admin Panel",
        r"/phpmyadmin/": "phpMyAdmin",
        r"/api/|/v[0-9]+/": "REST API Endpoint",
        r"\.env|\.git/|\.svn/": "Exposed Config",
        r"/swagger|/api-docs": "API Documentation",
        r"/graphql": "GraphQL Endpoint",
        r"/actuator|/health|/metrics": "Spring Boot Actuator",
        r"/server-status|/server-info": "Apache Status",
        r"/elmah\.axd|/trace\.axd": "ASP.NET Debug",
    },
}

# ── Known Vulnerability Mappings ─────────────────────────────────────────
# Maps detected tech → known CVE classes (for reporting, NOT exploitation)
VULN_INTEL: Dict[str, List[Dict[str, str]]] = {
    "WordPress": [
        {"cve_class": "CVE-2024-*", "risk": "HIGH", "vector": "Plugin RCE via XML-RPC"},
        {"cve_class": "CVE-2023-*", "risk": "MEDIUM", "vector": "SQLi in wp-comments"},
    ],
    "phpMyAdmin": [
        {"cve_class": "CVE-2023-*", "risk": "CRITICAL", "vector": "Auth bypass + RCE"},
    ],
    "Apache Tomcat": [
        {"cve_class": "CVE-2024-*", "risk": "HIGH", "vector": "GhostCat / AJP file read"},
    ],
    "Spring Boot Actuator": [
        {"cve_class": "CVE-2022-22965", "risk": "CRITICAL", "vector": "Spring4Shell RCE"},
    ],
    "Exposed Config": [
        {"cve_class": "CWE-200", "risk": "CRITICAL", "vector": "Credential leakage via .env/.git"},
    ],
    "Django": [
        {"cve_class": "CVE-2024-*", "risk": "MEDIUM", "vector": "DEBUG=True info disclosure"},
    ],
    "Elastic Stack": [
        {"cve_class": "CVE-2021-*", "risk": "HIGH", "vector": "Unauthenticated data access"},
    ],
}


@dataclass
class Finding:
    """Single reconnaissance finding."""
    category: str          # tech_fingerprint | exposed_endpoint | vuln_intel
    target: str            # URL or IP
    detail: str            # What was found
    severity: str          # CRITICAL | HIGH | MEDIUM | LOW | INFO
    evidence: str = ""     # Raw evidence (header value, matched pattern)
    cve_ref: str = ""      # CVE reference if applicable
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class LinkExtractor(HTMLParser):
    """Extract all href links from HTML."""
    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.links: List[str] = []

    def handle_starttag(self, tag: str, attrs: list):
        if tag in ("a", "link", "script", "img", "form"):
            for name, value in attrs:
                if name in ("href", "src", "action") and value:
                    full_url = urljoin(self.base_url, value)
                    if full_url.startswith(("http://", "https://")):
                        self.links.append(full_url)


class WebReconAgent:
    """Crawls target, fingerprints tech stack, maps to vulnerability intel."""

    def __init__(self, max_pages: int = 20, timeout: int = 10):
        self.max_pages = max_pages
        self.timeout = timeout
        self.visited: set = set()
        self.findings: List[Finding] = []
        self.stats = {"pages_crawled": 0, "techs_found": 0, "vulns_mapped": 0, "errors": 0}
        self._ctx = ssl.create_default_context()
        self._ctx.check_hostname = False
        self._ctx.verify_mode = ssl.CERT_NONE

    def _fetch(self, url: str) -> tuple[Optional[str], Dict[str, str]]:
        """Fetch URL content and headers."""
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (NEXUS-Recon/1.0; +nexus-security-audit)",
                "Accept": "text/html,application/xhtml+xml,*/*",
            })
            with urllib.request.urlopen(req, timeout=self.timeout, context=self._ctx) as resp:
                headers = {k: v for k, v in resp.getheaders()}
                body = resp.read().decode("utf-8", errors="ignore")
                return body, headers
        except Exception as e:
            self.stats["errors"] += 1
            logger.debug(f"Fetch failed: {url} — {e}")
            return None, {}

    def _fingerprint_headers(self, url: str, headers: Dict[str, str]):
        """Extract technology signatures from HTTP response headers."""
        for header_name, tech_label in TECH_SIGNATURES["headers"].items():
            value = headers.get(header_name, "")
            if value:
                self.findings.append(Finding(
                    category="tech_fingerprint",
                    target=url,
                    detail=f"{tech_label}: {value}",
                    severity="INFO",
                    evidence=f"{header_name}: {value}",
                ))
                self.stats["techs_found"] += 1

    def _fingerprint_body(self, url: str, body: str):
        """Scan HTML body for technology patterns."""
        for pattern, tech_name in TECH_SIGNATURES["body_patterns"].items():
            if re.search(pattern, body, re.IGNORECASE):
                self.findings.append(Finding(
                    category="tech_fingerprint",
                    target=url,
                    detail=f"Detected: {tech_name}",
                    severity="MEDIUM",
                    evidence=f"Pattern: {pattern}",
                ))
                self.stats["techs_found"] += 1
                self._map_vulns(url, tech_name)

    def _check_exposed_endpoints(self, url: str):
        """Check if URL matches known sensitive endpoint patterns."""
        for pattern, endpoint_type in TECH_SIGNATURES["url_patterns"].items():
            if re.search(pattern, url, re.IGNORECASE):
                severity = "CRITICAL" if "Config" in endpoint_type or "Admin" in endpoint_type else "HIGH"
                self.findings.append(Finding(
                    category="exposed_endpoint",
                    target=url,
                    detail=f"Exposed: {endpoint_type}",
                    severity=severity,
                    evidence=f"URL matched: {pattern}",
                ))

    def _map_vulns(self, url: str, tech_name: str):
        """Map detected technology to known vulnerability intelligence."""
        vulns = VULN_INTEL.get(tech_name, [])
        for vuln in vulns:
            self.findings.append(Finding(
                category="vuln_intel",
                target=url,
                detail=f"{tech_name} → {vuln['vector']}",
                severity=vuln["risk"],
                cve_ref=vuln["cve_class"],
            ))
            self.stats["vulns_mapped"] += 1

    def _dns_resolve(self, hostname: str) -> Optional[str]:
        """Resolve hostname to IP."""
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            return None

    def crawl(self, start_url: str) -> List[Finding]:
        """Main crawl loop with BFS link following."""
        logger.info(f"[RECON] Starting: {start_url} (max {self.max_pages} pages)")

        parsed = urlparse(start_url)
        target_domain = parsed.netloc
        ip = self._dns_resolve(parsed.hostname or "")
        if ip:
            self.findings.append(Finding(
                category="tech_fingerprint",
                target=start_url,
                detail=f"Resolved IP: {ip}",
                severity="INFO",
                evidence=f"DNS A record: {parsed.hostname} → {ip}",
            ))

        queue = [start_url]
        while queue and self.stats["pages_crawled"] < self.max_pages:
            url = queue.pop(0)
            url_hash = hashlib.md5(url.encode()).hexdigest()
            if url_hash in self.visited:
                continue
            self.visited.add(url_hash)

            self._check_exposed_endpoints(url)
            body, headers = self._fetch(url)
            if body is None:
                continue

            self.stats["pages_crawled"] += 1
            self._fingerprint_headers(url, headers)
            self._fingerprint_body(url, body)

            # Extract & enqueue same-domain links
            try:
                extractor = LinkExtractor(url)
                extractor.feed(body)
                for link in extractor.links:
                    link_parsed = urlparse(link)
                    if link_parsed.netloc == target_domain:
                        queue.append(link)
            except Exception:
                pass

            logger.info(f"  [{self.stats['pages_crawled']}/{self.max_pages}] {url[:80]}...")

        logger.info(f"[DONE] {self.stats['pages_crawled']} pages, "
                     f"{self.stats['techs_found']} techs, "
                     f"{self.stats['vulns_mapped']} vuln mappings")
        return self.findings


def main():
    parser = argparse.ArgumentParser(
        description="CRAWL4AI x METASPLOIT — Web Vulnerability Surface Recon Agent"
    )
    parser.add_argument("--target", required=True, help="Target URL (e.g. https://example.com)")
    parser.add_argument("--max-pages", type=int, default=20, help="Max pages to crawl (default: 20)")
    parser.add_argument("--timeout", type=int, default=10, help="HTTP timeout in seconds")
    parser.add_argument("--output", default="recon_report.json", help="Output JSON report path")
    args = parser.parse_args()

    agent = WebReconAgent(max_pages=args.max_pages, timeout=args.timeout)
    findings = agent.crawl(args.target)

    # Deduplicate findings by (category, target, detail)
    seen = set()
    unique_findings = []
    for f in findings:
        key = (f.category, f.target, f.detail)
        if key not in seen:
            seen.add(key)
            unique_findings.append(f)

    report = {
        "agent": "CRAWL4AI__X__METASPLOIT",
        "version": "1.0-gen1",
        "mission": "Web Vulnerability Surface Reconnaissance",
        "timestamp": datetime.now().isoformat(),
        "target": args.target,
        "stats": agent.stats,
        "risk_summary": {
            "CRITICAL": sum(1 for f in unique_findings if f.severity == "CRITICAL"),
            "HIGH": sum(1 for f in unique_findings if f.severity == "HIGH"),
            "MEDIUM": sum(1 for f in unique_findings if f.severity == "MEDIUM"),
            "LOW": sum(1 for f in unique_findings if f.severity == "LOW"),
            "INFO": sum(1 for f in unique_findings if f.severity == "INFO"),
        },
        "findings": [
            {
                "category": f.category,
                "target": f.target,
                "detail": f.detail,
                "severity": f.severity,
                "evidence": f.evidence,
                "cve_ref": f.cve_ref,
                "timestamp": f.timestamp,
            }
            for f in sorted(unique_findings, key=lambda x: {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}.get(x.severity, 5))
        ],
    }

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info(f"[REPORT] {len(unique_findings)} findings → {output}")

    # Print top critical findings to console
    crits = [f for f in unique_findings if f.severity in ("CRITICAL", "HIGH")]
    if crits:
        print(f"\n{'='*60}")
        print(f"⚠ TOP {len(crits)} CRITICAL/HIGH FINDINGS:")
        print(f"{'='*60}")
        for f in crits[:10]:
            print(f"  [{f.severity}] {f.detail}")
            if f.cve_ref:
                print(f"         CVE: {f.cve_ref}")
            print(f"         URL: {f.target}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
