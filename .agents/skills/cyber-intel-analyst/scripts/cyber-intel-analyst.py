#!/usr/bin/env python3
"""
CYBER-INTEL-ANALYST [NEXUS SYNTHESIZED v2.0]
Mission: OSINT threat intelligence aggregation and IoC correlation
Role: collector | Security: read-only | Interface: cli
"""

import sys
import json
import logging
import argparse
import re
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("CYBER-INTEL-ANALYST")

# ── Threat Severity Mapping ──────────────────────────────────────────────
CVSS_THRESHOLD = 7.0
IOC_PATTERNS = {
    "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "domain": re.compile(r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b"),
    "sha256": re.compile(r"\b[a-fA-F0-9]{64}\b"),
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
    "cve": re.compile(r"CVE-\d{4}-\d{4,7}"),
}

THREAT_PRIORITY = {
    "cve": "P0-IMMEDIATE",
    "sha256": "P0-IMMEDIATE",
    "ipv4": "P1-URGENT",
    "domain": "P2-REVIEW",
    "email": "P3-MONITOR",
}
# ─────────────────────────────────────────────────────────────────────────


class ThreatExtractor:
    """Scans raw text sources for indicators of compromise."""

    def __init__(self):
        self.stats = {"total_iocs": 0, "by_type": {}}

    def extract_from_text(self, text: str, source_label: str = "unknown") -> list[dict]:
        """Extract all IoC patterns from a text blob."""
        findings = []
        for ioc_type, pattern in IOC_PATTERNS.items():
            matches = set(pattern.findall(text))
            for match in matches:
                finding = {
                    "type": ioc_type,
                    "value": match,
                    "source": source_label,
                    "priority": THREAT_PRIORITY.get(ioc_type, "P3-MONITOR"),
                    "timestamp": datetime.now().isoformat(),
                }
                findings.append(finding)
                self.stats["total_iocs"] += 1
                self.stats["by_type"][ioc_type] = self.stats["by_type"].get(ioc_type, 0) + 1
        return findings


class ThreatCorrelator:
    """Cross-references extracted IoCs against a known-bad list."""

    def __init__(self, blocklist_path: Path | None = None):
        self.blocklist: set[str] = set()
        if blocklist_path and blocklist_path.exists():
            raw = blocklist_path.read_text(encoding="utf-8")
            self.blocklist = {line.strip() for line in raw.splitlines() if line.strip()}
            logger.info(f"Loaded {len(self.blocklist)} entries from blocklist.")

    def correlate(self, findings: list[dict]) -> list[dict]:
        """Flag findings that match the blocklist and escalate priority."""
        for f in findings:
            if f["value"] in self.blocklist:
                f["correlated"] = True
                f["priority"] = "P0-IMMEDIATE"
                f["note"] = "MATCH against known-bad blocklist."
            else:
                f["correlated"] = False
        return findings


class IntelReportGenerator:
    """Generates structured JSON and Markdown intelligence reports."""

    @staticmethod
    def to_json(findings: list[dict], stats: dict, output_path: Path):
        report = {
            "agent": "CYBER-INTEL-ANALYST",
            "version": "2.0-nexus",
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_iocs": stats.get("total_iocs", 0),
                "by_type": stats.get("by_type", {}),
                "correlated_hits": sum(1 for f in findings if f.get("correlated")),
                "threat_verdict": "CRITICAL" if any(f["priority"] == "P0-IMMEDIATE" and f.get("correlated") for f in findings)
                    else "ELEVATED" if any(f["priority"] in ("P0-IMMEDIATE", "P1-URGENT") for f in findings)
                    else "LOW",
            },
            "findings": sorted(findings, key=lambda x: x["priority"]),
        }
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        logger.info(f"[DONE] JSON report -> {output_path}")

    @staticmethod
    def to_markdown(findings: list[dict], stats: dict, output_path: Path):
        lines = [
            f"# Cyber Intel Report",
            f"**Generated:** {datetime.now().isoformat()}",
            f"**Total IoCs:** {stats.get('total_iocs', 0)}",
            "",
            "## Findings by Priority",
            "| Priority | Type | Value | Correlated | Source |",
            "|----------|------|-------|------------|--------|",
        ]
        for f in sorted(findings, key=lambda x: x["priority"]):
            corr = "✅ HIT" if f.get("correlated") else "—"
            lines.append(f"| {f['priority']} | {f['type']} | `{f['value']}` | {corr} | {f['source']} |")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(lines), encoding="utf-8")
        logger.info(f"[DONE] Markdown report -> {output_path}")


def main():
    parser = argparse.ArgumentParser(description="CYBER-INTEL-ANALYST: OSINT IoC Extractor & Correlator")
    parser.add_argument("--input", required=True, help="Path to raw text/log file or directory to scan")
    parser.add_argument("--blocklist", default=None, help="Path to a known-bad IoC list (one per line)")
    parser.add_argument("--output", default="intel_report.json", help="Output JSON report path")
    parser.add_argument("--markdown", default=None, help="Optional Markdown report output path")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        logger.error(f"Input not found: {input_path}")
        sys.exit(1)

    # Ingest text sources
    texts = []
    if input_path.is_dir():
        for f in input_path.rglob("*"):
            if f.is_file() and f.suffix in (".txt", ".log", ".md", ".json", ".csv"):
                texts.append((f.name, f.read_text(encoding="utf-8", errors="ignore")))
    else:
        texts.append((input_path.name, input_path.read_text(encoding="utf-8", errors="ignore")))

    logger.info(f"[*] Scanning {len(texts)} source(s) for IoCs...")

    extractor = ThreatExtractor()
    all_findings = []
    for label, content in texts:
        all_findings.extend(extractor.extract_from_text(content, source_label=label))

    logger.info(f"[*] Extracted {extractor.stats['total_iocs']} IoCs. Correlating...")

    blocklist_path = Path(args.blocklist).resolve() if args.blocklist else None
    correlator = ThreatCorrelator(blocklist_path)
    correlated = correlator.correlate(all_findings)

    IntelReportGenerator.to_json(correlated, extractor.stats, Path(args.output).resolve())

    if args.markdown:
        IntelReportGenerator.to_markdown(correlated, extractor.stats, Path(args.markdown).resolve())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
