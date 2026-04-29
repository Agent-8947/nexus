#!/usr/bin/env python3
"""
BAREMETAL-OS-LEGACY__X__METASPLOIT [NEXUS SYNTHESIZED Gen-1]
Mission: Build a security audit and vulnerability detection tool
Heritage: BAREMETAL-OS-LEGACY + METASPLOIT
Role: library | Domains: infra & security
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import re, hashlib, socket, ssl, subprocess
import re, socket, subprocess, platform

__all__ = ["main"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("BAREMETAL-OS-LEGACY__X__METASPLOIT")


# ── TCP port scanner for common service ports ──
def check_ports(host: str, ports: list[int] = None, timeout: float = 1.0) -> list[dict]:
    """Check which TCP ports are open on a host."""
    import socket
    if ports is None:
        ports = [22, 80, 443, 3306, 5432, 6379, 8080, 8443, 9200, 27017]
    results = []
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                r = s.connect_ex((host, port))
                results.append({"port": port, "open": r == 0})
        except Exception:
            results.append({"port": port, "open": False, "error": True})
    return results


# ── Local system info collector (OS, CPU, Python version) ──
def get_system_info() -> dict:
    """Collect system information."""
    import platform, os
    return {
        "os": platform.system(), "release": platform.release(),
        "machine": platform.machine(), "python": platform.python_version(),
        "cpu_count": os.cpu_count(),
        "hostname": platform.node(),
    }


# ── Cross-platform process listing ──
def list_processes() -> list[dict]:
    """List running processes (cross-platform)."""
    import subprocess, platform
    procs = []
    try:
        if platform.system() == "Windows":
            out = subprocess.check_output(["tasklist", "/FO", "CSV"], text=True, timeout=5)
            import csv
            for row in csv.DictReader(out.strip().splitlines()):
                procs.append({"name": row.get("Image Name", ""), "pid": row.get("PID", ""),
                              "mem": row.get("Mem Usage", "")})
        else:
            out = subprocess.check_output(["ps", "aux", "--no-headers"], text=True, timeout=5)
            for line in out.strip().splitlines()[:100]:
                parts = line.split(None, 10)
                if len(parts) >= 11:
                    procs.append({"user": parts[0], "pid": parts[1], "cpu": parts[2],
                                  "mem": parts[3], "cmd": parts[10][:80]})
    except Exception:
        pass
    return procs


# ── Scans filesystem for API keys, tokens, private keys, DB URLs, JWTs ──
SECRET_PATTERNS = {
    "aws_key": r"(?:AKIA|ASIA)[0-9A-Z]{16}",
    "github_token": r"gh[pousr]_[A-Za-z0-9_]{36,255}",
    "private_key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    "generic_secret": r"(?i)(?:secret|password|token|apikey)\s*[:=]\s*[\'\"]+([A-Za-z0-9\-_./+=]{8,64})",
    "db_url": r"(?i)(?:postgres|mysql|mongodb|redis)://[^\s\'\"]{10,200}",
    "jwt": r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
}

def scan_secrets(target: Path) -> list[dict]:
    """Scan files for leaked secrets."""
    findings = []
    skip = {".git", "__pycache__", "node_modules", ".venv"}
    for fpath in target.rglob("*"):
        if not fpath.is_file() or fpath.stat().st_size > 500_000:
            continue
        if any(s in fpath.parts for s in skip):
            continue
        try:
            text = fpath.read_text(encoding="utf-8", errors="ignore")
            for rule_name, pattern in SECRET_PATTERNS.items():
                for m in re.finditer(pattern, text):
                    line = text[:m.start()].count("\n") + 1
                    findings.append({
                        "type": rule_name, "file": str(fpath.relative_to(target)),
                        "line": line, "preview": m.group(0)[:8] + "***",
                        "severity": "CRITICAL" if "key" in rule_name or "private" in rule_name else "HIGH",
                    })
        except Exception:
            pass
    return findings


# ── Validates SSL certificates, extracts issuer/expiry/SANs ──
def check_ssl_cert(hostname: str, port: int = 443) -> dict:
    """Check SSL certificate validity and details."""
    import ssl, socket
    ctx = ssl.create_default_context()
    try:
        with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
            s.settimeout(5)
            s.connect((hostname, port))
            cert = s.getpeercert()
            return {
                "valid": True,
                "subject": dict(x[0] for x in cert.get("subject", ())),
                "issuer": dict(x[0] for x in cert.get("issuer", ())),
                "expires": cert.get("notAfter", ""),
                "sans": [x[1] for x in cert.get("subjectAltName", ())],
            }
    except Exception as e:
        return {"valid": False, "error": str(e)}


# ── Computes MD5/SHA1/SHA256 integrity hashes for files ──
def compute_hashes(file_path: Path) -> dict:
    """Compute MD5, SHA1, SHA256 hashes for a file."""
    import hashlib
    hashes = {"md5": hashlib.md5(), "sha1": hashlib.sha1(), "sha256": hashlib.sha256()}
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            for h in hashes.values():
                h.update(chunk)
    return {k: v.hexdigest() for k, v in hashes.items()}


def main():
    parser = argparse.ArgumentParser(description="BAREMETAL-OS-LEGACY__X__METASPLOIT")
    parser.add_argument("--target", required=True, help="Target path or URL")
    parser.add_argument("--output", default="report.json", help="Output JSON report")
    args = parser.parse_args()

    target = args.target
    logger.info(f"[START] {target}")

    results = {}

    try:
        results["port_check"] = port_check(target)
        logger.info(f"  [port_check] OK")
    except Exception as e:
        logger.warning(f"  [port_check] SKIP: {e}")

    try:
        results["system_info"] = system_info(target)
        logger.info(f"  [system_info] OK")
    except Exception as e:
        logger.warning(f"  [system_info] SKIP: {e}")

    try:
        results["scan_secrets"] = scan_secrets(Path(target))
        logger.info(f"  [scan_secrets] OK")
    except Exception as e:
        logger.warning(f"  [scan_secrets] SKIP: {e}")

    try:
        results["check_ssl_cert"] = check_ssl_cert(target)
        logger.info(f"  [check_ssl_cert] OK")
    except Exception as e:
        logger.warning(f"  [check_ssl_cert] SKIP: {e}")

    report = {
        "agent": "BAREMETAL-OS-LEGACY__X__METASPLOIT",
        "version": "1.0-gen1",
        "timestamp": datetime.now().isoformat(),
        "target": target,
        "results": results,
    }

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    logger.info(f"[DONE] Report -> {output}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
