import os
import json
import re
from pathlib import Path
from datetime import datetime

# ─── CONFIG ───────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS")
WIKI_ROOT   = PROJECT_ROOT / "PROJECT" / "WIKI"
STATE_FILE  = WIKI_ROOT / "nexus_farm_state.json"
DASHBOARD_FILE = PROJECT_ROOT / "FARM_STATUS.html"

# ─── TEMPLATE ─────────────────────────────────────────────────────────────────
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="30">
    <title>NEXUS FARMING DASHBOARD</title>
    <style>
        :root {{
            --bg: #0a0a0c;
            --card: #141418;
            --accent: #3b82f6;
            --text: #e2e8f0;
            --dim: #94a3b8;
            --star: #fbbf24;
        }}
        body {{
            background: var(--bg);
            color: var(--text);
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            margin: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }}
        .header {{
            width: 100%;
            padding: 2rem 0;
            background: linear-gradient(to bottom, #111827, transparent);
            text-align: center;
            border-bottom: 1px solid #1f2937;
        }}
        .status-container {{
            width: 90%;
            max-width: 1200px;
            margin: 2rem 0;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }}
        .card {{
            background: var(--card);
            border: 1px solid #1f2937;
            border-radius: 12px;
            padding: 1.5rem;
        }}
        .progress-bar {{
            height: 8px;
            background: #1f2937;
            border-radius: 4px;
            margin: 1rem 0;
            overflow: hidden;
        }}
        .progress-fill {{
            height: 100%;
            background: var(--accent);
            width: {progress}%;
            transition: width 1s ease-in-out;
            box-shadow: 0 0 20px var(--accent);
        }}
        .stat-value {{
            font-size: 2.5rem;
            font-weight: 800;
            color: var(--accent);
        }}
        .stat-label {{
            color: var(--dim);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 0.8rem;
        }}
        .repo-list {{
            list-style: none;
            padding: 0;
        }}
        .repo-item {{
            padding: 0.75rem 0;
            border-bottom: 1px solid #1f2937;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .domain-tag {{
            background: #1e293b;
            color: var(--accent);
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .score {{
            color: var(--star);
            font-weight: bold;
        }}
        .full-registry {{
            width: 90%;
            max-width: 1200px;
            margin: 2rem auto;
            background: var(--card);
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid #1f2937;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
        }}
        th {{
            text-align: left;
            color: var(--dim);
            border-bottom: 1px solid #1f2937;
            padding: 1rem;
            font-size: 0.8rem;
            text-transform: uppercase;
        }}
        td {{
            padding: 1rem;
            border-bottom: 1px solid #0f172a;
            font-size: 0.9rem;
        }}
        tr:hover {{
            background: #1e293b;
        }}
        .search-box {{
            width: 100%;
            padding: 12px;
            background: #0f172a;
            border: 1px solid #1f2937;
            border-radius: 8px;
            color: white;
            margin-bottom: 1rem;
            box-sizing: border-box;
        }}
    </style>
    <script>
        function filterTable() {{
            let input = document.getElementById('repoSearch');
            let filter = input.value.toUpperCase();
            let tr = document.querySelectorAll('.repo-row');
            tr.forEach(row => {{
                let text = row.textContent || row.innerText;
                row.style.display = text.toUpperCase().indexOf(filter) > -1 ? "" : "none";
            }});
        }}
    </script>
</head>
<body>
    <div class="header">
        <h1>NEXUS INTELLIGENCE FACTORY</h1>
        <div style="display: flex; align-items: center; justify-content: center; gap: 2rem;">
            <div><span class="pulse"></span><span style="color: #10b981;">LIVE AGENT-24 ACTION</span></div>
            <div style="color: var(--dim);">Last Updated: {last_sync}</div>
        </div>
    </div>

    <div class="status-container">
        <div class="card">
            <div class="stat-label">Global Wiki Ingestion</div>
            <div class="stat-value">{progress}%</div>
            <div class="progress-bar"><div class="progress-fill"></div></div>
            <div style="display: flex; justify-content: space-between;">
                <span>Processed: <b>{processed_count}</b></span>
                <span>Total: <b>{total_count}</b></span>
            </div>
        </div>

        <div class="card">
            <div class="stat-label">Top High-Value Discoveries</div>
            <ul class="repo-list">
                {top_repos}
            </ul>
        </div>

        <div class="card">
            <div class="stat-label">Recent Activity (Last 5)</div>
            <ul class="repo-list">
                {recent_activity}
            </ul>
        </div>
    </div>

    <div class="full-registry">
        <div class="stat-label">Full Intelligent Registry</div>
        <input type="text" id="repoSearch" class="search-box" onkeyup="filterTable()" placeholder="Поиск по названию, категории или описанию...">
        <table>
            <thead>
                <tr>
                    <th>Repository</th>
                    <th>Domain</th>
                    <th>Score</th>
                    <th>Intelligence Summary</th>
                </tr>
            </thead>
            <tbody>
                {full_table}
            </tbody>
        </table>
    </div>

    <div class="footer">
        Powered by NEXUS AI Core • Local Qwen2.5-coder:3b • 2026 MSD
    </div>
</body>
</html>
"""

# ─── LOGIC ────────────────────────────────────────────────────────────────────
def generate():
    if not STATE_FILE.exists():
        print("[!] No state file found.")
        return

    state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    processed = state.get("processed", [])
    
    all_repos = [d for d in WIKI_ROOT.iterdir() if d.is_dir() and not d.name.startswith("__")]
    total_count = len(all_repos)
    processed_count = len(processed)
    progress = round((processed_count / total_count) * 100, 1) if total_count > 0 else 0

    analyses = []
    # Scan more for the full table
    for repo_name in processed:
        analysis_path = WIKI_ROOT / repo_name / "NEXUS_ANALYSIS.md"
        if analysis_path.exists():
            content = analysis_path.read_text(encoding="utf-8")
            domain = "OTHER"
            score = "0"
            summary = "No summary found."
            
            d_match = re.search(r"Domain\*\* \| `(.*?)` \|", content)
            s_match = re.search(r"NEXUS Value\*\* \| .* (\d+)/10 \|", content)
            sum_match = re.search(r"## Summary\n(.*?)\n", content, re.DOTALL)
            
            if d_match: domain = d_match.group(1)
            if s_match: score = s_match.group(1)
            if sum_match: summary = sum_match.group(1).strip()
            
            analyses.append({
                "name": repo_name,
                "domain": domain,
                "score": int(score),
                "summary": summary
            })

    # Recent activity
    recent_html = ""
    for a in reversed(analyses[-5:]):
        recent_html += f"""
        <li class="repo-item">
            <span>{a['name'][:25]}</span>
            <span class="domain-tag">{a['domain']}</span>
        </li>
        """

    # Top repos
    top_repos = sorted(analyses, key=lambda x: x['score'], reverse=True)[:5]
    top_html = ""
    for a in top_repos:
        top_html += f"""
        <li class="repo-item">
            <span>{a['name'][:25]}</span>
            <span class="score">⭐ {a['score']}</span>
        </li>
        """

    # Full table
    table_html = ""
    for a in reversed(analyses):
        table_html += f"""
        <tr class="repo-row">
            <td style="font-weight:600; color:var(--accent);">{a['name']}</td>
            <td><span class="domain-tag">{a['domain']}</span></td>
            <td class="score">{a['score']}/10</td>
            <td style="color:var(--dim); font-size:0.85rem;">{a['summary']}</td>
        </tr>
        """

    html = HTML_TEMPLATE.format(
        progress=progress,
        processed_count=processed_count,
        total_count=total_count,
        recent_activity=recent_html,
        top_repos=top_html,
        full_table=table_html,
        last_sync=datetime.now().strftime("%H:%M:%S")
    )
    
    DASHBOARD_FILE.write_text(html, encoding="utf-8")
    print(f"[✓] Dashboard updated: {DASHBOARD_FILE}")

if __name__ == "__main__":
    generate()
