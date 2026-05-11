"""
NEXUS-FINANCE :: Analytical Center
==================================
Real-time analysis engine. Aggregates data, applies the
developed strategies, and rapidly issues trading positions.
"""
import logging
import pandas as pd
from core.strategy import BaseStrategy
from strategies.sma_crossover import SMACrossover
from strategies.rsi_strategy import RSIStrategy

logger = logging.getLogger("nexus.analytics")

class AnalyticalCenter:
    def __init__(self, active_strategy_config: dict):
        self.strategy_config = active_strategy_config
        self.strategy = self._instantiate_strategy(active_strategy_config)
        logger.info(f"[OK] Analytical Center armed with: {self.strategy.name}")

    def _instantiate_strategy(self, config: dict) -> BaseStrategy:
        st_type = config.get("type")
        if st_type == "SMA_Crossover":
            return SMACrossover(**config.get("params", {}))
        elif st_type == "RSI":
            return RSIStrategy(**config.get("params", {}))
        return SMACrossover()

    def analyze_realtime(self, symbol: str, current_data: pd.DataFrame) -> dict:
        """
        Performs real-time analysis on the latest data stream.
        """
        if current_data.empty:
            return {"action": "HOLD", "confidence": 0.0, "reason": "No data"}

        logger.info(f"Analytical Center processing real-time feed for {symbol}...")
        
        # Base strategy signal
        signal = self.strategy.analyze(current_data)
        
        # Analytical overlay (e.g., volume confirmation)
        if len(current_data) >= 2 and signal["action"] != "HOLD":
            current_vol = current_data['volume'].iloc[-1]
            avg_vol = current_data['volume'].rolling(10).mean().iloc[-1]
            
            if current_vol > avg_vol * 1.2:
                signal["confidence"] = min(signal["confidence"] * 1.5, 1.0)
                signal["reason"] += " | Confirmed by Volume Breakout"
            else:
                signal["confidence"] = signal["confidence"] * 0.8
                signal["reason"] += " | Low Volume Warning"
                
        return signal
