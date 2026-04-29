---
tags: [nexus-vault, filesystem, apple, linux, fuse]
category: OS / Filesystems
language: C++
github: https://github.com/siva765/apfs-fuse
---

# APFS-FUSE — Apple File System driver for Linux

## Описание
Драйвер для интерфейса **FUSE (Filesystem in Userspace)**, который позволяет читать данные из файловой системы **APFS (Apple File System)** на операционных системах Linux. APFS является стандартом для macOS (начиная с High Sierra), iOS, tvOS и watchOS.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Язык | C++ |
| Interface | FUSE (Filesystem in Userspace) |
| Encryption | Partial support (unencrypted / some encrypted) |
| Platform | Linux (Ubuntu, Fedora, Arch) |

## Зачем это нужно
1. **Digital Forensics** — извлечение данных с дисков Mac и iPhone в среде Linux.
2. **Data Recovery** — восстановление файлов с поврежденных macOS-разделов.
3. **Cross-platform access** — монтирование дисков Apple как обычных папок.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Кросс-платформенная совместимость данных. Если агенту NEXUS нужно проанализировать образ диска iPhone (iOS), APFS-FUSE — это точка входа.
- **Интеграция:** Модуль NEXUS Recon — автоматическое монтирование найденных образов дисков Apple.
- **Ключевое:** Работает в userspace, что минимизирует риск падения ядра (Kernel Panic).

## Пример монтирования в Linux
```bash
# Определяем раздел с APFS (используем lsblk)
# Монтируем раздел /dev/sdb2 в папку /mnt/mac
apfs-fuse /dev/sdb2 /mnt/mac

# Для разделов с шифрованием FileVault (требуется пароль):
apfs-fuse -p "your_password" /dev/sdb2 /mnt/mac
```

## Связанные Репозитории
- [[AMBER]] — загрузчики и evasion
- [[CHIPSEC]] — анализ безопасности железа
- [[BRUTAL]] — операционная система на микроядре
