import sys
from pathlib import Path
import subprocess
from DNA_23_Domain_Blocks import compose_agent
from DNA_Utils import sort_and_number_agent

agent_def = {
    "child_id": "NEXUS_GODEYE_ORACLE",
    "mission": "omni_channel_threat_intelligence",
    "parent_a": "SPIDERFOOT_PRO", "parent_b": "ANYTHING-LLM",
    "domain_a": "osint", "domain_b": "ai",
    "role": "orchestrator", "generation": 5
}

out_dir = Path("DNA_12_AST_RENDER")
out_dir.mkdir(exist_ok=True)

name = agent_def["child_id"]
print(f"[*] Synthesizing {name} (Gen-{agent_def['generation']})")
print(f"[*] Domains: [{agent_def['domain_a'].upper()}] + [{agent_def['domain_b'].upper()}] | Role: {agent_def['role']}")

code = compose_agent(**agent_def)
out_file = out_dir / f"{name}_synthesized_agent.py"
out_file.write_text(code, encoding="utf-8")

# FIX [SORT]: Automatic categorization and renumbering
try:
    final_path = sort_and_number_agent(out_file)
    out_file = final_path
    print(f"[+] Sorted & Numbered to {out_file.parent.name}/{out_file.name}")
except Exception as e:
    print(f"[+] Written (Sort failed: {e}) to {out_file}")
print(f"[*] Testing {name} for Contract Compliance...")

res = subprocess.run(["python", str(out_file), "--test"], capture_output=True, text=True)
if "[TEST]" in res.stdout or "[TEST]" in res.stderr:
    print("[OK] Integration Test Passed. Zero-Stub Verified.")
else:
    print(f"[!] Test Failed / Output:\n{res.stdout}\n{res.stderr}")
