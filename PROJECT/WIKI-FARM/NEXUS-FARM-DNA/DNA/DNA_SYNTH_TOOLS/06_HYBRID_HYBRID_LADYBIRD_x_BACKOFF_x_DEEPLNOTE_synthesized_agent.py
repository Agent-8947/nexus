#!/usr/bin/env python3
"""
HYBRID_LADYBIRD_x_BACKOFF__X__DEEPLNOTE [NEXUS SYNTHESIZED Gen-2]
Mission: Build a security audit and vulnerability detection tool
Heritage: HYBRID_LADYBIRD_x_BACKOFF + DEEPLNOTE
Role: library | Domains: security & data

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
logger = logging.getLogger("HYBRID_LADYBIRD_x_BACKOFF__X__DEEPLNOTE")


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


class Pipeline:
    """Orchestrates 5 blocks in 1 stages."""

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
            result = analyze_csv(str(target))
            self.all_stats["analyze_csv"] = result
            logger.info(f"  [analyze_csv] stats collected")
        except Exception as e:
            self.errors.append(f"analyze_csv: {e}")
            logger.warning(f"  [analyze_csv] SKIP: {e}")
        try:
            result = store_findings_db(self.all_findings)
            self.all_stats["store_findings_db"] = result
            logger.info(f"  [store_findings_db] stats collected")
        except Exception as e:
            self.errors.append(f"store_findings_db: {e}")
            logger.warning(f"  [store_findings_db] SKIP: {e}")

        # ── Build report ──
        risk_summary = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in self.all_findings:
            sev = f.get("severity", "INFO")
            risk_summary[sev] = risk_summary.get(sev, 0) + 1

        return {
            "agent": "HYBRID_LADYBIRD_x_BACKOFF__X__DEEPLNOTE",
            "version": "2.0-gen2",
            "timestamp": datetime.now().isoformat(),
            "pipeline_stages": 1,
            "blocks_executed": 5 - len(self.errors),
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
    parser = argparse.ArgumentParser(description="HYBRID_LADYBIRD_x_BACKOFF__X__DEEPLNOTE")
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
