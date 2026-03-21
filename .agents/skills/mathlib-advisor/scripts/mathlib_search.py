#!/usr/bin/env python3
"""
MathLib-Advisor — Search and Explore Lean 4 Mathematical Library.

Usage:
    python mathlib_search.py find "Fermat"
    python mathlib_search.py show "Mathlib.Algebra.Group.Defs"
    python mathlib_search.py search "Category Theory"
"""

import os
import sys
import re
import json

SOURCE_DIR = os.path.dirname(os.path.abspath(__file__)) + "/../source/Mathlib"

def find_theorems(query):
    results = []
    # Search for theorem/lemma/def in the source files
    pattern = re.compile(rf"(theorem|lemma|def)\s+([^\s\:]*{query}[^\s\:]*)", re.IGNORECASE)
    
    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.endswith(".lean"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        for i, line in enumerate(f):
                            match = pattern.search(line)
                            if match:
                                rel_path = os.path.relpath(path, SOURCE_DIR).replace(os.sep, ".")[:-5]
                                results.append({
                                    "type": match.group(1),
                                    "name": match.group(2),
                                    "module": "Mathlib." + rel_path,
                                    "line": i + 1,
                                    "file": path
                                })
                except Exception:
                    continue
    return results[:20] # Limit results

def get_definition(module_or_file):
    # Convert module dot notation to path
    if module_or_file.startswith("Mathlib."):
        path = os.path.join(SOURCE_DIR, module_or_file[8:].replace(".", os.sep) + ".lean")
    else:
        path = module_or_file

    if not os.path.exists(path):
        return {"error": f"Path not found: {path}"}

    with open(path, "r", encoding="utf-8") as f:
        return {"content": f.read()}

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    arg = sys.argv[2]

    if cmd == "find":
        res = find_theorems(arg)
        print(json.dumps(res, indent=2))
    elif cmd == "show":
        res = get_definition(arg)
        print(res["content"][:2000] + "..." if "content" in res else res)
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
