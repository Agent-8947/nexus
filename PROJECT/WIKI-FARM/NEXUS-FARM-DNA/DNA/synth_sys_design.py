import sys
import subprocess
from pathlib import Path
from DNA_23_Domain_Blocks import compose_agent

def main():
    agent_id = "NEXUS_SYSTEM_ARCHITECT"
    domain_a = "infra"
    domain_b = "ai"
    role = "presentation"
    
    print(f"[*] Synthesizing {agent_id} ({domain_a} + {domain_b}) as {role}...")
    
    # Скрещиваем инфраструктурного сканера и ИИ-анализатора 
    # для получения агента проектирования и визуализации архитектуры
    code = compose_agent(
        child_id=agent_id,
        mission="system_architecture_design",
        parent_a="INFRA_DISCOVERY_BOT",
        parent_b="AI_SYSTEMS_THINKER",
        domain_a=domain_a,
        domain_b=domain_b,
        role=role,
        generation=4
    )
    
    out_file = Path("DNA_12_AST_RENDER") / f"{agent_id}_synthesized_agent.py"
    out_file.write_text(code, encoding="utf-8")
    print(f"[+] Written to {out_file}")
    
    print(f"[*] Patching agent to fix structural drops...")
    subprocess.run([
        "python", "../DNA_REFACTOR/nexus_patcher.py", 
        "--file", str(out_file), 
        "--patch"
    ], capture_output=False, text=True)

    print(f"[*] Testing {agent_id}...")
    res = subprocess.run(["python", str(out_file), "--test"], capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
         print(f"[!] Warning/Errors: {res.stderr}")

if __name__ == "__main__":
    main()
