"""
NEXUS Agent 13  WIKI_MARKETER V5.0
================================
Специализация: Брендинг и маркетинговая упаковка готовых билдов.
Стиль: Строгая типографика, сетка, контраст, три языка (EN/UA/RU).
"""

import sys
import re
import shutil
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS")
WIKI_PROJECT_DIR = PROJECT_ROOT / "PROJECT" / "WIKI-PROJECT"

def banner():
    print("\n" + "=" * 60)
    print("  NEXUS AGENT 13  MARKETER V5.0")
    print("  Mission: Package  Brand  Present  Launch")
    print("=" * 60 + "\n")

def find_latest_build():
    build_dirs = []
    for domain_dir in WIKI_PROJECT_DIR.iterdir():
        if not domain_dir.is_dir(): continue
        build_path = domain_dir / "BUILD"
        if build_path.exists():
            for item in build_path.iterdir():
                if item.is_dir() and (item.name.startswith("B") or "PROD_" in item.name):
                    build_dirs.append(item)
    if not build_dirs: return None
    return sorted(build_dirs)[-1]

def extract_product_info(build_path):
    readme = build_path / "README.md"
    name = "NEXUS Tool"
    if readme.exists():
        content = readme.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"#\s+.+?:\s+(.+)", content)
        if m: name = m.group(1).strip()
    
    # Discovery  Scan src folder instead of blindly grabbing README stubs
    src_dir = build_path / "src"
    modules = []
    if src_dir.exists():
        # Priority on clean names from our newly synthesized Python files
        for f in src_dir.glob("*.py"):
            if f.name in ["__init__.py", "domain_intel.py", "shadow_cli.py"]: continue
            # Primary cleaning: osint-breach-finder-v9_0.py -> Breach Finder
            n = f.stem.lower()
            n = n.replace("osint-", "")
            # More aggressive version stripping (handles v9.0, v9_0, v90, etc.)
            n = re.sub(r"[-_.]v?\d+([_.]\d+)*", "", n)
            # Remove any trailing junk or leftovers from previous agent runs
            n = n.replace(".py", "").replace("_py", "").replace("-py", "").replace(".", " ").replace("-", " ").replace("_", " ")
            n = n.strip(" `").title()
            if n: modules.append(n)
    
    # Fallback/Merge if README actually has something descriptive
    if not modules and readme.exists():
        content = readme.read_text(encoding="utf-8", errors="ignore")
        raw = [l.strip("- ").strip() for l in content.split("\n") if l.strip().startswith("- ") and len(l) > 5]
        # Filter out common paths
        modules = [x for x in raw if "/`" not in x and "src/" not in x]
        
    return name, sorted(modules)

def extract_vision_info(build_path):
    """Ищет CONCEPT_*.md во всех релевантных путях."""
    defaults = {
        "summary": "An autonomous intelligence platform built on NEXUS architecture.",
        "architecture": "Modular micro-agent pipeline with asynchronous data ingestion layers.",
        "risks": "Scalability at corpus >10k nodes. API rate-limit exposure.",
        "workflow": ["Initialize env", "Ingest data", "Classify & rank", "Export artifacts"],
        "found": False
    }
    search_paths = [
        build_path,
        build_path.parent,
        build_path.parent.parent,
        build_path.parent.parent / "SPEC"
    ]
    for path in search_paths:
        if not path.exists(): continue
        for f in path.glob("*CONCEPT_*.md"):
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                m_s = re.search(r"## 1\. Executive Summary\n(.*?)\n##", content, re.S)
                m_a = re.search(r"## 2\. Technical Architecture\n(.*?)\n##", content, re.S)
                m_r = re.search(r"## 4\. Adversarial Review.*?\n(.*?)\n---", content, re.S)
                m_w = re.findall(r"\*\*Phase \d+\*\*:\s*(.+)", content)
                if m_s: defaults["summary"] = m_s.group(1).strip()
                if m_a: defaults["architecture"] = m_a.group(1).strip()
                if m_r: defaults["risks"] = m_r.group(1).strip()
                if m_w: defaults["workflow"] = m_w
                defaults["found"] = True
                print(f"  [+] Vision loaded: {f.name}")
                break
            except Exception: continue
        if defaults["found"]: break
    return defaults

def read_brand_identity(build_path):
    brand_file = build_path / "BRAND_IDENTITY.json"
    if brand_file.exists():
        try:
            data = json.loads(brand_file.read_text(encoding="utf-8"))
            print(f"  [+] Brand: '{data.get('creative_name')}'")
            return data
        except Exception: pass
    return None

