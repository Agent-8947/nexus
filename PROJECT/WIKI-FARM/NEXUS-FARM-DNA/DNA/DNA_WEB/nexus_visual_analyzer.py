"""
NEXUS Brand DNA Extractor v4.0 — Full Spectrum
Extracts: colors, typography, geometry, animations, buttons, layout,
          icons, images, favicon, OG meta, copy DNA, and generates
          a web scenario with hooks/slogans/CTAs.

Usage:  python nexus_visual_analyzer.py <url>
Output: DNA_BRAND/BRAND_NNN_<domain>/
"""

import sys, json, re, os
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

from js_payloads import (JS_EXTRACT, JS_LOGO, JS_LINKS, JS_FAVICON,
                         JS_OG_META, JS_ICONS, JS_ANIMATIONS, JS_BUTTONS,
                         JS_LAYOUT, JS_IMAGES, JS_COPY, JS_ACCENT)

BASE_DIR = Path(__file__).parent.parent / "DNA_BRAND"


def merge(target, source):
    for item in source:
        target[item["value"]] = target.get(item["value"], 0) + item["count"]

def top(d, n=25):
    return [{"value": v, "count": c} for v, c in
            sorted(d.items(), key=lambda x: -x[1])[:n]]

def next_brand_id():
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    existing = [d.name for d in BASE_DIR.iterdir() if d.is_dir() and d.name.startswith("BRAND_")]
    nums = [int(m.group(1)) for name in existing if (m := re.match(r"BRAND_(\d+)", name))]
    return max(nums, default=0) + 1


