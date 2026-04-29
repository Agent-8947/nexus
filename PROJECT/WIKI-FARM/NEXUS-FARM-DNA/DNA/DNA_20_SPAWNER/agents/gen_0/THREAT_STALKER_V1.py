#!/usr/bin/env python3
"""
AGENT ID: THREAT_STALKER_V1 [GEN-0 ANALYZER]
PROTOCOL: NEXUS V5.0 HARDENED
====================================================
Role: Threat Intelligence Analyzer (OSINT)
Security: CRITICAL (Fernet Encryption)
Interface: API (FastAPI)
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from cryptography.fernet import Fernet
from fastapi import FastAPI
import pandas as pd

# ── CONFIG BLOCK ────────────────────────────────────────────────────────
NODE_ID = "THREAT_STALKER_V1"
SOURCE_FILE = Path(__file__).resolve().parent.parent.parent.parent / "WIKI-FARM" / "farm_library.json"
# Create an encryption key for this session
SESSION_KEY = Fernet.generate_key()
cipher = Fernet(SESSION_KEY)

app = FastAPI(title="NEXUS Threat Stalker API")
logging.basicConfig(level=logging.INFO, format=f"%(asctime)s - [{NODE_ID}] - %(message)s")
logger = logging.getLogger(NODE_ID)

class ThreatStalker:
    def __init__(self, data_path: Path):
        self.data_path = data_path
        if not self.data_path.exists():
            raise FileNotFoundError("Real OSINT data required.")

    def analyze_threats(self):
        """Analyzes repository topics for high-risk security tools."""
        logger.info("Deep-scanning repository library for threat indicators...")
        
        with open(self.data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        records = []
        for url, meta in data.get("REPOSITORIES", {}).items():
            records.append({
                "name": meta.get("name"),
                "topics": ",".join(meta.get("topics", [])),
                "desc": (meta.get("description") or "").lower()
            })
            
        df = pd.DataFrame(records)
        
        # Threat Detection Logic: Critical Keywords
        threat_mask = df['topics'].str.contains('exploit|malware|cve|rce|backdoor', case=False) | \
                      df['desc'].str.contains('exploit|malware|vulnerability|zero-day', case=False)
        
        matches = df[threat_mask]
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "detected_threat_count": len(matches),
            "targets": matches['name'].tolist()
        }
        
        # Security: Critical - Encrypting the report
        report_bytes = json.dumps(report).encode()
        encrypted_report = cipher.encrypt(report_bytes)
        
        return encrypted_report.decode(), SESSION_KEY.decode()

@app.get("/threat-report")
async def get_intel():
    stalker = ThreatStalker(SOURCE_FILE)
    encrypted_data, key = stalker.analyze_threats()
    return {
        "node_id": NODE_ID,
        "status": "ENCRYPTED_INTEL_READY",
        "payload": encrypted_data,
        "note": "Use the provided session_key for decryption via Fernet."
    }

if __name__ == "__main__":
    import uvicorn
    # Standalone execution for testing
    logger.info("Standalone mode: generating report for local audit log...")
    stalker = ThreatStalker(SOURCE_FILE)
    report, key = stalker.analyze_threats()
    print(f"\n[STALKER] SESSION_KEY: {key}")
    print(f"[STALKER] ENCRYPTED_REPORT: {report[:50]}...")
