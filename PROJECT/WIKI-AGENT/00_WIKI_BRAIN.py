"""
NEXUS AGENT 00  THE BRAIN V1.0
================================
Mission: Strategic oversight, historical context analysis, and 
         generating precise technical directives for the Engineer (Agent 06).
"""

import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS")
WIKI_ROOT = PROJECT_ROOT / "PROJECT" / "WIKI-PROJECT"
MEMORY_FILE = PROJECT_ROOT / "PROJECT" / "memory.json"

def banner():
    print("\n" + "=" * 60)
    print("  NEXUS AGENT 00  THE BRAIN V1.0 [BRAIN]")
    print("  Mission: Analyze past builds & provide Architecture Directives")
    print("=" * 60 + "\n")

def load_memory():
    """Loads historical context from all previous builds across all domains."""
    memory = {"past_builds": [], "lessons_learned": []}
    
    # Recursively scan for src directories containing python modules
    if WIKI_ROOT.exists():
        for src_dir in WIKI_ROOT.rglob("src"):
            if src_dir.is_dir():
                modules = [f.stem for f in src_dir.glob("*.py") if not f.name.startswith("__")]
                if modules:
                    # Use the parent directory name as the build name
                    build_name = src_dir.parent.name
                    memory["past_builds"].append({
                        "domain": src_dir.parent.parent.parent.name if len(src_dir.parts) > 3 else "UNKNOWN",
                        "name": build_name,
                        "modules": modules
                    })
    return memory

def analyze_target(target_path, memory):
    """
    Studies the problem based on the target name/content and 
    cross-references with past builds to avoid deduplication.
    """
    target_name = target_path.name if isinstance(target_path, Path) else target_path
    
    print(f"  [BRAIN] Analyzing Target: {target_name}")
    print(f"  [BRAIN] Recalling {len(memory['past_builds'])} previous builds...")

    # Simulated reasoning logic based on historical data
    avoid_modules = set()
    for b in memory["past_builds"]:
        for m in b["modules"]:
            avoid_modules.add(m)

    directive = f"""#  BRAIN DIRECTIVE: {target_name}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 1. STRATEGIC OVERSIGHT
Target identified: `{target_name}`. 
This falls under the scope of NEXUS Intelligence Expansion.

## 2. HISTORICAL CONTEXT
The system currently possesses `{len(avoid_modules)}` unique modules from previous builds.
**Do NOT re-implement exact clones of:**
{chr(10).join(f"- {m}" for list_m in [avoid_modules][:10] for m in list_m)}

## 3. ENGINEER DIRECTIVE (For Agent 06)
Your task is to synthesize new capabilities.
1. **Focus**: Build specialized reconnaissance/analysis tools relevant to `{target_name}`.
2. **Architecture**: Adhere strictly to the `run(target)` standard.
3. **Validation**: Ensure all loops have timeouts. Do not block Agent 16.

*Execute immediately.*
"""
    return directive

def emit_directive(target_dir, directive_text):
    """Writes the directive to the target folder for Agent 06 to pick up."""
    if not isinstance(target_dir, Path):
        target_dir = Path(target_dir)
        
    target_dir.mkdir(parents=True, exist_ok=True)
    directive_path = target_dir / "000_BRAIN_DIRECTIVE.md"
    directive_path.write_text(directive_text, encoding="utf-8")
    print(f"  [+] Directive emitted: {directive_path.name}")

def main():
    banner()
    memory = load_memory()
    
    # For now, let's test it on a hypothetical next target B002
    next_target = WIKI_ROOT / "LEGAL" / "BUILD" / "B002_NEXUS-VANGUARD"
    
    directive = analyze_target(next_target, memory)
    emit_directive(next_target, directive)
    
    print("\n[DONE] Agent 00 has charted the course. Engineer (06) may proceed.")

if __name__ == "__main__":
    main()
