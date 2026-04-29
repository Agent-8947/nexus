#!/usr/bin/env python3
"""
NEXUS DNA AI Agent: MODEL_DRIFT_MONITOR
Tier: A-Target (Production-Hardened)
Spec Hash: 4d4f44454c5f4452

Monitor ML models for performance drift and data distribution shifts.
"""

import logging
import math
import json
import sqlite3
import hashlib
import time
import sys
from dataclasses import dataclass, field, asdict
from typing import List

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("MODEL_DRIFT_MONITOR")

@dataclass
class DriftRecord:
    model_name: str
    metric: str
    reference_value: float
    current_value: float
    is_drifting: int

@dataclass
class DriftMonitorReport:
    model_name: str
    records: List[DriftRecord] = field(default_factory=list)
    scanned_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    errors: List[str] = field(default_factory=list)

class ModelDriftMonitorAgent:
    def __init__(self, db_path: str = "nexus_ai_ml.db"):
        self.db_path = db_path
        self._init_storage()

    def _init_storage(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""CREATE TABLE IF NOT EXISTS model_drift_monitor 
                                (id INTEGER PRIMARY KEY, model_name TEXT, metric TEXT, ref_val REAL, cur_val REAL, is_drifting INTEGER, data_hash TEXT UNIQUE, ts DATETIME DEFAULT CURRENT_TIMESTAMP)""")
                conn.commit()
            logger.info("Storage ready.")
        except sqlite3.Error as exc:
            logger.critical("DB init failed: %s", exc)
            raise SystemExit(1) from exc

    @staticmethod
    def _hash(payload: str) -> str:
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def calculate_kl_divergence(self, p: list, q: list) -> float:
        """Kullback-Leibler Divergence for drift detection."""
        return sum(pi * math.log(pi / qi) for pi, qi in zip(p, q) if pi > 0 and qi > 0)

    def execute_check(self, model_name: str, p_dist: list, q_dist: list) -> DriftMonitorReport:
        logger.info("Checking drift for model: %s", model_name)
        report = DriftMonitorReport(model_name=model_name)
        
        try:
            kl = self.calculate_kl_divergence(p_dist, q_dist)
            is_drifting = 1 if kl > 0.1 else 0
            logger.info("Drift for %s: %f (Drift: %d)", model_name, kl, is_drifting)
            
            record = DriftRecord(model_name=model_name, metric="KL-Divergence", reference_value=0.0, current_value=kl, is_drifting=is_drifting)
            report.records.append(record)
            self._persist(record)
        except Exception as e:
            logger.error("Failed to calculate drift: %s", e)
            report.errors.append(str(e))
            
        return report

    def _persist(self, m: DriftRecord) -> None:
        h = self._hash(f"{m.model_name}:{m.metric}:{m.current_value}")
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT OR IGNORE INTO model_drift_monitor (model_name, metric, ref_val, cur_val, is_drifting, data_hash) VALUES (?,?,?,?,?,?)",
                             (m.model_name, m.metric, m.reference_value, m.current_value, m.is_drifting, h))
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)

if __name__ == "__main__":
    if len(sys.argv) < 4: 
        print("Usage: python 24_MODEL_DRIFT_MONITOR_synthesized_agent.py <model> <p_dist_json> <q_dist_json>")
        sys.exit(1)
    try:
        p = json.loads(sys.argv[2])
        q = json.loads(sys.argv[3])
        print(json.dumps(asdict(ModelDriftMonitorAgent().execute_check(sys.argv[1], p, q)), indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
