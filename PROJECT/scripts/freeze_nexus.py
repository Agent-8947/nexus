import os
import shutil
from pathlib import Path

# Configuration
SOURCE_DIR = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-optimus")
BLUEPRINT_DIR = Path(r"e:\Downloads\--ANTIGRAVITY store\NEXUS-CORE-BLUEPRINT")

FILES_TO_FREEZE = [
    "START.md",
    "AGNOSTIC_ADR.md",
    "PROJECT/memory.json",
    "PROJECT/fault_registry.json"
]

DIRS_TO_FREEZE = [
    ".agents/workflows",
    "PROJECT/scripts/office",
    "PROJECT/scripts/utils",
    "PROJECT/NEXUS-orchestrator",
    "PROJECT/skills"
]

def freeze():
    print(f"Starting Nexus freeze from {SOURCE_DIR} to {BLUEPRINT_DIR}...")
    if not BLUEPRINT_DIR.exists():
        BLUEPRINT_DIR.mkdir(parents=True)
    
    # Copy files
    for f in FILES_TO_FREEZE:
        src = SOURCE_DIR / f
        dst = BLUEPRINT_DIR / f
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"Frozen: {f}")
        else:
            print(f"Warning: Source file {f} not found.")

    # Copy directories
    for d in DIRS_TO_FREEZE:
        src = SOURCE_DIR / d
        dst = BLUEPRINT_DIR / d
        if src.exists():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"Frozen directory: {d}")
        else:
            print(f"Warning: Source directory {d} not found.")
    
    print("\nNexus Blueprint created successfully.")

if __name__ == "__main__":
    freeze()
