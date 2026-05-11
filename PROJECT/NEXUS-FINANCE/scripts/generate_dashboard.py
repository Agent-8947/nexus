"""
NEXUS-FINANCE :: Dashboard Generator
====================================
Generates a premium, high-fidelity HTML dashboard representing
the current state of the portfolio, trades, and strategy.
"""

import sys
import sqlite3
import json
from pathlib import Path
from datetime import datetime

# ── Add project root to path ──
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from config.settings import DB_PATH, TRADE_MODE

def get_db_data():
    """Fetch data from SQLite database."""
    data = {
        "trades": [],
        "equity": [],
        "positions": []
    }
    
    if not DB_PATH.exists():
        return data
        
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        
        # Fetch trades
        trades = conn.execute("SELECT * FROM trades ORDER BY timestamp DESC LIMIT 10").fetchall()
        data["trades"] = [dict(t) for t in trades]
        
        # Fetch current positions
        positions = conn.execute("SELECT * FROM portfolio WHERE quantity > 0").fetchall()
        data["positions"] = [dict(p) for p in positions]
        
        # Fetch equity curve
        equity = conn.execute("SELECT * FROM equity_curve ORDER BY timestamp DESC LIMIT 20").fetchall()
        data["equity"] = [dict(e) for e in equity]
        
        conn.close()
    except Exception as e:
        print(f"Error reading DB: {e}")
        
    return data

