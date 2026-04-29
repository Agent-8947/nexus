#!/usr/bin/env python3
"""NEXUS Module: `OSINT-Scanner-v1.0.py` — Concurrent TCP port scanner (stdlib only)."""
import socket, json, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

TOP_PORTS = [21,22,23,25,53,80,110,143,443,445,993,995,3306,3389,5900,8080,8443,9200,27017]
SERVICES = {21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",80:"HTTP",443:"HTTPS",
             445:"SMB",3306:"MySQL",3389:"RDP",5900:"VNC",8080:"HTTP-Alt",9200:"Elasticsearch",27017:"MongoDB"}

def _check(host, port, timeout=1.0):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return {"port": port, "state": "open", "service": SERVICES.get(port, "unknown")}
    except: return None

def run(host: str, ports: list = None, timeout: float = 1.0) -> dict:
    ports = ports or TOP_PORTS
    open_ports = []
    with ThreadPoolExecutor(max_workers=50) as ex:
        for result in as_completed({ex.submit(_check, host, p, timeout): p for p in ports}):
            r = result.result()
            if r: open_ports.append(r)
    open_ports.sort(key=lambda x: x["port"])
    return {"host": host, "scanned": len(ports), "open_count": len(open_ports), "open_ports": open_ports}

if __name__ == "__main__":
    import sys
    print(json.dumps(run(sys.argv[1] if len(sys.argv) > 1 else "example.com"), indent=2))
