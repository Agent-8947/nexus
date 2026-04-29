import os
import json
import re
from pathlib import Path

# NEXUS OBSIDIAN DNA EXTRACTOR v3.1 [PORTABLE + UNIFIED OUTPUT]
# FIX [C-01]: All paths relative to __file__
# FIX [M-05]: Output unified to DNA_13_Obsidian_DNA.json (canonical location)

DNA_DIR    = Path(__file__).resolve().parent
FARM_ROOT  = DNA_DIR.parent.parent
VAULT_PATH = FARM_ROOT / "NEXUS-OBSIDIAN-VAULT"
REPOS_BASE = FARM_ROOT.parent / "WIKI"
OUTPUT_FILE = DNA_DIR / "DNA_13_Obsidian_DNA.json"   # FIX [M-05]: canonical path


def analyze_repository(target_dir: Path) -> dict:
    """v3.1: Deep recursive analysis of a repository."""
    stats = {
        "linked": True,
        "root": str(target_dir),
        "total_files": 0,
        "code_files": 0,
        "docs_files": 0,
        "languages": {},
        "entry_points": [],
        "repo_type": "UNKNOWN",
        "has_docker": False,
        "has_actions": False
    }

    try:
        count = 0
        for f in target_dir.rglob("*"):
            if f.is_file() and ".git" not in f.parts:
                count += 1
                if count > 1000:
                    break

                stats["total_files"] += 1
                ext = f.suffix.lower()
                if ext:
                    stats["languages"][ext] = stats["languages"].get(ext, 0) + 1

                if ext in [".py", ".go", ".rs", ".js", ".cpp", ".c", ".ts", ".java", ".sh"]:
                    stats["code_files"] += 1
                elif ext in [".md", ".rst", ".txt", ".pdf"]:
                    stats["docs_files"] += 1

                name_low = f.name.lower()
                if name_low in ["docker-compose.yml", "dockerfile"]:
                    stats["has_docker"] = True
                if ".github/workflows" in str(f):
                    stats["has_actions"] = True
                if name_low in ["main.py", "app.py", "index.js", "main.go", "cargo.toml",
                                 "requirements.txt", "setup.py"]:
                    stats["entry_points"].append(str(f.relative_to(target_dir)))

        # Heuristic classification
        if stats["code_files"] > (stats["total_files"] * 0.1):
            stats["repo_type"] = "CODEBASE"
        elif stats["code_files"] > 0:
            stats["repo_type"] = "MIXED"
        else:
            stats["repo_type"] = "DOCUMENTATION"

    except Exception as e:
        return {"linked": True, "error": str(e), "repo_type": "ERROR"}

    return stats


def run_v3_harvest():
    if not VAULT_PATH.exists():
        print(f"[!] Error: Vault not found: {VAULT_PATH}")
        return

    dna_library = []
    print(f"[*] Starting Nexus DNA v3.1 [Technical Audit]...")
    print(f"    Vault: {VAULT_PATH}")
    print(f"    Repos: {REPOS_BASE}")

    for md_file in sorted(VAULT_PATH.glob("*.md")):
        try:
            title = md_file.stem

            # Try multiple naming variants for repo lookup
            variants = [title, title.lower(), title.upper(), title.replace("-", "_")]
            repo_path = None
            for v in variants:
                test_p = REPOS_BASE / v
                if test_p.exists():
                    repo_path = test_p
                    break

            if repo_path:
                node_stats = analyze_repository(repo_path)
            else:
                node_stats = {"linked": False, "repo_type": "ORCHESTRATOR_ONLY"}

            dna_library.append({
                "id": title.upper(),
                "name": title,
                "type": node_stats["repo_type"],
                "stats": node_stats,
                "obsidian_md": str(md_file.relative_to(VAULT_PATH.parent)),
                "is_executable": (
                    node_stats.get("has_docker", False) or
                    len(node_stats.get("entry_points", [])) > 0
                )
            })

            print(f"  [AUDIT] {title:<25} | Type: {node_stats['repo_type']:<18} | Linked: {node_stats['linked']}")

        except Exception as e:
            print(f"  [ERR] {md_file.stem}: {e}")

    # FIX [M-05]: Write to canonical DNA_13 location
    result = {
        "version": "3.1-PORTABLE",
        "built_at": __import__('datetime').datetime.now().isoformat(),
        "total_nodes":    len(dna_library),
        "codebase_nodes": len([i for i in dna_library if i["type"] == "CODEBASE"]),
        "docs_nodes":     len([i for i in dna_library if i["type"] == "DOCUMENTATION"]),
        "data": dna_library
    }
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n[FINAL] AUDIT COMPLETE -> {OUTPUT_FILE}")
    print(f"[*] Codebase repos: {result['codebase_nodes']} | Docs repos: {result['docs_nodes']}")


if __name__ == "__main__":
    run_v3_harvest()
