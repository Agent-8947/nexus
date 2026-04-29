#!/usr/bin/env python3
"""
OBJECT_DETECTION_METRICS__X__HYBRID_LEETCODE_101_x_HYBRID_CIPHEY_x_HYBRID_DOCLING_x_HYBRID_LAZYDOCKER_x_AUTOSPLOIT [NEXUS SYNTHESIZED Gen-5]
Mission: Build a security audit and vulnerability detection tool
Heritage: OBJECT_DETECTION_METRICS + HYBRID_LEETCODE_101_x_HYBRID_CIPHEY_x_HYBRID_DOCLING_x_HYBRID_LAZYDOCKER_x_AUTOSPLOIT
Role: analyzer | Domains: infra & osint

I/O Contract:
  Input:  hostname (from CLI --target)
  Output: JSON report with typed findings/stats

Pipeline (2 stages, 6 blocks):
  Stage 1: [dns_recon, check_ports, system_info, process_list]
  Stage 2: [http_fingerprint, probe_endpoints]
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
import re, socket, ssl, urllib.request, urllib.error

__all__ = ["main", "Pipeline"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("OBJECT_DETECTION_METRICS__X__HYBRID_LEETCODE_101_x_HYBRID_CI")


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


class Pipeline:
    """Orchestrates 6 blocks in 2 stages."""

    def __init__(self):
        self.all_findings: List[Dict[str, Any]] = []
        self.all_stats: Dict[str, Any] = {}
        self.errors: List[str] = []

    def run(self, target) -> Dict[str, Any]:
        """Execute full pipeline. Target type: hostname."""

        # ── Stage 1 ──
        try:
            result = dns_recon(target)
            self.all_findings.extend(result)
            logger.info(f"  [dns_recon] {len(result)} findings")
        except Exception as e:
            self.errors.append(f"dns_recon: {e}")
            logger.warning(f"  [dns_recon] SKIP: {e}")
        try:
            result = check_ports(target)
            self.all_stats["check_ports"] = result
            logger.info(f"  [check_ports] {len(result) if isinstance(result, list) else 1} items")
        except Exception as e:
            self.errors.append(f"check_ports: {e}")
            logger.warning(f"  [check_ports] SKIP: {e}")
        try:
            result = system_info(target)
            self.all_stats["system_info"] = result
            logger.info(f"  [system_info] {len(result) if isinstance(result, list) else 1} items")
        except Exception as e:
            self.errors.append(f"system_info: {e}")
            logger.warning(f"  [system_info] SKIP: {e}")
        try:
            result = process_list(target)
            self.all_findings.extend(result)
            logger.info(f"  [process_list] {len(result)} findings")
        except Exception as e:
            self.errors.append(f"process_list: {e}")
            logger.warning(f"  [process_list] SKIP: {e}")

        # ── Stage 2 ──
        try:
            result = http_fingerprint(str(target))
            self.all_stats["http_fingerprint"] = result
            logger.info(f"  [http_fingerprint] {len(result) if isinstance(result, list) else 1} items")
        except Exception as e:
            self.errors.append(f"http_fingerprint: {e}")
            logger.warning(f"  [http_fingerprint] SKIP: {e}")
        try:
            result = probe_endpoints(str(target))
            self.all_findings.extend(result)
            logger.info(f"  [probe_endpoints] {len(result)} findings")
        except Exception as e:
            self.errors.append(f"probe_endpoints: {e}")
            logger.warning(f"  [probe_endpoints] SKIP: {e}")

        # ── Build report ──
        risk_summary = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in self.all_findings:
            sev = f.get("severity", "INFO")
            risk_summary[sev] = risk_summary.get(sev, 0) + 1

        return {
            "agent": "OBJECT_DETECTION_METRICS__X__HYBRID_LEETCODE_101_x_HYBRID_CIPHEY_x_HYBRID_DOCLING_x_HYBRID_LAZYDOCKER_x_AUTOSPLOIT",
            "version": "2.0-gen5",
            "timestamp": datetime.now().isoformat(),
            "pipeline_stages": 2,
            "blocks_executed": 6 - len(self.errors),
            "target": str(target),
            "risk_summary": risk_summary,
            "findings": self.all_findings,
            "stats": self.all_stats,
            "errors": self.errors,
        }


def _integration_test():
    """End-to-end pipeline test with mock data."""
    pipe = Pipeline()
    test_target = "localhost"
    report = pipe.run(test_target)

    # Contract assertions
    assert isinstance(report, dict), "Report must be dict"
    assert "agent" in report, "Report must have agent field"
    assert "findings" in report, "Report must have findings field"
    assert "stats" in report, "Report must have stats field"
    assert "risk_summary" in report, "Report must have risk_summary"
    assert isinstance(report["findings"], list), "Findings must be list"
    for f in report["findings"]:
        assert "type" in f, f"Finding missing type: {f}"
        assert "severity" in f, f"Finding missing severity: {f}"
        assert "detail" in f, f"Finding missing detail: {f}"
        assert "source" in f, f"Finding missing source: {f}"
    logger.info(f"[TEST] Pipeline OK: {len(report['findings'])} findings, {len(report['errors'])} errors")
    return True


def main():
    parser = argparse.ArgumentParser(description="OBJECT_DETECTION_METRICS__X__HYBRID_LEETCODE_101_x_HYBRID_CIPHEY_x_HYBRID_DOCLING_x_HYBRID_LAZYDOCKER_x_AUTOSPLOIT")
    parser.add_argument("--target", required=True, help="Target (hostname)")
    parser.add_argument("--output", default="report.json", help="Output JSON report")
    parser.add_argument("--test", action="store_true", help="Run integration test")
    args = parser.parse_args()

    if args.test:
        _integration_test()
        return

    target = args.target

    pipe = Pipeline()
    report = pipe.run(target)

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    logger.info(f"[DONE] {len(report['findings'])} findings → {output}")

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
