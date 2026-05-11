"""
NEXUS-FINANCE :: Database Layer
===============================
SQLite-based local storage. Zero external dependencies.
Stores: portfolio snapshots, trade log, market data cache.
"""

import sys
import sqlite3
from pathlib import Path

# Always add project root to sys.path so imports work regardless of how this
# file is invoked (directly, as -m module, or via orchestrator).
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from config.settings import DB_PATH


def get_connection() -> sqlite3.Connection:
    """Return a connection with WAL mode and foreign keys enabled."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create all tables if they don't exist. Idempotent."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        -- Portfolio state
        CREATE TABLE IF NOT EXISTS portfolio (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT    NOT NULL DEFAULT (datetime('now')),
            symbol      TEXT    NOT NULL,
            side        TEXT    NOT NULL CHECK(side IN ('LONG', 'SHORT', 'FLAT')),
            quantity     REAL   NOT NULL DEFAULT 0,
            entry_price  REAL   NOT NULL DEFAULT 0,
            current_price REAL  NOT NULL DEFAULT 0,
            pnl_usd      REAL  NOT NULL DEFAULT 0,
            stop_loss     REAL  NOT NULL DEFAULT 0
        );

        -- Trade log (append-only ledger)
        CREATE TABLE IF NOT EXISTS trades (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT    NOT NULL DEFAULT (datetime('now')),
            symbol      TEXT    NOT NULL,
            action      TEXT    NOT NULL CHECK(action IN ('BUY', 'SELL', 'STOP_LOSS', 'TAKE_PROFIT')),
            quantity     REAL   NOT NULL,
            price        REAL   NOT NULL,
            fee_usd      REAL   NOT NULL DEFAULT 0,
            pnl_usd      REAL   NOT NULL DEFAULT 0,
            mode         TEXT   NOT NULL DEFAULT 'PAPER',
            strategy     TEXT   NOT NULL DEFAULT 'manual',
            note         TEXT   DEFAULT ''
        );

        -- Cached OHLCV data
        CREATE TABLE IF NOT EXISTS ohlcv_cache (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol      TEXT    NOT NULL,
            interval    TEXT    NOT NULL,
            timestamp   TEXT    NOT NULL,
            open        REAL   NOT NULL,
            high        REAL   NOT NULL,
            low         REAL   NOT NULL,
            close       REAL   NOT NULL,
            volume      REAL   NOT NULL,
            UNIQUE(symbol, interval, timestamp)
        );

        -- Daily equity snapshots for drawdown tracking
        CREATE TABLE IF NOT EXISTS equity_curve (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT    NOT NULL DEFAULT (datetime('now')),
            total_usd   REAL   NOT NULL,
            cash_usd    REAL   NOT NULL,
            positions_usd REAL NOT NULL
        );
    """)

    conn.commit()
    conn.close()
    print("[OK] Database initialized:", DB_PATH)


if __name__ == "__main__":
    init_db()
