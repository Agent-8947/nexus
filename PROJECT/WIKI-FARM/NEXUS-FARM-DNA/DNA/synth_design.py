import sys
from pathlib import Path
from DNA_23_Domain_Blocks import compose_agent

def main():
    agent_id = "NEXUS_DESIGN_AI_PRESENTER"
    domain_a = "web"
    domain_b = "ai"
    role = "presentation"
    
    print(f"[*] Synthesizing {agent_id} ({domain_a} + {domain_b}) as {role}...")
    
    code = compose_agent(
        child_id=agent_id,
        mission="dashboard_ui_design",
        parent_a="UI_RENDERER",
        parent_b="AI_DESIGNER",
        domain_a=domain_a,
        domain_b=domain_b,
        role=role,
        generation=3
    )
    
    out_file = Path("DNA_12_AST_RENDER") / f"{agent_id}_synthesized_agent.py"
    out_file.parent.mkdir(exist_ok=True, parents=True)
    out_file.write_text(code, encoding="utf-8")
    
    print(f"[+] Written to {out_file}")
    
    # Run tests
    import subprocess
    print("[*] Running Integration Test...")
    res = subprocess.run(["python", str(out_file), "--test"], capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print(f"[!] Errors:\n{res.stderr}")

if __name__ == "__main__":
    main()
