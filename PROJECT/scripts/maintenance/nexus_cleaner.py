import os
import shutil
from pathlib import Path

# --- CONFIGURATION (NEXUS 2026 STANDARDS) ---
ROOT_DIR = Path("e:/Downloads/--ANTIGRAVITY store/IDE-optimus")
STRUCTURE = {
    "DOCS": {
        "patterns": ["AGNOSTIC_ADR.md", "findings.md", "*.pdf", "*.docx"],
        "description": "Technical documentation and exports"
    },
    "LOGS": {
        "patterns": ["progress.md", "task_plan.md", "activity_log.json"],
        "description": "Tracking and auditing state"
    },
    "SYSTEM": {
        "patterns": ["skills-lock.json", "temp_skills"],
        "description": "Internal AI system metadata"
    },
    "INBOX": {
        "patterns": ["IN"],
        "description": "Incoming raw data"
    },
    "ARCHIVE": {
        "patterns": ["BACKUPS"],
        "description": "Compressed snapshots"
    }
}

PROTECTED = ["START.md", "TURBO-BOOST.bat", "PROJECT", ".agents", ".agent", ".venv", ".git"]

def clean_nexus():
    print("🚀 NEXUS CLEANER: Starting organization...")
    
    for folder_name, config in STRUCTURE.items():
        target_path = ROOT_DIR / folder_name
        if not target_path.exists():
            target_path.mkdir(parents=True, exist_ok=True)
            print(f" [+] Created: {folder_name}/")

        for pattern in config["patterns"]:
            for item in ROOT_DIR.glob(pattern):
                if item.name in PROTECTED:
                    continue
                
                # Special case for directories
                target_item = target_path / item.name
                try:
                    if item.is_dir():
                        if target_item.exists():
                             # Merge or skip if subdirectory exists? For now, we move contents.
                             for subitem in item.iterdir():
                                 shutil.move(str(subitem), str(target_item / subitem.name))
                             item.rmdir()
                        else:
                            shutil.move(str(item), str(target_item))
                    else:
                        shutil.move(str(item), str(target_item))
                    print(f"  -> Moved {item.name} to {folder_name}/")
                except Exception as e:
                    print(f"  [!] Error moving {item.name}: {e}")

    print("✅ NEXUS CLEANER: Workspace optimized.")

if __name__ == "__main__":
    clean_nexus()
