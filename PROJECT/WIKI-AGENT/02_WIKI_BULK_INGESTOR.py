import os
import json
import subprocess
import shutil
import time
from pathlib import Path

# Config
PROJECT_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS")
WIKI_DIR = PROJECT_ROOT / "PROJECT" / "WIKI"
EXTERNAL_DIR = PROJECT_ROOT / "PROJECT" / "EXTERNAL-LIBRARY"
QUEUE_FILE = WIKI_DIR / "sync_queue.json"

# Ensure dirs
WIKI_DIR.mkdir(parents=True, exist_ok=True)
EXTERNAL_DIR.mkdir(parents=True, exist_ok=True)

class WikiBulkIngestor:
    def __init__(self):
        print(f"[WIKI-BULK-AGENT] Nexus Agent v5.0 Hardened Loop activated.")
        self.queue = self.load_queue()

    def load_queue(self):
        try:
            with open(QUEUE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Failed to load queue: {e}")
            return []

    def run_minimal_clone(self, repo_url, target_folder):
        print(f"  > Cloning {repo_url}...")
        try:
            # Use subprocess with timeout and depth 1
            subprocess.run(["git", "clone", "--depth", "1", repo_url, str(target_folder)], 
                           check=True, capture_output=True, timeout=120)
            return True
        except Exception as e:
            print(f"  ❌ Clone failed/timed out: {e}")
            return False

    def ingest_knowledge(self, repo_path, repo_name):
        dest_folder = WIKI_DIR / repo_name.upper().replace(" ", "-")
        dest_folder.mkdir(exist_ok=True)
        count = 0
        for root, dirs, files in os.walk(repo_path):
            if any(x in root for x in [".git", "node_modules", "dist", "build"]): continue
            for file in files:
                if file.lower().endswith((".md", ".json", ".txt")):
                    src_file = Path(root) / file
                    # Targeted extraction: Readmes, tutorials, docs
                    if any(x in file.upper() for x in ["README", "CONTRIBU", "LICENSE", "DOC"]) or len(files) < 15:
                        rel_path = os.path.relpath(src_file, repo_path).replace(os.sep, "_")
                        shutil.copy2(src_file, dest_folder / rel_path)
                        count += 1
        return count

    def update_status_file(self, current_idx, total, current_repo, latest_success):
        status_file = PROJECT_ROOT / "PROJECT" / "WIKI" / "SYNC_STATUS.md"
        progress = int((current_idx / total) * 100)
        bar_len = 10
        filled = int(bar_len * current_idx / total)
        bar = "█" * filled + "░" * (bar_len - filled)
        
        content = f"""[ {bar} ] {current_idx}/{total} ({progress}%)
Текущая цель: {current_repo}
"""
        with open(status_file, "w", encoding="utf-8") as f:
            f.write(content)

    def start_loop(self):
        total = len(self.queue)
        latest_success = "None"
        print(f"[AGENT] Starting processing of {total} targets...")
        
        for i, item in enumerate(self.queue):
            repo_name = item['name']
            repo_url = item['url']
            
            # Status Update (Exact user format)
            self.update_status_file(i + 1, total, repo_name, latest_success)
            
            # Resume Check
            if (WIKI_DIR / repo_name.upper().replace(" ", "-")).exists():
                print(f"[{i+1}/{total}] Skipping {repo_name} (Already in Wiki).")
                continue
                
            print(f"[{i+1}/{total}] Syncing {repo_name}...")
            tmp_path = EXTERNAL_DIR / f"tmp_{i}"
            
            if self.run_minimal_clone(repo_url, tmp_path):
                files_found = self.ingest_knowledge(tmp_path, repo_name)
                latest_success = repo_name
                self.history.append(repo_name)
                print(f"  ✅ Extracted {files_found} knowledge nodes.")
                shutil.rmtree(tmp_path, ignore_errors=True)
                time.sleep(2)
            else:
                print(f"  ⚠️ Skipping {repo_name} due to failure.")
                
        # Final update
        self.update_status_file(total, total, "DONE", latest_success)

if __name__ == "__main__":
    ingestor = WikiBulkIngestor()
    ingestor.start_loop()
