---
tags: [nexus-vault, software-engineering, cpp, cheat-sheet, reference, modern-cpp]
category: Education / Programming Languages (C++)
language: C++11 / C++14 / C++17 / C++20
github: https://github.com/gibsjose/cpp-cheat-sheet
---

# CPP-CHEAT-SHEET — Modern C++ Reference Master List

## Описание
**C++ Cheat Sheet** — это компактный, структурированный справочник по языку **C++** (включая стандарты C++11, 14, 17, 20). Он охватывает всё: от примитивных типов и циклов до управления памятью (Smart Pointers), константности (const-correctness) и продвинутых шаблонов (Templates). Это идеальный источник для быстрого поиска синтаксиса или освежения в памяти правил работы со стандартной библиотекой STL.

## Что внутри (Разделы)
1. **Basics**— Variables, Control flow, Loops.
2. **Memory**— Raw Pointers, References, RAII, `unique_ptr`, `shared_ptr`.
3. **OOP**— Class, Inheritance, Polymorphism, Virtual functions.
4. **Const Correctness**— `const` with pointers, functions, methods.
5. **Modern C++**— `auto`, `lambda`, `nullptr`, Move semantics (`std::move`).
6. **STL**— Vector, Map, Set, Algorithms (`std::sort`, `std::find`).

## Почему это Killer-App для ИИ
- **Snippet Collection**— Сотни готовых кусков кода (snippets) для генерации качественного C++ кода.
- **Reference Table**— Таблицы сложности операций (Big O) в контейнерах STL.
- **Rules of Thumb**— Лаконичные правила "когда что использовать" (напр. `unique_ptr` vs `shared_ptr`).

## Архитектурная Ценность для NEXUS
- **Паттерн:** Высокая Производительность (High Performance). Если агент NEXUS пишет модуль на С++, он должен следовать этим лучшим практикам.
- **Интеграция:** Модуль NEXUS Code Constructor — генерация и отладка низкоуровневых системных компонентов.
- **Ключевое:** Охватывает темы управления памятью, что критично для стабильности.

## Пример шпаргалки (Smart Pointers)
```cpp
// 1. Владение одним объектом (рекомендуется)
std::unique_ptr<int> p1 = std::make_unique<int>(10);

// 2. Разделяемое владение (счетчик ссылок)
std::shared_ptr<int> p2 = std::make_shared<int>(20);

// 3. Слабая ссылка (без владения, во избежание циклов)
std::weak_ptr<int> p3 = p2;
```

## Связанные Репозитории
- [[ALGS4]] — алгоритмы (база для С++)
- [[BUILD-YOUR-OWN-X]] — практика на С++ (напр. движки)
- [[CGAL]] — сложная С++ геометрия
- [[BULLET3]] — С++ физика
- [[CLEAN-CODE-JAVASCRIPT]] — общие правила чистого кода
- [[APPLICATIONINSPECTOR]] — анализ безопасности этого кода
