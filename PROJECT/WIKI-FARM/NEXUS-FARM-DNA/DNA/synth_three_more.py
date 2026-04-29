import sys
from pathlib import Path
import subprocess
from DNA_23_Domain_Blocks import compose_agent

AGENTS_TO_BUILD = [
    {
        "child_id": "NEXUS_MALWARE_SENTRY",
        "mission": "zero_day_threat_detection",
        "parent_a": "VIRUSTOTAL_CORE", "parent_b": "ANOMALIB_ENGINE",
        "domain_a": "security", "domain_b": "ai",
        "role": "collector", "generation": 5
    },
    {
        "child_id": "NEXUS_CODE_AUDITOR",
        "mission": "static_code_analysis",
        "parent_a": "GITLEAKS_SCANNER", "parent_b": "APPINFOSCANNER",
        "domain_a": "web", "domain_b": "infra",
        "role": "analyzer", "generation": 5
    },
    {
        "child_id": "NEXUS_THREAT_REPORTER",
        "mission": "executive_threat_briefing",
        "parent_a": "EXPLOIT_DB", "parent_b": "SQLMAP",
        "domain_a": "security", "domain_b": "data",
        "role": "presentation", "generation": 5
    }
]

out_dir = Path("DNA_12_AST_RENDER")
out_dir.mkdir(exist_ok=True)

for params in AGENTS_TO_BUILD:
    name = params["child_id"]
    print(f"[*] Synthesizing {name} ({params['domain_a']} + {params['domain_b']} | {params['role']} | Gen-{params['generation']})")
    
    code = compose_agent(**params)
    out_file = out_dir / f"{name}_synthesized_agent.py"
    out_file.write_text(code, encoding="utf-8")
    
    print(f"[+] Written to {out_file}")
    res = subprocess.run(["python", str(out_file), "--test"], capture_output=True, text=True)
    if "[TEST]" in res.stdout or "[TEST]" in res.stderr:
        print("[OK] Integration Test Passed.")
    else:
        print(f"[!] Test Failed / Output:\n{res.stdout}\n{res.stderr}")
    print("-" * 60)
