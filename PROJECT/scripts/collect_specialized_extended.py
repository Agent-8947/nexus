import requests
import csv
import time
from pathlib import Path
from deep_translator import GoogleTranslator
import sys

# Config
IN_FILE = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\github-mid-stars-specialized-ru.csv")
OUT_FILE = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\github-mid-stars-specialized-ru-extended.csv")

QUERIES = {
    "Math & Mathematics": "math mathematics stars:2000..50000",
    "Data Analysis": "data science analysis stars:2000..50000",
    "Planning & Forecasting": "planning forecasting prediction stars:2000..50000",
    "Algorithms": "algorithms stars:2000..50000",
    "Psychology & Cognition": "psychology cognitive behavior stars:2000..50000",
    "Jurisprudence & Legal": "law legal jurisprudence stars:2000..50000"
}

def translate(text):
    if not text: return ""
    try:
        return GoogleTranslator(source='auto', target='ru').translate(text)
    except:
        return text

def main():
    collected = []
    seen = set()
    
    # Load previously seen so we don't duplicate
    if IN_FILE.exists():
        with open(IN_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                collected.append(row)
                seen.add(row["Repository"].lower())
        print(f"[*] Loaded {len(collected)} existing items from previous run/file.")

    for category, query in QUERIES.items():
        print(f"\n[*] Глубокий поиск: {category}")
        pages = 5 # fetch 5 pages * 100 = 500 max per category
        added_in_category = 0
        
        for page in range(1, pages + 1):
            url = "https://api.github.com/search/repositories"
            params = {
                "q": query,
                "sort": "stars",
                "order": "desc",
                "per_page": 100,
                "page": page
            }
            headers = {"Accept": "application/vnd.github.v3+json"}
            
            try:
                req = requests.get(url, params=params, headers=headers, timeout=15)
                if req.status_code == 200:
                    items = req.json().get("items", [])
                    if not items:
                        break # no more pages
                        
                    for item in items:
                        repo_name = item.get("name", "")
                        if repo_name.lower() in seen:
                            continue
                            
                        seen.add(repo_name.lower())
                        desc = (item.get("description") or "").replace('\n', ' ').replace('\r', '')
                        desc_ru = translate(desc)
                        
                        collected.append({
                            "Category": category,
                            "Repository": repo_name,
                            "Link": item.get("html_url", ""),
                            "Stars": item.get("stargazers_count", 0),
                            "Language": item.get("language", ""),
                            "Description (RU)": desc_ru
                        })
                        added_in_category += 1
                        
                        if added_in_category > 0 and added_in_category % 20 == 0:
                            print(f"  ... найдено и переведено: {added_in_category}")
                            
                elif req.status_code == 403: # rate limit
                    print("  [!] API Rate limit. Ожидание 20 сек...")
                    time.sleep(20)
                else:
                    print(f"❌ Ошибка API: {req.status_code}")
                    break
            except Exception as e:
                print(f"❌ Ошибка: {e}")
                break
                
            time.sleep(4) # delay to avoid rapid rate limits
            
        print(f"   ✅ Добавлено {added_in_category} новых проектов для '{category}'.")
        
        # Save incrementally
        collected.sort(key=lambda x: int(x["Stars"]) if str(x["Stars"]).isdigit() else 0, reverse=True)
        with open(OUT_FILE, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["Category", "Repository", "Link", "Stars", "Language", "Description (RU)"])
            writer.writeheader()
            writer.writerows(collected)
            
    print(f"\n✅ Глубокий поиск завершен. Всего в базе расширено до: {len(collected)}")

if __name__ == "__main__":
    main()
