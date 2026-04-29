import json
import requests
import time
import sys
from pathlib import Path
from datetime import datetime

# MASTER DNA FARM v1.1 [PORTABLE + RELIABLE STATE]
# FIX [C-01]: All paths relative to __file__
# FIX [C-03]: STATE_FILE bound to DNA_DIR, not CWD
# FIX [H-03]: last_chunk always saved (success or fail) + retry_queue

DNA_DIR      = Path(__file__).resolve().parent
FARM_ROOT    = DNA_DIR.parent.parent
LIBRARY_PATH = FARM_ROOT / "farm_library.json"
STATE_FILE   = DNA_DIR / "DNA_06_Active_State.json"    # FIX [C-03]
OUTPUT_MD    = DNA_DIR / "MASTER_DNA.md"
OLLAMA_URL   = "http://localhost:11434/api/generate"
MODEL        = "qwen2.5-coder:3b"


class MasterDNAFarm:
    def __init__(self, chunk_size: int = 25, delay_seconds: int = 20):
        self.library     = self._load_library()
        self.state       = self._load_state()
        self.chunk_size  = chunk_size
        self.delay       = delay_seconds

    def _load_library(self) -> list:
        if not LIBRARY_PATH.exists():
            print(f"[!] Error: Knowledge source not found at {LIBRARY_PATH}")
            return []
        return json.loads(LIBRARY_PATH.read_text(encoding="utf-8"))

    def _load_state(self) -> dict:
        if STATE_FILE.exists():
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        return {"last_chunk": 0, "fragments": [], "retry_queue": [], "started_at": datetime.now().isoformat()}

    def _save_state(self):
        self.state["updated_at"] = datetime.now().isoformat()
        STATE_FILE.write_text(
            json.dumps(self.state, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    def _call_ollama(self, prompt: str, timeout: int = 180) -> str | None:
        """Single Ollama call with error handling. Returns text or None."""
        payload = {"model": MODEL, "prompt": prompt, "stream": False}
        try:
            resp = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
            if resp.status_code == 200:
                return resp.json().get("response", "")
            else:
                print(f"[!] Ollama error (HTTP {resp.status_code})")
                return None
        except requests.exceptions.ConnectionError:
            print(f"[!] Ollama not running at {OLLAMA_URL}")
            return None
        except Exception as e:
            print(f"[!] Connection error: {e}")
            return None

    def run_synthesis(self):
        total_repos = len(self.library)
        if total_repos == 0:
            print("[!] Empty library. Nothing to process.")
            return

        start_idx = self.state["last_chunk"] * self.chunk_size

        print(f"\n[MASTER-DNA] Farm started (total repos: {total_repos})")
        print(f"[LOW-LOAD] Resuming from chunk {self.state['last_chunk']} | Delay: {self.delay}s")

        for i in range(start_idx, total_repos, self.chunk_size):
            chunk = self.library[i : i + self.chunk_size]
            current_block = i // self.chunk_size + 1

            print(f"\n[BLOCK {current_block}] Analyzing {len(chunk)} repos...")

            context = "\n".join(f"- {repo.get('name', '?')}: {repo.get('summary', '')}" for repo in chunk)
            prompt  = f"Извлеки архитектурную ДНК (ключевые идеи, технологии, фишки) из этого списка:\n{context}"

            result = self._call_ollama(prompt)

            # FIX [H-03]: Save state regardless of success/failure
            if result:
                self.state["fragments"].append(result)
                print(f"[[V]] Block {current_block} farmed.")
            else:
                print(f"[[X]] Block {current_block} failed -- adding to retry_queue.")
                if "retry_queue" not in self.state:
                    self.state["retry_queue"] = []
                self.state["retry_queue"].append(current_block)

            # Always advance chunk pointer (prevents infinite re-process on error)
            self.state["last_chunk"] = current_block
            self._save_state()

            if i + self.chunk_size < total_repos:
                print(f"[WAIT] Sleeping {self.delay}s (Low-Load Mode)...")
                time.sleep(self.delay)

        self.finalize()

    def retry_failed(self):
        """Re-process chunks that previously failed."""
        queue = self.state.get("retry_queue", [])
        if not queue:
            print("[*] No failed chunks to retry.")
            return

        print(f"[RETRY] Processing {len(queue)} failed chunks...")
        for block_idx in list(queue):
            i = (block_idx - 1) * self.chunk_size
            chunk = self.library[i : i + self.chunk_size]
            context = "\n".join(f"- {r.get('name', '?')}: {r.get('summary', '')}" for r in chunk)
            prompt  = f"Извлеки архитектурную ДНК из этого списка:\n{context}"
            result  = self._call_ollama(prompt)
            if result:
                self.state["fragments"].append(result)
                self.state["retry_queue"].remove(block_idx)
                self._save_state()
                print(f"[[V]] Block {block_idx} recovered.")
            else:
                print(f"[[X]] Block {block_idx} still failing.")

    def finalize(self):
        print("\n[MASTER-DNA] Final synthesis of all fragments...")
        all_dna = "\n---\n".join(self.state["fragments"])

        final_prompt = f"""Ты -- ТЕХНИЧЕСКИЙ ДИРЕКТОР (CTO) NEXUS [Hardened Edition].
ЗАДАЧА: Анализ RAW-данных всей фермы репозиториев.
ИГНОРИРУЙ: Маркетинг, общие фразы.
ФОКУС: Хардкорные технологии, архитектурная связность, инженерные паттерны.

ДНК-ФРАГМЕНТЫ:
{all_dna}

СОЗДАЙ ТЕХНИЧЕСКИЙ МАНИФЕСТ ДНК:
1. 🛠 ТЕХНОЛОГИЧЕСКИЙ СТЕК (Доминирующие языки, критические либы).
2. ⚙️ ПАТТЕРНЫ & ПРОТОКОЛЫ (Распределенные системы, AI-инференс).
3. 🕵️ СЕКТОР БЕЗОПАСНОСТИ & OSINT.
4. 🧠 АЛХИМИЯ АГЕНТОВ (Как скрестить в Автономный Оркестратор NEXUS).
5. ⚡ РЕПОЗИТОРИИ-ФЛАГМАНЫ (Топ-5 самых ценных находок).
"""
        payload = {
            "model": MODEL,
            "prompt": final_prompt,
            "stream": False,
            "options": {"num_ctx": 24000, "temperature": 0.2}
        }
        try:
            print("[NEXUS-SYNTHESIS] Final synthesis running...")
            resp = requests.post(OLLAMA_URL, json=payload, timeout=900)
            if resp.status_code == 200:
                final_dna = resp.json().get("response", "")
                OUTPUT_MD.write_text(final_dna, encoding="utf-8")
                print(f"\n[SUCCESS] MASTER DNA FORMED: {OUTPUT_MD}")
            else:
                print("[!] Finalization error.")
        except Exception as e:
            print(f"[!] Error: {e}")


if __name__ == "__main__":
    farm = MasterDNAFarm(chunk_size=20, delay_seconds=20)
    farm.run_synthesis()
