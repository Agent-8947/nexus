import os
import uuid
import importlib.util

# ==============================================================================
# NEXUS WORKFLOW: OSINT -> WIKI PIPELINE
# GOVERNED BY: NEXUS CONSTITUTION (LAW-08: ORCHESTRATION, LAW-15: SECURE HANDOFF)
# ==============================================================================

def load_agent(name: str, path: str):
    """Dynamically loads agent modules that start with numbers (e.g. 06_WIKI...)"""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def run_osint_pipeline(target_domain: str):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    trace_id = f"JOB-{str(uuid.uuid4())[:8]}"
    
    print(f"\n=======================================================")
    print(f"[*] NEXUS PIPELINE INITIATED")
    print(f"[*] TARGET  : {target_domain}")
    print(f"[*] TRACE_ID: {trace_id}")
    print(f"=======================================================\n")

    # 1. Загрузка агентов в память
    # [LAW-11: COMPOSABLE ACTIONS] Переиспользование инструментов
    print(">>> STAGE 1: LOADING NEURAL NODES")
    osint_mod = load_agent("agent_06", os.path.join(base_dir, "06_WIKI_OSINT.py"))
    compounder_mod = load_agent("agent_19", os.path.join(base_dir, "19_WIKI_COMPOUNDER.py"))
    
    # 2. Фаза Разведки (Агент 06)
    print("\n>>> STAGE 2: OSINT RECONNAISSANCE")
    osint_agent = osint_mod.NexusOsintAgent()
    target_data = osint_mod.OsintTarget(
        target_domain=target_domain, 
        trace_id=trace_id, 
        stealth_mode=True
    )
    # Выполнение
    result_obj = osint_agent.run(target_data)
    
    # 3. Фаза Безопасной Передачи (Secure Handoff) [LAW-15]
    print("\n>>> STAGE 3: SECURE HANDOFF (JSON PAYLOAD)")
    # Агент 06 выдает строгий Pydantic JSON согласно контракту [LAW-03]
    raw_output_json = result_obj.model_dump_json(indent=2)
    
    # 4. Фаза Интеграции в Библиотеку (Агент 19)
    print("\n>>> STAGE 4: KNOWLEDGE COMPOUNDING")
    compounder_agent = compounder_mod.NexusCompounder()
    # Агент 19 переваривает JSON и делает WIKI-статью
    compounder_agent.run(
        source_agent="06_WIKI_OSINT", 
        output_text=raw_output_json
    )
    
    print(f"\n[+] ORCHESTRATION PIPELINE COMPLETE FOR '{target_domain}'.")

if __name__ == "__main__":
    # Test target for integration [LAW-14: REGRESSION]
    test_domain = "deepmind.google" # Цель
    run_osint_pipeline(test_domain)
