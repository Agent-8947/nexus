import json
import requests
from pathlib import Path
from datetime import datetime

# NEXUS DNA RE-SYNTHESIZER v1.1 [PORTABLE]
# FIX [C-01]: All paths relative to __file__
# FIX [C-03]: STATE_FILE bound to DNA_DIR, not CWD

DNA_DIR    = Path(__file__).resolve().parent
STATE_FILE = DNA_DIR / "DNA_06_Active_State.json"      # FIX [C-03]: canonical
OUTPUT_MD  = DNA_DIR / "MASTER_DNA_V2.md"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL      = "qwen2.5-coder:3b"


def run_resynthesis():
    if not STATE_FILE.exists():
        print(f"[!] Error: State file not found at {STATE_FILE}")
        print(f"    Run DNA_02_Master_Harvester.py first to generate it.")
        return

    print("[NEXUS] Loading DNA fragments...")
    data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    fragments = data.get("fragments", [])

    if not fragments:
        print("[!] No fragments found in state. Run DNA_02 first.")
        return

    print(f"[NEXUS] {len(fragments)} fragments loaded. Starting deep synthesis...")

    all_dna = "\n---\n".join(fragments)

    final_prompt = f"""Ты -- ТЕХНИЧЕСКИЙ ДИРЕКТОР (CTO) NEXUS [Hardened Edition].
ЗАДАЧА: Анализ {len(fragments)} фрагментов RAW-данных всей фермы репозиториев.
ИГНОРИРУЙ: Маркетинг, общие фразы.
ФОКУС: Хардкорные технологии, архитектурная связность, инженерные паттерны.

ДНК-ФРАГМЕНТЫ:
{all_dna}

СОЗДАЙ ТЕХНИЧЕСКИЙ МАНИФЕСТ ДНК:
# 🧬 NEXUS ARCHITECTURAL DNA [ENGINEERING EDITION]

## 🛠 ТЕХНОЛОГИЧЕСКИЙ СТЕК
(Проанализируй доминирующие языки и критические либы. Rust/Go/Python/C++.)

## ⚙️ ПАТТЕРНЫ & ПРОТОКОЛЫ
(Распределенные системы: RAFT, Контейнеризация: K8s/Docker, AI-инференс: CUDA/TensorFlow.)

## 🕵️ СЕКТОР БЕЗОПАСНОСТИ & OSINT
(Методы эксплуатации, Shodan-запросы, анализ трафика, обход антивирусов.)

## 🧠 АЛХИМИЯ АГЕНТОВ
(Предложи план: как скрестить технологии в Автономный Оркестратор NEXUS.)

## ⚡ РЕПОЗИТОРИИ-ФЛАГМАНЫ
(Топ-5 самых ценных инструментов с кратким обоснованием.)
"""

    payload = {
        "model": MODEL,
        "prompt": final_prompt,
        "stream": True,
        "options": {"num_ctx": 28000, "temperature": 0.1}
    }

    print("[NEXUS-SYNTHESIS] Starting deep synthesis with streaming... (V2)")
    try:
        response_text = ""
        with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=1200) as r:
            for line in r.iter_lines():
                if line:
                    chunk = json.loads(line)
                    content = chunk.get("response", "")
                    response_text += content
                    if len(response_text) % 500 < len(content):
                        print(f"  Received {len(response_text)} chars...", end="\r")
                    if chunk.get("done"):
                        break

        if response_text:
            OUTPUT_MD.write_text(response_text, encoding="utf-8")
            print(f"\n[SUCCESS] DEEP DNA MAP CREATED: {OUTPUT_MD}")
        else:
            print("\n[!] Error: Empty response from model.")

    except requests.exceptions.ConnectionError:
        print(f"\n[!] Ollama not running at {OLLAMA_URL}")
    except Exception as e:
        print(f"\n[!] Final Synthesis Error: {e}")


if __name__ == "__main__":
    run_resynthesis()