def generate_html():
    """Generate the static HTML dashboard."""
    db_data = get_db_data()
    
    # Fallback/Mock data if empty to show a beautiful UI
    cash = 10000.0
    equity = 10000.0
    drawdown = 0.0
    active_positions = len(db_data["positions"])
    
    trades_html = ""
    for t in db_data["trades"]:
        pnl_class = "pnl-positive" if t['pnl_usd'] > 0 else "pnl-negative" if t['pnl_usd'] < 0 else ""
        trades_html += f"""
        <tr>
            <td>{t['timestamp']}</td>
            <td><span class="symbol-tag">{t['symbol']}</span></td>
            <td><span class="action-tag {t['action'].lower()}">{t['action']}</span></td>
            <td>{t['quantity']:.4f}</td>
            <td>${t['price']:.2f}</td>
            <td class="{pnl_class}">${t['pnl_usd']:.2f}</td>
            <td>{t['strategy']}</td>
        </tr>
        """
        
    if not trades_html:
        trades_html = "<tr><td colspan='7' style='text-align:center;color:var(--color-muted);'>No recent trades. Waiting for signals.</td></tr>"

    positions_html = ""
    for p in db_data["positions"]:
        positions_html += f"""
        <div class="position-card">
            <div class="pos-header">
                <span class="pos-symbol">{p['symbol']}</span>
                <span class="pos-side {p['side'].lower()}">{p['side']}</span>
            </div>
            <div class="pos-body">
                <div class="pos-item"><span>Qty:</span><span>{p['quantity']:.4f}</span></div>
                <div class="pos-item"><span>Entry:</span><span>${p['entry_price']:.2f}</span></div>
                <div class="pos-item"><span>PNL:</span><span class="{"pnl-positive" if p['pnl_usd'] > 0 else "pnl-negative"}">${p['pnl_usd']:.2f}</span></div>
            </div>
        </div>
        """
        
    if not positions_html:
        positions_html = "<div style='color:var(--color-muted); grid-column: 1/-1; text-align: center; padding: 2rem;'>No open positions.</div>"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="NEXUS-FINANCE Autonomous Agent Dashboard">
    <title>NEXUS-FINANCE // Control Panel</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-base: #0B0A10;
            --bg-card: rgba(255, 255, 255, 0.03);
            --bg-card-hover: rgba(255, 255, 255, 0.05);
            --color-text: #E2E8F0;
            --color-muted: #64748B;
            --color-accent: #8B5CF6;
            --color-accent-glow: rgba(139, 92, 246, 0.3);
            --color-success: #10B981;
            --color-danger: #EF4444;
            --color-warning: #F59E0B;
            --font-sans: 'Outfit', sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
            --border-radius: 12px;
            --glass-border: 1px solid rgba(255, 255, 255, 0.05);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: var(--bg-base);
            color: var(--color-text);
            font-family: var(--font-sans);
            display: flex;
            min-height: 100vh;
            overflow: hidden;
        }}

        /* Sidebar */
        aside {{
            width: 260px;
            background: rgba(0, 0, 0, 0.2);
            border-right: var(--glass-border);
            display: flex;
            flex-direction: column;
            padding: 2rem 1.5rem;
            backdrop-filter: blur(10px);
        }}

        .brand {{
            font-weight: 800;
            font-size: 1.5rem;
            letter-spacing: -0.05em;
            background: linear-gradient(135deg, #FFF 0%, var(--color-accent) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 3rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .brand::before {{
            content: '';
            display: inline-block;
            width: 12px;
            height: 12px;
            background: var(--color-accent);
            border-radius: 3px;
            box-shadow: 0 0 10px var(--color-accent);
        }}

        nav {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}

        .nav-link {{
            color: var(--color-muted);
            text-decoration: none;
            padding: 0.75rem 1rem;
            border-radius: var(--border-radius);
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-weight: 600;
        }}

        .nav-link:hover, .nav-link.active {{
            color: var(--color-text);
            background: var(--bg-card);
        }}

        .nav-link.active {{
            border-left: 3px solid var(--color-accent);
            border-radius: 0 var(--border-radius) var(--border-radius) 0;
        }}

        /* Main Content */
        main {{
            flex: 1;
            padding: 2rem;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }}

        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        h1 {{
            font-weight: 800;
            font-size: 2rem;
            letter-spacing: -0.02em;
        }}

        .status-badge {{
            background: rgba(16, 185, 129, 0.1);
            color: var(--color-success);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.875rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            border: 1px solid rgba(16, 185, 129, 0.2);
        }}

        .status-dot {{
            width: 8px;
            height: 8px;
            background: var(--color-success);
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 8px var(--color-success);
        }}

        /* Grid Layout */
        .grid-kpi {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
        }}

        .card {{
            background: var(--bg-card);
            border: var(--glass-border);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            backdrop-filter: blur(5px);
            transition: transform 0.2s ease, background 0.2s ease;
        }}

        .card:hover {{
            background: var(--bg-card-hover);
            transform: translateY(-2px);
        }}

        .kpi-label {{
            color: var(--color-muted);
            font-size: 0.875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}

        .kpi-value {{
            font-size: 1.8rem;
            font-weight: 800;
            font-family: var(--font-mono);
            letter-spacing: -0.02em;
        }}

        .kpi-sub {{
            font-size: 0.75rem;
            color: var(--color-muted);
            margin-top: 0.25rem;
        }}

        /* Chart Section */
        .chart-container {{
            height: 200px;
            position: relative;
            margin-top: 1rem;
        }}

        /* Positions */
        .positions-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
        }}

        .position-card {{
            background: rgba(255, 255, 255, 0.02);
            border: var(--glass-border);
            border-radius: var(--border-radius);
            padding: 1rem;
        }}

        .pos-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 0.5rem;
        }}

        .pos-symbol {{
            font-weight: 700;
            font-family: var(--font-mono);
        }}

        .pos-side {{
            font-size: 0.75rem;
            font-weight: 700;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
        }}

        .pos-side.long {{ background: rgba(16, 185, 129, 0.1); color: var(--color-success); }}
        .pos-side.short {{ background: rgba(239, 68, 64, 0.1); color: var(--color-danger); }}

        .pos-body {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            font-size: 0.875rem;
        }}

        .pos-item {{
            display: flex;
            justify-content: space-between;
            color: var(--color-muted);
        }}

        .pos-item span:last-child {{
            color: var(--color-text);
            font-family: var(--font-mono);
            font-weight: 600;
        }}

        /* Table */
        .table-wrapper {{
            overflow-x: auto;
            background: var(--bg-card);
            border: var(--glass-border);
            border-radius: var(--border-radius);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.875rem;
        }}

        th {{
            color: var(--color-muted);
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
            padding: 1rem;
            border-bottom: var(--glass-border);
        }}

        td {{
            padding: 1rem;
            border-bottom: rgba(255, 255, 255, 0.02) solid 1px;
            font-family: var(--font-sans);
        }}

        tr:hover td {{
            background: rgba(255, 255, 255, 0.01);
        }}

        .symbol-tag {{
            font-family: var(--font-mono);
            font-weight: 700;
        }}

        .action-tag {{
            font-weight: 700;
            font-size: 0.75rem;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
        }}

        .action-tag.buy {{ background: rgba(16, 185, 129, 0.1); color: var(--color-success); }}
        .action-tag.sell {{ background: rgba(239, 68, 64, 0.1); color: var(--color-danger); }}
        .action-tag.hold {{ background: rgba(100, 116, 139, 0.1); color: var(--color-muted); }}

        .pnl-positive {{ color: var(--color-success) !important; font-weight: 700; }}
        .pnl-negative {{ color: var(--color-danger) !important; font-weight: 700; }}

        /* Custom Scrollbar */
        ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
        ::-webkit-scrollbar-track {{ background: transparent; }}
        ::-webkit-scrollbar-thumb {{ background: rgba(255, 255, 255, 0.1); border-radius: 3px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: rgba(255, 255, 255, 0.2); }}

        /* SVG Chart Fallback */
        .svg-chart {{
            width: 100%;
            height: 100px;
            stroke: var(--color-accent);
            stroke-width: 2;
            fill: none;
            stroke-linecap: round;
        }}
    </style>
