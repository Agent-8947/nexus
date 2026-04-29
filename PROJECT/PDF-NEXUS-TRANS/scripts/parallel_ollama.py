"""
OLLAMA MULTI-THREAD TRANSLATOR v5.0 [NEXUS EDITION]
Fast parallel translation for large documents (e.g., 68 pages).
Distributes load across multiple Ollama workers.
"""

import json
import sys
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict

# CONFIGURATION
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"
THREADS = 1 # ECO MODE TO PREVENT OVERHEATING

SYSTEM_PROMPT = """You are a professional technical translator for printing equipment.
Translate English manual text into Russian. 
Rules: Formal style, keep models (Epson, ADL07E06) in English, NO explanations."""

def translate_single(text: str) -> str:
    if not text.strip() or len(text) < 2: return text
    
    # Give some time for thermal cooling between blocks
    time.sleep(0.5) 

    payload = {
        "model": MODEL,
        "prompt": f"{SYSTEM_PROMPT}\n\nText: {text}",
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 512}
    }
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=30)
        return r.json().get("response", "").strip()
    except Exception as e:
        return text

def process_parallel(raw_path, output_path):
    print(f"[START] Parallel Translation ({THREADS} threads) for {raw_path}")
    with open(raw_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Flatten pages for parallel processing
    flat_blocks = []
    for page, blocks in data.items():
        for i, b in enumerate(blocks):
            flat_blocks.append((page, i, b["en_text"]))

    results = []
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        # Submit all tasks
        futures = {executor.submit(translate_single, txt): (pg, idx, txt) for pg, idx, txt in flat_blocks}
        
        count = 0
        for future in futures:
            pg, idx, en = futures[future]
            ru = future.result()
            results.append((pg, idx, en, ru))
            count += 1
            
            # REAL-TIME PRINTING
            print(f"[{count}/{len(flat_blocks)}] PAGE {pg} | EN: {en[:40]}... -> RU: {ru[:40]}...")
            import sys
            sys.stdout.flush() 

            if count % 20 == 0:
                elapsed = time.time() - start_time
                speed = count / elapsed
                print(f"--- STATUS --- Speed: {speed:.2f} blk/s. Est. rem: {(len(flat_blocks)-count)/speed/60:.1f}m")
                sys.stdout.flush()

    # Reassemble JSON
    translated_data = {}
    for pg, idx, en, ru in results:
        if pg not in translated_data: translated_data[pg] = []
        # Find original font_size and bbox
        original_block = None
        for b in data[pg]:
            if b["en_text"] == en:
                original_block = b
                break
        
        translated_data[pg].append({
            "bbox": original_block["bbox"],
            "en_text": en,
            "ru_text": ru,
            "font_size": original_block["font_size"]
        })

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(translated_data, f, ensure_ascii=False, indent=2)
    print(f"[DONE] Total time: {(time.time()-start_time)/60:.1f}m. Saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python parallel_ollama.py <input.json> <output.json>")
    else:
        process_parallel(sys.argv[1], sys.argv[2])
