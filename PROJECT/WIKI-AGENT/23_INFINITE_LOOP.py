import os
import time
import uuid
import random
import importlib.util

# ==============================================================================
# NEXUS INFINITE COMPOUNDING LOOP [ENDLESS REGIME]
# ==============================================================================
# Эта программа работает в бесконечном цикле, случайно выбирая репозиторий 
# из библиотеки, извлекая факты и скармливая их компаундеру.
# Идеально для работы на VPS или локальном сервере в Screen/Tmux.
# ==============================================================================

def load_agent(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def get_random_topic(wiki_path: str) -> str:
    # Динамически вытаскиваем название репозитория из нашей библиотеки (1440+ папок)
    try:
        repos = [d for d in os.listdir(wiki_path) if os.path.isdir(os.path.join(wiki_path, d))]
        if repos:
            return random.choice(repos)
    except Exception:
        pass
    
    # Fallback темы
    fallback = ["Quantum Computing", "Advanced DevOps", "Aero-Dynamics", "Zero-Trust Security"]
    return random.choice(fallback)

def run_infinite_loop():
    print("=======================================================")
    print("     🚀 INFINITE COMPOUNDING LOOP INITIATED 🚀         ")
    print("     Press CTRL+C to trigger Emergency Kill-Switch     ")
    print("=======================================================\n")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    wiki_base_path = os.path.abspath(os.path.join(base_dir, "..", "WIKI"))
    kill_switch_path = os.path.join(base_dir, "..", "STOP.txt")
    
    # Загрузка нейромозга
    compounder_mod = load_agent("agent_19", os.path.join(base_dir, "19_WIKI_COMPOUNDER.py"))
    compounder = compounder_mod.NexusCompounder()
    
    cycle = 1
    
    try:
        while True:
            # [LAW-69: EMERGENCY KILL SWITCH] Проверка перед каждым циклом
            if os.path.exists(kill_switch_path):
                print("\n[!] LAW-69 TRIGGERED: STOP.txt detected. Emergency shutdown initiated.")
                break
                
            topic = get_random_topic(wiki_base_path)
            topic_path = os.path.join(wiki_base_path, topic)
            trace_id = f"INF-{str(uuid.uuid4())[:8]}"
            
            print(f"\n[+] CYCLE {cycle} | Topic: '{topic}' | Trace: {trace_id}")
            
            # [INTELLIGENCE EXTRACTION] Read actual repository data
            intel_text = ""
            try:
                # Priority 1: README.md
                for readme_name in ["README.md", "readme.md", "README.txt"]:
                    rp = os.path.join(topic_path, readme_name)
                    if os.path.exists(rp):
                        with open(rp, "r", encoding="utf-8", errors="ignore") as f:
                            intel_text = f.read(2000) # Read up to 2k chars to fit Groq 6k TPM limit
                        break
                
                # Priority 2: List files if no readme
                if not intel_text:
                    files = os.listdir(topic_path)[:20]
                    intel_text = f"Repository {topic} contains files: " + ", ".join(files)
            except Exception as e:
                intel_text = f"Could not read repo {topic}: {e}"

            print(f"    [*] Data Extracted: {len(intel_text)} characters.")
            print("    [!] Handoff to WIKI_COMPOUNDER [LAW-15]")
            
            # Отправка реальных фактов в компаундер
            compounder.run(
                source_agent="23_INFINITE_LOOP",
                output_text=intel_text if intel_text else f"Topic: {topic} (Empty repo)"
            )
            
            print("    [zZz] Fast cycle cooldown (1s)... [LOCAL_MODE]")
            time.sleep(1)
            
            cycle += 1
            
    except KeyboardInterrupt:
        print("\n[!] Manual Override Detected (CTRL+C). Graceful Shutdown.")
    
    print("\n[✓] INFINITE LOOP TERMINATED.")

if __name__ == "__main__":
    run_infinite_loop()
