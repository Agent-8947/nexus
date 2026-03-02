import json
from pathlib import Path

def generate():
    project_root = Path("e:/Downloads/--ANTIGRAVITY store/IDE-optimus")
    context_path = project_root / "tmp" / "raw_context.json"
    output_path = project_root / "PROJECT" / "DOCS" / "TECHNICAL_BRIEF.md"
    
    if not context_path.exists():
        print("❌ Context not found. Run extract_context.py first.")
        return

    with open(context_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    mem = data.get("memory", {})
    stack = mem.get("stack", {})
    
    md = f"""# NEXUS: Technical Brief
**Generated on**: 2026-03-01
**Archetype**: {mem.get('archetype', 'N/A')}

## 1. System Architecture
```mermaid
graph TD
    UI[Frontend: {stack.get('frontend', {}).get('static', 'Astro')}] --> API[Backend: {stack.get('backend', {}).get('main', 'FastAPI')}]
    API --> AI[AI Agents: {stack.get('ai_automation', {}).get('agents', 'LangGraph')}]
    API --> DB[DB: {stack.get('database', {}).get('main', 'Supabase')}]
    API --> OS[OS Automation: {stack.get('desktop', {}).get('cli', 'Python')}]
```

## 2. Technology Stack
| Layer | Technology | Status |
|---|---|---|
| Frontend | {stack.get('frontend', {}).get('static')} | Active |
| Backend | {stack.get('backend', {}).get('main')} | Active |
| AI/Agent | {stack.get('ai_automation', {}).get('agents')} | Active |
| Database | {stack.get('database', {}).get('main')} | Active |

## 3. Current Objectives
{data.get('current_goal', 'N/A')}

## 4. Active Scripts
"""
    for script in data.get("scripts", []):
        md += f"- `{script}`\n"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding='utf-8') as f:
        f.write(md)
        
    print(f"✅ Documentation generated: {output_path}")

if __name__ == "__main__":
    generate()
