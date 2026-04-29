import requests
import csv
import time
from pathlib import Path

# Config
OUT_FILE = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\github-mid-stars-specialized.csv")

# Domains to search mapped to GitHub queries
QUERIES = {
    "Math & Mathematics": "math mathematics stars:2000..50000",
    "Data Analysis": "data science analysis stars:2000..50000",
    "Planning & Forecasting": "planning forecasting prediction stars:2000..50000",
    "Algorithms": "algorithms stars:2000..50000",
    "Psychology & Cognition": "psychology cognitive behavior stars:2000..50000",
    "Jurisprudence & Legal": "law legal jurisprudence stars:2000..50000"
}

def search_github(query, limit=50):
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": limit
    }
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    print(f"[*] Сканирование: {query}")
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

def main():
    collected = []
    seen = set()
    
    for category, query in QUERIES.items():
        items = search_github(query, limit=40)
        category_count = 0
        for item in items:
            repo_name = item.get("name", "")
            if repo_name in seen:
                continue
            
            seen.add(repo_name)
            collected.append({
                "Category": category,
                "Repository": repo_name,
                "Link": item.get("html_url", ""),
                "Stars": item.get("stargazers_count", 0),
                "Language": item.get("language", ""),
                "Description": (item.get("description") or "").replace('\n', ' ').replace('\r', '')
            })
            category_count += 1
            
        print(f"   ✅ Найдено {category_count} уникальных проектов для категории '{category}'.")
        time.sleep(2) # Anti-ratelimit
        
    print(f"[*] Всего собрано {len(collected)} проектов. Сохранение в CSV...")
    
    # Sort globally by stars descending
    collected.sort(key=lambda x: x["Stars"], reverse=True)
    
    with open(OUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Category", "Repository", "Link", "Stars", "Language", "Description"])
        writer.writeheader()
        writer.writerows(collected)
        
    print(f"✅ Успешно сохранено в {OUT_FILE.name}")

if __name__ == "__main__":
    main()
