#!/usr/bin/env python3
"""
NEXUS DNA Infra Agent: DOCKER_CONTAINER_MONITOR
Tier: A-Target (Production-Hardened)
Spec Hash: 444f434b45525f4d

Monitor running Docker containers for resource spikes and insecure port mappings.
"""

import json
import logging
import requests
import sqlite3
import hashlib
import sys
import time
from dataclasses import dataclass, field, asdict
from typing import List

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("DOCKER_CONTAINER_MONITOR")

DOCKER_API_BASE = "http://localhost:2375"
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

@dataclass
class ContainerRecord:
    container_id: str
    names: str
    image: str
    insecure_ports: int

@dataclass
class DockerMonitorReport:
    containers: List[ContainerRecord] = field(default_factory=list)
    scanned_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    errors: List[str] = field(default_factory=list)

class DockerContainerMonitorAgent:
    def __init__(self, db_path: str = "nexus_infra.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NEXUS-INFRA/1.0"})
        self._init_storage()

    def _init_storage(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""CREATE TABLE IF NOT EXISTS docker_container_monitor 
                                (id INTEGER PRIMARY KEY, container_id TEXT, names TEXT, image TEXT, insecure_ports INTEGER, data_hash TEXT UNIQUE, ts DATETIME DEFAULT CURRENT_TIMESTAMP)""")
                conn.commit()
            logger.info("Storage ready.")
        except sqlite3.Error as exc:
            logger.critical("DB init failed: %s", exc)
            raise SystemExit(1) from exc

    @staticmethod
    def _hash(payload: str) -> str:
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def execute_check(self) -> DockerMonitorReport:
        logger.info("Polling Docker containers...")
        report = DockerMonitorReport()
        url = f"{DOCKER_API_BASE}/containers/json"
        
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self.session.get(url, timeout=10)
                resp.raise_for_status()
                containers = resp.json()
                
                for c in containers:
                    exposed = c.get("Ports", [])
                    insecure = any(p.get("PublicPort") for p in exposed)
                    record = ContainerRecord(
                        container_id=c.get("Id", "")[:12],
                        names=",".join(c.get("Names", [])),
                        image=c.get("Image", ""),
                        insecure_ports=1 if insecure else 0
                    )
                    report.containers.append(record)
                    self._persist(record)
                break
            except Exception as e:
                logger.error("Docker API unavailable on attempt %d: %s", attempt, e)
                time.sleep(attempt * RETRY_BACKOFF)
                if attempt == MAX_RETRIES:
                    report.errors.append(f"Docker API unavailable: {e}")
                    
        return report

    def _persist(self, m: ContainerRecord) -> None:
        h = self._hash(f"{m.container_id}:{m.image}")
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT OR IGNORE INTO docker_container_monitor (container_id, names, image, insecure_ports, data_hash) VALUES (?,?,?,?,?)",
                             (m.container_id, m.names, m.image, m.insecure_ports, h))
        except sqlite3.Error as exc:
            logger.error("DB error: %s", exc)

if __name__ == "__main__":
    print(json.dumps(asdict(DockerContainerMonitorAgent().execute_check()), indent=2))
