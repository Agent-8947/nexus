---
tags: [nexus-vault, security, vulnerability-scan, surface-analysis, microsoft]
category: Security / Infrastructure Audit
language: C# / CLI
github: https://github.com/microsoft/AttackSurfaceAnalyzer
---

# ATTACKSURFACEANALYZER — System Attack Surface Analyzer (A.S.A.)

## Описание
**Attack Surface Analyzer** — это продвинутый инструмент аудита от **Microsoft**, который сравнивает состояние системы **ДО** и **ПОСЛЕ** установки программного обеспечения или изменения конфигурации. Он находит всё: новые файлы, ключи реестра, открытые порты, сервисы и изменения прав доступа, которые программа тайно внесла в систему.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Язык | C# (.NET Core 6+) |
| Interface | CLI / Electron GUI |
| Platforms | Windows, Linux, macOS |
| Database | SQLite (local) |
| Output | JSON / HTML / Diff |

## Ключевые Анализаторы
1. **File System** — находит новосозданные или измененные файлы (даже скрытые).
2. **Registry (Windows)** — отслеживает манипуляции с ключами автозагрузки и системными настройками.
3. **Network Ports** — детектирует новые открытые сокеты (Backdoors/Listeners).
4. **Services** — мониторит создание новых системных служб.
5. **Certificates** — проверяет добавление новых доверенных CA (техника Man-In-The-Middle).
6. **User Accounts** — видит создание новых пользователей или групп.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Контроль Поверхности Атаки (Attack Surface Control). "Что изменилось в моем окружении?"
- **Интеграция:** Модуль NEXUS Monitor — автоматическое сканирование системы раз в час для обнаружения скрытых изменений (Intrusion Detection).
- **Ключевое:** Использование инкрементальных снимков (Snapshotting) для точного сравнения состояний.

## Пример запуска (CLI)
```bash
# Делаем "чистый" снимок системы ДО установки
asa.exe collect --name BeforeUpdate

# Устанавливаем сомнительный софт...
# Делаем снимок ПОСЛЕ
asa.exe collect --name AfterUpdate

# Генерируем отчет о разнице (DIFF)
asa.exe export --first BeforeUpdate --second AfterUpdate -o diff_report.html
```

## Связанные Репозитории
- [[APPLICATIONINSPECTOR]] — анализ "намерений" самого кода
- [[CHIPSEC]] — аудит безопасности прошивок
- [[AUTOSPLOIT]] — эксплуатация найденных дыр
- [[AMBER]] — технима обхода таких сканеров (Evasion)
- [[BLACK-HAT-RUST]] — наступательная безопасность
