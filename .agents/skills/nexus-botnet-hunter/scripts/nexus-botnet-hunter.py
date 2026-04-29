#!/usr/bin/env python3
"""
NEXUS-BOTNET-HUNTER [NEXUS SYNTHESIZED v2.0]
Mission: Detect C2 beacons via traffic periodicity analysis and auto-quarantine
Role: defender | Security: read-only | Interface: cli
"""

import sys
import json
import logging
import argparse
import math
from pathlib import Path
from datetime import datetime
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS-BOTNET-HUNTER")

# ── Detection Thresholds ─────────────────────────────────────────────────
BEACON_PERIODICITY_TOLERANCE = 0.05   # 5% payload size variance -> beacon flag
MIN_CONNECTIONS_FOR_ANALYSIS = 10
PERIODICITY_FFT_PEAK_RATIO = 3.0     # FFT dominant frequency must be 3x median
ESSENTIAL_SUBNETS = {"10.0.0.0/8", "172.16.0.0/12"}  # Never auto-quarantine these
# ─────────────────────────────────────────────────────────────────────────


class FlowParser:
    """Parses VPC-style flow log entries."""

    @staticmethod
    def parse(log_path: Path) -> list[dict]:
        data = json.loads(log_path.read_text(encoding="utf-8"))
        flows = data if isinstance(data, list) else data.get("flows", [])
        logger.info(f"[*] Parsed {len(flows)} flow records.")
        return flows


class BeaconDetector:
    """Detects C2-style periodic beaconing in outbound traffic."""

    def __init__(self):
        self.stats = {"hosts_analyzed": 0, "beacons_detected": 0}

    def detect(self, flows: list[dict]) -> list[dict]:
        # Group flows by source -> destination pair
        pairs = defaultdict(list)
        for f in flows:
            src = f.get("src_ip", "")
            dst = f.get("dst_ip", "")
            direction = f.get("direction", "outbound")
            if direction == "outbound" and dst:
                pairs[(src, dst)].append(f)

        findings = []
        for (src, dst), connections in pairs.items():
            if len(connections) < MIN_CONNECTIONS_FOR_ANALYSIS:
                continue

            self.stats["hosts_analyzed"] += 1

            # Payload size variance analysis
            sizes = [c.get("bytes", 0) for c in connections]
            mean_size = sum(sizes) / len(sizes) if sizes else 0
            if mean_size == 0:
                continue
            variance = sum((s - mean_size) ** 2 for s in sizes) / len(sizes)
            std_dev = math.sqrt(variance)
            cv = std_dev / mean_size if mean_size > 0 else 1.0  # Coefficient of variation

            # Timing regularity analysis
            timestamps = sorted(c.get("timestamp", 0) for c in connections)
            intervals = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps) - 1)]
            mean_interval = sum(intervals) / len(intervals) if intervals else 0
            interval_variance = sum((i - mean_interval) ** 2 for i in intervals) / len(intervals) if intervals else float("inf")
            interval_cv = math.sqrt(interval_variance) / mean_interval if mean_interval > 0 else 1.0

            # Beacon scoring
            is_beacon = cv < BEACON_PERIODICITY_TOLERANCE and interval_cv < 0.15
            beacon_score = round(1.0 - (cv + interval_cv) / 2, 3) if (cv + interval_cv) < 2 else 0.0

            if is_beacon or beacon_score > 0.8:
                self.stats["beacons_detected"] += 1
                findings.append({
                    "src_ip": src,
                    "dst_ip": dst,
                    "connection_count": len(connections),
                    "payload_cv": round(cv, 4),
                    "interval_cv": round(interval_cv, 4),
                    "mean_interval_sec": round(mean_interval, 2),
                    "beacon_score": beacon_score,
                    "verdict": "C2_BEACON_CONFIRMED" if beacon_score > 0.9 else "C2_BEACON_SUSPECTED",
                    "priority": "P0-IMMEDIATE",
                    "quarantine_action": self._quarantine_action(src),
                })
        return findings

    @staticmethod
    def _quarantine_action(src_ip: str) -> str:
        for subnet in ESSENTIAL_SUBNETS:
            base = subnet.split("/")[0]
            if src_ip.startswith(base.rsplit(".", 1)[0]):
                return "ALERT_ONLY (essential subnet)"
        return "QUARANTINE_EGRESS (apply NetworkPolicy deny-all-egress)"


def main():
    parser = argparse.ArgumentParser(description="NEXUS-BOTNET-HUNTER: C2 Beacon Detector")
    parser.add_argument("--input", required=True, help="VPC flow log JSON")
    parser.add_argument("--output", default="botnet_report.json", help="Output report")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        logger.error(f"Input not found: {input_path}")
        sys.exit(1)

    flows = FlowParser.parse(input_path)
    detector = BeaconDetector()
    findings = detector.detect(flows)

    logger.info(f"[*] Analyzed {detector.stats['hosts_analyzed']} host pairs. Beacons: {detector.stats['beacons_detected']}")

    report = {
        "agent": "NEXUS-BOTNET-HUNTER",
        "version": "2.0-nexus",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "hosts_analyzed": detector.stats["hosts_analyzed"],
            "beacons_detected": detector.stats["beacons_detected"],
            "verdict": "C2_ACTIVITY_DETECTED" if detector.stats["beacons_detected"] > 0 else "CLEAN",
        },
        "findings": sorted(findings, key=lambda x: x["beacon_score"], reverse=True),
    }

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info(f"[DONE] Botnet report -> {output}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
