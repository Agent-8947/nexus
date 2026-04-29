"""
GROQ-LLAMA TRANSLATOR v3.0 [NEXUS EDITION]
Translates PDF-JSON blocks using Groq API (Llama-3.1 7b/70b).
Extreme speed: 500+ tokens/sec.
"""

import json
import sys
import os
import requests
import time
from typing import List, Dict

# CONFIGURATION
API_KEY = "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"
MODEL = "llama-3.1-70b-versatile" # upgraded to 70B for best translation quality
API_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """You are a highly accurate technical translator. 
Translate the following English technical manual text blocks into Russian.
- Maintain a strict technical and professional tone.
- Keep model names (ADL07E06, Epson 3200A1, etc.) in English.
- Return ONLY the translation, no explanations.
- If the text is just a page number like "Page 1 of 68", translate as "Стр. 1 из 68"."""

def translate_batch(texts: List[str]) -> List[str]:
    """Translates a batch of texts to optimize API calls."""
    if not API_KEY or API_KEY == "gsk_...":
        print("[ERROR] GROQ_API_KEY not set. Set it in script or environment.")
        return texts

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "\n---\n".join(texts)}
        ],
        "temperature": 0.1,
        "max_tokens": 4096
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        full_response = response.json()["choices"][0]["message"]["content"]
        
        # Split back (handle edge cases)
        translated_parts = full_response.split("---")
        # Clean up each part
        cleaned = [p.strip() for p in translated_parts if p.strip()]
        
        # If output count doesn't match input, fallback to single translation (slow)
        if len(cleaned) != len(texts):
            return [translate_single(t) for t in texts]
        return cleaned
    except Exception as e:
        print(f"[RETRY ERROR] {str(e)}")
        return [translate_single(t) for t in texts]

def translate_single(text: str) -> str:
    """Fallback for problematic blocks."""
    if not text.strip() or len(text) < 2: return text
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        "temperature": 0.1
    }
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        return response.json()["choices"][0]["message"]["content"].strip()
    except:
        return text # Return original on failure

def process_file(raw_path, output_path):
    print(f"[PROCESS] Starting Groq translation: {raw_path}")
    with open(raw_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    result = {}
    
    # Flatten all valid text blocks for batching
    all_blocks = []
    for pg, items in data.items():
        for item in items:
            all_blocks.append((pg, item))

    # Translate in chunks of 5 for reliability and limits
    chunk_size = 5
    for i in range(0, len(all_blocks), chunk_size):
        chunk = all_blocks[i:i + chunk_size]
        en_texts = [item["en_text"] for pg, item in chunk]
        
        # Skip translations for pure numbers/symbols
        results = []
        for t in en_texts:
            import re
            if re.match(r'^[\d\s\.\,\-\+\%\℃\/\(\)\*×xXmMkKgGwWhHzZvV㎡]+$', t.strip()):
                results.append(t)
            else:
                # Actual translation via API
                translated = translate_batch([t])[0] # Simplified chunk for demo
                results.append(translated)

        # Re-map results back to result structure
        for (pg, item), ru in zip(chunk, results):
            if pg not in result: result[pg] = []
            result[pg].append({
                "bbox": item["bbox"],
                "en_text": item["en_text"],
                "ru_text": ru,
                "font_size": item["font_size"]
            })
        
        print(f"[PROGRESS] {i + len(chunk)} / {len(all_blocks)} blocks processed...")
        # Groq Free Tier Limit Friendly delay
        time.sleep(1.5)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"[DONE] Saved: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python groq_translate.py <raw_json> <output_json>")
    else:
        process_file(sys.argv[1], sys.argv[2])