def run(url, max_pages=4):
    parsed = urlparse(url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    domain = parsed.netloc.replace("www.", "").split(".")[0]

    brand_id = next_brand_id()
    out_dir = BASE_DIR / f"BRAND_{brand_id:03d}_{domain}"
    out_dir.mkdir(parents=True, exist_ok=True)
    icons_dir = out_dir / "icons"
    icons_dir.mkdir(exist_ok=True)
    images_dir = out_dir / "images"
    images_dir.mkdir(exist_ok=True)

    log = lambda msg: print(f"[{msg}]", file=sys.stderr)
    log(f"NEXUS Brand DNA Extractor v4.0")
    log(f"Target:  {url}")
    log(f"Output:  {out_dir}")

    # Accumulators
    acc = {k: {} for k in ["bg","text","borders","families","sizes","weights",
                            "line_heights","letter_spacings","radii","shadows","paddings"]}
    all_gradients, all_copy, all_buttons = [], {"headings":[],"ctas":[],"paragraphs":[],"tagline":""}, []
    og_meta, favicon_list, anim_data, layout_data, accent_data = {}, [], {}, {}, {}
    logo_data = None
    visited, to_visit = set(), [parsed.path or "/"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})

        while to_visit and len(visited) < max_pages:
            path = to_visit.pop(0)
            if path in visited: continue
            visited.add(path)
            full = origin + path
            log(f"SCAN {full}")
            try:
                page.goto(full, wait_until="load", timeout=30000)
                page.wait_for_timeout(2500)
            except Exception as e:
                log(f"SKIP {e}"); continue

            is_first = len(visited) == 1

            # Screenshot
            if is_first:
                page.screenshot(path=str(out_dir / "screenshot.png"), full_page=False)
                log("SAVE screenshot.png")

            # CSS Tokens
            try:
                data = page.evaluate(JS_EXTRACT)
                merge(acc["bg"], data["colors"]["backgrounds"])
                merge(acc["text"], data["colors"]["text"])
                merge(acc["borders"], data["colors"]["borders"])
                merge(acc["families"], data["typography"]["families"])
                merge(acc["sizes"], data["typography"]["sizes"])
                merge(acc["weights"], data["typography"]["weights"])
                merge(acc["line_heights"], data["typography"]["line_heights"])
                merge(acc["letter_spacings"], data["typography"]["letter_spacings"])
                merge(acc["radii"], data["geometry"]["border_radii"])
                merge(acc["shadows"], data["geometry"]["box_shadows"])
                merge(acc["paddings"], data["spacing"]["paddings"])
                for g in data.get("gradients", []):
                    if g not in all_gradients: all_gradients.append(g)
            except Exception as e:
                log(f"ERR extract: {e}"); continue

            # First-page-only extractions
            if is_first:
                # Logo
                try:
                    logos = page.evaluate(JS_LOGO)
                    if logos:
                        best = logos[0]
                        if best["type"] == "svg":
                            (out_dir / "logo.svg").write_text(best["data"], encoding="utf-8")
                            logo_data = {"type":"svg","file":"logo.svg","w":best["w"],"h":best["h"]}
                            log(f"SAVE logo.svg ({best['w']}x{best['h']})")
                        else:
                            import urllib.request
                            ext = "png" if ".png" in best["data"] else "svg" if ".svg" in best["data"] else "png"
                            urllib.request.urlretrieve(best["data"], str(out_dir / f"logo.{ext}"))
                            logo_data = {"type":ext,"file":f"logo.{ext}","w":best["w"],"h":best["h"]}
                            log(f"SAVE logo.{ext}")
                except Exception as e: log(f"WARN logo: {e}")

                # Favicon
                try:
                    favicon_list = page.evaluate(JS_FAVICON)
                    for i, fav in enumerate(favicon_list[:3]):
                        try:
                            import urllib.request
                            ext = fav["href"].split(".")[-1].split("?")[0][:4]
                            urllib.request.urlretrieve(fav["href"], str(out_dir / f"favicon_{i}.{ext}"))
                            log(f"SAVE favicon_{i}.{ext}")
                        except: pass
                except: pass

                # OG Meta
                try: og_meta = page.evaluate(JS_OG_META)
                except: pass

                # Accent colors (context-aware)
                try:
                    accent_data = page.evaluate(JS_ACCENT)
                    rules = accent_data.get('accent_rules', [])
                    top_rule = rules[0] if rules else {}
                    log(f"SAVE accent: {len(rules)} rules, top={top_rule.get('font_family','?')} {top_rule.get('font_style','?')} {top_rule.get('color','?')} (score {top_rule.get('score',0)})")
                except Exception as e: log(f"WARN accent: {e}")

                # Links
                try:
                    links = page.evaluate(JS_LINKS, origin)
                    priority_kw = ["pricing","features","about","platform","technology","solutions","product"]
                    scored = [(10 if any(kw in l.lower() for kw in priority_kw) else 0, l) for l in links]
                    scored.sort(key=lambda x: -x[0])
                    to_visit.extend([s[1] for s in scored if s[1] not in visited])
                except: pass

            # Every page: icons, animations, buttons, layout, images, copy
            try:
                icons = page.evaluate(JS_ICONS)
                for i, icon in enumerate(icons):
                    fname = f"icon_{len(list(icons_dir.iterdir()))+1:02d}.svg"
                    (icons_dir / fname).write_text(icon["svg"], encoding="utf-8")
                if icons: log(f"SAVE {len(icons)} icons")
            except: pass

            try:
                ad = page.evaluate(JS_ANIMATIONS)
                for k in ["transitions","easings","animations"]:
                    if k not in anim_data: anim_data[k] = {}
                    for item in ad.get(k, []):
                        anim_data[k][item["value"]] = anim_data[k].get(item["value"],0) + item["count"]
            except: pass

            try: all_buttons.extend(page.evaluate(JS_BUTTONS))
            except: pass

            try:
                ld = page.evaluate(JS_LAYOUT)
                for k in ["max_widths","gaps"]:
                    if k not in layout_data: layout_data[k] = {}
                    for item in ld.get(k, []):
                        layout_data[k][item["value"]] = layout_data[k].get(item["value"],0) + item["count"]
            except: pass

            try:
                imgs = page.evaluate(JS_IMAGES)
                for img in imgs[:5]:
                    try:
                        import urllib.request
                        fname = f"img_{len(list(images_dir.iterdir()))+1:02d}.jpg"
                        urllib.request.urlretrieve(img["src"], str(images_dir / fname))
                    except: pass
                if imgs: log(f"SAVE {min(len(imgs),5)} images")
            except: pass

            try:
                copy = page.evaluate(JS_COPY)
                all_copy["headings"].extend(copy.get("headings", []))
                all_copy["ctas"].extend(list(set(copy.get("ctas", []))))
                all_copy["paragraphs"].extend(copy.get("paragraphs", []))
                if not all_copy["tagline"] and copy.get("tagline"):
                    all_copy["tagline"] = copy["tagline"]
            except: pass

        browser.close()

    # Deduplicate
    seen_cta = set()
    unique_ctas = []
    for c in all_copy["ctas"]:
        if c not in seen_cta: seen_cta.add(c); unique_ctas.append(c)
    all_copy["ctas"] = unique_ctas[:20]

    seen_btn = set()
    unique_btns = []
    for b in all_buttons:
        key = b["bg"]+b["color"]+b["radius"]
        if key not in seen_btn: seen_btn.add(key); unique_btns.append(b)
    all_buttons = unique_btns[:10]

    # Build DNA
    dna = {
        "meta": {"source_url":url,"domain":domain,"brand_id":brand_id,
                 "pages_scanned":list(visited),"total_pages":len(visited),
                 "logo":logo_data,"og_meta":og_meta,
                 "favicons":[f["href"] for f in favicon_list[:3]]},
        "colors": {"backgrounds":top(acc["bg"]),"text":top(acc["text"]),"borders":top(acc["borders"])},
        "typography": {"families":top(acc["families"],10),"sizes":top(acc["sizes"],15),
                       "weights":top(acc["weights"]),"line_heights":top(acc["line_heights"],10),
                       "letter_spacings":top(acc["letter_spacings"],10)},
        "geometry": {"border_radii":top(acc["radii"]),"box_shadows":top(acc["shadows"],10)},
        "spacing": {"paddings":top(acc["paddings"],15)},
        "gradients": all_gradients[:10],
        "animations": {k:[{"value":v,"count":c} for v,c in sorted(d.items(),key=lambda x:-x[1])[:10]]
                       for k,d in anim_data.items()},
        "buttons": all_buttons,
        "layout": {k:[{"value":v,"count":c} for v,c in sorted(d.items(),key=lambda x:-x[1])[:10]]
                   for k,d in layout_data.items()},
        "copy_dna": all_copy,
        "accent_palette": accent_data
    }

    (out_dir / "dna.json").write_text(json.dumps(dna, indent=2, ensure_ascii=False), encoding="utf-8")
    log("SAVE dna.json")

    # Generate copy analysis & web scenario
    generate_copy_report(dna, out_dir)
    log("SAVE copy_dna.md")

    # Generate brandbook
    generate_brandbook(dna, out_dir)
    log("SAVE brandbook.html")

    log(f"DONE -> {out_dir}")
    return dna, out_dir


