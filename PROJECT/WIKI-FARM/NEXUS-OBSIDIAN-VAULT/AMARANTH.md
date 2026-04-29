---
tags: [nexus-vault, hardware, hdl, fpga, python, amaranth, nmigen, digital-logic, asic, yosys, chipflow]
category: Hardware / FPGA Development
language: Python
github: https://github.com/amaranth-lang/amaranth
---

# AMARANTH HDL — Проектирование "Железа" на языке Python

## Описание
Amaranth (ранее nMigen) — это тулчейн с открытым исходным кодом для разработки аппаратного обеспечения на основе синхронной цифровой логики. Вместо традиционных Verilog или VHDL, Amaranth использует Python для описания структуры чипа. Это позволяет использовать всю мощь Python (генераторы, метапрограммирование) для создания сложных иерархических дизайнов ПЛИС (FPGA) и специализированных интегральных схем (ASIC).

## Основные Компоненты
1. **Amaranth HDL** — расширяемый язык описания аппаратуры.
2. **Standard Library** — базовые блоки (FIFO, делители, мультиплексоры).
3. **Simulator** — встроенный движок для верификации логики перед прошивкой.
4. **Build System** — интеграция с Yosys, nextpnr и проприетарными тулчейнами (Vivado, Quartus, Diamond).

## Почему это Killer-App
- **Eliminate Mistakes** — строгая типизация и структура Amaranth предотвращают классические ошибки Verilog (например, ненамеренное создание защелок/latches).
- **Reusable Components** — объектно-ориентированный подход к аппаратуре: создание сложных SoC (System on Chip) из модулей Python.
- **Modern Workflow** — поддержка современных FPGA семейств (Lattice iCE40, ECP5, AMD 7-series, UltraScale+) через FOSS тулчейны.
- **Integration** — возможность встраивать существующий Verilog/VHDL код напрямую в Amaranth-дизайны.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Hardware Synthesis Engine — NEXUS может генерировать специализированные аппаратные ускорители (например, для криптографии), синтезируя Amaranth-код.
- **Интеграция:** Использование `amaranth-soc` для проектирования кастомных контроллеров внутри робототехнических узлов NEXUS.
- **Ключевое:** Поддержка `Yosys+nextpnr` как целевого пайплайна для автономной прошивки FPGA агентами NEXUS.

## Поддерживаемые Платформы
- **Lattice:** iCE40, MachXO2/3, ECP5, Nexus (Radiant).
- **AMD (Xilinx):** 7-series (Vivado), Spartan 6, Virtex 4/5/6 (ISE).
- **Altera (Intel):** Quartus.
- **Quicklogic:** EOS S3 (Yosys+VPR).

## Связанные Репозитории
- [[YOSYS]] — основной движок логического синтеза
- [[NEXTPNR]] — инструмент трассировки (Place & Route)
- [[AMARANTH-BOARDS]] — определения популярных отладочных плат
- [[AMARANTH-SOC]] — библиотека для построения систем на кристалле
