import psutil
import time
import os
from datetime import datetime

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def monitor():
    print("NEXUS Resource Monitor [v1.0] - Press Ctrl+C to exit")
    print("-" * 50)
    
    try:
        while True:
            # CPU Info
            cpu_usage = psutil.cpu_percent(interval=1)
            
            # RAM Info
            svmem = psutil.virtual_memory()
            
            # Disk Info
            partitions = psutil.disk_partitions()
            disk_usage = psutil.disk_usage('/')
            
            clear_screen()
            print(f"NEXUS Resource Monitor | {datetime.now().strftime('%H:%M:%S')}")
            print("-" * 50)
            
            # CPU
            print(f"CPU Usage:    [{'#' * int(cpu_usage / 5)}{' ' * (20 - int(cpu_usage / 5))}] {cpu_usage}%")
            
            # RAM
            ram_bar = int(svmem.percent / 5)
            print(f"RAM Usage:    [{'#' * ram_bar}{' ' * (20 - ram_bar)}] {svmem.percent}% ({get_size(svmem.used)} / {get_size(svmem.total)})")
            print(f"RAM Free:     {get_size(svmem.available)}")
            
            # Disk
            disk_bar = int(disk_usage.percent / 5)
            print(f"Disk Usage:   [{'#' * disk_bar}{' ' * (20 - disk_bar)}] {disk_usage.percent}% ({get_size(disk_usage.used)} / {get_size(disk_usage.total)})")
            
            print("-" * 50)
            print("Status: SUCCESS | Mode: Lightweight")
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    monitor()
