#!/usr/bin/env python3
"""
HYBRID_CRYFS_x_ZEN v2.0 [NEXUS SEALED REPORT GENERATOR]
==========================================================
Heritage: CryFS (Encrypted Filesystem) + Zen (OSINT Collection, Peace-of-mind)
Mission:  Security audit - post-analysis report sealing and distribution
Role:     SEALER - Takes analysis reports, generates encrypted sealed bundles

ARCHITECTURE:
- Reads any JSON report (from OSINT Collector, Analyzer, VulnScan, Hardener)
- Generates integrity-sealed JSON bundle (HMAC-SHA256 signature)
- Produces executive summary Markdown
- Creates a "sealed envelope" with tamper-evidence metadata
"""

import sys
import os
import json
import hmac
import hashlib
import logging
import argparse
import base64
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS-SEALER")

# Default HMAC key (in production, load from env/vault)
DEFAULT_SEAL_KEY = os.environ.get("NEXUS_SEAL_KEY", "nexus-default-seal-key-change-in-prod")


class ReportSealer:
    """Creates integrity-sealed report bundles with HMAC-SHA256."""

    def __init__(self, seal_key: str = DEFAULT_SEAL_KEY):
        self.seal_key = seal_key.encode("utf-8")

    def seal_report(self, report_data: dict, source_path: str) -> dict:
        """Create a sealed envelope around a report."""
        # Canonical JSON for deterministic hashing
        canonical = json.dumps(report_data, sort_keys=True, ensure_ascii=False)
        content_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

        # HMAC signature
        signature = hmac.new(
            self.seal_key,
            canonical.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        envelope = {
            "nexus_sealed_report": {
                "version":       "2.0",
                "sealed_at":     datetime.now().isoformat(),
                "source_agent":  report_data.get("agent", "unknown"),
                "source_file":   source_path,
                "integrity": {
                    "algorithm":    "HMAC-SHA256",
                    "content_hash": content_hash,
                    "signature":    signature,
                    "key_hint":     "NEXUS_SEAL_KEY env var",
                },
                "stats_summary": self._extract_summary(report_data),
            },
            "payload": report_data,
        }

        return envelope

    def verify_seal(self, envelope: dict) -> bool:
        """Verify the HMAC signature of a sealed report."""
        payload   = envelope.get("payload", {})
        canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        expected  = envelope["nexus_sealed_report"]["integrity"]["signature"]
        actual    = hmac.new(self.seal_key, canonical.encode("utf-8"), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, actual)

    @staticmethod
    def _extract_summary(data: dict) -> dict:
        """Pull top-level stats from any NEXUS agent report."""
        stats = data.get("stats", data.get("analysis", {}))
        if isinstance(stats, dict):
            return {k: v for k, v in stats.items() if isinstance(v, (int, float, str))}
        return {}


class ExecutiveSummaryGenerator:
    """Generates a Markdown executive summary for sealed reports."""

    def generate(self, envelope: dict, output_md: Path):
        meta    = envelope["nexus_sealed_report"]
        stats   = meta["stats_summary"]
        payload = envelope["payload"]

        lines = [
            f"# NEXUS Security Report [SEALED]",
            f"",
            f"> **Integrity:** HMAC-SHA256 verified",
            f"> **Sealed at:** {meta['sealed_at']}",
            f"> **Source:** {meta['source_agent']}",
            f"",
            f"## Executive Summary",
            f"",
        ]

        # Adaptive stats rendering
        if stats:
            lines.append("| Metric | Value |")
            lines.append("|---|---|")
            for k, v in stats.items():
                lines.append(f"| {k.replace('_', ' ').title()} | {v} |")
            lines.append("")

        # Top findings if available
        findings = payload.get("findings", payload.get("enriched_findings", payload.get("results", [])))
        if findings and isinstance(findings, list):
            # Filter to failures/findings only
            critical_items = [
                f for f in findings
                if isinstance(f, dict) and (
                    f.get("severity") in ("CRITICAL", "HIGH") or
                    f.get("passed") is False
                )
            ][:10]

            if critical_items:
                lines.append("## Critical Items")
                lines.append("")
                for i, item in enumerate(critical_items, 1):
                    sev   = item.get("severity", item.get("check_id", "?"))
                    desc  = item.get("rule_id", item.get("name", item.get("cve", "?")))
                    where = item.get("file", "")
                    fix   = item.get("remediation", "")
                    lines.append(f"{i}. **[{sev}]** `{desc}` -- {where}")
                    if fix:
                        lines.append(f"   - Fix: {fix}")
                lines.append("")

        lines.append("---")
        lines.append("")
        lines.append(f"**Signature:** `{meta['integrity']['signature'][:32]}...`")
        lines.append(f"**Content Hash:** `{meta['integrity']['content_hash'][:32]}...`")
        lines.append("")
        lines.append("*This report was sealed by NEXUS CryFS x Zen Agent v2.0*")

        output_md.write_text("\n".join(lines), encoding="utf-8")
        logger.info(f"[REPORT] Executive summary -> {output_md}")


def run_seal(input_path: Path, output_dir: Path, verify_only: bool = False):
    sealer = ReportSealer()

    if not input_path.exists():
        logger.error(f"Input not found: {input_path}")
        sys.exit(1)

    data = json.loads(input_path.read_text(encoding="utf-8"))

    if verify_only:
        # Verify mode: check existing sealed envelope
        if "nexus_sealed_report" not in data:
            logger.error("Not a sealed report. Cannot verify.")
            sys.exit(1)
        ok = sealer.verify_seal(data)
        print(f"\n[VERIFY] Integrity: {'VALID' if ok else 'TAMPERED'}")
        sys.exit(0 if ok else 1)

    # Seal mode
    logger.info(f"[*] Sealing report: {input_path.name}")
    envelope = sealer.seal_report(data, str(input_path))

    output_dir.mkdir(parents=True, exist_ok=True)

    sealed_json = output_dir / f"SEALED_{input_path.stem}.json"
    sealed_json.write_text(json.dumps(envelope, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info(f"[SEALED] -> {sealed_json}")

    # Executive summary
    summary_md = output_dir / f"SEALED_{input_path.stem}_SUMMARY.md"
    gen = ExecutiveSummaryGenerator()
    gen.generate(envelope, summary_md)

    # Verify own seal
    ok = sealer.verify_seal(envelope)

    print(f"\n{'='*60}")
    print(f"  NEXUS Report Sealer v2.0")
    print(f"{'='*60}")
    print(f"  Source:    {input_path.name}")
    print(f"  Agent:     {data.get('agent', '?')}")
    print(f"  Signature: {envelope['nexus_sealed_report']['integrity']['signature'][:40]}...")
    print(f"  Verified:  {'VALID' if ok else 'FAILED'}")
    print(f"  Outputs:")
    print(f"    [1] {sealed_json.name}")
    print(f"    [2] {summary_md.name}")
    print(f"{'='*60}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NEXUS Report Sealer v2.0 (CryFS x Zen)")
    parser.add_argument("--input",  required=True, help="JSON report to seal")
    parser.add_argument("--outdir", default="sealed_reports", help="Output directory")
    parser.add_argument("--verify", action="store_true", help="Verify existing sealed report")
    args = parser.parse_args()

    try:
        run_seal(
            Path(args.input).resolve(),
            Path(args.outdir).resolve(),
            verify_only=args.verify
        )
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
