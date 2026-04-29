import os
import shutil
from pathlib import Path

source_dir = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\EXTERNAL-LIBRARY\gitignore")
dest_dir = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\TEMPLATES\GITIGNORE")

if not dest_dir.exists():
    dest_dir.mkdir(parents=True)

print(f"[NEXUS] Starting Gitignore Migration from {source_dir}...")

moved_count = 0
for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.endswith(".gitignore"):
            # Use parent folder name if needed, but for gitignore repo, 
            # many are in root or Global/
            rel_path = os.path.relpath(os.path.join(root, file), source_dir)
            target_name = rel_path.replace(os.sep, "_")
            target_file = dest_dir / target_name
            shutil.copy2(os.path.join(root, file), target_file)
            moved_count += 1

print(f"✅ Migration complete. {moved_count} templates successfully moved to {dest_dir}.")
