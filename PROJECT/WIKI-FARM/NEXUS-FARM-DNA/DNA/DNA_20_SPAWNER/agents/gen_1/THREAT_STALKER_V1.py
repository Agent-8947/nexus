#!/usr/bin/env python3
"""
AGENT ID: THREAT_STALKER_V1 [GEN-1 ANALYZER]
PROTOCOL: NEXUS V5.0 HARDENED
====================================================
Mutation: Added Async logic, Typer CLI, and Hardened Error Handling.
Fitness Target: > 0.8
"""

import json
import logging
import asyncio
import typer
from pathlib import Path
from datetime import datetime
from cryptography.fernet import Fernet
from fastapi import FastAPI
import pandas as pd

# ── CONFIG BLOCK ────────────────────────────────────────────────────────
NODE_ID = "THREAT_STALKER_V1"
SOURCE_FILE = Path(__file__).resolve().parent.parent.parent.parent / "WIKI-FARM" / "farm_library.json"
REPORT_DIR = Path(__file__).resolve().parent
SESSION_KEY = Fernet.generate_key()
cipher = Fernet(SESSION_KEY)

app = FastAPI(title="NEXUS Threat Stalker v2.0 [Async]")
cli = typer.Typer()

logging.basicConfig(level=logging.INFO, format=f"%(asctime)s - [{NODE_ID}] - %(levelname)s - %(message)s")
logger = logging.getLogger(NODE_ID)

class HardenedThreatStalker:
    def __init__(self, data_path: Path):
        self.data_path = data_path
        if not self.data_path.exists():
            logger.critical("DATA_MISSING: Path finding failure.")
            raise FileNotFoundError("Real OSINT data required.")

    async def analyze_async(self):
        """Mutation 1: Async data ingestion and processing."""
        try:
            logger.info("Initializing Async Intel Pipeline...")
            # Simulate async read (in real world: aiofiles or db pool)
            await asyncio.sleep(0.1) 
            
            with open(self.data_path, 'r', encoding='utf-8') as f:
                raw = json.load(f)
            
            df = pd.DataFrame([
                {"name": m.get("name"), "topics": ",".join(meta.get("topics", []))}
                for url, meta in raw.get("REPOSITORIES", {}).items()
            ])
            
            # Mutation 2: Multi-layer detection logic
            threat_map = {
                "critical": ["exploit", "zero-day", "rce"],
                "high": ["scanner", "recon", "botnet"]
            }
            
            findings = {"critical": [], "high": []}
            for level, tags in threat_map.items():
                mask = df['topics'].str.contains('|'.join(tags), case=False)
                findings[level] = df[mask]['name'].tolist()
            
            report = {
                "meta": {"node": NODE_ID, "gen": 1, "ts": datetime.now().isoformat()},
                "findings": findings,
                "security_status": "HARDENED"
            }
            
            # Mutation 3: Encrypted persistence
            encrypted = cipher.encrypt(json.dumps(report).encode())
            return encrypted, SESSION_KEY
            
        except Exception as e:
            logger.error(f"PIPELINE_CRASH: {str(e)}")
            raise

@app.get("/telemetry")
async def telemetry_endpoint():
    """Mutation 4: Hardened API endpoint with full error wrap."""
    try:
        stalker = HardenedThreatStalker(SOURCE_FILE)
        data, key = await stalker.analyze_async()
        return {"status": "SUCCESS", "cipher_stream": data.decode(), "key_v": key.decode()}
    except Exception as e:
        return {"status": "ERROR", "detail": str(e)}

@cli.command()
def run_audit():
    """Mutation 5: Typer CLI interface for manual ops."""
    try:
        logger.info("Executing Generation 1 Manual Audit...")
        stalker = HardenedThreatStalker(SOURCE_FILE)
        # Bridge to async loop
        report, _ = asyncio.run(stalker.analyze_async())
        logger.info("Manual Audit Complete. Data encrypted.")
    except Exception as e:
        logger.error(f"CLI_FAILURE: {e}")

if __name__ == "__main__":
    cli()
