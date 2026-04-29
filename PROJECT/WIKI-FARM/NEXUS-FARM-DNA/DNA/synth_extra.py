import sys
from pathlib import Path
from DNA_23_Domain_Blocks import compose_agent

def main():
    agent_id = "NEXUS_DATA_VIZ_ENGINE"
    domain_a = "data"
    domain_b = "web"
    role = "presentation"
    
    print(f"[*] Synthesizing {agent_id} ({domain_a} + {domain_b}) as {role}...")
    
    code = compose_agent(
        child_id=agent_id,
        mission="data_visualization",
        parent_a="DATA_CRUNCHER",
        parent_b="WEB_RENDERER",
        domain_a=domain_a,
        domain_b=domain_b,
        role=role,
        generation=3
    )
    
    out_file = Path("DNA_12_AST_RENDER") / f"{agent_id}_synthesized_agent.py"
    out_file.parent.mkdir(exist_ok=True, parents=True)
    out_file.write_text(code, encoding="utf-8")
    print(f"[+] Written to {out_file}")
    
    agent_id2 = "NEXUS_HARDWARE_AUDITOR"
    domain_a2 = "hardware"
    domain_b2 = "security"
    role2 = "analyzer"
    
    print(f"[*] Synthesizing {agent_id2} ({domain_a2} + {domain_b2}) as {role2}...")
    code2 = compose_agent(
        child_id=agent_id2,
        mission="hardware_security_audit",
        parent_a="SOC_INSPECTOR",
        parent_b="VULN_SCANNER",
        domain_a=domain_a2,
        domain_b=domain_b2,
        role=role2,
        generation=3
    )
    
    out_file2 = Path("DNA_12_AST_RENDER") / f"{agent_id2}_synthesized_agent.py"
    out_file2.write_text(code2, encoding="utf-8")
    print(f"[+] Written to {out_file2}")

    # Tests
    import subprocess
    print(f"[*] Testing {agent_id}...")
    subprocess.run(["python", str(out_file), "--test"], capture_output=False, text=True)
    
    print(f"[*] Testing {agent_id2}...")
    subprocess.run(["python", str(out_file2), "--test"], capture_output=False, text=True)

if __name__ == "__main__":
    main()
