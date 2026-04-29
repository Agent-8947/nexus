#!/usr/bin/env python3
"""
KERAS__X__HYBRID_BAREMETAL-OS-LEGACY_x_METASPLOIT [NEXUS SYNTHESIZED Gen-2]
Mission: Build a security audit and vulnerability detection tool
Heritage: KERAS + HYBRID_BAREMETAL-OS-LEGACY_x_METASPLOIT
Role: collector | Domains: ai & security
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
import re, math, csv, statistics

__all__ = ["main"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("KERAS__X__HYBRID_BAREMETAL-OS-LEGACY_x_METASPLOIT")


# ── Statistical Z-Score anomaly detection ──
def detect_anomalies_zscore(values: list[float], threshold: float = 3.0) -> list[dict]:
    """Z-Score anomaly detection on numeric series."""
    import math
    if len(values) < 5:
        return []
    mean = sum(values) / len(values)
    var = sum((v - mean) ** 2 for v in values) / len(values)
    std = math.sqrt(var) if var > 0 else 1e-8
    anomalies = []
    for i, v in enumerate(values):
        z = abs(v - mean) / std
        if z >= threshold:
            anomalies.append({"index": i, "value": v, "zscore": round(z, 3),
                              "severity": "CRITICAL" if z >= 4 else "WARNING"})
    return anomalies


# ── TF-based cosine similarity between two texts ──
def cosine_similarity(text_a: str, text_b: str) -> float:
    """Compute cosine similarity between two texts using word frequency."""
    import math, re
    def tokenize(t):
        words = re.findall(r"[a-z]+", t.lower())
        freq = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
        return freq
    fa, fb = tokenize(text_a), tokenize(text_b)
    all_words = set(fa) | set(fb)
    dot = sum(fa.get(w, 0) * fb.get(w, 0) for w in all_words)
    norm_a = math.sqrt(sum(v ** 2 for v in fa.values()))
    norm_b = math.sqrt(sum(v ** 2 for v in fb.values()))
    if norm_a < 1e-8 or norm_b < 1e-8:
        return 0.0
    return round(dot / (norm_a * norm_b), 4)


# ── Descriptive statistics (mean, median, std, quartiles, IQR) ──
def compute_stats(values: list[float]) -> dict:
    """Compute descriptive statistics for a numeric series."""
    import math, statistics
    if not values:
        return {}
    s = sorted(values)
    n = len(s)
    mean = sum(s) / n
    median = statistics.median(s)
    std = statistics.stdev(s) if n > 1 else 0.0
    q1 = statistics.median(s[:n//2]) if n > 2 else s[0]
    q3 = statistics.median(s[(n+1)//2:]) if n > 2 else s[-1]
    return {"count": n, "mean": round(mean, 4), "median": round(median, 4),
            "std": round(std, 4), "min": s[0], "max": s[-1],
            "q1": round(q1, 4), "q3": round(q3, 4), "iqr": round(q3 - q1, 4)}


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
    parser = argparse.ArgumentParser(description="KERAS__X__HYBRID_BAREMETAL-OS-LEGACY_x_METASPLOIT")
    parser.add_argument("--target", required=True, help="Target path or URL")
    parser.add_argument("--output", default="report.json", help="Output JSON report")
    args = parser.parse_args()

    target = args.target
    logger.info(f"[START] {target}")

    results = {}

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
        "agent": "KERAS__X__HYBRID_BAREMETAL-OS-LEGACY_x_METASPLOIT",
        "version": "1.0-gen2",
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
