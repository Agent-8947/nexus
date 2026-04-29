#!/usr/bin/env python3
"""
OBJECT_DETECTION_METRICS__X__HYBRID_BAREMETAL-OS-LEGACY_x_HYBRID_MACHINE_LEARNING_EXAMPLES_x_SPARK [NEXUS SYNTHESIZED Gen-3]
Mission: Build a security audit and vulnerability detection tool
Heritage: OBJECT_DETECTION_METRICS + HYBRID_BAREMETAL-OS-LEGACY_x_HYBRID_MACHINE_LEARNING_EXAMPLES_x_SPARK
Role: analyzer | Domains: infra & ai

I/O Contract:
  Input:  hostname (from CLI --target)
  Output: JSON report with typed findings/stats

Pipeline (2 stages, 6 blocks):
  Stage 1: [check_ports, system_info, process_list]
  Stage 2: [detect_anomalies, compute_stats, text_similarity]
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
import re, math

__all__ = ["main", "Pipeline"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("OBJECT_DETECTION_METRICS__X__HYBRID_BAREMETAL-OS-LEGACY_x_HY")


# ── [AI] Z-Score + IQR anomaly detection on numeric series ──
def detect_anomalies(target: List[float]) -> List[Dict[str, Any]]:
    """Detect anomalies using Z-Score and IQR methods. Returns findings."""
    findings: List[Dict[str, Any]] = []
    if len(target) < 5:
        return findings
    mean = sum(target) / len(target)
    var = sum((v - mean) ** 2 for v in target) / len(target)
    std = math.sqrt(var) if var > 0 else 1e-8
    # Z-Score detection
    for i, v in enumerate(target):
        z = abs(v - mean) / std
        if z >= 3.0:
            findings.append({
                "type": "anomaly_zscore", "severity": "CRITICAL" if z >= 4.0 else "WARNING",
                "detail": f"Index {i}: value={v:.3f}, z-score={z:.2f}",
                "source": f"index_{i}",
                "index": i, "value": v, "score": round(z, 3),
            })
    # IQR detection
    s = sorted(target)
    n = len(s)
    q1 = s[n // 4]
    q3 = s[3 * n // 4]
    iqr = q3 - q1
    if iqr > 1e-8:
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        for i, v in enumerate(target):
            if v < lower or v > upper:
                dist = max(abs(v - lower), abs(v - upper)) / iqr
                findings.append({
                    "type": "anomaly_iqr", "severity": "HIGH",
                    "detail": f"Index {i}: value={v:.3f}, IQR distance={dist:.2f}",
                    "source": f"index_{i}",
                    "index": i, "value": v, "score": round(dist, 3),
                })
    return findings


# ── [AI] Descriptive statistics (mean, median, std, quartiles, IQR) ──
def compute_stats(target: List[float]) -> Dict[str, Any]:
    """Compute descriptive statistics for a numeric series. Returns stats."""
    if not target:
        return {"count": 0, "error": "empty input"}
    s = sorted(target)
    n = len(s)
    mean = sum(s) / n
    median = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
    var = sum((v - mean) ** 2 for v in s) / n
    std = math.sqrt(var)
    q1 = s[n // 4] if n >= 4 else s[0]
    q3 = s[3 * n // 4] if n >= 4 else s[-1]
    return {
        "count": n, "mean": round(mean, 4), "median": round(median, 4),
        "std": round(std, 4), "min": s[0], "max": s[-1],
        "q1": round(q1, 4), "q3": round(q3, 4), "iqr": round(q3 - q1, 4),
    }


# ── [AI] TF-based cosine similarity between text sections ──
def text_similarity(target: str) -> Dict[str, Any]:
    """Split text in half and compute self-similarity. Returns stats."""
    mid = len(target) // 2
    a, b = target[:mid], target[mid:]
    def tokenize(t):
        words = re.findall(r"[a-z]+", t.lower())
        freq: Dict[str, int] = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
        return freq
    fa, fb = tokenize(a), tokenize(b)
    all_words = set(fa) | set(fb)
    dot = sum(fa.get(w, 0) * fb.get(w, 0) for w in all_words)
    norm_a = math.sqrt(sum(v ** 2 for v in fa.values())) or 1e-8
    norm_b = math.sqrt(sum(v ** 2 for v in fb.values())) or 1e-8
    similarity = dot / (norm_a * norm_b)
    return {
        "similarity": round(similarity, 4),
        "tokens_a": len(fa), "tokens_b": len(fb),
        "method": "cosine_tf",
    }


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


class Pipeline:
    """Orchestrates 6 blocks in 2 stages."""

    def __init__(self):
        self.all_findings: List[Dict[str, Any]] = []
        self.all_stats: Dict[str, Any] = {}
        self.errors: List[str] = []

    def run(self, target) -> Dict[str, Any]:
        """Execute full pipeline. Target type: hostname."""

        # ── Stage 1 ──
        try:
            result = check_ports(target)
            self.all_stats["check_ports"] = result
            logger.info(f"  [check_ports] {len(result) if isinstance(result, list) else 1} items")
        except Exception as e:
            self.errors.append(f"check_ports: {e}")
            logger.warning(f"  [check_ports] SKIP: {e}")
        try:
            result = system_info(target)
            self.all_stats["system_info"] = result
            logger.info(f"  [system_info] {len(result) if isinstance(result, list) else 1} items")
        except Exception as e:
            self.errors.append(f"system_info: {e}")
            logger.warning(f"  [system_info] SKIP: {e}")
        try:
            result = process_list(target)
            self.all_findings.extend(result)
            logger.info(f"  [process_list] {len(result)} findings")
        except Exception as e:
            self.errors.append(f"process_list: {e}")
            logger.warning(f"  [process_list] SKIP: {e}")

        # ── Stage 2 ──
        try:
            result = detect_anomalies([f.get('value', 0) for f in self.all_findings if 'value' in f] or [0.0])
            self.all_findings.extend(result)
            logger.info(f"  [detect_anomalies] {len(result)} findings")
        except Exception as e:
            self.errors.append(f"detect_anomalies: {e}")
            logger.warning(f"  [detect_anomalies] SKIP: {e}")
        try:
            result = compute_stats([f.get('value', 0) for f in self.all_findings if 'value' in f] or [0.0])
            self.all_stats["compute_stats"] = result
            logger.info(f"  [compute_stats] stats collected")
        except Exception as e:
            self.errors.append(f"compute_stats: {e}")
            logger.warning(f"  [compute_stats] SKIP: {e}")
        try:
            # [PATCHER] Удалён артефакт text_similarity(str(target))
            # # [PATCHER] Удалён артефакт text_similarity(str(target))
            # [PATCHER] Удалён артефакт text_similarity(str(target))
            # # # [PATCHER] Удалён артефакт text_similarity(str(target))
            # [PATCHER] Удалён артефакт text_similarity(str(target))
            # # [PATCHER] Удалён артефакт text_similarity(str(target))
            # [PATCHER] Удалён артефакт text_similarity(str(target))
            # # # result = text_similarity(str(target))
            self.all_stats["text_similarity"] = result
            logger.info(f"  [text_similarity] stats collected")
        except Exception as e:
            self.errors.append(f"text_similarity: {e}")
            logger.warning(f"  [text_similarity] SKIP: {e}")

        # ── Build report ──
        risk_summary = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in self.all_findings:
            sev = f.get("severity", "INFO")
            risk_summary[sev] = risk_summary.get(sev, 0) + 1

        return {
            "agent": "OBJECT_DETECTION_METRICS__X__HYBRID_BAREMETAL-OS-LEGACY_x_HYBRID_MACHINE_LEARNING_EXAMPLES_x_SPARK",
            "version": "2.0-gen3",
            "timestamp": datetime.now().isoformat(),
            "pipeline_stages": 2,
            "blocks_executed": 6 - len(self.errors),
            "target": str(target),
            "risk_summary": risk_summary,
            "findings": self.all_findings,
            "stats": self.all_stats,
            "errors": self.errors,
        }


def _integration_test():
    """End-to-end pipeline test with mock data."""
    pipe = Pipeline()
    test_target = [1.0, 1.1, 0.9, 1.0, 1.05, 0.95, 1.0, 100.0, 1.0, 0.98]
    report = pipe.run(test_target)

    # Contract assertions
    assert isinstance(report, dict), "Report must be dict"
    assert "agent" in report, "Report must have agent field"
    assert "findings" in report, "Report must have findings field"
    assert "stats" in report, "Report must have stats field"
    assert "risk_summary" in report, "Report must have risk_summary"
    assert isinstance(report["findings"], list), "Findings must be list"
    for f in report["findings"]:
        assert "type" in f, f"Finding missing type: {f}"
        assert "severity" in f, f"Finding missing severity: {f}"
        assert "detail" in f, f"Finding missing detail: {f}"
        assert "source" in f, f"Finding missing source: {f}"
    logger.info(f"[TEST] Pipeline OK: {len(report['findings'])} findings, {len(report['errors'])} errors")
    return True


def main():
    parser = argparse.ArgumentParser(description="OBJECT_DETECTION_METRICS__X__HYBRID_BAREMETAL-OS-LEGACY_x_HYBRID_MACHINE_LEARNING_EXAMPLES_x_SPARK")
    parser.add_argument("--target", required=True, help="Target (hostname)")
    parser.add_argument("--output", default="report.json", help="Output JSON report")
    parser.add_argument("--test", action="store_true", help="Run integration test")
    args = parser.parse_args()

    if args.test:
        _integration_test()
        return

    target = args.target

    pipe = Pipeline()
    report = pipe.run(target)

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    logger.info(f"[DONE] {len(report['findings'])} findings → {output}")

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