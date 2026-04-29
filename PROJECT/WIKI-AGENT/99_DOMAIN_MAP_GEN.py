import os
import re
from pathlib import Path
import json

WIKI_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI")

def parse_analysis(file_path):
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None
    
    # Extract Domain
    domain_match = re.search(r"\| \*\*Domain\*\* \| `(.*)` \|", content)
    domain = domain_match.group(1).strip() if domain_match else "OTHER"
    
    # Extract Score
    score_match = re.search(r"\| \*\*NEXUS Value\*\* \| .* (\d+)/10 \|", content)
    score = int(score_match.group(1)) if score_match else 5
    
    # Extract Technologies
    techs = []
    # Key Technologies section extraction
    parts = content.split("## Key Technologies")
    if len(parts) > 1:
        tech_chunk = parts[1].split("##")[0].strip()
        tech_lines = tech_chunk.split("\n")
        for line in tech_lines:
            m = re.search(r"- `(.*)`", line)
            if m:
                techs.append(m.group(1).strip())
    
    return {
        "repo": file_path.parent.name,
        "domain": domain,
        "score": score,
        "techs": techs
    }

def generate_map():
    data = []
    for analysis_file in WIKI_ROOT.glob("*/NEXUS_ANALYSIS.md"):
        item = parse_analysis(analysis_file)
        if item:
            data.append(item)
            
    # Group by Domain
    domains = {}
    for item in data:
        d = item["domain"]
        if d not in domains:
            domains[d] = {"count": 0, "avg_score": 0, "tech_stack": set(), "top_repos": []}
        
        domains[d]["count"] += 1
        domains[d]["avg_score"] += item["score"]
        domains[d]["tech_stack"].update(item["techs"])
        domains[d]["top_repos"].append((item["repo"], item["score"]))
        
    for d in domains:
        if domains[d]["count"] > 0:
            domains[d]["avg_score"] /= domains[d]["count"]
        domains[d]["tech_stack"] = sorted(list(domains[d]["tech_stack"]))
        domains[d]["top_repos"] = [r[0] for r in sorted(domains[d]["top_repos"], key=lambda x: x[1], reverse=True)[:5]]

    # Descriptions for domains
    descriptions = {
        "AI": "Искусственный интеллект, LLM, нейросети и машинное обучение. Фундамент для принятия решений в NEXUS.",
        "OSINT": "Сведения из открытых источников, разведка, парсинг данных и анализ цифровых следов.",
        "ROBOTICS": "Автономные системы, управление манипуляторами и сенсорная обработка.",
        "SECURITY": "Информационная безопасность, аудит кода, поиск уязвимостей и защита систем.",
        "UAV": "Беспилотные летательные аппараты, навигация, управление роями и аэродинамика.",
        "CRYPTO": "Криптография, блокчейн, смарт-контракты и приватность данных.",
        "LEGAL": "Юридические технологии, анализ контрактов, нормативная база и комплаенс.",
        "SYSTEMS": "Низкоуровневое ПО, операционные системы, драйверы и архитектура железа.",
        "MATH": "Математическое моделирование, алгоритмы оптимизации и численные методы.",
        "DATA": "Хранение, обработка и визуализация больших данных.",
        "WEB": "Веб-интерфейсы, дашборды, API и сетевые протоколы.",
        "OTHER": "Прочие инструменты, библиотеки общего назначения и вспомогательные скрипты."
    }

    # Cross-tech mapping (tech - domains)
    tech_map = {}
    for item in data:
        for t in item["techs"]:
            if t not in tech_map:
                tech_map[t] = set()
            tech_map[t].add(item["domain"])
            
    cross_links = {t: list(ds) for t, ds in tech_map.items() if len(ds) > 1}

    report = {
        "domains": domains,
        "descriptions": descriptions,
        "cross_links": cross_links,
        "total_processed": len(data)
    }
    
    output_path = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\domain_map.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"Map generated: {output_path}")

if __name__ == "__main__":
    generate_map()
