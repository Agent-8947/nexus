"""
NEXUS Pure Pipe Benchmark
Server + Client in one script (separate processes).
Measures RAW Named Pipe throughput without Dispatcher overhead.
"""
import time
import sys
import multiprocessing as mp

try:
    import win32pipe, win32file, pywintypes
except ImportError:
    print("ERROR: pywin32 not installed. Run: pip install pywin32")
    sys.exit(1)

PIPE_NAME = r'\\.\pipe\nexus-bench-pipe'
BUFFER_SIZE = 65536
MSG_COUNT = 100_000
PAYLOAD = b"NEXUS_BENCH_MSG_22B_OK"


def server_process(counter, ready_event):
    """Pure pipe reader — no dispatcher, no file writes."""
    handle = win32pipe.CreateNamedPipe(
        PIPE_NAME,
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        1, BUFFER_SIZE, BUFFER_SIZE, 0, None
    )
    ready_event.set()

    win32pipe.ConnectNamedPipe(handle, None)

    while True:
        try:
            resp, data = win32file.ReadFile(handle, BUFFER_SIZE)
            if resp == 0:
                counter.value += 1
            else:
                break
        except pywintypes.error:
            break

    win32file.CloseHandle(handle)


def client_process(ready_event):
    """Pure pipe writer — fire-and-forget."""
    ready_event.wait()
    time.sleep(0.2)

    handle = win32file.CreateFile(
        PIPE_NAME,
        win32file.GENERIC_READ | win32file.GENERIC_WRITE,
        0, None,
        win32file.OPEN_EXISTING,
        0, None
    )
    win32pipe.SetNamedPipeHandleState(handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)

    print(f"[CLIENT] Sending {MSG_COUNT:,} messages...")
    start = time.time()

    for _ in range(MSG_COUNT):
        win32file.WriteFile(handle, PAYLOAD)

    elapsed = time.time() - start
    win32file.CloseHandle(handle)

    rate = MSG_COUNT / elapsed
    latency_us = (elapsed / MSG_COUNT) * 1_000_000

    print()
    print("=" * 45)
    print(f"  NEXUS PIPE BENCHMARK RESULTS")
    print("=" * 45)
    print(f"  Messages    : {MSG_COUNT:>12,}")
    print(f"  Payload     : {len(PAYLOAD)} bytes")
    print(f"  Total Time  : {elapsed:>12.4f} s")
    print(f"  Throughput  : {rate:>12,.0f} msg/s")
    print(f"  Latency     : {latency_us:>12.2f} us/msg")
    print("=" * 45)


if __name__ == "__main__":
    mp.freeze_support()

    counter = mp.Value('i', 0)
    ready_event = mp.Event()

    srv = mp.Process(target=server_process, args=(counter, ready_event))
    srv.start()

    print("=== NEXUS PURE PIPE BENCHMARK ===")
    print(f"[*] Pipe: {PIPE_NAME}")
    print(f"[*] Payload: {len(PAYLOAD)}B x {MSG_COUNT:,} iterations")
    print()

    client_process(ready_event)

    time.sleep(1)
    print(f"  Server Recv : {counter.value:>12,} msgs")

    srv.terminate()
    srv.join(timeout=2)
