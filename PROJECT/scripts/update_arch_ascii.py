import json
import os
import re

# 1. Update ASCII in tmp_presentation.html
with open('tmp_presentation.html', 'r', encoding='utf-8') as f:
    html = f.read()

OLD_ARCH = re.search(r'<pre>.*?</pre>', html, re.DOTALL).group(0)

NEW_ARCH = """<pre>                                  +-----------------------------+
                                  |     NEXUS CONSTITUTION      |
                                  |   (Prime Laws & Context)    |
                                  +--------------+--------------+
                                                 |
                                                 v
         +-----------------------+    +-----------------------+    +-----------------------+
         | WIKI DASHBOARD [v5.8] |    |  NEXUS ORCHESTRATOR   |    |   OSINT ENGINE [v3]   |
         | (Astro / wiki_engine) | &lt;-&gt;|   (Polymorphic AI)    | &lt;-&gt;| (Maigret / CloudEnum) |
         +-----------+-----------+    +-----------+-----------+    +-----------+-----------+
                     |                            |                            |
                     v                            v                            v
         +-----------------------+    +-----------------------+    +-----------------------+
         |   COGNITIVE MEMORY    |    |     SENTINEL DAG      |    |    ACADEMIC BRIDGE    |
         |  (Neo4j / pgvector)   |    | (Airflow / Security)  |    |  (arXiv / Semantic)   |
         +-----------+-----------+    +-----------+-----------+    +-----------+-----------+
                     |                            |                            |
                     +----------------------------+----------------------------+
                                                  |
                                                  v
                                  +-----------------------------+
                                  |    LEGAL-DEVOPS DATABASE    |
                                  |  (Supabase / Entity Intel)  |
                                  +-----------------------------+</pre>"""

html = html.replace(OLD_ARCH, NEW_ARCH)
with open('tmp_presentation.html', 'w', encoding='utf-8') as f:
    f.write(html)


# 2. Update descriptive cards in nexus_translations.js
with open('PROJECT/outputs/WEB_UPDATE/nexus_translations.js', 'r', encoding='utf-8') as f:
    text = f.read().replace('const T = ', '').replace(';', '')
    T = json.loads(text)

T['en']['a2b'] = "Presentation"
T['en']['a2h'] = "Hardened Wiki Dashboard"
T['en']['a2p'] = "Next-gen frontend integration using Astro v5. Directly synchronizes with wiki_engine.py for real-time Cognitive Master status."
T['en']['a2t'] = "v5.8 ACTIVE"

T['en']['a3b'] = "Intelligence"
T['en']['a3h'] = "OSINT & Cognitive Core"
T['en']['a3p'] = "RAG integration via pgvector and Neo4j graph relationships. Unified entity tracking through Sentinel DAG and Custom OSINT pipeline."
T['en']['a3t'] = "Advanced Recursion"

T['ru']['a2b'] = "Представление"
T['ru']['a2h'] = "Hardened Wiki Dashboard"
T['ru']['a2p'] = "Интеграция фронтенда следующего поколения на Astro v5. Прямая синхронизация с wiki_engine.py для вывода статуса Cognitive Master."
T['ru']['a2t'] = "v5.8 ACTIVE"

T['ru']['a3b'] = "Интеллект"
T['ru']['a3h'] = "OSINT и Когнитивное Ядро"
T['ru']['a3p'] = "RAG-интеграция через pgvector и графовые связи Neo4j. Унифицированный трекинг сущностей через Sentinel DAG и OSINT конвейер."
T['ru']['a3t'] = "Продвинутая рекурсия"

T['ua']['a2b'] = "Представлення"
T['ua']['a2h'] = "Hardened Wiki Dashboard"
T['ua']['a2p'] = "Інтеграція фронтенду наступного покоління на Astro v5. Пряма синхронізація з wiki_engine.py для виведення статусу Cognitive Master."
T['ua']['a2t'] = "v5.8 ACTIVE"

T['ua']['a3b'] = "Інтелект"
T['ua']['a3h'] = "OSINT та Когнітивне Ядро"
T['ua']['a3p'] = "RAG-інтеграція через pgvector і графові зв'язки Neo4j. Уніфікований трекінг сутностей через Sentinel DAG і OSINT конвеєр."
T['ua']['a3t'] = "Просунута рекурсія"

with open('PROJECT/outputs/WEB_UPDATE/nexus_translations.js', 'w', encoding='utf-8') as f:
    f.write('const T = ' + json.dumps(T, ensure_ascii=False, indent=4) + ';')

print("ASCII Architecture and Cards successfully modernized!")
