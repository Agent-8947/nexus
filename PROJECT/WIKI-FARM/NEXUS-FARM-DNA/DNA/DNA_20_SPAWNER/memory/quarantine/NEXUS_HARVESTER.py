#!/usr/bin/env python3
"""
AGENT ID: NEXUS_HARVESTER [GEN-0]
PROTOCOL: NEXUS V5.0 HARDENED (INDUSTRIAL MASTERPIECE)
====================================================
Topology: Local ETL Daemon
Resolution: Traits CLI + Security(High) = Local PBKDF2 Encrypted Vault.
No APIs. No keys in memory or logs. Complete cryptographic isolation.
"""

import json
import logging
import asyncio
import getpass
import os
import base64
from pathlib import Path
from datetime import datetime

import typer
import pandas as pd
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidKey

# ── ARCHITECTURAL CONFIG ────────────────────────────────────────────────
NODE_ID = "NEXUS_HARVESTER"
BASE_DIR = Path(__file__).resolve().parent
SOURCE_FILE = BASE_DIR.parent.parent.parent.parent / "WIKI-FARM" / "farm_library.json"
VAULT_FILE = BASE_DIR / "harvester_analytics.vault"

cli = typer.Typer(help="NEXUS Local ETL Daemon (Crypto-Vault)")

logging.basicConfig(level=logging.INFO, format=f"%(asctime)s - [{NODE_ID}] - %(levelname)s - %(message)s")
logger = logging.getLogger(NODE_ID)

class CryptoVault:
    """True cryptographic security utilizing user-provided passwords and PBKDF2."""
    
    @staticmethod
    def _derive_key(password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    @staticmethod
    def encrypt_data(password: str, data: dict) -> bytes:
        salt = os.urandom(16)
        key = CryptoVault._derive_key(password, salt)
        cipher = Fernet(key)
        payload = json.dumps(data).encode()
        encrypted = cipher.encrypt(payload)
        # We prepend the salt to the ciphertext so we can derive the key later
        return salt + encrypted

    @staticmethod
    def decrypt_data(password: str, raw_bytes: bytes) -> dict:
        try:
            salt, ciphertext = raw_bytes[:16], raw_bytes[16:]
            key = CryptoVault._derive_key(password, salt)
            cipher = Fernet(key)
            decrypted = cipher.decrypt(ciphertext)
            return json.loads(decrypted.decode())
        except InvalidKey:
            raise ValueError("FATAL: Invalid Vault Password or corrupted salt.")
        except Exception as e:
            raise RuntimeError(f"Decryption infrastructure failure: {e}")

class IndustrialHarvester:
    def __init__(self, data_path: Path):
        self.data_path = data_path

    async def execute_etl(self) -> dict:
        """Extract, Transform, and summarize intelligence metrics."""
        if not self.data_path.exists():
            raise FileNotFoundError(f"OSINT Data Missing: {self.data_path}")
            
        def read_json():
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        raw = await asyncio.to_thread(read_json)
        
        records = []
        for url, meta in raw.get("REPOSITORIES", {}).items():
            records.append({
                "name": meta.get('name', 'Unknown'),
                "lang": meta.get('language', 'Unknown'),
                "stars": int(meta.get('stargazers_count', 0)),
                "size_kb": int(meta.get('size', 0))
            })
            
        if not records:
            raise ValueError("Data source contains no usable records for ETL.")
            
        df = pd.DataFrame(records)
        
        # Transformation Metrics
        lang_stats = df.groupby('lang').agg(
            total_repos=('name', 'count'),
            total_stars=('stars', 'sum'),
            total_size_mb=('size_kb', lambda x: round(x.sum() / 1024, 2))
        ).reset_index().to_dict(orient='records')
        
        return {
            "node_type": "ETL_DAEMON",
            "timestamp": datetime.now().isoformat(),
            "total_harvested": len(df),
            "language_distribution": lang_stats,
            "global_metrics": {
                "max_stars": int(df['stars'].max()),
                "total_db_size_mb": round(df['size_kb'].sum() / 1024, 2)
            }
        }

@cli.command("harvest")
def cmd_harvest():
    """Run the ETL pipeline and store the result in a secure vault."""
    logger.info("Initializing Harvester ETL...")
    try:
        harvester = IndustrialHarvester(SOURCE_FILE)
        result = asyncio.run(harvester.execute_etl())
        
        logger.info(f"ETL Complete. Harvested metrics from {result['total_harvested']} repositories.")
        
        # Secure CLI Prompt for Master Password (no echoing)
        pwd = getpass.getpass("Enter Vault Master Password for encryption (Do not lose this): ")
        if len(pwd) < 4:
            raise ValueError("Password too weak. Operation aborted.")
            
        encrypted_bytes = CryptoVault.encrypt_data(pwd, result)
        
        with open(VAULT_FILE, "wb") as f:
            f.write(encrypted_bytes)
            
        logger.info(f"Target Acquired. Data securely locked in {VAULT_FILE.name}.")
        
    except Exception as e:
        logger.error(f"HARVEST_FAILED: {e}")
        raise typer.Exit(code=1)

@cli.command("decrypt")
def cmd_decrypt():
    """Retrieve and display the contents of the secure vault."""
    try:
        if not VAULT_FILE.exists():
            raise FileNotFoundError(f"Vault file missing: {VAULT_FILE}")
            
        pwd = getpass.getpass("Enter Vault Master Password for decryption: ")
        
        with open(VAULT_FILE, "rb") as f:
            raw_bytes = f.read()
            
        data = CryptoVault.decrypt_data(pwd, raw_bytes)
        
        logger.info("Access Granted. Payload:")
        print(json.dumps(data, indent=2))
        
    except ValueError as val_e:
        logger.critical(str(val_e))
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"DECRYPT_FAILED: {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    cli()
