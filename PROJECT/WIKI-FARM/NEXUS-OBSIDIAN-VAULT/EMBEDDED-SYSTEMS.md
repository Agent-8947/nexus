---
tags: [nexus-vault, hardware, microcontrollers, assembler, c, embedded-c, robotics]
category: Hardware / Systems Programming (Mastery)
language: C / C++ / Assembly / Rust
github: https://github.com/m-p-c/embedded-systems (or equivalent learning repo)
---

# EMBEDDED-SYSTEMS — The Ultimate Guide to Systems Programming

## Описание
Этот репозиторий (и база знаний) представляет собой глубочайшее погружение в мир **встроенных систем (Embedded Systems)**. Он охватывает всё: от архитектуры процессоров и наборов команд (ISA) до написания драйверов на C и разработки операционных систем реального времени (**RTOS**). Это библия для тех, кто хочет программировать не только "софт", но и "железо": микроконтроллеры, ПЛИС (FPGA) и SoC.

## Основные Темы (Выжимка)
1. **CPU Architectures**— ARM Cortex-M (standard), RISC-V (open-source future), AVR, PIC.
2. **Low-level C/C++**— Указатели на регистры (Memory-mapped I/O), прерывания (Interrupts), работа с таймерами и DMA.
3. **Communication Protocols**— I2C, SPI, UART, CAN Bus, Ethernet, USB.
4. **RTOS Foundations**— Потоки (Tasks), мьютексы, семафоры, очереди (Queues).
5. **Hardware Security**— Secure Boot, TrustZone, физические атаки (Side-channel).
6. **Compilers & Build Systems**— GCC toolchains, Make, CMake, Linker Scripts.

## Почему это Killer-App
- **Deep Scrutiny**— Понимание того, как каждая строчка кода на С превращается в импульсы на ножках процессора.
- **Reference Code**— Примеры реализации драйверов для популярных периферийных устройств.
- **Problem Solving**— Как бороться с дребезгом контактов, помехами и нехваткой RAM (напр. 2 Кб на весь код).

## Архитектурная Ценность для NEXUS
- **Паттерн:** Физический Ров (Hardware Gaps). Агенты NEXUS должны уметь программировать свои датчики и устройства с нуля.
- **Интеграция:** Модуль NEXUS Firmware Builder — автоматическая генерация прошивок для ваших ESP32-узлов [[ESP32]] на базе этой базы знаний.
- **Ключевое:** Охватывает темы Bare-metal программирования (без ОС), что критично для скорости.

## Топ-3 концепции (Embedded)
- **Interrupts**— как процессор мгновенно реагирует на внешний сигнал (напр. нажатие кнопки).
- **Registers**— "магические адреса" в памяти, через которые софт общается с транзисторами.
- **Linker Script**— файл, определяющий, в какую именно ячейку памяти попадет ваш код.

## Связанные Репозитории
- [[ESP32]] — практическая реализация на популярном чипе
- [[CANOPENNODE]] — промышленная сеть (глава по протоколам)
- [[AMARANTH]] — синтез железных модулей на Python
- [[ARDUINO-FOC]] — если ИИ управляет моторами (физика)
- [[CHIPSEC]] — безопасность такого железа (аудит)
- [[BASIC_VERILOG]] — создание аппаратных модулей
- [[ARIEL-OS]] — ОС на Rust для этого класса устройств
- [[DNA-FARM]] — источник наших данных
- [[DESIGN-PATTERNS]] — паттерны для встроенных систем
- [[CLEAN-CODE-JAVASCRIPT]] — чистота кода (общая)
- [[APPLICATIONINSPECTOR]] — анализ кода
- [[ALLUXIO]] — кэширование данных
- [[ARDUPILOT]] — сложная встроенная система (автопилот)
- [[BULLET3]] — симуляция физики этих систем
