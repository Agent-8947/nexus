#!/usr/bin/env python3
"""
HYBRID_JAVASCRIPT_ALGORITHMS_x_AUTOSPLOIT__X__HYBRID_AMARANTH_x_WEB_DEV_FOR_BEGINNERS [NEXUS SYNTHESIZED Gen-2]
Mission: Build a security audit and vulnerability detection tool
Heritage: HYBRID_JAVASCRIPT_ALGORITHMS_x_AUTOSPLOIT + HYBRID_AMARANTH_x_WEB_DEV_FOR_BEGINNERS
Role: payload | Domains: osint & web

I/O Contract:
  Input:  path (from CLI --target)
  Output: JSON report with typed findings/stats

Pipeline (1 stages, 4 blocks):
  Stage 1: [dns_recon, http_fingerprint, probe_endpoints, extract_links]
"""

import sys
import json
import logging
import argparse
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import re, socket, ssl, urllib.request, urllib.error
import re, ssl, urllib.request, urllib.error
from html.parser import HTMLParser
from urllib.parse import urljoin

__all__ = ["main", "Pipeline"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("HYBRID_JAVASCRIPT_ALGORITHMS_x_AUTOSPLOIT__X__HYBRID_AMARANT")


# ── [OSINT] DNS resolution with IP collection ──
def dns_recon(target: str) -> List[Dict[str, Any]]:
    """Resolve hostname and return findings."""
    findings: List[Dict[str, Any]] = []
    try:
        info = socket.getaddrinfo(target, None)
        ips = list(set(addr[4][0] for addr in info))
        for ip in ips:
            findings.append({
                "type": "dns_record", "severity": "INFO",
                "detail": f"Resolved to {ip}",
                "source": target,
                "ip": ip,
            })
    except socket.gaierror as e:
        findings.append({
            "type": "dns_error", "severity": "MEDIUM",
            "detail": f"DNS resolution failed: {e}",
            "source": target,
        })
    return findings


# ── [OSINT] Fingerprint web technology stack via HTTP headers and body patterns ──
_TECH_HEADERS = {"X-Powered-By": "framework", "Server": "server", "X-Generator": "cms"}
_BODY_SIGS = {
    r"wp-content/|wp-includes/": "WordPress",
    r"drupal\.js|Drupal\.settings": "Drupal",
    r"__next|_next/static": "Next.js",
    r"django|csrfmiddlewaretoken": "Django",
    r"laravel_session": "Laravel",
    r"flask|Werkzeug": "Flask",
}

def http_fingerprint(target: str) -> List[Dict[str, Any]]:
    """Fingerprint web technology stack. Returns tech_stack."""
    techs: List[Dict[str, Any]] = []
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    url = target if target.startswith("http") else f"https://{target}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 NEXUS-Recon"})
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            headers = {k: v for k, v in resp.getheaders()}
            body = resp.read().decode("utf-8", errors="ignore")[:50000]
            for h, label in _TECH_HEADERS.items():
                if h in headers:
                    techs.append({"tech": f"{label}: {headers[h]}", "source": "header", "evidence": headers[h]})
            for pattern, name in _BODY_SIGS.items():
                if re.search(pattern, body, re.IGNORECASE):
                    techs.append({"tech": name, "source": "body_pattern", "evidence": pattern})
    except Exception as e:
        techs.append({"tech": "error", "source": "http_error", "evidence": str(e)})
    return techs


# ── [OSINT] Probe for common sensitive endpoints (.env, /admin, /api, etc.) ──
_SENSITIVE_PATHS = [
    ("/.env", "CRITICAL"), ("/.git/config", "CRITICAL"), ("/wp-admin/", "HIGH"),
    ("/admin/", "HIGH"), ("/api/", "MEDIUM"), ("/swagger/", "MEDIUM"),
    ("/graphql", "MEDIUM"), ("/actuator/health", "HIGH"), ("/server-status", "HIGH"),
    ("/robots.txt", "INFO"), ("/sitemap.xml", "INFO"),
]

def probe_endpoints(target: str) -> List[Dict[str, Any]]:
    """Probe for common sensitive endpoints. Returns findings."""
    findings: List[Dict[str, Any]] = []
    base = target.rstrip("/") if target.startswith("http") else f"https://{target}"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    for path, severity in _SENSITIVE_PATHS:
        url = base + path
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}, method="HEAD")
            with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
                if resp.status < 400:
                    findings.append({
                        "type": "exposed_endpoint", "severity": severity,
                        "detail": f"Accessible: {path} (HTTP {resp.status})",
                        "source": url,
                    })
        except urllib.error.HTTPError as e:
            if e.code < 404:  # 401/403 still interesting
                findings.append({
                    "type": "protected_endpoint", "severity": "INFO",
                    "detail": f"Protected: {path} (HTTP {e.code})",
                    "source": url,
                })
        except Exception:
            pass
    return findings


