---
tags: [nexus-vault, software-engineering, oop, design-patterns, architectural-patterns, refactoring]
category: Education / Software Architecture (Visual Guide)
language: Polyglot (Java, Python, C#, JS)
github: https://github.com/refactoring-guru/design-patterns-cpp (or equivalent Refactoring.Guru index)
---

# DESIGN-PATTERNS — The Software Architecture Master List

## Описание
**Design Patterns** — это коллекция проверенных временем **шаблонов проектирования**, которые решают типовые проблемы в объектно-ориентированном программировании (ООП). Это язык, на котором общаются Senior-архитекторы. Если вы знаете паттерны, вы пишите код, который не рассыпается при первом изменении требований. Основано на материалах "Refactoring.Guru".

## Группы Паттернов (Выжимка)
1. **Creational (Порождающие)**— Как создавать объекты, не делая их зависимости жесткими (Singleton, Factory Method, Abstract Factory, Builder, Prototype).
2. **Structural (Структурные)**— Как собирать объекты в большие структуры (Adapter, Bridge, Decorator, Facade, Proxy).
3. **Behavioral (Поведенческие)**— Как объекты общаются и делят ответственность (Strategy, Observer, State, Command, Template Method, Iterator).

## Почему это Killer-App
1. **Unified Language**— Сказать коллеге "Давай тут используем Strategy" вместо 20-минутного объяснения.
2. **Extensibility**— Использование паттерна "Decorator" позволяет добавлять функции (напр. логирование), не меняя старый код.
3. **Robustness**— Паттерн "Observer" (издатель-подписчик) делает систему слабосвязанной и надежной.
4. **Maintenance**— Код с паттернами легче читать и отлаживать новым разработчикам.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Масштабируемая Автономия (Scalable Autonomy). Весь **NEXUS Orchestrator** построен на паттернах: **Command** (команды агентам), **Observer** (метки прогресса), **Strategy** (смена LLM-моделей на лету).
- **Интеграция:** Агенты-Конструкторы NEXUS должны использовать эти паттерны при генерации нового софта.
- **Ключевое:** Разделение бизнес-логики и инфраструктуры (Facade/Proxy).

## Топ-3 Примера для NEXUS
- **Factory**— "Агент, создай мне OSINT-разведчика" (Фабрика решит, будет это Shodan или Censys агент).
- **Observer**— Панель Дашборда (она "слушает" события ото всех 1400+ репозиториев сразу).
- **Strategy**— Инструмент зашифровки (можно менять алгоритм AES на RSA без изменения кода приложения).

## Связанные Репозитории
- [[CLEAN-CODE-JAVASCRIPT]] — чистота на уровне строк
- [[ALGS4]] — как паттерны работают внутри алгоритмов
- [[BUILD-YOUR-OWN-X]] — практика применения паттернов
- [[ANYTHING-LLM]] — архитектура RAG-интерфейса
- [[APPLICATIONINSPECTOR]] — распознавание паттернов в чужом коде
- [[ADVANCED-JAVA]] — энтерпрайз-паттерны
