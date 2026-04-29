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

def optimize_wiki(targets):
    hashes = defaultdict(list)
    total_files = 0
    
    print("Step 1: Scanning for duplicates...")
    for target in targets:
        for root, dirs, files in os.walk(target):
            if any(skip in root for skip in ['.git', 'node_modules', 'venv', '__pycache__']):
                continue
            for filename in files:
                filepath = os.path.join(root, filename)
                if os.path.islink(filepath): continue
                
                size = os.path.getsize(filepath)
                if size < 100: continue # Skip tiny files
                
                h = get_file_hash(filepath)
                if h:
                    hashes[(size, h)].append(filepath)
                    total_files += 1
                    if total_files % 5000 == 0:
                        print(f"Processed {total_files} files...")

    print("\nStep 2: Performing Hard-Link Optimization...")
    optimized_count = 0
    saved_bytes = 0
    error_count = 0
    
    for (size, h), paths in hashes.items():
        if len(paths) <= 1:
            continue
            
        master = paths[0]
        for dupe in paths[1:]:
            try:
                # On Windows, os.link requires the destination to NOT exist
                # So we must delete the duplicate first
                if os.path.abspath(master).lower() == os.path.abspath(dupe).lower():
                    continue # Should not happen with current logic, but safety first
                
                # Check if they are already hardlinked (same inode equivalent)
                # In Python on Windows, st_ino might be 0, but we can check if they point to same file
                # Better: just replace it.
                
                temp_dupe = dupe + ".tmp"
                os.rename(dupe, temp_dupe)
                try:
                    os.link(master, dupe)
                    os.remove(temp_dupe)
                    optimized_count += 1
                    saved_bytes += size
                except Exception as link_err:
                    os.rename(temp_dupe, dupe) # Rollback
                    print(f"Error linking {dupe}: {link_err}")
                    error_count += 1
                    
            except Exception as e:
                print(f"Critical error processing {dupe}: {e}")
                error_count += 1

    print(f"\n--- OPTIMIZATION COMPLETE ---")
    print(f"Files replaced with hard links: {optimized_count}")
    print(f"Space reclaimed: {saved_bytes / (1024*1024):.2f} MB")
    print(f"Errors encountered: {error_count}")

if __name__ == "__main__":
    targets = [
        r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI",
        r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI-FARM"
    ]
    optimize_wiki(targets)