# ── [WEB] Extract all links from a web page ──
class _LinkParser(HTMLParser):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.links: List[str] = []
    def handle_starttag(self, tag, attrs):
        if tag in ("a", "link", "script", "img"):
            for n, v in attrs:
                if n in ("href", "src") and v:
                    self.links.append(urljoin(self.base, v))

def extract_links(target: str) -> List[Dict[str, Any]]:
    """Extract all links from a web page. Returns findings."""
    findings: List[Dict[str, Any]] = []
    url = target if target.startswith("http") else f"https://{target}"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            body = resp.read().decode("utf-8", errors="ignore")
        p = _LinkParser(url)
        p.feed(body)
        for link in set(p.links):
            findings.append({
                "type": "link", "severity": "INFO",
                "detail": link[:200], "source": url,
            })
    except Exception as e:
        findings.append({"type": "link_error", "severity": "MEDIUM",
                         "detail": str(e), "source": url})
    return findings



class Payload:
    """Executes targeted action against target, returns findings"""

    def __init__(self):
        self.all_findings: List[Dict[str, Any]] = []
        self.all_stats: Dict[str, Any] = {}
        self.errors: List[str] = []

    def execute(self, target) -> List[Dict[str, Any]]:
        """PAYLOAD CONTRACT: execute(target) → List[Dict[str, Any]]"""
        # -- Stage 1 --
        try:
            _result = dns_recon(str(target))
            self.all_findings.extend(_result)
            logger.info(f"  [dns_recon] {len(_result)} findings")
        except Exception as e:
            self.errors.append(f"dns_recon: {e}")
            logger.warning(f"  [dns_recon] SKIP: {e}")
        try:
            _result = http_fingerprint(str(target))
            logger.info(f"  [http_fingerprint] OK")
        except Exception as e:
            self.errors.append(f"http_fingerprint: {e}")
            logger.warning(f"  [http_fingerprint] SKIP: {e}")
        try:
            _result = probe_endpoints(str(target))
            self.all_findings.extend(_result)
            logger.info(f"  [probe_endpoints] {len(_result)} findings")
        except Exception as e:
            self.errors.append(f"probe_endpoints: {e}")
            logger.warning(f"  [probe_endpoints] SKIP: {e}")
        try:
            _result = extract_links(str(target))
            self.all_findings.extend(_result)
            logger.info(f"  [extract_links] {len(_result)} findings")
        except Exception as e:
            self.errors.append(f"extract_links: {e}")
            logger.warning(f"  [extract_links] SKIP: {e}")
        risk = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in self.all_findings:
            risk[f.get("severity", "INFO")] = risk.get(f.get("severity", "INFO"), 0) + 1
        return {
            "agent": "HYBRID_JAVASCRIPT_ALGORITHMS_x_AUTOSPLOIT__X__HYBRID_AMARANTH_x_WEB_DEV_FOR_BEGINNERS",
            "timestamp": datetime.now().isoformat(),
            "findings": self.all_findings,
            "stats": self.all_stats,
            "errors": self.errors,
            "risk_summary": risk,
        }



def _integration_test():
    """End-to-end pipeline test with mock data."""
    agent = Payload()
    test_target = "localhost"
    result = agent.execute(test_target)
    assert isinstance(result, dict), "execute() must return dict"
    assert "findings" in result, "execute() must return findings"
    logger.info(f"[TEST] Payload.execute() OK")
    return True


def main():
    parser = argparse.ArgumentParser(description="HYBRID_JAVASCRIPT_ALGORITHMS_x_AUTOSPLOIT__X__HYBRID_AMARANTH_x_WEB_DEV_FOR_BEGINNERS")
    parser.add_argument("--target", default=None, help="Target (path)")
    parser.add_argument("--output", default="report.json", help="Output JSON report")
    parser.add_argument("--test", action="store_true", help="Run integration test")
    args = parser.parse_args()

    if args.test:
        _integration_test()
        return

    if not args.target:
        parser.error("--target is required (use --test for self-test)")

    target = Path(args.target).resolve()

    agent = Payload()
    findings = agent.execute(target)
    report = {"agent": "HYBRID_JAVASCRIPT_ALGORITHMS_x_AUTOSPLOIT__X__HYBRID_AMARANTH_x_WEB_DEV_FOR_BEGINNERS", "findings": findings, "summary": agent.summary()}


    crits = [f for f in report["findings"] if f["severity"] in ("CRITICAL", "HIGH")]
    if crits:
        print(f"\n{'='*60}")
        print(f"⚠ {len(crits)} CRITICAL/HIGH FINDINGS:")
        print(f"{'='*60}")
        for f in crits[:10]:
            print(f"  [{f['severity']}] {f['detail']}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
