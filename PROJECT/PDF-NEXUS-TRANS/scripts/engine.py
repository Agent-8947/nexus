"""
PDF Translation Engine v2.0
Redact original text → Insert Russian translation.
Uses PyMuPDF (fitz) with proper font registration and batch redaction.
"""

import fitz
import json
import os
import sys


def extract_page_text(pdf_path, page_num):
    """Extract text blocks with bbox and font info from a single page."""
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    blocks = page.get_text("dict")["blocks"]

    text_data = []
    for b in blocks:
        if "lines" in b:
            block_text = ""
            for line in b["lines"]:
                for span in line["spans"]:
                    block_text += span["text"] + " "
            text_data.append({
                "bbox": list(b["bbox"]),
                "text": block_text.strip(),
                "font_size": b["lines"][0]["spans"][0]["size"] if b["lines"] and b["lines"][0]["spans"] else 11.0
            })
    doc.close()
    return text_data


def apply_translations(input_pdf, output_pdf, translations_json_path):
    """
    Two-pass approach per page:
      Pass 1: Add ALL redaction annotations for the page.
      Pass 2: Apply redactions ONCE, then insert all translated text.
    """
    doc = fitz.open(input_pdf)
    with open(translations_json_path, 'r', encoding='utf-8') as f:
        translations = json.load(f)

    font_path = r"C:\Windows\Fonts\arial.ttf"

    for page_idx, page_data in translations.items():
        page_num = int(page_idx)
        if page_num >= len(doc):
            continue
        page = doc.load_page(page_num)

        # --- Pass 1: Collect all redaction rects for this page ---
        items_to_insert = []
        for item in page_data:
            ru_text = item.get("ru_text", "")
            en_text = item.get("en_text", "")
            # Skip empty or identical (untranslated) blocks
            if not ru_text or not en_text:
                continue
            # Skip if text was not translated (identical to original)
            if ru_text == en_text:
                continue

            rect = fitz.Rect(item["bbox"])
            # Skip tiny rects (noise)
            if rect.width < 5 or rect.height < 5:
                continue

            # Add redaction annotation (white fill to erase original text)
            page.add_redact_annot(rect, fill=(1, 1, 1))
            items_to_insert.append(item)

        # --- Apply ALL redactions at once for this page ---
        if items_to_insert:
            page.apply_redactions()

        # --- Pass 2: Insert translated text into cleared areas ---
        for item in items_to_insert:
            rect = fitz.Rect(item["bbox"])
            ru_text = item["ru_text"]
            font_size = item.get("font_size", 10.0)

            # Compensate for Russian text expansion (typically 20-30% longer)
            en_len = len(item.get("en_text", ""))
            ru_len = len(ru_text)
            if en_len > 0 and ru_len > en_len * 1.1:
                ratio = en_len / ru_len
                font_size = max(font_size * ratio, 5.0)

            # Expand rect height slightly to accommodate Cyrillic descenders
            expanded_rect = fitz.Rect(
                rect.x0,
                rect.y0,
                rect.x1,
                rect.y1 + 2  # 2pt buffer
            )

            # Insert text using font file directly
            rc = page.insert_textbox(
                expanded_rect,
                ru_text,
                fontsize=font_size,
                fontname="arial-ru",
                fontfile=font_path,
                color=(0, 0, 0),
                align=0,  # Left-aligned (correct for manuals)
            )

            # If text didn't fit (rc < 0), try with smaller font
            if rc < 0:
                font_size *= 0.7
                page.insert_textbox(
                    expanded_rect,
                    ru_text,
                    fontsize=max(font_size, 4.0),
                    fontname="arial-ru",
                    fontfile=font_path,
                    color=(0, 0, 0),
                    align=0,
                )

    # Save output
    output_pdf = os.path.abspath(output_pdf)
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    doc.save(output_pdf, garbage=4, deflate=True)
    doc.close()
    print(f"[OK] Saved: {output_pdf}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "extract":
        pdf = sys.argv[2]
        pg = int(sys.argv[3])
        print(json.dumps(extract_page_text(pdf, pg), ensure_ascii=False))
    elif cmd == "apply":
        in_pdf = sys.argv[2]
        out_pdf = sys.argv[3]
        trans_json = sys.argv[4]
        apply_translations(in_pdf, out_pdf, trans_json)
