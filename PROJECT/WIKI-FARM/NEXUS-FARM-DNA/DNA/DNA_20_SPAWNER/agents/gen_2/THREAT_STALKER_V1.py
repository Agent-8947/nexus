#!/usr/bin/env python3
"""
AGENT ID: THREAT_STALKER_V1 [GEN-3 TRUE ARCHITECTURE]
PROTOCOL: NEXUS V5.0 HARDENED
====================================================
Adversarial Review Fixes:
1. SECURITY: Eliminated Security Theater. Separation of channels. Key is NEVER returned via API. 
   Keys are logged to a local secure keystore mapped by audit_id.
2. ROBUSTNESS: Async file I/O via asyncio.to_thread. Safe dictionary accesses (.get).
3. API DESIGN: Proper HTTP 500/400 exceptions. No 200 OK on failure.
4. CLI/SERVER: The CLI now properly boots the Uvicorn server or runs a local audit.
"""

import json
import logging
import asyncio
import uuid
from pathlib import Path
from datetime import datetime
from cryptography.fernet import Fernet
from fastapi import FastAPI, HTTPException, Request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import uvicorn
import typer

# ── ARCHITECTURAL CONFIG ────────────────────────────────────────────────
NODE_ID = "THREAT_STALKER_V1"
GEN = 3

BASE_DIR = Path(__file__).resolve().parent
SOURCE_FILE = BASE_DIR.parent.parent.parent.parent / "WIKI-FARM" / "farm_library.json"
KEYSTORE_FILE = BASE_DIR / "secure_vault.keystore"
AUDIT_LOG_FILE = BASE_DIR / "stalker_audit.log"

app = FastAPI(title=f"NEXUS {NODE_ID} Core v{GEN}.0")
cli = typer.Typer()

# Unified Audit Logging
logging.basicConfig(
    filename=AUDIT_LOG_FILE,
    level=logging.INFO,
    format=f"%(asctime)s - [{NODE_ID}-G{GEN}] - %(levelname)s - %(message)s"
)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(f"[{NODE_ID}] %(levelname)s - %(message)s"))
logger = logging.getLogger(NODE_ID)
logger.addHandler(console_handler)

class KeystoreManager:
    """Manages out-of-band encryption keys."""
    @staticmethod
    def store_key(audit_id: str, key: bytes):
        keys = {}
        if KEYSTORE_FILE.exists():
            with open(KEYSTORE_FILE, 'r') as f:
                keys = json.load(f)
        keys[audit_id] = key.decode()
        with open(KEYSTORE_FILE, 'w') as f:
            json.dump(keys, f, indent=2)
            
    @staticmethod
    def get_key(audit_id: str) -> bytes:
        if not KEYSTORE_FILE.exists():
            return None
        with open(KEYSTORE_FILE, 'r') as f:
            keys = json.load(f)
        key_str = keys.get(audit_id)
        return key_str.encode() if key_str else None

class TrueThreatStalker:
    def __init__(self, data_path: Path):
        self.data_path = data_path

    async def _async_read_data(self) -> dict:
        """Properly avoids blocking the event loop with synchronous disk I/O."""
        if not self.data_path.exists():
            raise FileNotFoundError(f"OSINT Target Database Missing: {self.data_path}")
            
        def read_json():
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        return await asyncio.to_thread(read_json)

    async def execute_ml_pipeline(self) -> dict:
        """Functional machine learning pipeline for threat cluster isolation."""
        raw = await self._async_read_data()
        
        records = []
        for url, meta in raw.get("REPOSITORIES", {}).items():
            # Robust mapping handling missing keys
            name = meta.get('name', 'Unknown_Entity')
            desc = meta.get('description', '') or ''
            topics = ' '.join(meta.get('topics', []))
            records.append({"u": url, "t": f"{name} {desc} {topics}", "n": name})
        
        if not records:
            raise ValueError("Data source contains no repository targets.")
            
        df = pd.DataFrame(records)
        
        # Scikit-learn Density Clustering
        vectorizer = TfidfVectorizer(max_features=150, stop_words='english')
        X = vectorizer.fit_transform(df['t'])
        km = KMeans(n_clusters=min(4, len(df)), random_state=42, n_init='auto')
        df['cluster'] = km.fit_predict(X)
        
        # Determine highest threat cluster without hardcoding the ID
        threat_vocab = ["exploit", "cve", "malware", "osint", "recon", "botnet", "bypass", "payload"]
        cluster_threat_density = {}
        for c_id in df['cluster'].unique():
            cluster_data = df[df['cluster'] == c_id]
            mask = cluster_data['t'].str.contains('|'.join(threat_vocab), case=False)
            density = float(mask.sum() / len(cluster_data))
            cluster_threat_density[int(c_id)] = density
            
        target_cluster = max(cluster_threat_density, key=cluster_threat_density.get)
        threat_assets = df[df['cluster'] == target_cluster]
        
        results = threat_assets['n'].tolist()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "ml_model": "TF-IDF + KMeans(n=4)",
            "threat_cluster_id": int(target_cluster),
            "threat_density": round(cluster_threat_density[target_cluster], 3),
            "total_threats_found": len(results),
            "critical_assets": results # Return the full list, let the client paginate/truncate
        }

@app.middleware("http")
async def audit_middleware(request: Request, call_next):
    """Enforces audit logging for all API operations."""
    start_time = datetime.now()
    response = await call_next(request)
    duration = (datetime.now() - start_time).total_seconds()
    logger.info(f"API_AUDIT: {request.method} {request.url.path} | Status: {response.status_code} | Duration: {duration}s")
    return response

@app.get("/intel/v3/scan")
async def api_scan_threats():
    """
    TRUE SECURITY ARCHITECTURE:
    The API generates a payload, encrypts it, and returns the ciphertext.
    The encryption key is intentionally excluded from the response.
    It is committed to the local Keystore. 
    """
    audit_id = str(uuid.uuid4())
    logger.info(f"Initializing threat scan via API. Audit ID: {audit_id}")
    
    try:
        stalker = TrueThreatStalker(SOURCE_FILE)
        report = await stalker.execute_ml_pipeline()
        
        # Channel separation: Key generation and local storage
        session_key = Fernet.generate_key()
        KeystoreManager.store_key(audit_id, session_key)
        
        # Encryption
        cipher = Fernet(session_key)
        encrypted_payload = cipher.encrypt(json.dumps(report).encode()).decode()
        
        return {
            "status": "SECURE_TRANSMISSION",
            "audit_id": audit_id,
            "data": encrypted_payload,
            "instruction": "Retrieve key from the local secure_vault.keystore using the audit_id to decrypt."
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Internal Pipeline Failure: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal intelligence pipeline failure.")

@cli.command()
def serve(host: str = "127.0.0.1", port: int = 8000):
    """Boot the API Server."""
    logger.info(f"Booting NEXUS Threat Stalker API on {host}:{port}")
    uvicorn.run(app, host=host, port=port, log_level="warning")

@cli.command()
def local_audit():
    """Run the analysis locally and display the decrypted results."""
    logger.info(f"Executing Local Machine Intelligence Audit...")
    try:
        stalker = TrueThreatStalker(SOURCE_FILE)
        report = asyncio.run(stalker.execute_ml_pipeline())
        logger.info(f"Execution complete. Found {report['total_threats_found']} assets in threat cluster {report['threat_cluster_id']}.")
        print(json.dumps(report, indent=2))
    except Exception as e:
        logger.error(f"Local audit failed: {e}")

if __name__ == "__main__":
    cli()
