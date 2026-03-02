import psutil
import os
import ctypes
import json

def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

def kill_bloat():
    print("NEXUS Cleaner [v2.0] - Cleaning background noise...")
    print("-" * 50)
    
    # Load targets from references
    ref_path = os.path.join(os.path.dirname(__file__), "..", "references", "targets.json")
    try:
        with open(ref_path, "r") as f:
            config = json.load(f)
            targets = config.get("bloat_processes", [])
    except Exception as e:
        print(f"Error loading targets: {e}")
        return

    if not is_admin():
        print("Note: Running without ADMIN rights. Some system processes might be skipped.")
    
    freed_count = 0
    current_pid = os.getpid()

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            name = proc.info['name']
            if name and name.lower() in [t.lower() for t in targets]:
                if proc.info['pid'] != current_pid:
                    proc.kill()
                    print(f"[X] Terminated: {name} (PID: {proc.info['pid']})")
                    freed_count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
            
    print("-" * 50)
    if freed_count > 0:
        print(f"SUCCESS: Recovered resources from {freed_count} processes.")
    else:
        print("System is already lean. No bloat detected.")

if __name__ == "__main__":
    kill_bloat()
