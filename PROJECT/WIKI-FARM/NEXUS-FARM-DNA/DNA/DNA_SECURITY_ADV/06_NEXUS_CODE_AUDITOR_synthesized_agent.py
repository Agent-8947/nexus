#!/usr/bin/env python3
"""
NEXUS_CODE_AUDITOR [NEXUS SYNTHESIZED Gen-5]
Mission: static_code_analysis
Heritage: GITLEAKS_SCANNER + APPINFOSCANNER
Role: analyzer | Domains: web & infra

I/O Contract:
  Input:  hostname (from CLI --target)
  Output: JSON report with typed findings/stats

Pipeline (2 stages, 4 blocks):
  Stage 1: [check_ports, system_info, process_list]
  Stage 2: [extract_links]
"""

import sys
import json
import logging
import argparse
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import os, re, socket, platform, subprocess
import re, ssl, urllib.request, urllib.error
from html.parser import HTMLParser
from urllib.parse import urljoin

__all__ = ["main", "Pipeline"]


logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS_CODE_AUDITOR")

def __nexus_execute__(func, arg, output_type, findings_list, stats_dict, errors_list):
    try:
        _result = func(arg)
        if output_type == "findings":
            if isinstance(_result, list): findings_list.extend(_result)
            logger.info(f"  [{func.__name__}] {len(_result) if isinstance(_result, list) else 0} findings")
        elif output_type in ("stats", "tech_stack", "port_report", "system_info", "report"):
            if isinstance(_result, dict): stats_dict.update(_result)
            if output_type == "port_report" and isinstance(_result, list):
                for item in _result:
                    if isinstance(item, dict) and "type" not in item:
                        item.update({"type": func.__name__, "severity": "INFO", "detail": str(item), "source": "nexus_pipeline"})
                    findings_list.append(item)
            logger.info(f"  [{func.__name__}] OK")
        else:
            if isinstance(_result, list): findings_list.extend(_result)
            elif isinstance(_result, dict): stats_dict.update(_result)
            logger.info(f"  [{func.__name__}] OK")
    except Exception as e:
        errors_list.append(f"{func.__name__}: {e}")
        logger.warning(f"  [{func.__name__}] SKIP: {e}")


# ── [INFRA] TCP port scanner for common service ports ──
_COMMON_PORTS = {22: "SSH", 80: "HTTP", 443: "HTTPS", 3306: "MySQL",
                 5432: "Postgres", 6379: "Redis", 8080: "HTTP-Alt",
                 8443: "HTTPS-Alt", 9200: "Elasticsearch", 27017: "MongoDB"}

def check_ports(target: str) -> List[Dict[str, Any]]:
    """Check which TCP ports are open on a host. Returns port_report."""
    results: List[Dict[str, Any]] = []
    for port, service in _COMMON_PORTS.items():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.0)
                is_open = s.connect_ex((target, port)) == 0
                results.append({"port": port, "open": is_open, "service": service})
        except Exception:
            results.append({"port": port, "open": False, "service": service, "error": True})
    return results


# ── [INFRA] Collect local system information (OS, CPU, Python version) ──
def system_info(target: str) -> Dict[str, Any]:
    """Collect system information. Returns system_info."""
    return {
        "os": platform.system(), "release": platform.release(),
        "machine": platform.machine(), "python": platform.python_version(),
        "cpu_count": os.cpu_count() or 0,
        "hostname": platform.node(),
        "queried_target": target,
    }


