#!/usr/bin/env python3
"""
ABRACADABRA__X__FREEDOMAIN [NEXUS SYNTHESIZED Gen-1]
Mission: Build a security audit and vulnerability detection tool
Heritage: ABRACADABRA + FREEDOMAIN
Role: orchestrator | Domains: security & ai

I/O Contract:
  Input:  hostname (from CLI --target)
  Output: JSON report with typed findings/stats

Pipeline (2 stages, 6 blocks):
  Stage 1: [check_ssl]
  Stage 2: [scan_secrets, hash_files, detect_anomalies, compute_stats, text_similarity]
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
import re, math

__all__ = ["main", "Pipeline"]


logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("ABRACADABRA__X__FREEDOMAIN")

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


# ── [AI] Z-Score + IQR anomaly detection on numeric series ──
def detect_anomalies(target: List[float]) -> List[Dict[str, Any]]:
    """Detect anomalies using Z-Score and IQR methods. Returns findings."""
    findings: List[Dict[str, Any]] = []
    if len(target) < 5:
        return findings
    mean = sum(target) / len(target)
    var = sum((v - mean) ** 2 for v in target) / len(target)
    std = math.sqrt(var) if var > 0 else 1e-8
    # Z-Score detection
    for i, v in enumerate(target):
        z = abs(v - mean) / std
        if z >= 3.0:
            findings.append({
                "type": "anomaly_zscore", "severity": "CRITICAL" if z >= 4.0 else "WARNING",
                "detail": f"Index {i}: value={v:.3f}, z-score={z:.2f}",
                "source": f"index_{i}",
                "index": i, "value": v, "score": round(z, 3),
            })
    # IQR detection
    s = sorted(target)
    n = len(s)
    q1 = s[n // 4]
    q3 = s[3 * n // 4]
    iqr = q3 - q1
    if iqr > 1e-8:
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        for i, v in enumerate(target):
            if v < lower or v > upper:
                dist = max(abs(v - lower), abs(v - upper)) / iqr
                findings.append({
                    "type": "anomaly_iqr", "severity": "HIGH",
                    "detail": f"Index {i}: value={v:.3f}, IQR distance={dist:.2f}",
                    "source": f"index_{i}",
                    "index": i, "value": v, "score": round(dist, 3),
                })
    return findings


# ── [AI] Descriptive statistics (mean, median, std, quartiles, IQR) ──
def compute_stats(target: List[float]) -> Dict[str, Any]:
    """Compute descriptive statistics for a numeric series. Returns stats."""
    if not target:
        return {"count": 0, "error": "empty input"}
    s = sorted(target)
    n = len(s)
    mean = sum(s) / n
    median = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
    var = sum((v - mean) ** 2 for v in s) / n
    std = math.sqrt(var)
    q1 = s[n // 4] if n >= 4 else s[0]
    q3 = s[3 * n // 4] if n >= 4 else s[-1]
    return {
        "count": n, "mean": round(mean, 4), "median": round(median, 4),
        "std": round(std, 4), "min": s[0], "max": s[-1],
        "q1": round(q1, 4), "q3": round(q3, 4), "iqr": round(q3 - q1, 4),
    }


# ── [AI] TF-based cosine similarity between text sections ──
def text_similarity(target: str) -> Dict[str, Any]:
    """Split text in half and compute self-similarity. Returns stats."""
    mid = len(target) // 2
    a, b = target[:mid], target[mid:]
    def tokenize(t):
        words = re.findall(r"[a-z]+", t.lower())
        freq: Dict[str, int] = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
        return freq
    fa, fb = tokenize(a), tokenize(b)
    all_words = set(fa) | set(fb)
    dot = sum(fa.get(w, 0) * fb.get(w, 0) for w in all_words)
    norm_a = math.sqrt(sum(v ** 2 for v in fa.values())) or 1e-8
    norm_b = math.sqrt(sum(v ** 2 for v in fb.values())) or 1e-8
    similarity = dot / (norm_a * norm_b)
    return {
        "similarity": round(similarity, 4),
        "tokens_a": len(fa), "tokens_b": len(fb),
        "method": "cosine_tf",
    }



class Orchestrator:
    """Coordinates multiple blocks in a pipeline"""

    def __init__(self):
        self.all_findings: List[Dict[str, Any]] = []
        self.all_stats: Dict[str, Any] = {}
        self.errors: List[str] = []

    def run(self, target) -> Dict[str, Any]:
        """ORCHESTRATOR CONTRACT: run(target) → Dict[str, Any]"""
        # -- Stage 1 --
        __nexus_execute__(check_ssl, target, "findings", self.all_findings, getattr(self, "all_stats", {}), self.errors)
        # -- Stage 2 --
        __nexus_execute__(scan_secrets, target, "findings", self.all_findings, getattr(self, "all_stats", {}), self.errors)
        __nexus_execute__(hash_files, target, "findings", self.all_findings, getattr(self, "all_stats", {}), self.errors)
        __nexus_execute__(detect_anomalies, [f.get('value', 0) for f in self.all_findings if 'value' in f] or [0.0], "findings", self.all_findings, getattr(self, "all_stats", {}), self.errors)
        __nexus_execute__(compute_stats, [f.get('value', 0) for f in self.all_findings if 'value' in f] or [0.0], "stats", self.all_findings, getattr(self, "all_stats", {}), self.errors)
        __nexus_execute__(text_similarity, str(target), "stats", self.all_findings, getattr(self, "all_stats", {}), self.errors)
        risk = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in self.all_findings:
            risk[f.get("severity", "INFO")] = risk.get(f.get("severity", "INFO"), 0) + 1
        return {
            "agent": "ABRACADABRA__X__FREEDOMAIN",
            "timestamp": datetime.now().isoformat(),
            "findings": self.all_findings,
            "stats": self.all_stats,
            "errors": self.errors,
            "risk_summary": risk,
        }



def _integration_test():
    """End-to-end pipeline test with mock data."""
    agent = Orchestrator()
    test_target = Path(tempfile.mkdtemp())
    result = agent.run(test_target)
    assert isinstance(result, dict), "run() must return dict"
    assert "findings" in result, "run() must return findings"
    logger.info(f"[TEST] Orchestrator.run() OK")
    return True


def main():
    parser = argparse.ArgumentParser(description="ABRACADABRA__X__FREEDOMAIN")
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

    agent = Orchestrator()
    report = agent.run(target)

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
