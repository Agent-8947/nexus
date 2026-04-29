#!/usr/bin/env python3
"""
HYBRID_OSINT_MASTER v1.0 [NEXUS SYNTHESIZED]
Heritage: 30-DAYS-OF-PYTHON x 1EARN
Role: collector | Security: critical | Interface: cli
Mission: Advanced multi-source OSINT collection with integrated credential discovery.
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
logger = logging.getLogger("OSINT-MASTER")

# ── Collection Patterns ──────────────────────────────────────────────────
PATTERNS = {
    "api_key": r"(?i)(api[_-]?key|token|access[_-]?key)\s*[:=]\s*['\"]([\w\.-]{16,})['\"]",
    "email_leak": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "env_vars": r"(?m)^\s*([A-Z_]{4,})\s*=\s*(.*)$",
    "private_key": r"-----BEGIN [A-Z ]+ PRIVATE KEY-----",
}
# ─────────────────────────────────────────────────────────────────────────

TARGET_EXTENSIONS = {".py", ".sh", ".env", ".yaml", ".json", ".log", ".txt", ".js"}


class OsintCollector:
    """Scans repositories and logs for leaked secrets and identities."""

    def __init__(self):
        self.stats = {"items_collected": 0, "files_scanned": 0, "errors": 0}

    def collect(self, target: Path) -> list[dict]:
        """Scan target directory for OSINT signals."""
        findings = []

        if not target.exists():
            logger.error(f"Target not found: {target}")
            return findings

        for fpath in target.rglob("*"):
            if not fpath.is_file():
                continue
            if fpath.suffix.lower() not in TARGET_EXTENSIONS:
                continue
            if any(p in fpath.parts for p in [".git", "node_modules", "__pycache__"]):
                continue

            try:
                content = fpath.read_text(encoding="utf-8", errors="ignore")
                self.stats["files_scanned"] += 1

                for rule_name, pattern in PATTERNS.items():
                    for match in re.finditer(pattern, content):
                        line_num = content[:match.start()].count("\n") + 1
                        findings.append({
                            "type": rule_name,
                            "content": match.group(0).strip()[:150],
                            "file": str(fpath.relative_to(target)),
                            "line": line_num,
                            "severity": "CRITICAL" if "key" in rule_name else "MEDIUM",
                        })
                        self.stats["items_collected"] += 1

            except Exception as e:
                self.stats["errors"] += 1
                logger.debug(f"Skip {fpath.name}: {e}")

        logger.info(f"[OSINT] Scanned {self.stats['files_scanned']} files, found {self.stats['items_collected']} signals")
        return findings


def main():
    parser = argparse.ArgumentParser(description="HYBRID_OSINT_MASTER")
    parser.add_argument("--target", required=True, help="Directory to scan")
    parser.add_argument("--output", default="osint_report.json", help="Output JSON")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    collector = OsintCollector()
    findings = collector.collect(target)

    report = {
        "agent": "HYBRID_OSINT_MASTER",
        "heritage": "30-DAYS-OF-PYTHON x 1EARN",
        "timestamp": datetime.now().isoformat(),
        "stats": collector.stats,
        "findings": findings
    }

    output = Path(args.output).resolve()
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logger.info(f"[DONE] Findings saved to {output}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
