---
tags: [nexus-vault, hardware, drone, robotics, autopilot, uav]
category: Hardware / Autopilot (Drone)
language: C++ / Python (Mavlink)
github: https://github.com/ArduPilot/ardupilot
---

# ARDUPILOT — Open-Source Autopilot System

## Описание
**ArduPilot** — самая передовая, полнофункциональная и надежная система **автопилота с открытым исходным кодом**. Поддерживает мультикоптеры (ArduCopter), самолеты (ArduPlane), вездеходы (ArduRover), подводные лодки (ArduSub) и дирижабли. Это "мозги" для миллионов беспилотных аппаратов по всему миру.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Язык | C++ (ядро) / Lua (скрипты) |
| Protocol | MAVLink (Micro Air Vehicle Link) |
| RTOS | ChibiOS / Linux (SITL) |
| Sensors | EKF3 (Extended Kalman Filter) |
| Simulation | SITL (Software In The Loop) / Gazzebo |

## Ключевые Фичи
1. **EKF3 Logic** — сложнейшая математика для объединения данных акселерометра, гироскопа, барометра и GPS.
2. **Autonomous Missions** — планирование полета по точкам (Waypoints) с обходом препятствий.
3. **Smart RTL** — умное возвращение домой по пройденному пути при потере связи.
4. **Collision Avoidance** — поддержка лидаров и сонаров в реальном времени.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Автономная навигация в физическом мире (Physical Intelligence). Если NEXUS должен управлять реальным агентом (дроном-разведчиком), ArduPilot — это стандарт.
- **Интеграция:** Использование MAVProxy (Python) для командного управления дронами удаленно.
- **Ключевое:** Использование асинхронного планировщика задач для жесткого реального времени.

## Пример команды через MAVProxy
```bash
# Взлет дрона на 10 метров (автоматически)
takeoff 10

# Движение к точке (latitude, longitude)
guided 55.7558 37.6173
```

## Связанные Репозитории
- [[ARDUINO-FOC]] — низкоуровневое управление моторами
- [[ARGON-DESIGN-SYSTEM]] — управление графической телеметрией
- [[ARIEL-OS]] — ОС на Rust для IoT
- [[CHIPSEC]] — безопасность железа
