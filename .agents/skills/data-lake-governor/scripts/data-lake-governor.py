#!/usr/bin/env python3
"""
DATA-LAKE-GOVERNOR [NEXUS SYNTHESIZED v2.0]
Mission: Data lifecycle management — archive old data, deduplicate events, verify integrity
Role: operator | Security: read-write | Interface: cli
"""

import sys
import json
import logging
import argparse
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("DATA-LAKE-GOVERNOR")

# ── Lifecycle Policies ───────────────────────────────────────────────────
HOT_RETENTION_DAYS = 90
COLD_RETENTION_DAYS = 365
COMPRESSION_ALGO = "LZ4"
# ─────────────────────────────────────────────────────────────────────────


class DataInventoryScanner:
    """Scans a data directory and classifies files by age tier."""

    def __init__(self, hot_days: int = HOT_RETENTION_DAYS, cold_days: int = COLD_RETENTION_DAYS):
        self.hot_days = hot_days
        self.cold_days = cold_days
        self.stats = {"total_files": 0, "hot": 0, "warm": 0, "cold": 0, "total_bytes": 0}

    def scan(self, data_dir: Path) -> list[dict]:
        now = datetime.now()
        inventory = []
        for f in data_dir.rglob("*"):
            if not f.is_file():
                continue
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            age_days = (now - mtime).days
            size = f.stat().st_size
            sha256 = self._hash_file(f)

            if age_days <= self.hot_days:
                tier = "HOT"
                self.stats["hot"] += 1
            elif age_days <= self.cold_days:
                tier = "WARM"
                self.stats["warm"] += 1
            else:
                tier = "COLD"
                self.stats["cold"] += 1

            inventory.append({
                "path": str(f),
                "filename": f.name,
                "size_bytes": size,
                "modified": mtime.isoformat(),
                "age_days": age_days,
                "tier": tier,
                "sha256": sha256,
            })
            self.stats["total_files"] += 1
            self.stats["total_bytes"] += size

        return inventory

    @staticmethod
    def _hash_file(filepath: Path, chunk_size: int = 65536) -> str:
        h = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(chunk_size):
                h.update(chunk)
        return h.hexdigest()


class Deduplicator:
    """Identifies duplicate files by SHA-256 hash."""

    @staticmethod
    def find_duplicates(inventory: list[dict]) -> list[dict]:
        hash_map = defaultdict(list)
        for item in inventory:
            hash_map[item["sha256"]].append(item)

        duplicates = []
        for sha, items in hash_map.items():
            if len(items) > 1:
                items_sorted = sorted(items, key=lambda x: x["age_days"])
                keep = items_sorted[0]
                for dup in items_sorted[1:]:
                    duplicates.append({
                        "duplicate": dup["path"],
                        "original": keep["path"],
                        "sha256": sha,
                        "wasted_bytes": dup["size_bytes"],
                        "action": "SAFE_TO_DELETE",
                    })
        return duplicates


class ArchivalPlanner:
    """Generates migration plan for WARM/COLD tier data."""

    @staticmethod
    def plan(inventory: list[dict]) -> list[dict]:
        migrations = []
        for item in inventory:
            if item["tier"] == "WARM":
                migrations.append({
                    "file": item["path"],
                    "current_tier": "WARM",
                    "target_tier": "COLD_STORAGE",
                    "compression": COMPRESSION_ALGO,
                    "sha256_before": item["sha256"],
                    "action": "COMPRESS_AND_ARCHIVE",
                })
            elif item["tier"] == "COLD":
                migrations.append({
                    "file": item["path"],
                    "current_tier": "COLD",
                    "target_tier": "GLACIER_ARCHIVE",
                    "compression": COMPRESSION_ALGO,
                    "sha256_before": item["sha256"],
                    "action": "DEEP_ARCHIVE",
                })
        return migrations


def main():
    parser = argparse.ArgumentParser(description="DATA-LAKE-GOVERNOR: Lifecycle & Dedup Manager")
    parser.add_argument("--input", required=True, help="Data directory to scan")
    parser.add_argument("--output", default="data_lake_report.json", help="Output report")
    parser.add_argument("--dedup", action="store_true", help="Run deduplication analysis")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists() or not input_path.is_dir():
        logger.error(f"Input directory not found: {input_path}")
        sys.exit(1)

    scanner = DataInventoryScanner()
    inventory = scanner.scan(input_path)

    logger.info(f"[*] Scanned {scanner.stats['total_files']} files ({scanner.stats['total_bytes'] / 1024 / 1024:.1f} MB)")
    logger.info(f"    HOT: {scanner.stats['hot']} | WARM: {scanner.stats['warm']} | COLD: {scanner.stats['cold']}")

    duplicates = Deduplicator.find_duplicates(inventory) if args.dedup else []
    migrations = ArchivalPlanner.plan(inventory)

    wasted = sum(d["wasted_bytes"] for d in duplicates)

    report = {
        "agent": "DATA-LAKE-GOVERNOR",
        "version": "2.0-nexus",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_files": scanner.stats["total_files"],
            "total_size_mb": round(scanner.stats["total_bytes"] / 1024 / 1024, 2),
            "by_tier": {"hot": scanner.stats["hot"], "warm": scanner.stats["warm"], "cold": scanner.stats["cold"]},
            "duplicates_found": len(duplicates),
            "wasted_bytes": wasted,
            "migrations_planned": len(migrations),
        },
        "duplicates": duplicates[:50],
        "migration_plan": migrations[:100],
    }

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info(f"[DONE] Data lake report -> {output}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
