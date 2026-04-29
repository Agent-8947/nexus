#!/usr/bin/env python3
"""
AGENT ID: PANDAS__X__BLACK-HAT-RUST [GEN-1 ANALYZER]
PROTOCOL: NEXUS V5.0 HARDENED
====================================================
Role: OSINT Analyzer (Security Stack Auditor)
Input: farm_library.json (Local OSINT Data Source)
Output: security_audit_report.json
"""

import json
import logging
import pandas as pd
from pathlib import Path
from datetime import datetime

# ── CONFIG BLOCK (From Traits) ──────────────────────────────────────────
NODE_ID = "PANDAS__X__BLACK-HAT-RUST"
SOURCE_FILE = Path(__file__).resolve().parent.parent.parent.parent / "farm_library.json"
OUTPUT_FILE = Path(__file__).resolve().parent / "security_audit_report.json"
LOG_LEVEL = logging.INFO

# Setup Logging
logging.basicConfig(
    level=LOG_LEVEL,
    format=f"%(asctime)s - [{NODE_ID}] - %(levelname)s - %(message)s"
)
logger = logging.getLogger(NODE_ID)

class SecurityStackAnalyzer:
    """Real OSINT Analyzer: Scans the repository library for stack vulnerabilities."""
    
    def __init__(self, source_path: Path):
        self.source_path = source_path
        if not self.source_path.exists():
            logger.error(f"Source data missing: {self.source_path}")
            raise FileNotFoundError("Real data source is required.")

    def load_data(self) -> pd.DataFrame:
        """Input Handler: Processes the actual repository library JSON."""
        logger.info(f"Ingesting real data from: {self.source_path.name}")
        with open(self.source_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Flattening repository metadata
        flat_data = []
        for repo_url, meta in data.get("REPOSITORIES", {}).items():
            flat_data.append({
                "url": repo_url,
                "name": meta.get("name"),
                "topics": ",".join(meta.get("topics", [])),
                "description": meta.get("description", "")
            })
        return pd.DataFrame(flat_data)

    def audit_security_stack(self, df: pd.DataFrame):
        """Core Logic: Performing real analytics on the osint database."""
        logger.info("Starting security audit of the repository stack...")
        
        # Detection logic for sensitive tech keywords
        keywords = {
            "critical_recon": ["shodan", "censys", "recon", "osint"],
            "vulnerability_research": ["exploit", "cve", "poc", "bypass"],
            "automation": ["bot", "crawler", "agent"]
        }
        
        audit_results = {
            "timestamp": datetime.now().isoformat(),
            "total_investigated": len(df),
            "findings": {}
        }
        
        for category, tags in keywords.items():
            mask = df['topics'].str.contains('|'.join(tags), case=False) | \
                   df['description'].str.contains('|'.join(tags), case=False)
            matches = df[mask]
            audit_results["findings"][category] = {
                "count": len(matches),
                "samples": matches['name'].head(5).tolist()
            }
        
        return audit_results

    def save_output(self, result: dict):
        """Output Handler: Persistence to local storage."""
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        logger.info(f"Security Audit Report exported to: {OUTPUT_FILE.name}")

def main():
    try:
        analyzer = SecurityStackAnalyzer(SOURCE_FILE)
        raw_db = analyzer.load_data()
        
        # Real execution loop
        report = analyzer.audit_security_stack(raw_db)
        analyzer.save_output(report)
        
        print(f"\n[S-CORE] Audit Complete. Found {report['findings']['critical_recon']['count']} Recon Tools.")
        
    except Exception as e:
        logger.error(f"Execution Error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
