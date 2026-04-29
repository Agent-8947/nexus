import csv
from pathlib import Path
from deep_translator import GoogleTranslator

IN_FILE = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\github-mid-stars-specialized.csv")
OUT_FILE = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\github-mid-stars-specialized-ru.csv")

def translate(text):
    if not text:
        return ""
    try:
        return GoogleTranslator(source='auto', target='ru').translate(text)
    except:
        return text

def main():
    collected = []
    with open(IN_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc_ru = translate(row["Description"])
            row["Description"] = desc_ru
            collected.append(row)
            print(f"Translating: {row['Repository']}...")
            
    with open(OUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Category", "Repository", "Link", "Stars", "Language", "Description"])
        writer.writeheader()
        writer.writerows(collected)
        
    print(f"✅ Translated and saved to {OUT_FILE.name}")

if __name__ == "__main__":
    main()
