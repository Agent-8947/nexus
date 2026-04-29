"""
NEXUS AGENT 17  GITHUB PROFILE WRITER V1.0
============================================
Mission: Generate professional GitHub repository descriptions,
         README.md, topics, and metadata from build artifacts.

Input:  BUILD/<name>/ folder with src/, vision/, brand_identity.json
Output: README.md, .github/FUNDING.yml, repo description + topics via gh CLI
"""

import json
import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS")
BUILD_DIR = PROJECT_ROOT / "PROJECT" / "WIKI-PROJECT" / "LEGAL" / "BUILD"


def banner():
    print("\n" + "=" * 60)
    print("  NEXUS AGENT 17  GITHUB PROFILE WRITER V1.0")
    print("  Mission: Professional GitHub presence from build artifacts")
    print("=" * 60 + "\n")


def find_latest_build():
    builds = sorted([d for d in BUILD_DIR.iterdir() if d.is_dir()], key=lambda x: x.name)
    if not builds:
        return None
    return builds[-1]


def scan_modules(build_path):
    """Scan src/ for Python modules and extract docstrings."""
    src = build_path / "src"
    modules = []
    if not src.exists():
        return modules
    for py in sorted(src.glob("*.py")):
        if py.name.startswith("__"):
            continue
        name = py.stem
        docstring = ""
        try:
            lines = py.read_text(encoding="utf-8", errors="ignore").splitlines()
            in_doc = False
            for line in lines[:30]:
                if '"""' in line or "'''" in line:
                    if in_doc:
                        break
                    in_doc = True
                    # Single-line docstring
                    stripped = line.strip().strip("\"'")
                    if stripped:
                        docstring = stripped
                    continue
                if in_doc:
                    docstring += " " + line.strip()
        except Exception:
            pass
        modules.append({"name": name, "doc": docstring.strip()})
    return modules


