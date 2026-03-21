import os
import psutil
import ctypes
import shutil
import time
import json
from datetime import datetime

def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

def load_config():
    ref_path = os.path.join(os.path.dirname(__file__), "..", "references", "targets.json")
    try:
        with open(ref_path, "r") as f:
            return json.load(f)
    except:
        return {}

def optimize_memory():
    print("[1/3] RAM: Compressing Working Sets...")
    count = 0
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['pid'] < 100: continue
            handle = ctypes.windll.kernel32.OpenProcess(0x0500, False, proc.info['pid'])
            if handle:
                ctypes.windll.psapi.EmptyWorkingSet(handle)
                ctypes.windll.kernel32.CloseHandle(handle)
                count += 1
        except: continue
    print(f"   Success: Trimmed {count} processes.")

def cleanup_cpu(targets):
    print("[2/3] CPU: Hunting ghost agents & target processes...")
    agents = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            name = proc.info['name']
            if name and "Antigravity" in name:
                agents.append(proc)
            if name and name.lower() in [t.lower() for t in targets]:
                proc.kill()
                print(f"   Terminated background target: {name}")
        except: continue
    
    if len(agents) > 3:
        agents.sort(key=lambda x: x.cpu_percent() if x.is_running() else 0, reverse=True)
        killed = 0
        for p in agents[3:]:
            try:
                p.kill()
                killed += 1
            except: pass
        print(f"   Success: Terminated {killed} ghost agents.")

def cleanup_disk(paths):
    print("[3/3] DISK: Evicting junk files...")
    total_removed = 0
    for path in paths:
        if path == "LOCAL_TEMP":
            path = os.environ.get('TEMP')
        if not path or not os.path.exists(path): continue
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                    total_removed += 1
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    total_removed += 1
            except: continue
    print(f"   Success: Removed {total_removed} items.")

def run_boost():
    config = load_config()
    targets = config.get("turbo_targets", [])
    paths = config.get("cleanup_paths", [])

    start_time = time.time()
    print(f"\n--- NEXUS TURBO BOOST | {datetime.now().strftime('%H:%M:%S')} ---")
    print("=" * 45)
    
    optimize_memory()
    cleanup_cpu(targets)
    cleanup_disk(paths)
    
    duration = time.time() - start_time
    print("=" * 45)
    print(f"SYSTEM STATUS: OPTIMIZED | TIME: {duration:.2f}s")

if __name__ == "__main__":
    run_boost()
