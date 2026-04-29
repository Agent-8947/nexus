#!/usr/bin/env python3
"""
DATABASE-SHARD-MANAGER [NEXUS SYNTHESIZED v2.0]
Mission: Analyze database metrics, detect bloat, recommend sharding and index strategies
Role: analyzer | Security: read-only | Interface: cli
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("DATABASE-SHARD-MANAGER")

# ── Thresholds ───────────────────────────────────────────────────────────
INDEX_BLOAT_RATIO = 0.20       # 20% buffer cache overshoot -> shard trigger
REPLICATION_LAG_CRITICAL = 30  # seconds
TABLE_ROW_SHARD_TRIGGER = 50_000_000
LOCK_TIMEOUT_MS = 2000
DEAD_TUPLE_RATIO = 0.15       # 15% dead tuples -> vacuum needed
# ─────────────────────────────────────────────────────────────────────────


class TableAnalyzer:
    """Evaluates table health from pg_stat metrics."""

    def __init__(self):
        self.stats = {"tables_analyzed": 0, "shard_candidates": 0, "vacuum_needed": 0, "slow_queries": 0}

    def analyze_tables(self, tables: list[dict]) -> list[dict]:
        findings = []
        for t in tables:
            name = t.get("table_name", "unknown")
            rows = t.get("live_tuples", 0)
            dead = t.get("dead_tuples", 0)
            index_size_mb = t.get("index_size_mb", 0)
            buffer_cache_mb = t.get("buffer_cache_mb", float("inf"))
            last_vacuum = t.get("last_vacuum", "never")

            issues = []
            recommendations = []

            # Sharding trigger
            if rows >= TABLE_ROW_SHARD_TRIGGER:
                issues.append("SHARD_CANDIDATE")
                recommendations.append(f"Table exceeds {TABLE_ROW_SHARD_TRIGGER:,} rows. Implement hash-based horizontal partitioning.")
                self.stats["shard_candidates"] += 1

            # Index bloat
            if buffer_cache_mb > 0 and (index_size_mb / buffer_cache_mb) > (1 + INDEX_BLOAT_RATIO):
                issues.append("INDEX_BLOAT")
                recommendations.append(f"Index size ({index_size_mb}MB) exceeds buffer cache ({buffer_cache_mb}MB) by >{INDEX_BLOAT_RATIO*100}%.")

            # Dead tuple ratio
            total = rows + dead
            if total > 0 and (dead / total) > DEAD_TUPLE_RATIO:
                issues.append("VACUUM_NEEDED")
                recommendations.append(f"Dead tuple ratio: {dead/total:.1%}. Run VACUUM ANALYZE. Last vacuum: {last_vacuum}.")
                self.stats["vacuum_needed"] += 1

            if issues:
                findings.append({
                    "table": name,
                    "live_tuples": rows,
                    "dead_tuples": dead,
                    "index_size_mb": index_size_mb,
                    "issues": issues,
                    "recommendations": recommendations,
                    "priority": "P0-IMMEDIATE" if "SHARD_CANDIDATE" in issues else "P1-URGENT",
                })

            self.stats["tables_analyzed"] += 1
        return findings


class ReplicaMonitor:
    """Checks replication lag across read-replicas."""

    @staticmethod
    def check(replicas: list[dict]) -> list[dict]:
        findings = []
        for r in replicas:
            lag_sec = r.get("lag_seconds", 0)
            if lag_sec > REPLICATION_LAG_CRITICAL:
                findings.append({
                    "replica_id": r.get("replica_id", "unknown"),
                    "lag_seconds": lag_sec,
                    "issue": "REPLICATION_LAG_CRITICAL",
                    "priority": "P0-IMMEDIATE",
                    "remediation": f"Lag {lag_sec}s exceeds {REPLICATION_LAG_CRITICAL}s threshold. Check WAL sender, network, or I/O bottleneck.",
                })
        return findings


class QueryProfiler:
    """Flags slow queries from pg_stat_statements-like exports."""

    def __init__(self):
        self.slow_count = 0

    def profile(self, queries: list[dict], threshold_ms: float = 500) -> list[dict]:
        findings = []
        for q in queries:
            mean_ms = q.get("mean_exec_time_ms", 0)
            calls = q.get("calls", 0)
            if mean_ms > threshold_ms and calls > 10:
                self.slow_count += 1
                findings.append({
                    "query_hash": q.get("queryid", "unknown"),
                    "query_preview": q.get("query", "")[:200],
                    "mean_exec_time_ms": mean_ms,
                    "calls": calls,
                    "total_time_ms": round(mean_ms * calls, 1),
                    "issue": "SLOW_QUERY",
                    "priority": "P1-URGENT" if mean_ms > 2000 else "P2-REVIEW",
                    "remediation": "Run EXPLAIN ANALYZE. Consider adding index or rewriting query.",
                })
        findings.sort(key=lambda x: x["total_time_ms"], reverse=True)
        return findings


def main():
    parser = argparse.ArgumentParser(description="DATABASE-SHARD-MANAGER: DB Health & Scaling Advisor")
    parser.add_argument("--input", required=True, help="Database metrics JSON")
    parser.add_argument("--output", default="db_shard_report.json", help="Output report")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        logger.error(f"Input not found: {input_path}")
        sys.exit(1)

    data = json.loads(input_path.read_text(encoding="utf-8"))

    table_analyzer = TableAnalyzer()
    query_profiler = QueryProfiler()

    table_findings = table_analyzer.analyze_tables(data.get("tables", []))
    replica_findings = ReplicaMonitor.check(data.get("replicas", []))
    query_findings = query_profiler.profile(data.get("queries", []))

    all_findings = table_findings + replica_findings + query_findings
    logger.info(f"[*] {len(all_findings)} issues found across {table_analyzer.stats['tables_analyzed']} tables")

    report = {
        "agent": "DATABASE-SHARD-MANAGER",
        "version": "2.0-nexus",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "tables_analyzed": table_analyzer.stats["tables_analyzed"],
            "shard_candidates": table_analyzer.stats["shard_candidates"],
            "vacuum_needed": table_analyzer.stats["vacuum_needed"],
            "slow_queries": query_profiler.slow_count,
            "replica_lag_alerts": len(replica_findings),
            "verdict": "ACTION-REQUIRED" if any(f.get("priority") == "P0-IMMEDIATE" for f in all_findings) else "HEALTHY",
        },
        "findings": all_findings,
    }

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info(f"[DONE] DB report -> {output}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
