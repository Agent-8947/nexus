#!/usr/bin/env python3
"""
HYBRID_AUTOFORMER_x_BUILD-YOUR-OWN-X v2.0 [NEXUS AI ANOMALY FORECASTER]
========================================================================
Heritage: Autoformer (Time-series Transformer) + Build-Your-Own-X (Custom Logic)
Role:     ANALYZER - Detects anomalies and forecasts resource exhaustion
Input:    JSON telemetry from HYBRID_ELASTICSEARCH_x_BUILD-YOUR-OWN-X (Harvester)
Output:   Enriched analysis JSON with health_score and alerts
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS-FORECASTER")

class AIAnomalyDetector:
    """Heuristic time-series analyzer inspired by Autoformer."""

    def __init__(self, thresholds: dict = None):
        self.thresholds = thresholds or {
            "cpu_high": 85.0,
            "ram_high": 90.0,
            "spike_limit": 30.0 # Delta between samples
        }

    def analyze_telemetry(self, samples: list[dict]) -> dict:
        """Processes telemetry samples for anomalies."""
        if not samples:
            return {"status": "EMPTY", "health_score": 1.0}

        cpu_vals = [s.get("cpu_pct", 0) for s in samples]
        ram_vals = [s.get("ram_pct", 0) for s in samples]
        events   = []
        
        # 1. Threshold Breach
        for i, s in enumerate(samples):
            if s.get("cpu_pct", 0) > self.thresholds["cpu_high"]:
                events.append({"ts": s["timestamp"], "type": "CPU_CRITICAL", "val": s["cpu_pct"]})
            if s.get("ram_pct", 0) > self.thresholds["ram_high"]:
                events.append({"ts": s["timestamp"], "type": "RAM_CRITICAL", "val": s["ram_pct"]})
            if "log_events" in s:
                for le in s["log_events"]:
                    events.append({"ts": s["timestamp"], "type": "LOG_ERROR", "msg": le})

        # 2. Trend Analysis (Spike Detection)
        cpu_avg = sum(cpu_vals) / len(cpu_vals)
        if len(cpu_vals) > 1:
            spike = max(abs(cpu_vals[i] - cpu_vals[i-1]) for i in range(1, len(cpu_vals)))
            if spike > self.thresholds["spike_limit"]:
                events.append({"type": "CPU_SPIKE", "delta": round(spike, 2)})

        # 3. Health Score Calculation
        penalty = len(events) * 0.15
        health_score = max(0.0, round(1.0 - penalty, 2))

        return {
            "health_score": health_score,
            "avg_cpu": round(cpu_avg, 2),
            "avg_ram": round(sum(ram_vals) / len(ram_vals), 2),
            "anomalies": events,
            "verdict": "HEALTHY" if health_score > 0.8 else "WARNING" if health_score > 0.4 else "CRITICAL"
        }

def main():
    parser = argparse.ArgumentParser(description="NEXUS AI Anomaly Forecaster")
    parser.add_argument("--input", required=True, help="Input telemetry JSON")
    parser.add_argument("--output", default="ai_analysis.json", help="Output analysis JSON")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Input not found: {input_path}")
        sys.exit(1)

    data = json.loads(input_path.read_text(encoding="utf-8"))
    samples = data.get("payload", [])
    
    detector = AIAnomalyDetector()
    analysis = detector.analyze_telemetry(samples)
    
    report = {
        "agent": "HYBRID_AUTOFORMER_x_BUILD-YOUR-OWN-X",
        "timestamp": datetime.now().isoformat(),
        "source": data.get("agent", "unknown"),
        "result": analysis
    }
    
    Path(args.output).write_text(json.dumps(report, indent=2), encoding="utf-8")
    
    logger.info(f"--- AI MONITOR VERDICT: {analysis['verdict']} (Score: {analysis['health_score']}) ---")
    if analysis['anomalies']:
        logger.warning(f"[!] Detected {len(analysis['anomalies'])} anomalies.")
    
    logger.info(f"[SUCCESS] Analysis -> {args.output}")

if __name__ == "__main__":
    main()
