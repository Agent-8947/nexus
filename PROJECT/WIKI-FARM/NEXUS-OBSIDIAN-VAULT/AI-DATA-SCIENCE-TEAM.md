---
tags: [nexus-vault, ai, agents, data-science, pipeline, streamlit, langchain, pandas, automl, mlflow, multi-agent]
category: AI / Data Science Orchestration
language: Python
github: https://github.com/business-science/ai-data-science-team
---

# AI DATA SCIENCE TEAM — Мульти-Агентная Лаборатория Анализа Данных

## Описание
Библиотека специализированных ИИ-агентов для полной автоматизации рабочих процессов в Data Science. Включает флагманское приложение **AI Pipeline Studio**, которое превращает хаотичные исследования в визуализированные, воспроизводимые пайплайны. Агенты берут на себя загрузку данных, очистку, визуализацию (EDA) и построение моделей машинного обучения.

## Основные Разделы
1. **AI Pipeline Studio** — визуальный редактор пайплайнов с поддержкой lineage и автоматической генерацией скриптов.
2. **Specialized Agents** — Wrangling Agent, Cleaning Agent, Visualization Agent, Feature Engineering Agent.
3. **Multi-Agent Workflows** — совместная работа агентов (например, "Pandas Data Analyst" + "SQL Data Analyst").
4. **Supervisor Agent** — центральный контроллер, распределяющий задачи между узкоспециализированными агентами.
5. **AutoML & MLflow Integration** — интеграция с H2O и инструментами управления жизненным циклом моделей.

## Почему это Killer-App
- **Reproducibility** — каждый шаг ИИ фиксируется в коде и метаданных.
- **Hybrid Workflow** — возможность комбинировать ручные шаги эксперта с автоматическими действиями агентов.
- **Plug-and-Play Architecture** — легкое создание кастомных инструментов (`Custom Tools`) для специфических задач.
- **Ollama Support** — полная совместимость с локальными моделями через LangChain/Ollama.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Multi-Agent Data Ops — архитектура "Supervisor + Specialists" является целевой для NEXUS Intelligence Factory.
- **Интеграция:** Использование `MLflow Tools Agent` для мониторинга производительности NEXUS DNA мутаций.
- **Ключевое:** Принцип `metadata-only project save` позволяет NEXUS эффективно обмениваться "чертежами" исследований без передачи гигабайтов данных.

## Топ-3 приложения в составе
- **AI Pipeline Studio:** основной инструмент аналитика.
- **EDA Explorer App:** интерактивный ко-пилот для разведочного анализа.
- **SQL Data Analyst:** агент, работающий напрямую с базами данных.

## Связанные Репозитории
- [[LANGCHAIN]] — база для создания агентов
- [[STREAMLIT]] — фреймворк для UI приложений
- [[H2O-3]] — библиотека для AutoML
- [[PANDAS-AI]] — аналогичный подход к анализу через чат
