import json
import os
import sys
import requests
from pathlib import Path
from oracle import FarmOracle, LIBRARY_PATH

if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# CYBER-ORACLE v2.0 [THINKING MODE]
# Upgrade: Semantic Analysis & Intelligence Synthesis via Local Ollama

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:3b"

class CyberOracle(FarmOracle):
    def __init__(self, library_path=LIBRARY_PATH):
        super().__init__(library_path)

    def think(self, query, top_k=3):
        # 1. Fast Retrieval
        candidates = self.search(query, min_score=0)[:top_k]
        
        if not candidates:
            return "Оракул не нашел даже отдаленно похожих инструментов в текущей базе. Возможно, нужно профармить больше репозиториев.", []

        # 2. Intelligence Synthesis
        print(f"[CYBER-THINKING] Выбрано {len(candidates)} ключевых компонента.")
        print(f"[CYBER-THINKING] Генерация КАРТЫ СИНТЕЗА...")
        
        # Prepare data for LLM
        context = ""
        for i, c in enumerate(candidates, 1):
            context += f"ID: {i} | Name: {c['name']} | Summary: {c['summary']} | Use: {c['nexus_use']}\n"

        prompt = f"""
Ты — ГЛАВНЫЙ АРХИТЕКТОР NEXUS. Твоя цель: создать ПОДРОБНУЮ КАРТУ СИНТЕЗА для последующей реализации в GPT-4/Claude. 

ЗАПРОС: "{query}"

ДОСТУПНЫЕ КОМПОНЕНТЫ:
{context}

ФОРМАТ КАРТЫ СИНТЕЗА (Markdown):
1. # 🗺 NEXUS SYNTHESIS MAP: [Название Проекта]
2. ## 🧱 CORE COMPONENTS (Критически важные репозитории)
3. ## ⚙️ DATA FLOW & LOGIC (Как данные текут между модулями)
4. ## 🚀 DEPLOYMENT STRATEGY (Docker/CLI/Environment)
5. ## 🧠 PROMPT FOR COMPLEX MODEL (Инструкция для GPT-4/Claude по сборке этого проекта)

Отвечай СТРОГО на русском языке. Исключи "воду", только структура и логика.
"""
        payload = {
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }

        try:
            resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
            if resp.status_code == 200:
                thought = resp.json().get("response", "Ошибка генерации.")
                # Save to file
                output_file = Path(__file__).resolve().parent / "synthesis_map.md"
                output_file.write_text(thought, encoding="utf-8")
                print(f"[CYBER-SUCCESS] Карта синтеза сохранена в: {output_file}")
                return thought, candidates
            else:
                return f"Ошибка Ollama: {resp.status_code}", candidates
        except Exception as e:
            return f"Кибер-мозг недоступен (Ollama error): {e}", candidates

    def get_next_synthesis_folder(self):
        base_dir = Path(__file__).resolve().parent
        i = 1
        while True:
            folder_name = f"SYNTHESIS_{i:03d}"
            folder_path = base_dir / folder_name
            if not folder_path.exists():
                folder_path.mkdir(parents=True, exist_ok=True)
                return folder_path
            i += 1

    def full_vault_dna(self, chunk_size=30):
        print(f"\n[DNA-ORACLE] ЗАПУСК ГЛОБАЛЬНОГО СКАНИРОВАНИЯ (Всего {len(self.library)} репозиториев)...")
        
        # 1. Fragmenting DNA
        fragments = []
        for i in range(0, len(self.library), chunk_size):
            chunk = self.library[i:i + chunk_size]
            print(f"[DNA-STEP] Анализ блока {i // chunk_size + 1}...")
            
            context = ""
            for repo in chunk:
                context += f"- {repo['name']}: {repo['summary']}\n"

            prompt = f"Извлеки архитектурную суть (ДНК) из этого списка репозиториев для системы NEXUS. Будь краток, выдели ключевые технологии и идеи: \n{context}"
            
            payload = {"model": MODEL, "prompt": prompt, "stream": False}
            try:
                resp = requests.post(OLLAMA_URL, json=payload, timeout=90)
                if resp.status_code == 200:
                    fragments.append(resp.json().get("response", ""))
            except:
                print(f"[!] Ошибка блока {i // chunk_size + 1}")

        # 2. Grand Fusion
        print("[DNA-FANSION] Слияние всех фрагментов в NEXUS MASTER MAP...")
        all_fragments = "\n---\n".join(fragments)
        
        final_prompt = f"""
Ты — ВЕРХОВНЫЙ АРХИТЕКТОР NEXUS. Объедини эти фрагменты в единую ГЛОБАЛЬНУЮ КАРТУ ДНК всей базы знаний.
ФРАГМЕНТЫ БАЗЫ:
{all_fragments}

ФОРМАТ ОТВЕТА (Markdown):
# 🧬 NEXUS MASTER DNA MAP
## 🧩 ГЛОБАЛЬНЫЕ ТЕХНОЛОГИЧЕСКИЕ ВЕКТОРЫ
## ⚙️ СИСТЕМНАЯ АРХИТЕКТУРА (Как всё со всем связано)
## 🚀 ПОТЕНЦИАЛ NEXUS (Что эта база позволяет собрать)
## 🧠 ИНСТРУКЦИЯ ДЛЯ СУПЕР-МОДЕЛИ (Handoff)
"""
        payload = {"model": MODEL, "prompt": final_prompt, "stream": False}
        resp = requests.post(OLLAMA_URL, json=payload, timeout=180)
        return resp.json().get("response", "Ошибка слияния.") if resp.status_code == 200 else "Ошибка слияния."

    def run_interface(self, query):
        print("\n" + "═" * 70)
        print("   CYBER-ORACLE v3.0 — NEXUS DNA ARCHIVIST")
        print("   Status: FULL VAULT ANALYTICS ENABLED")
        print("═" * 70)

        if query.lower() in ["dna", "днк", "full", "все"]:
            thought = self.full_vault_dna()
        else:
            thought, raw_results = self.think(query)
        
        # Final Save in sequential folder
        folder = self.get_next_synthesis_folder()
        save_path = folder / "synthesis.md"
        save_path.write_text(thought, encoding="utf-8")
        
        print(f"\n[ORACLE] Результаты сохранены в: {save_path}")
        print("\n" + thought)

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "dna"
    oracle = CyberOracle()
    oracle.run_interface(query)
