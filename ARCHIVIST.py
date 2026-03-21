"""
NEXUS ARCHIVIST v1.0
Autonomous agent for workspace hygiene and cataloging.
Runs autonomously to clean the workspace and build a master index of all files, 
so the AI and the USER always know exactly where everything is located.
"""
import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

# Prevent UnicodeEncodeError on Windows 
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = ROOT_DIR / "PROJECT"
SYSTEM_DIR = ROOT_DIR / "SYSTEM"

# Master Index paths
INDEX_FILE_MD = SYSTEM_DIR / "ARCHIVE_INDEX.md"
INDEX_FILE_JSON = SYSTEM_DIR / "ARCHIVE_MAP.json"

# Rules for auto-sorting orphaned files dropped in the root folder
STRUCTURE = {
    "DOCS": {
        "patterns": ["*.pdf", "*.docx", "AGNOSTIC_ADR.md", "findings.md", "*.xlsx"],
        "description": "Documents and exports"
    },
    "LOGS": {
        "patterns": ["*.log", "activity_log.json", "progress.md"],
        "description": "System tracking"
    },
    "INBOX": {
        "patterns": ["IN_*", "raw_*"],
        "description": "Incoming raw data"
    },
    "ARCHIVE": {
        "patterns": ["*.zip", "*.tar.gz", "*.rar"],
        "description": "Compressed archives"
    }
}

# Directories to ignore during deep cataloging (large or system specific)
IGNORE_DIRS = {".git", ".venv", "__pycache__", "node_modules", ".agents", ".agent", "tmp"}

def clean_and_sort():
    print("🧹 [Archivist] Scanning root for loose files to sort...")
    moved = 0
    for folder_name, config in STRUCTURE.items():
        target_path = ROOT_DIR / folder_name
        for pattern in config["patterns"]:
            for item in ROOT_DIR.glob(pattern):
                if item.is_file() and item.name != "ARCHIVIST.py":
                    target_path.mkdir(exist_ok=True)
                    shutil.move(str(item), str(target_path / item.name))
                    print(f"  -> Moved {item.name} to {folder_name}/")
                    moved += 1
    if moved == 0:
        print("  -> Root is clean. No orphaned files found.")
    else:
        print(f"  -> {moved} files automatically sorted.")

def build_catalog():
    print("🗂️ [Archivist] Building absolute project catalog...")
    catalog = {}
    markdown_lines = [
        "# 🏛️ NEXUS ARCHIVE INDEX",
        f"> **Last updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "This is the Absolute Truth map generated autonomously by the Archivist.",
        "It catalogs exactly what lies where, ensuring zero hallucination for the Agent.",
        "---",
        ""
    ]

    total_files = 0
    total_dirs = 0

    for root, dirs, files in os.walk(ROOT_DIR):
        # In-place modification to skip ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        rel_path = Path(root).relative_to(ROOT_DIR)
        display_path = "/" if str(rel_path) == "." else f"/{str(rel_path).replace(os.sep, '/')}"

        # Do not include the root files inside the catalog unless it's the root itself
        # This keeps the tree clean.

        folder_data = {"files": [], "subdirs": dirs}
        
        if files:
            markdown_lines.append(f"### 📂 `{display_path}`")
            for f in files:
                folder_data["files"].append(f)
                markdown_lines.append(f"- 📄 {f}")
                total_files += 1
            total_dirs += 1
            markdown_lines.append("")

        catalog[str(rel_path)] = folder_data

    # Save Catalog to SYSTEM directory
    SYSTEM_DIR.mkdir(exist_ok=True)
    with open(INDEX_FILE_JSON, "w", encoding="utf-8") as jf:
        json.dump(catalog, jf, indent=2, ensure_ascii=False)
    
    with open(INDEX_FILE_MD, "w", encoding="utf-8") as mf:
        mf.write("\n".join(markdown_lines))

    print(f"✅ [Archivist] Cataloging complete. Mapped {total_files} files in {total_dirs} directories.")
    print(f"📄 Saved to: SYSTEM/ARCHIVE_INDEX.md")
    print(f"🧠 Updated for AI at: SYSTEM/ARCHIVE_MAP.json")

if __name__ == "__main__":
    print("\n" + "="*55)
    print("🏛️  NEXUS ARCHIVIST : AUTONOMOUS HYGIENE & CATALOGING")
    print("="*55)
    clean_and_sort()
    build_catalog()
    print("="*55 + "\n")
