import os
import re
import json
from pathlib import Path
from datetime import datetime

WIKI_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI")
OUTPUT_DIR = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI-FARM")
TEMPLATE_FILE = OUTPUT_DIR / "index.html"

def parse_analysis(file_path):
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None

    # Domain
    domain_match = re.search(r"\| \*\*Domain\*\* \| `(.*)` \|", content)
    domain = domain_match.group(1).strip() if domain_match else "OTHER"

    # Normalize to 7 vectors
    vec_map = {
        "AI": "AI / Cognitive",
        "DATA": "Data Intelligence",
        "SECURITY": "Security & Audit",
        "OSINT": "OSINT / Recce",
        "SYSTEMS": "Systems / HW",
        "ROBOTICS": "Robotics / UAV",
        "UAV": "Robotics / UAV",
        "CRYPTO": "Crypto & Privacy",
    }
    vector = vec_map.get(domain, "Core / Other")

    # Score
    score_match = re.search(r"\| \*\*NEXUS Value\*\* \| .* (\d+)/10 \|", content)
    score = int(score_match.group(1)) if score_match else 5

    # Summary -> Expand this
    summary = "N/A"
    # Find everything between ## Summary and the next ##
    summary_match = re.search(r"## Summary\n(.*?)(?=\n##|$)", content, re.DOTALL)
    if summary_match:
        summary = summary_match.group(1).strip().replace('"', '\\"').replace("\n", " ")

    # NEXUS Use -> We will merge this into summary for "more description" or handle as detail
    nexus_use = "N/A"
    use_match = re.search(r"## NEXUS Application\n(.*?)$", content, re.DOTALL)
    if use_match:
        nexus_use = use_match.group(1).strip().replace('"', '\\"').replace("\n", " ")

    # Technologies
    techs = []
    parts = content.split("## Key Technologies")
    if len(parts) > 1:
        tech_chunk = parts[1].split("##")[0].strip()
        for line in tech_chunk.split("\n"):
            m = re.search(r"- `(.*)`", line)
            if m:
                techs.append(m.group(1).strip())

    return {
        "name": file_path.parent.name,
        "domain": domain,
        "vector": vector,
        "score": score,
        "summary": summary,
        "nexus_use": nexus_use, # We leave it in JSON but will hide in UI
        "techs": techs,
    }


def build():
    print(f"\n{'='*60}")
    print(f"  NEXUS WIKI-FARM BUILDER [Updated Construction]")
    print(f"{'='*60}\n")

    all_data = []
    for analysis_file in sorted(WIKI_ROOT.glob("*/NEXUS_ANALYSIS.md")):
        item = parse_analysis(analysis_file)
        if item:
            all_data.append(item)

    print(f"[*] Parsed {len(all_data)} dossiers.")

    template = TEMPLATE_FILE.read_text(encoding="utf-8")
    data_json = json.dumps(all_data, ensure_ascii=False)
    
    # Inject data (template already has the placeholder)
    final_html = template.replace("__REPO_DATA_PLACEHOLDER__", data_json)

    # Write final
    TEMPLATE_FILE.write_text(final_html, encoding="utf-8")
    print(f"[+] Dashboard updated manually.")

if __name__ == "__main__":
    build()
