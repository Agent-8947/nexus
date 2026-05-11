"""
NEXUS-FINANCE :: Risk Manager
===============================
Enforces all risk limits BEFORE any trade execution.
This module is the last line of defense.
"""

import sys
import logging
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from config.settings import (
    MAX_POSITION_SIZE_USD,
    MAX_DRAWDOWN_PCT,
    MAX_OPEN_POSITIONS,
    STOP_LOSS_PCT,
)

logger = logging.getLogger("nexus.risk")


class RiskViolation(Exception):
    """Raised when a trade would violate risk parameters."""
    pass


class RiskManager:
    """
    Stateless risk gate. Every trade request passes through here.
    If any check fails, the trade is REJECTED — no exceptions.
    """

    def __init__(self, portfolio_state: dict):
        """
        Args:
            portfolio_state: dict with keys:
                - total_equity_usd: float
                - peak_equity_usd: float
                - open_positions: int
                - cash_usd: float
        """
        self.state = portfolio_state

    def check_position_size(self, size_usd: float) -> bool:
        """Reject if position exceeds max allowed size."""
        if size_usd > MAX_POSITION_SIZE_USD:
            raise RiskViolation(
                f"Position size ${size_usd:.2f} exceeds limit "
                f"${MAX_POSITION_SIZE_USD:.2f}"
            )
        if size_usd > self.state["cash_usd"]:
            raise RiskViolation(
                f"Position size ${size_usd:.2f} exceeds available "
                f"cash ${self.state['cash_usd']:.2f}"
            )
        return True

    def check_max_positions(self) -> bool:
        """Reject if too many positions are already open."""
        if self.state["open_positions"] >= MAX_OPEN_POSITIONS:
            raise RiskViolation(
                f"Max open positions ({MAX_OPEN_POSITIONS}) reached. "
                f"Close a position before opening a new one."
            )
        return True

    def check_drawdown(self) -> bool:
        """Reject ALL trading if drawdown exceeds limit."""
        peak = self.state["peak_equity_usd"]
        current = self.state["total_equity_usd"]

        if peak <= 0:
            return True

        drawdown_pct = ((peak - current) / peak) * 100

        if drawdown_pct >= MAX_DRAWDOWN_PCT:
            raise RiskViolation(
                f"Drawdown {drawdown_pct:.2f}% exceeds limit "
                f"{MAX_DRAWDOWN_PCT}%. ALL TRADING HALTED."
            )
        return True

    def calculate_stop_loss(self, entry_price: float, side: str) -> float:
        """Calculate stop-loss price for a position."""
        multiplier = STOP_LOSS_PCT / 100
        if side == "LONG":
            return entry_price * (1 - multiplier)
        elif side == "SHORT":
            return entry_price * (1 + multiplier)
        else:
            raise ValueError(f"Unknown side: {side}")

    def validate_trade(self, size_usd: float) -> bool:
        """
        Run ALL risk checks. Returns True only if every check passes.
        Raises RiskViolation with specific reason on failure.
        """
        self.check_drawdown()
        self.check_max_positions()
        self.check_position_size(size_usd)

        logger.info(
            f"[OK] Risk check PASSED: ${size_usd:.2f}, "
            f"positions: {self.state['open_positions']}/{MAX_OPEN_POSITIONS}"
        )
        return True
