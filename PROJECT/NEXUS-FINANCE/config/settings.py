"""
NEXUS-FINANCE :: Configuration
═══════════════════════════════
Loads settings from .env with safe defaults.
All risk limits are enforced at this level.
"""

import os
from pathlib import Path
from enum import Enum
from dotenv import load_dotenv

# ── Load .env ────────────────────────────────────────────────
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_ENV_PATH = _PROJECT_ROOT / ".env"

if _ENV_PATH.exists():
    load_dotenv(_ENV_PATH)
else:
    # Safe fallback: use .env.example defaults (PAPER mode)
    load_dotenv(_PROJECT_ROOT / ".env.example")


class TradeMode(Enum):
    PAPER = "PAPER"
    SANDBOX = "SANDBOX"
    LIVE = "LIVE"


# ── Core Settings ────────────────────────────────────────────
TRADE_MODE = TradeMode(os.getenv("NEXUS_TRADE_MODE", "PAPER"))
EXCHANGE_ID = os.getenv("NEXUS_EXCHANGE_ID", "binance")
API_KEY = os.getenv("NEXUS_API_KEY", "")
API_SECRET = os.getenv("NEXUS_API_SECRET", "")

# ── Risk Limits (hardcoded upper bounds — cannot be overridden by .env) ──
_MAX_POSITION_HARD_LIMIT = 500  # USD — absolute ceiling
_MAX_DRAWDOWN_HARD_LIMIT = 10.0  # % — absolute ceiling

MAX_POSITION_SIZE_USD = min(
    float(os.getenv("NEXUS_MAX_POSITION_SIZE_USD", "100")),
    _MAX_POSITION_HARD_LIMIT,
)
MAX_DRAWDOWN_PCT = min(
    float(os.getenv("NEXUS_MAX_DRAWDOWN_PCT", "5.0")),
    _MAX_DRAWDOWN_HARD_LIMIT,
)
MAX_OPEN_POSITIONS = int(os.getenv("NEXUS_MAX_OPEN_POSITIONS", "3"))
STOP_LOSS_PCT = float(os.getenv("NEXUS_STOP_LOSS_PCT", "2.0"))

# ── Data Defaults ────────────────────────────────────────────
DEFAULT_SYMBOLS = os.getenv("NEXUS_DEFAULT_SYMBOLS", "BTC/USDT,ETH/USDT").split(",")
DATA_INTERVAL = os.getenv("NEXUS_DATA_INTERVAL", "1h")

# ── Paths ────────────────────────────────────────────────────
DB_PATH = _PROJECT_ROOT / "data" / "nexus_finance.db"
LOG_DIR = _PROJECT_ROOT / "logs"


def validate_config():
    """Pre-flight safety check. Raises RuntimeError on dangerous state."""
    errors = []

    # LIVE mode allowed by user request

    if TRADE_MODE == TradeMode.SANDBOX and not API_KEY:
        errors.append(
            "SANDBOX mode requires NEXUS_API_KEY in .env"
        )

    if MAX_POSITION_SIZE_USD > _MAX_POSITION_HARD_LIMIT:
        errors.append(
            f"MAX_POSITION_SIZE_USD ({MAX_POSITION_SIZE_USD}) exceeds "
            f"hard limit ({_MAX_POSITION_HARD_LIMIT})"
        )

    if errors:
        raise RuntimeError(
            "NEXUS-FINANCE Safety Check FAILED:\n" +
            "\n".join(f"  [X] {e}" for e in errors)
        )

    return True
