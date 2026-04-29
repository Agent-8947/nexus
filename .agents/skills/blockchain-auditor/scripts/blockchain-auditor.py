#!/usr/bin/env python3
"""
BLOCKCHAIN-AUDITOR [NEXUS SYNTHESIZED v2.0]
Mission: Smart contract static analysis and vulnerability scoring
Role: analyzer | Security: read-only | Interface: cli
"""

import sys
import json
import logging
import argparse
import re
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("BLOCKCHAIN-AUDITOR")

# ── Vulnerability Patterns ───────────────────────────────────────────────
VULN_PATTERNS = {
    "reentrancy": {
        "pattern": re.compile(r"\.call\{value:", re.IGNORECASE),
        "severity": "CRITICAL",
        "remediation": "Use checks-effects-interactions pattern. Apply ReentrancyGuard from OpenZeppelin.",
    },
    "unchecked_return": {
        "pattern": re.compile(r"\.send\(|\.transfer\(", re.IGNORECASE),
        "severity": "HIGH",
        "remediation": "Check return value of low-level calls. Prefer call{value:} with explicit revert.",
    },
    "tx_origin": {
        "pattern": re.compile(r"tx\.origin"),
        "severity": "HIGH",
        "remediation": "Replace tx.origin with msg.sender for authorization checks.",
    },
    "selfdestruct": {
        "pattern": re.compile(r"selfdestruct\(|suicide\("),
        "severity": "CRITICAL",
        "remediation": "Remove selfdestruct. Use circuit-breaker patterns instead.",
    },
    "integer_overflow": {
        "pattern": re.compile(r"pragma solidity\s+\^?0\.[0-6]\.", re.IGNORECASE),
        "severity": "HIGH",
        "remediation": "Upgrade to Solidity >=0.8.0 (built-in overflow checks) or use SafeMath.",
    },
    "uninitialized_proxy": {
        "pattern": re.compile(r"delegatecall\("),
        "severity": "CRITICAL",
        "remediation": "Ensure proxy implementation is initialized. Use initializer modifier.",
    },
    "hardcoded_gas": {
        "pattern": re.compile(r"\.gas\(\d+\)"),
        "severity": "MEDIUM",
        "remediation": "Avoid hardcoded gas stipends. They break with EVM gas schedule changes.",
    },
    "timestamp_dependence": {
        "pattern": re.compile(r"block\.timestamp|now"),
        "severity": "LOW",
        "remediation": "Avoid using block.timestamp for critical logic. Miners can manipulate +/- 15s.",
    },
}

SEVERITY_SCORES = {"CRITICAL": 1.0, "HIGH": 0.75, "MEDIUM": 0.45, "LOW": 0.15}
# ─────────────────────────────────────────────────────────────────────────


class ContractScanner:
    """Scans Solidity source files for known vulnerability patterns."""

    def __init__(self):
        self.stats = {"total_vulns": 0, "by_severity": {}, "files_scanned": 0}

    def scan_file(self, filepath: Path) -> list[dict]:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        lines = content.splitlines()
        findings = []

        for vuln_id, vuln_info in VULN_PATTERNS.items():
            for line_num, line in enumerate(lines, 1):
                if vuln_info["pattern"].search(line):
                    finding = {
                        "vuln_id": vuln_id.upper(),
                        "severity": vuln_info["severity"],
                        "risk_score": SEVERITY_SCORES[vuln_info["severity"]],
                        "file": str(filepath),
                        "line": line_num,
                        "code_snippet": line.strip()[:120],
                        "remediation": vuln_info["remediation"],
                    }
                    findings.append(finding)
                    sev = vuln_info["severity"]
                    self.stats["total_vulns"] += 1
                    self.stats["by_severity"][sev] = self.stats["by_severity"].get(sev, 0) + 1

        self.stats["files_scanned"] += 1
        return findings


class GasAnalyzer:
    """Estimates gas complexity from function signature density."""

    @staticmethod
    def estimate(filepath: Path) -> dict:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        functions = re.findall(r"function\s+\w+", content)
        modifiers = re.findall(r"modifier\s+\w+", content)
        events = re.findall(r"event\s+\w+", content)
        return {
            "file": str(filepath),
            "function_count": len(functions),
            "modifier_count": len(modifiers),
            "event_count": len(events),
            "complexity_tier": "HIGH" if len(functions) > 20 else "MEDIUM" if len(functions) > 8 else "LOW",
        }


def main():
    parser = argparse.ArgumentParser(description="BLOCKCHAIN-AUDITOR: Solidity Vulnerability Scanner")
    parser.add_argument("--input", required=True, help="Path to .sol file or directory of contracts")
    parser.add_argument("--output", default="audit_report.json", help="Output JSON report")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        logger.error(f"Input not found: {input_path}")
        sys.exit(1)

    sol_files = list(input_path.rglob("*.sol")) if input_path.is_dir() else [input_path]
    if not sol_files:
        logger.error("No .sol files found.")
        sys.exit(1)

    logger.info(f"[*] Scanning {len(sol_files)} contract(s)...")

    scanner = ContractScanner()
    all_findings = []
    gas_reports = []

    for sol in sol_files:
        all_findings.extend(scanner.scan_file(sol))
        gas_reports.append(GasAnalyzer.estimate(sol))

    scores = [f["risk_score"] for f in all_findings]
    report = {
        "agent": "BLOCKCHAIN-AUDITOR",
        "version": "2.0-nexus",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "files_scanned": scanner.stats["files_scanned"],
            "total_vulnerabilities": scanner.stats["total_vulns"],
            "by_severity": scanner.stats["by_severity"],
            "top_risk_score": max(scores) if scores else 0,
            "mean_risk_score": round(sum(scores) / len(scores), 3) if scores else 0,
            "audit_verdict": "CRITICAL" if any(s >= 0.75 for s in scores)
                else "ELEVATED" if any(s >= 0.45 for s in scores) else "PASS",
        },
        "findings": sorted(all_findings, key=lambda x: x["risk_score"], reverse=True),
        "gas_analysis": gas_reports,
    }

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info(f"[DONE] Audit report -> {output}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
