"""
NEXUS-FINANCE :: SMA Crossover Strategy
════════════════════════════════════════
Classic dual moving average crossover.
Conservative, well-understood, low-risk.
"""

import pandas as pd
from core.strategy import BaseStrategy


class SMACrossover(BaseStrategy):
    """
    Signal logic:
    - BUY when fast SMA crosses above slow SMA
    - SELL when fast SMA crosses below slow SMA
    - HOLD otherwise
    """

    def __init__(self, fast_period: int = 10, slow_period: int = 30):
        self.fast_period = fast_period
        self.slow_period = slow_period

    @property
    def name(self) -> str:
        return f"SMA_Crossover({self.fast_period}/{self.slow_period})"

    def analyze(self, df: pd.DataFrame) -> dict:
        if len(df) < self.slow_period + 2:
            return {
                "action": "HOLD",
                "confidence": 0.0,
                "reason": f"Insufficient data ({len(df)} < {self.slow_period + 2})",
            }

        df = df.copy()
        df["sma_fast"] = df["close"].rolling(window=self.fast_period).mean()
        df["sma_slow"] = df["close"].rolling(window=self.slow_period).mean()

        # Current and previous crossover state
        current_fast = df["sma_fast"].iloc[-1]
        current_slow = df["sma_slow"].iloc[-1]
        prev_fast = df["sma_fast"].iloc[-2]
        prev_slow = df["sma_slow"].iloc[-2]

        # Crossover detection
        if prev_fast <= prev_slow and current_fast > current_slow:
            # Golden cross — bullish
            spread = abs(current_fast - current_slow) / current_slow
            confidence = min(spread * 100, 1.0)  # Larger spread = higher confidence
            return {
                "action": "BUY",
                "confidence": round(confidence, 3),
                "reason": (
                    f"Golden Cross: SMA{self.fast_period}={current_fast:.2f} "
                    f"crossed above SMA{self.slow_period}={current_slow:.2f}"
                ),
            }

        elif prev_fast >= prev_slow and current_fast < current_slow:
            # Death cross — bearish
            spread = abs(current_slow - current_fast) / current_slow
            confidence = min(spread * 100, 1.0)
            return {
                "action": "SELL",
                "confidence": round(confidence, 3),
                "reason": (
                    f"Death Cross: SMA{self.fast_period}={current_fast:.2f} "
                    f"crossed below SMA{self.slow_period}={current_slow:.2f}"
                ),
            }

        else:
            return {
                "action": "HOLD",
                "confidence": 0.0,
                "reason": (
                    f"No crossover. SMA{self.fast_period}={current_fast:.2f}, "
                    f"SMA{self.slow_period}={current_slow:.2f}"
                ),
            }
