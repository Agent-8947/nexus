#!/usr/bin/env python3
"""
92_NEXUS_DNA_ORCHESTRATOR Synthesized Agent V3 [HARDENED PRODUCTION]
Identity: NexusDNAOrchestrator
Domain: SYNTH_TOOLS / INFRA
Lineage: NEXUS-Hive-Mind-v3

HARDENED FEATURES: 
- SQLite WAL Mode & IMMEDIATE Transactions (Concurrency Safety)
- Dynamic Class-based Execution (Agent V2 Standard)
- CPU-Optimized Parallel Processing (Multiprocessing Pool)
- Discovery Cache & Intelligence-based Routing
- Relative Path Resolution
"""

import os
import sqlite3
import json
import logging
import importlib.util
import multiprocessing
import time
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] DNA_Orchestrator_V3: %(message)s")
logger = logging.getLogger("DNA_Orchestrator_V3")

@dataclass
class AgentMetadata:
    id: str
    name: str
    domain: str
    path: str
    last_seen: str = field(default_factory=lambda: datetime.now().isoformat())

class NexusDNAOrchestratorAgent:
    def __init__(self, spine_db: str = "nexus_spine_v3.db"):
        self.dna_root = os.path.dirname(os.path.abspath(__file__))
        self.spine_db = os.path.join(self.dna_root, spine_db)
        self.agents: Dict[str, AgentMetadata] = {}
        self._init_spine()
        self.refresh_registry()
        
    def _init_spine(self):
        """Initialize High-Concurrency Spine."""
        with sqlite3.connect(self.spine_db) as conn:
            conn.execute("PRAGMA journal_mode=WAL") # Enable Write-Ahead Logging
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS agent_registry (
                    agent_id TEXT PRIMARY KEY,
                    name TEXT,
                    domain TEXT,
                    path TEXT,
                    last_seen TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS task_queue (
                    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target_domain TEXT,
                    payload TEXT,
                    status TEXT DEFAULT 'PENDING',
                    result TEXT,
                    error TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def refresh_registry(self):
        """Standardized Agent Discovery v3."""
        logger.info("PHASE 1: Hive Discovery v3 [Standardized Inspect]")
        for root, _, files in os.walk(self.dna_root):
            for file in files:
                if file.endswith("_synthesized_agent.py") and file != os.path.basename(__file__):
                    agent_id = file.split("_")[0]
                    path = os.path.join(root, file)
                    
                    domain = "General"
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            content = f.read(2000)
                            match = re.search(r"Domain:\s*([^\n\r]+)", content)
                            if match: domain = match.group(1).strip()
                    except: pass
                    
                    metadata = AgentMetadata(id=agent_id, name=file.replace(".py", ""), domain=domain, path=path)
                    self.agents[agent_id] = metadata
                    self._persist_agent_meta(metadata)
        logger.info("Hive Synced. %d active specialists online.", len(self.agents))

    def _persist_agent_meta(self, meta: AgentMetadata):
        with sqlite3.connect(self.spine_db) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO agent_registry (agent_id, name, domain, path, last_seen)
                VALUES (?, ?, ?, ?, ?)
            """, (meta.id, meta.name, meta.domain, meta.path, meta.last_seen))

    @staticmethod
    def run_agent_executor(agent_path: str, payload_str: str) -> str:
        """Isolated V2 Class Execution Gate."""
        try:
            payload = json.loads(payload_str)
            spec = importlib.util.spec_from_file_location("nexus_agent_v2", agent_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'Agent'):
                agent_instance = module.Agent()
                result = agent_instance.execute(payload)
                return json.dumps(result)
            return json.dumps({"status": "ERROR", "error": "Agent class not found"})
        except Exception as e:
            return json.dumps({"status": "ERROR", "error": f"Executor Exception: {str(e)}"})

    def _atomic_task_claim(self) -> Optional[sqlite3.Row]:
        """Atomic Task Acquisition via IMMEDIATE transaction."""
        conn = sqlite3.connect(self.spine_db, isolation_level='IMMEDIATE')
        conn.row_factory = sqlite3.Row
        try:
            with conn: # Atomic transaction start
                task = conn.execute("SELECT * FROM task_queue WHERE status = 'PENDING' LIMIT 1").fetchone()
                if task:
                    conn.execute("UPDATE task_queue SET status = 'RUNNING' WHERE task_id = ?", (task['task_id'],))
                    return task
        except sqlite3.OperationalError:
            return None # Locked
        finally:
            conn.close()
        return None

    def execute_hive_loop(self, max_concurrent: int = 4):
        """Executive Hardened Loop with Backpressure."""
        logger.info("PHASE 2: Hive Orchestration Active [V3 Hardened Engine]")
        with multiprocessing.Pool(processes=max_concurrent) as pool:
            while True:
                task = self._atomic_task_claim()
                if task:
                    target_domain = task['target_domain']
                    candidates = [a for a in self.agents.values() if target_domain.upper() in a.domain.upper()]
                    
                    if candidates:
                        winner = candidates[0]
                        logger.info("Task %d -> %s", task['task_id'], winner.name)
                        def callback(res): self._update_task(task['task_id'], "COMPLETED", result=res)
                        def error_callback(err): self._update_task(task['task_id'], "FAILED", error=str(err))
                        
                        pool.apply_async(NexusDNAOrchestratorAgent.run_agent_executor, 
                                        (winner.path, task['payload']), 
                                        callback=callback, 
                                        error_callback=error_callback)
                    else:
                        self._update_task(task['task_id'], "SKIPPED", error="No agent for domain")
                
                if os.getenv("NEXUS_DRY_RUN"): break
                time.sleep(0.5)

    def _update_task(self, task_id: int, status: str, result: str = None, error: str = None):
        with sqlite3.connect(self.spine_db) as conn:
            conn.execute("UPDATE task_queue SET status = ?, result = ?, error = ? WHERE task_id = ?",
                         (status, result, error, task_id))

if __name__ == "__main__":
    orchestrator = NexusDNAOrchestratorAgent()
    # To start the hive: 
    # orchestrator.execute_hive_loop()
