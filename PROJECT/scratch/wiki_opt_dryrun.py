import os
import hashlib
from collections import defaultdict
import json

def get_file_hash(filepath):
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        return None

def scan_wiki_for_duplicates(targets):
    hashes = defaultdict(list)
    total_files = 0
    total_size = 0
    
    for target in targets:
        print(f"Scanning directory: {target}")
        for root, dirs, files in os.walk(target):
            # Skip junk
            if any(skip in root for skip in ['.git', 'node_modules', 'venv', '__pycache__']):
                continue
                
            for filename in files:
                filepath = os.path.join(root, filename)
                if os.path.islink(filepath):
                    continue
                    
                file_size = os.path.getsize(filepath)
                if file_size == 0:
                    continue
                    
                file_hash = get_file_hash(filepath)
                if file_hash:
                    hashes[(file_size, file_hash)].append(filepath)
                    total_files += 1
                    total_size += file_size
                    if total_files % 5000 == 0:
                        print(f"Processed {total_files} files...")

    duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    return duplicates, total_files, total_size

if __name__ == "__main__":
    targets = [
        r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI",
        r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI-FARM"
    ]
    
    dupes, total_count, total_bytes = scan_wiki_for_duplicates(targets)
    
    # Analyze dupes
    saved_bytes = 0
    dupe_file_count = 0
    
    # Sort by size to see biggest wins first
    sorted_dupes = sorted(dupes.items(), key=lambda x: x[0][0], reverse=True)
    
    summary = []
    for (size, h), paths in sorted_dupes:
        saved_bytes += size * (len(paths) - 1)
        dupe_file_count += (len(paths) - 1)
        summary.append({
            "size": size,
            "count": len(paths),
            "example_path": paths[0],
            "sample_content": "" # Could preview here
        })

    print(f"\n--- WIKI OPTIMIZATION DRY RUN ---")
    print(f"Total files scanned: {total_count}")
    print(f"Total size: {total_bytes / (1024*1024):.2f} MB")
    print(f"Duplicate files found: {dupe_file_count}")
    print(f"Potential space savings: {saved_bytes / (1024*1024):.2f} MB")
    
    # Output top 50 duplicates to a file
    with open("wiki_dupe_summary.json", 'w', encoding='utf-8') as f:
        json.dump(summary[:50], f, indent=4)
