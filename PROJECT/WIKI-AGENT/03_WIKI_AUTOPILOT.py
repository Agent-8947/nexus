import os
import subprocess
import shutil
from pathlib import Path

# Config
PROJECT_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS")
WIKI_DIR = PROJECT_ROOT / "PROJECT" / "WIKI"
EXTERNAL_DIR = PROJECT_ROOT / "PROJECT" / "EXTERNAL-LIBRARY"
MANIFEST_FILE = WIKI_DIR / "inbox_repos.csv"  # Downloaded Manifest

# Ensure directories
WIKI_DIR.mkdir(parents=True, exist_ok=True)
EXTERNAL_DIR.mkdir(parents=True, exist_ok=True)

class WikiAutopilot:
    def __init__(self):
        print("[NEXUS-WIKI-AGENT] Autopilot initialized.")

    def run_minimal_clone(self, repo_url, target_folder):
        """Perform a shallow clone to save space."""
        try:
            print(f"  > Cloning {repo_url}...")
            subprocess.run(["git", "clone", "--depth", "1", repo_url, str(target_folder)], 
                           check=True, capture_output=True)
            return True
        except Exception as e:
            print(f"  ❌ Failed to clone {repo_url}: {e}")
            return False

    def ingest_repo_knowledge(self, repo_path, repo_name):
        """Extract only MD and JSON files into a flat Wiki structure."""
        print(f"  > Extracting knowledge from {repo_name}...")
        dest_folder = WIKI_DIR / repo_name.upper()
        dest_folder.mkdir(exist_ok=True)
        
        count = 0
        for root, dirs, files in os.walk(repo_path):
            # Skip heavy folders
            if any(x in root for x in [".git", "node_modules", "dist", "build"]):
                continue
                
            for file in files:
                if file.lower().endswith((".md", ".json", ".txt")):
                    src_file = Path(root) / file
                    # We only care about README, DOCS, or important guides
                    if "README" in file.upper() or "DOC" in root.upper() or len(files) < 10:
                        rel_path = os.path.relpath(src_file, repo_path).replace(os.sep, "_")
                        shutil.copy2(src_file, dest_folder / rel_path)
                        count += 1
        print(f"  ✅ Ingested {count} core files into Wiki/{repo_name.upper()}")

    def process_queue(self, manifest_data, limit=5):
        """Process a limited number of items from the manifest."""
        processed = 0
        for item in manifest_data:
            if processed >= limit:
                break
            
            repo_name = item['name']
            repo_url = item['url']
            
            # Skip if already in wiki
            if (WIKI_DIR / repo_name.upper()).exists():
                continue
            
            print(f"[*] Processing {repo_name} ({repo_url})...")
            tmp_path = EXTERNAL_DIR / repo_name
            
            if self.run_minimal_clone(repo_url, tmp_path):
                self.ingest_repo_knowledge(tmp_path, repo_name)
                # Cleanup immediately
                shutil.rmtree(tmp_path, ignore_errors=True)
                processed += 1
                print(f"  🗑️ Temporary files cleaned up. System stable.")
            
        print(f"[*] Batch complete. {processed} items processed.")

if __name__ == "__main__":
    # Integration logic for the specific sheet data we saw
    # Note: normally we would parse the CSV, here I seed it with 
    # the 'Professional Programming' and 'Windows inside Docker' as high value.
    agent = WikiAutopilot()
    manifest = [
        {"name": "professional-programming", "url": "https://github.com/charlax/professional-programming"},
        {"name": "windows-docker", "url": "https://github.com/dockur/windows"},
        {"name": "lazydocker", "url": "https://github.com/jesseduffield/lazydocker"},
        {"name": "hiring-without-whiteboards", "url": "https://github.com/poteto/hiring-without-whiteboards"},
        {"name": "100-days-of-ml", "url": "https://github.com/Avik-Jain/100-Days-Of-ML-Code"}
    ]
    agent.process_queue(manifest, limit=3) # Start with 3 to be safe
