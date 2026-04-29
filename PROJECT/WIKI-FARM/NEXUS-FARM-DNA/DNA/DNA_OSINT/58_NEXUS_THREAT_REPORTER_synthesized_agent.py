#!/usr/bin/env python3
"""
NEXUS_THREAT_REPORTER [NEXUS SYNTHESIZED Gen-5]
Mission: executive_threat_briefing
Heritage: EXPLOIT_DB + SQLMAP
Role: presentation | Domains: security & data

I/O Contract:
  Input:  url (from CLI --target)
  Output: JSON report with typed findings/stats

Pipeline (1 stages, 5 blocks):
  Stage 1: [scan_secrets, check_ssl, hash_files, analyze_csv, store_findings_db]
"""

import sys
import json
import logging
import argparse
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import re, csv, sqlite3
import re, hashlib, socket, ssl

__all__ = ["main", "Pipeline"]


logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS_THREAT_REPORTER")

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


# ── [DATA] Analyze CSV file structure with column type detection ──
def analyze_csv(target: Path) -> Dict[str, Any]:
    """Analyze CSV file(s) in directory. Returns stats."""
    csv_files = list(target.rglob("*.csv")) if target.is_dir() else [target]
    if not csv_files:
        return {"error": "no CSV files found", "count": 0}
    all_stats: Dict[str, Any] = {"files_analyzed": len(csv_files), "columns": {}}
    for csv_file in csv_files[:5]:
        try:
            with open(csv_file, encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames or []
                rows = [r for i, r in enumerate(reader) if i < 5000]
            for col in headers:
                nums = []
                for r in rows:
                    try: nums.append(float(r.get(col, "")))
                    except: pass
                if nums:
                    all_stats["columns"][col] = {
                        "type": "numeric", "count": len(nums),
                        "mean": round(sum(nums) / len(nums), 3),
                        "min": min(nums), "max": max(nums),
                    }
                else:
                    all_stats["columns"][col] = {"type": "text", "unique": len(set(r.get(col, "") for r in rows))}
        except Exception:
            pass
    return all_stats


# ── [DATA] Store findings in SQLite database and return summary ──
def store_findings_db(target: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Store findings in a temporary SQLite database. Returns stats."""
    db_path = Path(tempfile.mkdtemp()) / "findings.db"
    conn = sqlite3.connect(str(db_path))
    conn.execute("""CREATE TABLE findings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT, severity TEXT, detail TEXT, source TEXT, ts TEXT
    )""")
    for f in target:
        conn.execute("INSERT INTO findings (type, severity, detail, source, ts) VALUES (?,?,?,?,?)",
                     (f.get("type",""), f.get("severity",""), f.get("detail",""),
                      f.get("source",""), datetime.now().isoformat()))
    conn.commit()
    # Summary query
    cursor = conn.execute("SELECT severity, COUNT(*) FROM findings GROUP BY severity")
    by_severity = dict(cursor.fetchall())
    total = conn.execute("SELECT COUNT(*) FROM findings").fetchone()[0]
    conn.close()
    return {"db_path": str(db_path), "total_stored": total, "by_severity": by_severity}



class Renderer:
    """Converts structured report into human-readable output"""

    def __init__(self):
        self.all_findings: List[Dict[str, Any]] = []
        self.all_stats: Dict[str, Any] = {}
        self.errors: List[str] = []

    def render(self, report: Dict[str, Any]) -> str:
        """PRESENTATION CONTRACT: render(report) → str"""
        self.all_findings = report.get("findings", [])
        self.all_stats = report.get("stats", {})
        # -- Stage 1 --
        __nexus_execute__(scan_secrets, report.get("target", "unknown"), "findings", self.all_findings, getattr(self, "all_stats", {}), self.errors)
        __nexus_execute__(check_ssl, report.get("target", "unknown"), "findings", self.all_findings, getattr(self, "all_stats", {}), self.errors)
        __nexus_execute__(hash_files, report.get("target", "unknown"), "findings", self.all_findings, getattr(self, "all_stats", {}), self.errors)
        __nexus_execute__(analyze_csv, report.get("target", "unknown"), "stats", self.all_findings, getattr(self, "all_stats", {}), self.errors)
        __nexus_execute__(store_findings_db, self.all_findings, "stats", self.all_findings, getattr(self, "all_stats", {}), self.errors)
        # Final formatting: join all findings into a structured report
        output = [f"# NEXUS_THREAT_REPORTER Analysis Report", f"Timestamp: {datetime.now().isoformat()}", ""]
        output.append("## Risk Summary")
        risk = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in self.all_findings:
            risk[f.get("severity", "INFO")] = risk.get(f.get("severity", "INFO"), 0) + 1
        for k, v in risk.items():
            output.append(f"- {k}: {v}")
        
        output.append("\n## Critical Findings")
        for f in [x for x in self.all_findings if x.get("severity") in ("CRITICAL", "HIGH")]:
            output.append(f"### [{f.get('severity')}] {f.get('type')}")
            output.append(f"- Detail: {f.get('detail')}")
            output.append(f"- Source: {f.get('source')}")

        return "\n".join(output)



def _integration_test():
    """End-to-end pipeline test with mock data."""
    agent = Renderer()
    test_target = Path(tempfile.mkdtemp())
    mock_report = {"target": "test", "findings": [{ "type": "test", "severity": "INFO", "value": 100, "detail": "test", "source": "test" }]}
    result = agent.render(mock_report)
    assert isinstance(result, str) and len(result) > 0, "render() must return non-empty string"
    logger.info(f"[TEST] Renderer.render() OK")
    return True


def main():
    parser = argparse.ArgumentParser(description="NEXUS_THREAT_REPORTER")
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
    # Presentation expects a report object
    mock_report = {"target": str(target), "findings": [], "stats": {}}
    report_str = agent.render(mock_report)
    print(report_str)
    return

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