def read_brand(build_path):
    """Read brand_identity.json if present."""
    bp = build_path / "brand_identity.json"
    if bp.exists():
        try:
            return json.loads(bp.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def read_vision(build_path):
    """Read the first vision/concept markdown file."""
    vision_dir = build_path / "vision"
    if not vision_dir.exists():
        vision_dir = build_path
    for md in sorted(vision_dir.glob("*.md")):
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")
            # Extract first meaningful paragraph
            lines = [l.strip() for l in text.splitlines() if l.strip() and not l.startswith("#")]
            return " ".join(lines[:5])
        except Exception:
            continue
    return ""


def extract_project_name(build_path):
    """Extract human-readable name from build folder."""
    name = build_path.name
    # Strip B001_ prefix
    if name[:4].startswith("B") and name[4] == "_":
        name = name[5:]
    return name.replace("-", " ").replace("_", " ").title()


def generate_topics(modules, brand):
    """Generate GitHub topics from modules and brand data."""
    base_topics = ["osint", "intelligence", "reconnaissance", "python", "automation", "nexus"]
    module_keywords = {
        "domain_intel": ["domain-analysis", "dns", "whois"],
        "ssl_scanner": ["ssl", "tls", "certificates"],
        "web_crawler": ["web-scraping", "crawler"],
        "security_analyzer": ["security", "vulnerability-scanner"],
        "breach_intel": ["data-breach", "haveibeenpwned"],
        "social_profiler": ["social-media", "profiling"],
        "entity_mapper": ["entity-extraction", "knowledge-graph"],
    }
    topics = set(base_topics)
    for m in modules:
        if m["name"] in module_keywords:
            topics.update(module_keywords[m["name"]])
    return sorted(topics)[:20]  # GitHub allows max 20 topics


def generate_readme(build_path, project_name, modules, brand, vision_text):
    """Generate a professional README.md."""
    repo_name = build_path.name
    github_url = f"https://github.com/Agent-8947/{repo_name}"

    # --- Slogan & Description ---
    raw_slogan = brand.get("slogan", "Autonomous Intelligence Pipeline")
    slogan = raw_slogan.get("en", raw_slogan) if isinstance(raw_slogan, dict) else str(raw_slogan)
    
    raw_pitch = brand.get("pitch", "")
    pitch = raw_pitch.get("en", raw_pitch) if isinstance(raw_pitch, dict) else str(raw_pitch)
    if not pitch:
        pitch = vision_text[:200] if vision_text else "Multi-layer OSINT reconnaissance system."

    # --- What to provide ---
    provide_data = brand.get("what_to_provide", {})
    provide_items = provide_data.get("items", {}).get("en", [
        "A domain name (e.g. example.com)",
        "OR a company name",
        "OR an email address"
    ])

    # --- Deployment ---
    dep = brand.get("deployment", {})
    requirements = dep.get("requirements", ["Python 3.10+", "pip"])

    # --- Module table ---
    module_rows = ""
    for i, m in enumerate(modules, 1):
        doc = m["doc"][:80] + "..." if len(m.get("doc", "")) > 80 else m.get("doc", "")
        module_rows += f"| `{m['name']}` | {doc} |\n"

    # --- README content ---
    readme = f"""<div align="center">
<img src="logo.png" width="300" alt="{project_name} Logo">

# {project_name}

**{slogan}**

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)]({github_url}/blob/master/LICENSE)
[![NEXUS](https://img.shields.io/badge/NEXUS-Intelligence_Factory-DC1E1E.svg)]({github_url})

---

*{pitch}*

</div>

## Overview

{project_name} is an autonomous multi-layer intelligence pipeline built by the **NEXUS Intelligence Factory**. It ingests a target (domain, company, or individual), searches across multiple intelligence layers, and delivers a structured reconnaissance report  without human intervention.

## Modules

| Module | Description |
|--------|-------------|
{module_rows}
## Quick Start

```bash
# Clone
git clone {github_url}.git
cd {repo_name}

# Install dependencies
pip install -r requirements.txt

# Run the full pipeline
python src/shadow_cli.py example.com
```

## What You Need to Provide

{chr(10).join(f'- {item}' for item in provide_items)}

## Requirements

{chr(10).join(f'- {r}' for r in requirements)}

## Architecture

```

              SHADOW CLI (Orchestrator)       

 Domain     SSL      Web      Security    
  Intel   Scanner  Crawler    Analyzer    

 Breach   Social   Entity     ... more    
  Intel  Profiler  Mapper     plugins     

          JSON Report + Logs 
```

## Output

All results are saved as structured JSON reports in the `logs/` directory with timestamps.

## Built With

- **NEXUS Intelligence Factory**  Autonomous agent-based code synthesis
- **Python 3.10+**  Core runtime
- **PIL / Pillow**  Logo generation
- **Standard Library**  `ssl`, `socket`, `http.client`, `json`, `threading`

## License

MIT  See [LICENSE]({github_url}/blob/master/LICENSE) for details.

---

<div align="center">
<sub>Synthesized by <b>NEXUS Agent 11</b>  Validated by <b>Agent 16</b>  Branded by <b>Agent 13</b>  Profiled by <b>Agent 17</b></sub>
</div>
"""
    return readme


def generate_short_description(project_name, brand):
    """One-liner for GitHub repo description field."""
    raw = brand.get("slogan", "")
    slogan = raw.get("en", raw) if isinstance(raw, dict) else str(raw)
    if slogan:
        return f"{project_name}  {slogan}"
    return f"{project_name}  Autonomous OSINT Intelligence Pipeline by NEXUS"


def apply_to_github(build_path, description, topics):
    """Use gh CLI to set repo description and topics."""
    import subprocess
    repo_name = build_path.name

    gh = "gh"
    gh_path = Path(r"C:\Program Files\GitHub CLI\gh.exe")
    if gh_path.exists():
        gh = f'"{gh_path}"'

    # Set description
    cmd_desc = f'{gh} repo edit Agent-8947/{repo_name} --description "{description}"'
    res = subprocess.run(cmd_desc, capture_output=True, text=True, shell=True)
    if res.returncode == 0:
        print(f"  [+] GitHub description set.")
    else:
        print(f"  [!] Description failed: {res.stderr.strip()[:100]}")

    # Set topics
    topics_str = ",".join(topics)
    cmd_topics = f'{gh} repo edit Agent-8947/{repo_name} --add-topic "{topics_str}"'
    res = subprocess.run(cmd_topics, capture_output=True, text=True, shell=True)
    if res.returncode == 0:
        print(f"  [+] GitHub topics set: {topics_str}")
    else:
        print(f"  [!] Topics failed: {res.stderr.strip()[:100]}")


def push_readme(build_path):
    """Git add, commit, push the README."""
    import subprocess
    cmds = [
        'git add README.md',
        'git commit -m "docs: professional README by Agent 17"',
        'git push origin master'
    ]
    for cmd in cmds:
        res = subprocess.run(cmd, capture_output=True, text=True, shell=True, cwd=str(build_path))
        if res.returncode != 0 and "nothing to commit" not in res.stderr + res.stdout:
            print(f"  [!] Git: {res.stderr.strip()[:100]}")
            return False
    print("  [+] README pushed to GitHub.")
    return True


def main():
    banner()

    build_path = find_latest_build()
    if not build_path:
        print("[!] No build found.")
        sys.exit(1)

    print(f"  [*] Build: {build_path.name}")

    project_name = extract_project_name(build_path)
    modules = scan_modules(build_path)
    brand = read_brand(build_path)
    vision_text = read_vision(build_path)

    print(f"  [*] Project: {project_name}")
    print(f"  [*] Modules found: {len(modules)}")

    # 1. Generate README
    readme = generate_readme(build_path, project_name, modules, brand, vision_text)
    readme_path = build_path / "README.md"
    readme_path.write_text(readme, encoding="utf-8")
    print(f"  [+] README.md generated ({len(readme)} chars)")

    # 2. Generate topics & description
    topics = generate_topics(modules, brand)
    description = generate_short_description(project_name, brand)
    print(f"  [+] Description: {description}")
    print(f"  [+] Topics: {', '.join(topics)}")

    # 3. Push README to GitHub
    push_readme(build_path)

    # 4. Apply description + topics via gh CLI
    apply_to_github(build_path, description, topics)

    print(f"\n[DONE] {build_path.name}  GitHub profile complete.")


if __name__ == "__main__":
    main()
