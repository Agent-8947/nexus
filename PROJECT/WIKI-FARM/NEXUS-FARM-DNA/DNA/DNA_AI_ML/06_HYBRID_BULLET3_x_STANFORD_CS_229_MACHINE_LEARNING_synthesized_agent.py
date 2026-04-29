#!/usr/bin/env python3
"""
BULLET3__X__STANFORD_CS_229_MACHINE_LEARNING [NEXUS SYNTHESIZED Gen-1]
Mission: Build an AI model monitoring and anomaly detection system
Heritage: BULLET3 + STANFORD_CS_229_MACHINE_LEARNING
Role: storage | Security: none | Interface: api
"""

import sys
import json
import sqlite3
import logging
import argparse
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("BULLET3__X__STANFORD_CS_229_MACHINE_LEARNING")


class PersistentStore:
    """SQLite-backed persistent storage for NEXUS agent data."""

    def __init__(self, db_path: str = "nexus_store.db"):
        self.db_path = db_path
        self.stats = {"inserted": 0, "queried": 0}
        self._init()

    def _init(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT, category TEXT, data TEXT, ts TEXT
            )""")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_source ON records(source)")

    def insert(self, source: str, category: str, data: dict):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO records (source, category, data, ts) VALUES (?,?,?,?)",
                         (source, category, json.dumps(data), datetime.now().isoformat()))
        self.stats["inserted"] += 1

    def query(self, source: str = None, limit: int = 100) -> list[dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            if source:
                rows = conn.execute("SELECT * FROM records WHERE source=? ORDER BY ts DESC LIMIT ?", (source, limit)).fetchall()
            else:
                rows = conn.execute("SELECT * FROM records ORDER BY ts DESC LIMIT ?", (limit,)).fetchall()
        self.stats["queried"] += 1
        return [dict(r) for r in rows]

    def export_json(self, path: Path):
        records = self.query(limit=10000)
        path.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
        logger.info(f"[EXPORT] {len(records)} records -> {path}")


def main():
    parser = argparse.ArgumentParser(description="BULLET3__X__STANFORD_CS_229_MACHINE_LEARNING")
    parser.add_argument("--ingest", help="JSON file to ingest")
    parser.add_argument("--query", help="Query by source name")
    parser.add_argument("--export", help="Export DB to JSON")
    parser.add_argument("--db", default="nexus_store.db", help="DB path")
    args = parser.parse_args()

    store = PersistentStore(args.db)
    if args.ingest:
        data = json.loads(Path(args.ingest).read_text(encoding="utf-8"))
        items = data if isinstance(data, list) else data.get("findings", data.get("records", []))
        for item in items:
            store.insert(item.get("source", "unknown"), item.get("type", "misc"), item)
        logger.info(f"[DONE] Ingested {store.stats['inserted']} records")
    elif args.query:
        results = store.query(args.query)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    elif args.export:
        store.export_json(Path(args.export))
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
