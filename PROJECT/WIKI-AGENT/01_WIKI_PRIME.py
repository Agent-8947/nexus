"""
NEXUS Wiki Autonomous Prime Agent v6.0

Mission: Ingest ALL 381 repositories from the GitHub Intelligence Database.
Strategy: Adaptive  full clone for small repos, README-only for giants.
Memory: UNRESTRICTED. CPU throttle only at 95%.
"""

import os
import csv
import json
import subprocess
import shutil
import time
import psutil
from pathlib import Path
from datetime import datetime

# ==========================================
# CONFIGURATION
# ==========================================
PROJECT_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS")
DATA_SOURCE  = PROJECT_ROOT / "PROJECT" / "WIKI" / "github-mid-stars-specialized-ru-extended.csv"
WIKI_DIR     = PROJECT_ROOT / "PROJECT" / "WIKI"
TMP_DIR      = PROJECT_ROOT / "PROJECT" / "EXTERNAL-LIBRARY" / "_clone_tmp"
STATUS_FILE  = WIKI_DIR / "SYNC_STATUS.md"
REPORT_FILE  = WIKI_DIR / "INGESTION_REPORT.json"

MAX_CPU_LOAD     = 95.0   # Only throttle at extreme load
CLONE_TIMEOUT    = 300    # 5 minutes max per clone
COOLDOWN_SEC     = 2      # Seconds between repos
BIG_REPO_CUTOFF  = 200    # Files threshold: above this = "big repo" mode

# Files we ALWAYS want (the "DNA")
WISDOM_PATTERNS = [
    "README", "ARCHITECTURE", "DESIGN", "CONTRIBUTING", "CHANGELOG",
    "GUIDE", "TUTORIAL", "ROADMAP", "SPEC", "API", "OVERVIEW",
    "GETTING_STARTED", "QUICKSTART", "INSTALL", "SETUP", "CONFIG",
    "FAQ", "SECURITY", "LICENSE", "MANIFEST", "SUMMARY",
]

# Directories to ALWAYS skip during walk
SKIP_DIRS = {
    ".git", "node_modules", "dist", "build", "venv", ".venv",
    "__pycache__", ".tox", ".eggs", "vendor", "third_party",
    "test", "tests", "benchmark", "benchmarks", "examples",
    ".github", ".circleci", ".azure", "fixtures", "testdata",
    "e2e", "cypress", "coverage", ".nyc_output", "target",
}