def generate_copy_report(dna, out_dir):
    """Generate text analysis + web scenario."""
    copy = dna.get("copy_dna", {})
    og = dna["meta"].get("og_meta", {})
    domain = dna["meta"]["domain"].upper()

    headings = copy.get("headings", [])
    ctas = copy.get("ctas", [])
    paras = copy.get("paragraphs", [])
    tagline = copy.get("tagline", "")

    # Analyze tone
    h_texts = [h["text"] for h in headings]
    avg_h_len = sum(len(t) for t in h_texts) / max(len(h_texts), 1)
    avg_p_len = sum(len(t) for t in paras) / max(len(paras), 1)

    # Detect voice characteristics
    uses_you = sum(1 for t in h_texts + paras if "you" in t.lower() or "your" in t.lower())
    uses_we = sum(1 for t in h_texts + paras if " we " in t.lower() or "our " in t.lower())
    voice = "Second-person (You/Your)" if uses_you > uses_we else "First-person (We/Our)" if uses_we > 0 else "Neutral/Impersonal"

    md = f"""# {domain} — Copy DNA & Web Scenario
Auto-generated by NEXUS Brand DNA Extractor v4.0

---

## 1. Brand Voice Profile

| Parameter | Value |
|---|---|
| **Voice Direction** | {voice} |
| **Avg Heading Length** | {avg_h_len:.0f} chars |
| **Avg Paragraph Length** | {avg_p_len:.0f} chars |
| **Total Headings** | {len(headings)} |
| **Total CTAs** | {len(ctas)} |
| **Total Paragraphs** | {len(paras)} |

**OG Title:** {og.get('og:title', og.get('title', 'N/A'))}
**OG Description:** {og.get('og:description', og.get('description', 'N/A'))}
**Tagline:** {tagline or 'N/A'}

---

## 2. All Headings (H1-H3)

"""
    for h in headings[:30]:
        md += f"- **[{h['tag']}]** {h['text']}\n"

    md += "\n---\n\n## 3. All CTAs (Buttons & Links)\n\n"
    for c in ctas[:20]:
        md += f"- `{c}`\n"

    md += "\n---\n\n## 4. Key Paragraphs (Tone Samples)\n\n"
    for p in paras[:10]:
        md += f"> {p}\n\n"

    md += f"""---

## 5. Web Scenario (Ready for Build)

### Hook (Hero Section)
**Headline:** {h_texts[0] if h_texts else 'N/A'}
**Subline:** {tagline or (paras[0][:120] + '...' if paras else 'N/A')}
**Primary CTA:** `{ctas[0] if ctas else 'Get Started'}`
**Secondary CTA:** `{ctas[1] if len(ctas) > 1 else 'Learn More'}`

### Section 2 — Value Proposition
"""
    for h in headings[1:4]:
        md += f"- **{h['text']}**\n"

    md += f"""
### Section 3 — Features / Solutions
"""
    for h in headings[4:8]:
        md += f"- {h['text']}\n"

    md += f"""
### Section 4 — Social Proof / Testimonials
> Use client logos, case study quotes, metrics.

### Section 5 — CTA Block (Conversion)
**Headline:** {headings[-2]['text'] if len(headings) > 2 else 'Ready to Start?'}
**CTA:** `{ctas[0] if ctas else 'Get a Demo'}`

---

## 6. Recommended Slogans (Derived from Copy DNA)

"""
    # Extract short punchy phrases from headings
    short_h = [h["text"] for h in headings if 10 < len(h["text"]) < 60]
    for s in short_h[:8]:
        md += f"- \"{s}\"\n"

    (out_dir / "copy_dna.md").write_text(md, encoding="utf-8")


