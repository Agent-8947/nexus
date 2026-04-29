import fitz
import json
import os
import sys

def build_premium_html(pdf_path, json_path, out_dir, title="Руководство по эксплуатации"):
    print(f"[PREMIUM TYPESETTING] Starting build for {pdf_path}...")
    os.makedirs(out_dir, exist_ok=True)
    img_dir = os.path.join(out_dir, "images")
    os.makedirs(img_dir, exist_ok=True)

    with open(json_path, 'r', encoding='utf-8') as f:
        ru_data = json.load(f)

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        doc = None

    html_head = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
      :root {{
        --bg: #0B1120;
        --surface: #111827;
        --surface-2: #1F2937;
        --border: rgba(255,255,255,0.06);
        --primary: #8B5CF6;
        --primary-dim: rgba(139,92,246,0.15);
        --accent: #EC4899;
        --success: #10B981;
        --danger: #EF4444;
        --warning: #F59E0B;
        --text: #F1F5F9;
        --text-2: #94A3B8;
        --text-3: #64748B;
        --radius: 16px;
      }}
      * {{ box-sizing: border-box; margin: 0; padding: 0; scroll-behavior: smooth; }}
      body {{ 
          font-family: 'Inter', sans-serif; 
          background: var(--bg); 
          color: var(--text); 
          line-height: 1.75;
          display: flex;
      }}
      /* Sidebar */
      nav {{
          width: 320px; min-width: 320px;
          height: 100vh; position: fixed;
          background: rgba(17, 24, 39, 0.85);
          backdrop-filter: blur(20px);
          border-right: 1px solid var(--border);
          padding: 30px 20px;
          overflow-y: auto;
          z-index: 100;
      }}
      nav .logo {{ font-family: 'Outfit'; font-size: 14px; color: var(--accent); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 30px; opacity: 0.9; }}
      nav h3 {{ font-family: 'Outfit'; font-size: 11px; color: var(--text-3); text-transform: uppercase; letter-spacing: 2px; margin: 25px 0 10px; }}
      nav a {{ display: block; color: var(--text-2); text-decoration: none; font-size: 14px; padding: 10px 14px; border-radius: 8px; margin: 2px 0; transition: all 0.2s; }}
      nav a:hover {{ background: var(--primary-dim); color: var(--text); }}
      nav a.active {{ background: var(--primary-dim); color: var(--primary); font-weight: 600; border-left: 3px solid var(--primary); }}
      
      /* Main Content */
      main {{
          margin-left: 320px; padding: 60px 80px; max-width: 1000px; width: 100%;
      }}
      
      /* Typography */
      h1 {{ font-family: 'Outfit'; font-size: 42px; font-weight: 800; line-height: 1.2; margin-bottom: 20px; background: linear-gradient(135deg, #8B5CF6, #EC4899); -webkit-background-clip: text; color: transparent; }}
      .subtitle {{ font-size: 16px; color: var(--text-2); margin-bottom: 50px; }}
      h2 {{ font-family: 'Outfit'; font-size: 32px; font-weight: 700; margin: 60px 0 20px; padding-top: 30px; border-top: 1px solid var(--border); }}
      h3 {{ font-family: 'Outfit'; font-size: 24px; font-weight: 600; color: var(--accent); margin: 35px 0 15px; }}
      h4 {{ font-family: 'Outfit'; font-size: 18px; font-weight: 600; margin: 25px 0 10px; }}
      p {{ font-size: 16px; color: var(--text-2); margin-bottom: 16px; }}
      
      /* Cards */
      .card {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 30px; margin: 25px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
      .page-indicator {{ text-align: right; font-family: 'JetBrains Mono'; font-size: 12px; color: var(--text-3); margin-top: -15px; margin-bottom: 20px; }}
      
      /* Specs */
      .spec-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
      .spec-item {{ background: var(--surface-2); padding: 16px 20px; border-radius: 12px; border: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }}
      .spec-item .label {{ font-size: 13px; color: var(--text-3); text-transform: uppercase; letter-spacing: 1px; }}
      .spec-item .value {{ font-family: 'JetBrains Mono'; font-size: 15px; color: var(--text); font-weight: 500; text-align: right; max-width: 50%; }}
      
      /* Alerts */
      .alert {{ padding: 20px 24px; border-radius: 12px; margin: 25px 0; border-left: 5px solid; }}
      .alert-danger {{ background: rgba(239,68,68,0.08); border-color: var(--danger); }}
      .alert-danger .alert-title {{ color: var(--danger); }}
      .alert-warning {{ background: rgba(245,158,11,0.08); border-color: var(--warning); }}
      .alert-warning .alert-title {{ color: var(--warning); }}
      .alert-info {{ background: rgba(139,92,246,0.08); border-color: var(--primary); }}
      .alert-info .alert-title {{ color: var(--primary); }}
      .alert-title {{ font-family: 'Outfit'; font-weight: 600; font-size: 16px; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }}
      .alert p {{ margin: 0; font-size: 15px; color: inherit; opacity: 0.9; }}
      
      /* Lists */
      ol, ul {{ padding-left: 24px; margin: 15px 0; }}
      li {{ font-size: 16px; color: var(--text-2); margin-bottom: 10px; }}
      
      /* Images */
      img {{ max-width: 100%; border-radius: 12px; margin: 40px auto; display: block; box-shadow: 0 15px 40px rgba(0,0,0,0.5); cursor: zoom-in; transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1); }}
      img:hover {{ transform: scale(1.02); }}
      
      /* Lightbox */
      #lightbox {{ display:none; position:fixed; z-index:999; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.95); justify-content:center; align-items:center; cursor:zoom-out; }}
      #lightbox img {{ max-height:90vh; max-width:90vw; border-radius:8px; box-shadow: 0 0 60px rgba(0,0,0,0.8); margin:0; cursor:zoom-out; }}
      
      /* Divider */
      .divider {{ height: 1px; background: var(--border); margin: 60px 0; }}
      
      @media(max-width: 900px) {{
          nav {{ display: none; }}
          main {{ margin-left: 0; padding: 30px 20px; }}
          .spec-grid {{ grid-template-columns: 1fr; }}
          .spec-item {{ flex-direction: column; align-items: flex-start; }}
          .spec-item .value {{ max-width: 100%; text-align: left; margin-top: 5px; }}
      }}
    </style>
    </head>
    <body>
    <nav>
        <div class="logo">AUDLEY · {title}</div>
        <h3>📚 Навигация</h3>
        <div id="toc"></div>
    </nav>
    
    <div id="lightbox" onclick="this.style.display='none'"><img id="lb-img" src=""></div>
    
    <main>
    <section id="intro">
      <h1>Машина для глажения (E06)</h1>
      <p class="subtitle">ADL07E06 · Полное руководство по эксплуатации · Henan Audley Digital Co., Ltd.</p>
    </section>
    """

    content = ""
    toc_links = ""
    heading_counter = 0

    num_pages = len(doc) if doc else len(ru_data.keys())

    for page_num in range(num_pages):
        page_str = str(page_num)
        blocks = ru_data.get(page_str, [])
        if not blocks:
            continue
            
        content += f'<div class="card" id="page-{page_num+1}">\n'
        content += f'<div class="page-indicator">Стр. {page_num+1}</div>\n'
        
        items = []
        
        # 1. Text blocks
        for b in blocks:
            text = b.get("ru_text") or b.get("en_text", "")
            items.append({
                "type": "text",
                "y0": b["bbox"][1],
                "text": text,
                "font_size": b["font_size"]
            })
            
        # 2. Image blocks
        if doc:
            page = doc[page_num]
            img_info = page.get_image_info(xrefs=True)
            seen_bboxes = set() 
            for img in img_info:
                xref = img.get("xref")
                bbox = img.get("bbox")
                if not xref or not bbox: continue
                bbox_key = (round(bbox[0]), round(bbox[1]), round(bbox[2]), round(bbox[3]))
                if bbox_key in seen_bboxes: continue
                seen_bboxes.add(bbox_key)
                try:
                    pix = fitz.Pixmap(doc, xref)
                    if pix.n - pix.alpha > 3:
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    img_filename = f"img_p{page_num}_{xref}.png"
                    pix.save(os.path.join(img_dir, img_filename))
                    if pix.width > 30 and pix.height > 30:
                        items.append({
                            "type": "image",
                            "y0": bbox[1],
                            "src": f"images/{img_filename}"
                        })
                except Exception as e:
                    pass
                
        # 3. Sort Everything Top-to-Bottom
        items.sort(key=lambda x: x["y0"])
        
        # 4. Render Layout
        for item in items:
            if item["type"] == "text":
                text = item["text"].strip()
                if not text or ("Стр." in text and "из" in text):
                    continue
                    
                fs = item["font_size"]
                
                # Heuristics for formatting
                text_lower = text.lower()
                
                # Headings
                if fs >= 20 or "глава" in text_lower or (fs >= 15 and len(text) < 50 and not text.endswith('.')):
                    heading_counter += 1
                    hid = f"h-{heading_counter}"
                    if fs >= 24 or "глава" in text_lower:
                        content += f'<h2 id="{hid}">{text}</h2>\n'
                        # Add to TOC only if it's a major heading
                        if "глава" in text_lower or heading_counter <= 10:
                            short_text = text[:40] + "..." if len(text) > 40 else text
                            toc_links += f'<a href="#{hid}">{short_text}</a>\n'
                    else:
                        content += f'<h3 id="{hid}">{text}</h3>\n'
                        
                # Warnings / Cautions
                elif "предупреждение" in text_lower or "warning" in text_lower:
                    clean_text = text.replace("ПРЕДУПРЕЖДЕНИЕ", "").replace("WARNING", "").strip()
                    content += f'<div class="alert alert-danger"><div><div class="alert-title">⚠️ ПРЕДУПРЕЖДЕНИЕ</div><p>{clean_text}</p></div></div>\n'
                elif "осторожно" in text_lower or "caution" in text_lower:
                    clean_text = text.replace("ОСТОРОЖНО", "").replace("CAUTION", "").strip()
                    content += f'<div class="alert alert-warning"><div><div class="alert-title">⚠️ ОСТОРОЖНО</div><p>{clean_text}</p></div></div>\n'
                elif "внимание" in text_lower or "note" in text_lower:
                    clean_text = text.replace("ВНИМАНИЕ", "").replace("NOTE", "").strip()
                    content += f'<div class="alert alert-info"><div><div class="alert-title">💡 ВНИМАНИЕ</div><p>{clean_text}</p></div></div>\n'
                    
                # Specs (Key : Value)
                elif ":" in text and len(text) < 100 and fs < 15:
                    parts = text.split(":", 1)
                    if len(parts) == 2 and parts[1].strip():
                        content += f'<div class="spec-item"><div class="label">{parts[0].strip()}</div><div class="value">{parts[1].strip()}</div></div>\n'
                    else:
                        content += f"<p>{text}</p>\n"
                        
                # Bullets
                elif text.startswith("") or text.startswith("l "):
                    clean_text = text[1:].strip()
                    content += f"<ul><li>{clean_text}</li></ul>\n"
                    
                # Regular Paragraph
                else:
                    content += f"<p>{text}</p>\n"
                    
            elif item["type"] == "image":
                content += f'<img src="{item["src"]}" onclick="document.getElementById(\'lb-img\').src=this.src; document.getElementById(\'lightbox\').style.display=\'flex\';" alt="Схема оборудования">\n'
                
        content += "</div>\n"

    # Assemble HTML
    final_html = html_head + content + f"""
    <div class="divider"></div>
    <p style="text-align:center; color:var(--text-3); font-size:13px; padding: 20px 0;">© Henan Audley Digital Co., Ltd. · NEXUS Translation Engine</p>
    </main>
    <script>
        document.getElementById('toc').innerHTML = `{toc_links}`;
    </script>
    </body>
    </html>
    """

    filename = title.replace(" ", "_") + "_Premium.html"
    html_path = os.path.join(out_dir, filename)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    print(f"[DONE] Premium E06 UI saved to: {html_path}")

if __name__ == "__main__":
    pdf_path = sys.argv[1]
    json_path = sys.argv[2]
    out_dir = sys.argv[3]
    build_premium_html(pdf_path, json_path, out_dir, "ADL07E06_Руководство")
