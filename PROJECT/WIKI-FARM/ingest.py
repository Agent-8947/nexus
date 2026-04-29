import json
import re
from pathlib import Path

# Extract REPO_DATA from index.html for NEXUS FARM-Oracle ingestion
HTML_FILE = Path(__file__).resolve().parent / "index.html"
OUTPUT_JSON = Path(__file__).resolve().parent / "farm_library.json"

def extract():
    if not HTML_FILE.exists():
        print(f"[!] Error: {HTML_FILE} not found")
        return

    content = HTML_FILE.read_text(encoding="utf-8")
    
    # Use regex to find the REPO_DATA array
    match = re.search(r"const REPO_DATA\s*=\s*(\[.*?\]);", content, re.DOTALL)
    if not match:
        print("[!] Error: Could not find REPO_DATA in HTML")
        return

    json_str = match.group(1)
    
    try:
        # Clean up some trailing commas if any, though standard JSON won't have them
        # Actually, it's JS, so it might have trailing commas.
        # We try to load it. If it fails, we might need a safer parser.
        data = json.loads(json_str) 
        
        OUTPUT_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=True), encoding="utf-8")
        print(f"[+] Successfully extracted {len(data)} repositories to {OUTPUT_JSON}")
    except Exception as e:
        print(f"[!] JSON Error: {e}")
        # Fallback: maybe it's not strictly valid JSON (e.g. key names without quotes)
        # But our previous edits used quoted keys.

if __name__ == "__main__":
    extract()
