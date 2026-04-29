import sys
from pathlib import Path
import shutil

p = Path("e:/Downloads/--ANTIGRAVITY store/IDE-NEXUS/PROJECT/WIKI-FARM/NEXUS-FARM-DNA/DNA/DNA_12_AST_RENDER")

count = 0
for bak in p.glob("*.py.bak"):
    orig_name = bak.name.replace(".py.bak", ".py")
    target = bak.with_name(orig_name)
    shutil.move(str(bak), str(target))
    count += 1
    
print(f"Restored {count} clean backups. Garbage patches removed.")
