import os
import json

def generate_dashboard():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    memory_path = os.path.join(script_dir, "..", "..", "memory.json")
    if not os.path.exists(memory_path):
        print("Error: memory.json not found")
        return

    with open(memory_path, 'r') as f:
        data = json.load(f)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NEXUS Dashboard</title>
        <style>
            :root {{
                --bg: #0a0a0c;
                --panel: #16161a;
                --accent: #00f2ff;
                --text: #e0e0e0;
            }}
            body {{
                background: var(--bg);
                color: var(--text);
                font-family: 'Inter', sans-serif;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}
            .card {{
                background: var(--panel);
                padding: 2rem;
                border-radius: 12px;
                border: 1px solid var(--accent);
                box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
                text-align: center;
            }}
            h1 {{ color: var(--accent); }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>NEXUS Dashboard</h1>
            <p>Project: {data.get('project_name')}</p>
            <p>Status: {data.get('status')}</p>
            <div style="background: rgba(0, 242, 255, 0.1); padding: 10px; border-radius: 5px;">
                Ready for /start
            </div>
        </div>
    </body>
    </html>
    """
    with open("../../dashboard.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Dashboard generated successfully: dashboard.html")

if __name__ == "__main__":
    generate_dashboard()
