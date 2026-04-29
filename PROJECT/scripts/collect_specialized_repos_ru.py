import requests
import csv
import time
from pathlib import Path
from deep_translator import GoogleTranslator

# Config
OUT_FILE = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\github-mid-stars-specialized-ru.csv")

QUERIES = {
    "Math & Mathematics": "math mathematics stars:2000..50000",
    "Data Analysis": "data science analysis stars:2000..50000",
    "Planning & Forecasting": "planning forecasting prediction stars:2000..50000",
    "Algorithms": "algorithms stars:2000..50000",
    "Psychology & Cognition": "psychology cognitive behavior stars:2000..50000",
    "Jurisprudence & Legal": "law legal jurisprudence stars:2000..50000"
}

def search_github(query, limit=100):
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": limit
    }
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    print(f"\n[*] Сканирование: {query}")
    try:
        req = requests.get(url, params=params, headers=headers, timeout=15)
        if req.status_code == 200:
            return req.json().get("items", [])
        else:
            print(f"❌ Ошибка API: {req.status_code} - {req.text}")
            return []
    except Exception as e:
        print(f"❌ Ошибка соединения: {e}")
        return []

def translate(text):
    if not text:
        return ""
    try:
        # Using Google Translate via alternative requests if rate limited but deep_translator handles it reasonably for small batches
        return GoogleTranslator(source='auto', target='ru').translate(text)
    except:
        return text

def main():
    collected = []
    seen = set()
    
    for category, query in QUERIES.items():
        items = search_github(query, limit=100) # Increased to 100 per category
        category_count = 0
        for i, item in enumerate(items):
            repo_name = item.get("name", "")
            if repo_name in seen:
                continue
                
            seen.add(repo_name)
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
            category_count += 1
            if i > 0 and i % 20 == 0:
                print(f"  ... переведено {i}/{len(items)}")
            
        print(f"   ✅ Найдено и переведено {category_count} проектов для '{category}'.")
        time.sleep(3)
        
    print(f"\n[*] Всего собрано {len(collected)} проектов. Сохранение...")
    collected.sort(key=lambda x: x["Stars"], reverse=True)
    
    with open(OUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Category", "Repository", "Link", "Stars", "Language", "Description (RU)"])
        writer.writeheader()
        writer.writerows(collected)
        
    print(f"✅ Успешно сохранено в {OUT_FILE.name}")

if __name__ == "__main__":
    main()
