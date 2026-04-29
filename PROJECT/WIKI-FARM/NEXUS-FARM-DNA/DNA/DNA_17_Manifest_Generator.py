import os
import re
from pathlib import Path

# NEXUS MASTER MANIFEST GENERATOR v4.1 [PORTABLE + SMART HEURISTIC]
# FIX [C-01]: All paths relative to __file__

DNA_DIR    = Path(__file__).resolve().parent
FARM_ROOT  = DNA_DIR.parent.parent
VAULT_PATH = FARM_ROOT / "NEXUS-OBSIDIAN-VAULT"
OUTPUT_FILE = DNA_DIR / "DNA_05_Core_Manifest.md"


def extract_section(content: str, section_patterns: list) -> str:
    """Smart RegEx to find sections regardless of exact naming."""
    for pattern in section_patterns:
        match = re.search(
            rf"(?:^|\n)##\s+.*?{pattern}.*?\n(.*?)(?=\n##\s+|\Z)",
            content, re.DOTALL | re.IGNORECASE
        )
        if match:
            return match.group(1).strip()
    return ""


def extract_bullets(text: str, max_items: int = 5) -> str:
    """Extract bullet points intelligently."""
    if not text:
        return "N/A"
    items = []
    for line in text.split('\n'):
        clean = line.strip()
        if clean.startswith('- ') or clean.startswith('* '):
            items.append(clean.lstrip('-* ').replace('**', '').strip())
    if items:
        return " ; ".join(items[:max_items])
    return text.replace('\n', ' ').replace('**', '').strip()[:200] + "..."


def extract_code(content: str) -> str:
    """Find the first bash/python code snippet."""
    blocks = re.findall(r'```(?:bash|python|sh|js|json)?\n(.*?)```', content, re.DOTALL)
    if blocks:
        code_oneliner = blocks[0].replace('\n', ' ■ ').strip()
        return code_oneliner[:150] + ("..." if len(code_oneliner) > 150 else "")
    return "N/A"


def generate_manifest():
    if not VAULT_PATH.exists():
        print(f"[!] Vault not found: {VAULT_PATH}")
        return

    manifest_entries = []
    print("[*] Launching Semantic Extraction Engine v4.1 (PORTABLE)...")
    print(f"    Vault: {VAULT_PATH}")

    files = sorted(list(VAULT_PATH.glob("*.md")))
    print(f"    Processing {len(files)} files...")

    for md_f in files:
        if md_f.name == "000--DNA.md":
            continue

        try:
            content = md_f.read_text(encoding="utf-8")
            title = md_f.stem

            cat_match = re.search(r'category:\s*(.*)', content, re.IGNORECASE)
            category = cat_match.group(1).strip() if cat_match else "N/A"

            desc_sec = extract_section(content, ["Описани", "Description", "Что это"])
            sut = desc_sec.replace('\n', ' ').replace('**', '')[:200] if desc_sec else "N/A"
            if sut == "N/A":
                sut_match = re.search(r"(?:^|\n)##\s+[^\n]+\n(.*?)(?=\n##\s+|\Z)", content, re.DOTALL)
                if sut_match:
                    sut = sut_match.group(1).replace('\n', ' ').replace('**', '')[:200].strip()

            feat_sec = extract_section(content, ["Ключев", "Фичи", "Особенност", "Умеет", "Killer",
                                                  "Capabilities", "Тем[ыа]"])
            superpower = extract_bullets(feat_sec)
            code_usage = extract_code(content)

            arch_sec = extract_section(content, ["Архитектур", "Ценность", "NEXUS"])
            architecture_val = extract_bullets(arch_sec, max_items=5)

            links = re.findall(r'\[\[(.*?)\]\]', content)
            svyazi = ", ".join(f"[[{l}]]" for l in set(links)) if links else "N/A"

            entry  = f"## [{title.upper()}]\n"
            entry += f"- **категория**: {category}\n"
            entry += f"- **суть**: {sut}\n"
            entry += f"- **суперсила**: {superpower}\n"
            entry += f"- **код / запуск**: `{code_usage}`\n"
            entry += f"- **архитектура**: {architecture_val}\n"
            entry += f"- **связи**: {svyazi}\n"
            manifest_entries.append(entry)

        except Exception as e:
            print(f"  [ERR] {md_f.stem}: {e}")

    OUTPUT_FILE.write_text(
        "# NEXUS PLATFORM: MASTER DNA ARCHIVE\n\n---\n\n" +
        "\n---\n\n".join(manifest_entries) +
        "\n---\n",
        encoding="utf-8"
    )
    print(f"[SUCCESS] SMART MANIFEST COMPILED: {OUTPUT_FILE}")
    print(f"[*] Total entries: {len(manifest_entries)}")


if __name__ == "__main__":
    generate_manifest()
