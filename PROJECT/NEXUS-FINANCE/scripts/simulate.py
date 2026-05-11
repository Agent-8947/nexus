"""
NEXUS-FINANCE :: Fast-Forward Simulator
=======================================
Simulates live trading over historical data to demonstrate
the agent's strategies and populate the dashboard with trades.
"""

import sys
import time
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

# ── Add project root to path ──
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from core.data_feed import fetch_ohlcv
from core.portfolio import PaperPortfolio, Position
from core.strategy_developer import StrategyDeveloperAgent
from core.analytical_center import AnalyticalCenter
from scripts.generate_dashboard import generate_html
from db.database import get_connection

def run_simulation():
    print("Initializing simulation...")
    
    # Clear old simulation data to have a clean view
    conn = get_connection()
    conn.execute("DELETE FROM trades")
    conn.execute("DELETE FROM portfolio")
    conn.execute("DELETE FROM equity_curve")
    conn.commit()
    conn.close()
    
    portfolio = PaperPortfolio(initial_capital=10000.0)
    dev = StrategyDeveloperAgent()
    
    symbol = "BTC/USDT"
    print(f"Fetching historical data for {symbol}...")
    df = fetch_ohlcv(symbol, interval="1h", period="7d", use_cache=False)
    
    if df.empty or len(df) < 50:
        print("Not enough data for simulation. Need at least 50 candles.")
        return
        
    print(f"Data loaded: {len(df)} candles. Starting simulation...")
    
    # Initialize strategy based on first 30 candles
    initial_slice = df.iloc[:30]
    config = dev.develop_strategies(initial_slice)
    center = AnalyticalCenter(config)
    
    # Simulate step-by-step
    start_idx = 30
    
    for i in range(start_idx, len(df)):
        current_slice = df.iloc[:i]
        current_candle = df.iloc[i]
        current_price = current_candle['close']
        ts = current_candle['timestamp']
        
        # Analyze
        signal = center.analyze_realtime(symbol, current_slice)
        
        # Mock the current price in portfolio execution
        # We need to monkey patch get_current_price or manually handle it.
        # For simplicity in simulation, we handle it manually here:
        
        if signal["action"] == "BUY" and signal["confidence"] > 0.1:
            existing = next((p for p in portfolio.positions if p.symbol == symbol), None)
            if not existing:
                size_usd = min(3000.0, portfolio.cash * 0.5)
                quantity = size_usd / current_price
                
                # Manual open to control price and timestamp
                pos = Position(
                    symbol=symbol,
                    side="LONG",
                    quantity=quantity,
                    entry_price=current_price,
                    stop_loss=current_price * 0.95,
                    timestamp=ts
                )
                portfolio.cash -= size_usd
                portfolio.positions.append(pos)
                
                # Log trade
                conn = get_connection()
                conn.execute(
                    "INSERT INTO trades (symbol, action, quantity, price, pnl_usd, mode, strategy, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (symbol, "BUY", quantity, current_price, 0.0, "PAPER", config["name"], ts)
                )
                conn.commit()
                conn.close()
                print(f"[{ts}] SIM BUY {symbol} @ ${current_price:.2f}")
                
        elif signal["action"] == "SELL":
            pos = next((p for p in portfolio.positions if p.symbol == symbol), None)
            if pos:
                pnl = (current_price - pos.entry_price) * pos.quantity
                portfolio.cash += pos.quantity * current_price
                portfolio.positions.remove(pos)
                
                # Log trade
                conn = get_connection()
                conn.execute(
                    "INSERT INTO trades (symbol, action, quantity, price, pnl_usd, mode, strategy, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (symbol, "SELL", pos.quantity, current_price, pnl, "PAPER", config["name"], ts)
                )
                conn.commit()
                conn.close()
                print(f"[{ts}] SIM SELL {symbol} @ ${current_price:.2f} | PnL: ${pnl:.2f}")
                
        # Check stop loss
        for pos in list(portfolio.positions):
            if current_price <= pos.stop_loss:
                pnl = (current_price - pos.entry_price) * pos.quantity
                portfolio.cash += pos.quantity * current_price
                portfolio.positions.remove(pos)
                
                conn = get_connection()
                conn.execute(
                    "INSERT INTO trades (symbol, action, quantity, price, pnl_usd, mode, strategy, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (symbol, "STOP_LOSS", pos.quantity, current_price, pnl, "PAPER", "stop_loss", ts)
                )
                conn.commit()
                conn.close()
                print(f"[{ts}] SIM STOP LOSS {symbol} @ ${current_price:.2f} | PnL: ${pnl:.2f}")

        # Update equity curve occasionally
        if i % 5 == 0:
            total_equity = portfolio.cash + sum(p.quantity * current_price for p in portfolio.positions)
            conn = get_connection()
            conn.execute(
                "INSERT INTO equity_curve (timestamp, total_usd, cash_usd, positions_usd) VALUES (?, ?, ?, ?)",
                (ts, total_equity, portfolio.cash, total_equity - portfolio.cash)
            )
            conn.commit()
            conn.close()

    print("Simulation complete. Generating dashboard...")
    generate_html()
    print("Dashboard updated with simulation data.")

if __name__ == "__main__":
    run_simulation()
