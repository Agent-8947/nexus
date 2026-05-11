"""
NEXUS-FINANCE :: Strategy Base
══════════════════════════════
Abstract base class for all trading strategies.
"""

from abc import ABC, abstractmethod
import pandas as pd


class BaseStrategy(ABC):
    """
    Every strategy must implement:
    - name: human-readable identifier
    - analyze(): return a signal dict
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Strategy name for logging."""
        ...

    @abstractmethod
    def analyze(self, df: pd.DataFrame) -> dict:
        """
        Analyze OHLCV data and return a signal.

        Args:
            df: DataFrame with columns [open, high, low, close, volume]

        Returns:
            dict with keys:
                - action: 'BUY', 'SELL', or 'HOLD'
                - confidence: float 0.0 - 1.0
                - reason: str explanation
        """
        ...
