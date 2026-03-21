import time
import win32file
import win32pipe
import pywintypes

PIPE_NAME = r'\\.\pipe\ide-optimus-core'

def run_bench(iterations=100000):
    print(f"[*] BENCHMARK STARTING: {iterations} messages")
    
    try:
        handle = win32file.CreateFile(
            PIPE_NAME,
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            0, None,
            win32file.OPEN_EXISTING,
            0, None
        )
        
        # Переводим в Message Mode
        res = win32pipe.SetNamedPipeHandleState(handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)
        
        payload = b"NEXUS_MSG_001_DATA_VAL"
        
        start_time = time.time()
        for i in range(iterations):
            win32file.WriteFile(handle, payload)
            
        elapsed = time.time() - start_time
        rate = iterations / elapsed
        latency = (elapsed / iterations) * 1000 # ms
        
        print("-" * 30)
        print(f"RESULTS for {iterations} msg:")
        print(f"  TOTAL TIME: {elapsed:.4f} s")
        print(f"  THROUGHPUT: {rate:.2f} msg/s")
        print(f"  LATENCY:    {latency:.6f} ms")
        print("-" * 30)
        
        win32file.CloseHandle(handle)
        
    except pywintypes.error as e:
        print(f"[-] Bench Error: {e}")

if __name__ == "__main__":
    # Ждем запуска сервера
    time.sleep(1)
    run_bench()
