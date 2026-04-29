# 🧬 NEXUS Evolution Blueprint: Hermes Core

Выжимка ключевых компонентов из `NousResearch/hermes-agent-self-evolution` для интеграции в NEXUS (Hardened Edition).

## 1. Core Logic: The Evolution Loop

Для работы в NEXUS нам нужен цикличный пайплайн самосовершенствования:

1. **Target Selection**: Выбор `SKILL.md` (например, `codebase-inspection`).
2. **Trace Collection**: Сбор логов выполнения (success/fail).
3. **Synthetic Eval Gen**: Если данных мало, LLM генерирует 20-50 пограничных кейсов (Edge Cases).
4. **Mutation Phase**:
   - **Engine**: GEPA (Genetic-Pareto).
   - **Action**: Создание 5-10 вариаций промпта с разными тактиками (Few-shot, Chain-of-Thought, Zero-shot).
5. **Evaluation**:
   - Проверка через `pytest` (функциональность).
   - LLM-Jury (проверка на галлюцинации и стиль).
6. **Promotion**: Замена старого `SKILL.md` на победителя, если Score > текущего на 5+%.

## 2. Essential Components (Must-Copy)

- **`evolution/evals/`**: Модели судейства (Jury models). Они определяют, что "хорошо", а что "плохо".
- **`evolution/skills/`**: Логика парсинга и мутации markdown-файлов навыков.
- **`GEPA Optimizer`**: Алгоритм отбора по Парето (точность vs цена).

## 3. NEXUS Integration Strategy

- **Агент-Эволюционер**: Создать отдельный агент `WIKI_EVOLUTION_MASTER.py`.
- **Trigger**: Запускать раз в неделю или при падении Success Rate навыка.
- **Git Flow**: Каждая эволюция — это новая ветка. Авто-PR после прохождения тестов.

## 4. Immediate ROI

- **Повышение точности**: С 70% до 90+% за 10 итераций.
- **Авто-фикс багов**: Система сама правит свои инструкции после ошибки.
