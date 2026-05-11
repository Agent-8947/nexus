"""
NEXUS-FINANCE :: RSI Strategy
=============================
Relative Strength Index (RSI) strategy.
Overbought (>70) -> SELL
Oversold (<30) -> BUY
"""

import logging
import pandas as pd
from core.strategy import BaseStrategy

logger = logging.getLogger("nexus.strategy.rsi")

class RSIStrategy(BaseStrategy):
    def __init__(self, period: int = 14, overbought: int = 70, oversold: int = 30):
        self.period = period
        self.overbought = overbought
        self.oversold = oversold

    @property
    def name(self) -> str:
        return f"RSI({self.period})"

    def analyze(self, df: pd.DataFrame) -> dict:
        if len(df) < self.period + 1:
            return {"action": "HOLD", "confidence": 0.0, "reason": "Not enough data"}

        # Calculate RSI
        delta = df['close'].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        # Use Wilder's moving average (smoothed)
        avg_gain = gain.ewm(com=self.period - 1, min_periods=self.period).mean()
        avg_loss = loss.ewm(com=self.period - 1, min_periods=self.period).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        current_rsi = rsi.iloc[-1]
        
        if pd.isna(current_rsi):
            return {"action": "HOLD", "confidence": 0.0, "reason": "RSI calculation yielded NaN"}

        if current_rsi < self.oversold:
            # Confidence grows as it gets deeper into oversold territory
            confidence = min((self.oversold - current_rsi) / 20.0, 1.0)
            return {
                "action": "BUY",
                "confidence": max(confidence, 0.1),
                "reason": f"Oversold territory (RSI={current_rsi:.2f})"
            }
        elif current_rsi > self.overbought:
            # Confidence grows as it gets deeper into overbought territory
            confidence = min((current_rsi - self.overbought) / 20.0, 1.0)
            return {
                "action": "SELL",
                "confidence": max(confidence, 0.1),
                "reason": f"Overbought territory (RSI={current_rsi:.2f})"
            }
        else:
            return {
                "action": "HOLD",
                "confidence": 0.0,
                "reason": f"RSI at {current_rsi:.2f} (Neutral)"
            }
