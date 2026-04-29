import os
from docx import Document
import json

def parse_docx(filepath):
    doc = Document(filepath)
    text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    return text

en_text = parse_docx("INBOX/EN/NEXUS_EN_COMBINED.docx")
ru_text = parse_docx("INBOX/RU/NEXUS_RU_COMBINED.docx")
ua_text = parse_docx("INBOX/UA/NEXUS_UA_COMBINED.docx")

data = {"en": en_text, "ru": ru_text, "ua": ua_text}
with open("extracted_docs.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Extraction complete.")
