import requests
import json
import csv
import time
from pathlib import Path

SAVE_PATH_MD = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\github-top-stars-full.md")
SAVE_PATH_CSV = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\github-top-stars-full-ru.csv")

def collect_repos():
    # NO AUTH HEADERS (avoiding 401 Gdrive token issues)
    headers = {"Accept": "application/vnd.github.v3+json"}

    all_repos = []
    print("[NEXUS] Starting PUBLIC deep collection (50k - 500k stars)...")
    
    for page in range(1, 11): # Up to 1000 items
        url = f"https://api.github.com/search/repositories?q=stars:50000..500000&sort=stars&order=desc&per_page=100&page={page}"
        print(f"  > Fetching page {page}...")
        
        while True:
            res = requests.get(url, headers=headers, timeout=20)
            if res.status_code == 200:
                data = res.json()
                items = data.get("items", [])
                if not items: break
                
                for item in items:
                    stars = item["stargazers_count"]
                    if stars < 50000: continue
                    all_repos.append({
                        "name": item["name"],
                        "url": item["html_url"],
                        "stars": stars,
                        "desc": item["description"] or "None"
                    })
                
                if items[-1]["stargazers_count"] < 50000: 
                    print(f"  > Reached lower limit (50k) on page {page}.")
                    break
                
                # Public API limit is 10/min. We need to wait.
                print("  > Waiting 6.5s to avoid rate limits...")
                time.sleep(6.5) 
                break
            elif res.status_code == 403: # Rate limit
                reset_time = int(res.headers.get("X-RateLimit-Reset", time.time() + 60))
                wait_sec = max(1, reset_time - int(time.time()) + 1)
                print(f"  ⚠️ Rate limit hit. Waiting {wait_sec} seconds...")
                time.sleep(wait_sec)
            else:
                print(f"  ❌ Error on page {page}: {res.status_code} - {res.text}")
                return # Stop on other errors

        # Final check to exit page loop if last item < 50k
        if all_repos and all_repos[-1]["stars"] < 50000: break

    print(f"✅ Total repos collected: {len(all_repos)}")
    
    # Save as Markdown
    with open(SAVE_PATH_MD, "w", encoding="utf-8") as f:
        f.write("# GitHub Repositories (50k - 500k Stars)\n\n| # | Repository | Stars | Description |\n|---|---|---|---|\n")
        for i, r in enumerate(all_repos, 1):
            f.write(f"| {i} | [{r['name']}]({r['url']}) | {r['stars']} | {r['desc']} |\n")

    # Save as CSV 
    with open(SAVE_PATH_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["#", "Repository", "Link", "Stars", "Description"])
        for i, r in enumerate(all_repos, 1):
            writer.writerow([i, r['name'], r['url'], r['stars'], r['desc']])

    print(f"✅ Success.")

if __name__ == "__main__":
    collect_repos()
