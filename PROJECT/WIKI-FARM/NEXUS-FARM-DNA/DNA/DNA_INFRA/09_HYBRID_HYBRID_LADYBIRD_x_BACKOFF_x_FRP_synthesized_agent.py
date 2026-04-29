#!/usr/bin/env python3
"""
HYBRID_LADYBIRD_x_BACKOFF__X__FRP [NEXUS SYNTHESIZED Gen-2]
Mission: Build a security audit and vulnerability detection tool
Heritage: HYBRID_LADYBIRD_x_BACKOFF + FRP
Role: library | Domains: security & infra

I/O Contract:
  Input:  url (from CLI --target)
  Output: JSON report with typed findings/stats

Pipeline (1 stages, 6 blocks):
  Stage 1: [scan_secrets, check_ssl, hash_files, check_ports, system_info, process_list]
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
import re, hashlib, socket, ssl

__all__ = ["main", "Pipeline"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("HYBRID_LADYBIRD_x_BACKOFF__X__FRP")


# ── [SECURITY] Scan directory for leaked secrets (API keys, tokens, passwords) ──
SECRET_PATTERNS: Dict[str, tuple[str, str]] = {
    "aws_key":        (r"(?:AKIA|ASIA)[0-9A-Z]{16}", "CRITICAL"),
    "github_token":   (r"gh[pousr]_[A-Za-z0-9_]{36,255}", "CRITICAL"),
    "private_key":    (r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", "CRITICAL"),
    "generic_secret": (r"(?i)(?:secret|password|token|apikey)\s*[:=]\s*['\"]+([A-Za-z0-9\-_./+=]{8,64})", "HIGH"),
    "db_url":         (r"(?i)(?:postgres|mysql|mongodb|redis)://[^\s\'\"]{10,200}", "CRITICAL"),
    "jwt":            (r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}", "HIGH"),
}
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv"}

def scan_secrets(target: Path) -> List[Dict[str, Any]]:
    """Scan files for leaked secrets. Returns standardized findings."""
    findings: List[Dict[str, Any]] = []
    for fpath in target.rglob("*"):
        if not fpath.is_file() or fpath.stat().st_size > 500_000:
            continue
        if any(s in fpath.parts for s in SKIP_DIRS):
            continue
        try:
            text = fpath.read_text(encoding="utf-8", errors="ignore")
            for rule_name, (pattern, severity) in SECRET_PATTERNS.items():
                for m in re.finditer(pattern, text):
                    line = text[:m.start()].count("\n") + 1
                    findings.append({
                        "type": rule_name,
                        "severity": severity,
                        "detail": f"{rule_name} found at line {line}",
                        "source": str(fpath.relative_to(target)),
                        "line": line,
                        "preview": m.group(0)[:8] + "***",
                    })
        except Exception:
            pass
    return findings


# ── [SECURITY] Check SSL certificate validity, extract issuer/expiry/SANs ──
def check_ssl(target: str) -> List[Dict[str, Any]]:
    """Check SSL certificate and return findings."""
    findings: List[Dict[str, Any]] = []
    ctx = ssl.create_default_context()
    try:
        with ctx.wrap_socket(socket.socket(), server_hostname=target) as s:
            s.settimeout(5)
            s.connect((target, 443))
            cert = s.getpeercert()
            expires = cert.get("notAfter", "")
            findings.append({
                "type": "ssl_valid", "severity": "INFO",
                "detail": f"SSL valid, expires {expires}",
                "source": target,
            })
            # Check expiry
            from datetime import datetime as _dt
            try:
                exp_date = _dt.strptime(expires, "%b %d %H:%M:%S %Y %Z")
                days_left = (exp_date - _dt.now()).days
                if days_left < 30:
                    findings.append({
                        "type": "ssl_expiring", "severity": "HIGH",
                        "detail": f"SSL expires in {days_left} days",
                        "source": target,
                    })
            except Exception:
                pass
    except Exception as e:
        findings.append({
            "type": "ssl_error", "severity": "CRITICAL",
            "detail": f"SSL check failed: {e}",
            "source": target,
        })
    return findings


# ── [SECURITY] Compute integrity hashes (SHA256) for all files in directory ──
def hash_files(target: Path) -> List[Dict[str, Any]]:
    """Compute SHA256 hashes for files, returning as findings."""
    findings: List[Dict[str, Any]] = []
    for fpath in target.rglob("*"):
        if not fpath.is_file() or fpath.stat().st_size > 2_000_000:
            continue
        if ".git" in fpath.parts:
            continue
        try:
            sha = hashlib.sha256(fpath.read_bytes()).hexdigest()
            findings.append({
                "type": "file_hash", "severity": "INFO",
                "detail": f"SHA256: {sha[:16]}...",
                "source": str(fpath.relative_to(target)),
                "hash": sha,
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
    """Orchestrates 6 blocks in 1 stages."""

    def __init__(self):
        self.all_findings: List[Dict[str, Any]] = []
        self.all_stats: Dict[str, Any] = {}
        self.errors: List[str] = []

    def run(self, target) -> Dict[str, Any]:
        """Execute full pipeline. Target type: url."""

        # ── Stage 1 ──
        try:
            result = scan_secrets(str(target))
            self.all_findings.extend(result)
            logger.info(f"  [scan_secrets] {len(result)} findings")
        except Exception as e:
            self.errors.append(f"scan_secrets: {e}")
            logger.warning(f"  [scan_secrets] SKIP: {e}")
        try:
            result = check_ssl(str(target))
            self.all_findings.extend(result)
            logger.info(f"  [check_ssl] {len(result)} findings")
        except Exception as e:
            self.errors.append(f"check_ssl: {e}")
            logger.warning(f"  [check_ssl] SKIP: {e}")
        try:
            result = hash_files(str(target))
            self.all_findings.extend(result)
            logger.info(f"  [hash_files] {len(result)} findings")
        except Exception as e:
            self.errors.append(f"hash_files: {e}")
            logger.warning(f"  [hash_files] SKIP: {e}")
        try:
            result = check_ports(str(target))
            self.all_stats["check_ports"] = result
            logger.info(f"  [check_ports] {len(result) if isinstance(result, list) else 1} items")
        except Exception as e:
            self.errors.append(f"check_ports: {e}")
            logger.warning(f"  [check_ports] SKIP: {e}")
        try:
            result = system_info(str(target))
            self.all_stats["system_info"] = result
            logger.info(f"  [system_info] {len(result) if isinstance(result, list) else 1} items")
        except Exception as e:
            self.errors.append(f"system_info: {e}")
            logger.warning(f"  [system_info] SKIP: {e}")
        try:
            result = process_list(str(target))
            self.all_findings.extend(result)
            logger.info(f"  [process_list] {len(result)} findings")
        except Exception as e:
            self.errors.append(f"process_list: {e}")
            logger.warning(f"  [process_list] SKIP: {e}")

        # ── Build report ──
        risk_summary = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in self.all_findings:
            sev = f.get("severity", "INFO")
            risk_summary[sev] = risk_summary.get(sev, 0) + 1

        return {
            "agent": "HYBRID_LADYBIRD_x_BACKOFF__X__FRP",
            "version": "2.0-gen2",
            "timestamp": datetime.now().isoformat(),
            "pipeline_stages": 1,
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
    test_target = Path(tempfile.mkdtemp())
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
    parser = argparse.ArgumentParser(description="HYBRID_LADYBIRD_x_BACKOFF__X__FRP")
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
