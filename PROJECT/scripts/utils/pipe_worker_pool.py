import os
import sys
import time
import json
import multiprocessing as mp
from multiprocessing import Queue

# --- CONFIGURATION ---
NUM_WORKERS = mp.cpu_count() or 4
METRICS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../outputs/metrics.json"))

def worker_process(worker_id, task_queue, result_counter):
    """
    Simulates high-performance command execution from the Named Pipe.
    """
    print(f"[Worker-{worker_id}] Started.")
    while True:
        try:
            task = task_queue.get(timeout=1)
            if task == "SHUTDOWN":
                break
            
            # Simulate processing (Logic AI/Command mapping)
            # In a real IDE Optimus, this would trigger a task via RPC or OS Command
            result_counter.value += 1
            
        except:
            continue

def dashboard_updater(result_counter):
    """
    Periodically writes metrics to metrics.json for the Landing Page.
    """
    while True:
        try:
            metrics = {
                "timestamp": time.time(),
                "processed_total": result_counter.value,
                "active_workers": NUM_WORKERS,
                "status": "OPERATIONAL"
            }
            with open(METRICS_FILE, "w") as f:
                json.dump(metrics, f)
            time.sleep(1)
        except Exception as e:
            print(f"Metrics error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    mp.freeze_support()
    task_queue = Queue()
    result_counter = mp.Value('i', 0)
    
    workers = []
    for i in range(NUM_WORKERS):
        p = mp.Process(target=worker_process, args=(i, task_queue, result_counter))
        p.start()
        workers.append(p)
        
    # Start metrics monitor
    monitor = mp.Process(target=dashboard_updater, args=(result_counter,))
    monitor.daemon = True
    monitor.start()

    print(f"=== IDE OPTIMUS WORKER POOL V1.0 ===")
    print(f"[*] Scaling to {NUM_WORKERS} workers...")
    print(f"[*] Listening on Task Queue (multiprocessing channel)")
    print(f"[*] Metrics: {METRICS_FILE}")

    try:
        # This script stays alive to manage the pool. 
        # Integration with pipe_server.py will feed this queue.
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[!] Shutting down pool...")
        for _ in range(NUM_WORKERS):
            task_queue.put("SHUTDOWN")
        for p in workers:
            p.join()
