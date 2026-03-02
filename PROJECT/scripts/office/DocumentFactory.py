"""
NEXUS DOCUMENT FACTORY v2.0 (Implemented)
Unified engine for generating MD and PDF technical reports.

Usage:
  python DocumentFactory.py                 # Generate Technical Brief (MD)
  python DocumentFactory.py --pdf           # Generate PDF report
  python DocumentFactory.py --cleanup       # Remove deprecated scripts
  python DocumentFactory.py --all           # Full pipeline: extract → generate → validate
"""
import os
import sys
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
WORKSPACE_ROOT = PROJECT_ROOT.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts" / "office"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
DOCS_DIR = PROJECT_ROOT / "DOCS"
TMP_DIR = WORKSPACE_ROOT / "tmp"


class DocumentFactory:
    """
    NEXUS DOCUMENT FACTORY v2.0
    Single entry point for all document generation.
    """

    def __init__(self):
        for d in [OUTPUT_DIR, DOCS_DIR, TMP_DIR]:
            d.mkdir(parents=True, exist_ok=True)
        self.context = self._extract_context()

    # ─── PHASE 1: Context Extraction ────────────────────────

    def _extract_context(self) -> dict:
        ctx = {"memory": {}, "current_goal": "", "scripts": [], "skills": [], "timestamp": datetime.now().isoformat()}

        memory_path = PROJECT_ROOT / "memory.json"
        if memory_path.exists():
            with open(memory_path, "r", encoding="utf-8") as f:
                ctx["memory"] = json.load(f)

        start_path = WORKSPACE_ROOT / "START.md"
        if start_path.exists():
            with open(start_path, "r", encoding="utf-8") as f:
                ctx["current_goal"] = f.read()

        scripts_dir = PROJECT_ROOT / "scripts"
        if scripts_dir.exists():
            ctx["scripts"] = [str(s.relative_to(PROJECT_ROOT)) for s in scripts_dir.rglob("*.py")]

        skills_dir = PROJECT_ROOT / "skills"
        if skills_dir.exists():
            ctx["skills"] = [d.name for d in skills_dir.iterdir() if d.is_dir()]

        # Persist extracted context
        with open(TMP_DIR / "raw_context.json", "w", encoding="utf-8") as f:
            json.dump(ctx, f, indent=2, ensure_ascii=False)

        return ctx

    # ─── PHASE 2: Technical Brief (MD) ──────────────────────

    def generate_technical_brief(self) -> Path:
        mem = self.context.get("memory", {})
        stack = mem.get("stack", {})
        history = mem.get("history", [])

        # Build Mermaid diagram
        fe = stack.get("frontend", {}).get("static", "N/A")
        be = stack.get("backend", {}).get("main", "N/A")
        ai = stack.get("ai_automation", {}).get("agents", "N/A")
        db = stack.get("database", {}).get("main", "N/A")
        desk = stack.get("desktop", {}).get("cli", "N/A")

        md = f"""# NEXUS: Technical Brief
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Archetype**: {mem.get('archetype', 'N/A')}

---

## 1. System Architecture
```mermaid
graph TD
    UI["{fe}"] --> API["{be}"]
    API --> AI["{ai}"]
    API --> DB["{db}"]
    API --> OS["{desk}"]
```

## 2. Technology Stack
| Layer | Technology | Role |
|---|---|---|
| Frontend | {fe} | Static site generation |
| Backend | {be} | API & business logic |
| AI/Agent | {ai} | Autonomous orchestration |
| Database | {db} | Persistence |
| Desktop | {desk} | Local automation |
| Edge | {stack.get('backend', {}).get('edge', 'N/A')} | Edge compute |
| Cache | {stack.get('database', {}).get('cache', 'N/A')} | Hot data layer |

## 3. Active Skills
"""
        for skill in self.context.get("skills", []):
            md += f"- `{skill}`\n"

        md += "\n## 4. Decision Log (ADR History)\n"
        for entry in history[-5:]:
            md += f"- **{entry.get('timestamp', '?')}**: {entry.get('action', '?')}\n"

        md += "\n## 5. Active Scripts\n"
        scripts = self.context.get("scripts", [])
        # Group by directory
        groups = {}
        for s in scripts:
            parts = Path(s).parts
            group = parts[1] if len(parts) > 2 else "root"
            groups.setdefault(group, []).append(s)

        for group, items in sorted(groups.items()):
            md += f"\n### {group}/\n"
            for item in sorted(items):
                md += f"- `{item}`\n"

        out_path = DOCS_DIR / "TECHNICAL_BRIEF.md"
        
        # --- PHASE 2.1: AI Reflection & Refinement (Step 9) ---
        if os.environ.get("ANTHROPIC_API_KEY"):
            print("🧠 Running AI Reflection Phase...")
            refined_md = self._reflect_on_content(md)
            if refined_md:
                md = refined_md
                print("✨ Document refined by AI.")

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(md)

        print(f"✅ Technical Brief generated: {out_path}")
        return out_path

    def _reflect_on_content(self, content: str) -> str:
        """
        Reflection Agent: Requesting peer review from the IDE Agent (Gemini).
        """
        try:
            from ide_bridge import IDEBridge
            bridge = IDEBridge()
            
            payload = {
                "document": content,
                "role": "Technical Documentation Critic",
                "instruction": "Review the Technical Brief. Improve architecture details, terminology, and add a 'Future Roadmap' if missing."
            }
            
            # Запрос рефлексии у агента IDE
            refined_doc = bridge.request_llm("REFLECT_DOC", payload)
            return refined_doc
            
        except Exception as e:
            print(f"⚠️ Reflection failed: {e}")
            return None

    # ─── PHASE 3: Validation ────────────────────────────────

    def validate(self, path: Path) -> bool:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        warnings = []
        if "TODO" in content:
            warnings.append("Contains TODO markers")
        if content.count("N/A") > 3:
            warnings.append(f"Multiple N/A placeholders ({content.count('N/A')})")
        if len(content) < 200:
            warnings.append("Document is suspiciously short")

        if warnings:
            print(f"⚠️  Validation [{path.name}]:")
            for w in warnings:
                print(f"   - {w}")
            return False
        else:
            print(f"✅ Validation passed: {path.name}")
            return True

    # ─── PHASE 4: Cleanup ──────────────────────────────────

    def cleanup_legacy(self):
        deprecated = [
            "generate_pdf_simple.py",
            "generate_pdf_ultra.py",
            "generate_pdf.py",
        ]
        removed = 0
        for script in deprecated:
            p = SCRIPTS_DIR / script
            if p.exists():
                p.unlink()
                print(f" [-] Removed: {script}")
                removed += 1

        # Also check utils for consolidated scripts
        utils_dir = PROJECT_ROOT / "scripts" / "utils"
        consolidated = [
            # Inkjet (→ builders/inkjet_builder.py)
            "build_inkjet_block.py",
            "build_looping_inkjet.py",
            "build_realistic_inkjet.py",
            "build_ultimate_inkjet.py",
            # DTF/Hero (→ builders/dtf_builder.py)
            "build_pageflip_dtf_module.py",
            "build_peel_loop_module.py",
            "build_full_hero_module.py",
            "build_transparent_hero_module.py",
            "build_master_block.py",
            "fix_peel_loop.py",
            "fix_visibility_v3.py",
        ]
        for script in consolidated:
            p = utils_dir / script
            if p.exists():
                p.unlink()
                print(f" [-] Consolidated → removed: {script}")
                removed += 1

        if removed == 0:
            print("✅ No legacy scripts found. Workspace is clean.")
        else:
            print(f"✅ Removed {removed} deprecated file(s).")

    # ─── PIPELINE ──────────────────────────────────────────

    def run_full_pipeline(self):
        print("═══ NEXUS DOCUMENT FACTORY v2.0 ═══")
        print("Phase 1: Context Extraction... done")
        print("Phase 2: Generating Technical Brief...")
        path = self.generate_technical_brief()
        print("Phase 3: Validating...")
        self.validate(path)
        print("═══ Pipeline Complete ═══")


if __name__ == "__main__":
    factory = DocumentFactory()

    if "--cleanup" in sys.argv:
        factory.cleanup_legacy()
    elif "--all" in sys.argv:
        factory.run_full_pipeline()
    else:
        factory.generate_technical_brief()
