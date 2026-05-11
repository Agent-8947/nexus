"""
NEXUS-FINANCE :: Trading Agent Orchestrator
===========================================
Autonomous orchestrator that:
1. Engages Strategy Developer to build strategies based on current market.
2. Arms the Analytical Center with the best strategy.
3. Streams real-time data to Analytical Center.
4. Executes trades on Test/Sandbox accounts via Risk Manager.
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime

# ── Add project root to path ──
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.settings import validate_config, TRADE_MODE, DEFAULT_SYMBOLS, DATA_INTERVAL
from db.database import init_db
from core.data_feed import fetch_ohlcv
from core.portfolio import PaperPortfolio
from core.strategy_developer import StrategyDeveloperAgent
from core.analytical_center import AnalyticalCenter

# ── Logging Setup ────────────────────────────────────────────
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)-14s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            LOG_DIR / f"agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
            encoding="utf-8",
        ),
    ],
)
logger = logging.getLogger("nexus.orchestrator")


class TradingOrchestrator:
    """
    Main autonomous orchestrator integrating all Nexus agents.
    """

    def __init__(self):
        self.portfolio = PaperPortfolio(initial_capital=10000.0)
        self.symbols = DEFAULT_SYMBOLS
        self.strategy_developer = StrategyDeveloperAgent()
        self.analytical_center = None

    def run_cycle(self):
        """Execute one full autonomous cycle."""
        logger.info("=" * 60)
        logger.info(f"NEXUS-FINANCE Autonomous Cycle | Mode: {TRADE_MODE.value} (Test/Sandbox/Paper)")
        logger.info(f"Symbols: {', '.join(self.symbols)}")
        logger.info("=" * 60)

        # ── 1. Strategy Development Phase ────────────────
        logger.info("── Phase 1: Strategy Development ──")
        # Fetch macro data for market regime detection
        macro_df = fetch_ohlcv("BTC/USDT", interval="1d", period="30d")
        optimal_config = self.strategy_developer.develop_strategies(macro_df)
        
        # ── 2. Analytical Center Initialization ──────────
        logger.info("── Phase 2: Analytical Center Activation ──")
        self.analytical_center = AnalyticalCenter(optimal_config)

        # ── 3. Stop-Loss & Risk Management ───────────────
        logger.info("── Phase 3: Risk Management & Stop-Losses ──")
        self.portfolio.check_stop_losses()

        # ── 4. Real-time Analysis & Execution ────────────
        logger.info("── Phase 4: Real-time Analysis ──")
        for symbol in self.symbols:
            symbol = symbol.strip()
            
            df = fetch_ohlcv(symbol, interval=DATA_INTERVAL, period="7d")
            if df.empty:
                logger.warning(f"No data for {symbol}. Skipping.")
                continue

            # Real-time analysis by Analytical Center
            signal = self.analytical_center.analyze_realtime(symbol, df)
            
            logger.info(
                f"Signal for {symbol}: {signal['action']} "
                f"(confidence={signal['confidence']:.1%}) - "
                f"{signal['reason']}"
            )

            # Execution Logic
            if signal["action"] == "BUY" and signal["confidence"] > 0.01: # Adjusted threshold for testing
                existing = next((p for p in self.portfolio.positions if p.symbol == symbol), None)
                if existing:
                    logger.info(f"Already holding {symbol}. Skip BUY.")
                    continue

                from config.settings import MAX_POSITION_SIZE_USD
                size = min(MAX_POSITION_SIZE_USD, self.portfolio.cash * 0.3)
                self.portfolio.open_position(
                    symbol=symbol,
                    side="LONG",
                    size_usd=size,
                    strategy=optimal_config["name"],
                )

            elif signal["action"] == "SELL":
                self.portfolio.close_position(
                    symbol=symbol,
                    reason=optimal_config["name"],
                )

        # ── 5. Reporting ─────────────────────────────────
        snapshot = self.portfolio.snapshot()
        logger.info("── Portfolio Snapshot ──")
        logger.info(json.dumps(snapshot, indent=2))

        return snapshot


def main():
    logger.info("+" + "=" * 55 + "+")
    logger.info("| NEXUS-FINANCE :: Autonomous Multi-Agent Trading System |")
    logger.info("+" + "=" * 55 + "+")

    try:
        validate_config()
        logger.info("[OK] Configuration validated. Ready for Sandbox/Paper/Testnet trading.")
    except RuntimeError as e:
        logger.critical(f"ABORT: {e}")
        sys.exit(1)

    init_db()

    orchestrator = TradingOrchestrator()
    snapshot = orchestrator.run_cycle()

    # ── Generate Dashboard ───────────────────────────
    try:
        from scripts.generate_dashboard import main as generate_dashboard
        generate_dashboard()
    except Exception as e:
        logger.error(f"Failed to generate dashboard: {e}")

    logger.info("=" * 60)
    logger.info("Autonomous cycle complete.")
    logger.info(f"Equity: ${snapshot['total_equity_usd']:.2f}")
    logger.info(f"Drawdown: {snapshot['drawdown_pct']:.2f}%")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
