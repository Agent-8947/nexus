# NEXUS DNA SYNTHESIS ARCHITECTURE (v5.0 Hardened)

## 1. Эволюция архитектуры (The Path to Gen-5)
Изначальный подход (Gen-1/Gen-2) использовал **AST Template Unrolling** — разворачивание защитных блоков (`try/except/logger`) для каждой функции. Это приводило к громоздкому, замусоренному коду. 
Попытки лечить этот код с помощью автоматических "вакцин" (`nexus_patcher.py`) привели к проблеме Goodhart's Law: патчер дублировал код, игнорировал контекст (NameExceptions) и приводил к потере данных (Ephemeral Data Loss через `getattr` на пустых словарях).

Решение — полный отказ от постобработки в пользу **Zero-Stub Pipeline** и **Паттерна Экзекутора**.

## 2. Ключевые компоненты (Zero-Stub Pipeline)

### Module A: `DNA_23_Domain_Blocks.py` (The Assembler)
Отвечает за сборку агента. Вместо копипасты бойлерплейта, он внедряет один универсальный метод `__nexus_execute__` во все синтезированные файлы. 
Вызовы блоков теперь выглядят так:
```python
__nexus_execute__(extract_links, target, "findings", self.findings, self.all_stats, self.errors)
```

### Module B: `DNA_25_Role_Contracts.py` (The Interfaces)
Гарантирует, что агент строго соблюдает свой тип.
Устранен баг с потерей статистики (Lost Stats Bug). Теперь `self.all_stats: Dict` аппаратно прошит в `__init__` для ролей **Collector**, **Analyzer**, **Storage**, **Orchestrator** и **Presentation**.

### Module C: `__nexus_execute__` (The Universal Engine)
Глобальная вспомогательная функция, которая аппаратно генерируется в верхней части каждого агента.
**Возможности:**
- Обрабатывает ошибки без падения агента (отправляет их в `errors_list`).
- Динамическая маршрутизация:
  - Тип `findings` -> безопасно дописывается через `.extend()`.
  - Типы `stats` / `system_info` -> обновляют `.update()` словарь глобальной статистики.
  - Гибридные типы (напр. `port_report`) -> обновляют словарь И конвертируются в `Finding` объекты.

## 3. Матрица Ролей (Role Matrix Support)
Агенты могут динамически наследовать одну из ролей со строгой проверкой типов на входе и выходе:

| Роль | Метод | Ожидаемый Вход | Ожидаемый Выход |
| :--- | :--- | :--- | :--- |
| **Collector** | `collect(target)` | `str` (Path/URL) | `List[Dict]` |
| **Analyzer** | `analyze(findings)` | `List[Dict]` | `List[Dict]` |
| **Presentation**| `render(report)` | `Dict` (Отчет) | `str` (Markdown) |
| **Orchestrator**| `run(target)` | `str` | `Dict` (Полный отчет)|

## 4. Защита от дурака (Fail-Safes)
*   **Zero-Guessing Analysis**: Если `Analyzer` вызывает блок с маркером входа "target", сборщик берет `target` из поля `source` первой найденной записи. `NameError` устранен.
*   **Type Guard**: `TypeError` блокируются на входе `__nexus_execute__`.
*   **Integration Test**: Каждый агент проходит встроенный `--test`. Сборка успешна только по `Exit Code: 0`.
