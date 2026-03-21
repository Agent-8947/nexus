---
description: Генерация глубокой технической документации в текстовом формате (.md) по проекту NEXUS.
---

# /doc — Technical Documentation Generator

Этот воркфлоу генерирует "живой слепок" архитектуры NEXUS через `DocumentFactory`.

### 1. Полный Pipeline (Extract → Generate → Validate)

// turbo
python PROJECT/scripts/office/DocumentFactory.py --all

### 2. Результат

Файл `PROJECT/DOCS/TECHNICAL_BRIEF.md` содержит:

- **Architecture Overview**: Mermaid-схема системы.
- **Stack Definition**: Таблица технологий из `memory.json`.
- **Active Skills**: Список навыков из `PROJECT/skills/`.
- **ADR History**: Последние архитектурные решения.
- **Script Map**: Все активные скрипты, сгруппированные по директориям.

### 3. Финализация

Вывод готового документа и сохранение в `PROJECT/DOCS/`.
