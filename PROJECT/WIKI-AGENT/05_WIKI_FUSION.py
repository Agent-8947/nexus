"""
NEXUS Wiki Intelligence Fusion Agent v1.0
==========================================
Превращает 1442 ноды Wiki-библиотеки в операционный интеллект.

Вход:  Текстовый запрос (миссия / задача / кейс)
Выход: Markdown-брифинг с цепочкой инструментов, обоснованием и рисками.

Архитектура:
  Query -> Domain Mapper -> Cross-Domain Matcher -> Ranker -> Chain Builder -> Report

Зависимости: Только stdlib Python 3.10+
Данные:      PROJECT/WIKI/nexus_global_brain.json
Выход:       PROJECT/BRIEFINGS/<timestamp>_<slug>.md
"""

import json
import re
import sys
import os
from pathlib import Path
from datetime import datetime
from collections import Counter


# ============================================================
# PATHS
# ============================================================
PROJECT_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS")
BRAIN_PATH = PROJECT_ROOT / "PROJECT" / "WIKI" / "nexus_global_brain.json"
BRIEFINGS_DIR = PROJECT_ROOT / "PROJECT" / "BRIEFINGS"
BRIEFINGS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# DOMAIN KEYWORD MAP
# Маппинг естественного языка -> внутренние домены nexus_global_brain
# ============================================================
DOMAIN_KEYWORDS = {
    "OSINT": [
        "разведка", "osint", "reconnaissance", "recon", "расследование",
        "investigation", "digital forensics", "цифровой след", "слежка",
        "surveillance", "profiling", "профайлинг", "intelligence",
        "интеллект", "сбор данных", "scraping", "скрапинг", "crawler",
        "spider", "dorking", "shodan", "maltego", "spiderfoot",
        "maigret", "holehe", "социальные сети", "social media",
        "domain", "whois", "dns", "subdomain", "email", "leak",
        "утечка", "breach", "dark web", "darknet", "tor"
    ],
    "LEGAL": [
        "legal", "юридический", "комплаенс", "compliance", "лицензия",
        "license", "договор", "contract", "суд", "court", "закон",
        "law", "regulation", "регулирование", "аудит", "audit",
        "gdpr", "privacy", "конфиденциальность", "нарушение",
        "violation", "штраф", "penalty", "иск", "lawsuit",
        "арбитраж", "arbitration", "нотариус", "notary",
        "реестр", "registry", "компания", "company", "фирма",
        "firm", "директор", "director", "учредитель", "founder"
    ],
    "MACHINE_LEARNING": [
        "ml", "machine learning", "нейросеть", "neural", "deep learning",
        "обучение", "training", "модель", "model", "transformer",
        "llm", "gpt", "bert", "classification", "классификация",
        "prediction", "предсказание", "regression", "регрессия",
        "clustering", "кластеризация", "nlp", "computer vision",
        "cv", "распознавание", "recognition", "detection",
        "детекция", "генерация", "generation", "embedding",
        "fine-tune", "rag", "retrieval", "inference", "quantization"
    ],
    "CRYPTO": [
        "crypto", "криптография", "encryption", "шифрование",
        "blockchain", "блокчейн", "bitcoin", "ethereum", "wallet",
        "кошелек", "хеш", "hash", "signature", "подпись",
        "certificate", "сертификат", "ssl", "tls", "vpn",
        "анонимность", "anonymity", "privacy", "defi", "smart contract",
        "смарт-контракт", "token", "nft", "decentralization"
    ],
    "FORECASTING": [
        "forecast", "прогноз", "prediction", "предсказание",
        "time series", "временной ряд", "trend", "тренд",
        "risk", "риск", "финансы", "finance", "trading",
        "трейдинг", "stock", "акции", "market", "рынок",
        "portfolio", "портфель", "anomaly", "аномалия",
        "signal", "сигнал", "statistics", "статистика"
    ],
    "PSYCHOLOGY": [
        "psychology", "психология", "sentiment", "тональность",
        "emotion", "эмоция", "behavior", "поведение", "profile",
        "профиль", "manipulation", "манипуляция", "persuasion",
        "убеждение", "cognitive", "когнитивный", "bias",
        "social engineering", "социальная инженерия"
    ],
    "INFRASTRUCTURE": [
        "infra", "инфраструктура", "devops", "docker", "kubernetes",
        "ci/cd", "pipeline", "deploy", "сервер", "server",
        "database", "база данных", "api", "microservice",
        "monitoring", "мониторинг", "logging", "automation",
        "автоматизация", "cloud", "облако", "linux", "windows"
    ]
}


