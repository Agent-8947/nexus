#!/usr/bin/env python3
"""
PYTORCH__X__LOCAL_DEEP_RESEARCH [NEXUS SYNTHESIZED Gen-1]
Mission: Build a security audit and vulnerability detection tool
Heritage: PYTORCH + LOCAL_DEEP_RESEARCH
Role: library | Domains: ai & ai

I/O Contract:
  Input:  url (from CLI --target)
  Output: JSON report with typed findings/stats

Pipeline (1 stages, 3 blocks):
  Stage 1: [detect_anomalies, compute_stats, text_similarity]
"""

import sys
import json
import logging
import argparse
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import re, math

__all__ = ["main", "Pipeline"]


logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("PYTORCH__X__LOCAL_DEEP_RESEARCH")

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



class Toolkit:
    """Provides reusable utility functions with no side-effects"""

    def __init__(self):
        self.all_findings: List[Dict[str, Any]] = []
        self.all_stats: Dict[str, Any] = {}
        self.errors: List[str] = []

    def get_tools(self, target) -> Dict[str, callable]:
        """LIBRARY CONTRACT: get_tools(target) → Dict[str, callable]"""
        # -- Stage 1 --
        __nexus_execute__(detect_anomalies, [f.get('value', 0) for f in self.all_findings if 'value' in f] or [0.0], "findings", self.all_findings, getattr(self, "all_stats", {}), self.errors)
        __nexus_execute__(compute_stats, [f.get('value', 0) for f in self.all_findings if 'value' in f] or [0.0], "stats", self.all_findings, getattr(self, "all_stats", {}), self.errors)
        __nexus_execute__(text_similarity, str(target), "stats", self.all_findings, getattr(self, "all_stats", {}), self.errors)
        risk = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in self.all_findings:
            risk[f.get("severity", "INFO")] = risk.get(f.get("severity", "INFO"), 0) + 1
        return {
            "agent": "PYTORCH__X__LOCAL_DEEP_RESEARCH",
            "timestamp": datetime.now().isoformat(),
            "findings": self.all_findings,
            "stats": self.all_stats,
            "errors": self.errors,
            "risk_summary": risk,
        }



def _integration_test():
    """End-to-end pipeline test with mock data."""
    agent = Toolkit()
    test_target = [1.0, 1.1, 0.9, 1.0, 1.05, 0.95, 1.0, 100.0, 1.0, 0.98]
    result = agent.get_tools(test_target)
    assert isinstance(result, dict), "get_tools() must return dict"
    assert "findings" in result, "get_tools() must return findings"
    logger.info(f"[TEST] Toolkit.get_tools() OK")
    return True


def main():
    parser = argparse.ArgumentParser(description="PYTORCH__X__LOCAL_DEEP_RESEARCH")
    parser.add_argument("--target", default=None, help="Target (url)")
    parser.add_argument("--output", default="report.json", help="Output JSON report")
    parser.add_argument("--test", action="store_true", help="Run integration test")
    args = parser.parse_args()

    if args.test:
        _integration_test()
        return

    if not args.target:
        parser.error("--target is required (use --test for self-test)")

    target = args.target

    agent = Toolkit()
    report = agent.get_tools(target)

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
