import json
from pathlib import Path
from llm_evaluator import LLMEvaluator, get_tier, DOMAINS

def generate_html(data):
    # Calculate domain stats
    domain_stats = []
    for domain, items in data.items():
        if not items: continue
        avg = sum(i["fitness"] for i in items) / len(items)
        s_count = sum(1 for i in items if "S " in i["tier"])
        a_count = sum(1 for i in items if "A " in i["tier"])
        b_count = sum(1 for i in items if "B " in i["tier"])
        c_count = sum(1 for i in items if "C " in i["tier"])
        d_count = sum(1 for i in items if "D " in i["tier"])
        f_count = sum(1 for i in items if "F " in i["tier"])

        domain_stats.append({
            "name": domain,
            "avg": round(avg, 3),
            "tier": get_tier(avg),
            "count": len(items),
            "distribution": [s_count, a_count, b_count, c_count, d_count, f_count]
        })

    # Prepare JSON strings for frontend
    domains_json = json.dumps(domain_stats)
    agents_json = json.dumps(data)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXUS DNA Rating Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <style>
        :root {{
            --bg-deep: #0a0a0e;
            --glass-bg: rgba(20, 20, 30, 0.6);
            --glass-border: rgba(255, 255, 255, 0.08);
            --primary: #00ffcc;
            --primary-glow: rgba(0, 255, 204, 0.4);
            --text-main: #f0f0f5;
            --text-muted: #8a8a9e;
            --danger: #ff3366;
            --warning: #ffcc00;
            --success: #33ff77;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Outfit', sans-serif;
            background: var(--bg-deep) radial-gradient(circle at 50% 0, rgba(0, 255, 204, 0.15) 0%, transparent 60%);
            color: var(--text-main);
            min-height: 100vh;
            overflow-x: hidden;
            padding: 2rem;
        }}
        .glass {{
            background: var(--glass-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            border-radius: 1.5rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}
        header {{
            text-align: center;
            margin-bottom: 3rem;
            opacity: 0;
            transform: translateY(-20px);
        }}
        h1 {{
            font-weight: 800;
            font-size: 3rem;
            background: linear-gradient(90deg, #fff, var(--primary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}
        .subtitle {{ color: var(--text-muted); font-size: 1.1rem; letter-spacing: 1px; }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }}
        .card {{
            padding: 1.5rem;
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            opacity: 0;
            transform: translateY(30px);
        }}
        .card:hover {{
            transform: translateY(-5px);
            border-color: var(--primary-glow);
            box-shadow: 0 0 20px var(--primary-glow);
        }}
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            border-bottom: 1px solid var(--glass-border);
            padding-bottom: 1rem;
        }}
        .domain-name {{ font-size: 1.4rem; font-weight: 600; color: #fff; }}
        .score-badge {{
            background: rgba(0, 255, 204, 0.1);
            color: var(--primary);
            padding: 0.4rem 1rem;
            border-radius: 2rem;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
            font-size: 1.1rem;
        }}
        
        .agent-list {{
            margin-top: 2rem;
            max-width: 1400px;
            margin: 2rem auto;
            opacity: 0;
            transform: translateY(30px);
        }}
        .agent-list h2 {{ text-align: center; margin-bottom: 1.5rem; font-weight: 600; }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid var(--glass-border);
        }}
        th {{
            color: var(--text-muted);
            font-weight: 400;
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 1px;
        }}
        .agent-name {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            color: #fff;
        }}
        
        .tier-S {{ color: #e024ff; text-shadow: 0 0 10px rgba(224,36,255,0.5); }}
        .tier-A {{ color: var(--primary); text-shadow: 0 0 10px var(--primary-glow); }}
        .tier-B {{ color: var(--success); }}
        .tier-C {{ color: #33aaff; }}
        .tier-D {{ color: var(--warning); }}
        .tier-F {{ color: var(--danger); text-shadow: 0 0 10px rgba(255,51,102,0.5); }}
        
        .issues-tag {{
            display: inline-block;
            background: rgba(255, 51, 102, 0.1);
            color: var(--danger);
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-size: 0.8rem;
            margin-right: 0.5rem;
            margin-bottom: 0.2rem;
        }}
        
        canvas {{ max-height: 200px; margin-top: 1rem; }}
    </style>
</head>
<body>

    <header>
        <h1>NEXUS DNA RATING</h1>
        <p class="subtitle">Autonomous AI Agent Fitness & LLM Benchmarking</p>
    </header>

    <div class="grid" id="domain-grid"></div>

    <div class="glass agent-list" id="agents-section">
        <h2>Top Synthesis Results</h2>
        <table>
            <thead>
                <tr>
                    <th>Domain</th>
                    <th>Agent Identifier</th>
                    <th>Fitness Score</th>
                    <th>Tier Class</th>
                    <th>Risk Vectors (Issues)</th>
                </tr>
            </thead>
            <tbody id="agent-table-body">
            </tbody>
        </table>
    </div>

    <script>
        const domains = {domains_json};
        const agentsData = {agents_json};
        
        // Populate Domains grid
        const grid = document.getElementById('domain-grid');
        domains.forEach((dom, index) => {{
            const card = document.createElement('div');
            card.className = 'glass card';
            card.innerHTML = `
                <div class="card-header">
                    <div class="domain-name">${{dom.name.replace('DNA_', '')}}</div>
                    <div class="score-badge">${{dom.avg.toFixed(3)}}</div>
                </div>
                <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom: 1rem">${{dom.count}} Agents Evaluated — <strong>Tier ${{dom.tier.split(' ')[0]}}</strong></p>
                <canvas id="chart-${{index}}"></canvas>
            `;
            grid.appendChild(card);
            
            // Render Chart
            const ctx = document.getElementById(`chart-${{index}}`).getContext('2d');
            new Chart(ctx, {{
                type: 'doughnut',
                data: {{
                    labels: ['S', 'A', 'B', 'C', 'D', 'F'],
                    datasets: [{{
                        data: dom.distribution,
                        backgroundColor: [
                            '#e024ff', '#00ffcc', '#33ff77', '#33aaff', '#ffcc00', '#ff3366'
                        ],
                        borderWidth: 0,
                        hoverOffset: 4
                    }}]
                }},
                options: {{
                    responsive: true,
                    cutout: '75%',
                    plugins: {{
                        legend: {{ display: false }}
                    }}
                }}
            }});
        }});

        // Populate Top Agents Table
        const tbody = document.getElementById('agent-table-body');
        let allAgents = [];
        for (let dom in agentsData) {{
            agentsData[dom].forEach(agent => {{
                allAgents.push({{...agent, domain: dom}});
            }});
        }}
        
        // Sort by fitness descending
        allAgents.sort((a, b) => b.fitness - a.fitness);
        
        // Show top 30
        allAgents.slice(0, 30).forEach(agent => {{
            const tr = document.createElement('tr');
            
            const tierShort = agent.tier.split(' ')[0];
            const tierClass = "tier-" + tierShort;
            
            let issuesHtml = "";
            if (agent.issues && agent.issues.length > 0) {{
                issuesHtml = agent.issues.map(i => `<span class="issues-tag">${{i}}</span>`).join("");
            }} else {{
                issuesHtml = '<span style="color:var(--success); font-size:0.8rem">Zero Risk</span>';
            }}
            
            tr.innerHTML = `
                <td style="color:var(--text-muted); font-size:0.8rem">${{agent.domain.replace('DNA_', '')}}</td>
                <td class="agent-name">${{agent.file}}</td>
                <td style="font-family:'JetBrains Mono', monospace">${{agent.fitness.toFixed(3)}}</td>
                <td class="${{tierClass}}" style="font-weight:700">${{tierShort}}</td>
                <td>${{issuesHtml}}</td>
            `;
            tbody.appendChild(tr);
        }});

        // GSAP Animations
        gsap.to("header", {{y: 0, opacity: 1, duration: 1, ease: "power3.out"}});
        gsap.to(".card", {{
            y: 0, 
            opacity: 1, 
            duration: 0.8, 
            stagger: 0.1, 
            ease: "back.out(1.2)",
            delay: 0.3
        }});
        gsap.to(".agent-list", {{
            y: 0, 
            opacity: 1, 
            duration: 1, 
            ease: "power3.out",
            delay: 0.8
        }});
    </script>
</body>
</html>
"""
    
    out_file = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI-FARM\NEXUS-FARM-DNA\DNA\dashboard.html")
    out_file.write_text(html, encoding="utf-8")
    print(f"Interactive Dashboard HTML generated at: {out_file}")

def main():
    root = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI-FARM\NEXUS-FARM-DNA\DNA")
    evaluator = LLMEvaluator()
    reports = {}

    for domain_dir in root.glob("DNA_*"):
        if not domain_dir.is_dir():
             continue
        domain_name = domain_dir.name
        reports[domain_name] = []
        for py_file in domain_dir.glob("*.py"):
            fitness, scores, issues = evaluator.evaluate(py_file, domain_name)
            reports[domain_name].append({
                 "file": py_file.name,
                 "fitness": fitness,
                 "tier": get_tier(fitness),
                 "issues": issues,
                 "scores": scores
            })
            
    generate_html(reports)

if __name__ == "__main__":
    main()
