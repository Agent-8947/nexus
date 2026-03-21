import json
import sys
import os
from datetime import datetime

REGISTRY_PATH = r"e:\Downloads\--ANTIGRAVITY store\IDE-optimus\PROJECT\fault_registry.json"

def record_error(fault_type, description, root_cause, solution, prevention_rule):
    if not os.path.exists(REGISTRY_PATH):
        registry = []
    else:
        with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
            registry = json.load(f)

    new_id = f"ERR-{len(registry):03d}"
    new_entry = {
        "id": new_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "fault_type": fault_type,
        "description": description,
        "root_cause": root_cause,
        "solution": solution,
        "prevention_rule": prevention_rule
    }

    registry.append(new_entry)

    with open(REGISTRY_PATH, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    
    print(f"[+] Error recorded in registry with ID: {new_id}")
    print(f"[!] New Prevention Rule added: {prevention_rule}")

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python record_error.py <type> <desc> <cause> <sol> <rule>")
        sys.exit(1)
    
    record_error(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
