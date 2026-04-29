import os
import json
import time
import requests
from pathlib import Path

WIKI_DIR = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI")
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:3b"

SYSTEM_PROMPT = """You are Antigravity, the NEXUS Metamorphic Agent.
Your task is to analyze a technology repository's README and extract 2 key 'genes' (core capabilities).
You MUST output raw JSON in the exact format below, nothing else:
{
  "domain": "AI / Framework",
  "nexus_value_score": "10/10",
  "nexus_value_reason": "Short reason",
  "genes": [
    {
      "name": "GENE_EXAMPLE_DNA",
      "category": "AI / Concept",
      "logic": "Detailed explanation of what this gene does",
      "application": "How this will be used in the NEXUS system"
    },
    {
      "name": "GENE_ANOTHER_DNA",
      "category": "Concept",
      "logic": "Detailed explanation",
      "application": "How this will be used"
    }
  ]
}"""

def analyze_repo(repo_name, readme_content):
    prompt_text = f"Analyze this repository:\nName: {repo_name}\nREADME Context:\n{readme_content}\n\nTask: Output the JSON gene analysis."
    
    payload = {
        "model": MODEL_NAME,
        "system": SYSTEM_PROMPT,
        "prompt": prompt_text,
        "stream": False,
        "format": "json"
    }
    try:
        response = requests.post(OLLAMA_API, json=payload, timeout=120) # Increased timeout
        data = response.json()
        return json.loads(data['response'])
    except Exception as e:
        print(f"Error calling Qwen API for {repo_name}: {e}")
        return None

def process_repos():
    print(f"[*] Starting Autonomous Qwen-2.5-Coder Farming (NEXUS_ANALYSIS ONLY)...")
    repos = [d for d in WIKI_DIR.iterdir() if d.is_dir()]
    print(f"[*] Total repositories found: {len(repos)}")

    count = 0
    start_time = time.time()
    
    for repo in repos:
        analysis_path = repo / "NEXUS_ANALYSIS.md"
        # Check if we need to process this repo
        if analysis_path.exists():
            try:
                content = analysis_path.read_text(encoding='utf-8', errors='ignore')
                if "Auto-Extracted" not in content:
                    continue # Already manually done or done by AI
            except Exception:
                pass
                
        # Readme text to analyze
        readme_path = repo / "README.md"
        if not readme_path.exists():
            continue
        
        try:
            readme_text = readme_path.read_text(encoding='utf-8', errors='ignore')[:3000] # First 3000 chars
        except Exception:
            continue
            
        print(f"[{count+1}] Qwen is analyzing: {repo.name}...")
        result_json = analyze_repo(repo.name, readme_text)
        
        if result_json:
            try:
                # Create NEXUS_ANALYSIS.md
                md_content = f"# NEXUS Deep Gene Analysis: {repo.name}\n\n"
                md_content += f"> **Refined by Qwen-2.5-Coder (Autonomous Agent) — {time.strftime('%Y-%m-%d')}**\n"
                md_content += f"> Focus: {result_json.get('nexus_value_reason', 'N/A')}\n\n"
                md_content += f"## 🧬 Genetic Registry\n\n"
                
                genes = result_json.get('genes', [])
                for i, gene in enumerate(genes, start=1):
                    md_content += f"### {i}. `{gene.get('name', 'GENE')}` [{gene.get('category', 'General')}]\n"
                    md_content += f"- **Source**: `{repo.name}`\n"
                    md_content += f"- **Logic**: {gene.get('logic', '')}\n"
                    md_content += f"- **Application**: {gene.get('application', '')}\n\n"
                    
                md_content += "## 📊 Technical Benchmarks\n"
                md_content += f"- **Domain**: `{result_json.get('domain', 'Technology')}`\n"
                md_content += f"- **NEXUS Value**: ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ {result_json.get('nexus_value_score', '10/10')} ({result_json.get('nexus_value_reason', '')})\n"
                md_content += "- **Status**: `GENE_METADATA_LOCKED`\n"

                analysis_path.write_text(md_content, encoding='utf-8')
                print(f"  [+] Saved High-Fidelity analysis for {repo.name}.")
                count += 1
            except Exception as e:
                print(f"  [!] Error writing file: {e}")
        
    elapsed = time.time() - start_time
    print(f"[*] Autonomous Farming Complete. Improved {count} repositories in {elapsed:.2f} seconds.")

if __name__ == '__main__':
    process_repos()
