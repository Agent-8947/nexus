import os
import shutil
from pathlib import Path

source_dir = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\EXTERNAL-LIBRARY\developer-roadmap\src\data\roadmaps")
dest_dir = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\ROADMAPS")

if not dest_dir.exists():
    dest_dir.mkdir(parents=True)

print(f"[NEXUS] Starting Roadmap Migration from {source_dir}...")

moved_count = 0
for roadmap_folder in source_dir.iterdir():
    if roadmap_folder.is_dir():
        # Look for .json and .md files inside the folder
        for file in roadmap_folder.glob("*.*"):
            if file.suffix.lower() in [".json", ".md"]:
                target_file = dest_dir / file.name
                shutil.copy2(file, target_file)
                moved_count += 1

print(f"✅ Migration complete. {moved_count} files (Roadmaps & Docs) moved to {dest_dir}.")
