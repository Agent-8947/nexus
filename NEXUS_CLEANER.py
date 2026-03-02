"""
NEXUS CLEANER v2.0
Maintains root project hygiene by sorting orphaned files into target directories.

Usage:
  python NEXUS_CLEANER.py              # Execute cleanup
  python NEXUS_CLEANER.py --dry-run    # Preview changes without moving files
"""
import os
import sys
import shutil
from pathlib import Path

# --- PATH-AGNOSTIC CONFIGURATION ---
ROOT_DIR = Path(__file__).resolve().parent

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

PROTECTED = [
    "START.md", "TURBO-BOOST.bat", "NEXUS_CLEANER.py",
    "PROJECT", ".agents", ".agent", ".venv", ".git",
    "DOCS", "LOGS", "SYSTEM", "INBOX", "ARCHIVE", "tmp"
]

def clean_nexus(dry_run: bool = False):
    mode = "DRY-RUN" if dry_run else "EXECUTE"
    print(f"🚀 NEXUS CLEANER v2.0 [{mode}]")

    actions = []

    for folder_name, config in STRUCTURE.items():
        target_path = ROOT_DIR / folder_name

        for pattern in config["patterns"]:
            for item in ROOT_DIR.glob(pattern):
                if item.name in PROTECTED:
                    continue
                # Skip items already in target dirs
                if item.parent != ROOT_DIR:
                    continue

                target_item = target_path / item.name
                actions.append({
                    "source": item,
                    "dest": target_item,
                    "folder": folder_name,
                    "is_dir": item.is_dir()
                })

    if not actions:
        print("✅ Workspace is clean. Nothing to move.")
        return

    print(f"   Found {len(actions)} item(s) to organize:\n")

    for action in actions:
        label = "[DIR]" if action["is_dir"] else "[FILE]"
        print(f"   {label} {action['source'].name} → {action['folder']}/")

    if dry_run:
        print(f"\n   ⏸  Dry-run complete. No files were moved.")
        return

    # Execute
    for action in actions:
        target_dir = action["dest"].parent
        target_dir.mkdir(parents=True, exist_ok=True)
        try:
            if action["is_dir"]:
                if action["dest"].exists():
                    for subitem in action["source"].iterdir():
                        shutil.move(str(subitem), str(action["dest"] / subitem.name))
                    action["source"].rmdir()
                else:
                    shutil.move(str(action["source"]), str(action["dest"]))
            else:
                shutil.move(str(action["source"]), str(action["dest"]))
            print(f"   ✓ Moved {action['source'].name}")
        except Exception as e:
            print(f"   ✗ Error: {action['source'].name} — {e}")

    print(f"\n✅ NEXUS CLEANER: {len(actions)} item(s) organized.")


if __name__ == "__main__":
    is_dry = "--dry-run" in sys.argv
    clean_nexus(dry_run=is_dry)
