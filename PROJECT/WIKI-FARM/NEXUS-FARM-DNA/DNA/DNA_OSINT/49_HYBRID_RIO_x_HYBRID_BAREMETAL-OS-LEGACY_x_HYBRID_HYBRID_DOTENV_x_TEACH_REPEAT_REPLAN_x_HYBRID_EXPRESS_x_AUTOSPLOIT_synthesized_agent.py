#!/usr/bin/env python3
"""
RIO__X__HYBRID_BAREMETAL-OS-LEGACY_x_HYBRID_HYBRID_DOTENV_x_TEACH_REPEAT_REPLAN_x_HYBRID_EXPRESS_x_AUTOSPLOIT [NEXUS SYNTHESIZED Gen-4]
Mission: Build a security audit and vulnerability detection tool
Heritage: RIO + HYBRID_BAREMETAL-OS-LEGACY_x_HYBRID_HYBRID_DOTENV_x_TEACH_REPEAT_REPLAN_x_HYBRID_EXPRESS_x_AUTOSPLOIT
Role: collector | Domains: infra & infra

I/O Contract:
  Input:  path (from CLI --target)
  Output: JSON report with typed findings/stats

Pipeline (1 stages, 3 blocks):
  Stage 1: [check_ports, system_info, process_list]
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

__all__ = ["main", "Pipeline"]


logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("RIO__X__HYBRID_BAREMETAL-OS-LEGACY_x_HYBRID_HYBRID_DOTENV_x_")

def __nexus_execute__(func, arg, output_type, findings_list, stats_dict, errors_list):
    try:
        _result = func(arg)
        if output_type == "findings":
            if isinstance(_result, list): findings_list.extend(_result)
            logger.info(f"  [{func.__name__}] {len(_result) if isinstance(_result, list) else 0} findings")
        elif output_type in ("stats", "tech_stack", "port_report", "system_info", "report"):
            if isinstance(_result, dict): stats_dict.update(_result)
            if output_type == "port_report" and isinstance(_result, list):
                for item in _result:
                    if isinstance(item, dict) and "type" not in item:
                        item.update({"type": func.__name__, "severity": "INFO", "detail": str(item), "source": "nexus_pipeline"})
                    findings_list.append(item)
            logger.info(f"  [{func.__name__}] OK")
        else:
            if isinstance(_result, list): findings_list.extend(_result)
            elif isinstance(_result, dict): stats_dict.update(_result)
            logger.info(f"  [{func.__name__}] OK")
    except Exception as e:
        errors_list.append(f"{func.__name__}: {e}")
        logger.warning(f"  [{func.__name__}] SKIP: {e}")


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



class Collector:
    """Gathers raw data from target and returns standardized findings"""

    def __init__(self):
        self.findings: List[Dict[str, Any]] = []
        self.all_stats: Dict[str, Any] = {}
        self.errors: List[str] = []

    def collect(self, target) -> List[Dict[str, Any]]:
        """COLLECTOR CONTRACT: collect(target) → List[Finding]"""
        self.findings = []
        self.errors = []
        # -- Stage 1 --
        __nexus_execute__(check_ports, target, "port_report", self.findings, getattr(self, "all_stats", {}), self.errors)
        __nexus_execute__(system_info, target, "system_info", self.findings, getattr(self, "all_stats", {}), self.errors)
        __nexus_execute__(process_list, target, "findings", self.findings, getattr(self, "all_stats", {}), self.errors)
        return self.findings

    def summary(self) -> Dict[str, Any]:
        risk = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in self.findings:
            risk[f.get("severity", "INFO")] = risk.get(f.get("severity", "INFO"), 0) + 1
        return {"total": len(self.findings), "errors": len(self.errors), "risk": risk, "stats": self.all_stats}



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
    parser = argparse.ArgumentParser(description="RIO__X__HYBRID_BAREMETAL-OS-LEGACY_x_HYBRID_HYBRID_DOTENV_x_TEACH_REPEAT_REPLAN_x_HYBRID_EXPRESS_x_AUTOSPLOIT")
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
    report = {"agent": "RIO__X__HYBRID_BAREMETAL-OS-LEGACY_x_HYBRID_HYBRID_DOTENV_x_TEACH_REPEAT_REPLAN_x_HYBRID_EXPRESS_x_AUTOSPLOIT", "findings": findings, "summary": agent.summary()}

    # Display summary if report is a dict with findings
    if isinstance(report, dict) and "findings" in report:
        crits = [f for f in report["findings"] if f.get("severity") in ("CRITICAL", "HIGH")]
        if crits:
            print(f"\n{'='*60}")
            print(f"⚠ {len(crits)} CRITICAL/HIGH FINDINGS:")
            print(f"{'='*60}")
            for f in crits[:10]:
                print(f"  [{f.get('severity')}] {f.get('detail')}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
