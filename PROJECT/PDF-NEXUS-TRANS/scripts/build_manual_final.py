"""
NEXUS MANUAL BUILDER v4.0
Builds a clean, image-rich, clearly structured HTML manual.
Auto-places all images from PDF extraction alongside translated text blocks.
Images are sorted by page, then by xref order.
"""
import os, json, re, sys

def img_size_ok(path, min_bytes=5000):
    try: return os.path.getsize(path) >= min_bytes
    except: return False

def get_page_imgs(img_dir, page_num):
    """Return all images for a given page number, sorted by xref."""
    imgs = []
    prefix = f"img_p{page_num}_"
    for f in sorted(os.listdir(img_dir)):
        if f.startswith(prefix) and f.endswith(".png"):
            full = os.path.join(img_dir, f)
            if img_size_ok(full, 5000):
                imgs.append(f"images/{f}")
    return imgs

def ru(block):
    return (block.get("ru_text") or block.get("en_text") or "").strip()

def is_heading(text, fs):
    return fs >= 15 or ("глава" in text.lower()) or ("раздел" in text.lower())

def is_warning(text):
    t = text.lower()
    return any(w in t for w in ["предупреждение","warning","осторожно","caution"])

def is_note(text):
    t = text.lower()
    return "внимание" in t or "важно" in t or "note" in t

def build_manual(json_path, img_dir, out_path, title, model, accent, pages_total):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    # CSS
    css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root {{
  --accent: {accent};
  --accent-light: {accent}18;
  --bg: #FFFFFF;
  --sidebar: #111317;
  --black: #18191C;
  --gray-text: #555;
  --gray-border: #E8E9EC;
  --gray-bg: #F7F8FA;
  --danger-bg: #FFF4F4;
  --danger-border: #E74C3C;
  --warn-bg: #FFFBF0;
  --warn-border: #F39C12;
  --note-bg: #F0F7FF;
  --note-border: #3498DB;
  --font: 'Inter', system-ui, sans-serif;
  --font-head: 'Space Grotesk', system-ui, sans-serif;
  --radius: 10px;
  --shadow: 0 2px 12px rgba(0,0,0,0.08);
}}
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ scroll-behavior: smooth; }}
body {{ font-family: var(--font); background: var(--gray-bg); color: var(--black); display: flex; }}

/* Sidebar */
aside {{
  width: 260px; min-width: 260px; height: 100vh; position: sticky; top: 0;
  background: var(--sidebar); overflow-y: auto; display: flex; flex-direction: column;
  flex-shrink: 0;
}}
.sb-brand {{
  padding: 28px 24px 20px;
  border-bottom: 1px solid rgba(255,255,255,0.07);
}}
.sb-brand .sb-tag {{
  color: var(--accent);
  font-size: 10px; letter-spacing: 3px; text-transform: uppercase;
  font-family: var(--font-head); margin-bottom: 6px;
}}
.sb-brand .sb-model {{
  color: #fff; font-family: var(--font-head);
  font-size: 20px; font-weight: 700; line-height: 1.2;
}}
nav {{ flex: 1; padding: 16px 0; overflow-y: auto; }}
nav a {{
  display: block; padding: 10px 24px;
  color: rgba(255,255,255,0.55); text-decoration: none;
  font-size: 13px; font-weight: 500;
  border-left: 3px solid transparent;
  transition: all 0.15s;
}}
nav a:hover, nav a.on {{
  color: #fff;
  border-left-color: var(--accent);
  background: rgba(255,255,255,0.05);
}}
.nav-section-label {{
  padding: 20px 24px 6px;
  color: rgba(255,255,255,0.25);
  font-size: 9px; letter-spacing: 3px; text-transform: uppercase;
}}
.sb-foot {{
  padding: 16px 24px; border-top: 1px solid rgba(255,255,255,0.07);
  color: rgba(255,255,255,0.2); font-size: 10px; line-height: 1.6;
}}

/* Main */
main {{ flex: 1; overflow-x: hidden; }}

