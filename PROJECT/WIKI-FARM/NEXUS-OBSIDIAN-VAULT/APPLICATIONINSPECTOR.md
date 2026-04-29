---
tags: [nexus-vault, security, software-audit, cve, code-analysis, microsoft]
category: Security / Software Supply Chain
language: C# / Python / CLI
github: https://github.com/microsoft/ApplicationInspector
---

# APPLICATIONINSPECTOR — Microsoft Software Analysis Tool

## Описание
**ApplicationInspector** (Microsoft) — это кросс-платформенный инструмент командной строки, который помогает идентифицировать и анализировать "характеристики" исходного кода. Это не просто сканер уязвимостей, а инструмент для понимания того, **ЧТО делает код** (криптография, сеть, ОС-вызовы, работа с файлами).

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Язык | C# (.NET Core) |
| Interface | CLI / HTML Report |
| Languages | Python, Go, Java, JS, C#, C++, Ruby |
| Rules | 1000+ JSON-based patterns (RegEx) |

## Главные Функции
1. **Transparency Analysis** — понимание того, какие именно API использует сторонняя библиотека.
2. **Identification of Cryptography** — находит все алгоритмы шифрования (даже самописные).
3. **OS Functionality** — использование сокетов, процессов, реестра.
4. **Cloud Integration** — находит AWS/Azure/GCP API вызовы.
5. **Comparison** — сравнение двух версий кода на предмет добавления скрытых функций (Backdoors).

## Архитектурная Ценность для NEXUS
- **Паттерн:** Глубокая Прозрачность Кода (Full Transparency). Если агент NEXUS планирует интегрировать какой-то модуль из GitHub — ApplicationInspector сначала проверяет его.
- **Интеграция:** Можно встроить в NEXUS Constructor для автоматического написания документации к коду (на основе выявленных паттернов).
- **Ключевое:** В отличие от антивирусов, он фокусируется на "намерениях" кода.

## Пример запуска (CLI)
```bash
# Базовый анализ проекта в папке src
appinspector analyze -s ./src/ -f html -o report.html

# Только проверка на криптографию
appinspector analyze -s ./src/ -g "Cryptography"
```

## Связанные Репозитории
- [[APPINFOSCANNER]] — безопасность мобильных приложений
- [[BUNDLER-AUDIT]] — проверка Ruby зависимостей
- [[CHIPSEC]] — анализ безопасности железа
- [[AUTO-GLUON]] — как контрпример: автоматизация без ручного аудита
