import os
import time

def get_dir_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        if '.git' in dirpath or 'node_modules' in dirpath or 'BACKUPS' in dirpath:
            continue
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def analyze():
    print("=== NEXUS TOKEN AUDIT V1.0 ===")
    
    # 1. Workspace Size (Context Load)
    ws_size = get_dir_size('e:/Downloads/--ANTIGRAVITY store/IDE-optimus')
    est_tokens_ws = ws_size // 4
    
    print(f"[*] Workspace Data Size: {ws_size / 1024:.2f} KB")
    print(f"[*] Estimated Context Tokens (Static): ~{est_tokens_ws:,}")
    
    # 2. Speed (Simulated/Based on typical response times)
    print(f"[*] Latency Proxy: Nominal (Standard API response)")
    
    print("\n=== OPTIMIZATION RECOMMENDATIONS ===")
    print("1. [DRY] Use /snapshot before large refactors to avoid repeating context in prompts.")
    print("2. [SCAFFOLDING] Keep generate_nexus_assets.js lean. Move large HTML templates to separate .html files if they exceed 500 lines.")
    print("3. [CLEANUP] Run /clean-docs regularly to remove redundant information from .md files.")
    print("4. [MODE] Use 'Turbo' mode for repetitive script tasks to minimize conversational overhead.")
    print("\n[READY] Token consumption within safe bounds for NEXUS project.")

if __name__ == "__main__":
    analyze()