/* Cover */
.cover {{
  background: var(--sidebar);
  min-height: 100vh; display: flex; flex-direction: column;
  position: relative;
}}
.cover-stripe {{ height: 6px; background: var(--accent); }}
.cover-body {{ flex: 1; padding: 80px 64px; display: flex; flex-direction: column; justify-content: flex-end; }}
.cover-kicker {{
  font-family: var(--font-head);
  font-size: 11px; letter-spacing: 4px;
  text-transform: uppercase; color: var(--accent);
  margin-bottom: 16px;
}}
.cover-h1 {{
  font-family: var(--font-head);
  font-size: clamp(48px, 8vw, 80px);
  font-weight: 700; color: #fff;
  line-height: 1.05; margin-bottom: 24px;
}}
.cover-desc {{ font-size: 17px; color: rgba(255,255,255,0.5); max-width: 440px; line-height: 1.7; }}
.cover-chips {{
  padding: 40px 64px;
  display: flex; gap: 40px; flex-wrap: wrap;
  border-top: 1px solid rgba(255,255,255,0.08);
}}
.chip .chip-label {{ font-size: 10px; letter-spacing: 2px; text-transform: uppercase; color: rgba(255,255,255,0.3); margin-bottom: 4px; }}
.chip .chip-val {{ font-family: var(--font-head); font-size: 16px; font-weight: 600; color: #fff; }}

/* Content blocks */
.content-block {{
  background: var(--bg);
  margin: 24px 32px;
  border-radius: 16px;
  border: 1px solid var(--gray-border);
  box-shadow: var(--shadow);
  overflow: hidden;
}}
.block-header {{
  padding: 28px 36px 20px;
  border-bottom: 1px solid var(--gray-border);
  display: flex; align-items: center; gap: 12px;
}}
.block-num {{
  font-family: var(--font-head);
  font-size: 11px; font-weight: 700;
  letter-spacing: 2px; text-transform: uppercase;
  color: var(--accent);
  background: var(--accent-light);
  padding: 4px 10px; border-radius: 20px;
}}
.block-title {{
  font-family: var(--font-head);
  font-size: 22px; font-weight: 700; color: var(--black);
}}
.block-body {{ padding: 28px 36px; }}

/* Typography */
.t-body {{ font-size: 15px; color: var(--gray-text); line-height: 1.8; margin-bottom: 14px; }}
h3.t-sub {{
  font-family: var(--font-head); font-size: 15px; font-weight: 600;
  color: var(--black); margin: 28px 0 12px;
  padding-left: 12px; border-left: 3px solid var(--accent);
}}

/* Lists */
.t-list {{ list-style: none; margin: 8px 0 16px; }}
.t-list li {{
  font-size: 14px; color: var(--gray-text);
  padding: 9px 0 9px 20px; position: relative;
  border-bottom: 1px solid var(--gray-border);
}}
.t-list li:last-child {{ border-bottom: none; }}
.t-list li::before {{ content: '›'; position: absolute; left: 0; color: var(--accent); font-size: 18px; line-height: 1; top: 8px; }}
.t-list li strong {{ color: var(--black); }}

.steps {{ list-style: none; counter-reset: step; margin: 8px 0 16px; }}
.steps li {{
  counter-increment: step;
  padding: 14px 16px 14px 60px;
  position: relative; font-size: 14px; color: var(--gray-text);
  border-bottom: 1px solid var(--gray-border);
}}
.steps li:last-child {{ border-bottom: none; }}
.steps li::before {{
  content: counter(step);
  position: absolute; left: 16px; top: 50%; transform: translateY(-50%);
  width: 30px; height: 30px;
  background: var(--accent); color: #fff;
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  font-family: var(--font-head); font-size: 13px; font-weight: 700;
  line-height: 30px; text-align: center;
}}

/* Alerts */
.alert {{
  background: var(--warn-bg); border: 1px solid var(--warn-border);
  border-left: 5px solid var(--warn-border);
  border-radius: var(--radius); padding: 16px 20px;
  margin: 16px 0; display: flex; gap: 14px; align-items: flex-start;
}}
.alert.danger {{ background: var(--danger-bg); border-color: var(--danger-border); border-left-color: var(--danger-border); }}
.alert.note {{ background: var(--note-bg); border-color: var(--note-border); border-left-color: var(--note-border); }}
.alert-icon {{ font-size: 22px; flex-shrink: 0; line-height: 1.4; }}
.alert-text .alert-head {{ font-family: var(--font-head); font-size: 13px; font-weight: 700; margin-bottom: 4px; }}
.alert.danger .alert-head {{ color: var(--danger-border); }}
.alert.note .alert-head {{ color: var(--note-border); }}
.alert-text p {{ font-size: 14px; color: var(--gray-text); margin: 0; }}

/* Images */
.img-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin: 24px 0; }}
.img-card {{
  border: 1px solid var(--gray-border); border-radius: var(--radius);
  overflow: hidden; background: #fff;
}}
.img-card img {{
  width: 100%; display: block; cursor: zoom-in;
  transition: transform 0.3s;
}}
.img-card img:hover {{ transform: scale(1.02); }}
.img-card .img-cap {{
  padding: 8px 12px; font-size: 11px; color: rgba(0,0,0,0.35);
  letter-spacing: 1px; text-transform: uppercase;
  border-top: 1px solid var(--gray-border);
}}

