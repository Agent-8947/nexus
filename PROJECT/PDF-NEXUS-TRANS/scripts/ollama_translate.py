"""
OLLAMA TECHNICAL TRANSLATOR v4.0 [NEXUS EDITION]
Uses Local Ollama Instance (localhost:11434).
Powered by qwen2.5-coder:3b.
"""

import json
import sys
import requests
import time
from typing import List

# CONFIGURATION
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:3b"

SYSTEM_PROMPT = """You are a professional technical translator for printing equipment.
Translate the following English technical manual text into Russian.
Guidelines:
- Maintain technical terminology (e.g., 'ink', 'powder shaking', 'mesh belt').
- Keep product models and trademarked names (Epson, ADL07K10) in English.
- Use a formal, engineering-style Russian tone.
- Do not provide explanations, only the translation.
- If text is a range or units (e.g., 18℃-30℃), keep the numbers and format.
- Output ONLY the translated text."""

def translate_via_ollama(text: str) -> str:
    """Sends a single block to local Ollama."""
    if not text.strip() or len(text) < 2:
        return text
    
    # Quick filter for numbers/symbols
    import re
    if re.match(r'^[\d\s\.\,\-\+\%\℃\/\(\)\*×xXmMkKgGwWhHzZvV㎡]+$', text.strip()):
        return text

    payload = {
        "model": MODEL,
        "prompt": f"{SYSTEM_PROMPT}\n\nText to translate: {text}",
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 1024
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        print(f"[ERROR] {text[:20]}... : {str(e)}")
        return text

def process_file(raw_path, output_path):
    print(f"[START] Translating {raw_path} via Ollama ({MODEL})...")
    with open(raw_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    translated_data = {}
    total_blocks = sum(len(items) for items in data.values())
    count = 0

    for page, blocks in data.items():
        translated_data[page] = []
        for block in blocks:
            en_text = block["en_text"]
            ru_text = translate_via_ollama(en_text)
            
            translated_data[page].append({
                "bbox": block["bbox"],
                "en_text": en_text,
                "ru_text": ru_text,
                "font_size": block["font_size"]
            })
            count += 1
            if count % 10 == 0:
                print(f"[PROGRESS] {count} / {total_blocks} blocks translated...")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(translated_data, f, ensure_ascii=False, indent=2)
    
    print(f"[DONE] File saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python ollama_translate.py <input.json> <output.json>")
    else:
        process_file(sys.argv[1], sys.argv[2])
