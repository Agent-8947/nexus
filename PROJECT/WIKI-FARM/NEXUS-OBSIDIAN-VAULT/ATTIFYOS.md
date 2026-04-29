---
tags: [nexus-vault, security, iot, exploitation, pentest]
category: Security / IoT Audit Distro
language: Linux (Ubuntu-based)
github: https://github.com/adi0x90/attifyos
---

# ATTIFYOS — IoT Penetration Testing Distribution

## Описание
**AttifyOS** — это специализированный дистрибутив на базе **Ubuntu**, созданный специально для проведения аудита безопасности и **пентеста IoT-устройств** (Internet of Things). Он содержит все необходимые инструменты для взлома прошивок, анализа радиоканалов (SDR) и работы с аппаратными интерфейсами (UART, JTAG, SPI).

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| База | Ubuntu 18.04+ (в образе VM) |
| Firmware Analysis | Binwalk, Firmwalker, QEMU |
| Hardware Tools | OpenOCD, Flashrom, Baudrate.py |
| SDR Tools | GNU Radio, Gqrx, HackRF tools |
| Web/Network | Burp Suite, Nmap, Wireshark |

## Инструментальные Стеки в OS
- **Firmware Reversing**— распаковка бинарных файлов прошивок и поиск паролей.
- **Hardware Interaction**— чтение данных напрямую из микросхем памяти.
- **SDR**— перехват сигналов от 433 Мгц до 5 ГГц (пульты, замки, трекеры).
- **Embedded Security**— тестирование BLE (Bluetooth Low Energy) и Zigbee.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Единое рабочее место IoT-аудитора. Это "швейцарский нож" для вскрытия любых железных устройств.
- **Интеграция:** Можно использовать Docker-версии утилит из AttifyOS в NEXUS-агентах для автоматического анализа прошивок.
- **Ключевое:** Использование QEMU для запуска прошивок роутеров без реального железа (Эмуляция).

## Пример: Анализ прошивки в системе
```bash
# Распаковка прошивки и поиск интересного
binwalk -e firmware.bin
cd _firmware.bin.extracted
firmwalker .
# (Firmwalker выведет список всех паролей, API-ключей и IP внутри прошивки)
```

## Связанные Репозитории
- [[CHIPSEC]] — самый глубокий аудит прошивок BIOS/UEFI
- [[BASIC_VERILOG]] — создание таких систем
- [[CAMERADAR]] — поиск и взлом IP-камер
- [[ARIEL-OS]] — создание защищенного интернета вещей
- [[BLACK-HAT-RUST]] — хакинг систем
