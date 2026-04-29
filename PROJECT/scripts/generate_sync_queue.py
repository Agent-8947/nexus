import re
import json
from pathlib import Path

# Path to the raw firecrawl output we got
log_path = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\inbox_repos_raw.md")
queue_path = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI\sync_queue.json")

# If file doesn't exist, I'll use the data I remember from the turn
raw_text = """
| 384 | windows | https://github.com/dockur/windows | 50809 | Windows inside a Docker container. |
| 385 | professional-programming | https://github.com/charlax/professional-programming | 50717 | Коллекция learning resources for curious ПО engineers |
| 386 | awesome-wechat-weapp | https://github.com/justjavac/awesome-wechat-weapp | 50698 | 微信小程序开发资源汇总 :100: |
| 387 | hiring-without-whiteboards | https://github.com/poteto/hiring-without-whiteboards | 50529 | ⭐️ Companies that don't have a broken hiring process |
| 388 | lazydocker | https://github.com/jesseduffield/lazydocker | 50519 | The lazier way to manage everything docker |
| 389 | 100-Days-Of-ML-Code | https://github.com/Avik-Jain/100-Days-Of-ML-Code | 50316 | 100 Days of ML Coding |
| 390 | bulma | https://github.com/jgthms/bulma | 50067 | Modern CSS фреймворк based on Flexbox |
""" # (Note: I will use a more complete extraction logic in the script)

def extract_manifest():
    # Regex to find github links in markdown tables
    # | index | name | url | stars | desc |
    pattern = r"\|\s*\d+\s*\|\s*([^|]+)\|\s*(https://github\.com/[^\s|]+)\s*\|"
    
    # Try different encodings for PowerShell redirects
    try:
        with open(log_path, "r", encoding="utf-16") as f:
            content = f.read()
    except:
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
    matches = re.findall(pattern, content)
    queue = []
    for name, url in matches:
        queue.append({
            "name": name.strip(),
            "url": url.strip()
        })
    
    with open(queue_path, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2)
    
    print(f"✅ Queue generated: {len(queue)} repositories ready for processing.")

if __name__ == "__main__":
    # First, let's make sure the log file exists with the firecrawl data
    # (In a real flow I'd have saved the firecrawl output there)
    extract_manifest()