def generate_brandbook(dna, out_dir):
    """Generate visual HTML brandbook."""
    domain = dna["meta"]["domain"]
    url = dna["meta"]["source_url"]
    logo_info = dna["meta"].get("logo")
    og = dna["meta"].get("og_meta", {})
    main_font = dna["typography"]["families"][0]["value"] if dna["typography"]["families"] else "sans-serif"
    gfont = main_font.replace(" ", "+")

    # Logo
    logo_html = ""
    if logo_info and logo_info["type"] == "svg" and (out_dir / "logo.svg").exists():
        svg = (out_dir / "logo.svg").read_text(encoding="utf-8")
        svg = re.sub(r'<\?xml[^?]*\?>\s*', '', svg)
        svg = re.sub(r'<svg ', f'<svg width="{logo_info["w"]}" height="{logo_info["h"]}" ', svg, count=1)
        logo_html = f'<div class="logo-box">{svg}</div>'
    elif logo_info:
        logo_html = f'<div class="logo-box"><img src="{logo_info["file"]}" alt="Logo"></div>'

    def swatches(colors, label):
        items = "".join(f'<div class="sw"><div class="sw-c" style="background:{c["value"]}"></div>'
                        f'<code>{c["value"]}</code><small>{c["count"]}x</small></div>' for c in colors)
        return f'<div class="cg"><h3>{label}</h3><div class="sr">{items}</div></div>'

    bg_sw = swatches(dna["colors"]["backgrounds"][:12], "Backgrounds")
    txt_sw = swatches(dna["colors"]["text"][:10], "Text")
    brd_sw = swatches(dna["colors"]["borders"][:8], "Borders")

    font_cards = "".join(f'<div class="fc" style="font-family:\'{f["value"]}\',sans-serif">'
                         f'<b>{f["value"]}</b> <small>{f["count"]}x</small>'
                         f'<p style="font-size:24px;margin-top:8px">Aa Bb Cc 0123456789</p></div>'
                         for f in dna["typography"]["families"][:5])

    size_pills = "".join(f'<span class="pill"><b style="font-size:{s["value"]}">Aa</b> {s["value"]} ({s["count"]}x)</span>'
                         for s in dna["typography"]["sizes"][:10])

    radii_boxes = "".join(f'<div class="ri"><div class="rb" style="border-radius:{r["value"]}"></div>'
                          f'<code>{r["value"]}</code><small>{r["count"]}x</small></div>'
                          for r in dna["geometry"]["border_radii"][:8])

    btn_cards = "".join(f'<div class="btn-card" style="background:{b["bg"]};color:{b["color"]};'
                        f'border-radius:{b["radius"]};padding:{b["padding"]};font-size:{b["fontSize"]};'
                        f'font-weight:{b["fontWeight"]};letter-spacing:{b.get("letter_spacing","normal")};'
                        f'line-height:{b.get("line_height","normal")}">{b["text"] or "Button"}</div>'
                        for b in dna.get("buttons", [])[:8])

    tracking_pills = "".join(f'<span class="pill"><b>track:</b> {s["value"]} ({s["count"]}x)</span>'
                             for s in dna["typography"].get("letter_spacings", [])[:8])
    
    lh_pills = "".join(f'<span class="pill"><b>lh:</b> {s["value"]} ({s["count"]}x)</span>'
                       for s in dna["typography"].get("line_heights", [])[:8])

    anim_items = ""
    for k, items in dna.get("animations", {}).items():
        if items:
            anim_items += f"<h3>{k.title()}</h3><div class='sr'>"
            anim_items += "".join(f'<span class="pill">{a["value"]} ({a["count"]}x)</span>' for a in items[:6])
            anim_items += "</div>"

    copy = dna.get("copy_dna", {})
    cta_pills = "".join(f'<span class="pill cta-pill">{c}</span>' for c in copy.get("ctas", [])[:10])
    heading_list = "".join(f'<li><b>[{h["tag"]}]</b> {h["text"]}</li>' for h in copy.get("headings", [])[:15])

    # Count icons
    icons_count = len(list((out_dir / "icons").iterdir())) if (out_dir / "icons").exists() else 0
    images_count = len(list((out_dir / "images").iterdir())) if (out_dir / "images").exists() else 0

    # Accent Rules visualization
    accent_cards = ""
    for r in dna.get("accent_palette", {}).get("accent_rules", [])[:5]:
        sample = r["samples"][0] if r.get("samples") else "Accent Sample"
        ls = r.get('letter_spacing', 'normal')
        lh = r.get('line_height', 'normal')
        tt = r.get('text_transform', 'none')
        accent_cards += f'''<div class="fc">
            <div style="font-family:\'{r["font_family"]}\'; font-style:{r["font_style"]}; font-weight:{r["font_weight"]}; color:{r["color"]}; letter-spacing:{ls}; line-height:{lh}; text-transform:{tt}; font-size:24px;">{sample}</div>
            <code style="font-size:11px; color:#666; display:block; margin-top:8px;">{r["font_family"]} | {r["font_style"]} | {r["font_weight"]} | {r["color"]} | track:{ls}</code>
        </div>'''

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{domain.upper()} -- Brand DNA v4.0</title>
<link href="https://fonts.googleapis.com/css2?family={gfont}:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'{main_font}',system-ui,sans-serif;background:#F8F8F6;color:#1A1A1A;padding:40px 20px;line-height:1.6}}
.w{{max-width:960px;margin:0 auto}}
header{{margin-bottom:40px;padding-bottom:24px;border-bottom:1px solid #E5E5E0}}
h1{{font-size:32px;font-weight:600;letter-spacing:-0.03em;margin-bottom:6px}}
h2{{font-size:20px;font-weight:600;margin-bottom:16px;letter-spacing:-0.02em}}
h3{{font-size:13px;font-weight:600;color:#888;text-transform:uppercase;letter-spacing:0.05em;margin:16px 0 10px}}
p.sub{{color:#888;font-size:14px}}
.logo-box{{margin:20px 0;padding:20px;background:#fff;border:1px solid #E5E5E0;border-radius:8px;display:inline-block}}
.logo-box img,.logo-box svg{{max-height:50px;width:auto}}
.sec{{margin-bottom:40px}}
.cg{{margin-bottom:20px}}
.sr{{display:flex;flex-wrap:wrap;gap:10px}}
.sw{{display:flex;flex-direction:column;align-items:center;gap:3px}}
.sw-c{{width:56px;height:56px;border-radius:6px;border:1px solid rgba(0,0,0,0.08)}}
.sw code{{font-size:10px;color:#555}}.sw small{{font-size:9px;color:#aaa}}
.fc{{background:#fff;border:1px solid #E5E5E0;border-radius:8px;padding:16px;margin-bottom:10px}}
.pill{{display:inline-block;padding:4px 10px;background:#fff;border:1px solid #E5E5E0;border-radius:100px;font-size:12px;margin:3px}}
.cta-pill{{background:#1A1A1A;color:#fff;border:none}}
.ri{{display:flex;flex-direction:column;align-items:center;gap:4px}}
.rb{{width:48px;height:48px;background:#E5E5E0;border:2px solid #ccc}}
.btn-card{{display:inline-block;margin:4px;border:1px solid rgba(0,0,0,0.1)}}
.meta-t{{width:100%;border-collapse:collapse}}
.meta-t td{{padding:6px 10px;border-bottom:1px solid #eee;font-size:13px}}
.meta-t td:first-child{{font-weight:600;color:#888;width:140px}}
.ss img{{max-width:100%;border-radius:8px;border:1px solid #E5E5E0}}
ul{{list-style:none;padding:0}} li{{padding:4px 0;font-size:14px;border-bottom:1px solid #f0f0f0}}
.stat-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:16px 0}}
.stat-box{{background:#fff;border:1px solid #E5E5E0;border-radius:8px;padding:16px;text-align:center}}
.stat-box b{{font-size:28px;display:block}}
.stat-box small{{color:#888;font-size:12px}}
</style></head><body><div class="w">
<header>
<h1>{domain.upper()} -- Brand DNA</h1>
<p class="sub">Extracted from <a href="{url}">{url}</a> | {dna['meta']['total_pages']} pages | v4.0</p>
{logo_html}
</header>

<div class="stat-grid">
<div class="stat-box"><b>{len(dna['colors']['backgrounds'])}</b><small>Colors</small></div>
<div class="stat-box"><b>{len(dna['typography']['families'])}</b><small>Fonts</small></div>
<div class="stat-box"><b>{icons_count}</b><small>Icons</small></div>
<div class="stat-box"><b>{images_count}</b><small>Images</small></div>
</div>

<div class="sec"><h2>Screenshot</h2><div class="ss"><img src="screenshot.png" alt="Homepage"></div></div>

<div class="sec"><h2>Color Palette</h2>{bg_sw}{txt_sw}{brd_sw}</div>

<div class="sec"><h2>Typography</h2>{font_cards}
<h3>Accent Rules</h3>{accent_cards}
<h3>Tracking (Global)</h3><div class="sr">{tracking_pills}</div>
<h3>Line Heights (Global)</h3><div class="sr">{lh_pills}</div>
<h3>Sizes</h3><div class="sr">{size_pills}</div></div>

<div class="sec"><h2>Geometry</h2><h3>Border Radii</h3><div class="sr">{radii_boxes}</div></div>

<div class="sec"><h2>Buttons</h2><div class="sr">{btn_cards}</div></div>

{"<div class='sec'><h2>Animations</h2>" + anim_items + "</div>" if anim_items else ""}

<div class="sec"><h2>Copy DNA</h2>
<h3>Tagline</h3><p style="font-size:18px;font-weight:500;margin-bottom:16px">{copy.get('tagline','N/A')}</p>
<h3>CTAs</h3><div class="sr">{cta_pills}</div>
<h3>Headings</h3><ul>{heading_list}</ul>
</div>

<div class="sec"><h2>OG Meta</h2>
<table class="meta-t">
<tr><td>Title</td><td>{og.get('og:title', og.get('title','N/A'))}</td></tr>
<tr><td>Description</td><td>{og.get('og:description', og.get('description','N/A'))}</td></tr>
<tr><td>OG Image</td><td>{og.get('og:image','N/A')}</td></tr>
</table></div>

<div class="sec"><h2>Assets</h2>
<table class="meta-t">
<tr><td>Logo</td><td>{logo_info['file'] if logo_info else 'Not found'}</td></tr>
<tr><td>Favicons</td><td>{len(dna['meta'].get('favicons',[]))} extracted</td></tr>
<tr><td>Icons</td><td>{icons_count} SVGs in /icons/</td></tr>
<tr><td>Images</td><td>{images_count} files in /images/</td></tr>
<tr><td>Copy Report</td><td>copy_dna.md</td></tr>
</table></div>

</div></body></html>"""

    (out_dir / "brandbook.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python nexus_visual_analyzer.py <url>"); sys.exit(1)
    target = sys.argv[1]
    if not target.startswith("http"): target = "https://" + target
    dna, out = run(target)
    print(f"\n[OK] Brand DNA extracted to: {out}")
