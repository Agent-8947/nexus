import os
import json
import re
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import threading

# ─── CONFIG ───────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS")
WIKI_ROOT   = PROJECT_ROOT / "PROJECT" / "WIKI"
STATE_FILE  = WIKI_ROOT / "nexus_farm_state.json"
DASHBOARD_FILE = PROJECT_ROOT / "FARM_STATUS.html"
PORT = 8844

# ─── LOGIC ────────────────────────────────────────────────────────────────────
def get_farming_data():
    if not STATE_FILE.exists():
        return {"error": "No state file found"}

    state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    processed = state.get("processed", [])
    
    all_repos = [d for d in WIKI_ROOT.iterdir() if d.is_dir() and not d.name.startswith("__")]
    total_count = len(all_repos)
    processed_count = len(processed)
    progress = round((processed_count / total_count) * 100, 1) if total_count > 0 else 0

    analyses = []
    # Scan last 200 for details to keep response fast
    for repo_name in processed[-200:]:
        analysis_path = WIKI_ROOT / repo_name / "NEXUS_ANALYSIS.md"
        if analysis_path.exists():
            content = analysis_path.read_text(encoding="utf-8")
            domain = "OTHER"
            score = 0
            summary = "No summary found."
            
            d_match = re.search(r"Domain\*\* \| `(.*?)` \|", content)
            s_match = re.search(r"NEXUS Value\*\* \| .* (\d+)/10 \|", content)
            sum_match = re.search(r"## Summary\n(.*?)\n", content, re.DOTALL)
            
            if d_match: domain = d_match.group(1)
            if s_match: score = int(s_match.group(1))
            if sum_match: summary = sum_match.group(1).strip()
            
            analyses.append({
                "name": repo_name,
                "domain": domain,
                "score": score,
                "summary": summary
            })

    top_repos = sorted(analyses, key=lambda x: x['score'], reverse=True)[:5]
    
    return {
        "progress": progress,
        "processed_count": processed_count,
        "total_count": total_count,
        "recent": analyses[-10:],
        "top": top_repos,
        "all_processed": analyses[::-1],
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }

class NexusAPIHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            if DASHBOARD_FILE.exists():
                self.wfile.write(DASHBOARD_FILE.read_bytes())
            else:
                self.wfile.write(b"<h1>Error: DASHBOARD_FILE not found</h1>")
        elif self.path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            data = get_farming_data()
            self.wfile.write(json.dumps(data).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return # Silent log

def run_server():
    server = HTTPServer(('localhost', PORT), NexusAPIHandler)
    print(f"[*] NEXUS Live API started on http://localhost:{PORT}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
