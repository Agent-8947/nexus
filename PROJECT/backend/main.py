"""
NEXUS CORE API v2.0
Unified FastAPI backend integrating Dispatcher, SQLite, and System Metrics.
Replaces: old main.py stub + Flask api_bridge.py

Usage:
  python main.py                  # Start on port 8000 (dev)
  uvicorn main:app --reload       # Start with hot-reload

API Docs: http://localhost:8000/docs
"""

import os
import sys
import json
import time
import sqlite3
import logging
from pathlib import Path
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# PATH RESOLUTION (path-agnostic: works from any CWD)
# ---------------------------------------------------------------------------
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
UTILS_DIR = SCRIPTS_DIR / "utils"
DB_PATH = PROJECT_ROOT / "nexus_optimus.db"
METRICS_FILE = PROJECT_ROOT / "outputs" / "metrics.json"
MEMORY_FILE = PROJECT_ROOT / "memory.json"
FAULT_REGISTRY = PROJECT_ROOT / "fault_registry.json"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

# Ensure dispatcher is importable
sys.path.insert(0, str(UTILS_DIR))

# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("nexus.api")

# ---------------------------------------------------------------------------
# DATABASE LAYER (SQLite — zero-config, zero-latency)
# ---------------------------------------------------------------------------
class NexusDB:
    """Thin wrapper around SQLite for the NEXUS Core API."""

    def __init__(self, db_path: Path):
        self.db_path = str(db_path)
        self._ensure_schema()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")  # Better concurrent reads
        return conn

    def _ensure_schema(self):
        conn = self._get_conn()
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                archetype TEXT,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                file_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_type TEXT,
                file_size INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS nexus_state (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS command_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT NOT NULL,
                executor TEXT DEFAULT 'api',
                result TEXT,
                execution_time_ms REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        c.execute("INSERT OR IGNORE INTO nexus_state (key, value) VALUES ('archetype', 'AI-Orchestrated-NEXUS-v2')")
        c.execute("INSERT OR IGNORE INTO nexus_state (key, value) VALUES ('version', '2026.1')")
        conn.commit()
        conn.close()
        logger.info(f"Database ready: {self.db_path}")

    def log_command(self, command: str, result: dict, exec_time_ms: float):
        """Persist every command execution into command_history."""
        conn = self._get_conn()
        conn.execute(
            "INSERT INTO command_history (command, executor, result, execution_time_ms) VALUES (?, ?, ?, ?)",
            (command, "api", json.dumps(result, ensure_ascii=False), exec_time_ms),
        )
        conn.commit()
        conn.close()

    def get_history(self, limit: int = 20) -> list[dict]:
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT id, command, executor, result, execution_time_ms, timestamp FROM command_history ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_state(self) -> dict:
        conn = self._get_conn()
        rows = conn.execute("SELECT key, value FROM nexus_state").fetchall()
        conn.close()
        return {r["key"]: r["value"] for r in rows}

    def set_state(self, key: str, value: str):
        conn = self._get_conn()
        conn.execute(
            "INSERT OR REPLACE INTO nexus_state (key, value, updated_at) VALUES (?, ?, ?)",
            (key, value, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
        conn.close()

    def check_health(self) -> dict:
        try:
            conn = self._get_conn()
            row = conn.execute("SELECT COUNT(*) as cnt FROM command_history").fetchone()
            tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            conn.close()
            return {
                "status": "connected",
                "path": self.db_path,
                "tables": [t["name"] for t in tables],
                "total_commands": row["cnt"],
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}


# ---------------------------------------------------------------------------
# DISPATCHER INTEGRATION
# ---------------------------------------------------------------------------
def _get_dispatcher():
    """Import dispatcher dynamically so it resolves paths correctly."""
    try:
        import dispatcher
        return dispatcher
    except ImportError:
        logger.warning("Dispatcher not found in sys.path. Command execution disabled.")
        return None


# ---------------------------------------------------------------------------
# PYDANTIC MODELS
# ---------------------------------------------------------------------------
class CommandRequest(BaseModel):
    cmd: str = Field(..., description="Command name (e.g. SCAN_TODO, SYS_INFO, SYS_CLEAN, DOC_GEN)")
    arg: Optional[str] = Field(None, description="Optional argument for the command")

class StateUpdate(BaseModel):
    key: str
    value: str

class ErrorReport(BaseModel):
    fault_type: str
    description: str
    root_cause: str
    solution: str
    prevention_rule: str


# ---------------------------------------------------------------------------
# LIFESPAN (startup / shutdown)
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    logger.info("═══ NEXUS CORE API v2.0 ═══")
    logger.info(f"Project Root : {PROJECT_ROOT}")
    logger.info(f"Database     : {DB_PATH}")
    logger.info(f"Dispatcher   : {'✅ Loaded' if _get_dispatcher() else '❌ Missing'}")
    app.state.db = NexusDB(DB_PATH)
    app.state.db.set_state("api_status", "online")
    app.state.start_time = time.time()
    yield
    # --- Shutdown ---
    app.state.db.set_state("api_status", "offline")
    logger.info("NEXUS Core API stopped.")


# ---------------------------------------------------------------------------
# APP INIT
# ---------------------------------------------------------------------------
app = FastAPI(
    title="NEXUS Core API",
    description="Unified Backend Engine for NEXUS IDE — Dispatcher + SQLite + Metrics",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для Dashboard/Frontend access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# ENDPOINTS: Health & Status
# ---------------------------------------------------------------------------
@app.get("/", tags=["status"])
async def root():
    uptime = time.time() - app.state.start_time
    return {
        "engine": "NEXUS Core API v2.0",
        "status": "operational",
        "uptime_seconds": round(uptime, 1),
        "docs": "/docs",
    }


@app.get("/health", tags=["status"])
async def health_check():
    db_health = app.state.db.check_health()
    metrics = _read_metrics()
    return {
        "api": "healthy",
        "database": db_health,
        "pipe_server": metrics.get("status", "unknown"),
        "active_workers": metrics.get("active_workers", 0),
        "dispatcher": "loaded" if _get_dispatcher() else "unavailable",
    }


@app.get("/api/v1/metrics", tags=["status"])
async def get_metrics():
    """Live metrics from Pipe Server (if running)."""
    metrics = _read_metrics()
    if not metrics:
        return {"status": "pipe_server_offline", "hint": "Start pipe_server.py to see live metrics"}
    return metrics


def _read_metrics() -> dict:
    try:
        if METRICS_FILE.exists():
            with open(METRICS_FILE, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


# ---------------------------------------------------------------------------
# ENDPOINTS: Command Execution (Dispatcher Integration)
# ---------------------------------------------------------------------------
@app.post("/api/v1/command", tags=["commands"])
async def execute_command(req: CommandRequest):
    """
    Execute a NEXUS command through the Dispatcher.
    Available commands: SCAN_TODO, SYS_INFO, SYS_CLEAN, DOC_GEN, RUN_AUDIT, RUN_GEO,
    SELF_HEAL, GEN_MARKETING, PLAN_TASK, MCP.
    """
    dispatcher = _get_dispatcher()
    if not dispatcher:
        raise HTTPException(status_code=503, detail="Dispatcher module not available")

    start = time.time()

    # Build raw data the way dispatcher expects it
    raw = json.dumps({"cmd": req.cmd, "arg": req.arg}) if req.arg else req.cmd

    result = dispatcher.process_cmd(raw)
    exec_time = round((time.time() - start) * 1000, 2)

    # Log to SQLite
    app.state.db.log_command(req.cmd, result, exec_time)

    return {
        "command": req.cmd,
        "execution_time_ms": exec_time,
        **result,
    }


@app.get("/api/v1/commands/available", tags=["commands"])
async def list_available_commands():
    """List all commands the Dispatcher can handle."""
    dispatcher = _get_dispatcher()
    built_in = ["SCAN_TODO", "SYS_INFO", "SYS_CLEAN"]
    agent_cmds = list(dispatcher.AGENT_MAP.keys()) if dispatcher else []
    return {
        "built_in": built_in,
        "agent_delegated": agent_cmds,
        "total": len(built_in) + len(agent_cmds),
    }


@app.get("/api/v1/commands/history", tags=["commands"])
async def command_history(limit: int = Query(20, ge=1, le=100)):
    """Retrieve recent command execution history from SQLite."""
    return app.state.db.get_history(limit)


# ---------------------------------------------------------------------------
# ENDPOINTS: State & Memory
# ---------------------------------------------------------------------------
@app.get("/api/v1/state", tags=["state"])
async def get_state():
    """Read all key-value pairs from nexus_state table."""
    return app.state.db.get_state()


@app.put("/api/v1/state", tags=["state"])
async def update_state(update: StateUpdate):
    """Set or update a key-value pair in nexus_state."""
    app.state.db.set_state(update.key, update.value)
    return {"status": "updated", "key": update.key}


@app.get("/api/v1/memory", tags=["state"])
async def get_memory():
    """Read the full memory.json (project state, stack, history)."""
    try:
        if MEMORY_FILE.exists():
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"error": "memory.json not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# ENDPOINTS: Fault Registry
# ---------------------------------------------------------------------------
@app.get("/api/v1/faults", tags=["faults"])
async def get_faults():
    """Read all recorded faults."""
    try:
        if FAULT_REGISTRY.exists():
            with open(FAULT_REGISTRY, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/faults", tags=["faults"])
async def record_fault(report: ErrorReport):
    """Record a new fault into the registry."""
    registry = []
    if FAULT_REGISTRY.exists():
        with open(FAULT_REGISTRY, "r", encoding="utf-8") as f:
            registry = json.load(f)

    new_entry = {
        "id": f"ERR-{len(registry):03d}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "fault_type": report.fault_type,
        "description": report.description,
        "root_cause": report.root_cause,
        "solution": report.solution,
        "prevention_rule": report.prevention_rule,
    }
    registry.append(new_entry)

    with open(FAULT_REGISTRY, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

    return {"status": "recorded", "fault_id": new_entry["id"]}


# ---------------------------------------------------------------------------
# ENDPOINTS: Assets (Output Files)
# ---------------------------------------------------------------------------
@app.get("/api/v1/assets", tags=["assets"])
async def list_assets(file_type: Optional[str] = Query(None, description="Filter: pdf, html, md")):
    """List all generated output files."""
    if not OUTPUT_DIR.exists():
        return []

    assets = []
    for f in sorted(OUTPUT_DIR.iterdir()):
        if f.is_file():
            if file_type and not f.suffix.lstrip(".") == file_type:
                continue
            assets.append({
                "name": f.name,
                "type": f.suffix.lstrip("."),
                "size_kb": round(f.stat().st_size / 1024, 1),
                "modified": datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc).isoformat(),
            })
    return assets


# ---------------------------------------------------------------------------
# RUN
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