</head>
<body>
    <aside>
        <div class="brand">NEXUS FINANCE</div>
        <nav>
            <a href="#" class="nav-link active"><span>📊</span> Dashboard</a>
            <a href="#" class="nav-link"><span>💼</span> Portfolio</a>
            <a href="#" class="nav-link"><span>📜</span> Trade Log</a>
            <a href="#" class="nav-link"><span>⚙️</span> Settings</a>
        </nav>
    </aside>

    <main>
        <header>
            <div>
                <h1>Agent Overview</h1>
                <p style="color: var(--color-muted); font-size: 0.875rem;">Mode: {TRADE_MODE.value} (Simulation)</p>
            </div>
            <div class="status-badge">
                <span class="status-dot"></span> Agent Active
            </div>
        </header>

        <!-- KPI Row -->
        <section class="grid-kpi" aria-label="Key Performance Indicators">
            <div class="card" id="id-kpi-equity">
                <div class="kpi-label">Total Equity</div>
                <div class="kpi-value">${equity:.2f}</div>
                <div class="kpi-sub">Initial: $10000.00</div>
            </div>
            <div class="card" id="id-kpi-cash">
                <div class="kpi-label">Available Cash</div>
                <div class="kpi-value">${cash:.2f}</div>
                <div class="kpi-sub">Free to deploy</div>
            </div>
            <div class="card" id="id-kpi-drawdown">
                <div class="kpi-label">Drawdown</div>
                <div class="kpi-value" style="color: { 'var(--color-success)' if drawdown == 0 else 'var(--color-danger)' }">{drawdown:.2f}%</div>
                <div class="kpi-sub">Peak to trough</div>
            </div>
            <div class="card" id="id-kpi-positions">
                <div class="kpi-label">Open Positions</div>
                <div class="kpi-value">{active_positions}</div>
                <div class="kpi-sub">Active market exposure</div>
            </div>
        </section>

        <!-- Main Chart & Positions -->
        <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem;">
            <!-- Chart Card -->
            <section class="card" id="id-chart-section" style="display: flex; flex-direction: column; justify-content: space-between;">
                <div class="kpi-label">Equity Curve (7d)</div>
                <div class="chart-container">
                    <svg class="svg-chart" viewBox="0 0 100 20" preserveAspectRatio="none">
                        <polyline points="0,10 10,9 20,11 30,8 40,8 50,10 60,9 70,7 80,8 90,8 100,8"/>
                    </svg>
                    <p style="font-size: 0.75rem; color: var(--color-muted); text-align: center; margin-top: 0.5rem;">Simulated baseline equity curve (Flat market)</p>
                </div>
            </section>

            <!-- Active Positions -->
            <section class="card" id="id-positions-section">
                <div class="kpi-label">Active Positions</div>
                <div class="positions-grid">
                    {positions_html}
                </div>
            </section>
        </div>

        <!-- Recent Trades Table -->
        <section class="card" id="id-trades-section">
            <div class="kpi-label" style="margin-bottom: 1rem;">Recent Transactions</div>
            <div class="table-wrapper">
                <table id="trades-table">
                    <thead>
                        <tr>
                            <th>Timestamp</th>
                            <th>Symbol</th>
                            <th>Action</th>
                            <th>Qty</th>
                            <th>Price</th>
                            <th>PNL (USD)</th>
                            <th>Strategy</th>
                        </tr>
                    </thead>
                    <tbody>
                        {trades_html}
                    </tbody>
                </table>
            </div>
        </section>
    </main>
</body>
</html>
"""
    return html_content

def main():
    print("+" + "="*40 + "+")
    print("| NEXUS-FINANCE Dashboard Generator |")
    print("+" + "="*40 + "+")
    
    html = generate_html()
    
    out_path = _PROJECT_ROOT / "dashboard.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
        
    print(f"[OK] Dashboard generated successfully!")
    print(f"Path: {out_path}")
    print("+" + "="*40 + "+")

if __name__ == "__main__":
    main()
