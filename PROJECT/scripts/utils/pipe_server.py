import os
import sys
import time
import json
import win32pipe, win32file, pywintypes
import multiprocessing as mp
import dispatcher  # NEXUS COMMAND DISPATCHER

# --- CONFIGURATION ---
PIPE_NAME = r'\\.\pipe\ide-optimus-core'
BUFFER_SIZE = 65536
NUM_WORKERS = mp.cpu_count() or 4
METRICS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../outputs/metrics.json"))

def worker_process(worker_id, task_queue, result_counter):
    """
    Consumes commands from the pipe queue and calls the dispatcher.
    """
    while True:
        try:
            task = task_queue.get(block=True)
            if task == "SHUTDOWN": break
            
            # Execute REAL logic through Dispatcher
            dispatcher.process_cmd(task)
            
            result_counter.value += 1
        except Exception as e:
            # print(f"[Worker-{worker_id}] Processing error: {e}")
            continue

def metrics_updater(result_counter):
    """
    Writes metrics to metrics.json for the Dashboard/Landing Page.
    """
    while True:
        try:
            metrics = {
                "timestamp": time.time(),
                "throughput_counter": result_counter.value,
                "active_workers": NUM_WORKERS,
                "protocol": "Named-Pipe-Windows",
                "status": "OPERATIONAL"
            }
            # Ensure output directory exists before writing
            os.makedirs(os.path.dirname(METRICS_FILE), exist_ok=True)
            with open(METRICS_FILE, "w") as f:
                json.dump(metrics, f)
            time.sleep(1)
        except: time.sleep(1)

def start_server():
    # --- Initialize Multiprocessing ---
    task_queue = mp.Queue(maxsize=1000000)
    result_counter = mp.Value('i', 0)
    
    workers = []
    for i in range(NUM_WORKERS):
        p = mp.Process(target=worker_process, args=(i, task_queue, result_counter))
        p.start()
        workers.append(p)
        
    monitor = mp.Process(target=metrics_updater, args=(result_counter,))
    monitor.daemon = True
    monitor.start()

    print(f"=== IDE OPTIMUS HIGH-PERFORMANCE SERVER (INTEGRATED) ===")
    print(f"[*] Pipe: {PIPE_NAME}")
    print(f"[*] Scaling: {NUM_WORKERS} Parallel Workers Active")

    while True:
        handle = None
        try:
            handle = win32pipe.CreateNamedPipe(
                PIPE_NAME,
                win32pipe.PIPE_ACCESS_DUPLEX,
                win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                1, BUFFER_SIZE, BUFFER_SIZE, 0, None
            )
            
            print("[+] Waiting for client...")
            win32pipe.ConnectNamedPipe(handle, None)
            
            while True:
                resp, data = win32file.ReadFile(handle, BUFFER_SIZE)
                if resp == 0:
                    task_queue.put(data)
                else: break
        except pywintypes.error as e:
            if e.args[0] == 109: # Broken Pipe
                pass # Silent reconnect
        except KeyboardInterrupt:
            break
        finally:
            if handle:
                win32file.CloseHandle(handle)

    print("[!] Shutting down workers...")
    for _ in range(NUM_WORKERS):
        task_queue.put("SHUTDOWN")
    for p in workers:
        p.join()

if __name__ == "__main__":
    mp.freeze_support()
    try:
        start_server()
    except KeyboardInterrupt:
        print("[!] Server shutdown.")
        sys.exit(0)
