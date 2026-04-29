#!/usr/bin/env python3
"""
AGENT ID: ANYTHING-LLM__X__DART [GEN-1 PROCESSOR]
PROTOCOL: NEXUS V5.0 HARDENED
====================================================
Role: Intelligent Entity Extractor (Recon)
Input: farm_library.json
Model: Ollama (Local Inference)
"""

import json
import logging
import subprocess
from pathlib import Path

# ── CONFIG BLOCK ────────────────────────────────────────────────────────
NODE_ID = "ANYTHING-LLM__X__DART"
SOURCE_FILE = Path(__file__).resolve().parent.parent.parent.parent / "farm_library.json"
OLLAMA_MODEL = "qwen2.5-coder:3b"
LOG_FORMAT = f"%(asctime)s - [{NODE_ID}] - %(levelname)s - %(message)s"

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(NODE_ID)

class LLR_Processor:
    """Large Language Recon: Process textual data via local AI model."""
    
    def __init__(self, model_name: str):
        self.model = model_name

    def call_ollama(self, prompt: str) -> str:
        """Real input handler for local LLM."""
        try:
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                capture_output=True, text=True, encoding='utf-8', timeout=60
            )
            return result.stdout.strip()
        except Exception as e:
            logger.error(f"Ollama call failed: {e}")
            return "ERROR: MODEL_OFFLINE"

    def process_dart_intel(self, source_path: Path):
        """Scans for Dart repos and uses AI to summarize their 'secret' purpose."""
        logger.info(f"Scanning library for Dart-specific intelligence...")
        
        with open(source_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        findings = []
        # Filter for Dart/Flutter repos
        for url, meta in data.get("REPOSITORIES", {}).items():
            desc = meta.get("description") or ""
            topics = meta.get("topics", [])
            
            if "dart" in desc.lower() or "dart" in topics:
                logger.info(f"Found Target: {meta['name']}. Analyzing with LLM...")
                
                prompt = f"Analyze this repo description and list top 3 technical capabilities in 1 string: {desc}"
                capabilities = self.call_ollama(prompt)
                
                findings.append({
                    "name": meta["name"],
                    "url": url,
                    "ai_extracted_capabilities": capabilities
                })
        
        return findings

def main():
    processor = LLR_Processor(OLLAMA_MODEL)
    if not SOURCE_FILE.exists():
        logger.error("Mandatory OSINT data source missing.")
        return

    intel = processor.process_dart_intel(SOURCE_FILE)
    
    output_path = Path(__file__).resolve().parent / "dart_intelligence.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(intel, f, indent=2, ensure_ascii=False)
        
    logger.info(f"Intelligent Recon complete. Found {len(intel)} high-value Dart assets.")

if __name__ == "__main__":
    main()
