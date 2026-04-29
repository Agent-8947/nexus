#!/usr/bin/env python3
"""
GRAFANA__X__ANOMALIB [NEXUS SYNTHESIZED Gen-1]
Mission: Real-time metric anomaly detection with statistical scoring
Heritage: GRAFANA (monitoring/visualization) + ANOMALIB (anomaly detection)
Role: analyzer | Security: none | Interface: cli | Domains: infra & ai

This agent reads time-series metrics (JSON/CSV), detects anomalies using
statistical models (Z-score, IQR, rolling MAD), and produces a Grafana-
compatible alert report. Pure Python — no ML frameworks required.
"""

import sys
import csv
import json
import math
import logging
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from collections import deque

__all__ = ["main", "AnomalyDetector"]

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("GRAFANA_x_ANOMALIB")


@dataclass
class AnomalyAlert:
    """Single anomaly detection alert."""
    metric_name: str
    timestamp: str
    value: float
    expected_range: Tuple[float, float]
    deviation_score: float        # How many sigma/IQR deviations
    method: str                   # zscore | iqr | rolling_mad
    severity: str                 # CRITICAL | WARNING | INFO
    context: Dict[str, float] = field(default_factory=dict)


@dataclass
class MetricSummary:
    """Statistical summary of a metric series."""
    name: str
    count: int
    mean: float
    median: float
    std: float
    min_val: float
    max_val: float
    q1: float
    q3: float
    iqr: float
    anomaly_count: int = 0
    anomaly_rate: float = 0.0


