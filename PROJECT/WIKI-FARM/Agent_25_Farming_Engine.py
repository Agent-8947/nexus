import os
import json
import re
import requests
from pathlib import Path
from datetime import datetime
import time

# NEXUS AGENT 25 — THE HYPER-HARVESTER
# ====================================
# Цель: Автоматический фарминг оставшихся 1300+ репозиториев.
# Метод: Анализ локальных файлов -> Ollama (qwen2.5-coder:3b) -> Obsidian Vault.

DNA_DIR    = Path(__file__).resolve().parent / "NEXUS-FARM-DNA" / "DNA"
VAULT_PATH = Path(__file__).resolve().parent / "NEXUS-DOSSIERS"
REPOS_BASE = Path(__file__).resolve().parent.parent / "WIKI"
STATE_FILE = Path(__file__).resolve().parent / "agent_25_state.json"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL      = "qwen2.5-coder:3b"

class HyperHarvester:
    def __init__(self):
        self.state = self._load_state()
        self.existing_vault = set(f.stem.upper() for f in VAULT_PATH.glob("*.md"))

    def _load_state(self):
        if STATE_FILE.exists():
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        return {"processed": [], "failed": []}

    def _save_state(self):
        STATE_FILE.write_text(json.dumps(self.state, indent=2, ensure_ascii=False), encoding="utf-8")

    def _call_ollama(self, prompt, num_ctx=8000):
        payload = {
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"num_ctx": num_ctx, "temperature": 0.3}
        }
        try:
            resp = requests.post(OLLAMA_URL, json=payload, timeout=300)
            if resp.status_code == 200:
                return resp.json().get("response", "")
        except Exception as e:
            print(f"  [!] Ollama Error: {e}")
        return None

    def get_repo_context(self, repo_path: Path):
        context = ""
        # 1. Try NEXUS_ANALYSIS.md
        analysis_f = repo_path / "NEXUS_ANALYSIS.md"
        if analysis_f.exists():
            context += f"CORE ANALYSIS:\n{analysis_f.read_text(encoding='utf-8', errors='ignore')[:3000]}\n"
        
        # 2. Try README.md
        readme_f = None
        for r in ["README.md", "README", "readme.md"]:
             if (repo_path / r).exists():
                 readme_f = repo_path / r
                 break
        
        if readme_f:
            context += f"README CONTENT:\n{readme_f.read_text(encoding='utf-8', errors='ignore')[:5000]}\n"
        
        return context

    def synthesize_dossier(self, repo_name, context):
        prompt = f"""Ты -- AI-АРХИТЕКТОР NEXUS [Hardened Edition].
ЗАДАЧА: Создать глубокую техническую карточку (Technical Dossier) для репозитория '{repo_name}'.
ФОРМАТ: Строгий технический Markdown с YAML фронтматером.
ЯЗЫК: Русский (кроме терминов и имен).

КОНТЕКСТ РЕПОЗИТОРИЯ:
{context}

ТРЕБОВАНИЯ К ВЫХОДУ:
1. YAML: tags (min 5), category, language, github url.
2. ## Описание (Техническая суть, а не маркетинг).
3. ## Основные Разделы (Анализ структуры проекта).
4. ## Почему это Killer-App (Уникальность).
5. ## Архитектурная Ценность для NEXUS (Как это усилит наш интеллект-движок).
6. ## Топ-3 примера (Команды или куски кода).
7. ## Связанные Репозитории (Упомяни 3-5 похожих или комплементарных проектов из NEXUS).

ВЫХОД ДОЛЖЕН БЫТЬ ТОЛЬКО MARKDOWN:
"""
        return self._call_ollama(prompt)

    def process_batch(self, limit=5):
        print(f"[*] Scanning {REPOS_BASE}...", flush=True)
        repos = [d for d in REPOS_BASE.iterdir() if d.is_dir() and ".git" not in d.name]
        print(f"[*] Found {len(repos)} repositories.", flush=True)
        
        count = 0
        for r_path in repos:
            if count >= limit: break
            
            repo_name = r_path.name
            if repo_name.upper() in self.existing_vault or repo_name in self.state["processed"]:
                # print(f"  [.] Skipping {repo_name} (already in vault/state)", flush=True)
                continue
            
            print(f"[*] Farming {repo_name}...", flush=True)
            context = self.get_repo_context(r_path)
            if not context:
                print(f"  [!] No context found for {repo_name}. Skipping.", flush=True)
                continue
            
            print(f"  [~] Calling Ollama for {repo_name}...", flush=True)
            dossier = self.synthesize_dossier(repo_name, context)
            if dossier:
                print(f"  [+] Synthesis successful.", flush=True)
                # Clean up dossier if LLM included triple backticks
                if dossier.startswith("```markdown"):
                    dossier = dossier.replace("```markdown", "", 1).rsplit("```", 1)[0]
                elif dossier.startswith("```"):
                    dossier = dossier.replace("```", "", 1).rsplit("```", 1)[0]
                
                out_file = VAULT_PATH / f"{repo_name.upper()}.md"
                out_file.write_text(dossier, encoding="utf-8")
                
                self.state["processed"].append(repo_name)
                self.existing_vault.add(repo_name.upper())
                print(f"  [V] Dossier created: {out_file.name}", flush=True)
                count += 1
                self._save_state()
            else:
                print(f"  [X] Failed to synthesize dossier for {repo_name}", flush=True)
                if repo_name not in self.state["failed"]:
                    self.state["failed"].append(repo_name)
                    self._save_state()

if __name__ == "__main__":
    harvester = HyperHarvester()
    harvester.process_batch(limit=1000)
