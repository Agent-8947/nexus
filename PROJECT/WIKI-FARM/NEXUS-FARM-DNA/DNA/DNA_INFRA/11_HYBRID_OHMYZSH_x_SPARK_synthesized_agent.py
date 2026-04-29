#!/usr/bin/env python3
"""
OHMYZSH__X__SPARK [NEXUS SYNTHESIZED Gen-1]
Mission: Build a security audit and vulnerability detection tool
Heritage: OHMYZSH + SPARK
Role: collector | Domains: infra & osint

I/O Contract:
  Input:  path (from CLI --target)
  Output: JSON report with typed findings/stats

Pipeline (1 stages, 6 blocks):
  Stage 1: [dns_recon, http_fingerprint, probe_endpoints, check_ports, system_info, process_list]
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
logger = logging.getLogger("OHMYZSH__X__SPARK")


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



class Collector:
    """Gathers raw data from target and returns standardized findings"""

    def __init__(self):
        self.findings: List[Dict[str, Any]] = []
        self.errors: List[str] = []

    def collect(self, target) -> List[Dict[str, Any]]:
        """COLLECTOR CONTRACT: collect(target) → List[Finding]"""
        self.findings = []
        self.errors = []
        # -- Stage 1 --
        try:
            _result = dns_recon(str(target))
            self.findings.extend(_result)
            logger.info(f"  [dns_recon] {len(_result)} findings")
        except Exception as e:
            self.errors.append(f"dns_recon: {e}")
            logger.warning(f"  [dns_recon] SKIP: {e}")
        try:
            _result = http_fingerprint(str(target))
            # [PATCHER] Восстановлена передача данных из http_fingerprint
            if isinstance(_result, list): self.findings.extend(_result)
            if isinstance(_result, list):
                for item in _result:
                    if isinstance(item, dict) and "type" not in item:
                        item["type"] = "http_fingerprint"
                        item["severity"] = "INFO"
                        item["detail"] = str(item)
                        item["source"] = str(target)
                    self.findings.append(item)
            logger.info(f"  [http_fingerprint] OK")
        except Exception as e:
            self.errors.append(f"http_fingerprint: {e}")
            logger.warning(f"  [http_fingerprint] SKIP: {e}")
        try:
            _result = probe_endpoints(str(target))
            self.findings.extend(_result)
            logger.info(f"  [probe_endpoints] {len(_result)} findings")
        except Exception as e:
            self.errors.append(f"probe_endpoints: {e}")
            logger.warning(f"  [probe_endpoints] SKIP: {e}")
        try:
            _result = check_ports(str(target))
            # [PATCHER] Восстановлена передача данных из check_ports
            if isinstance(_result, list): self.findings.extend(_result)
            if isinstance(_result, list):
                for item in _result:
                    if isinstance(item, dict) and "type" not in item:
                        item["type"] = "check_ports"
                        item["severity"] = "INFO"
                        item["detail"] = str(item)
                        item["source"] = str(target)
                    self.findings.append(item)
            logger.info(f"  [check_ports] OK")
        except Exception as e:
            self.errors.append(f"check_ports: {e}")
            logger.warning(f"  [check_ports] SKIP: {e}")
        try:
            _result = system_info(str(target))
            # [PATCHER] Сохранено из system_info
            if isinstance(_result, dict): self.all_stats.update(_result)
            # [PATCHER] Сохранено из system_info
            if isinstance(_result, dict): self.all_stats.update(_result)
            # [PATCHER] Сохранено из system_info
            if isinstance(_result, dict): self.all_stats.update(_result)
            if isinstance(_result, list):
                for item in _result:
                    if isinstance(item, dict) and "type" not in item:
                        item["type"] = "system_info"
                        item["severity"] = "INFO"
                        item["detail"] = str(item)
                        item["source"] = str(target)
                    self.findings.append(item)
            logger.info(f"  [system_info] OK")
        except Exception as e:
            self.errors.append(f"system_info: {e}")
            logger.warning(f"  [system_info] SKIP: {e}")
        try:
            _result = process_list(str(target))
            self.findings.extend(_result)
            logger.info(f"  [process_list] {len(_result)} findings")
        except Exception as e:
            self.errors.append(f"process_list: {e}")
            logger.warning(f"  [process_list] SKIP: {e}")
        return self.findings

    def summary(self) -> Dict[str, Any]:
        risk = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in self.findings:
            risk[f.get("severity", "INFO")] = risk.get(f.get("severity", "INFO"), 0) + 1
        return {"total": len(self.findings), "errors": len(self.errors), "risk": risk}



def _integration_test():
    """End-to-end pipeline test with mock data."""
    agent = Collector()
    test_target = "localhost"
    result = agent.collect(test_target)
    assert isinstance(result, list), "collect() must return List[Finding]"
    for f in result:
        assert "type" in f, f"Finding missing type"
        assert "severity" in f, f"Finding missing severity"
    logger.info(f"[TEST] Collector.collect() OK: {len(result)} findings")
    return True


def main():
    parser = argparse.ArgumentParser(description="OHMYZSH__X__SPARK")
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

    agent = Collector()
    findings = agent.collect(target)
    report = {"agent": "OHMYZSH__X__SPARK", "findings": findings, "summary": agent.summary()}


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