class AnomalyDetector:
    """Multi-method anomaly detector for time-series metrics.
    
    Combines three approaches inspired by Anomalib's ensemble philosophy:
    1. Z-Score: Classical statistical distance from mean
    2. IQR (Interquartile Range): Robust to outliers
    3. Rolling MAD (Median Absolute Deviation): Adaptive local detection
    """

    def __init__(
        self,
        zscore_threshold: float = 3.0,
        iqr_multiplier: float = 1.5,
        mad_window: int = 30,
        mad_threshold: float = 3.5,
    ):
        self.zscore_threshold = zscore_threshold
        self.iqr_multiplier = iqr_multiplier
        self.mad_window = mad_window
        self.mad_threshold = mad_threshold
        self.alerts: List[AnomalyAlert] = []

    @staticmethod
    def _median(values: List[float]) -> float:
        s = sorted(values)
        n = len(s)
        if n == 0:
            return 0.0
        mid = n // 2
        return s[mid] if n % 2 else (s[mid - 1] + s[mid]) / 2.0

    @staticmethod
    def _percentile(values: List[float], pct: float) -> float:
        s = sorted(values)
        n = len(s)
        if n == 0:
            return 0.0
        idx = (pct / 100.0) * (n - 1)
        lo = int(math.floor(idx))
        hi = int(math.ceil(idx))
        if lo == hi:
            return s[lo]
        frac = idx - lo
        return s[lo] * (1 - frac) + s[hi] * frac

    def _classify_severity(self, score: float, method: str) -> str:
        """Assign severity based on deviation score."""
        if method == "zscore":
            if score >= 4.0:
                return "CRITICAL"
            elif score >= 3.0:
                return "WARNING"
            return "INFO"
        elif method == "iqr":
            if score >= 3.0:
                return "CRITICAL"
            elif score >= 1.5:
                return "WARNING"
            return "INFO"
        else:  # rolling_mad
            if score >= 5.0:
                return "CRITICAL"
            elif score >= 3.5:
                return "WARNING"
            return "INFO"

    def detect_zscore(self, metric_name: str, timestamps: List[str], values: List[float]):
        """Z-Score anomaly detection — global statistical deviation."""
        if len(values) < 5:
            return
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        std = math.sqrt(variance) if variance > 0 else 1e-8

        for ts, val in zip(timestamps, values):
            z = abs(val - mean) / std
            if z >= self.zscore_threshold:
                self.alerts.append(AnomalyAlert(
                    metric_name=metric_name,
                    timestamp=ts,
                    value=val,
                    expected_range=(mean - self.zscore_threshold * std, mean + self.zscore_threshold * std),
                    deviation_score=round(z, 3),
                    method="zscore",
                    severity=self._classify_severity(z, "zscore"),
                    context={"mean": round(mean, 3), "std": round(std, 3)},
                ))

    def detect_iqr(self, metric_name: str, timestamps: List[str], values: List[float]):
        """IQR-based anomaly detection — robust to skewed distributions."""
        if len(values) < 10:
            return
        q1 = self._percentile(values, 25)
        q3 = self._percentile(values, 75)
        iqr = q3 - q1
        if iqr < 1e-8:
            return
        lower = q1 - self.iqr_multiplier * iqr
        upper = q3 + self.iqr_multiplier * iqr

        for ts, val in zip(timestamps, values):
            if val < lower or val > upper:
                distance = max(abs(val - lower), abs(val - upper)) / iqr
                self.alerts.append(AnomalyAlert(
                    metric_name=metric_name,
                    timestamp=ts,
                    value=val,
                    expected_range=(round(lower, 3), round(upper, 3)),
                    deviation_score=round(distance, 3),
                    method="iqr",
                    severity=self._classify_severity(distance, "iqr"),
                    context={"q1": round(q1, 3), "q3": round(q3, 3), "iqr": round(iqr, 3)},
                ))

    def detect_rolling_mad(self, metric_name: str, timestamps: List[str], values: List[float]):
        """Rolling Median Absolute Deviation — adaptive local anomaly detection."""
        if len(values) < self.mad_window:
            return
        window: deque = deque(maxlen=self.mad_window)

        for i, (ts, val) in enumerate(zip(timestamps, values)):
            window.append(val)
            if len(window) < self.mad_window:
                continue

            w_list = list(window)
            med = self._median(w_list)
            mad = self._median([abs(v - med) for v in w_list])
            if mad < 1e-8:
                continue

            # Modified Z-score using MAD (0.6745 = normal distribution constant)
            mod_z = 0.6745 * abs(val - med) / mad
            if mod_z >= self.mad_threshold:
                self.alerts.append(AnomalyAlert(
                    metric_name=metric_name,
                    timestamp=ts,
                    value=val,
                    expected_range=(round(med - self.mad_threshold * mad / 0.6745, 3),
                                    round(med + self.mad_threshold * mad / 0.6745, 3)),
                    deviation_score=round(mod_z, 3),
                    method="rolling_mad",
                    severity=self._classify_severity(mod_z, "rolling_mad"),
                    context={"window_median": round(med, 3), "mad": round(mad, 6)},
                ))

    def analyze(self, metric_name: str, timestamps: List[str], values: List[float]) -> MetricSummary:
        """Run all three detection methods on a single metric series."""
        self.detect_zscore(metric_name, timestamps, values)
        self.detect_iqr(metric_name, timestamps, values)
        self.detect_rolling_mad(metric_name, timestamps, values)

        mean = sum(values) / len(values) if values else 0
        med = self._median(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values) if values else 0
        std = math.sqrt(variance)
        q1 = self._percentile(values, 25)
        q3 = self._percentile(values, 75)

        metric_alerts = [a for a in self.alerts if a.metric_name == metric_name]
        # Deduplicate by timestamp (same point flagged by multiple methods)
        unique_ts = set(a.timestamp for a in metric_alerts)

        return MetricSummary(
            name=metric_name,
            count=len(values),
            mean=round(mean, 3),
            median=round(med, 3),
            std=round(std, 3),
            min_val=min(values) if values else 0,
            max_val=max(values) if values else 0,
            q1=round(q1, 3),
            q3=round(q3, 3),
            iqr=round(q3 - q1, 3),
            anomaly_count=len(unique_ts),
            anomaly_rate=round(len(unique_ts) / max(len(values), 1), 4),
        )


