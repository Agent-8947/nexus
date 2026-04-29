---
tags: [nexus-vault, security, exploit, pe-loader, evasion]
category: Security / Offensive
language: Go
github: https://github.com/nickvdyck/amber
---

# AMBER — PE Loader with AV Evasion

## Описание
**Amber** — reflective PE loader (загрузчик исполняемых файлов) с встроенным обходом антивирусов. Использует SGN encoder для полиморфного шифрования пейлоада и CRC32/IAT API hashing для сокрытия вызовов WinAPI.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Язык | Go + ASM (x86/x64) |
| Encoder | SGN (Shikata Ga Nai) |
| API Resolution | CRC32 hashing / IAT patching |
| Target | Windows PE (EXE/DLL) |
| Evasion | Polymorphic shellcode |

## Механика Работы
1. **Input:** Берет обычный PE-файл (Windows EXE)
2. **Pack:** Оборачивает в рефлективный загрузчик
3. **Encode:** Применяет SGN encoder (полиморфное шифрование)
4. **Resolve:** WinAPI вызовы через CRC32 hash вместо имён
5. **Output:** «Невидимый» исполняемый файл

## Архитектурная Ценность для NEXUS
- **Паттерн:** Техника рефлективной загрузки — применима для загрузки агентов в память без записи на диск
- **Интеграция:** API hashing через CRC32 — полезно для stealth-модулей NEXUS
- **Риск:** Высокий — инструмент наступательной безопасности. Только для Red Team / аудита

## Ключевые Техники
```
SGN Encoder Pipeline:
PE File → XOR Encryption → Polymorphic Stub → CRC32 API Resolution → In-Memory Execution

Anti-Detection:
- No static imports in IAT
- Encrypted payload body
- Randomized stub generation
- No disk write (reflective load)
```

## Связанные Репозитории
- [[CHAOS-ROOTKIT]] — rootkit для x64
- [[AUTOSPLOIT]] — автоматизация эксплуатации
- [[CHIPSEC]] — анализ безопасности железа
- [[BLACK-HAT-RUST]] — offensive security на Rust
