import sys
from pathlib import Path
import subprocess
from DNA_23_Domain_Blocks import compose_agent

AGENTS_TO_BUILD = [
    {
        "child_id": "NEXUS_CYBER_CRAWLER",
        "mission": "automated_surface_reconnaissance",
        "parent_a": "NMAP_SCANNER", "parent_b": "CRAWL4AI",
        "domain_a": "security", "domain_b": "web",
        "role": "collector", "generation": 4
    },
    {
        "child_id": "NEXUS_INFRA_OVERSEER",
        "mission": "system_metrics_and_auditing",
        "parent_a": "GRAFANA_CORE", "parent_b": "GITLEAKS_ENGINE",
        "domain_a": "infra", "domain_b": "data",
        "role": "orchestrator", "generation": 4
    },
    {
        "child_id": "NEXUS_FIRMWARE_AUDITOR",
        "mission": "iot_binary_inspection",
        "parent_a": "BINWALK_PRO", "parent_b": "EXPLOIT_DB",
        "domain_a": "hardware", "domain_b": "security",
        "role": "analyzer", "generation": 4
    }
]

out_dir = Path("DNA_12_AST_RENDER")
out_dir.mkdir(exist_ok=True)

for params in AGENTS_TO_BUILD:
    name = params["child_id"]
    print(f"[*] Synthesizing {name} ({params['domain_a']} + {params['domain_b']} | {params['role']})")
    
    code = compose_agent(**params)
    out_file = out_dir / f"{name}_synthesized_agent.py"
    out_file.write_text(code, encoding="utf-8")
    
    print(f"[+] Written to {out_file}")
    print(f"[*] Formatting & Testing {name}...")
    
    res = subprocess.run(["python", str(out_file), "--test"], capture_output=True, text=True)
    if "[TEST]" in res.stdout or "[TEST]" in res.stderr:
        print("[OK] Integration Test Passed.")
    else:
        print(f"[!] Test Failed / Output:\n{res.stdout}\n{res.stderr}")
    print("-" * 60)
