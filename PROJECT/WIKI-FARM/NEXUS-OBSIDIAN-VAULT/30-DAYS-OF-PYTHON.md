---
tags: [nexus-vault, python, education, beginner, web-scraping, api, mongodb, oop, 30-days-challenge]
category: Education / Python Programming
language: Python, Markdown
github: https://github.com/Asabeneh/30-Days-Of-Python
---

# 30-DAYS-OF-PYTHON — Полный Курс Python за 30 Дней

## Описание
Структурированный 30-дневный Python-курс от нуля до продвинутого уровня. Охватывает: базовые типы данных, ООП, файловая система, регулярные выражения, web scraping, API, FastAPI, MongoDB интеграция. Каждый день — теория + упражнения трёх уровней (Easy/Medium/Hard). Поддерживается на нескольких языках (Portuguese, Chinese). Один из самых популярных Python-репозиториев на GitHub (50k+ stars).

## Основные Разделы
1. **Days 1–10**: Основы — типы, операторы, строки, списки, словари, циклы, функции
2. **Days 11–20**: Средний уровень — модули, comprehensions, ООП, обработка ошибок, файлы, pip
3. **Days 21–25**: Продвинутый — ООП полностью, web scraping (BeautifulSoup), pandas, statistics
4. **Days 26–30**: Production — Flask/Django, MongoDB, REST API, building API, выводы

## Почему это Killer-App
- **Zero-to-Hero траектория** — один репозиторий закрывает весь базовый Python.
- **Трёхуровневые упражнения** — адаптивная сложность под любого студента.
- **Production-ready навыки** — MongoDB, REST API, web scraping = реальные задачи.
- **50k+ звёзд, переводы** — проверенный мировым сообществом материал.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Onboarding Reference — база знаний для автоматической генерации стартовых агентов.
- **Интеграция:** Day 28–29 (API) — прямой referent для NEXUS HTTP-агентов (`osint collector`).
- **Ключевое:** Day 22 (Web Scraping) — основа NEXUS OSINT/Harvest агентов.

## Топ-3 примера

```python
# Day 21: Простое ООП
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def greet(self): return f"Hi, I'm {self.name}"

# Day 22: Web Scraping
from bs4 import BeautifulSoup; import requests
html = requests.get("https://example.com").text
soup = BeautifulSoup(html, 'html.parser')

# Day 29: FastAPI
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def read_root(): return {"Hello": "NEXUS"}
```

## Связанные Репозитории
- [[100-DAYS-OF-ML-CODE]] — продолжение для ML после Python базы
- [[30-DAYS-OF-JAVASCRIPT]] — аналог для JavaScript стека
- [[PYTHON-DS]] — Python для Data Science после курса
- [[AWESOME-PYTHON]] — библиотеки для углубления
- [[FASTAPI]] — production фреймворк из Day 29
