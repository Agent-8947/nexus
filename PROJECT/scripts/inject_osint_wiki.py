import json
import os

# Updated translations JS (first we read it)
with open('PROJECT/outputs/WEB_UPDATE/nexus_translations.js', 'r', encoding='utf-8') as f:
    text = f.read().replace('const T = ', '').replace(';', '')
    T = json.loads(text)

# New items
new_agents = {
    'en': [
        {"b": "OSINT Core", "h": "Entity Profiling Engine", "p": "Autonomous OSINT reconnaissance pipeline. Hardened entity profiling combining Maigret, Holehe, Ignorant, and CloudEnum with strict timeouts."},
        {"b": "Cognitive", "h": "Knowledge Wiki Engine", "p": "Cognitive Master dashboard sync. Automates real-time synchronization between wiki_engine.py and the Wiki interface, reflecting article metrics and health."},
        {"b": "Security", "h": "Legal-DevOps OSINT", "p": "Deep multi-layered identity verification. Cross-references academic, business, and legal registries to resolve collisions and map real-world infrastructure."},
        {"b": "Research", "h": "Academic Bridge", "p": "Intelligence enrichment via institutional knowledge. Integrates MIT, Oxford, arXiv, and Semantic Scholar for rigorous scientific validation and critique."}
    ],
    'ru': [
        {"b": "OSINT Ядро", "h": "Entity Profiling Engine", "p": "Автономный конвейер OSINT-разведки. Профилирование через Maigret, Holehe, Ignorant и CloudEnum с жесткими таймаутами и обработкой ошибок."},
        {"b": "Когнитивность", "h": "Knowledge Wiki Engine", "p": "Ядро базы знаний Cognitive Master. Автоматизирует синхронизацию wiki_engine.py и дашборда для отображения состояния статей м метрик в реальном времени."},
        {"b": "Безопасность", "h": "Legal-DevOps OSINT", "p": "Многоуровневая верификация личности. Анализ академических, деловых и юридических реестров для разрешения коллизий и маппинга инфраструктуры."},
        {"b": "Исследования", "h": "Academic Bridge", "p": "Интеллектуальное обогащение данных. Интеграция с MIT, Oxford, arXiv и Semantic Scholar для научного анализа и строгой валидации OSINT-отчетов."}
    ],
    'ua': [
        {"b": "OSINT Ядро", "h": "Entity Profiling Engine", "p": "Автономний конвеєр OSINT-розвідки. Профілювання сутностей через Maigret, Holehe, Ignorant та CloudEnum з жорсткими таймаутами і обробкою помилок."},
        {"b": "Когнітивність", "h": "Knowledge Wiki Engine", "p": "Ядро бази знань Cognitive Master. Автоматизує синхронізацію wiki_engine.py та дашборда, відображаючи стан статей і метрики в реальному часі."},
        {"b": "Безпека", "h": "Legal-DevOps OSINT", "p": "Багаторівнева верифікація особистості. Аналіз академічних, ділових та юридичних реєстрів для запобігання колізіям і маппінгу інфраструктури."},
        {"b": "Дослідження", "h": "Academic Bridge", "p": "Інтелектуальне збагачення даних. Інтеграція з MIT, Oxford, arXiv та Semantic Scholar для наукового аналізу та строгої валідації OSINT-звітів."}
    ]
}

# Append new agents and update count
for lang in ['en', 'ru', 'ua']:
    # Ensure they aren't duplicate
    existing_titles = [x.get('h','') for x in T[lang].get('ag', [])]
    for n in new_agents[lang]:
        if n['h'] not in existing_titles:
            T[lang]['ag'].append(n)
    
    T[lang]['s3'] = str(len(T[lang]['ag']))

# Write back
with open('PROJECT/outputs/WEB_UPDATE/nexus_translations.js', 'w', encoding='utf-8') as f:
    f.write('const T = ' + json.dumps(T, ensure_ascii=False, indent=4) + ';')

print("Injected new OSINT and Wiki blocks successfully.")
