#!/usr/bin/env python3
"""
AGENT ID: PANDAS__X__APPINFOSCANNER [GEN-1 ANALYZER]
PROTOCOL: NEXUS V5.0 HARDENED
====================================================
Role: Tech Stack Profiler
Input: farm_library.json (Local Repository Data)
Output: app_stack_profile.json
"""

import json
import logging
import pandas as pd
from pathlib import Path
from datetime import datetime

# ── CONFIG BLOCK ────────────────────────────────────────────────────────
NODE_ID = "PANDAS__X__APPINFOSCANNER"
SOURCE_FILE = Path(__file__).resolve().parent.parent.parent.parent / "farm_library.json"
OUTPUT_REPORT = Path(__file__).resolve().parent / "app_stack_profile.json"
LOG_FORMAT = f"%(asctime)s - [{NODE_ID}] - %(levelname)s - %(message)s"

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(NODE_ID)

class AppStackProfiler:
    def __init__(self, data_path: Path):
        self.data_path = data_path
        if not data_path.exists():
            raise FileNotFoundError(f"Missing mandatory data source: {data_path}")

    def ingest(self) -> pd.DataFrame:
        """Loads and normalizes the repository library."""
        logger.info(f"Ingesting OSINT data from {self.data_path.name}")
        with open(self.data_path, 'r', encoding='utf-8') as f:
            raw = json.load(f)
        
        records = []
        for url, meta in raw.get("REPOSITORIES", {}).items():
            records.append({
                "repo_name": meta.get("name"),
                "desc": (meta.get("description") or "").lower(),
                "ts": meta.get("topics", [])
            })
        return pd.DataFrame(records)

    def compute_stack_intelligence(self, df: pd.DataFrame) -> dict:
        """Core Implementation: Profiling application types without mocks."""
        logger.info("Profiling tech stack across the library...")
        
        stack_patterns = {
            "web_frameworks": ["react", "vue", "nextjs", "flask", "django", "fastapi"],
            "data_science": ["pandas", "numpy", "tensorflow", "pytorch", "scikit-learn"],
            "security_tools": ["scanner", "audit", "exploit", "recon", "brute"],
            "languages": ["python", "javascript", "typescript", "rust", "go", "cpp"]
        }
        
        profile = {
            "generation_ts": datetime.now().isoformat(),
            "total_apps_analyzed": len(df),
            "stack_distribution": {}
        }
        
        for category, keywords in stack_patterns.items():
            # Real search logic in description and topics
            mask = df['desc'].str.contains('|'.join(keywords), na=False) | \
                   df['ts'].apply(lambda x: any(k in x for k in keywords))
            
            matches = df[mask]
            profile["stack_distribution"][category] = {
                "count": int(len(matches)),
                "dominance_score": round(len(matches) / len(df), 4)
            }
            
        return profile

    def persist(self, data: dict):
        """Saves the intelligence report."""
        with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Synthesized Intelligence saved to {OUTPUT_REPORT.name}")

def main():
    try:
        profiler = AppStackProfiler(SOURCE_FILE)
        data = profiler.ingest()
        report = profiler.compute_stack_intelligence(data)
        profiler.persist(report)
        print(f"\n[SYNTHESIS COMPLETE] Profiled {report['total_apps_analyzed']} assets. Intelligence Ready.")
    except Exception as e:
        logger.error(f"Synthesis Aborted: {str(e)}")

if __name__ == "__main__":
    main()
