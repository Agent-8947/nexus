#!/usr/bin/env python3
"""
NEXUS-LEGAL-NOTARY [NEXUS SYNTHESIZED v2.0]
Mission: PII scanning, compliance enforcement, and cryptographic commit notarization
Role: enforcer | Security: read-only | Interface: cli
"""

import sys
import json
import logging
import argparse
import re
import hashlib
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS-LEGAL-NOTARY")

# ── PII Detection Patterns ──────────────────────────────────────────────
PII_PATTERNS = {
    "credit_card": {
        "pattern": re.compile(r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b"),
        "severity": "CRITICAL",
        "regulation": "PCI-DSS",
    },
    "ssn_us": {
        "pattern": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
        "severity": "CRITICAL",
        "regulation": "CCPA / HIPAA",
    },
    "email_personal": {
        "pattern": re.compile(r"\b[A-Za-z0-9._%+-]+@(?:gmail|yahoo|hotmail|outlook)\.[a-z]{2,}\b", re.IGNORECASE),
        "severity": "HIGH",
        "regulation": "GDPR Art.6",
    },
    "phone_intl": {
        "pattern": re.compile(r"\+\d{1,3}[\s-]?\(?\d{1,4}\)?[\s-]?\d{3,4}[\s-]?\d{3,4}\b"),
        "severity": "HIGH",
        "regulation": "GDPR Art.6",
    },
    "iban": {
        "pattern": re.compile(r"\b[A-Z]{2}\d{2}[\s]?[\dA-Z]{4}[\s]?(?:[\dA-Z]{4}[\s]?){2,7}[\dA-Z]{1,4}\b"),
        "severity": "CRITICAL",
        "regulation": "PSD2 / GDPR",
    },
    "ipn_ua": {
        "pattern": re.compile(r"\b\d{10}\b"),
        "severity": "MEDIUM",
        "regulation": "UA Data Protection Law",
    },
    "passport_ua": {
        "pattern": re.compile(r"\b[А-ЯІЇЄҐ]{2}\d{6}\b"),
        "severity": "CRITICAL",
        "regulation": "UA Data Protection Law",
    },
}

SEVERITY_SCORES = {"CRITICAL": 1.0, "HIGH": 0.75, "MEDIUM": 0.45, "LOW": 0.15}
# ─────────────────────────────────────────────────────────────────────────


class PIIScanner:
    """Scans source files for personally identifiable information leaks."""

    def __init__(self):
        self.stats = {"total_pii": 0, "by_type": {}, "files_scanned": 0}

    def scan_file(self, filepath: Path) -> list[dict]:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        lines = content.splitlines()
        findings = []

        for pii_type, pii_info in PII_PATTERNS.items():
            for line_num, line in enumerate(lines, 1):
                matches = pii_info["pattern"].findall(line)
                for match in matches:
                    redacted = match[:3] + "***" + match[-2:] if len(match) > 5 else "***"
                    findings.append({
                        "type": pii_type,
                        "value_redacted": redacted,
                        "severity": pii_info["severity"],
                        "risk_score": SEVERITY_SCORES[pii_info["severity"]],
                        "regulation": pii_info["regulation"],
                        "file": str(filepath.name),
                        "line": line_num,
                        "remediation": f"Remove or vault this {pii_type}. Regulation: {pii_info['regulation']}.",
                    })
                    self.stats["total_pii"] += 1
                    self.stats["by_type"][pii_type] = self.stats["by_type"].get(pii_type, 0) + 1

        self.stats["files_scanned"] += 1
        return findings


class CommitNotarizer:
    """Creates a SHA-256 fingerprint of a file state for legal non-repudiation."""

    @staticmethod
    def notarize(filepath: Path) -> dict:
        content = filepath.read_bytes()
        sha256 = hashlib.sha256(content).hexdigest()
        return {
            "file": str(filepath),
            "sha256": sha256,
            "size_bytes": len(content),
            "notarized_at": datetime.now().isoformat(),
        }


class ComplianceReporter:
    """Generates structured compliance report."""

    @staticmethod
    def generate(findings: list[dict], notary_log: list[dict], stats: dict, output_path: Path):
        scores = [f["risk_score"] for f in findings]
        report = {
            "agent": "NEXUS-LEGAL-NOTARY",
            "version": "2.0-nexus",
            "timestamp": datetime.now().isoformat(),
            "compliance_summary": {
                "files_scanned": stats["files_scanned"],
                "total_pii_findings": stats["total_pii"],
                "by_type": stats["by_type"],
                "max_risk": max(scores) if scores else 0,
                "verdict": "NON-COMPLIANT" if any(s >= 0.75 for s in scores)
                    else "REVIEW-REQUIRED" if any(s >= 0.45 for s in scores) else "COMPLIANT",
                "regulations_triggered": list({f["regulation"] for f in findings}),
            },
            "pii_findings": sorted(findings, key=lambda x: x["risk_score"], reverse=True),
            "notarization_log": notary_log,
        }
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        logger.info(f"[DONE] Compliance report -> {output_path}")


def main():
    parser = argparse.ArgumentParser(description="NEXUS-LEGAL-NOTARY: PII Scanner & Compliance Enforcer")
    parser.add_argument("--input", required=True, help="File or directory to scan for PII")
    parser.add_argument("--output", default="compliance_report.json", help="Output report path")
    parser.add_argument("--notarize", action="store_true", help="Generate SHA-256 notarization log")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        logger.error(f"Input not found: {input_path}")
        sys.exit(1)

    scan_exts = {".py", ".js", ".ts", ".json", ".yml", ".yaml", ".env", ".md", ".txt", ".csv", ".sql"}
    files = [f for f in input_path.rglob("*") if f.is_file() and f.suffix in scan_exts] if input_path.is_dir() else [input_path]

    logger.info(f"[*] Scanning {len(files)} file(s) for PII leaks...")

    scanner = PIIScanner()
    all_findings = []
    notary_log = []

    for f in files:
        all_findings.extend(scanner.scan_file(f))
        if args.notarize:
            notary_log.append(CommitNotarizer.notarize(f))

    ComplianceReporter.generate(all_findings, notary_log, scanner.stats, Path(args.output).resolve())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