# File extensions worth keeping
GOOD_EXTENSIONS = {".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".cfg", ".ini", ".rst"}


class NexusWikiPrimeV6:

    def __init__(self):
        self._banner()
        WIKI_DIR.mkdir(parents=True, exist_ok=True)
        TMP_DIR.mkdir(parents=True, exist_ok=True)

        self.existing = self._scan_existing()
        self.targets  = self._load_targets()
        self.report   = {"started": datetime.now().isoformat(), "processed": [], "skipped": [], "failed": []}

    #  UI 
    @staticmethod
    def _banner():
        print("\n" + "=" * 58)
        print("  NEXUS WIKI PRIME v6.0  FULL SPECTRUM INGESTION")
        print("  RAM: UNRESTRICTED | CPU Throttle: 95%")
        print("  Strategy: Adaptive (Full / DNA-only)")
        print("=" * 58 + "\n")

    #  Data Loading 
    def _scan_existing(self):
        """Return set of upper-cased folder names already in WIKI."""
        return {f.name for f in WIKI_DIR.iterdir() if f.is_dir() and f.name != "__pycache__"}

    def _load_targets(self):
        """Read CSV, skip already-ingested, return ordered list."""
        targets = []
        with open(DATA_SOURCE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row["Repository"].strip()
                folder_name = name.upper().replace(" ", "-")
                if folder_name in self.existing:
                    continue
                targets.append({
                    "name": name,
                    "folder": folder_name,
                    "url": row["Link"].strip(),
                    "stars": int(row["Stars"]) if row["Stars"].strip().isdigit() else 0,
                })
        print(f"[SCAN] {len(self.existing)} already ingested, {len(targets)} remaining.\n")
        return targets

    #  System Guard 
    @staticmethod
    def _wait_for_cpu():
        """Block until CPU drops below threshold."""
        while True:
            cpu = psutil.cpu_percent(interval=0.5)
            if cpu < MAX_CPU_LOAD:
                return
            print(f"   CPU {cpu:.0f}%  cooling down")
            time.sleep(5)

    #  Clone 
    def _clone(self, url: str, dest: Path) -> bool:
        """Shallow-clone a repo. Returns True on success."""
        if dest.exists():
            shutil.rmtree(dest, ignore_errors=True)
            
        # Inject GITHUB PAT Token for authenticated requests to bypass Rate Limits
        auth_url = url.replace("https://github.com/", "https://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@github.com/")
        
        try:
            subprocess.run(
                ["git", "clone", "--depth", "1", "--single-branch", auth_url, str(dest)],
                check=True, capture_output=True, timeout=CLONE_TIMEOUT,
            )
            return True
        except subprocess.TimeoutExpired:
            print(f"   Clone timed out after {CLONE_TIMEOUT}s")
            return False
        except subprocess.CalledProcessError as e:
            stderr = e.stderr.decode(errors="ignore")[:200] if e.stderr else ""
            print(f"   Clone error: {stderr}")
            return False

    #  Knowledge Extraction 
    def _count_files(self, root: Path) -> int:
        """Fast file count ignoring skip dirs."""
        total = 0
        for _, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            total += len(files)
            if total > BIG_REPO_CUTOFF:
                return total  # early exit  we know it's big
        return total

    def _is_wisdom_file(self, filename: str) -> bool:
        """Check if filename matches any wisdom pattern."""
        upper = filename.upper()
        for pat in WISDOM_PATTERNS:
            if pat in upper:
                return True
        return False

    def _extract(self, clone_path: Path, dest: Path) -> int:
        """Extract valuable files. Strategy adapts to repo size."""
        dest.mkdir(exist_ok=True)

        file_count = self._count_files(clone_path)
        is_big = file_count > BIG_REPO_CUTOFF

        if is_big:
            print(f"   BIG REPO ({file_count}+ files)  DNA-only extraction")
        else:
            print(f"   Standard repo ({file_count} files)  full knowledge extraction")

        extracted = 0
        for root, dirs, files in os.walk(clone_path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

            for fname in files:
                ext = Path(fname).suffix.lower()

                # Skip binary / irrelevant files
                if ext not in GOOD_EXTENSIONS:
                    continue

                src = Path(root) / fname

                # For big repos: only grab wisdom files
                if is_big and not self._is_wisdom_file(fname):
                    continue

                # For any repo: skip huge files (>500KB)
                try:
                    if src.stat().st_size > 512_000:
                        continue
                except OSError:
                    continue

                # Copy with flattened name
                flat_name = os.path.relpath(src, clone_path).replace(os.sep, "_")
                try:
                    shutil.copy2(src, dest / flat_name)
                    extracted += 1
                except Exception:
                    pass

        # Fallback: if we got nothing, at least grab the root README
        if extracted == 0:
            for candidate in ["README.md", "readme.md", "README.rst", "README.txt", "README"]:
                readme = clone_path / candidate
                if readme.exists():
                    shutil.copy2(readme, dest / candidate)
                    extracted = 1
                    break

        return extracted

    #  Status File 
    def _update_status(self, idx: int, total: int, name: str, stats: dict):
        progress = int(idx / total * 100) if total else 0
        bar_len = 30
        filled = int(bar_len * progress / 100)
        bar = "" * filled + "" * (bar_len - filled)

        ok = stats.get("ok", 0)
        fail = stats.get("fail", 0)
        skip = stats.get("skip", 0)

        txt = f"""# NEXUS Wiki Ingestion  Prime v6.0
[ {bar} ] {idx}/{total} ({progress}%)

**Текущий узел**: `{name}`
**Успешно**: {ok} | **Ошибки**: {fail} | **Пропущено (уже есть)**: {skip}

> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        STATUS_FILE.write_text(txt, encoding="utf-8")

    #  Main Loop 
    def run(self):
        total = len(self.targets)
        if total == 0:
            print(" All 381 repositories are already ingested. Nothing to do.")
            return

        stats = {"ok": len(self.existing), "fail": 0, "skip": len(self.existing)}

        for idx, t in enumerate(self.targets, start=1):
            name = t["name"]
            folder = t["folder"]
            url = t["url"]
            dest = WIKI_DIR / folder

            self._update_status(idx, total, name, stats)
            self._wait_for_cpu()

            print(f"[{idx}/{total}] {name}  {t['stars']:,}")

            clone_dest = TMP_DIR / f"repo_{idx}"
            ok = self._clone(url, clone_dest)

            if ok:
                nodes = self._extract(clone_dest, dest)
                print(f"   {nodes} knowledge segments extracted.")
                stats["ok"] += 1
                self.report["processed"].append({"name": name, "nodes": nodes})
            else:
                stats["fail"] += 1
                self.report["failed"].append({"name": name, "url": url})
                print(f"   Skipped (clone failed). Continuing")

            # Always clean up tmp
            shutil.rmtree(clone_dest, ignore_errors=True)
            time.sleep(COOLDOWN_SEC)

        # Final status
        self._update_status(total, total, "DONE ", stats)
        self.report["finished"] = datetime.now().isoformat()
        self.report["stats"] = stats
        REPORT_FILE.write_text(json.dumps(self.report, indent=2, ensure_ascii=False), encoding="utf-8")

        print(f"\n{'=' * 58}")
        print(f"  MISSION COMPLETE")
        print(f"  Успешно: {stats['ok']} | Ошибки: {stats['fail']}")
        print(f"  Отчёт: {REPORT_FILE}")
        print(f"{'=' * 58}\n")


if __name__ == "__main__":
    agent = NexusWikiPrimeV6()
    agent.run()
