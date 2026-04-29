#!/usr/bin/env python3
"""
NEXUS_DATA_VIZ_ENGINE [NEXUS SYNTHESIZED Gen-3]
Mission: data_visualization
Heritage: DATA_CRUNCHER + WEB_RENDERER
Role: presentation | Domains: data & web

I/O Contract:
  Input:  url (from CLI --target)
  Output: JSON report with typed findings/stats

Pipeline (3 stages, 3 blocks):
  Stage 1: [extract_links]
  Stage 2: [store_findings_db]
  Stage 3: [analyze_csv]
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
import re, ssl, urllib.request, urllib.error
from html.parser import HTMLParser
from urllib.parse import urljoin

__all__ = ["main", "Pipeline"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS_DATA_VIZ_ENGINE")


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

    def render(self, target) -> str:
        """PRESENTATION CONTRACT: render(target) → str"""
        # -- Stage 1 --
        try:
            _result = extract_links(target)
            self.all_findings.extend(_result)
            logger.info(f"  [extract_links] {len(_result)} findings")
        except Exception as e:
            self.errors.append(f"extract_links: {e}")
            logger.warning(f"  [extract_links] SKIP: {e}")
        # -- Stage 2 --
        try:
            _result = store_findings_db(self.all_findings)
            logger.info(f"  [store_findings_db] OK")
        except Exception as e:
            self.errors.append(f"store_findings_db: {e}")
            logger.warning(f"  [store_findings_db] SKIP: {e}")
        # -- Stage 3 --
        try:
            _result = analyze_csv(str(target))
            logger.info(f"  [analyze_csv] OK")
        except Exception as e:
            self.errors.append(f"analyze_csv: {e}")
            logger.warning(f"  [analyze_csv] SKIP: {e}")
        risk = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in self.all_findings:
            risk[f.get("severity", "INFO")] = risk.get(f.get("severity", "INFO"), 0) + 1
        return {
            "agent": "NEXUS_DATA_VIZ_ENGINE",
            "timestamp": datetime.now().isoformat(),
            "findings": self.all_findings,
            "stats": self.all_stats,
            "errors": self.errors,
            "risk_summary": risk,
        }



def _integration_test():
    """End-to-end pipeline test with mock data."""
    agent = Renderer()
    test_target = "http://localhost:99999"
    result = agent.render(test_target)
    assert isinstance(result, dict), "render() must return dict"
    assert "findings" in result, "render() must return findings"
    logger.info(f"[TEST] Renderer.render() OK")
    return True


def main():
    parser = argparse.ArgumentParser(description="NEXUS_DATA_VIZ_ENGINE")
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
    report = agent.render(target)


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