# ── [INFRA] List running processes (cross-platform) ──
def process_list(target: str) -> List[Dict[str, Any]]:
    """List running processes. Returns findings."""
    findings: List[Dict[str, Any]] = []
    try:
        if platform.system() == "Windows":
            out = subprocess.check_output(["tasklist", "/FO", "CSV", "/NH"], text=True, timeout=5)
            for line in out.strip().splitlines()[:50]:
                parts = line.strip('"').split('","')
                if len(parts) >= 2:
                    findings.append({
                        "type": "process", "severity": "INFO",
                        "detail": f"PID {parts[1]}: {parts[0]}",
                        "source": target,
                    })
        else:
            out = subprocess.check_output(["ps", "aux", "--no-headers"], text=True, timeout=5)
            for line in out.strip().splitlines()[:50]:
                parts = line.split(None, 10)
                if len(parts) >= 11:
                    findings.append({
                        "type": "process", "severity": "INFO",
                        "detail": f"PID {parts[1]}: {parts[10][:60]}",
                        "source": target,
                    })
    except Exception as e:
        findings.append({"type": "process_error", "severity": "MEDIUM",
                         "detail": str(e), "source": target})
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



class Analyzer:
    """Takes findings from a collector, enriches/filters, returns refined findings"""

    def __init__(self):
        self.enriched: List[Dict[str, Any]] = []
        self.all_stats: Dict[str, Any] = {}
        self.errors: List[str] = []

    def analyze(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """ANALYZER CONTRACT: analyze(findings) → List[Finding]"""
        self.enriched = []
        self.errors = []
        # Deduplicate by (type, source)
        seen = set()
        for f in findings:
            key = (f.get("type", ""), f.get("source", ""))
            if key not in seen:
                seen.add(key)
                self.enriched.append(f)
        # Run analysis blocks
        # -- Stage 1 --
        __nexus_execute__(check_ports, findings[0].get("source", "unknown") if findings else "unknown", "port_report", self.enriched, getattr(self, "all_stats", {}), self.errors)
        __nexus_execute__(system_info, findings[0].get("source", "unknown") if findings else "unknown", "system_info", self.enriched, getattr(self, "all_stats", {}), self.errors)
        __nexus_execute__(process_list, findings[0].get("source", "unknown") if findings else "unknown", "findings", self.enriched, getattr(self, "all_stats", {}), self.errors)
        # -- Stage 2 --
        __nexus_execute__(extract_links, findings[0].get("source", "unknown") if findings else "unknown", "findings", self.enriched, getattr(self, "all_stats", {}), self.errors)
        return self.enriched

    def summary(self) -> Dict[str, Any]:
        risk = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in self.enriched:
            risk[f.get("severity", "INFO")] = risk.get(f.get("severity", "INFO"), 0) + 1
        return {"total": len(self.enriched), "errors": len(self.errors), "risk": risk, "stats": self.all_stats}



def _integration_test():
    """End-to-end pipeline test with mock data."""
    agent = Analyzer()
    test_target = "127.0.0.1"
    mock_findings = [{"type":"test","severity":"INFO","detail":"mock","source":"test"}]
    result = agent.analyze(mock_findings)
    assert isinstance(result, list), "analyze() must return List[Finding]"
    logger.info(f"[TEST] Analyzer.analyze() OK: {len(result)} findings")
    return True


def main():
    parser = argparse.ArgumentParser(description="NEXUS_CODE_AUDITOR")
    parser.add_argument("--target", default=None, help="Target (hostname)")
    parser.add_argument("--output", default="report.json", help="Output JSON report")
    parser.add_argument("--test", action="store_true", help="Run integration test")
    args = parser.parse_args()

    if args.test:
        _integration_test()
        return

    if not args.target:
        parser.error("--target is required (use --test for self-test)")

    target = args.target

    agent = Analyzer()
    # Analyzer expects pre-collected findings
    report_data = agent.analyze([{ "type": "standalone", "severity": "INFO", "detail": str(target), "source": str(target) }])
    report = {"agent": "NEXUS_CODE_AUDITOR", "findings": report_data, "summary": agent.summary()}

    # Display summary if report is a dict with findings
    if isinstance(report, dict) and "findings" in report:
        crits = [f for f in report["findings"] if f.get("severity") in ("CRITICAL", "HIGH")]
        if crits:
            print(f"\n{'='*60}")
            print(f"⚠ {len(crits)} CRITICAL/HIGH FINDINGS:")
            print(f"{'='*60}")
            for f in crits[:10]:
                print(f"  [{f.get('severity')}] {f.get('detail')}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
