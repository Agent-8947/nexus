import os
import hashlib
import json
from pathlib import Path

DNA_ROOT = Path("e:/Downloads/--ANTIGRAVITY store/IDE-NEXUS/PROJECT/WIKI-FARM/NEXUS-FARM-DNA/DNA")
LOCK_FILE = DNA_ROOT / "skills-lock.json"

def calculate_hash(filepath: Path) -> str:
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def generate_lock():
    skills = {}
    
    # Scan main DNA directory and subdirectories
    for root, dirs, files in os.walk(DNA_ROOT):
        # Skip hidden and special folders
        if "__pycache__" in root or ".github" in root:
            continue
            
        rel_root = Path(root).relative_to(DNA_ROOT)
        
        for file in files:
            if file.endswith(".py") and not file.startswith("_"):
                filepath = Path(root) / file
                rel_path = str(rel_root / file).replace("\\", "/")
                
                # Use filename as skill identifier
                skill_id = file.replace(".py", "")
                
                skills[skill_id] = {
                    "path": rel_path,
                    "hash": calculate_hash(filepath),
                    "version": "1.0.0"
                }

    lock_data = {
        "version": 1,
        "engine": "NEXUS-V5",
        "skills": skills
    }

    with open(LOCK_FILE, "w", encoding="utf-8") as f:
        json.dump(lock_data, f, indent=2)
    
    print(f"DONE: {len(skills)} skills locked in {LOCK_FILE}")

if __name__ == "__main__":
    generate_lock()