def get_names(folder_name, brand=None):
    if brand and brand.get("creative_name"):
        short = brand["creative_name"]
        slogan = brand.get("slogan", "")
        pitch = brand.get("sales_pitch", "")
        slug = short.upper().replace(" ", "-")
        return short, slug, slogan, pitch
    source = re.sub(r"(B\d{3}_|PROD_|TEST_|\d{8}_\d{6})", "", folder_name)
    source = re.sub(r"(LEGAL-DEVOPS|MASTER[-_]SYSTEM|NEXUS|LEGAL|DEVOPS)", "", source, flags=re.I)
    source = source.replace("_", " ").replace("-", " ").strip()
    words = [w for w in source.split() if len(w) > 2]
    short = " ".join(words[:3]).title() if words else "NEXUS Hub"
    return short, short.upper().replace(" ", "-"), "Autonomous intelligence platform.", "Next-gen OSINT & Legal-DevOps system."

def rename_build(build_path, slug):
    parent = build_path.parent
    m = re.match(r"(B\d{3})_", build_path.name)
    prefix = m.group(1) if m else "B001"
    new_name = f"{prefix}_{slug}"
    new_path = parent / new_name
    if new_path == build_path: return build_path
    try:
        if new_path.exists(): shutil.rmtree(new_path)
        result = build_path.rename(new_path)
        print(f"  [+] Renamed: {new_name}")
        return new_path
    except PermissionError:
        print(f"  [!] Rename skipped (file lock).")
        return build_path

def get_actual_github_url(slug):
    """Deterministic URL: GitHub Owner + Build Slug."""
    return f"https://github.com/Agent-8947/{slug}"

