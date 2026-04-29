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

    doc = fitz.open(pdf_path)

    html_head = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
    <meta charset="utf-8">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
      :root {{
         --bg: #0f172a;
         --surface: #1e293b;
         --primary: #3b82f6;
         --accent: #0ea5e9;
         --text: #f8fafc;
         --text-muted: #94a3b8;
         --danger: #ef4444;
         --warning: #f59e0b;
      }}
      * {{ box-sizing: border-box; scroll-behavior: smooth; }}
      body {{ 
          font-family: 'Inter', sans-serif; 
          margin: 0; padding: 0; 
          background: var(--bg); 
          color: var(--text); 
          display: flex;
      }}
      /* Sidebar */
      #sidebar {{
          width: 300px;
          height: 100vh;
          position: fixed;
          background: rgba(30, 41, 59, 0.8);
          backdrop-filter: blur(12px);
          border-right: 1px solid rgba(255,255,255,0.1);
          padding: 30px 20px;
          overflow-y: auto;
          box-shadow: 2px 0 15px rgba(0,0,0,0.5);
      }}
      #sidebar h2 {{ font-family: 'Outfit', sans-serif; font-size: 20px; margin-top: 0; color: var(--accent); }}
      #sidebar a {{ display: block; color: var(--text-muted); text-decoration: none; margin: 12px 0; font-size: 14px; transition: 0.2s; }}
      #sidebar a:hover {{ color: var(--text); padding-left: 5px; border-left: 2px solid var(--primary); }}
      
      /* Main Content */
      #content {{
          margin-left: 300px;
          padding: 50px 80px;
          max-width: 1100px;
          width: calc(100% - 300px);
      }}
      
      .page-card {{ 
          background: var(--surface); 
          padding: 50px; 
          margin-bottom: 50px; 
          border-radius: 20px; 
          box-shadow: 0 20px 25px -5px rgba(0,0,0,0.3);
          border: 1px solid rgba(255,255,255,0.05);
      }}
      
      .page-number {{
          display: inline-block;
          font-family: 'Outfit';
          background: rgba(59, 130, 246, 0.2);
          color: var(--primary);
          padding: 5px 12px;
          border-radius: 20px;
          font-size: 12px;
          font-weight: 600;
          margin-bottom: 25px;
      }}

      h1, h2, h3 {{ font-family: 'Outfit', sans-serif; color: #fff; margin-top: 40px; }}
      h1 {{ font-size: 38px; background: linear-gradient(to right, #3b82f6, #0ea5e9); -webkit-background-clip: text; color: transparent; border-bottom: 2px solid rgba(59,130,246,0.3); padding-bottom: 15px; }}
      h2 {{ font-size: 26px; border-left: 4px solid var(--primary); padding-left: 15px; }}
      h3 {{ font-size: 20px; color: var(--accent); }}
      
      p {{ font-size: 16px; line-height: 1.8; color: #cbd5e1; }}
      
      /* Smart Components */
      .alert {{
          padding: 20px; border-radius: 12px; margin: 25px 0; display: flex; align-items: flex-start;
          box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
      }}
      .alert-danger {{ background: rgba(239, 68, 68, 0.1); border-left: 5px solid var(--danger); }}
      .alert-danger strong {{ color: var(--danger); font-size: 18px; display: block; margin-bottom: 8px; }}
      .alert-warning {{ background: rgba(245, 158, 11, 0.1); border-left: 5px solid var(--warning); }}
      .alert-warning strong {{ color: var(--warning); font-size: 18px; display: block; margin-bottom: 8px; }}
      
      /* Grid list for specs */
      .spec-item {{
          background: rgba(0,0,0,0.2);
          padding: 15px 20px;
          border-radius: 8px;
          margin-bottom: 10px;
          border: 1px solid rgba(255,255,255,0.05);
          display: flex;
          justify-content: space-between;
      }}
      
      /* Image Styling */
      img {{ 
          max-width: 100%; height: auto; 
          margin: 40px auto; display: block; 
          border-radius: 12px; 
          box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5);
          cursor: pointer; transition: transform 0.3s;
      }}
      img:hover {{ transform: scale(1.02); }}

      /* Lightbox */
      #lightbox {{
          display: none; position: fixed; z-index: 999; top: 0; left: 0; width: 100%; height: 100%;
          background: rgba(0,0,0,0.9); justify-content: center; align-items: center; cursor: pointer;
      }}
      #lightbox img {{ max-height: 90%; max-width: 90%; box-shadow: 0 0 30px rgba(0,0,0,0.8); }}

      @media(max-width: 900px) {{
          #sidebar {{ display: none; }}
          #content {{ margin-left: 0; width: 100%; padding: 20px; }}
      }}
    </style>
    </head>
    <body>
    <div id="sidebar">
        <h2>📑 Навигация</h2>
        <div id="toc"></div>
    </div>
    
    <div id="content">
    <div id="lightbox" onclick="this.style.display='none'">
        <img id="lb-img" src="">
    </div>
    """

    content = ""
    toc_links = ""
    heading_counter = 0

    for page_num in range(len(doc)):
        page = doc[page_num]
        content += f'<div class="page-card" id="page-{page_num+1}">\n<div class="page-number">Стр. {page_num+1}</div>\n'
        
        items = []
        
        # 1. Text blocks
        blocks = ru_data.get(str(page_num), [])
        for b in blocks:
            items.append({
                "type": "text",
                "y0": b["bbox"][1],
                "text": b["ru_text"],
                "font_size": b["font_size"]
            })
            
        # 2. Image blocks
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
            except:
                pass
                
        # 3. Sort Everything
        items.sort(key=lambda x: x["y0"])
        
        # 4. Render Logic
        in_list = False
        for item in items:
            if item["type"] == "text":
                text = item["text"].strip()
                if not text or "Стр." in text and "из" in text:
                    continue
                    
                fs = item["font_size"]
                
                # Heading Detection (Building TOC)
                if fs >= 20 or "Глава " in text or "Инструкция" in text:
                    heading_counter += 1
                    hid = f"h-{heading_counter}"
                    if fs >= 25 or "Глава" in text:
                        content += f'<h1 id="{hid}">{text}</h1>\n'
                        toc_links += f'<a href="#{hid}">{text}</a>\n'
                    else:
                        content += f'<h2 id="{hid}">{text}</h2>\n'
                        toc_links += f'<a href="#{hid}">{text}</a>\n'
                
                # Warnings / Cautions
                elif "ПРЕДУПРЕЖДЕНИЕ" in text or "WARNING" in text:
                    text = text.replace("ПРЕДУПРЕЖДЕНИЕ", "").replace("WARNING", "").strip()
                    content += f'<div class="alert alert-danger"><div><strong>⚠️ ПРЕДУПРЕЖДЕНИЕ</strong>{text}</div></div>\n'
                elif "ОСТОРОЖНО" in text or "CAUTION" in text:
                    text = text.replace("ОСТОРОЖНО", "").replace("CAUTION", "").strip()
                    content += f'<div class="alert alert-warning"><div><strong>⚠️ ОСТОРОЖНО</strong>{text}</div></div>\n'
                
                # Parameters logic (Spec Items)
                elif ":" in text and len(text) < 100:
                    parts = text.split(":", 1)
                    if len(parts) == 2 and parts[1].strip():
                        content += f'<div class="spec-item"><span>{parts[0]}</span> <strong>{parts[1]}</strong></div>\n'
                    else:
                        content += f"<p>{text}</p>\n"
                
                # Regular Paragraph
                else:
                    content += f"<p>{text}</p>\n"
                    
            elif item["type"] == "image":
                content += f'<img src="{item["src"]}" onclick="document.getElementById(\'lb-img\').src=this.src; document.getElementById(\'lightbox\').style.display=\'flex\';" alt="Image">\n'
                
        content += "</div>\n"

    # Assemble HTML
    final_html = html_head + content + f"""
    </div>
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
        
    print(f"[DONE] Premium UI saved to: {html_path}")

if __name__ == "__main__":
    pdf_path = sys.argv[1]
    json_path = sys.argv[2]
    out_dir = sys.argv[3]
    build_premium_html(pdf_path, json_path, out_dir, "ADL07K10_Руководство")
