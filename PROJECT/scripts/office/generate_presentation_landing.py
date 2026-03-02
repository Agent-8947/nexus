import os
import json
from datetime import datetime

class NexusLandingGenerator:
    def __init__(self, project_root):
        self.project_root = project_root
        self.template_path = os.path.join(project_root, "PROJECT", "templates", "landing_template.html")
        self.output_path = os.path.join(project_root, "PROJECT", "outputs", "NEXUS_PRESENTATION.html")
        self.memory_path = os.path.join(project_root, "PROJECT", "memory.json")

    def load_stack(self):
        with open(self.memory_path, 'r', encoding='utf-8') as f:
            return json.load(f).get('stack', {})

    def generate(self):
        stack = self.load_stack()
        
        # Данные для лендинга на основе нашей новой карты стеков
        context = {
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "frontend_logic": f"{stack['frontend']['static']} + {stack['frontend']['islands']}",
            "backend_logic": f"{stack['backend']['main']} + {stack['backend']['edge']}",
            "ai_logic": f"{stack['ai_automation']['llm']} + {stack['ai_automation']['agents']}",
            "db_logic": f"{stack['database']['main']} / {stack['database']['local']}",
            "devops_logic": stack['devops']['deployment'],
            "desktop_logic": stack['desktop']['cli']
        }

        with open(self.template_path, 'r', encoding='utf-8') as f:
            html = f.read()

        # Обновляем контент лендинга под новую историю
        html = html.replace('THE SPEED OF <br />', 'AI-ORCHESTRATED <br />')
        html = html.replace('PURE LOGIC.', 'NEXUS SYSTEM 2026.')
        html = html.replace('Redefining high-performance messaging', 'Fully integrated 6-direction development stack')
        html = html.replace('104k msg/s throughput.', 'S-Tier 2025 Standard Compliance.')
        
        # Вставляем динамические данные в секцию статистики или другие части
        # Для простоты, мы просто перезапишем файл целиком с актуальными данными
        
        # Интегрируем описание 6 направлений
        directions_html = f"""
        <section id="stack-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-40">
            <div class="glass-card p-8 rounded-2xl border-l-4 border-sky-500">
                <h4 class="text-sky-400 font-bold mb-2">🎨 FRONTEND</h4>
                <p class="text-xs text-slate-400 mb-4">{context['frontend_logic']}</p>
                <div class="text-[10px] mono text-slate-500 uppercase tracking-widest">Astro v5 + Svelte Islands</div>
            </div>
            <div class="glass-card p-8 rounded-2xl border-l-4 border-emerald-500">
                <h4 class="text-emerald-400 font-bold mb-2">⚙️ BACKEND</h4>
                <p class="text-xs text-slate-400 mb-4">{context['backend_logic']}</p>
                <div class="text-[10px] mono text-slate-500 uppercase tracking-widest">FastAPI + Hono Edge</div>
            </div>
            <div class="glass-card p-8 rounded-2xl border-l-4 border-purple-500">
                <h4 class="text-purple-400 font-bold mb-2">🤖 AI / AUTO</h4>
                <p class="text-xs text-slate-400 mb-4">{context['ai_logic']}</p>
                <div class="text-[10px] mono text-slate-500 uppercase tracking-widest">Claude 3.5 + LangGraph</div>
            </div>
            <div class="glass-card p-8 rounded-2xl border-l-4 border-amber-500">
                <h4 class="text-amber-400 font-bold mb-2">🗄 DATABASE</h4>
                <p class="text-xs text-slate-400 mb-4">{context['db_logic']}</p>
                <div class="text-[10px] mono text-slate-500 uppercase tracking-widest">Supabase + SQLite Local</div>
            </div>
            <div class="glass-card p-8 rounded-2xl border-l-4 border-blue-500">
                <h4 class="text-blue-400 font-bold mb-2">🚀 DEVOPS</h4>
                <p class="text-xs text-slate-400 mb-4">{context['devops_logic']}</p>
                <div class="text-[10px] mono text-slate-500 uppercase tracking-widest">Vercel / Railway / Cloudflare</div>
            </div>
            <div class="glass-card p-8 rounded-2xl border-l-4 border-red-500">
                <h4 class="text-red-400 font-bold mb-2">🖥 DESKTOP</h4>
                <p class="text-xs text-slate-400 mb-4">{context['desktop_logic']}</p>
                <div class="text-[10px] mono text-slate-500 uppercase tracking-widest">Tauri + Python FS Access</div>
            </div>
        </section>
        """
        
        # Вставляем перед Command Control Section
        html = html.replace('<section id="terminal" class="mb-40">', directions_html + '<section id="terminal" class="mb-40">')
        
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(html)
            
        print(f"[*] NEXUS Presentation Landing generated: {self.output_path}")

if __name__ == "__main__":
    PROJECT_ROOT = r"e:\Downloads\--ANTIGRAVITY store\IDE-optimus"
    generator = NexusLandingGenerator(PROJECT_ROOT)
    generator.generate()