def generate_logo(build_path, short_name):
    try:
        from PIL import Image, ImageDraw, ImageFont
        W, H = 600, 600
        img = Image.new("RGB", (W, H), color=(8, 8, 8))
        draw = ImageDraw.Draw(img)
        
        # Red accent stripe (top) & bottom
        draw.rectangle([0, 0, W, 12], fill=(220, 30, 30))
        draw.rectangle([0, H-12, W, H], fill=(220, 30, 30))
        
        # --- SYMBOL GENERATION: Cyber-Eye / Tech Node ---
        cx, cy = W // 2, H // 2 - 40
        
        # 1. Outer Tech Diamond
        eye_w, eye_h = 240, 120
        pts = [
            (cx - eye_w//2, cy),
            (cx, cy - eye_h//2),
            (cx + eye_w//2, cy),
            (cx, cy + eye_h//2)
        ]
        draw.polygon(pts, outline=(255, 255, 255), width=10)
        
        # 2. Inner Red Iris
        r_iris = 42
        draw.ellipse([cx - r_iris, cy - r_iris, cx + r_iris, cy + r_iris], outline=(220, 30, 30), width=8)
        
        # 3. Core Node / Pupil
        r_core = 16
        draw.ellipse([cx - r_core, cy - r_core, cx + r_core, cy + r_core], fill=(220, 30, 30))
        
        # 4. Reticles / Radars (Intersecting lines)
        rl = 60 # line length outside
        draw.line([cx - eye_w//2 - rl, cy, cx - eye_w//2 + 10, cy], fill=(255, 255, 255), width=3)
        draw.line([cx + eye_w//2 - 10, cy, cx + eye_w//2 + rl, cy], fill=(255, 255, 255), width=3)
        draw.line([cx, cy - eye_h//2 - rl, cx, cy - eye_h//2 + 10], fill=(220, 30, 30), width=3)
        draw.line([cx, cy + eye_h//2 - 10, cx, cy + eye_h//2 + rl], fill=(220, 30, 30), width=3)

        # --- TEXT GENERATION ---
        try:
            font_main = ImageFont.truetype("arialbd.ttf", 46)
            font_sub = ImageFont.truetype("arial.ttf", 22)
        except:
            font_main = ImageFont.load_default(); font_sub = font_main

        name_str = short_name.upper()
        if hasattr(draw, "textbbox"):
            bb1 = draw.textbbox((0,0), name_str, font=font_main)
            tw1, th1 = bb1[2]-bb1[0], bb1[3]-bb1[1]
            draw.text(((W - tw1)//2, cy + 120), name_str, fill=(255,255,255), font=font_main)
            
            label = "NEXUS INTELLIGENCE FACTORY"
            bb2 = draw.textbbox((0,0), label, font=font_sub)
            tw2 = bb2[2]-bb2[0]
            draw.text(((W - tw2)//2, cy + 120 + th1 + 15), label, fill=(150,150,150), font=font_sub)
        else:
            # Fallback for older PIL
            draw.text((60, cy + 120), name_str, fill=(255,255,255), font=font_main)

        img.save(build_path / "logo.png")
        print("  [+] Symbolic logo generated.")
    except Exception as e:
        print(f"  [!] Logo generation error: {e}")

def generate_og_image(build_path, short_name):
    """Generate 1200x630 banner for Social Media previews."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        W, H = 1200, 630
        img = Image.new("RGB", (W, H), color=(8, 8, 8))
        draw = ImageDraw.Draw(img)
        
        # Red accents
        draw.rectangle([0, 0, W, 12], fill=(220, 30, 30))
        draw.rectangle([0, H-12, W, H], fill=(220, 30, 30))
        
        # Tech Symbol (Eye)
        cx, cy = W // 2, H // 2 - 40
        eye_w, eye_h = 400, 200
        pts = [(cx - eye_w//2, cy), (cx, cy - eye_h//2), (cx + eye_w//2, cy), (cx, cy + eye_h//2)]
        draw.polygon(pts, outline=(255, 255, 255), width=15)
        draw.ellipse([cx-70, cy-70, cx+70, cy+70], outline=(220, 30, 30), width=10)
        draw.ellipse([cx-25, cy-25, cx+25, cy+25], fill=(220, 30, 30))
        
        # Text
        try:
            f_main = ImageFont.truetype("arialbd.ttf", 80)
            f_sub = ImageFont.truetype("arial.ttf", 30)
        except:
            f_main = ImageFont.load_default(); f_sub = f_main

        name_str = short_name.upper()
        if hasattr(draw, "textbbox"):
            bb = draw.textbbox((0,0), name_str, font=f_main)
            tw = bb[2]-bb[0]
            draw.text(((W-tw)//2, cy + 150), name_str, fill=(255,255,255), font=f_main)
            
            label = "NEXUS INTELLIGENCE FACTORY // OSINT PIPELINE"
            bb2 = draw.textbbox((0,0), label, font=f_sub)
            tw2 = bb2[2]-bb2[0]
            draw.text(((W-tw2)//2, cy + 150 + 90), label, fill=(150,150,150), font=f_sub)
        
        img.save(build_path / "og-image.png")
        img.save(build_path / "landing" / "og-image.png")
        print("  [+] Wide OG-image generated (1200x630).")
    except Exception as e:
        print(f"  [!] OG-Image error: {e}")

def generate_pdf(build_path, short_name, slogan, vision):
    try:
        from fpdf import FPDF, XPos, YPos

        class PDF(FPDF):
            def header(self): pass
            def footer(self): pass

        pdf = PDF()
        pdf.set_auto_page_break(auto=False)

        # --- Page 1: Cover ---
        pdf.add_page()
        pdf.set_fill_color(8, 8, 8)
        pdf.rect(0, 0, 210, 297, 'F')
        # Red strip top
        pdf.set_fill_color(220, 30, 30)
        pdf.rect(0, 0, 210, 4, 'F')
        # Name big
        pdf.set_font("Helvetica", "B", 56)
        pdf.set_text_color(255, 255, 255)
        pdf.set_xy(15, 80)
        pdf.cell(0, 20, short_name.upper()[:12], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        # Slogan
        pdf.set_font("Helvetica", "", 14)
        pdf.set_text_color(150, 150, 150)
        pdf.set_xy(15, 115)
        pdf.multi_cell(180, 7, slogan)
        # Date + agent
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(80, 80, 80)
        pdf.set_xy(15, 270)
        pdf.cell(0, 6, f"NEXUS Intelligence Factory  |  Agent 13 V5.0  |  {datetime.now().strftime('%Y-%m-%d')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        # Red strip bottom
        pdf.set_fill_color(220, 30, 30)
        pdf.rect(0, 293, 210, 4, 'F')

        # --- Page 2: Summary in English ---
        pdf.add_page()
        pdf.set_fill_color(8, 8, 8)
        pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_fill_color(220, 30, 30)
        pdf.rect(0, 0, 210, 4, 'F')

        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(220, 30, 30)
        pdf.set_xy(15, 20)
        pdf.cell(0, 6, "01 / EXECUTIVE OVERVIEW", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font("Helvetica", "B", 28)
        pdf.set_text_color(255, 255, 255)
        pdf.set_xy(15, 35)
        pdf.cell(0, 12, "What is it?", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Clean ascii summary
        summary_clean = vision["summary"].encode("ascii", errors="replace").decode("ascii")
        pdf.set_font("Helvetica", "", 12)
        pdf.set_text_color(200, 200, 200)
        pdf.set_xy(15, 60)
        pdf.multi_cell(180, 7, summary_clean or "An autonomous multi-layer intelligence pipeline. Designed to ingest, classify, and deliver structured OSINT findings without human intervention.")

        # Architecture block
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(220, 30, 30)
        pdf.set_xy(15, 130)
        pdf.cell(0, 6, "02 / SYSTEM ARCHITECTURE", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font("Helvetica", "B", 22)
        pdf.set_text_color(255, 255, 255)
        pdf.set_xy(15, 145)
        pdf.cell(0, 10, "How it works", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        arch_clean = vision["architecture"].encode("ascii", errors="replace").decode("ascii")
        pdf.set_font("Helvetica", "", 12)
        pdf.set_text_color(200, 200, 200)
        pdf.set_xy(15, 162)
        pdf.multi_cell(180, 7, arch_clean or "Modular micro-agent pipeline: Data Ingestion -> Classification Engine -> Output Interface. All layers operate asynchronously.")

        # Workflow
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(220, 30, 30)
        pdf.set_xy(15, 215)
        pdf.cell(0, 6, "03 / IMPLEMENTATION PHASES", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(200, 200, 200)
        y = 228
        for i, phase in enumerate(vision.get("workflow", [])[:4], 1):
            phase_clean = phase.encode("ascii", errors="replace").decode("ascii")
            pdf.set_xy(15, y)
            pdf.cell(0, 7, f"  {i:02d}.  {phase_clean}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            y += 9

        pdf.set_fill_color(220, 30, 30)
        pdf.rect(0, 293, 210, 4, 'F')

        pdf.output(str(build_path / "presentation.pdf"))
        print("  [+] PDF generated.")
    except Exception as e:
        print(f"  [!] PDF error: {e}")

def generate_landing(build_path, short_name, slogan, pitch, vision, modules, github_url):
    landing_dir = build_path / "landing"
    landing_dir.mkdir(exist_ok=True)

    brand = read_brand_identity(build_path)

    # Load human story from Agent 14
    story = brand.get("human_story", {}) if brand else {}

    def s(section, lang):
        return story.get(section, {}).get(lang, story.get(section, {}).get("en", ""))

    story_cards = [
        ("What is it?",        "Що це таке?",    "Что это такое?",       "what_it_is"),
        ("Who needs it?",      "Кому потрібно?", "Кому нужно?",          "who_needs_it"),
        ("How does it work?",  "Як працює?",     "Как работает?",        "how_it_works"),
        ("What do you get?",   "Що отримаєте?",  "Что вы получаете?",    "what_you_get"),
    ]

    story_html = ""
    for (title_en, title_ua, title_ru, key) in story_cards:
        en_text = s(key, "en")
        ua_text = s(key, "ua")
        ru_text = s(key, "ru")
        story_html += f"""<div class="st-card">
  <div class="st-title" data-en="{title_en}" data-ua="{title_ua}" data-ru="{title_ru}">{title_en}</div>
  <p class="st-body" data-en="{en_text}" data-ua="{ua_text}" data-ru="{ru_text}">{en_text}</p>
</div>\n"""

    # English defaults (clean)
    summary_en = "An autonomous multi-layer intelligence pipeline. Designed to ingest, classify, and deliver structured OSINT findings without human intervention."
    arch_en = "Modular micro-agent architecture with asynchronous data pipelines: Data Ingestion Buffer -> Logic Core -> Output Interface."

    modules_html = ""
    for i, m in enumerate(modules[:9], 1):
        modules_html += f'<div class="m-card"><span class="m-num">{i:02d}</span><p class="m-txt">{m}</p></div>\n'
    if not modules_html:
        for i, lab in enumerate(["Data Ingestion","Recon Engine","OSINT Layer","Legal Classifier","Audit Module","Export Pipeline"], 1):
            modules_html += f'<div class="m-card"><span class="m-num">{i:02d}</span><p class="m-txt">{lab}</p></div>\n'

    en_steps = [
        "Initialize environment & verify dependencies",
        "Prototype core analysis algorithms",
        "Test in isolated NEXUS WIKI circuit",
        "Release & integrate into main orchestrator"
    ]
    workflow_steps = vision.get("workflow", [])[:4]
    steps_html = ""
    for i in range(4):
        # Use the actual step text if available, else English default
        raw = workflow_steps[i] if i < len(workflow_steps) else ""
        label_ru = raw.strip() if raw.strip() else en_steps[i]
        label_en = en_steps[i]
        steps_html += (
            f'<div class="step">'
            f'<span class="step-n">{i+1:02d}</span>'
            f'<span class="step-t" data-en="{label_en}" data-ua="{label_en}" data-ru="{label_ru}">{label_en}</span>'
            f'</div>\n'
        )

    # Build "what to provide" section from Agent 14
    provide_data = brand.get("what_to_provide", {}) if brand else {}
    provide_title_en = provide_data.get("title", {}).get("en", "What you need to give the system")
    provide_title_ua = provide_data.get("title", {}).get("ua", "Що потрібно надати системі")
    provide_title_ru = provide_data.get("title", {}).get("ru", "Что нужно передать системе")
    provide_note_en = provide_data.get("note", {}).get("en", "")
    provide_note_ua = provide_data.get("note", {}).get("ua", "")
    provide_note_ru = provide_data.get("note", {}).get("ru", "")

    items_en = provide_data.get("items", {}).get("en", ["A name, domain, or email address"])
    items_ua = provide_data.get("items", {}).get("ua", items_en)
    items_ru = provide_data.get("items", {}).get("ru", items_en)

    provide_items_html = ""
    for i, (ie, iua, iru) in enumerate(zip(items_en, items_ua, items_ru)):
        provide_items_html += (
            f'<li class="p-item" data-en="{ie}" data-ua="{iua}" data-ru="{iru}">{ie}</li>\n'
        )

    # Build Deployment & Tech Stack
    dep_data = brand.get("deployment", {}) if brand else {}
    dep_where_en = dep_data.get("where", {}).get("en", "Runs locally.")
    dep_where_ua = dep_data.get("where", {}).get("ua", "Працює локально.")
    dep_where_ru = dep_data.get("where", {}).get("ru", "Работает локально.")
    
    dep_reqs = dep_data.get("requirements", [])
    reqs_html = "".join([f'<li class="d-req">{r}</li>\n' for r in dep_reqs])

    tech_data = brand.get("tech_stack", {}) if brand else {}
    tech_label_en = tech_data.get("label", {}).get("en", "Open-source repositories powering this tool")
    tech_label_ua = tech_data.get("label", {}).get("ua", "Відкриті репозиторії інструменту")
    tech_label_ru = tech_data.get("label", {}).get("ru", "Открытые репозитории инструмента")

    repos = tech_data.get("repos", [])
    repos_html = ""
    for r in repos:
        repos_html += f"""<div class="repo-card">
  <div class="repo-name">{r.get('name', '')}</div>
  <div class="repo-url">{r.get('url', '')}</div>
  <div class="repo-desc">{r.get('desc', '')}</div>
</div>\n"""


    # Meta pitch (for OG tags) - prioritize a human-friendly story
    og_pitch = pitch
    if brand and "human_story" in brand:
        og_pitch = brand["human_story"].get("what_it_is", {}).get("en", pitch)

    # Build build_slug for meta tags
    build_slug = build_path.name.lower().replace('_', '-')
    v_url = f"https://{build_slug}.vercel.app"

    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{short_name} | NEXUS</title>
<meta name="description" content="{og_pitch}">

<!-- Open Graph / Meta -->
<meta property="og:type" content="website">
<meta property="og:url" content="{v_url}">
<meta property="og:title" content="{short_name} | NEXUS Intelligence">
<meta property="og:description" content="{og_pitch}">
<meta property="og:image" content="{v_url}/og-image.png">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="{v_url}">
<meta property="twitter:title" content="{short_name} | NEXUS Intelligence">
<meta property="twitter:description" content="{og_pitch}">
<meta property="twitter:image" content="{v_url}/og-image.png">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;700&family=Space+Mono&family=Noto+Sans:wght@400;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
:root {{
  --red: #DC1E1E;
  --black: #080808;
  --white: #F5F5F0;
  --grey: #999;
  --line: #222;
}
html {scroll-behavior:smooth;}
body {background:var(--black);color:var(--white);font-family:'Space Grotesk','Noto Sans',sans-serif;line-height:1.5;overflow-x:hidden;}

/* NAV */
nav {{
  padding:30px 6%;display:flex;justify-content:space-between;
  align-items:center;border-bottom:1px solid var(--line);
}
.n-logo {{font-weight:700;font-size:.85rem;letter-spacing:4px;color:var(--white);}
.n-right {{ display:flex; gap:20px; align-items:center; }
.n-gh {{ color:var(--white); transition:.2s; display:flex; align-items:center; }
.n-gh:hover {{ color:var(--red); }
.n-lang {{display:flex;gap:0;border:1px solid var(--line);}
.l-btn {{
  background:none;border:none;color:var(--grey);
  padding:8px 14px;cursor:pointer;font-family:inherit;
  font-size:.75rem;letter-spacing:2px;transition:.2s;
}
.l-btn.on,.l-btn:hover{{background:var(--red);color:var(--white);}

/* HERO */
.hero {{
  min-height:100vh;display:grid;
  grid-template-rows:1fr auto;
  padding:120px 6% 60px;
  border-bottom:1px solid var(--line);
}
.hero-top {{display:flex;flex-direction:column;justify-content:flex-end;}
.h-tag {{font-size:.7rem;letter-spacing:4px;color:var(--red);font-weight:500;margin-bottom:24px;font-family:'Space Mono',monospace;}
.h-title {{
  font-size:clamp(4rem,12vw,10rem);font-weight:700;
  line-height:1;margin-bottom:20px;letter-spacing:-2px;
}
.hero-bottom {{display:flex;justify-content:space-between;align-items:flex-end;}
.h-slogan {{font-size:1.1rem;color:var(--grey);max-width:400px;line-height:1.6;}
.h-scroll {{
  font-family:'Space Mono',monospace;font-size:.7rem;
  letter-spacing:3px;color:var(--white);text-transform:uppercase;
}

/* SECTION */
.section {{padding:120px 6%;border-bottom:1px solid var(--line);}
.s-label {{
  font-family:'Space Mono',monospace;font-size:.7rem;
  letter-spacing:3px;color:var(--red);margin-bottom:60px;
  text-transform:uppercase;
}

/* STORY */
.st-grid {{ display:grid;grid-template-columns:1fr 1fr;gap:0; }
.st-card {{
  padding:50px 40px;border:1px solid var(--line);
  transition:.3s;
}
.st-card:hover{{border-color:var(--red);background:rgba(220,30,30,.04);}
.st-title {{
  font-family:'Space Mono',monospace;font-size:.7rem;
  letter-spacing:3px;color:var(--red);text-transform:uppercase;
  margin-bottom:20px;
}
.st-body {{font-size:1.05rem;color:var(--grey);line-height:1.7;}

/* PROVIDE  What to give the system */
.provide-box {{
  display:grid;grid-template-columns:1fr 1fr;gap:0;
  border:1px solid var(--red);
}
.provide-left {{
  padding:50px 40px;
  border-right:1px solid var(--red);
}
.provide-right {{ padding:50px 40px; }
.p-heading {{
  font-size:clamp(1.5rem,3vw,2.5rem);font-weight:700;
  line-height:1.1;margin-bottom:8px;
}
.p-sub {{
  font-size:.85rem;color:var(--grey);margin-bottom:40px;
}
.p-list {{ list-style:none;display:flex;flex-direction:column;gap:16px; }
.p-item {{
  display:flex;align-items:flex-start;gap:16px;
  font-size:1rem;color:var(--white);line-height:1.5;
}
.p-item::before {{
  content:'';color:var(--red);font-family:'Space Mono',monospace;
  font-size:.9rem;flex-shrink:0;margin-top:2px;
}
.p-note {{
  margin-top:30px;padding:20px;border:1px solid var(--line);
  font-size:.85rem;color:var(--grey);font-style:italic;
}

/* DEPLOYMENT & TECH STACK */
.d-box {{ border:1px solid var(--line); padding:40px; }
.d-where {{ font-size:1.1rem; color:var(--white); margin-bottom:20px; line-height:1.6; border-left:3px solid var(--red); padding-left:20px; }
.d-reqs {{ list-style:none; display:flex; gap:12px; flex-wrap:wrap; }
.d-req {{ background:rgba(255,255,255,0.03); padding:8px 16px; font-size:.85rem; border:1px solid var(--line); color:var(--grey); }

.repo-grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(300px, 1fr)); gap:20px; }
.repo-card {{ border:1px solid var(--line); padding:30px; transition:0.3s; }
.repo-card:hover {{ border-color:var(--red); background:rgba(220,30,30,0.03); }
.repo-name {{ font-size:1.2rem; font-weight:700; color:var(--white); margin-bottom:8px; }
.repo-url {{ font-family:'Space Mono',monospace; font-size:.75rem; color:var(--red); margin-bottom:12px; }
.repo-desc {{ font-size:.95rem; color:var(--grey); line-height:1.5; }

/* MODULES */
.m-grid {{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:0;
}
.m-card {{
  padding:40px 30px;border:1px solid var(--line);
  position:relative;transition:.3s;cursor:default;
}
.m-card:hover{{background:rgba(220,30,30,.06);border-color:var(--red);}
.m-num {{
  font-family:'Space Mono',monospace;font-size:.65rem;
  color:var(--red);letter-spacing:2px;display:block;margin-bottom:12px;
}
.m-txt {{font-size:.95rem;color:var(--grey);}

/* WORKFLOW */
.steps {{display:flex;gap:0;flex-wrap:wrap;}
.step {{
  flex:1;min-width:200px;padding:40px 30px;border:1px solid var(--line);
  position:relative;transition:.3s;
}
.step:hover{{border-color:var(--red);background:rgba(255,255,255,.02);}
.step-n {{
  font-family:'Space Mono',monospace;font-size:2.5rem;
  font-weight:700;color:var(--line);display:block;margin-bottom:16px;
}
.step-t {{font-size:1rem;color:var(--grey);}

/* PDF CTA */
.cta-bar {{
  display:flex;justify-content:space-between;align-items:center;
  padding:60px 6%;border-bottom:1px solid var(--line);
  flex-wrap:wrap;gap:30px;
}
.cta-text {{font-size:clamp(1.5rem,4vw,3rem);font-weight:700;}
.cta-btn {{
  display:inline-block;padding:18px 48px;
  background:var(--red);color:var(--white);
  text-decoration:none;font-weight:700;
  letter-spacing:2px;font-size:.85rem;
  border:1px solid var(--red);transition:.3s;
}
.cta-btn:hover{{background:transparent;color:var(--red);}

/* FOOTER */
footer {{
  padding:40px 6%;display:flex;
  justify-content:space-between;align-items:center;
  flex-wrap:wrap;gap:10px;
}
.f-left {{font-size:.7rem;letter-spacing:2px;color:var(--grey);font-family:'Space Mono',monospace;}
.f-right {{font-size:.7rem;color:var(--line);}

/* red stripe */
.stripe {{height:4px;background:var(--red);}

@media(max-width:768px){{
  .about-grid{grid-template-columns:1fr;gap:40px;}
  .m-grid{grid-template-columns:1fr;}
}}
</style>
</head>
<body>
<div class="stripe"></div>

<nav>
  <div class="n-logo">NEXUS / 13</div>
  <div class="n-right">
    <a href="{github_url}" target="_blank" class="n-gh" title="View Source on GitHub">
      <svg height="24" aria-hidden="true" viewBox="0 0 16 16" version="1.1" width="24" fill="currentColor">
        <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
      </svg>
    </a>
    <div class="n-lang">
      <button class="l-btn on" onclick="setL('en',this)">EN</button>
      <button class="l-btn" onclick="setL('ua',this)">UA</button>
      <button class="l-btn" onclick="setL('ru',this)">RU</button>
    </div>
  </div>
</nav>

<!-- HERO -->
<section class="hero">
  <div class="hero-top">
    <div class="h-tag" id="tag" data-en="NEXUS INTELLIGENCE SYSTEM" data-ua="NEXUS СИСТЕМА РОЗВІДКИ" data-ru="NEXUS СИСТЕМА РАЗВЕДКИ">NEXUS INTELLIGENCE SYSTEM</div>
    <h1 class="h-title">{short_name}</h1>
  </div>
  <div class="hero-bottom">
    <p class="h-slogan" id="slogan" data-en="{slogan}" data-ua="Автономна фабрика розвідки. Збирає. Аналізує. Доставляє." data-ru="Автономная фабрика разведки. Собирает. Анализирует. Доставляет.">{slogan}</p>
    <span class="h-scroll">SCROLL </span>
  </div>
</section>

<!-- STORY: Simple explanation (by Agent 14) -->
<section class="section" id="story">
  <div class="s-label">00  IN SIMPLE TERMS</div>
  <div class="st-grid">
    {story_html}
  </div>
</section>

<!-- PROVIDE: What to give the system (by Agent 14) -->
<section class="section" id="provide">
  <div class="s-label" id="provide-label"
       data-en="START HERE  WHAT YOU NEED TO PROVIDE"
       data-ua="З ЧОГО ПОЧАТИ  ЩО ПОТРІБНО НАДАТИ"
       data-ru="С ЧЕГО НАЧАТЬ  ЧТО НУЖНО ПЕРЕДАТЬ">
    START HERE  WHAT YOU NEED TO PROVIDE
  </div>
  <div class="provide-box">
    <div class="provide-left">
      <h2 class="p-heading" id="p-heading"
          data-en="{provide_title_en}"
          data-ua="{provide_title_ua}"
          data-ru="{provide_title_ru}">{provide_title_en}</h2>
      <p class="p-sub" id="p-note"
         data-en="{provide_note_en}"
         data-ua="{provide_note_ua}"
         data-ru="{provide_note_ru}">{provide_note_en}</p>
    </div>
    <div class="provide-right">
      <ul class="p-list">
        {provide_items_html}
      </ul>
    </div>
  </div>
</section>

<!-- ABOUT -->
<section class="section" id="about">
  <div class="s-label">01  ABOUT THE SYSTEM</div>
  <div class="about-grid">
    <div>
      <h2 class="a-title" id="atitle" data-en="What is it?" data-ua="Що це таке?" data-ru="Что это такое?">What is it?</h2>
      <div class="a-tag" id="atag" data-en="AUTONOMOUS // 24/7" data-ua="АВТОНОМНО // 24/7" data-ru="АВТОНОМНО // 24/7">AUTONOMOUS // 24/7</div>
    </div>
    <div>
      <p class="a-body" id="summary"
         data-en="{summary_en}"
         data-ua="Автономна платформа збору та аналізу розвідувальних даних. Побудована на архітектурі NEXUS з модульними конвейерами."
         data-ru="Автономная платформа сбора и анализа разведывательных данных. Построена на архитектуре NEXUS с модульными конвейерами обработки данных.">{summary_en}</p>
    </div>
  </div>
</section>

<!-- ARCHITECTURE -->
<section class="section" id="arch">
  <div class="s-label">02  ARCHITECTURE</div>
  <div class="about-grid">
    <div>
      <h2 class="a-title" id="archtitle" data-en="How it works" data-ua="Як це працює" data-ru="Как это работает">How it works</h2>
    </div>
    <div>
      <p class="a-body" id="archbody"
         data-en="{arch_en}"
         data-ua="Модульна архітектура мікроагентів з асинхронними конвейерами: Ingestion  Classification  Output."
         data-ru="Модульная архитектура микроагентов с асинхронными конвейерами: Ingestion  Classification  Output.">{arch_en}</p>
    </div>
  </div>
</section>

<!-- WORKFLOW -->
<section class="section" id="workflow">
  <div class="s-label">03  IMPLEMENTATION PHASES</div>
  <div class="steps">
    {steps_html}
  </div>
</section>

<!-- MODULES -->
<section class="section" id="modules">
  <div class="s-label">04  SYSTEM MODULES</div>
  <div class="m-grid">
    {modules_html}
  </div>
</section>

<!-- DEPLOYMENT -->
<section class="section" id="deploy">
  <div class="s-label">05  DEPLOYMENT & REQUIREMENTS</div>
  <div class="d-box">
    <div class="d-where" data-en="{dep_where_en}" data-ua="{dep_where_ua}" data-ru="{dep_where_ru}">{dep_where_en}</div>
    <ul class="d-reqs">
      {reqs_html}
    </ul>
  </div>
</section>

<!-- TECH STACK -->
<section class="section" id="stack">
  <div class="s-label" data-en="06  {tech_label_en}" data-ua="06  {tech_label_ua}" data-ru="06  {tech_label_ru}">06  {tech_label_en}</div>
  <div class="repo-grid">
    {repos_html}
  </div>
</section>

<footer>
  <span class="f-left">NEXUS INTELLIGENCE FACTORY / AGENT 13 V5.0 / {cur_year}</span>
  <span class="f-right">Co-authored by Agent 09 & Agent 14</span>
</footer>

<div class="stripe"></div>

<script>
function setL(l, btn) {{
  document.querySelectorAll('.l-btn').forEach(b=>b.classList.remove('on'));
  btn.classList.add('on');
  document.querySelectorAll('[data-'+l+']').forEach(el=>{{
    el.textContent = el.getAttribute('data-'+l);
  }} );
}
</script>
</body>
</html>"""

    build_slug = build_path.name.lower().replace('_', '-')
    v_url = f"https://{build_slug}.vercel.app"
    logo_abs_url = f"{v_url}/logo.png"

    # Inject dynamic content via safe .replace() to avoid CSS brace collisions
    placeholders = {
        "short_name": short_name, "slogan": slogan, "pitch": pitch, "og_pitch": og_pitch,
        "github_url": github_url, "v_url": v_url, "logo_url": logo_abs_url,
        "summary_en": summary_en, "arch_en": arch_en,
        "steps_html": steps_html, "modules_html": modules_html, "repos_html": repos_html,
        "reqs_html": reqs_html, "story_html": story_html,
        "dep_where_en": dep_where_en, "dep_where_ua": dep_where_ua, "dep_where_ru": dep_where_ru,
        "tech_label_en": tech_label_en, "tech_label_ua": tech_label_ua, "tech_label_ru": tech_label_ru,
        "provide_title_en": provide_title_en, "provide_title_ua": provide_title_ua, "provide_title_ru": provide_title_ru,
        "provide_note_en": provide_note_en, "provide_note_ua": provide_note_ua, "provide_note_ru": provide_note_ru,
        "provide_items_html": provide_items_html,
        "cur_year": datetime.now().strftime('%Y')
    }
    for key, val in placeholders.items():
        html = html.replace("{" + key + "}", str(val))

    # Fix CSS syntax from legacy format() artifacts
    html = html.replace("{{", "{").replace("}}", "}")

    (landing_dir / "index.html").write_text(html, encoding="utf-8")
    print("  [+] Landing generated. (EN/UA/RU)")

def main():
    banner()
    build_path = find_latest_build()
    if not build_path: print("No build found."); sys.exit(1)

    name, modules = extract_product_info(build_path)
    vision = extract_vision_info(build_path)
    brand = read_brand_identity(build_path)
    short_name, slug, slogan, pitch = get_names(build_path.name, brand)

    build_path = rename_build(build_path, slug)
    github_url = get_actual_github_url(build_path.name)
    generate_logo(build_path, short_name)
    generate_og_image(build_path, short_name)
    generate_pdf(build_path, short_name, slogan, vision)
    generate_landing(build_path, short_name, slogan, pitch, vision, modules, github_url)
    print(f"\n[DONE] {build_path.name}")
    print("   logo.png | presentation.pdf | landing/index.html (EN/UA/RU)")

if __name__ == "__main__":
    main()
