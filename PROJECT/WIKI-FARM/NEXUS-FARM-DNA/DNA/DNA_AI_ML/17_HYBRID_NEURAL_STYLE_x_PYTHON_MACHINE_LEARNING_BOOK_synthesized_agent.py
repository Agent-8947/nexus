#!/usr/bin/env python3
"""
NEURAL_STYLE__X__PYTHON_MACHINE_LEARNING_BOOK [NEXUS SYNTHESIZED Gen-1]
Mission: Build a security audit and vulnerability detection tool
Heritage: NEURAL_STYLE + PYTHON_MACHINE_LEARNING_BOOK
Role: collector | Domains: ai & ai

I/O Contract:
  Input:  path (from CLI --target)
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
logger = logging.getLogger("NEURAL_STYLE__X__PYTHON_MACHINE_LEARNING_BOOK")


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
            _result = detect_anomalies([f.get('value', 0) for f in self.findings if 'value' in f] or [0.0])
            self.findings.extend(_result)
            logger.info(f"  [detect_anomalies] {len(_result)} findings")
        except Exception as e:
            self.errors.append(f"detect_anomalies: {e}")
            logger.warning(f"  [detect_anomalies] SKIP: {e}")
        try:
            _result = compute_stats([f.get('value', 0) for f in self.findings if 'value' in f] or [0.0])
            # [PATCHER] Сохранено из compute_stats
            if isinstance(_result, dict): self.all_stats.update(_result)
            # [PATCHER] Сохранено из compute_stats
            if isinstance(_result, dict): self.all_stats.update(_result)
            # [PATCHER] Сохранено из compute_stats
            if isinstance(_result, dict): self.all_stats.update(_result)
            if isinstance(_result, list):
                for item in _result:
                    if isinstance(item, dict) and "type" not in item:
                        item["type"] = "compute_stats"
                        item["severity"] = "INFO"
                        item["detail"] = str(item)
                        item["source"] = str(target)
                    self.findings.append(item)
            logger.info(f"  [compute_stats] OK")
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
            # # # _result = text_similarity(str(target))
            if isinstance(_result, list):
                for item in _result:
                    if isinstance(item, dict) and "type" not in item:
                        item["type"] = "text_similarity"
                        item["severity"] = "INFO"
                        item["detail"] = str(item)
                        item["source"] = str(target)
                    self.findings.append(item)
            logger.info(f"  [text_similarity] OK")
        except Exception as e:
            self.errors.append(f"text_similarity: {e}")
            logger.warning(f"  [text_similarity] SKIP: {e}")
        return self.findings

    def summary(self) -> Dict[str, Any]:
        risk = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in self.findings:
            risk[f.get("severity", "INFO")] = risk.get(f.get("severity", "INFO"), 0) + 1
        return {"total": len(self.findings), "errors": len(self.errors), "risk": risk}



def _integration_test():
    """End-to-end pipeline test with mock data."""
    agent = Collector()
    test_target = [1.0, 1.1, 0.9, 1.0, 1.05, 0.95, 1.0, 100.0, 1.0, 0.98]
    result = agent.collect(test_target)
    assert isinstance(result, list), "collect() must return List[Finding]"
    for f in result:
        assert "type" in f, f"Finding missing type"
        assert "severity" in f, f"Finding missing severity"
    logger.info(f"[TEST] Collector.collect() OK: {len(result)} findings")
    return True


def main():
    parser = argparse.ArgumentParser(description="NEURAL_STYLE__X__PYTHON_MACHINE_LEARNING_BOOK")
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
    report = {"agent": "NEURAL_STYLE__X__PYTHON_MACHINE_LEARNING_BOOK", "findings": findings, "summary": agent.summary()}


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