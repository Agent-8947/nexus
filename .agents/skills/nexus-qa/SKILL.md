---
name: nexus-qa
description: "QA Lead Mode for NEXUS. [v5.0 Hardened] Automatically tests web applications using browser automation to find UI bugs and user flow breakages."
---

# 🕵️ NEXUS QA: QA Lead Mode

Этот навык дает агенту глаза и методологию тестирования. Вместо догадок о том, «работает ли UI», мы идем и кликаем.

## ⚙️ Команда: `/qa` (Browser Validation)

Когда агент завершает правку интерфейса, он вызывает `/qa`:

### 1. Diff-Aware Testing
- Агент читает `git diff` или список последних изменений.
- Определяет, какие роуты и страницы затронуты (например, `/login` или `/dashboard`).

### 2. Browser Exploration
- Запуск `read_browser_page` (или эквивалента) для перехода по URL.
- Проверка на:
    - 404/500 ошибки.
    - Визуальные наложения (Z-index).
    - Кликабельность кнопок (формы должны сабмититься).

### 3. Verification Report
Результат работы — лог-файл `docs/qa_report-ID.md` с:
1. **Health Score**: От 0 до 100%.
2. **Top 3 Issues**: Критичные ошибки интерфейса с предложением авто-фикса.

## 🛠 Инструменты

- Использовать `read_browser_page` для получения DOM и скриншотов.
- Использовать `firecrawl` для глубокого сканирования сайта (Site mapping).

---
**Status**: ACTIVE | **Role**: QA LEAD / SDET
