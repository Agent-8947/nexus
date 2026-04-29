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

def scan_for_duplicates(root_dir):
    hashes = defaultdict(list)
    total_files = 0
    
    print(f"Scanning directory: {root_dir}")
    for root, dirs, files in os.walk(root_dir):
        # Skip common junk folders
        if any(skip in root for skip in ['.git', 'node_modules', 'venv', '__pycache__']):
            continue
            
        for filename in files:
            filepath = os.path.join(root, filename)
            if os.path.islink(filepath):
                continue
                
            file_hash = get_file_hash(filepath)
            if file_hash:
                hashes[file_hash].append(filepath)
                total_files += 1
                if total_files % 1000 == 0:
                    print(f"Processed {total_files} files...")

    duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    return duplicates

if __name__ == "__main__":
    target = r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT"
    output_file = r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\duplicate_report.json"
    
    results = scan_for_duplicates(target)
    
    # Calculate stats
    total_dupes = sum(len(paths) - 1 for paths in results.values())
    
    report = {
        "total_duplicate_instances": total_dupes,
        "unique_duplicate_contents": len(results),
        "duplicates": results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4)
        
    print(f"Audit complete. Found {total_dupes} duplicate files.")
    print(f"Report saved to: {output_file}")
