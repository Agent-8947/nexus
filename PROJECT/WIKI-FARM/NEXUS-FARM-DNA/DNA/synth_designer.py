import json
import sys
from pathlib import Path

# Добавляем путь к DNA для импорта Assembler
DNA_DIR = Path("e:/Downloads/--ANTIGRAVITY store/IDE-NEXUS/PROJECT/WIKI-FARM/NEXUS-FARM-DNA/DNA")
sys.path.insert(0, str(DNA_DIR))

from DNA_10_Code_Assembler import synthesize

def run_design_synthesis():
    core_path = DNA_DIR / "DNA_04_Synthesis_Core.json"
    dna_data = json.loads(core_path.read_text(encoding="utf-8"))
    nodes = {n["node_id"]: n for n in dna_data["NODES"]}
    
    parent_a = nodes["98.CSS"]
    parent_b = nodes["TAILWIND"]
    
    mission = "Develop a premium design system architect and UI component generator with 98.CSS nostalgic aesthetics and Tailwind utility efficiency."
    
    print(f"[*] Starting DESIGNER AGENT synthesis...")
    result = synthesize(
        parent_a=parent_a,
        parent_b=parent_b,
        mission=mission
    )
    
    if result.get("success"):
        print(f"[SUCCESS] Agent generated: {result['child_id']}")
        print(f"[PATH] {result['file_path']}")
    else:
        print(f"[ERROR] {result.get('error')}")

if __name__ == "__main__":
    run_design_synthesis()
