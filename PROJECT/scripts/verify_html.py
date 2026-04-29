import json

with open('PROJECT/outputs/WEB_UPDATE/nexus_translations.js', 'r', encoding='utf-8') as f:
    text = f.read()
    
# extract JSON
text = text.replace('const T = ', '').replace(';', '')
data = json.loads(text)

ru_d = data['ru']
print(f"Agents: {len(ru_d['ag'])}")
print(f"MCP: {len(ru_d['mcp'])}")
