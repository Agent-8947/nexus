#!/usr/bin/env python3
"""
HYBRID_AUTOGLUON_x_ALLUXIO v2.0 [NEXUS OSINT ANALYZER]
========================================================
Heritage: AutoGluon (AutoML Scoring) + Alluxio (Data Orchestration)
Role:     ANALYZER - Consumes Collector JSON, classifies findings, assigns composite risk
Input:    JSON from HYBRID_TROUBLESHOOTING_x_CRATE (Collector)
Output:   Enriched JSON with risk_score, priority, and remediation advice

DNA Signature: Network=0.5, Intelligence=1.0, Autonomy=1.0, Hardware=0.0, Stealth=0.0, Scale=0.0
Security:      high
Interface:     CLI
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS-ANALYZER")


# ── Risk Model (AutoGluon-inspired multi-dimensional scoring) ────────────
SEVERITY_BASE = {"CRITICAL": 1.0, "HIGH": 0.75, "MEDIUM": 0.45, "LOW": 0.15}
CATEGORY_WEIGHTS = {"credential": 1.0, "network": 0.6, "identity": 0.3, "config": 0.5}

# Context multipliers: patterns in `context` field that increase/decrease risk
CONTEXT_SIGNALS = {
    "production":  1.4,
    "staging":     1.1,
    "test":        0.5,
    "example":     0.3,
    "TODO":        0.4,
    "mock":        0.2,
    "localhost":   0.3,
    "0.0.0.0":    1.5,
}

REMEDIATION_MAP = {
    "aws_key":            "Rotate AWS key immediately. Use IAM roles instead of static keys.",
    "generic_secret":     "Move secret to environment variable or vault (HashiCorp Vault / AWS SSM).",
    "private_key_header": "Remove private key from repo. Rotate keypair. Use ssh-agent.",
    "jwt_token":          "Invalidate the JWT. Check token expiry and issuer.",
    "connection_string":  "Move connection string to .env or secrets manager. Rotate credentials.",
    "ipv4_private":       "Verify this internal IP is intentional. Remove if leaked.",
    "ipv4_public":        "Assess exposure. Add to asset inventory if production.",
    "domain_internal":    "Confirm internal domain is not exposed in public repo.",
    "email_corporate":    "Assess if email exposure creates phishing risk.",
}


class RiskScorer:
    """Multi-dimensional risk scoring engine (AutoGluon-inspired)."""

    def __init__(self):
        self.scored = 0

    def score_finding(self, finding: dict) -> dict:
        """Compute composite risk_score in [0.0, 1.0]."""
        # Dimension 1: Base severity
        base = SEVERITY_BASE.get(finding["severity"], 0.3)

        # Dimension 2: Category weight
        cat_w = CATEGORY_WEIGHTS.get(finding["category"], 0.4)

        # Dimension 3: Context multiplier (scan the context line)
        ctx_mult = 1.0
        context_lower = finding.get("context", "").lower()
        for signal, mult in CONTEXT_SIGNALS.items():
            if signal.lower() in context_lower:
                ctx_mult = mult
                break  # First match wins

        # Dimension 4: File path risk (dotenv, config = higher risk)
        path_mult = 1.0
        fpath = finding.get("file", "").lower()
        if ".env" in fpath or "secret" in fpath or "credential" in fpath:
            path_mult = 1.3
        elif "test" in fpath or "fixture" in fpath or "mock" in fpath:
            path_mult = 0.4

        # Composite
        raw_score = base * cat_w * ctx_mult * path_mult
        risk_score = round(min(1.0, raw_score), 3)

        # Priority bucket
        if risk_score >= 0.8:
            priority = "P0-IMMEDIATE"
        elif risk_score >= 0.5:
            priority = "P1-URGENT"
        elif risk_score >= 0.25:
            priority = "P2-REVIEW"
        else:
            priority = "P3-INFO"

        # Remediation
        remediation = REMEDIATION_MAP.get(finding["rule_id"], "Review and assess risk manually.")

        self.scored += 1
        return {
            **finding,
            "risk_score":   risk_score,
            "priority":     priority,
            "remediation":  remediation,
            "model":        "autogluon_composite_v2",
            "dimensions": {
                "base_severity":   base,
                "category_weight": cat_w,
                "context_mult":    ctx_mult,
                "path_mult":       path_mult
            }
        }


class AnalysisPipeline:
    """Orchestrates the analysis flow (Alluxio-inspired data management)."""

    def __init__(self, scorer: RiskScorer):
        self.scorer = scorer

    def analyze_report(self, report: dict) -> dict:
        """Process a Collector report and produce enriched analysis."""
        findings = report.get("findings", [])
        logger.info(f"[*] Analyzing {len(findings)} findings...")

        enriched = [self.scorer.score_finding(f) for f in findings]
        enriched.sort(key=lambda x: x["risk_score"], reverse=True)

        # Aggregate stats
        by_priority = {}
        by_category = {}
        for e in enriched:
            by_priority[e["priority"]] = by_priority.get(e["priority"], 0) + 1
            by_category[e["category"]] = by_category.get(e["category"], 0) + 1

        top_risk = enriched[0]["risk_score"] if enriched else 0.0
        mean_risk = sum(e["risk_score"] for e in enriched) / max(len(enriched), 1)

        return {
            "agent":       "HYBRID_AUTOGLUON_x_ALLUXIO",
            "version":     "2.0",
            "timestamp":   datetime.now().isoformat(),
            "source":      report.get("agent", "unknown"),
            "analysis": {
                "total_findings":  len(enriched),
                "top_risk_score":  round(top_risk, 3),
                "mean_risk_score": round(mean_risk, 3),
                "by_priority":     by_priority,
                "by_category":     by_category,
                "risk_verdict":    "CRITICAL" if top_risk >= 0.8 else
                                   "HIGH" if top_risk >= 0.5 else
                                   "MEDIUM" if top_risk >= 0.25 else "LOW"
            },
            "enriched_findings": enriched
        }


def run_analysis(input_path: Path, output_path: Path):
    """Load Collector report, analyze, write enriched report."""
    if not input_path.exists():
        logger.error(f"Input not found: {input_path}")
        sys.exit(1)

    report = json.loads(input_path.read_text(encoding="utf-8"))
    logger.info(f"[*] Loaded report from {report.get('agent', '?')} ({report['stats']['findings']} findings)")

    scorer   = RiskScorer()
    pipeline = AnalysisPipeline(scorer)
    result   = pipeline.analyze_report(report)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info(f"[DONE] Analysis -> {output_path}")

    # Summary
    a = result["analysis"]
    print(f"\n{'='*60}")
    print(f"  NEXUS OSINT ANALYZER v2.0 -- ANALYSIS COMPLETE")
    print(f"{'='*60}")
    print(f"  Total findings:   {a['total_findings']}")
    print(f"  Top risk score:   {a['top_risk_score']}")
    print(f"  Mean risk score:  {a['mean_risk_score']}")
    print(f"  Risk verdict:     {a['risk_verdict']}")
    print(f"  Priority breakdown:")
    for p in ["P0-IMMEDIATE", "P1-URGENT", "P2-REVIEW", "P3-INFO"]:
        cnt = a["by_priority"].get(p, 0)
        if cnt:
            print(f"    {p}: {cnt}")
    print(f"{'='*60}")

    # Top 5 risks
    if result["enriched_findings"]:
        print(f"\n  TOP RISKS:")
        for i, f in enumerate(result["enriched_findings"][:5], 1):
            print(f"  {i}. [{f['risk_score']:.2f}] {f['rule_id']:20s} | {f['file']}:{f['line']}")
        print()

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="NEXUS OSINT Analyzer v2.0 -- Risk scoring and classification"
    )
    parser.add_argument("--input",  required=True, help="Collector JSON report")
    parser.add_argument("--output", default="osint_analysis_report.json", help="Output analysis JSON")
    args = parser.parse_args()

    try:
        run_analysis(Path(args.input).resolve(), Path(args.output).resolve())
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
