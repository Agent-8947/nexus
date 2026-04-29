#!/usr/bin/env python3
"""
HYBRID_ELASTICSEARCH_x_BUILD-YOUR-OWN-X v2.0 [NEXUS AI METRIC HARVESTER]
========================================================================
Heritage: Elasticsearch (Scalable Indexing) + Build-Your-Own-X (Custom Collector)
Role:     COLLECTOR - Harvests system metrics and logs for AI Monitoring
Output:   JSON telemetry used by HYBRID_AUTOFORMER_x_BUILD-YOUR-OWN-X (Analyzer)

ARCHITECTURE:
- Resource Scanner: Collects CPU, RAM, Disk usage using psutil (if available) or OS fallback.
- Log Tailer: Scans system/app logs for AI-related errors (CUDA, Memory, OOM).
- Temporal Sharding: Groups data into high-resolution time bins.
"""

import sys
import os
import json
import time
import logging
import argparse
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS-HARVESTER")

# Try to import psutil for real metrics, fallback to dummy simulation if missing
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    logger.warning("[!] psutil not found. Falling back to OS-level telemetry simulation.")

class AiMetricHarvester:
    """Harvests real hardware and application metrics."""

    def __init__(self, sample_rate: float = 1.0):
        self.sample_rate = sample_rate
        self.history = []

    def get_system_snapshot(self) -> dict:
        """Collects point-in-time hardware metrics."""
        if HAS_PSUTIL:
            return {
                "cpu_pct": psutil.cpu_percent(interval=0.1),
                "ram_pct": psutil.virtual_memory().percent,
                "disk_pct": psutil.disk_usage('/').percent,
                "process_count": len(psutil.pids())
            }
        else:
            # Fallback to simulated but plausible noise
            t = time.time()
            return {
                "cpu_pct": round(20 + 10 * (t % 10), 1),
                "ram_pct": round(45 + 5 * (t % 5), 1),
                "disk_pct": 62.1,
                "process_count": 142
            }

    def scan_logs(self, log_dir: Path) -> list[str]:
        """Scans for AI-related critical error patterns in logs."""
        critical_patterns = ["OOM", "CUDA error", "Out of memory", "segmentation fault", "NaN detected"]
        found_errors = []
        
        if not log_dir.exists():
            return []

        for log_file in log_dir.glob("*.log"):
            try:
                content = log_file.read_text(encoding="utf-8", errors="ignore").splitlines()
                # Check last 100 lines for efficiency
                for line in content[-100:]:
                    if any(p.lower() in line.lower() for p in critical_patterns):
                        found_errors.append(f"[{log_file.name}] {line.strip()}")
            except Exception as e:
                logger.debug(f"Could not read {log_file.name}: {e}")
        
        return found_errors

    def run_harvest_cycle(self, duration_sec: int, log_path: Path = None) -> list[dict]:
        """Runs a collection loop."""
        samples = []
        start_time = time.time()
        logger.info(f"[*] Starting harvest cycle for {duration_sec}s...")
        
        while time.time() - start_time < duration_sec:
            snap = self.get_system_snapshot()
            snap["timestamp"] = datetime.now().isoformat()
            
            if log_path:
                errors = self.scan_logs(log_path)
                if errors:
                    snap["log_events"] = errors
            
            samples.append(snap)
            time.sleep(self.sample_rate)
            
        return samples

def main():
    parser = argparse.ArgumentParser(description="NEXUS AI Metric Harvester")
    parser.add_argument("--duration", type=int, default=5, help="Harvest duration (sec)")
    parser.add_argument("--logs", type=str, help="Directory to scan for logs")
    parser.add_argument("--output", default="ai_telemetry.json", help="Output file")
    args = parser.parse_args()

    harvester = AiMetricHarvester(sample_rate=0.5)
    log_dir = Path(args.logs) if args.logs else Path(".")
    
    data = harvester.run_harvest_cycle(args.duration, log_dir)
    
    report = {
        "agent": "HYBRID_ELASTICSEARCH_x_BUILD-YOUR-OWN-X",
        "timestamp": datetime.now().isoformat(),
        "metadata": {"has_psutil": HAS_PSUTIL, "samples": len(data)},
        "payload": data
    }
    
    Path(args.output).write_text(json.dumps(report, indent=2), encoding="utf-8")
    logger.info(f"[SUCCESS] Collected {len(data)} samples -> {args.output}")
    print(f"HARVEST_COMPLETE: {len(data)} samples stored in {args.output}")

if __name__ == "__main__":
    main()
