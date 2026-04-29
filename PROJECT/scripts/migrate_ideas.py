import os
import shutil
from pathlib import Path

source_dir = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\EXTERNAL-LIBRARY\app-ideas\Projects")
dest_dir = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\IDEAS")

if not dest_dir.exists():
    dest_dir.mkdir(parents=True)

print(f"[NEXUS] Starting Corrected App-Ideas Migration from {source_dir}...")

moved_count = 0
# Iterate through categories (1-Beginner, 2-Intermediate, 3-Advanced)
for level in source_dir.iterdir():
    if level.is_dir():
        print(f"  > Processing {level.name}...")
        # Find all .md files inside the category folder
        for file in level.glob("*.md"):
            # Prefix with level for organization
            target_name = f"{level.name}_{file.name}"
            target_file = dest_dir / target_name
            shutil.copy2(file, target_file)
            moved_count += 1

print(f"✅ Migration complete. {moved_count} project specs successfully indexed in {dest_dir}.")
