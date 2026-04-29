import re
import json
import os

with open("extracted_docs.json", "r", encoding="utf-8") as f:
    docs = json.load(f)

# Read the HTML template
with open("tmp_presentation.html", "r", encoding="utf-8") as f:
    html_template = f.read()

# I will craft a single standalone HTML file for each language that does not require JS to render the content, 
# but rather has the content baked in. This makes the "document instruction" truly separate.

def generate_static_html(lang, text):
    # Parse the text into structured blocks
    # We know the text has headers like "Answering Engine\nAI-powered..."
    
    # We will just split by double newlines or similar, but since we parsed it with single newlines..
    lines = text.split('\n')
    
    sections = []
    current_section = {"title": "Introduction", "content": []}
    
    for line in lines:
        line = line.strip()
        if not line: continue
        if line.startswith("--- Document:"): continue
        if line == "⬡ NEXUS OS": continue
        
        # Heuristic for Titles vs Text
        if len(line) < 40 and not line.endswith('.') and not line.endswith(':'):
            # It's likely a title/header
            if current_section["content"]:
                sections.append(current_section)
                current_section = {"title": line, "content": []}
            else:
                current_section["title"] += " - " + line
        else:
            current_section["content"].append(line)
            
    if current_section["content"]:
        sections.append(current_section)

    head = html_template.split("<nav")[0]
    
    # We'll replace the dynamic parts and inject static content
    html = head
    html += '''
<style>
/* Adjustments for static document */
body { overflow-y: auto; }
.hero { min-height: 50vh; padding: 100px 40px 40px; }
.hero h1 { font-size: 4rem; }
.instruction-section { padding: 40px; max-width: 1000px; margin: 0 auto; }
.instruction-card { background: var(--sf); border: 1px solid var(--bd); padding: 30px; margin-bottom: 20px; border-radius: 8px; }
.instruction-card h3 { color: var(--ac); font-family: 'JetBrains Mono', monospace; font-size: 1.4rem; margin-bottom: 10px; }
.instruction-card p { font-size: 1.1rem; line-height: 1.6; color: var(--tx2); margin-bottom: 10px; }
</style>
</head>
<body>
    <div class="noise"></div>
    <section class="hero">
        <div class="hero-grid"></div>
        <div class="hero-glow"></div>
        <div class="hero-c">
            <div class="hero-tag">NEXUS OPERATIONAL MANUAL</div>
            <h1>NEXUS <span>INSTRUCTION</span></h1>
            <p class="hero-sub">Language: ''' + lang.upper() + '''</p>
        </div>
    </section>
    
    <div class="instruction-section">
'''
    for sec in sections:
        html += '<div class="instruction-card">'
        html += f'<h3>{sec["title"]}</h3>'
        for p in sec["content"]:
            html += f'<p>{p}</p>'
        html += '</div>'
        
    html += '''
    </div>
</body>
</html>
'''
    return html

os.makedirs("INBOX/WEB", exist_ok=True)

for lang in ["en", "ru", "ua"]:
    text = docs[lang]
    html = generate_static_html(lang, text)
    with open(f"INBOX/WEB/instruction_{lang}.html", "w", encoding="utf-8") as f:
        f.write(html)
        
print("Generated static HTML instructions.")
