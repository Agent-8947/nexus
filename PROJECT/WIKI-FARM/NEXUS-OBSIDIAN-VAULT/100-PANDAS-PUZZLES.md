---
tags: [nexus-vault, data, pandas, python, data-engineering, exercises, etl]
category: Data / Data Engineering
language: Python, Jupyter Notebook
github: https://github.com/ajcr/100-pandas-puzzles
---

# 100-PANDAS-PUZZLES — Боевая Тренировка по pandas

## Описание
100 практических задач для глубокого освоения библиотеки pandas. Фокус — на ядре инструментария: индексация (loc/iloc/fancy), группировка (groupby), агрегация, очистка данных (NaN handling), работа с DatetimeIndex, MultiIndex и визуализация. Каждая задача — конкретный сценарий манипуляции с DataFrame/Series, с решениями в отдельном notebook.

## Основные Разделы
1. **DataFrame Basics** — select, sort, add columns, aggregation (Easy)
2. **Beyond Basics** — комбинирование методов, chaining (Medium)
3. **Harder Problems** — нестандартные задачи, требующие composit-подхода (Hard)
4. **DatetimeIndex** — time series manipulation, resampling
5. **Cleaning Data** — работа с пропусками, типами, дубликатами
6. **MultiIndex** — иерархические индексы
7. **Plotting** — pandas plot API

## Почему это Killer-App
- **Задачи реального мира** — не синтетические примеры, а типичные задачи Data Engineer.
- **Graduated Difficulty** — от Easy до Hard, можно дозировано подбирать сложность.
- **Solutions Notebook** — встроенная self-check система.
- **Community-driven** — активные контрибьюторы добавляют новые задачи.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Тест-кейсы для Data Validation слоя NEXUS пайплайна.
- **Интеграция:** Основа для `NEXUS-FARM Data Quality Agent` — автоматическая проверка структуры загружаемых датасетов.
- **Ключевое:** MultiIndex задачи критичны для работы с NEXUS иерархическими DNA структурами.

## Топ-3 примера

```python
# Группировка + агрегация
df.groupby('category')['value'].agg(['mean', 'std', 'count'])

# Работа с пропусками
df.dropna(subset=['critical_col']).fillna({'other_col': 0})

# DatetimeIndex resample
df.set_index('date').resample('W')['value'].sum()
```

## Связанные Репозитории
- [[PANDAS]] — исходная библиотека
- [[100-DAYS-OF-ML-CODE]] — смежный образовательный курс
- [[PANDAS-AI]] — LLM-powered надстройка над pandas
- [[DATA-SCIENCE-IPYTHON-NOTEBOOKS]] — Jupyter-ноутбуки для практики
- [[PYTHON-DS]] — Python для Data Science
