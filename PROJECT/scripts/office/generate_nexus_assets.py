import os
import sys

# Import existing generation scripts
try:
    from generate_doc import create_premium_report
except ImportError:
    pass

try:
    from generate_pdf_ultra import create_ultra_pdf
except ImportError:
    pass

OUTPUT_DIR = r'e:\Downloads\--ANTIGRAVITY store\IDE-optimus\PROJECT\outputs'

def create_dashboard_html():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, 'Architecture_Dashboard.html')
    
    html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXUS | ARCHITECTURAL MONOLITH</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@100;300;400;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        :root { --gold: #D4AF37; --bg: #050505; --accent: #1E293B; }
        body { font-family: 'Outfit', sans-serif; background-color: var(--bg); color: #E2E8F0; -webkit-font-smoothing: antialiased; }
        .serif { font-family: 'Playfair Display', serif; }
        .glass { background: rgba(15, 15, 15, 0.8); backdrop-filter: blur(25px); border: 1px solid rgba(255, 255, 255, 0.03); }
        .gold-border { position: relative; }
        .gold-border::after { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 1px; background: linear-gradient(90deg, transparent, var(--gold), transparent); opacity: 0.3; }
        .noise { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: url('https://grainy-gradients.vercel.app/noise.svg'); opacity: 0.05; pointer-events: none; z-index: 100; }
        @keyframes subtleFloat { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
        .float { animation: subtleFloat 8s ease-in-out infinite; }
        .reveal { animation: reveal 1.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; opacity: 0; }
        @keyframes reveal { from { transform: translateY(30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
    </style>
</head>
<body class="overflow-x-hidden">
    <div class="noise"></div>

    <!-- MAIN NAV -->
    <nav class="fixed top-0 w-full z-50 px-10 py-6 flex justify-between items-center glass border-b border-white/5">
        <div class="text-2xl font-light tracking-[0.3em] uppercase">Nexus <span class="font-bold text-slate-500">Architecture</span></div>
        <div class="flex gap-10 text-[10px] uppercase tracking-[0.2em] text-slate-400">
            <a href="#" class="hover:text-white transition-colors">ADR-Log</a>
            <a href="#" class="hover:text-white transition-colors">Stack-Metrics</a>
            <a href="#" class="hover:text-white transition-colors">Roadmap</a>
            <div class="flex items-center gap-2">
                <div class="w-1.5 h-1.5 bg-emerald-500 rounded-full shadow-[0_0_10px_#10b981]"></div>
                <span class="text-emerald-500">Live</span>
            </div>
        </div>
    </nav>

    <main class="pt-40 px-10 pb-20 max-w-screen-2xl mx-auto">
        
        <!-- HERO SECTION -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-20 items-center mb-40">
            <div class="reveal">
                <h2 class="serif italic text-3xl text-slate-500 mb-4">Engineering the future of messaging</h2>
                <h1 class="text-7xl lg:text-9xl font-bold tracking-tighter leading-none mb-10">THE <span class="text-white">MONOLITH</span> KERNEL.</h1>
                <p class="text-xl text-slate-400 max-w-xl font-light leading-relaxed mb-12">
                    A high-performance infrastructure designed for the Windows-Lite environment. 
                    Targeting sub-millisecond latency with a custom Rust engine and Python-integrated logic.
                </p>
                <div class="flex gap-4">
                    <button class="px-8 py-4 bg-white text-black font-bold uppercase tracking-widest text-xs hover:bg-slate-200 transition-all">Download PDF</button>
                    <button class="px-8 py-4 border border-white/20 uppercase tracking-widest text-xs hover:bg-white/5 transition-all">Technical ADR</button>
                </div>
            </div>
            <div class="reveal relative" style="animation-delay: 0.3s">
                <div class="absolute -inset-20 bg-emerald-500/10 rounded-full blur-[120px]"></div>
                <img src="C:\\Users\\MAC\\.gemini\\antigravity\\brain\\858d0bd1-44f8-418a-847c-07d05808974d\\nexus_monolith_concept_1772197577106.png" class="w-full h-auto rounded-3xl shadow-2xl float opacity-90 grayscale hover:grayscale-0 transition-all duration-1000" alt="Nexus Monolith">
            </div>
        </div>

        <!-- SPECS GRID -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-40 lg:-mt-20 z-20 relative">
            <div class="glass p-10 rounded-3xl reveal" style="animation-delay: 0.5s">
                <span class="text-[10px] uppercase tracking-[0.3em] text-slate-500 block mb-6">Messaging Throughput</span>
                <div class="text-6xl font-bold mb-4">100k <span class="text-sm font-light text-slate-500">msg/s</span></div>
                <div class="h-1 w-20 bg-emerald-500/50"></div>
            </div>
            <div class="glass p-10 rounded-3xl reveal" style="animation-delay: 0.6s">
                <span class="text-[10px] uppercase tracking-[0.3em] text-slate-500 block mb-6">Target Latency</span>
                <div class="text-6xl font-bold mb-4">&lt; 0.1 <span class="text-sm font-light text-slate-500">ms</span></div>
                <div class="h-1 w-20 bg-sky-500/50"></div>
            </div>
            <div class="glass p-10 rounded-3xl reveal" style="animation-delay: 0.7s">
                <span class="text-[10px] uppercase tracking-[0.3em] text-slate-500 block mb-6">Memory Footprint</span>
                <div class="text-6xl font-bold mb-4">6 <span class="text-sm font-light text-slate-500">GB RAM</span></div>
                <div class="h-1 w-20 bg-rose-500/50"></div>
            </div>
        </div>

        <!-- TECH MATRIX -->
        <div class="reveal" style="animation-delay: 0.8s">
            <div class="flex items-center justify-between mb-12">
                <h2 class="serif italic text-4xl">Technology Matrix</h2>
                <div class="text-[10px] uppercase tracking-widest text-slate-500 italic">Curated Bayesian Selection</div>
            </div>
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-10">
                <div class="lg:col-span-8 overflow-hidden rounded-3xl glass">
                    <table class="w-full text-left">
                        <thead class="bg-white/5">
                            <tr class="text-[10px] uppercase tracking-widest text-slate-500">
                                <th class="p-8 font-normal">Component</th>
                                <th class="p-8 font-normal">Selection</th>
                                <th class="p-8 font-normal">Rationale</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-white/5">
                            <tr class="hover:bg-white/[0.02] transition-colors">
                                <td class="p-8 font-bold">Processor</td>
                                <td class="p-8 text-white">Rust (Tokio)</td>
                                <td class="p-8 text-sm font-light text-slate-400">Zero-GC, Direct memory safety.</td>
                            </tr>
                            <tr class="hover:bg-white/[0.02] transition-colors">
                                <td class="p-8 font-bold">Logic Engine</td>
                                <td class="p-8 text-white">Python 3.13</td>
                                <td class="p-8 text-sm font-light text-slate-400">Rapid iteration & AI integration.</td>
                            </tr>
                            <tr class="hover:bg-white/[0.02] transition-colors">
                                <td class="p-8 font-bold">Registry</td>
                                <td class="p-8 text-white">Go / PocketBase</td>
                                <td class="p-8 text-sm font-light text-slate-400">Ultra-light orchestration.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="lg:col-span-4 glass p-10 rounded-3xl flex flex-col justify-between">
                    <h3 class="text-xs uppercase tracking-widest text-slate-500 mb-10">Real-time Load Simulation</h3>
                    <canvas id="loadChart" height="200"></canvas>
                    <div class="mt-10 pt-10 border-t border-white/5">
                        <p class="text-xs text-slate-400 italic">"Simplicity is the ultimate sophistication."</p>
                    </div>
                </div>
            </div>
        </div>

    </main>

    <footer class="p-20 border-t border-white/5 glass text-center">
        <div class="text-5xl font-bold tracking-tighter mb-6">NEXUS PRIME.</div>
        <div class="text-[10px] uppercase tracking-[0.5em] text-slate-500">Infinite Intelligence // 2026</div>
    </footer>

    <script>
        const ctx = document.getElementById('loadChart').getContext('2d');
        const loadChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: Array(30).fill(''),
                datasets: [{
                    data: Array(30).fill(0).map(() => Math.random() * 20 + 70),
                    borderColor: '#ffffff',
                    borderWidth: 1,
                    pointRadius: 0,
                    fill: true,
                    backgroundColor: 'rgba(255,255,255,0.02)',
                    tension: 0.5
                }]
            },
            options: {
                plugins: { legend: { display: false } },
                scales: { 
                    x: { display: false },
                    y: { 
                        display: false,
                        min: 0, max: 100 
                    }
                }
            }
        });
        setInterval(() => {
            loadChart.data.datasets[0].data.shift();
            loadChart.data.datasets[0].data.push(Math.random() * 10 + 80);
            loadChart.update('none');
        }, 1000);
    </script>
</body>
</html>
"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"LUXURY_DASHBOARD_GENERATED: {path}")

def generate_nexus_assets():
    print("--- INITIATING OMNI-REPORTER SEQUENCE ---")
    
    # Generate HTML
    try:
        create_dashboard_html()
    except Exception as e:
        print(f"ERROR: Failed to generate dashboard HTML - {e}")
        
    # Generate DOCX
    try:
        if 'create_premium_report' in globals():
            create_premium_report()
        else:
            print("WARNING: DOCX generator (generate_doc.py) not found.")
    except Exception as e:
        print(f"ERROR: Failed to generate DOCX - {e}")

    # Generate PDF
    try:
        if 'create_ultra_pdf' in globals():
            create_ultra_pdf()
        else:
            print("WARNING: PDF generator (generate_pdf_ultra.py) not found.")
    except Exception as e:
        print(f"ERROR: Failed to generate PDF - {e}")
        
    print("--- OMNI-REPORTER SEQUENCE COMPLETED ---")

if __name__ == "__main__":
    generate_nexus_assets()
