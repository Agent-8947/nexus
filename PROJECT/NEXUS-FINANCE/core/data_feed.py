"""
NEXUS-FINANCE :: Data Feed
==========================
Market data fetching via yfinance (free, no API key).
Caches results in SQLite to avoid redundant network calls.
"""

import sys
import logging
from datetime import datetime, timedelta
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import pandas as pd
import yfinance as yf

from db.database import get_connection

logger = logging.getLogger("nexus.data")

# yfinance uses Yahoo tickers, not exchange pairs.
# This map converts common crypto pairs to Yahoo format.
SYMBOL_MAP = {
    "BTC/USDT": "BTC-USD",
    "ETH/USDT": "ETH-USD",
    "SOL/USDT": "SOL-USD",
    "BNB/USDT": "BNB-USD",
    "XRP/USDT": "XRP-USD",
    "ADA/USDT": "ADA-USD",
    "DOGE/USDT": "DOGE-USD",
    "AAPL": "AAPL",
    "MSFT": "MSFT",
    "GOOGL": "GOOGL",
    "TSLA": "TSLA",
    "AMZN": "AMZN",
    "NVDA": "NVDA",
}


def _to_yahoo(symbol: str) -> str:
    """Convert CCXT-style symbol to Yahoo ticker."""
    return SYMBOL_MAP.get(symbol, symbol.replace("/", "-"))


def fetch_ohlcv(
    symbol: str,
    interval: str = "1h",
    period: str = "30d",
    use_cache: bool = True,
) -> pd.DataFrame:
    """
    Fetch OHLCV data for a symbol.

    Args:
        symbol: e.g. 'BTC/USDT' or 'AAPL'
        interval: '1m', '5m', '15m', '1h', '1d'
        period: '7d', '30d', '90d', '1y'
        use_cache: if True, check SQLite cache first

    Returns:
        DataFrame with columns: open, high, low, close, volume
    """
    yahoo_ticker = _to_yahoo(symbol)

    if use_cache:
        cached = _load_from_cache(symbol, interval)
        if cached is not None and len(cached) > 0:
            # Check if cache is fresh (less than 1 hour old)
            last_ts = pd.to_datetime(cached["timestamp"].iloc[-1])
            if datetime.utcnow() - last_ts < timedelta(hours=1):
                logger.info(f"Cache hit for {symbol} ({len(cached)} rows)")
                return cached

    try:
        ticker = yf.Ticker(yahoo_ticker)
        df = ticker.history(period=period, interval=interval)

        if df.empty:
            logger.warning(f"No data returned for {yahoo_ticker}")
            return pd.DataFrame()

        df = df.rename(columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        })
        df = df[["open", "high", "low", "close", "volume"]].copy()
        df["timestamp"] = df.index.strftime("%Y-%m-%d %H:%M:%S")
        df = df.reset_index(drop=True)

        if use_cache:
            _save_to_cache(symbol, interval, df)

        logger.info(f"Fetched {len(df)} candles for {symbol}")
        return df

    except Exception as e:
        logger.error(f"Failed to fetch data for {symbol}: {e}")
        # Fallback to cache even if stale
        cached = _load_from_cache(symbol, interval)
        if cached is not None:
            logger.warning(f"Using stale cache for {symbol}")
            return cached
        return pd.DataFrame()


def get_current_price(symbol: str) -> float:
    """Get the latest price for a symbol. Returns 0.0 on failure."""
    try:
        yahoo_ticker = _to_yahoo(symbol)
        ticker = yf.Ticker(yahoo_ticker)
        data = ticker.history(period="1d", interval="1m")
        if data.empty:
            return 0.0
        return float(data["Close"].iloc[-1])
    except Exception as e:
        logger.error(f"Failed to get price for {symbol}: {e}")
        return 0.0


def _save_to_cache(symbol: str, interval: str, df: pd.DataFrame):
    """Save OHLCV data to SQLite cache."""
    conn = get_connection()
    for _, row in df.iterrows():
        conn.execute(
            """
            INSERT OR REPLACE INTO ohlcv_cache
            (symbol, interval, timestamp, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                symbol, interval, row["timestamp"],
                row["open"], row["high"], row["low"],
                row["close"], row["volume"],
            ),
        )
    conn.commit()
    conn.close()


def _load_from_cache(symbol: str, interval: str) -> pd.DataFrame | None:
    """Load OHLCV data from SQLite cache."""
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT timestamp, open, high, low, close, volume
        FROM ohlcv_cache
        WHERE symbol = ? AND interval = ?
        ORDER BY timestamp
        """,
        (symbol, interval),
    ).fetchall()
    conn.close()

    if not rows:
        return None

    return pd.DataFrame(
        [dict(r) for r in rows],
        columns=["timestamp", "open", "high", "low", "close", "volume"],
    )