# ============================================================
# CORE: FUSION ENGINE
# ============================================================
class FusionEngine:
    """Ядро Intelligence Fusion Agent."""

    def __init__(self, brain_path: Path = BRAIN_PATH):
        self.brain = self._load_brain(brain_path)
        self.total_nodes = len(self.brain)
        print(f"[FUSION] Brain loaded: {self.total_nodes} nodes")

    @staticmethod
    def _load_brain(path: Path) -> dict:
        if not path.exists():
            raise FileNotFoundError(f"Brain not found: {path}")
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    # ----------------------------------------------------------
    # Phase 1: Domain Mapping
    # ----------------------------------------------------------
    def map_query_to_domains(self, query: str) -> dict[str, float]:
        """
        Определяет релевантность каждого домена к запросу.
        Возвращает dict {domain: score 0.0-1.0}
        """
        query_lower = query.lower()
        scores = {}

        for domain, keywords in DOMAIN_KEYWORDS.items():
            hits = sum(1 for kw in keywords if kw in query_lower)
            if hits > 0:
                # Нормализуем: чем больше ключевых слов совпало, тем выше очки
                scores[domain] = min(1.0, hits / 3.0)

        # Если ни один домен не найден  fallback на INFRASTRUCTURE
        if not scores:
            scores["INFRASTRUCTURE"] = 0.3

        return scores

    # ----------------------------------------------------------
    # Phase 2: Cross-Domain Matching
    # ----------------------------------------------------------
    def find_relevant_tools(self, domain_scores: dict[str, float],
                            min_overlap: int = 1) -> list[dict]:
        """
        Ищет инструменты, чьи домены пересекаются с запрошенными.
        Возвращает список tool-записей, отсортированных по релевантности.
        """
        target_domains = set(domain_scores.keys())
        results = []

        for name, data in self.brain.items():
            tool_domains = set(data.get("domains", []))
            overlap = target_domains & tool_domains

            if len(overlap) < min_overlap:
                continue

            # Расчет рейтинга: сумма весов совпавших доменов * кол-во совпадений
            relevance = sum(domain_scores.get(d, 0) for d in overlap)
            # Бонус за мультидоменность (пересечение >2 доменов)
            if len(overlap) >= 3:
                relevance *= 1.5
            elif len(overlap) >= 2:
                relevance *= 1.2

            results.append({
                "name": name,
                "domains": list(tool_domains),
                "overlap": list(overlap),
                "overlap_count": len(overlap),
                "relevance": round(relevance, 2),
                "perspective": data.get("legal_devops_perspective", ""),
                "readiness": data.get("readiness", "UNKNOWN")
            })

        results.sort(key=lambda x: (-x["relevance"], -x["overlap_count"]))
        return results

    # ----------------------------------------------------------
    # Phase 3: Chain Builder
    # ----------------------------------------------------------
    @staticmethod
    def build_chain(tools: list[dict], max_chain: int = 7) -> list[dict]:
        """
        Строит операционную цепочку из ТОП инструментов.
        Назначает инструменты по функциональным ролям:
          Recon -> Profiling -> Analysis -> Compliance -> Protection -> Prediction -> Platform
        Каждая роль заполняется лучшим кандидатом, даже если инструменты
        имеют одинаковый первичный домен.
        """
        # Функциональные роли и какие домены их обслуживают
        ROLE_PIPELINE = [
            {"role": "Recon (Разведка)", "needs": ["OSINT"],
             "desc": "Первичный сбор данных, скрапинг, OSINT-рекогносцировка"},
            {"role": "Profiling (Профайлинг)", "needs": ["PSYCHOLOGY", "OSINT"],
             "desc": "Когнитивный анализ целей, поведенческие паттерны"},
            {"role": "Analysis (Анализ)", "needs": ["MACHINE_LEARNING"],
             "desc": "ML/NLP обработка собранных данных, классификация, детекция"},
            {"role": "Compliance (Комплаенс)", "needs": ["LEGAL"],
             "desc": "Юридическая валидация, проверка лицензий, аудит нарушений"},
            {"role": "Protection (Защита)", "needs": ["CRYPTO"],
             "desc": "Шифрование, анонимизация, безопасность передачи данных"},
            {"role": "Prediction (Прогноз)", "needs": ["FORECASTING"],
             "desc": "Прогнозирование рисков, финансовый анализ, временные ряды"},
            {"role": "Platform (Платформа)", "needs": ["INFRASTRUCTURE"],
             "desc": "Инфраструктура запуска, DevOps, API, оркестрация"},
        ]

        used_names = set()
        chain = []

        for role_spec in ROLE_PIPELINE:
            if len(chain) >= max_chain:
                break

            role_domains = set(role_spec["needs"])
            best_candidate = None

            for tool in tools:
                if tool["name"] in used_names:
                    continue

                tool_all_domains = set(tool.get("domains", []))
                # Инструмент подходит для роли, если хотя бы один его домен
                # пересекается с требуемыми доменами роли
                if role_domains & tool_all_domains:
                    best_candidate = tool
                    break  # tools уже отсортированы по relevance

            if best_candidate:
                best_candidate = dict(best_candidate)  # shallow copy
                best_candidate["role"] = role_spec["role"]
                best_candidate["role_desc"] = role_spec["desc"]
                chain.append(best_candidate)
                used_names.add(best_candidate["name"])

        return chain

    # ----------------------------------------------------------
    # Phase 4: Adversarial Review
    # ----------------------------------------------------------
    @staticmethod
    def adversarial_review(chain: list[dict]) -> list[str]:
        """Атакует собственное решение. Озвучивает слабые места."""
        risks = []

        if len(chain) < 2:
            risks.append("CRITICAL: Цепочка содержит менее 2 инструментов. "
                          "Недостаточно для полноценного анализа.")

        domains_in_chain = set()
        for tool in chain:
            domains_in_chain.update(tool["overlap"])

        if "OSINT" not in domains_in_chain:
            risks.append("WARNING: Нет OSINT-компонента. Разведка ограничена.")
        if "LEGAL" not in domains_in_chain:
            risks.append("WARNING: Нет LEGAL-компонента. Юридический комплаенс не обеспечен.")
        if "CRYPTO" not in domains_in_chain:
            risks.append("INFO: Нет CRYPTO-компонента. Данные передаются без шифрования.")

        # Проверка на зависимость от одного домена
        domain_counts = Counter(d for t in chain for d in t["overlap"])
        dominant = domain_counts.most_common(1)
        if dominant and dominant[0][1] > len(chain) * 0.7:
            risks.append(f"WARNING: Цепочка перекошена в сторону {dominant[0][0]}. "
                          f"Рекомендуется диверсификация.")

        if not risks:
            risks.append("OK: Критических рисков не обнаружено.")

        return risks

    # ----------------------------------------------------------
    # Phase 5: Report Generation
    # ----------------------------------------------------------
    def generate_briefing(self, query: str) -> Path:
        """Полный цикл: запрос -> брифинг."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        slug = re.sub(r"[^a-zA-Z0-9а-яА-ЯёЁ]+", "_", query)[:40].strip("_")

        print(f"[FUSION] Query: {query}")

        # Phase 1: Domain mapping
        domain_scores = self.map_query_to_domains(query)
        print(f"[FUSION] Domains: {domain_scores}")

        # Phase 2: Find tools
        all_tools = self.find_relevant_tools(domain_scores, min_overlap=1)
        print(f"[FUSION] Matched: {len(all_tools)} tools")

        # Phase 3: Build chain
        chain = self.build_chain(all_tools)
        print(f"[FUSION] Chain: {len(chain)} steps")

        # Phase 4: Adversarial review
        risks = self.adversarial_review(chain)

        # Phase 5: Generate report
        report_path = BRIEFINGS_DIR / f"{timestamp}_{slug}.md"
        self._write_report(report_path, query, domain_scores,
                           all_tools, chain, risks)

        print(f"[FUSION] Briefing saved: {report_path}")
        return report_path

    def _write_report(self, path: Path, query: str,
                      domain_scores: dict, all_tools: list,
                      chain: list, risks: list):
        """Записывает финальный Markdown-брифинг."""
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# NEXUS Intelligence Briefing\n\n")
            f.write(f"> Generated: {datetime.now().isoformat()}\n")
            f.write(f"> Agent: Wiki Intelligence Fusion v1.0\n")
            f.write(f"> Brain: {self.total_nodes} nodes\n\n")
            f.write(f"---\n\n")

            # Mission
            f.write(f"## Mission\n\n")
            f.write(f"```\n{query}\n```\n\n")

            # Domain Analysis
            f.write(f"## Domain Analysis\n\n")
            f.write(f"| Domain | Relevance |\n")
            f.write(f"|--------|-----------|\n")
            for domain, score in sorted(domain_scores.items(),
                                        key=lambda x: -x[1]):
                bar = "" * int(score * 10) + "" * (10 - int(score * 10))
                f.write(f"| {domain} | {bar} {score:.1f} |\n")
            f.write(f"\n")

            # Operational Chain
            f.write(f"## Operational Chain ({len(chain)} steps)\n\n")
            for i, tool in enumerate(chain, 1):
                role = tool.get("role", f"Step {i}")
                role_desc = tool.get("role_desc", "")
                f.write(f"### Step {i}: {role}\n\n")
                f.write(f"**Tool:** `{tool['name']}`\n\n")
                if role_desc:
                    f.write(f"**Function:** {role_desc}\n\n")
                f.write(f"- **Domains:** {', '.join(tool['overlap'])}\n")
                f.write(f"- **Relevance:** {tool['relevance']}\n")
                f.write(f"- **Readiness:** {tool['readiness']}\n")
                f.write(f"- **Perspective:** {tool['perspective']}\n\n")

            # Full Arsenal
            f.write(f"## Full Arsenal ({len(all_tools)} matches)\n\n")
            f.write(f"| # | Tool | Domains | Relevance |\n")
            f.write(f"|---|------|---------|----------|\n")
            for i, tool in enumerate(all_tools[:30], 1):
                domains_str = ", ".join(tool["overlap"][:3])
                f.write(f"| {i} | {tool['name']} | {domains_str} | {tool['relevance']} |\n")

            if len(all_tools) > 30:
                f.write(f"\n*... и еще {len(all_tools) - 30} инструментов*\n")

            # Adversarial Review
            f.write(f"\n## Adversarial Review\n\n")
            for risk in risks:
                prefix = "" if "WARNING" in risk else ("" if "CRITICAL" in risk else "")
                f.write(f"- {prefix} {risk}\n")

            f.write(f"\n---\n")
            f.write(f"*NEXUS Fusion Agent | Zero-Hallucination Protocol*\n")


# ============================================================
# CLI / INTERACTIVE
# ============================================================
def interactive_mode(engine: FusionEngine):
    """Интерактивный режим Fusion Agent."""
    print("\n" + "=" * 60)
    print("  NEXUS INTELLIGENCE FUSION AGENT v1.0")
    print("  Введите задачу / миссию. Команда 'exit' для выхода.")
    print("=" * 60 + "\n")

    while True:
        try:
            query = input("[FUSION] > ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not query or query.lower() in ("exit", "quit", "q"):
            print("[FUSION] Session ended.")
            break

        try:
            path = engine.generate_briefing(query)
            print(f"[FUSION] Report ready: {path}\n")
        except Exception as e:
            print(f"[FUSION] Error: {e}\n")


def single_query(engine: FusionEngine, query: str):
    """Одиночный запрос из командной строки."""
    path = engine.generate_briefing(query)
    # Выводим содержимое в stdout
    with open(path, encoding="utf-8") as f:
        print(f.read())


if __name__ == "__main__":
    engine = FusionEngine()

    if len(sys.argv) > 1:
        # CLI mode: python wiki_fusion_agent.py "Разведка по IT-компании"
        single_query(engine, " ".join(sys.argv[1:]))
    else:
        # Interactive mode
        interactive_mode(engine)
