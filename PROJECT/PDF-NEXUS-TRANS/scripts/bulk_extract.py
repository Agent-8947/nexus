import fitz
import json
import sys

def extract_all(pdf_path):
    doc = fitz.open(pdf_path)
    all_data = {}
    for i in range(len(doc)):
        page = doc.load_page(i)
        blocks = page.get_text("dict")["blocks"]
        page_items = []
        for b in blocks:
            if "lines" in b:
                text = ""
                for l in b["lines"]:
                    for s in l["spans"]:
                        text += s["text"] + " "
                page_items.append({
                    "bbox": list(b["bbox"]),
                    "en_text": text.strip(),
                    "font_size": b["lines"][0]["spans"][0]["size"] if b["lines"] and b["lines"][0]["spans"] else 11
                })
        all_data[i] = page_items
    doc.close()
    return all_data

if __name__ == "__main__":
    pdf = sys.argv[1]
    out_json = sys.argv[2]
    data = extract_all(pdf)
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