/* Specs grid */
.spec-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin: 16px 0; }}
.spec-card {{
  background: var(--gray-bg); border: 1px solid var(--gray-border);
  border-radius: var(--radius); padding: 16px 20px;
}}
.spec-card .sc-label {{ font-size: 11px; letter-spacing: 1px; text-transform: uppercase; color: rgba(0,0,0,0.35); margin-bottom: 6px; }}
.spec-card .sc-value {{ font-family: var(--font-head); font-size: 18px; font-weight: 600; color: var(--black); }}

/* Fault table */
.fault-table {{ width: 100%; border-collapse: collapse; font-size: 14px; margin: 16px 0; }}
.fault-table th {{
  background: var(--black); color: #fff; text-align: left;
  padding: 12px 16px; font-family: var(--font-head); font-size: 11px;
  letter-spacing: 2px; text-transform: uppercase;
}}
.fault-table th:first-child {{ background: var(--accent); color: #fff; width: 180px; }}
.fault-table td {{ padding: 14px 16px; vertical-align: top; border-bottom: 1px solid var(--gray-border); }}
.fault-table td:first-child {{ font-family: var(--font-head); font-weight: 600; color: var(--accent); }}
.fault-table ol {{ padding-left: 18px; }}
.fault-table li {{ margin-bottom: 6px; color: var(--gray-text); }}

/* Temp table */
.temp-table {{ width: 100%; border-collapse: collapse; font-size: 14px; margin: 16px 0; border-radius: var(--radius); overflow: hidden; }}
.temp-table th {{ background: var(--accent); color: #fff; padding: 11px 16px; font-family: var(--font-head); font-size: 11px; letter-spacing: 1px; text-transform: uppercase; }}
.temp-table td {{ padding: 11px 16px; border-bottom: 1px solid var(--gray-border); }}
.temp-table td:first-child {{ font-weight: 600; }}

/* Lightbox */
#lb {{ display: none; position: fixed; inset: 0; z-index: 9999; background: rgba(0,0,0,0.92); justify-content: center; align-items: center; cursor: zoom-out; }}
#lb.show {{ display: flex; }}
#lb img {{ max-width: 92vw; max-height: 92vh; border-radius: 8px; }}

/* Responsive */
@media (max-width: 768px) {{
  body {{ flex-direction: column; }}
  aside {{ width: 100%; height: auto; position: relative; }}
  .cover-body {{ padding: 40px 24px; }}
  .cover-chips {{ padding: 24px; gap: 20px; }}
  .content-block {{ margin: 12px; }}
  .block-body {{ padding: 20px; }}
  .img-grid {{ grid-template-columns: 1fr; }}
}}
@media print {{
  aside {{ display: none; }}
  .cover {{ page-break-after: always; }}
  .content-block {{ break-inside: avoid; box-shadow: none; border: 1px solid #ddd; }}
  #lb {{ display: none !important; }}
}}
</style>"""

    # JS
    js = """
<script>
const links = document.querySelectorAll('nav a[data-id]');
const blocks = document.querySelectorAll('[data-block]');
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      links.forEach(l => l.classList.toggle('on', l.dataset.id === e.target.dataset.block));
    }
  });
}, {threshold: 0.1, rootMargin: '-20% 0px -70% 0px'});
blocks.forEach(b => observer.observe(b));

function zoom(src) {
  document.getElementById('lb-img').src = src;
  document.getElementById('lb').classList.add('show');
}
document.getElementById('lb').addEventListener('click', () => document.getElementById('lb').classList.remove('show'));
</script>"""

    # NAV links placeholder
    nav_items = []

    # Build pages — group by logical section
    # Key pages for K10: 0=cover, 1=title, 2=contents, 3-5=safety, 5=specs, 6-7=interface, 8-9=switches/sensors, 10-11=probe/powder, 12=purifier/film, 13-14=maintenance/trouble, 15=service
    # The structure: we put all images AFTER the text block of their page

    sections = []
    block_id = 0

    for page_str in sorted(data.keys(), key=lambda x: int(x)):
        page_num = int(page_str)
        blocks_raw = data.get(page_str, [])
        if not blocks_raw:
            continue

        # Collect text
        texts = []
        for b in sorted(blocks_raw, key=lambda x: x["bbox"][1]):
            t = ru(b)
            if not t or re.match(r'Стр\.\s*\d+', t):
                continue
            texts.append({"text": t, "fs": b["font_size"]})

        # Collect images for this page
        page_imgs = get_page_imgs(img_dir, page_num)

        if not texts and not page_imgs:
            continue

        sections.append({
            "page": page_num,
            "id": f"page-{page_num}",
            "texts": texts,
            "imgs": page_imgs
        })
        block_id += 1

    # Render HTML
    html_parts = []
    html_parts.append(f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
{css}
</head>
<body>
<div id="lb"><img id="lb-img" src="" alt=""></div>
""")

    # SIDEBAR
    aside = f"""<aside>
<div class="sb-brand">
  <div class="sb-tag">Audley · Руководство</div>
  <div class="sb-model">{model}</div>
</div>
<nav>
  <div class="nav-section-label">Навигация</div>"""

    for s in sections:
        # Find best label
        label = f"Стр. {s['page']+1}"
        for t in s["texts"]:
            tx = t["text"]
            if any(w in tx.lower() for w in ["безопасность","параметры","интерфейс","установк","обслуживан","неисправ","программ","температур","порошок","очистит","схема","сервис","введение","содержание","глава"]):
                label = tx[:38] + ("…" if len(tx) > 38 else "")
                break
            elif t["fs"] >= 14 and len(tx) < 50:
                label = tx[:38] + ("…" if len(tx) > 38 else "")
                break
        aside += f'\n  <a href="#{s["id"]}" data-id="{s["id"]}">{label}</a>'

    aside += """
</nav>
<div class="sb-foot">Henan Audley Digital Co., Ltd.<br>© NEXUS Translation Engine</div>
</aside>"""

    html_parts.append(aside)
    html_parts.append("<main>")

    # COVER
    html_parts.append(f"""
<section class="cover" id="cover">
  <div class="cover-stripe"></div>
  <div class="cover-body">
    <div class="cover-kicker">Руководство по эксплуатации</div>
    <h1 class="cover-h1">{title}</h1>
    <p class="cover-desc">Полное руководство по установке, эксплуатации и обслуживанию оборудования {model}.</p>
  </div>
  <div class="cover-chips">
    <div class="chip"><div class="chip-label">Модель</div><div class="chip-val">{model}</div></div>
    <div class="chip"><div class="chip-label">Страниц</div><div class="chip-val">{pages_total}</div></div>
    <div class="chip"><div class="chip-label">Производитель</div><div class="chip-val">AUDLEY DIGITAL</div></div>
  </div>
</section>""")

    block_counter = 0
    for s in sections:
        block_counter += 1
        page = s["page"]
        bid = s["id"]
        texts = s["texts"]
        imgs = s["imgs"]

        # Find primary title
        page_title = f"Стр. {page+1}"
        for t in texts:
            if t["fs"] >= 14 and len(t["text"]) < 60:
                page_title = t["text"]
                break

        block_num_str = f"{block_counter:02d}"
        html_parts.append(f'\n<div class="content-block" id="{bid}" data-block="{bid}">')
        html_parts.append(f'''
<div class="block-header">
  <span class="block-num">Стр. {page+1}</span>
  <span class="block-title">{page_title}</span>
</div>
<div class="block-body">''')

        # Render text
        in_list = False
        list_items = []

        def flush_list():
            nonlocal in_list, list_items
            if list_items:
                html_parts.append('<ul class="t-list">')
                for li in list_items:
                    html_parts.append(f"<li>{li}</li>")
                html_parts.append("</ul>")
                list_items = []
            in_list = False

        for i, t in enumerate(texts):
            tx = t["text"]
            fs = t["fs"]

            if tx == page_title and i == 0:
                continue    # Already used as block title

            # ALERT
            if any(w in tx.lower() for w in ["предупреждение","warning"]):
                flush_list()
                clean = tx.replace("ПРЕДУПРЕЖДЕНИЕ","").replace("WARNING","").strip()
                html_parts.append(f"""<div class="alert danger">
  <span class="alert-icon">⚠️</span>
  <div class="alert-text"><div class="alert-head">ПРЕДУПРЕЖДЕНИЕ</div><p>{clean}</p></div>
</div>""")
            elif any(w in tx.lower() for w in ["осторожно","caution"]):
                flush_list()
                clean = tx.replace("ОСТОРОЖНО","").replace("CAUTION","").strip()
                html_parts.append(f"""<div class="alert">
  <span class="alert-icon">⚠️</span>
  <div class="alert-text"><div class="alert-head">ОСТОРОЖНО</div><p>{clean}</p></div>
</div>""")
            elif any(w in tx.lower() for w in ["внимание","важно"]) and len(tx) < 200:
                flush_list()
                html_parts.append(f"""<div class="alert note">
  <span class="alert-icon">💡</span>
  <div class="alert-text"><div class="alert-head">ВАЖНО</div><p>{tx}</p></div>
</div>""")
            # Sub-heading
            elif fs >= 14 and len(tx) < 80:
                flush_list()
                html_parts.append(f"<h3 class='t-sub'>{tx}</h3>")
            # Short label:value → spec card
            elif ":" in tx and fs < 13 and len(tx) < 100:
                parts = tx.split(":", 1)
                if len(parts) == 2 and parts[1].strip():
                    flush_list()
                    html_parts.append(f"""<div class="spec-card" style="margin:8px 0">
  <div class="sc-label">{parts[0].strip()}</div>
  <div class="sc-value">{parts[1].strip()}</div>
</div>""")
                else:
                    list_items.append(tx)
                    in_list = True
            # Start a bullet
            elif tx.startswith(("☞","•","●","◆","l ","◦")):
                list_items.append(tx[1:].strip())
                in_list = True
            # Regular paragraph
            else:
                flush_list()
                html_parts.append(f"<p class='t-body'>{tx}</p>")

        flush_list()

        # Images
        if imgs:
            html_parts.append('<div class="img-grid">')
            for idx, src in enumerate(imgs):
                cap = f"Рисунок {page+1}-{idx+1}"
                html_parts.append(f"""<div class="img-card">
  <img src="{src}" loading="lazy" onclick="zoom(this.src)" alt="{cap}">
  <div class="img-cap">{cap}</div>
</div>""")
            html_parts.append("</div>")

        html_parts.append("</div>")   # block-body
        html_parts.append("</div>")   # content-block

    html_parts.append("</main>")
    html_parts.append(js)
    html_parts.append("</body></html>")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html_parts))
    print(f"[DONE] {out_path}")

if __name__ == "__main__":
    base = r"E:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\PDF-NEXUS-TRANS"

    deploy = r"E:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\NEXUS-MANUALS-DEPLOY"

    build_manual(
        json_path=base + r"\k10_ru_CLEAN.json",
        img_dir=r"E:\Downloads\00000111111111222222\K10_MANUAL\images",
        out_path=os.path.join(deploy, "k10", "index.html"),
        title="Машина для встряхивания порошка",
        model="ADL07K10",
        accent="#E84545",
        pages_total=16
    )

    build_manual(
        json_path=base + r"\e06_ru_CLEAN.json",
        img_dir=r"E:\Downloads\00000111111111222222\E06_MANUAL\images",
        out_path=os.path.join(deploy, "e06", "index.html"),
        title="Машина для глажения",
        model="ADL07E06",
        accent="#1A73E8",
        pages_total=68
    )
