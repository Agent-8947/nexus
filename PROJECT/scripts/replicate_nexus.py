import os
import shutil
import sys
from pathlib import Path

BLUEPRINT_DIR = Path(r"e:\Downloads\--ANTIGRAVITY store\NEXUS-CORE-BLUEPRINT")

def replicate(target_dir_str):
    target_dir = Path(target_dir_str)
    
    if not BLUEPRINT_DIR.exists():
        print(f"Error: Blueprint not found at {BLUEPRINT_DIR}. Run /freeze-nexus first.")
        return

    print(f"Replicating Nexus Blueprint to {target_dir}...")
    
    if not target_dir.exists():
        target_dir.mkdir(parents=True)

    # Recursive copy from Blueprint to Target
    for item in BLUEPRINT_DIR.iterdir():
        dest = target_dir / item.name
        if item.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest)
            print(f"Replicated Directory: {item.name}")
        else:
            shutil.copy2(item, dest)
            print(f"Replicated File: {item.name}")

    print("\n[SUCCESS] Nexus architecture развернута в новом рабочем пространстве.")
    print("Next Steps: cd into the new directory and run 'node PROJECT/scripts/office/generate_nexus_assets.js'")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python replicate_nexus.py <target_directory_path>")
        sys.exit(1)
    
    replicate(sys.argv[1])
