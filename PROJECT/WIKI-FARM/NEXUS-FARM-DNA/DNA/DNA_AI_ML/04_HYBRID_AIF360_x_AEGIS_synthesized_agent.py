#!/usr/bin/env python3
"""
HYBRID_FAIR_GUARD v1.0 [NEXUS SYNTHESIZED]
Heritage: AIF360 x AEGIS
Role: analyzer | Security: high | Interface: api
Mission: ML-driven audit of security policies for bias and vulnerability detection.
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("FAIR-GUARD")

# ── Audit Scoring ────────────────────────────────────────────────────────
SEVERITY_WEIGHTS = {"CRITICAL": 1.0, "HIGH": 0.8, "MEDIUM": 0.5, "LOW": 0.2}

MODALITY_BIAS_RULES = {
    "access_control": 0.9,     # High weight for fairness in access
    "biometric_auth": 1.0,      # Highest weight (AIF360 influence)
    "audit_logging": 0.4,
}


class PolicyAnalyzer:
    """Analyzes security findings for both technical vulnerabilities and algorithmic bias."""

    def __init__(self):
        self.stats = {"audited": 0, "bias_alerts": 0, "vuln_alerts": 0}

    def analyze(self, findings: list[dict]) -> list[dict]:
        """Apply fairness and security heuristics to findings."""
        enriched = []
        for f in findings:
            f_type = f.get("type", "generic")
            severity = f.get("severity", "MEDIUM")
            
            # Security Score (AEGIS)
            base_score = SEVERITY_WEIGHTS.get(severity, 0.5)
            
            # Bias Multiplier (AIF360)
            bias_factor = MODALITY_BIAS_RULES.get(f_type, 0.5)
            
            final_score = round(base_score * 0.7 + bias_factor * 0.3, 3)
            
            # [REMEDIATION] FAIR-GUARD Advice
            advice = "Review access logs for statistical parity. Check for unbalanced credential rotation." if bias_factor > 0.8 else "Standard hardening required."

            f.update({
                "fair_security_score": final_score,
                "bias_proxy": bias_factor > 0.7,
                "remediation": advice,
                "audit_ts": datetime.now().isoformat()
            })
            
            if bias_factor > 0.7: self.stats["bias_alerts"] += 1
            if base_score > 0.7: self.stats["vuln_alerts"] += 1
            self.stats["audited"] += 1
            enriched.append(f)

        enriched.sort(key=lambda x: x["fair_security_score"], reverse=True)
        return enriched


def main():
    parser = argparse.ArgumentParser(description="HYBRID_FAIR_GUARD")
    parser.add_argument("--input", required=True, help="Findings JSON")
    parser.add_argument("--output", default="fair_audit.json", help="Output JSON")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        logger.error(f"Input not found: {input_path}")
        sys.exit(1)

    data = json.loads(input_path.read_text(encoding="utf-8"))
    findings = data.get("findings", [])
    
    analyzer = PolicyAnalyzer()
    enriched = analyzer.analyze(findings)

    report = {
        "agent": "HYBRID_FAIR_GUARD",
        "heritage": "AIF360 x AEGIS",
        "timestamp": datetime.now().isoformat(),
        "stats": analyzer.stats,
        "results": enriched
    }

    output = Path(args.output).resolve()
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logger.info(f"[DONE] Audit complete: {output}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
