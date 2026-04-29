import os
import time
import uuid
import importlib.util
from datetime import datetime

# ==============================================================================
# NEXUS AUTO-FARM (COMPOUNDING LOOP)
# GOVERNED BY: NEXUS CONSTITUTION 
# [LAW-62: POWER MANAGEMENT]
# [LAW-12: TELEMETRY]
# ==============================================================================

def load_agent(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def run_farm():
    print("=======================================================")
    print("🧠 NEXUS NEURAL FARM INITIATED")
    print("=======================================================\n")
    
    # Твои темы для самообразования
    topics = ["Drones", "Zero-day", "DevOps"]
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    compounder_mod = load_agent("agent_19", os.path.join(base_dir, "19_WIKI_COMPOUNDER.py"))
    compounder = compounder_mod.NexusCompounder()
    
    for idx, topic in enumerate(topics):
        trace_id = f"FARM-{str(uuid.uuid4())[:8]}"
        print(f"\n[+] CYCLE {idx+1}/{len(topics)}: Extracting intelligence on '{topic}' ...")
        print(f"    Trace ID: {trace_id}")
        
        # В реальной жизни здесь Researcher/Searcher идет в интернет (SerpAPI, ArXiv)
        # Сейчас мы делаем Mock-запрос, чтобы показать работу Компаундера
        time.sleep(2) # Имитация работы агента-добытчика
        
        mock_raw_output = f"""
        Domain: GENERAL
        Topic: {topic}
        Fact 1: {topic} represents a significant evolution in technology as of 2026.
        Fact 2: Automated orchestration inside {topic} allows scale without human intervention.
        """
        
        print("    [!] Handoff to WIKI_COMPOUNDER [LAW-15]")
        # Скапливаем знания в WIKI
        compounder.run(
            source_agent="22_AUTO_FARM",
            output_text=mock_raw_output
        )
        
        # [LAW-62: POWER MANAGEMENT] Спим между запросами, чтобы не спамить API
        print("    [zZz] Cooling down for 3 seconds...")
        time.sleep(3)

    print("\n=======================================================")
    print("[✓] FARM CYCLE COMPLETE. Knowledge base expanded.")
    print("=======================================================")

if __name__ == "__main__":
    run_farm()
