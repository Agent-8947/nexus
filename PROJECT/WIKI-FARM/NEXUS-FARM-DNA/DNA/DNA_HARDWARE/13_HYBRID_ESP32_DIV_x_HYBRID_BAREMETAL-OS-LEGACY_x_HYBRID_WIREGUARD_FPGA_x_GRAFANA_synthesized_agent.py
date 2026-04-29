#!/usr/bin/env python3
"""
ESP32_DIV__X__HYBRID_BAREMETAL-OS-LEGACY_x_HYBRID_WIREGUARD_FPGA_x_GRAFANA [NEXUS SYNTHESIZED Gen-3]
Mission: Build a security audit and vulnerability detection tool
Heritage: ESP32_DIV + HYBRID_BAREMETAL-OS-LEGACY_x_HYBRID_WIREGUARD_FPGA_x_GRAFANA
Role: collector | Domains: hardware & hardware

I/O Contract:
  Input:  path (from CLI --target)
  Output: JSON report with typed findings/stats

Pipeline (1 stages, 1 blocks):
  Stage 1: [find_serial_ports]
"""

import sys
import json
import logging
import argparse
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import re, platform, subprocess

__all__ = ["main", "Pipeline"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("ESP32_DIV__X__HYBRID_BAREMETAL-OS-LEGACY_x_HYBRID_WIREGUARD_")


# ── [HARDWARE] Discover available serial ports (Windows/Linux) ──
def find_serial_ports(target: str) -> List[Dict[str, Any]]:
    """Discover available serial ports. Returns findings."""
    findings: List[Dict[str, Any]] = []
    if platform.system() == "Windows":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DEVICEMAP\SERIALCOMM")
            i = 0
            while True:
                try:
                    name, val, _ = winreg.EnumValue(key, i)
                    findings.append({"type": "serial_port", "severity": "INFO",
                                     "detail": f"{val} ({name})", "source": target})
                    i += 1
                except OSError:
                    break
        except Exception:
            findings.append({"type": "serial_scan", "severity": "INFO",
                             "detail": "No serial ports found (Windows)", "source": target})
    else:
        for p in Path("/dev").glob("tty*"):
            if any(x in p.name for x in ("USB", "ACM", "AMA")):
                findings.append({"type": "serial_port", "severity": "INFO",
                                 "detail": str(p), "source": target})
    return findings



class Collector:
    """Gathers raw data from target and returns standardized findings"""

    def __init__(self):
        self.findings: List[Dict[str, Any]] = []
        self.errors: List[str] = []

    def collect(self, target) -> List[Dict[str, Any]]:
        """COLLECTOR CONTRACT: collect(target) → List[Finding]"""
        self.findings = []
        self.errors = []
        # -- Stage 1 --
        try:
            _result = find_serial_ports(str(target))
            self.findings.extend(_result)
            logger.info(f"  [find_serial_ports] {len(_result)} findings")
        except Exception as e:
            self.errors.append(f"find_serial_ports: {e}")
            logger.warning(f"  [find_serial_ports] SKIP: {e}")
        return self.findings

    def summary(self) -> Dict[str, Any]:
        risk = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in self.findings:
            risk[f.get("severity", "INFO")] = risk.get(f.get("severity", "INFO"), 0) + 1
        return {"total": len(self.findings), "errors": len(self.errors), "risk": risk}



def _integration_test():
    """End-to-end pipeline test with mock data."""
    agent = Collector()
    test_target = "localhost"
    result = agent.collect(test_target)
    assert isinstance(result, list), "collect() must return List[Finding]"
    for f in result:
        assert "type" in f, f"Finding missing type"
        assert "severity" in f, f"Finding missing severity"
    logger.info(f"[TEST] Collector.collect() OK: {len(result)} findings")
    return True


def main():
    parser = argparse.ArgumentParser(description="ESP32_DIV__X__HYBRID_BAREMETAL-OS-LEGACY_x_HYBRID_WIREGUARD_FPGA_x_GRAFANA")
    parser.add_argument("--target", default=None, help="Target (path)")
    parser.add_argument("--output", default="report.json", help="Output JSON report")
    parser.add_argument("--test", action="store_true", help="Run integration test")
    args = parser.parse_args()

    if args.test:
        _integration_test()
        return

    if not args.target:
        parser.error("--target is required (use --test for self-test)")

    target = Path(args.target).resolve()

    agent = Collector()
    findings = agent.collect(target)
    report = {"agent": "ESP32_DIV__X__HYBRID_BAREMETAL-OS-LEGACY_x_HYBRID_WIREGUARD_FPGA_x_GRAFANA", "findings": findings, "summary": agent.summary()}


    crits = [f for f in report["findings"] if f["severity"] in ("CRITICAL", "HIGH")]
    if crits:
        print(f"\n{'='*60}")
        print(f"⚠ {len(crits)} CRITICAL/HIGH FINDINGS:")
        print(f"{'='*60}")
        for f in crits[:10]:
            print(f"  [{f['severity']}] {f['detail']}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
