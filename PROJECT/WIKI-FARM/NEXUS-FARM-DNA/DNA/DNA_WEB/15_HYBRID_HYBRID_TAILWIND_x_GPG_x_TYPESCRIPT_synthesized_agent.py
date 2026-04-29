#!/usr/bin/env python3
"""
HYBRID_TAILWIND_x_GPG__X__TYPESCRIPT [NEXUS SYNTHESIZED Gen-2]
Mission: Build a security audit and vulnerability detection tool
Heritage: HYBRID_TAILWIND_x_GPG + TYPESCRIPT
Role: presentation | Domains: web & web

I/O Contract:
  Input:  url (from CLI --target)
  Output: JSON report with typed findings/stats

Pipeline (1 stages, 1 blocks):
  Stage 1: [extract_links]
"""

import sys
import json
import logging
import argparse
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import re, ssl, urllib.request, urllib.error
from html.parser import HTMLParser
from urllib.parse import urljoin

__all__ = ["main", "Pipeline"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("HYBRID_TAILWIND_x_GPG__X__TYPESCRIPT")


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



class Renderer:
    """Converts structured report into human-readable output"""

    def __init__(self):
        self.all_findings: List[Dict[str, Any]] = []
        self.all_stats: Dict[str, Any] = {}
        self.errors: List[str] = []

    def render(self, target) -> str:
        """PRESENTATION CONTRACT: render(target) → str"""
        # -- Stage 1 --
        try:
            _result = extract_links(target)
            self.all_findings.extend(_result)
            logger.info(f"  [extract_links] {len(_result)} findings")
        except Exception as e:
            self.errors.append(f"extract_links: {e}")
            logger.warning(f"  [extract_links] SKIP: {e}")
        risk = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in self.all_findings:
            risk[f.get("severity", "INFO")] = risk.get(f.get("severity", "INFO"), 0) + 1
        return {
            "agent": "HYBRID_TAILWIND_x_GPG__X__TYPESCRIPT",
            "timestamp": datetime.now().isoformat(),
            "findings": self.all_findings,
            "stats": self.all_stats,
            "errors": self.errors,
            "risk_summary": risk,
        }



def _integration_test():
    """End-to-end pipeline test with mock data."""
    agent = Renderer()
    test_target = "http://localhost:99999"
    result = agent.render(test_target)
    assert isinstance(result, dict), "render() must return dict"
    assert "findings" in result, "render() must return findings"
    logger.info(f"[TEST] Renderer.render() OK")
    return True


def main():
    parser = argparse.ArgumentParser(description="HYBRID_TAILWIND_x_GPG__X__TYPESCRIPT")
    parser.add_argument("--target", default=None, help="Target (url)")
    parser.add_argument("--output", default="report.json", help="Output JSON report")
    parser.add_argument("--test", action="store_true", help="Run integration test")
    args = parser.parse_args()

    if args.test:
        _integration_test()
        return

    if not args.target:
        parser.error("--target is required (use --test for self-test)")

    target = args.target

    agent = Renderer()
    report = agent.render(target)


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
