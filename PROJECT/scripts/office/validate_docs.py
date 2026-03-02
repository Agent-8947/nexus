import sys
from pathlib import Path

def validate():
    if len(sys.argv) < 2:
        print("❌ Usage: python validate_docs.py <path>")
        return

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"❌ File not found: {path}")
        sys.exit(1)

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    errors = []
    if "TODO" in content:
        errors.append("Found TODO markers")
    if "N/A" in content:
        errors.append("Found N/A placeholders (Incomplete Context)")

    if errors:
        print(f"⚠️ Validation warnings for {path.name}:")
        for err in errors:
            print(f"  - {err}")
    else:
        print(f"✅ Document {path.name} is valid and clean.")

if __name__ == "__main__":
    validate()
