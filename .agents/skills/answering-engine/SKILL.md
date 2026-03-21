---
name: answering-engine
description: "AI-powered research engine [NEXUS Hardened v5.0]. Implements the Deep Search loop: Search → Verify → Synthesize with mandatory source citations."
---

# 🔍 Answering Engine (v5.0): Hardened Edition

Этот навык превращает NEXUS в высокоточный аналитический инструмент, способный проводить многоуровневое исследование (Deep Research) с опорой на внешние источники.

## 🧬 Operational Philosophy

Борьба с галлюцинациями через **"Truth is Outside"**. Внутренняя память LLM — для логики, внешний поиск — для фактов.

### Phase 1: Deep Search Loop
1. **Multi-Query Expansion**: Разбивать один сложный вопрос на 3-5 специфических поисковых запросов.
2. **Exhaustive Extraction**: Если информация не найдена на первой странице — менять тактику поиска (использовать `Exa` или `Tavily` в паре).
3. **Pagination Handling**: При чтении длинных статей/документации использовать чанки по 100 строк.

### Phase 2: Mandatory Verification
- **Cross-Checking**: Подтверждать критические факты как минимум в двух независимых источниках.
- **Conflict Resolution**: Если источники противоречат друг другу — явно указывать это в ответе, сохраняя архитектурный нейтралитет.

### Phase 3: Zero-Preamble Synthesis
- Ответ должен начинаться с **Сути**. Никаких "Я провел исследование...", "Вот что мне удалось найти...".
- Использование ссылок в формате `[Название источника](URL)` обязательно для каждого утверждения.

---

## 🛠️ NEXUS Implementation Patterns (v5.0)

### 1. Research Workflow
Использовать логику `researcher.md` для циклического сбора данных.
*Путь: [researcher.md](file:///e:/Downloads/--ANTIGRAVITY%20store/IDE-NEXUS/.agents/skills/answering-engine/prompts/researcher.md)*

### 2. Search Connectors
Использовать `searxng-connector.js` для первичного сбора данных.
*Путь: [searxng-connector.js](file:///e:/Downloads/--ANTIGRAVITY%20store/IDE-NEXUS/.agents/skills/answering-engine/logic/searxng-connector.js)*

### 3. Data Visualization (Widget Protocol)
Сложные данные (графики, котировки) оформлять через Widget Schema.
*Путь: [widgets-schema.md](file:///e:/Downloads/--ANTIGRAVITY%20store/IDE-NEXUS/.agents/skills/answering-engine/logic/widgets-schema.md)*

---

## 🚨 Critical Constraints

- **Source Integrity**: Запрещено выдумывать ссылки или цитировать источники, которые не были физически прочитаны через инструменты.
- **Objectivity**: Не поддаваться наводящим вопросам пользователя. Если факты говорят об обратном — сообщать об этом прямо.
- **Freshness**: Всегда проверять актуальность данных (дату публикации), если вопрос касается технологий или новостей.

---
**Status**: ACTIVE | **Protocol**: NEXUS-V5-HARDENED
