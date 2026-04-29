import json
import os

# Read the translations
with open('PROJECT/outputs/WEB_UPDATE/nexus_translations.js', 'r', encoding='utf-8') as f:
    text = f.read().replace('const T = ', '').replace(';', '')
    T = json.loads(text)

# We must PURGE all RAG/Neo4j hallucinations.
# We will use the Karpathy / TheLivingWiki terminology.

system_desc = {
    'en': "Autonomous knowledge system. Flat .md architecture. SHA-256 deduplication. Closed compound loops. Pure Python portability. Android/Windows/Linux native.",
    'ru': "Автономная система знаний. Архитектура на плоских .md файлах. SHA-256 дедупликация. Замкнутые циклы компаундов (Compound Loops). Чистый Python.",
    'ua': "Автономна система знань. Архітектура на плоских .md файлах. SHA-256 дедуплікація. Замкнуті цикли компаундів (Compound Loops). Чистий Python."
}

for lang in ['en', 'ru', 'ua']:
    # Fix the description cards to reflect REAL architecture
    T[lang]['a2h'] = "TheLivingWiki Dashboard"
    T[lang]['a2p'] = "Real-time synchronization with wiki_engine.py. Autonomous knowledge compounding on flat .md files. Zero dependencies."
    T[lang]['a2t'] = "v5.9 [KARPATHY-STEER]"
    
    T[lang]['a3h'] = "Compound Intelligence"
    T[lang]['a3p'] = "Closing the loop: Inbox -> SHA-256 -> Keyword Classification -> WIKI/compounds/. Grep-based search, 100% debuggable logic."
    T[lang]['a3t'] = "CODIFIED CONTEXT"
    
    # Update stats to show real system stats
    T[lang]['s2'] = "22 Connectors" # MCP
    T[lang]['s2h'] = "Neural Net Hands"
    T[lang]['s3'] = "25 Skills" # Fleet
    T[lang]['s3h'] = "AI Orchestration"

# Write back updated translations JS
with open('PROJECT/outputs/WEB_UPDATE/nexus_translations.js', 'w', encoding='utf-8') as f:
    f.write('const T = ' + json.dumps(T, ensure_ascii=False, indent=4) + ';')

print("Purged RAG hallucinations and injected real Karpathy-protocol content.")
