#!/usr/bin/env python3
"""
NEXUS_HARDWARE_AUDITOR [NEXUS SYNTHESIZED Gen-3]
Mission: hardware_security_audit
Heritage: SOC_INSPECTOR + VULN_SCANNER
Role: analyzer | Domains: hardware & security

I/O Contract:
  Input:  hostname (from CLI --target)
  Output: JSON report with typed findings/stats

Pipeline (2 stages, 4 blocks):
  Stage 1: [check_ssl, find_serial_ports]
  Stage 2: [scan_secrets, hash_files]
"""

import sys
import json
import logging
import argparse
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import re, hashlib, socket, ssl
import re, platform, subprocess

__all__ = ["main", "Pipeline"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS_HARDWARE_AUDITOR")


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


# ── [HARDWARE] Discover available serial ports (Windows/Linux) ──
def find_serial_ports(target: str) -> List[Dict[str, Any]]:
    """Discover available serial ports. Returns findings."""
    findings: List[Dict[str, Any]] = []
    if platform.system() == "Windows":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DEVICEMAP\SERIALCOMM")
            i = 0
            while True:
                try:
                    name, val, _ = winreg.EnumValue(key, i)
                    findings.append({"type": "serial_port", "severity": "INFO",
                                     "detail": f"{val} ({name})", "source": target})
                    i += 1
                except OSError:
                    break
        except Exception:
            findings.append({"type": "serial_scan", "severity": "INFO",
                             "detail": "No serial ports found (Windows)", "source": target})
    else:
        for p in Path("/dev").glob("tty*"):
            if any(x in p.name for x in ("USB", "ACM", "AMA")):
                findings.append({"type": "serial_port", "severity": "INFO",
                                 "detail": str(p), "source": target})
    return findings



class Analyzer:
    """Takes findings from a collector, enriches/filters, returns refined findings"""

    def __init__(self):
        self.enriched: List[Dict[str, Any]] = []
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
        try:
            _result = check_ssl(target)
            self.enriched.extend(_result)
            logger.info(f"  [check_ssl] {len(_result)} findings")
        except Exception as e:
            self.errors.append(f"check_ssl: {e}")
            logger.warning(f"  [check_ssl] SKIP: {e}")
        try:
            _result = find_serial_ports(target)
            self.enriched.extend(_result)
            logger.info(f"  [find_serial_ports] {len(_result)} findings")
        except Exception as e:
            self.errors.append(f"find_serial_ports: {e}")
            logger.warning(f"  [find_serial_ports] SKIP: {e}")
        # -- Stage 2 --
        try:
            _result = scan_secrets(str(target))
            self.enriched.extend(_result)
            logger.info(f"  [scan_secrets] {len(_result)} findings")
        except Exception as e:
            self.errors.append(f"scan_secrets: {e}")
            logger.warning(f"  [scan_secrets] SKIP: {e}")
        try:
            _result = hash_files(str(target))
            self.enriched.extend(_result)
            logger.info(f"  [hash_files] {len(_result)} findings")
        except Exception as e:
            self.errors.append(f"hash_files: {e}")
            logger.warning(f"  [hash_files] SKIP: {e}")
        return self.enriched

    def summary(self) -> Dict[str, Any]:
        risk = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in self.enriched:
            risk[f.get("severity", "INFO")] = risk.get(f.get("severity", "INFO"), 0) + 1
        return {"total": len(self.enriched), "errors": len(self.errors), "risk": risk}



def _integration_test():
    """End-to-end pipeline test with mock data."""
    agent = Analyzer()
    test_target = Path(tempfile.mkdtemp())
    mock_findings = [{"type":"test","severity":"INFO","detail":"mock","source":"test"}]
    result = agent.analyze(mock_findings)
    assert isinstance(result, list), "analyze() must return List[Finding]"
    logger.info(f"[TEST] Analyzer.analyze() OK: {len(result)} findings")
    return True


def main():
    parser = argparse.ArgumentParser(description="NEXUS_HARDWARE_AUDITOR")
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
    # Analyzer expects pre-collected findings; in standalone mode collect from target
    report = agent.analyze([{"type":"standalone","severity":"INFO","detail":str(target),"source":str(target)}])
    report = {"agent": "NEXUS_HARDWARE_AUDITOR", "findings": report, "summary": agent.summary()}


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
