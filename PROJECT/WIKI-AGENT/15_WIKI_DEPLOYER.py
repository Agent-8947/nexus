"""
NEXUS Agent 15 — WIKI_DEPLOYER
Mission: Push builds to GitHub and deploy frontend to Vercel.
"""

import os
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS")
WIKI_PROJECT_DIR = PROJECT_ROOT / "PROJECT" / "WIKI-PROJECT"

class NexusDeployerAgent:
    def __init__(self):
        print("\n" + "="*60)
        print("  NEXUS AGENT 15 — THE DEPLOYMENT MANAGER V1.0")
        print("  Mission: CI/CD • GitHub Release • Vercel Deploy")
        print("="*60 + "\n")

    def find_latest_build(self):
        build_dirs = []
        for domain_dir in WIKI_PROJECT_DIR.iterdir():
            if not domain_dir.is_dir(): continue
            bp = domain_dir / "BUILD"
            if bp.exists():
                for item in bp.iterdir():
                    if item.is_dir() and (item.name.startswith("B") or "PROD_" in item.name):
                        build_dirs.append(item)
        return sorted(build_dirs)[-1] if build_dirs else None

    def inject_dynamic_github_link(self, build_path):
        gh_cmd = '"C:\\Program Files\\GitHub CLI\\gh.exe"' if Path("C:\\Program Files\\GitHub CLI\\gh.exe").exists() else "gh"
        print("  [*] Fetching active GitHub username...")
        res = subprocess.run(f'{gh_cmd} api user -q .login', capture_output=True, text=True, shell=True)
        if res.returncode == 0 and res.stdout.strip():
            username = res.stdout.strip()
            print(f"  [+] Active GitHub user: {username}")
            
            index_file = build_path / "landing" / "index.html"
            if index_file.exists():
                content = index_file.read_text(encoding="utf-8")
                # Update link to actual repo
                if "https://github.com/Antigravity-NEXUS/" in content:
                    content = content.replace("https://github.com/Antigravity-NEXUS/", f"https://github.com/{username}/")
                    index_file.write_text(content, encoding="utf-8")
                    print(f"  [+] Injected dynamic GitHub link into navbar.")
            return username
        return "Antigravity-NEXUS"

    def deploy_to_github(self, build_path):
        print(f"[*] Deploying to GitHub: {build_path.name}")
        cwd = str(build_path)
        
        # 0. Inject correct github logic
        username = self.inject_dynamic_github_link(build_path)

        # 1. Init git
        if not (build_path / ".git").exists():
            subprocess.run(["git", "init"], cwd=cwd, capture_output=True)
            print("  [+] Git repository initialized.")
            
            # Create basic .gitignore
            gitignore = build_path / ".gitignore"
            if not gitignore.exists():
                gitignore.write_text("venv/\n__pycache__/\n*.env\n.DS_Store\n", encoding="utf-8")
        
        # 2. Add & Commit
        subprocess.run(["git", "add", "."], cwd=cwd, capture_output=True)
        res = subprocess.run(["git", "commit", "-m", "Nexus Autonomous Release"], cwd=cwd, capture_output=True)
        if b"working tree clean" in res.stdout or b"nothing to commit" in res.stdout:
            print("  [-] No new changes to commit.")
        else:
            print("  [+] Changes committed.")

        # 3. GitHub CLI create repo
        repo_name = build_path.name
        print(f"  [*] Attempting to create / push to GitHub repo: {repo_name}...")
        try:
            gh_cmd = '"C:\\Program Files\\GitHub CLI\\gh.exe"' if Path("C:\\Program Files\\GitHub CLI\\gh.exe").exists() else "gh"
            gh_res = subprocess.run(
                f'{gh_cmd} repo create {repo_name} --public --source=. --remote=origin --push',
                cwd=cwd, capture_output=True, text=True, shell=True
            )
            if gh_res.returncode == 0:
                print(f"  [+] Successfully deployed to GitHub: https://github.com/Antigravity-NEXUS/{repo_name}")
            else:
                if "already exists" in gh_res.stderr or "already exists" in gh_res.stdout:
                    print("  [*] Repo already exists. Pushing updates...")
                    push_res = subprocess.run(["git", "push", "-u", "origin", "master"], cwd=cwd, capture_output=True, shell=True)
                    if push_res.returncode != 0:
                        subprocess.run(["git", "push", "-u", "origin", "main"], cwd=cwd, capture_output=True, shell=True)
                    print("  [+] Successfully pushed updates to GitHub.")
                else:
                    print(f"  [!] GitHub CLI deployment note: {gh_res.stderr.strip() or gh_res.stdout.strip()}")
        except Exception as e:
            print(f"  [!] GitHub CLI ('gh') failed: {e}")

    def deploy_to_vercel(self, build_path):
        landing_dir = build_path / "landing"
        if not landing_dir.exists():
            print("  [!] Skip Vercel: no 'landing' dir found.")
            return

        print(f"[*] Deploying Landing Page to Vercel...")
        try:
            v_cmd = '"C:\\Users\\MAC\\AppData\\Roaming\\npm\\vercel.cmd"' if Path("C:\\Users\\MAC\\AppData\\Roaming\\npm\\vercel.cmd").exists() else "vercel"
            v_res = subprocess.run(f'{v_cmd} --prod --yes', cwd=str(landing_dir), capture_output=True, text=True, shell=True)
            
            if v_res.returncode == 0:
                lines = v_res.stdout.split('\n') + v_res.stderr.split('\n')
                url = next((l for l in lines if "vercel.app" in l or "https://" in l), "Check Vercel Dashboard")
                print(f"  [+] Deployed successfully! Url: {url}")
            else:
                print(f"  [!] Vercel failed. Need login? 'vercel login'. Error: {v_res.stderr.strip()}")
        except Exception as e:
            print(f"  [!] Vercel CLI ('vercel') failed: {e}")

if __name__ == "__main__":
    import sys
    agent = NexusDeployerAgent()
    build = Path(sys.argv[1]) if len(sys.argv) > 1 else agent.find_latest_build()
    
    if build and build.exists():
        agent.deploy_to_github(build)
        agent.deploy_to_vercel(build)
    else:
        print("No build found or path does not exist.")
