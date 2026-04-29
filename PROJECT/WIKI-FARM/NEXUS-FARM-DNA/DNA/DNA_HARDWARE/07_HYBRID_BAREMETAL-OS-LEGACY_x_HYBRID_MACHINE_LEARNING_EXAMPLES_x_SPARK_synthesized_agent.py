#!/usr/bin/env python3
"""
BAREMETAL-OS-LEGACY__X__HYBRID_MACHINE_LEARNING_EXAMPLES_x_SPARK [NEXUS SYNTHESIZED Gen-2]
Mission: Build a security audit and vulnerability detection tool
Heritage: BAREMETAL-OS-LEGACY + HYBRID_MACHINE_LEARNING_EXAMPLES_x_SPARK
Role: library | Domains: infra & ai
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import re, math, csv, statistics
import re, socket, subprocess, platform

__all__ = ["main"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("BAREMETAL-OS-LEGACY__X__HYBRID_MACHINE_LEARNING_EXAMPLES_x_S")


# ── TCP port scanner for common service ports ──
def check_ports(host: str, ports: list[int] = None, timeout: float = 1.0) -> list[dict]:
    """Check which TCP ports are open on a host."""
    import socket
    if ports is None:
        ports = [22, 80, 443, 3306, 5432, 6379, 8080, 8443, 9200, 27017]
    results = []
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                r = s.connect_ex((host, port))
                results.append({"port": port, "open": r == 0})
        except Exception:
            results.append({"port": port, "open": False, "error": True})
    return results


# ── Local system info collector (OS, CPU, Python version) ──
def get_system_info() -> dict:
    """Collect system information."""
    import platform, os
    return {
        "os": platform.system(), "release": platform.release(),
        "machine": platform.machine(), "python": platform.python_version(),
        "cpu_count": os.cpu_count(),
        "hostname": platform.node(),
    }


# ── Cross-platform process listing ──
def list_processes() -> list[dict]:
    """List running processes (cross-platform)."""
    import subprocess, platform
    procs = []
    try:
        if platform.system() == "Windows":
            out = subprocess.check_output(["tasklist", "/FO", "CSV"], text=True, timeout=5)
            import csv
            for row in csv.DictReader(out.strip().splitlines()):
                procs.append({"name": row.get("Image Name", ""), "pid": row.get("PID", ""),
                              "mem": row.get("Mem Usage", "")})
        else:
            out = subprocess.check_output(["ps", "aux", "--no-headers"], text=True, timeout=5)
            for line in out.strip().splitlines()[:100]:
                parts = line.split(None, 10)
                if len(parts) >= 11:
                    procs.append({"user": parts[0], "pid": parts[1], "cpu": parts[2],
                                  "mem": parts[3], "cmd": parts[10][:80]})
    except Exception:
        pass
    return procs


# ── Statistical Z-Score anomaly detection ──
def detect_anomalies_zscore(values: list[float], threshold: float = 3.0) -> list[dict]:
    """Z-Score anomaly detection on numeric series."""
    import math
    if len(values) < 5:
        return []
    mean = sum(values) / len(values)
    var = sum((v - mean) ** 2 for v in values) / len(values)
    std = math.sqrt(var) if var > 0 else 1e-8
    anomalies = []
    for i, v in enumerate(values):
        z = abs(v - mean) / std
        if z >= threshold:
            anomalies.append({"index": i, "value": v, "zscore": round(z, 3),
                              "severity": "CRITICAL" if z >= 4 else "WARNING"})
    return anomalies


# ── TF-based cosine similarity between two texts ──
def cosine_similarity(text_a: str, text_b: str) -> float:
    """Compute cosine similarity between two texts using word frequency."""
    import math, re
    def tokenize(t):
        words = re.findall(r"[a-z]+", t.lower())
        freq = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
        return freq
    fa, fb = tokenize(text_a), tokenize(text_b)
    all_words = set(fa) | set(fb)
    dot = sum(fa.get(w, 0) * fb.get(w, 0) for w in all_words)
    norm_a = math.sqrt(sum(v ** 2 for v in fa.values()))
    norm_b = math.sqrt(sum(v ** 2 for v in fb.values()))
    if norm_a < 1e-8 or norm_b < 1e-8:
        return 0.0
    return round(dot / (norm_a * norm_b), 4)


# ── Descriptive statistics (mean, median, std, quartiles, IQR) ──
def compute_stats(values: list[float]) -> dict:
    """Compute descriptive statistics for a numeric series."""
    import math, statistics
    if not values:
        return {}
    s = sorted(values)
    n = len(s)
    mean = sum(s) / n
    median = statistics.median(s)
    std = statistics.stdev(s) if n > 1 else 0.0
    q1 = statistics.median(s[:n//2]) if n > 2 else s[0]
    q3 = statistics.median(s[(n+1)//2:]) if n > 2 else s[-1]
    return {"count": n, "mean": round(mean, 4), "median": round(median, 4),
            "std": round(std, 4), "min": s[0], "max": s[-1],
            "q1": round(q1, 4), "q3": round(q3, 4), "iqr": round(q3 - q1, 4)}


def main():
    parser = argparse.ArgumentParser(description="BAREMETAL-OS-LEGACY__X__HYBRID_MACHINE_LEARNING_EXAMPLES_x_SPARK")
    parser.add_argument("--target", required=True, help="Target path or URL")
    parser.add_argument("--output", default="report.json", help="Output JSON report")
    args = parser.parse_args()

    target = args.target
    logger.info(f"[START] {target}")

    results = {}

    try:
        results["port_check"] = port_check(target)
        logger.info(f"  [port_check] OK")
    except Exception as e:
        logger.warning(f"  [port_check] SKIP: {e}")

    try:
        results["system_info"] = system_info(target)
        logger.info(f"  [system_info] OK")
    except Exception as e:
        logger.warning(f"  [system_info] SKIP: {e}")

    report = {
        "agent": "BAREMETAL-OS-LEGACY__X__HYBRID_MACHINE_LEARNING_EXAMPLES_x_SPARK",
        "version": "1.0-gen2",
        "timestamp": datetime.now().isoformat(),
        "target": target,
        "results": results,
    }

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    logger.info(f"[DONE] Report -> {output}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
