#!/usr/bin/env python3
"""
CLOUD-FINOPS-OPTIMIZER [NEXUS SYNTHESIZED v2.0]
Mission: Detect cloud resource waste and generate cost-optimization recommendations
Role: analyzer | Security: read-only | Interface: cli
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("CLOUD-FINOPS-OPTIMIZER")

# ── Waste Detection Thresholds ───────────────────────────────────────────
CPU_ZOMBIE_THRESHOLD = 5.0     # percent
RAM_ZOMBIE_THRESHOLD = 10.0    # percent
ZOMBIE_WINDOW_HOURS = 72
ORPHAN_VOLUME_DAYS = 30
CROSS_AZ_COST_FACTOR = 0.01   # $/GB
# ─────────────────────────────────────────────────────────────────────────


class ResourceAnalyzer:
    """Analyzes cloud resource utilization from exported metrics JSON."""

    def __init__(self):
        self.stats = {"zombies": 0, "orphans": 0, "oversized": 0, "total_waste_usd": 0.0}

    def analyze_compute(self, instances: list[dict]) -> list[dict]:
        findings = []
        for inst in instances:
            cpu = inst.get("avg_cpu_pct", 100)
            ram = inst.get("avg_ram_pct", 100)
            hours = inst.get("idle_hours", 0)
            monthly_cost = inst.get("monthly_cost_usd", 0)

            issues = []
            if cpu < CPU_ZOMBIE_THRESHOLD and hours >= ZOMBIE_WINDOW_HOURS:
                issues.append("CPU_ZOMBIE")
                self.stats["zombies"] += 1
            if ram < RAM_ZOMBIE_THRESHOLD and hours >= ZOMBIE_WINDOW_HOURS:
                issues.append("RAM_ZOMBIE")

            # Oversized detection: paying for large but using small
            size_tier = inst.get("instance_type", "")
            if cpu < 20 and any(tag in size_tier for tag in ["xlarge", "2xlarge", "4xlarge", "metal"]):
                issues.append("OVERSIZED")
                self.stats["oversized"] += 1

            if issues:
                potential_savings = monthly_cost * 0.7 if "ZOMBIE" in str(issues) else monthly_cost * 0.4
                self.stats["total_waste_usd"] += potential_savings
                findings.append({
                    "resource_id": inst.get("instance_id", "unknown"),
                    "resource_type": "compute",
                    "instance_type": size_tier,
                    "issues": issues,
                    "avg_cpu_pct": cpu,
                    "avg_ram_pct": ram,
                    "idle_hours": hours,
                    "monthly_cost_usd": monthly_cost,
                    "potential_savings_usd": round(potential_savings, 2),
                    "remediation": self._compute_remediation(issues),
                })
        return findings

    def analyze_storage(self, volumes: list[dict]) -> list[dict]:
        findings = []
        for vol in volumes:
            attached = vol.get("attached", True)
            days_unattached = vol.get("days_unattached", 0)
            monthly_cost = vol.get("monthly_cost_usd", 0)

            if not attached and days_unattached >= ORPHAN_VOLUME_DAYS:
                self.stats["orphans"] += 1
                self.stats["total_waste_usd"] += monthly_cost
                findings.append({
                    "resource_id": vol.get("volume_id", "unknown"),
                    "resource_type": "storage",
                    "issues": ["ORPHAN_VOLUME"],
                    "days_unattached": days_unattached,
                    "size_gb": vol.get("size_gb", 0),
                    "monthly_cost_usd": monthly_cost,
                    "potential_savings_usd": monthly_cost,
                    "remediation": "Snapshot volume, verify no active references, then delete.",
                })
        return findings

    def analyze_network(self, transfers: list[dict]) -> list[dict]:
        findings = []
        for xfer in transfers:
            if xfer.get("cross_az", False):
                gb = xfer.get("gb_transferred", 0)
                cost = gb * CROSS_AZ_COST_FACTOR
                if cost > 50:
                    self.stats["total_waste_usd"] += cost * 0.5
                    findings.append({
                        "resource_id": xfer.get("service_pair", "unknown"),
                        "resource_type": "network",
                        "issues": ["CROSS_AZ_BLOAT"],
                        "gb_transferred": gb,
                        "estimated_cost_usd": round(cost, 2),
                        "potential_savings_usd": round(cost * 0.5, 2),
                        "remediation": "Co-locate services in the same AZ or use VPC endpoints.",
                    })
        return findings

    @staticmethod
    def _compute_remediation(issues: list[str]) -> str:
        parts = []
        if "CPU_ZOMBIE" in issues or "RAM_ZOMBIE" in issues:
            parts.append("Terminate or downscale instance. Consider Spot if stateless.")
        if "OVERSIZED" in issues:
            parts.append("Rightsize to smaller instance type matching actual utilization.")
        return " ".join(parts) or "Review manually."


def main():
    parser = argparse.ArgumentParser(description="CLOUD-FINOPS-OPTIMIZER: Cloud Waste Detector")
    parser.add_argument("--input", required=True, help="Cloud metrics JSON export")
    parser.add_argument("--output", default="finops_report.json", help="Output report")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        logger.error(f"Input not found: {input_path}")
        sys.exit(1)

    data = json.loads(input_path.read_text(encoding="utf-8"))
    analyzer = ResourceAnalyzer()

    all_findings = []
    all_findings.extend(analyzer.analyze_compute(data.get("instances", [])))
    all_findings.extend(analyzer.analyze_storage(data.get("volumes", [])))
    all_findings.extend(analyzer.analyze_network(data.get("network_transfers", [])))

    logger.info(f"[*] Found {len(all_findings)} waste issues. Est. savings: ${analyzer.stats['total_waste_usd']:.2f}/mo")

    report = {
        "agent": "CLOUD-FINOPS-OPTIMIZER",
        "version": "2.0-nexus",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "zombies_detected": analyzer.stats["zombies"],
            "orphan_volumes": analyzer.stats["orphans"],
            "oversized_instances": analyzer.stats["oversized"],
            "total_estimated_waste_usd": round(analyzer.stats["total_waste_usd"], 2),
            "verdict": "ACTION-REQUIRED" if analyzer.stats["total_waste_usd"] > 100 else "OPTIMIZED",
        },
        "findings": sorted(all_findings, key=lambda x: x["potential_savings_usd"], reverse=True),
    }

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info(f"[DONE] FinOps report -> {output}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
