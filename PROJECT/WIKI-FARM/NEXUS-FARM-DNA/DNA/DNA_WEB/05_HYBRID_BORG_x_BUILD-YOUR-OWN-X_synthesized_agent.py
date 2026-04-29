#!/usr/bin/env python3
"""
HYBRID_BORG_x_BUILD-YOUR-OWN-X v2.0 [NEXUS AI FLEET MANAGER]
=============================================================
Heritage: Borg (Cluster Orchestration) + Build-Your-Own-X (Custom Tooling)
Role:     ORCHESTRATOR - Manages AI monitoring lifecycle across nodes
Input:    Target log directory or system identifier
Output:   Consolidated Status Report
"""

import sys
import json
import time
import logging
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS-BORG")

# ── Paths ────────────────────────────────────────────────────────────────
DNA_DIR = Path(__file__).resolve().parent
HARVESTER = DNA_DIR / "HYBRID_ELASTICSEARCH_x_BUILD-YOUR-OWN-X_synthesized_agent.py"
FORECASTER = DNA_DIR / "HYBRID_AUTOFORMER_x_BUILD-YOUR-OWN-X_synthesized_agent.py"
# ────────────────────────────────────────────────────────────────────────

def run_agent(script: Path, args: list, label: str) -> bool:
    """Executes a sub-agent."""
    cmd = [sys.executable, str(script)] + args
    logger.info(f"[{label}] Launching: {script.name}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            logger.info(f"[{label}] SUCCESS")
            return True
        else:
            logger.error(f"[{label}] FAILED (Exit {result.returncode})")
            if result.stderr:
                logger.error(f"  Error: {result.stderr.splitlines()[-1]}")
            return False
    except Exception as e:
        logger.error(f"[{label}] FATAL ERROR: {e}")
        return False

def orchestrate(log_dir: Path, output_dir: Path):
    """Orchestrates Harvester -> Forecaster pipeline."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    telemetry_file = output_dir / "telemetry_dump.json"
    analysis_file  = output_dir / "analysis_result.json"
    
    t0 = time.time()
    logger.info("=== NEXUS BORG: Starting AI Monitoring Mission ===")
    
    # 1. Harvest
    ok1 = run_agent(HARVESTER, ["--duration", "3", "--logs", str(log_dir), "--output", str(telemetry_file)], "HARVEST")
    if not ok1:
        sys.exit(1)
        
    # 2. Forecast
    ok2 = run_agent(FORECASTER, ["--input", str(telemetry_file), "--output", str(analysis_file)], "FORECAST")
    if not ok2:
        sys.exit(1)
        
    # 3. Final Report
    analysis = json.loads(analysis_file.read_text(encoding="utf-8"))
    res = analysis["result"]
    elapsed = round(time.time() - t0, 1)
    
    print(f"\n{'='*70}")
    print(f" NEXUS AI FLEET STATUS: {res['verdict']} (Health: {res['health_score']})")
    print(f"{'='*70}")
    print(f"  CPU Avg: {res['avg_cpu']}% | RAM Avg: {res['avg_ram']}%")
    print(f"  Telemetry Samples: {len(json.loads(telemetry_file.read_text())['payload'])}")
    print(f"  Anomalies Detected: {len(res['anomalies'])}")
    print(f"  Orchestration Time: {elapsed}s")
    print(f"{'='*70}\n")
    
    logger.info(f"[DONE] Mission complete. Report at {analysis_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NEXUS AI Fleet Manager (Borg Hybrid)")
    parser.add_argument("--logs", default=".", help="Directory to scan logs")
    parser.add_argument("--outdir", default="ai_status", help="Output reports dir")
    args = parser.parse_args()
    
    orchestrate(Path(args.logs).resolve(), Path(args.outdir).resolve())
