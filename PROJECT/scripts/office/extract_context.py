import json
import os
from pathlib import Path

def extract():
    project_root = Path("e:/Downloads/--ANTIGRAVITY store/IDE-optimus")
    memory_path = project_root / "PROJECT" / "memory.json"
    start_md_path = project_root / "START.md"
    
    context = {
        "memory": {},
        "current_goal": "",
        "scripts": []
    }
    
    if memory_path.exists():
        with open(memory_path, 'r', encoding='utf-8') as f:
            context["memory"] = json.load(f)
            
    if start_md_path.exists():
        with open(start_md_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Extract objective or /start instructions
            context["current_goal"] = "".join(lines)

    # Scan for active scripts
    scripts_dir = project_root / "PROJECT" / "scripts"
    if scripts_dir.exists():
        for script in scripts_dir.rglob("*.py"):
            context["scripts"].append(str(script.relative_to(project_root)))

    output_dir = project_root / "tmp"
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / "raw_context.json", "w", encoding='utf-8') as f:
        json.dump(context, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Context extracted to tmp/raw_context.json")

if __name__ == "__main__":
    extract()
