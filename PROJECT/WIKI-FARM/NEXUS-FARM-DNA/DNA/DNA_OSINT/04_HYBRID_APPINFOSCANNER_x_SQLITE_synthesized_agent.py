#!/usr/bin/env python3
"""
HYBRID_APPINFOSCANNER_x_SQLITE v2.0 [NEXUS SYNTHESIZED]
========================================================
Heritage: AppInfoScanner (Mobile OSINT) + SQLite (Persistent Storage)
Role:     COLLECTOR - Persistent storage and historical auditing of app metadata
Mission:  Build an OSINT intelligence gathering and analysis pipeline
Input:    App package name or batch file
Output:   SQLite database with audit trail + JSON export
"""

import sys
import json
import sqlite3
import logging
import argparse
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS-APPDB")

DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS app_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package TEXT NOT NULL,
    category TEXT DEFAULT 'unknown',
    permissions TEXT,
    risk_score REAL DEFAULT 0.0,
    raw_data TEXT,
    ts TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_package ON app_audit(package);
CREATE INDEX IF NOT EXISTS idx_ts ON app_audit(ts);
"""


class AppAuditDatabase:
    """Persistent SQLite store for mobile app OSINT metadata."""

    def __init__(self, db_path: str = "app_osint.db"):
        self.db_path = db_path
        self.stats = {"inserted": 0, "queried": 0, "errors": 0}
        self._init_db()

    def _init_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.executescript(DB_SCHEMA)
            logger.info(f"[DB] Initialized: {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"[DB] Init failed: {e}")
            self.stats["errors"] += 1

    def log_app(self, package: str, data: dict) -> bool:
        """Insert app metadata into the audit database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO app_audit (package, category, permissions, risk_score, raw_data, ts) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        package,
                        data.get("category", "unknown"),
                        json.dumps(data.get("permissions", [])),
                        data.get("risk_score", 0.0),
                        json.dumps(data),
                        datetime.now().isoformat()
                    )
                )
            self.stats["inserted"] += 1
            logger.info(f"[+] Logged: {package}")
            return True
        except sqlite3.Error as e:
            logger.error(f"[DB] Insert failed for {package}: {e}")
            self.stats["errors"] += 1
            return False

    def query_history(self, package: str) -> list[dict]:
        """Retrieve audit history for a package."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(
                    "SELECT * FROM app_audit WHERE package = ? ORDER BY ts DESC", (package,)
                ).fetchall()
            self.stats["queried"] += 1
            return [dict(r) for r in rows]
        except sqlite3.Error as e:
            logger.error(f"[DB] Query failed: {e}")
            return []

    def export_json(self, output_path: Path) -> int:
        """Export entire database to JSON."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute("SELECT * FROM app_audit ORDER BY ts DESC").fetchall()
            records = [dict(r) for r in rows]
            output_path.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
            logger.info(f"[EXPORT] {len(records)} records -> {output_path}")
            return len(records)
        except Exception as e:
            logger.error(f"[EXPORT] Failed: {e}")
            return 0


def main():
    parser = argparse.ArgumentParser(description="NEXUS App OSINT Database Manager")
    parser.add_argument("--package", help="App package to log")
    parser.add_argument("--data", default="{}", help="JSON metadata string")
    parser.add_argument("--query", help="Query history for a package")
    parser.add_argument("--export", help="Export DB to JSON file")
    parser.add_argument("--db", default="app_osint.db", help="Database file path")
    args = parser.parse_args()

    db = AppAuditDatabase(args.db)

    if args.package:
        data = json.loads(args.data)
        db.log_app(args.package, data)
    elif args.query:
        history = db.query_history(args.query)
        print(json.dumps(history, indent=2, ensure_ascii=False))
    elif args.export:
        db.export_json(Path(args.export))
    else:
        parser.print_help()

    logger.info(f"[STATS] {db.stats}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
