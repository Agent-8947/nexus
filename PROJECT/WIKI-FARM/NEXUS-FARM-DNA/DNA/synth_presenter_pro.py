import sys
from pathlib import Path
from DNA_23_Domain_Blocks import compose_agent

def main():
    agent_id = "NEXUS_AI_PRESENTER_PRO"
    domain_a = "ai"
    domain_b = "web"
    role = "presentation"
    
    print(f"[*] Synthesizing {agent_id} ({domain_a} + {domain_b}) as {role}...")
    
    # Синтезируем премиального ИИ-презентатора
    # Он объединяет возможности анализа (AI) и визуальной верстки (Web)
    code = compose_agent(
        child_id=agent_id,
        mission="technical_ai_presentation",
        parent_a="GENOMIC_ANALYST",
        parent_b="VESSEL_RENDERER",
        domain_a=domain_a,
        domain_b=domain_b,
        role=role,
        generation=4
    )
    
    out_file = Path("DNA_12_AST_RENDER") / f"{agent_id}_synthesized_agent.py"
    out_file.parent.mkdir(exist_ok=True, parents=True)
    out_file.write_text(code, encoding="utf-8")
    
    print(f"[+] Written to {out_file}")
    
    # Тестируем синтез
    import subprocess
    print("[*] Running Integration Test...")
    res = subprocess.run(["python", str(out_file), "--test"], capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print(f"[!] Log:\n{res.stderr}")

if __name__ == "__main__":
    main()
