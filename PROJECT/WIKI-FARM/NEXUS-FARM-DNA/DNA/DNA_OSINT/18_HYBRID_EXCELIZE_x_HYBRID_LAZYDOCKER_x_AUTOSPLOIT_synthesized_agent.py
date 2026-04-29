#!/usr/bin/env python3
"""
EXCELIZE__X__HYBRID_LAZYDOCKER_x_AUTOSPLOIT [NEXUS SYNTHESIZED Gen-1]
Mission: Build an infrastructure monitoring and distributed orchestration agent
Heritage: EXCELIZE + HYBRID_LAZYDOCKER_x_AUTOSPLOIT
Role: collector | Security: none | Interface: cli
"""

import sys
import os
import re
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("EXCELIZE__X__HYBRID_LAZYDOCKER_x_AUTOSPLOIT")

# ── Collection Patterns ──────────────────────────────────────────────────
# [FILL:PATTERNS] Define 3-5 regex patterns this collector searches for.
# Example: PATTERNS = {"api_key": r"(?i)(api[_-]?key|token)\s*[:=]\s*[\w]{16,}"}
PATTERNS = {
    "sensitive_file": r"(?i)(password|secret|token|credential|apikey)",
    "config_exposure": r"(?i)(database_url|db_pass|aws_secret)",
    "hardcoded_ip": r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.?){4}\b",
}
# ─────────────────────────────────────────────────────────────────────────

# [FILL:EXTENSIONS] File extensions to scan. Add domain-specific ones.
TARGET_EXTENSIONS = {".py", ".js", ".json", ".yaml", ".yml", ".toml", ".env", ".cfg", ".ini", ".conf"}


class DataCollector:
    """Scans targets and extracts findings matching predefined patterns."""

    def __init__(self):
        self.stats = {"items_collected": 0, "files_scanned": 0, "errors": 0}

    def collect(self, target: Path) -> list[dict]:
        """Scan target directory for pattern matches."""
        findings = []

        if not target.exists():
            logger.error(f"Target not found: {target}")
            return findings

        for fpath in target.rglob("*"):
            if not fpath.is_file():
                continue
            if fpath.suffix.lower() not in TARGET_EXTENSIONS:
                continue
            if ".git" in fpath.parts or "__pycache__" in fpath.parts:
                continue

            try:
                content = fpath.read_text(encoding="utf-8", errors="ignore")
                self.stats["files_scanned"] += 1

                for rule_name, pattern in PATTERNS.items():
                    for match in re.finditer(pattern, content):
                        line_num = content[:match.start()].count("\n") + 1
                        findings.append({
                            "type": rule_name,
                            "content": match.group(0)[:200],
                            "file": str(fpath.relative_to(target)),
                            "line": line_num,
                            "severity": "HIGH" if "secret" in rule_name.lower() or "password" in rule_name.lower() else "MEDIUM",
                        })
                        self.stats["items_collected"] += 1

            except Exception as e:
                self.stats["errors"] += 1
                logger.debug(f"Skip {fpath.name}: {e}")

        logger.info(f"[SCAN] {self.stats['files_scanned']} files, {self.stats['items_collected']} findings")
        return findings


def main():
    parser = argparse.ArgumentParser(description="EXCELIZE__X__HYBRID_LAZYDOCKER_x_AUTOSPLOIT")
    parser.add_argument("--target", required=True, help="Directory to scan")
    parser.add_argument("--output", default="collection_report.json", help="Output JSON")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    collector = DataCollector()
    findings = collector.collect(target)

    report = {
        "agent": "EXCELIZE__X__HYBRID_LAZYDOCKER_x_AUTOSPLOIT",
        "version": "1.0-gen1",
        "timestamp": datetime.now().isoformat(),
        "target": str(target),
        "stats": collector.stats,
        "findings": findings
    }

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info(f"[DONE] {len(findings)} findings -> {output}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
