import os
import csv
from pathlib import Path
import json

PROJECT_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS")
WIKI_DIR = PROJECT_ROOT / "PROJECT" / "WIKI"
CSV_TOP = WIKI_DIR / "github-top-stars-full-ru-final.csv"
CSV_MID = WIKI_DIR / "github-mid-stars-specialized-ru-extended.csv"
OUT_HTML = WIKI_DIR / "dashboard.html"

def load_metadata():
    metadata = {}
    
    # Load TOP repos
    if CSV_TOP.exists():
        with open(CSV_TOP, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row["Repository"].strip()
                folder = name.upper().replace(" ", "-")
                metadata[folder] = {
                    "name": name,
                    "stars": row.get("Stars", "0"),
                    "url": row.get("Link", ""),
                    "desc": row.get("Description (RU)", ""),
                    "lang": row.get("Language", ""),
                    "category": "Mainstream/Global"
                }
                
    # Load Special repos
    if CSV_MID.exists():
        with open(CSV_MID, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row["Repository"].strip()
                folder = name.upper().replace(" ", "-")
                metadata[folder] = {
                    "name": name,
                    "stars": row.get("Stars", "0"),
                    "url": row.get("Link", ""),
                    "desc": row.get("Description (RU)", ""),
                    "lang": row.get("Language", ""),
                    "category": row.get("Category", "Specialized")
                }
                
    return metadata

def build_html():
    metadata = load_metadata()
    
    # Check what is actually downloaded
    downloaded = []
    
    for item in WIKI_DIR.iterdir():
        if item.is_dir() and item.name != "__pycache__":
            folder = item.name
            info = metadata.get(folder, {
                "name": folder, "stars": "?", "url": "#",
                "desc": "Локальное зеркало архитектуры без описания.", "lang": "Unknown", "category": "System"
            })
            info["folder_name"] = folder
            downloaded.append(info)
            
    downloaded.sort(key=lambda x: int(x["stars"]) if str(x["stars"]).isdigit() else 0, reverse=True)

    # Generate HTML cards
    cards_html = ""
    for d in downloaded:
        stars_formatted = f'{int(d["stars"]):,}' if str(d["stars"]).isdigit() else d["stars"]
        cards_html += f"""
        <div class="card">
            <div class="card-header">
                <span class="category">{d["category"]}</span>
                <span class="stars">⭐ {stars_formatted}</span>
            </div>
            <h3 class="repo-name">{d["name"]}</h3>
            <div class="lang-badge">{'⌨️ ' + d["lang"] if d["lang"] else '🧬 Multi'}</div>
            <p class="desc">{d["desc"]}</p>
            <div class="actions">
                <a href="{d["url"]}" target="_blank" class="btn btn-outline">GitHub ↗</a>
                <a href="./{d["folder_name"]}" target="_blank" class="btn btn-primary">Open DNA 📂</a>
            </div>
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXUS | Intelligence Engine</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-base: #050505;
            --bg-panel: rgba(20, 20, 24, 0.6);
            --border-glow: rgba(0, 255, 170, 0.15);
            --text-main: #f0f0f0;
            --text-dim: #9aa0a6;
            --accent: #00ffaa;
            --accent-hot: #ff3366;
            --accent-blue: #00ccff;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            background-color: var(--bg-base);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(0, 255, 170, 0.04) 0%, transparent 50%),
                radial-gradient(circle at 85% 30%, rgba(0, 204, 255, 0.04) 0%, transparent 50%);
            min-height: 100vh;
        }}
        
        header {{
            padding: 4rem 2rem;
            text-align: center;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            background: linear-gradient(180deg, rgba(10,10,12,0.8) 0%, rgba(5,5,5,0) 100%);
            backdrop-filter: blur(10px);
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        
        h1 {{
            font-size: 3rem;
            font-weight: 800;
            letter-spacing: -1px;
            background: linear-gradient(90deg, var(--text-main), var(--text-dim));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }}
        
        .stats {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            color: var(--accent);
        }}
        
        .stats div {{
            background: rgba(0, 255, 170, 0.05);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            border: 1px solid var(--border-glow);
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 3rem 2rem;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 2rem;
        }}

        .card {{
            background: var(--bg-panel);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 16px;
            padding: 1.5rem;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            backdrop-filter: blur(12px);
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }}

        .card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--accent), transparent);
            opacity: 0;
            transition: opacity 0.3s;
        }}

        .card:hover {{
            transform: translateY(-5px);
            border-color: var(--border-glow);
            box-shadow: 0 10px 30px -10px rgba(0, 255, 170, 0.1);
        }}

        .card:hover::before {{ opacity: 1; }}

        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
        }}

        .category {{
            color: var(--accent-blue);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .stars {{ color: #ffd700; }}

        .repo-name {{
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #fff;
            word-break: break-all;
        }}
        
        .lang-badge {{
            display: inline-block;
            font-size: 0.75rem;
            padding: 0.2rem 0.6rem;
            background: rgba(255,255,255,0.05);
            border-radius: 4px;
            color: var(--text-dim);
            margin-bottom: 1rem;
        }}

        .desc {{
            color: var(--text-dim);
            font-size: 0.95rem;
            line-height: 1.5;
            margin-bottom: 2rem;
            flex-grow: 1;
            display: -webkit-box;
            -webkit-line-clamp: 4;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}

        .actions {{
            display: flex;
            gap: 1rem;
            margin-top: auto;
        }}

        .btn {{
            flex: 1;
            text-align: center;
            padding: 0.7rem;
            border-radius: 8px;
            text-decoration: none;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            font-weight: 700;
            transition: all 0.2s ease;
        }}

        .btn-outline {{
            background: transparent;
            color: var(--text-main);
            border: 1px solid rgba(255,255,255,0.1);
        }}

        .btn-outline:hover {{ background: rgba(255,255,255,0.05); }}

        .btn-primary {{
            background: rgba(0, 255, 170, 0.1);
            color: var(--accent);
            border: 1px solid var(--accent);
        }}

        .btn-primary:hover {{
            background: var(--accent);
            color: #000;
            box-shadow: 0 0 15px rgba(0, 255, 170, 0.4);
        }}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-track {{ background: var(--bg-base); }}
        ::-webkit-scrollbar-thumb {{ background: #333; border-radius: 4px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: var(--accent); }}
        
    </style>
</head>
<body>

    <header>
        <h1>NEXUS Intelligence Factory</h1>
        <div class="stats">
            <div>Nodes Cloned: {len(downloaded)}</div>
            <div>Knowledge Segments: 1400+</div>
            <div>Status: Autonomous Engine Online</div>
        </div>
    </header>

    <div class="container">
        {cards_html}
    </div>

</body>
</html>
"""
    
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"✅ Dashboard generated at {OUT_HTML} with {len(downloaded)} local repos.")

if __name__ == "__main__":
    build_html()
