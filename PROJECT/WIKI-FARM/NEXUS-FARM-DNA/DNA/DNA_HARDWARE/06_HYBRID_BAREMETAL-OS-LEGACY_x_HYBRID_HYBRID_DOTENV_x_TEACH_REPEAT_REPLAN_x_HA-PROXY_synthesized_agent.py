#!/usr/bin/env python3
"""
BAREMETAL-OS-LEGACY__X__HYBRID_HYBRID_DOTENV_x_TEACH_REPEAT_REPLAN_x_HA-PROXY [NEXUS SYNTHESIZED Gen-3]
Mission: Build a security audit and vulnerability detection tool
Heritage: BAREMETAL-OS-LEGACY + HYBRID_HYBRID_DOTENV_x_TEACH_REPEAT_REPLAN_x_HA-PROXY
Role: library | Domains: infra & infra
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import re, socket, subprocess, platform

__all__ = ["main"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("BAREMETAL-OS-LEGACY__X__HYBRID_HYBRID_DOTENV_x_TEACH_REPEAT_")


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


def main():
    parser = argparse.ArgumentParser(description="BAREMETAL-OS-LEGACY__X__HYBRID_HYBRID_DOTENV_x_TEACH_REPEAT_REPLAN_x_HA-PROXY")
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
        "agent": "BAREMETAL-OS-LEGACY__X__HYBRID_HYBRID_DOTENV_x_TEACH_REPEAT_REPLAN_x_HA-PROXY",
        "version": "1.0-gen3",
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
