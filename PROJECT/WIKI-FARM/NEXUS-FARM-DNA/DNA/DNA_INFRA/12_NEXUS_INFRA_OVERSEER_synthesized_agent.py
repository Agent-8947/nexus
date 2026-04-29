#!/usr/bin/env python3
"""
NEXUS_INFRA_OVERSEER [NEXUS SYNTHESIZED Gen-4]
Mission: system_metrics_and_auditing
Heritage: GRAFANA_CORE + GITLEAKS_ENGINE
Role: orchestrator | Domains: infra & data

I/O Contract:
  Input:  hostname (from CLI --target)
  Output: JSON report with typed findings/stats

Pipeline (3 stages, 5 blocks):
  Stage 1: [check_ports, system_info, process_list]
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
import os, re, socket, platform, subprocess
import re, csv, sqlite3

__all__ = ["main", "Pipeline"]


logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS_INFRA_OVERSEER")

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



class Orchestrator:
    """Coordinates multiple blocks in a pipeline"""

    def __init__(self):
        self.all_findings: List[Dict[str, Any]] = []
        self.all_stats: Dict[str, Any] = {}
        self.errors: List[str] = []

    def run(self, target) -> Dict[str, Any]:
        """ORCHESTRATOR CONTRACT: run(target) → Dict[str, Any]"""
        # -- Stage 1 --
        __nexus_execute__(check_ports, target, "port_report", self.all_findings, getattr(self, "all_stats", {}), self.errors)
        __nexus_execute__(system_info, target, "system_info", self.all_findings, getattr(self, "all_stats", {}), self.errors)
        __nexus_execute__(process_list, target, "findings", self.all_findings, getattr(self, "all_stats", {}), self.errors)
        # -- Stage 2 --
        __nexus_execute__(store_findings_db, self.all_findings, "stats", self.all_findings, getattr(self, "all_stats", {}), self.errors)
        # -- Stage 3 --
        __nexus_execute__(analyze_csv, target, "stats", self.all_findings, getattr(self, "all_stats", {}), self.errors)
        risk = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in self.all_findings:
            risk[f.get("severity", "INFO")] = risk.get(f.get("severity", "INFO"), 0) + 1
        return {
            "agent": "NEXUS_INFRA_OVERSEER",
            "timestamp": datetime.now().isoformat(),
            "findings": self.all_findings,
            "stats": self.all_stats,
            "errors": self.errors,
            "risk_summary": risk,
        }



def _integration_test():
    """End-to-end pipeline test with mock data."""
    agent = Orchestrator()
    test_target = "127.0.0.1"
    result = agent.run(test_target)
    assert isinstance(result, dict), "run() must return dict"
    assert "findings" in result, "run() must return findings"
    logger.info(f"[TEST] Orchestrator.run() OK")
    return True


def main():
    parser = argparse.ArgumentParser(description="NEXUS_INFRA_OVERSEER")
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
