---
tags: [nexus-vault, cs, algorithms, data-structures, python, jupyter, education]
category: CS / Algorithms & Data Structures
language: Python, Jupyter Notebook
github: https://github.com/coells/100days
---

# 100DAYS — 100 Дней Алгоритмов

## Описание
Проект реализации 100 алгоритмов день за днём — живой код в Jupyter Notebooks с визуализацией через Bokeh. Охватывает классические алгоритмы Computer Science: сортировки, поиск, графы, динамическое программирование, численные методы. Код написан на Python 3 с использованием Anaconda стека. Ключевая ценность — нет академической сухости, есть практичность и энтузиазм.

## Основные Разделы
1. **Sorting & Searching** — классические алгоритмы с наглядными реализациями
2. **Graph Algorithms** — обходы, кратчайшие пути
3. **Dynamic Programming** — задачи оптимизации с мемоизацией
4. **Numerical Methods** — вычислительные алгоритмы
5. **Data Structures** — деревья, хеш-таблицы, кучи
6. **Visualization** — Bokeh-анимации для понимания работы алгоритмов

## Почему это Killer-App
- **Живые notebook** — алгоритмы можно запустить и увидеть в действии.
- **Bokeh визуализации** — анимированные демонстрации работы структур данных.
- **Честность** — автор предупреждает: код написан в спешке, ищи баги сам. Это обучающий инструмент.
- **Компактность** — один алгоритм = один notebook = минимальный когнитивный overhead.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Референсные реализации алгоритмов для NEXUS Evolution Logic (`DNA_07`).
- **Интеграция:** Алгоритмы сортировки/поиска используются в `FarmOracle` для ранжирования репозиториев по релевантности.
- **Ключевое:** DP-алгоритмы оптимальны для задач маршрутизации агентов и уменьшения глубины поиска в DNA граф.

## Топ-3 примера

```python
# BFS обход графа
from collections import deque
def bfs(graph, start):
    visited, queue = set(), deque([start])
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            queue.extend(graph[node] - visited)
    return visited

# Memoized Fibonacci (DP)
from functools import lru_cache
@lru_cache(maxsize=None)
def fib(n): return n if n < 2 else fib(n-1) + fib(n-2)
```

## Связанные Репозитории
- [[JAVASCRIPT-ALGORITHMS]] — аналогичная коллекция на JS
- [[THEALGORITHMS-PYTHON]] — более полная коллекция алгоритмов
- [[ALGORITHM-VISUALIZER]] — веб-визуализатор алгоритмов
- [[HELLO-ALGO]] — современный учебник по алгоритмам с анимациями
- [[CLRS]] — академическая база (Introduction to Algorithms)
