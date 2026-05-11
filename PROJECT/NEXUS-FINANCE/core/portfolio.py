"""
NEXUS-FINANCE :: Paper Portfolio
================================
Simulated portfolio for paper trading.
All state persisted to SQLite.
"""

import sys
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from db.database import get_connection
from core.risk_manager import RiskManager, RiskViolation
from core.data_feed import get_current_price
from config.settings import TRADE_MODE, TradeMode

logger = logging.getLogger("nexus.portfolio")


@dataclass
class Position:
    symbol: str
    side: str  # LONG or SHORT
    quantity: float
    entry_price: float
    stop_loss: float
    timestamp: str = ""

    @property
    def current_price(self) -> float:
        return get_current_price(self.symbol)

    @property
    def pnl_usd(self) -> float:
        price = self.current_price
        if price == 0:
            return 0.0
        if self.side == "LONG":
            return (price - self.entry_price) * self.quantity
        else:
            return (self.entry_price - price) * self.quantity

    @property
    def value_usd(self) -> float:
        return self.quantity * self.current_price


class PaperPortfolio:
    """
    Simulated portfolio. No real money moves.
    All trades are logged to SQLite for analysis.
    """

    def __init__(self, initial_capital: float = 10000.0):
        self.cash = initial_capital
        self.initial_capital = initial_capital
        self.peak_equity = initial_capital
        self.positions: list[Position] = []

    @property
    def total_equity(self) -> float:
        positions_value = sum(p.value_usd for p in self.positions)
        return self.cash + positions_value

    @property
    def portfolio_state(self) -> dict:
        return {
            "total_equity_usd": self.total_equity,
            "peak_equity_usd": self.peak_equity,
            "open_positions": len(self.positions),
            "cash_usd": self.cash,
        }

    def open_position(
        self,
        symbol: str,
        side: str,
        size_usd: float,
        strategy: str = "manual",
    ) -> Position | None:
        """
        Open a position after passing ALL risk checks.
        Returns the Position on success, None on failure.
        """
        # ── Risk Gate ────────────────────────────────────
        risk = RiskManager(self.portfolio_state)
        try:
            risk.validate_trade(size_usd)
        except RiskViolation as e:
            logger.warning(f"[REJECT] Trade REJECTED: {e}")
            return None

        # ── Execution ────────────────────────────────────
        price = get_current_price(symbol)
        if price <= 0:
            logger.error(f"Cannot get price for {symbol}. Trade cancelled.")
            return None

        quantity = size_usd / price
        stop_loss = risk.calculate_stop_loss(price, side)

        position = Position(
            symbol=symbol,
            side=side,
            quantity=quantity,
            entry_price=price,
            stop_loss=stop_loss,
            timestamp=datetime.utcnow().isoformat(),
        )

        self.cash -= size_usd
        self.positions.append(position)

        # ── Log to DB ────────────────────────────────────
        self._log_trade(
            symbol=symbol,
            action="BUY" if side == "LONG" else "SELL",
            quantity=quantity,
            price=price,
            strategy=strategy,
            note=f"stop_loss={stop_loss:.4f}",
        )

        logger.info(
            f"[OK] Opened {side} {symbol}: "
            f"qty={quantity:.6f} @ ${price:.2f}, "
            f"SL=${stop_loss:.2f}"
        )
        return position

    def close_position(
        self,
        symbol: str,
        reason: str = "manual",
    ) -> float:
        """
        Close a position by symbol. Returns realized PnL.
        """
        pos = next((p for p in self.positions if p.symbol == symbol), None)
        if pos is None:
            logger.warning(f"No open position for {symbol}")
            return 0.0

        price = get_current_price(symbol)
        if price <= 0:
            logger.error(f"Cannot get price for {symbol}. Close cancelled.")
            return 0.0

        pnl = pos.pnl_usd
        value = pos.quantity * price
        self.cash += value
        self.positions.remove(pos)

        # Update peak equity
        if self.total_equity > self.peak_equity:
            self.peak_equity = self.total_equity

        # ── Log to DB ────────────────────────────────────
        action = "STOP_LOSS" if reason == "stop_loss" else "SELL"
        self._log_trade(
            symbol=symbol,
            action=action,
            quantity=pos.quantity,
            price=price,
            pnl_usd=pnl,
            strategy=reason,
        )

        logger.info(
            f"[OK] Closed {pos.side} {symbol}: "
            f"PnL=${pnl:.2f} ({reason})"
        )
        return pnl

    def check_stop_losses(self):
        """Check all positions for stop-loss triggers."""
        for pos in list(self.positions):
            price = get_current_price(pos.symbol)
            if price <= 0:
                continue

            triggered = False
            if pos.side == "LONG" and price <= pos.stop_loss:
                triggered = True
            elif pos.side == "SHORT" and price >= pos.stop_loss:
                triggered = True

            if triggered:
                logger.warning(
                    f"[ALERT] STOP-LOSS triggered for {pos.symbol} "
                    f"@ ${price:.2f} (SL=${pos.stop_loss:.2f})"
                )
                self.close_position(pos.symbol, reason="stop_loss")

    def snapshot(self) -> dict:
        """Return current portfolio state as a dict."""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "mode": TRADE_MODE.value,
            "cash_usd": round(self.cash, 2),
            "total_equity_usd": round(self.total_equity, 2),
            "peak_equity_usd": round(self.peak_equity, 2),
            "drawdown_pct": round(
                ((self.peak_equity - self.total_equity) / self.peak_equity) * 100
                if self.peak_equity > 0 else 0,
                2,
            ),
            "open_positions": [
                {
                    "symbol": p.symbol,
                    "side": p.side,
                    "quantity": round(p.quantity, 6),
                    "entry_price": round(p.entry_price, 2),
                    "current_price": round(p.current_price, 2),
                    "pnl_usd": round(p.pnl_usd, 2),
                    "stop_loss": round(p.stop_loss, 2),
                }
                for p in self.positions
            ],
        }

    def _log_trade(self, **kwargs):
        """Append trade to SQLite ledger."""
        conn = get_connection()
        conn.execute(
            """
            INSERT INTO trades
            (symbol, action, quantity, price, pnl_usd, mode, strategy, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                kwargs.get("symbol", ""),
                kwargs.get("action", ""),
                kwargs.get("quantity", 0),
                kwargs.get("price", 0),
                kwargs.get("pnl_usd", 0),
                TRADE_MODE.value,
                kwargs.get("strategy", ""),
                kwargs.get("note", ""),
            ),
        )
        conn.commit()
        conn.close()
