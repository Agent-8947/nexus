import json
import requests
from pathlib import Path

# NEXUS RELIABLE DNA SYNTHIZER [BATCH MODE]
# Split 20 fragments into 2 groups to avoid VRAM/Timeout limits.

STATE_FILE = Path("dna_state.json")
OUTPUT_MD = Path("MASTER_DNA_FINAL.md")
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:3b"

def get_analysis(fragments, batch_name):
    all_dna = "\n---\n".join(fragments)
    prompt = f"""
Ты -- ТЕХНИЧЕСКИЙ АРХИТЕКТОР NEXUS. Проанализируй эту часть технологической базы ({batch_name}).
Выдели ключевой СТЕК, ПАТТЕРНЫ и ИНСТРУМЕНТЫ БЕЗОПАСНОСТИ.
ДАННЫЕ:
{all_dna}
"""
    payload = {
        "model": MODEL, 
        "prompt": prompt, 
        "stream": False,
        "options": {"num_ctx": 12000, "temperature": 0.1}
    }
    print(f"[NEXUS] Анализ {batch_name}...")
    resp = requests.post(OLLAMA_URL, json=payload, timeout=500)
    return resp.json().get("response", "")

def run_reliable_synthesis():
    data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    fragments = data.get("fragments", [])
    
    # 1. Batch A (1-10)
    part_a = get_analysis(fragments[:10], "ЧАСТЬ_1 (Репозитории A-C)")
    
    # 2. Batch B (11-20)
    part_b = get_analysis(fragments[10:], "ЧАСТЬ_2 (Репозитории D-Z)")
    
    # 3. Final Fusion
    print("[NEXUS] Финальное слияние в МАНИФЕСТ...")
    fusion_prompt = f"""
Ты -- CTO NEXUS. Объедини два технических анализа в единый ТЕХНОЛОГИЧЕСКИЙ МАНИФЕСТ.
АНАЛИЗ 1: {part_a}
АНАЛИЗ 2: {part_b}

ФОРМАТ:
# 🧬 NEXUS ARCHITECTURAL DNA [HARDENED]
## 🛠 TECH STACK (Rust/Python/Go focus)
## ⚙️ INFRASTRUCTURE PATTERNS (Distributed/AI/K8s)
## 🕵️ SECURITY & OSINT VECTOR
## 🧠 AGENTIC ALCHEMY (How to build the Orchestrator)
"""
    payload = {
        "model": MODEL, 
        "prompt": fusion_prompt, 
        "stream": False,
        "options": {"num_ctx": 16000}
    }
    final_resp = requests.post(OLLAMA_URL, json=payload, timeout=500)
    OUTPUT_MD.write_text(final_resp.json().get("response", ""), encoding="utf-8")
    print(f"[SUCCESS] Документ создан: {OUTPUT_MD}")

if __name__ == "__main__":
    run_reliable_synthesis()
