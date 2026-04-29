#!/usr/bin/env python3
"""
HYBRID_TROUBLESHOOTING_x_CRATE v2.0 [NEXUS OSINT COLLECTOR]
=============================================================
Heritage: Troubleshooting (Batch Diagnostics) + Crate (Scalable Storage)
Role:     COLLECTOR - Scans filesystem for OSINT artifacts (secrets, IPs, domains)
Output:   JSON report consumed by HYBRID_AUTOGLUON_x_ALLUXIO (Analyzer)

DNA Signature: Network=0.6, Intelligence=0.8, Autonomy=0.6, Hardware=0.3, Stealth=0.0, Scale=0.5
Security:      none (read-only passive scan)
Interface:     CLI
Latency:       batch + real-time hybrid
"""

import sys
import os
import re
import json
import time
import logging
import argparse
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Generator

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS-COLLECTOR")

# ── Detection Rules ──────────────────────────────────────────────────────
DETECTION_RULES = {
    "aws_key": {
        "pattern": re.compile(r"(?:AKIA|ASIA)[A-Z0-9]{16}", re.ASCII),
        "severity": "CRITICAL",
        "category": "credential"
    },
    "generic_secret": {
        "pattern": re.compile(
            r"(?:password|secret|token|api_key|apikey|auth)\s*[=:]\s*['\"]?([^\s'\"]{8,})",
            re.IGNORECASE
        ),
        "severity": "HIGH",
        "category": "credential"
    },
    "private_key_header": {
        "pattern": re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"),
        "severity": "CRITICAL",
        "category": "credential"
    },
    "ipv4_private": {
        "pattern": re.compile(
            r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
            r"172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}|"
            r"192\.168\.\d{1,3}\.\d{1,3})\b"
        ),
        "severity": "MEDIUM",
        "category": "network"
    },
    "ipv4_public": {
        "pattern": re.compile(
            r"\b(?!(?:10|127|172\.(?:1[6-9]|2\d|3[01])|192\.168)\.)(?:\d{1,3}\.){3}\d{1,3}\b"
        ),
        "severity": "LOW",
        "category": "network"
    },
    "domain_internal": {
        "pattern": re.compile(
            r"\b[\w-]+\.(?:internal|local|corp|intra|dev|staging)\b", re.IGNORECASE
        ),
        "severity": "MEDIUM",
        "category": "network"
    },
    "email_corporate": {
        "pattern": re.compile(r"\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.(?:com|org|io|net|dev)\b"),
        "severity": "LOW",
        "category": "identity"
    },
    "jwt_token": {
        "pattern": re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]+"),
        "severity": "HIGH",
        "category": "credential"
    },
    "connection_string": {
        "pattern": re.compile(
            r"(?:mongodb|postgres|mysql|redis|amqp)://[^\s'\"]+", re.IGNORECASE
        ),
        "severity": "CRITICAL",
        "category": "credential"
    }
}

# File types worth scanning (by extension)
SCANNABLE_EXTS = {
    ".py", ".js", ".ts", ".go", ".rs", ".java", ".rb", ".php", ".sh", ".bash",
    ".yml", ".yaml", ".json", ".toml", ".ini", ".cfg", ".conf", ".env",
    ".md", ".txt", ".log", ".xml", ".html", ".tf", ".hcl",
    ".dockerfile", ".properties", ".gradle"
}

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".tox", "dist", "build"}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB


class OsintCollector:
    """Deep filesystem scanner for OSINT artifacts."""

    def __init__(self, rules: dict = None, max_file_size: int = MAX_FILE_SIZE):
        self.rules = rules or DETECTION_RULES
        self.max_file_size = max_file_size
        self.stats = {"files_scanned": 0, "files_skipped": 0, "findings": 0, "errors": 0}

    def scan_directory(self, root: Path) -> Generator[dict, None, None]:
        """Recursively scan a directory tree. Yields findings."""
        logger.info(f"[SCAN] Target: {root}")
        
        for dirpath, dirnames, filenames in os.walk(root):
            # Prune skip dirs in-place
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

            for fname in filenames:
                fpath = Path(dirpath) / fname

                # Filter by extension
                if fpath.suffix.lower() not in SCANNABLE_EXTS and fpath.name.lower() not in (
                    "dockerfile", ".env", ".env.local", ".env.production", "makefile"
                ):
                    self.stats["files_skipped"] += 1
                    continue

                # Size guard
                try:
                    if fpath.stat().st_size > self.max_file_size:
                        self.stats["files_skipped"] += 1
                        continue
                except OSError:
                    self.stats["errors"] += 1
                    continue

                yield from self._scan_file(fpath, root)

    def _scan_file(self, fpath: Path, root: Path) -> Generator[dict, None, None]:
        """Scan a single file against all detection rules."""
        try:
            content = fpath.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            self.stats["errors"] += 1
            logger.debug(f"[SKIP] {fpath.name}: {e}")
            return

        self.stats["files_scanned"] += 1
        rel_path = str(fpath.relative_to(root))

        for rule_id, rule in self.rules.items():
            for match in rule["pattern"].finditer(content):
                # Calculate line number
                line_no = content[:match.start()].count("\n") + 1
                # Extract context (the line containing the match)
                line_start = content.rfind("\n", 0, match.start()) + 1
                line_end   = content.find("\n", match.end())
                line_end   = line_end if line_end != -1 else len(content)
                context    = content[line_start:line_end].strip()

                # Redact the actual secret (show only first 8 chars)
                raw = match.group(0)
                redacted = raw[:8] + "****" if len(raw) > 12 else raw[:4] + "****"

                self.stats["findings"] += 1
                yield {
                    "rule_id":    rule_id,
                    "severity":   rule["severity"],
                    "category":   rule["category"],
                    "file":       rel_path,
                    "line":       line_no,
                    "match":      redacted,
                    "context":    context[:200],
                    "checksum":   hashlib.md5(raw.encode()).hexdigest()[:12]
                }


def run_scan(target: Path, output: Path, fmt: str = "json"):
    """Execute full scan and produce report."""
    collector = OsintCollector()
    findings  = list(collector.scan_directory(target))

    # Sort: CRITICAL first
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    findings.sort(key=lambda f: severity_order.get(f["severity"], 9))

    report = {
        "agent":     "HYBRID_TROUBLESHOOTING_x_CRATE",
        "version":   "2.0",
        "timestamp": datetime.now().isoformat(),
        "target":    str(target),
        "stats":     collector.stats,
        "findings":  findings
    }

    # Output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info(f"[DONE] Report -> {output}")

    # Summary
    by_sev = {}
    for f in findings:
        by_sev[f["severity"]] = by_sev.get(f["severity"], 0) + 1

    print(f"\n{'='*60}")
    print(f"  NEXUS OSINT COLLECTOR v2.0 -- SCAN COMPLETE")
    print(f"{'='*60}")
    print(f"  Files scanned:  {collector.stats['files_scanned']}")
    print(f"  Files skipped:  {collector.stats['files_skipped']}")
    print(f"  Total findings: {collector.stats['findings']}")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        count = by_sev.get(sev, 0)
        if count:
            print(f"    {sev:10s}: {count}")
    print(f"{'='*60}")

    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="NEXUS OSINT Collector v2.0 -- Filesystem secret scanner"
    )
    parser.add_argument("--target", default=".", help="Directory to scan (default: cwd)")
    parser.add_argument("--output", default="osint_collector_report.json", help="Output JSON")
    parser.add_argument("--verbose", action="store_true", help="Show every finding")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        run_scan(Path(args.target).resolve(), Path(args.output).resolve())
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
