import fitz
import json
import os
import sys

def build_html_manual(pdf_path, json_path, out_dir):
    print(f"[TYPESETTING] Starting HTML build for {pdf_path}...")
    os.makedirs(out_dir, exist_ok=True)
    img_dir = os.path.join(out_dir, "images")
    os.makedirs(img_dir, exist_ok=True)

    with open(json_path, 'r', encoding='utf-8') as f:
        ru_data = json.load(f)

    doc = fitz.open(pdf_path)

    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
    <meta charset="utf-8">
    <title>Руководство по эксплуатации</title>
    <style>
      :root {
         --primary: #1E3A8A;
         --bg: #F8FAFC;
         --card: #FFFFFF;
         --text: #334155;
      }
      body { 
          font-family: 'Inter', 'Segoe UI', sans-serif; 
          max-width: 800px; 
          margin: 0 auto; 
          padding: 20px; 
          background: var(--bg); 
          color: var(--text); 
          line-height: 1.7;
      }
      .page-card { 
          background: var(--card); 
          padding: 40px; 
          margin-bottom: 40px; 
          border-radius: 12px; 
          box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); 
      }
      .page-number {
          font-size: 12px;
          color: #94A3B8;
          text-align: right;
          border-bottom: 1px solid #E2E8F0;
          padding-bottom: 10px;
          margin-bottom: 20px;
          text-transform: uppercase;
          letter-spacing: 1px;
      }
      img { 
          max-width: 100%; 
          height: auto; 
          display: block; 
          margin: 30px auto; 
          border-radius: 8px; 
          box-shadow: 0 4px 6px rgba(0,0,0,0.05);
      }
      h1, h2, h3 { color: var(--primary); font-weight: 700; margin-top: 30px; }
      h2 { font-size: 24px; border-left: 4px solid var(--primary); padding-left: 10px; }
      h3 { font-size: 18px; }
      p { font-size: 16px; margin: 12px 0; }
      .warning-box {
          background-color: #FEF2F2;
          border-left: 4px solid #EF4444;
          padding: 15px;
          margin: 20px 0;
          border-radius: 0 8px 8px 0;
      }
    </style>
    </head>
    <body>
    """

    for page_num in range(len(doc)):
        page = doc[page_num]
        html_content += f'<div class="page-card">\n<div class="page-number">Страница {page_num+1}</div>\n'
        
        items = []
        
        # 1. Text blocks
        blocks = ru_data.get(str(page_num), [])
        for b in blocks:
            # Clean up the text
            text = b["ru_text"].replace("ПРЕДУПРЕЖДЕНИЕ", "<strong>⚠️ ПРЕДУПРЕЖДЕНИЕ:</strong>")
            text = text.replace("ОСТОРОЖНО", "<strong>⚠️ ОСТОРОЖНО:</strong>")
            
            items.append({
                "type": "text",
                "y0": b["bbox"][1],
                "text": text,
                "font_size": b["font_size"]
            })
            
        # 2. Image blocks
        img_info = page.get_image_info(xrefs=True)
        seen_bboxes = set() # Avoid duplicates
        for img in img_info:
            xref = img.get("xref")
            bbox = img.get("bbox")
            if not xref or not bbox: continue
            
            # Simple deduplication by coordinate rounding
            bbox_key = (round(bbox[0]), round(bbox[1]), round(bbox[2]), round(bbox[3]))
            if bbox_key in seen_bboxes: continue
            seen_bboxes.add(bbox_key)
            
            # Extract and save
            try:
                pix = fitz.Pixmap(doc, xref)
                if pix.n - pix.alpha > 3:
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                img_filename = f"img_p{page_num}_{xref}.png"
                pix.save(os.path.join(img_dir, img_filename))
                
                # Exclude ultra-small fragments (like tiny logos or background artifacts)
                if pix.width > 50 and pix.height > 50:
                    items.append({
                        "type": "image",
                        "y0": bbox[1],
                        "src": f"images/{img_filename}"
                    })
            except Exception as e:
                print(f"Skipped image {xref}: {e}")
                
        # 3. Sort Everything Top-to-Bottom
        items.sort(key=lambda x: x["y0"])
        
        # 4. Render Layout
        for item in items:
            if item["type"] == "text":
                text = item["text"]
                # Skip page numbers as we already added a clean header
                if "Стр." in text and "из" in text:
                    continue
                    
                # Typography logic based on original font size
                if item["font_size"] >= 20:
                    html_content += f"<h2>{text}</h2>\n"
                elif item["font_size"] >= 15:
                    html_content += f"<h3>{text}</h3>\n"
                else:
                    if "ПРЕДУПРЕЖДЕНИЕ" in text or "ОСТОРОЖНО" in text:
                        html_content += f'<div class="warning-box"><p>{text}</p></div>\n'
                    else:
                        html_content += f"<p>{text}</p>\n"
            elif item["type"] == "image":
                html_content += f'<img src="{item["src"]}" alt="Схема оборудования">\n'
                
        html_content += "</div>\n"

    html_content += "</body></html>"

    html_path = os.path.join(out_dir, "ADL07K10_Руководство.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"[DONE] Clean typeset manual saved to: {html_path}")

if __name__ == "__main__":
    pdf_path = sys.argv[1]
    json_path = sys.argv[2]
    out_dir = sys.argv[3]
    build_html_manual(pdf_path, json_path, out_dir)