def load_metrics(path: Path) -> Dict[str, Dict[str, List]]:
    """Load metrics from JSON or CSV.
    
    Expected JSON format:
        {"metrics": {"cpu_usage": {"timestamps": [...], "values": [...]}, ...}}
    Expected CSV format:
        timestamp, metric_name, value
    """
    text = path.read_text(encoding="utf-8")

    if path.suffix == ".json":
        data = json.loads(text)
        return data.get("metrics", data)

    elif path.suffix == ".csv":
        reader = csv.DictReader(text.splitlines())
        metrics: Dict[str, Dict[str, List]] = {}
        for row in reader:
            name = row.get("metric_name", row.get("metric", "unknown"))
            ts = row.get("timestamp", row.get("ts", ""))
            val = float(row.get("value", row.get("val", 0)))
            if name not in metrics:
                metrics[name] = {"timestamps": [], "values": []}
            metrics[name]["timestamps"].append(ts)
            metrics[name]["values"].append(val)
        return metrics

    else:
        raise ValueError(f"Unsupported format: {path.suffix} (use .json or .csv)")


def main():
    parser = argparse.ArgumentParser(
        description="GRAFANA x ANOMALIB — Metric Anomaly Detector Agent"
    )
    parser.add_argument("--input", required=True, help="Input metrics file (.json or .csv)")
    parser.add_argument("--output", default="anomaly_report.json", help="Output JSON report")
    parser.add_argument("--zscore", type=float, default=3.0, help="Z-score threshold (default: 3.0)")
    parser.add_argument("--iqr-mult", type=float, default=1.5, help="IQR multiplier (default: 1.5)")
    parser.add_argument("--mad-window", type=int, default=30, help="Rolling MAD window size")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        logger.error(f"Input not found: {input_path}")
        sys.exit(1)

    metrics = load_metrics(input_path)
    logger.info(f"[*] Loaded {len(metrics)} metric series from {input_path.name}")

    detector = AnomalyDetector(
        zscore_threshold=args.zscore,
        iqr_multiplier=args.iqr_mult,
        mad_window=args.mad_window,
    )

    summaries = []
    for name, series in metrics.items():
        timestamps = series.get("timestamps", [f"t{i}" for i in range(len(series.get("values", [])))])
        values = series.get("values", [])
        if not values:
            continue
        summary = detector.analyze(name, timestamps, values)
        summaries.append(summary)
        logger.info(f"  [{summary.name}] {summary.count} points, {summary.anomaly_count} anomalies ({summary.anomaly_rate:.1%})")

    # Build Grafana-compatible alert report
    report = {
        "agent": "GRAFANA__X__ANOMALIB",
        "version": "1.0-gen1",
        "mission": "Metric Anomaly Detection (Statistical Ensemble)",
        "timestamp": datetime.now().isoformat(),
        "source": str(input_path),
        "detection_config": {
            "zscore_threshold": args.zscore,
            "iqr_multiplier": args.iqr_mult,
            "mad_window": args.mad_window,
        },
        "summary": {
            "total_metrics": len(summaries),
            "total_anomalies": sum(s.anomaly_count for s in summaries),
            "critical_alerts": sum(1 for a in detector.alerts if a.severity == "CRITICAL"),
            "warning_alerts": sum(1 for a in detector.alerts if a.severity == "WARNING"),
        },
        "metric_summaries": [
            {
                "name": s.name, "count": s.count,
                "mean": s.mean, "median": s.median, "std": s.std,
                "min": s.min_val, "max": s.max_val,
                "q1": s.q1, "q3": s.q3, "iqr": s.iqr,
                "anomaly_count": s.anomaly_count,
                "anomaly_rate": s.anomaly_rate,
            }
            for s in summaries
        ],
        "alerts": [
            {
                "metric": a.metric_name,
                "timestamp": a.timestamp,
                "value": a.value,
                "expected_range": list(a.expected_range),
                "deviation_score": a.deviation_score,
                "method": a.method,
                "severity": a.severity,
                "context": a.context,
            }
            for a in sorted(detector.alerts, key=lambda x: x.deviation_score, reverse=True)
        ],
    }

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info(f"[REPORT] {len(detector.alerts)} alerts → {output}")

    crits = [a for a in detector.alerts if a.severity == "CRITICAL"]
    if crits:
        print(f"\n{'='*60}")
        print(f"⚠ {len(crits)} CRITICAL ANOMALIES DETECTED:")
        print(f"{'='*60}")
        for a in crits[:10]:
            print(f"  [{a.method}] {a.metric_name} = {a.value} (expected {a.expected_range})")
            print(f"         deviation: {a.deviation_score}σ @ {a.timestamp}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
