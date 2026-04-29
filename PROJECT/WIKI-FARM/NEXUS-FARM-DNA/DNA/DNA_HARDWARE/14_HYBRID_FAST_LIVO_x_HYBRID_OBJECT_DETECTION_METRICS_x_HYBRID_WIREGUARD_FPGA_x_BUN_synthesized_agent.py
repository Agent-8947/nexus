#!/usr/bin/env python3
"""
FAST_LIVO__X__HYBRID_OBJECT_DETECTION_METRICS_x_HYBRID_WIREGUARD_FPGA_x_BUN [NEXUS SYNTHESIZED Gen-3]
Mission: Build a security audit and vulnerability detection tool
Heritage: FAST_LIVO + HYBRID_OBJECT_DETECTION_METRICS_x_HYBRID_WIREGUARD_FPGA_x_BUN
Role: collector | Domains: infra & hardware

I/O Contract:
  Input:  path (from CLI --target)
  Output: JSON report with typed findings/stats

Pipeline (1 stages, 4 blocks):
  Stage 1: [check_ports, system_info, process_list, find_serial_ports]
"""

import sys
import json
import logging
import argparse
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import os, re, socket, platform, subprocess
import re, platform, subprocess

__all__ = ["main", "Pipeline"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("FAST_LIVO__X__HYBRID_OBJECT_DETECTION_METRICS_x_HYBRID_WIREG")


# ── [INFRA] TCP port scanner for common service ports ──
_COMMON_PORTS = {22: "SSH", 80: "HTTP", 443: "HTTPS", 3306: "MySQL",
                 5432: "Postgres", 6379: "Redis", 8080: "HTTP-Alt",
                 8443: "HTTPS-Alt", 9200: "Elasticsearch", 27017: "MongoDB"}

def check_ports(target: str) -> List[Dict[str, Any]]:
    """Check which TCP ports are open on a host. Returns port_report."""
    results: List[Dict[str, Any]] = []
    for port, service in _COMMON_PORTS.items():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.0)
                is_open = s.connect_ex((target, port)) == 0
                results.append({"port": port, "open": is_open, "service": service})
        except Exception:
            results.append({"port": port, "open": False, "service": service, "error": True})
    return results


# ── [INFRA] Collect local system information (OS, CPU, Python version) ──
def system_info(target: str) -> Dict[str, Any]:
    """Collect system information. Returns system_info."""
    return {
        "os": platform.system(), "release": platform.release(),
        "machine": platform.machine(), "python": platform.python_version(),
        "cpu_count": os.cpu_count() or 0,
        "hostname": platform.node(),
        "queried_target": target,
    }


# ── [INFRA] List running processes (cross-platform) ──
def process_list(target: str) -> List[Dict[str, Any]]:
    """List running processes. Returns findings."""
    findings: List[Dict[str, Any]] = []
    try:
        if platform.system() == "Windows":
            out = subprocess.check_output(["tasklist", "/FO", "CSV", "/NH"], text=True, timeout=5)
            for line in out.strip().splitlines()[:50]:
                parts = line.strip('"').split('","')
                if len(parts) >= 2:
                    findings.append({
                        "type": "process", "severity": "INFO",
                        "detail": f"PID {parts[1]}: {parts[0]}",
                        "source": target,
                    })
        else:
            out = subprocess.check_output(["ps", "aux", "--no-headers"], text=True, timeout=5)
            for line in out.strip().splitlines()[:50]:
                parts = line.split(None, 10)
                if len(parts) >= 11:
                    findings.append({
                        "type": "process", "severity": "INFO",
                        "detail": f"PID {parts[1]}: {parts[10][:60]}",
                        "source": target,
                    })
    except Exception as e:
        findings.append({"type": "process_error", "severity": "MEDIUM",
                         "detail": str(e), "source": target})
    return findings


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
            _result = check_ports(str(target))
            # [PATCHER] Восстановлена передача данных из check_ports
            if isinstance(_result, list): self.findings.extend(_result)
            if isinstance(_result, list):
                for item in _result:
                    if isinstance(item, dict) and "type" not in item:
                        item["type"] = "check_ports"
                        item["severity"] = "INFO"
                        item["detail"] = str(item)
                        item["source"] = str(target)
                    self.findings.append(item)
            logger.info(f"  [check_ports] OK")
        except Exception as e:
            self.errors.append(f"check_ports: {e}")
            logger.warning(f"  [check_ports] SKIP: {e}")
        try:
            _result = system_info(str(target))
            # [PATCHER] Сохранено из system_info
            if isinstance(_result, dict): self.all_stats.update(_result)
            # [PATCHER] Сохранено из system_info
            if isinstance(_result, dict): self.all_stats.update(_result)
            # [PATCHER] Сохранено из system_info
            if isinstance(_result, dict): self.all_stats.update(_result)
            if isinstance(_result, list):
                for item in _result:
                    if isinstance(item, dict) and "type" not in item:
                        item["type"] = "system_info"
                        item["severity"] = "INFO"
                        item["detail"] = str(item)
                        item["source"] = str(target)
                    self.findings.append(item)
            logger.info(f"  [system_info] OK")
        except Exception as e:
            self.errors.append(f"system_info: {e}")
            logger.warning(f"  [system_info] SKIP: {e}")
        try:
            _result = process_list(str(target))
            self.findings.extend(_result)
            logger.info(f"  [process_list] {len(_result)} findings")
        except Exception as e:
            self.errors.append(f"process_list: {e}")
            logger.warning(f"  [process_list] SKIP: {e}")
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
    test_target = "127.0.0.1"
    result = agent.collect(test_target)
    assert isinstance(result, list), "collect() must return List[Finding]"
    for f in result:
        assert "type" in f, f"Finding missing type"
        assert "severity" in f, f"Finding missing severity"
    logger.info(f"[TEST] Collector.collect() OK: {len(result)} findings")
    return True


def main():
    parser = argparse.ArgumentParser(description="FAST_LIVO__X__HYBRID_OBJECT_DETECTION_METRICS_x_HYBRID_WIREGUARD_FPGA_x_BUN")
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
    report = {"agent": "FAST_LIVO__X__HYBRID_OBJECT_DETECTION_METRICS_x_HYBRID_WIREGUARD_FPGA_x_BUN", "findings": findings, "summary": agent.summary()}


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