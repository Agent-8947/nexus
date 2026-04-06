import os
import shutil
from pathlib import Path

PROJECT_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS")
WIKI_PROJECT_DIR = PROJECT_ROOT / "PROJECT" / "WIKI-PROJECT"

DOMAINS = {
    "OSINT": ["osint", "recon", "crawler", "miner", "breach"],
    "LEGAL": ["legal", "contract", "license", "law", "registry"],
    "SPEC":  ["concept", "blueprint", "specification", "idea"],
    "AUDIT": ["audit", "researcher", "threat", "risk"]
}

class NexusSorterAgent:
    """Агент 12: Архивариус V2. Трёхзначная нумерация + B-префикс для Сборок."""
    def __init__(self):
        print("\n" + "=" * 58)
        print("  NEXUS AGENT 12 — ARCHIVIST V2 🧹")
        print("  Standard: 001/002... | Builds: B001/B002...")
        print("=" * 58 + "\n")

    def _auto_classify(self, entry):
        name_lower = entry.name.lower()
        for d, keys in DOMAINS.items():
            if any(k in name_lower for k in keys): return d
        return "MISC"

    def _strip_old_prefix(self, name):
        """Убирает старый двухзначный префикс если есть (01_, 02_...)"""
        import re
        return re.sub(r"^\d{2,3}[_B]*", "", name)

    def _index_directory(self, directory, is_build=False):
        """Полная переиндексация директории. Режим BUILD добавляет B-префикс."""
        entries = sorted([e for e in directory.iterdir()], key=lambda x: x.name)

        # Сначала снимаем все старые индексы
        cleaned = []
        for entry in entries:
            clean_name = self._strip_old_prefix(entry.name)
            if clean_name != entry.name:
                clean_path = directory / clean_name
                if not clean_path.exists():
                    entry.rename(clean_path)
                    cleaned.append(clean_path)
                else:
                    cleaned.append(entry)
            else:
                cleaned.append(entry)

        # Теперь заново нумеруем по порядку
        entries = sorted([e for e in directory.iterdir()], key=lambda x: x.name)
        for i, entry in enumerate(entries, start=1):
            clean_name = self._strip_old_prefix(entry.name)
            
            if is_build:
                new_name = f"B{i:03d}_{clean_name}"
            else:
                new_name = f"{i:03d}_{clean_name}"

            dest = directory / new_name
            if entry.name != new_name and not dest.exists():
                try:
                    entry.rename(dest)
                    print(f"  [#] {entry.name} -> {new_name}")
                except PermissionError:
                    print(f"  [!] Skipped {entry.name} (locked by system/editor)")


    def organize_workspace(self):
        """Полный цикл: Сортировка -> Sub-классификация -> Тотальная индексация."""
        print(f"[*] Starting V2 organization in {WIKI_PROJECT_DIR.name}...\n")

        # 1. Корень: файлы -> в домены
        for file in [f for f in WIKI_PROJECT_DIR.iterdir() if f.is_file()]:
            cat = self._auto_classify(file)
            target = WIKI_PROJECT_DIR / cat
            target.mkdir(exist_ok=True)
            shutil.move(str(file), str(target / file.name))

        # 2. Внутри доменов: файлы -> в SPEC / AUDIT / MISC
        for domain in [d for d in WIKI_PROJECT_DIR.iterdir() if d.is_dir() and d.name in DOMAINS]:
            for file in [f for f in domain.iterdir() if f.is_file()]:
                name_low = file.name.lower()
                sub = "MISC"
                if any(x in name_low for x in ["concept", "spec", "blueprint"]): sub = "SPEC"
                elif any(x in name_low for x in ["audit", "research", "report"]): sub = "AUDIT"
                target_sub = domain / sub
                target_sub.mkdir(exist_ok=True)
                shutil.move(str(file), str(target_sub / file.name))

            # 3. Индексация подпапок
            for sub_folder in [d for d in domain.iterdir() if d.is_dir()]:
                is_build = sub_folder.name == "BUILD"
                print(f"  [*] Indexing: {domain.name}/{sub_folder.name}")
                self._index_directory(sub_folder, is_build=is_build)

        print("\n✅ V2 Organization & Indexing complete.")
        print("   Files: 001_... | Builds: B001_...")

if __name__ == "__main__":
    sorter = NexusSorterAgent()
    sorter.organize_workspace()
