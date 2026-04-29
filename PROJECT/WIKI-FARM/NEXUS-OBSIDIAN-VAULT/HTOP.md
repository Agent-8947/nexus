---
tags: [nexus-vault, monitoring, linux, htop, process-manager, system-resources]
category: Infrastructure / System Monitoring (Real-time)
language: C (htop) / Python (htop-python)
github: https://github.com/htop-dev/htop / https://github.com/hmathew/htop-python
---

# HTOP — Interactive System-Monitor & Process Manager

## Описание
**htop** — это интерактивный кроссплатформенный монитор процессов для командной строки. В отличие от стандартного `top`, он предоставляет интуитивно понятное, цветное и динамичное отображение загрузки ресурсов системы: процессора (поядерно), оперативной памяти, swap-файла и списка всех запущенных процессов. Это главный инструмент любого системного администратора для быстрой диагностики "здоровья" сервера.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Core Engine | C (ncurses-based interface) |
| Metrics | CPU Load, RAM/Swap, Uptime, Load Average |
| Interaction | Keyboard shortcuts (F1-F10), Mouse support |
| Extensions | htop-python (Python wrapper for metrics) |
| Platforms | Linux, macOS, FreeBSD, Windows (via WSL/msys2) |

## Почему это Killer-App
1. **Visual Clarity**— Вы мгновенно видите "горячие" процессы, которые потребляют 100% CPU или утекают по памяти.
2. **Easy Kill**— Позволяет отправить сигнал процессу (SIGKILL, SIGTERM) парой нажатий клавиш без запоминания PID.
3. **Filtering & Search**— Можно быстро отфильтровать список процессов (напр. только `nexus_agent` или `python`) и проследить за их деревом зависимостей.
4. **Tree View**— Режим дерева позволяет увидеть, какой процесс породил какой (напр. `Nginx` -> `Workers`).
5. **Customizable**— Настройка верхней панели мониторинга под свои нужды (добавление температур, частот CPU или сетевого трафика).

## Архитектурная Ценность для NEXUS
- **Паттерн:** Оперативная Диагностика Ресурсов (Resource Health Check). Позволяет быстро понять, почему ферма Obsidian начала тормозить.
- **Интеграция:** Модуль NEXUS Self-Monitor — использование `htop-python` для автоматического сбора данных о нагрузке и отправки их в [[GRAFANA]].
- [[HTOP]] -> [[DASHBOARD]] мгновенный статус сервера.

## Пример использования (CLI)
```bash
# 1. Запуск htop (стандарт)
htop

# 2. Фильтрация процессов в командной строке
htop --filter=python

# 3. Сортировка по потреблению памяти сразу при запуске
htop --sort-key=PERCENT_MEM
```

## Связанные Репозитории
- [[GRAFANA]] — долгосрочная визуализация этих метрик
- [[PROMETHEUS]] — сборщик этих метрик для Grafana
- [[ALLUXIO]] — если метрики показывают нехватку дисковой скорости
- [[DNA-FARM]] — источник наших данных (репозиториев), нагружающих систему
- [[DEEPSEARCH]] — если поиск нагружает CPU (что видно в htop)
- [[ANYTHING-LLM]] — мониторинг нагрузки при работе ИИ
- [[CRAWL4AI]] — мониторинг ресурсов при скрапинге
- [[ETHICAL-HACKING-NOTES]] — поиск скрытных процессов (Rootkits) через htop
- [[BUN]] / [[NODE-JS]] — мониторинг утечек памяти в JS-сервисах
- [[ELECTRON]] — мониторинг "тяжелых" окон приложения
- [[FFMPEG]] — мониторинг нагрузки при кодировании видео
- [[FACE-RECOGNITION]] — мониторинг GPU/CPU при распознавании
- [[FASTCHAT]] / [[FASTAPI]] — мониторинг нагрузки на API-шлюз
- [[ESP32]] — (неприменимо напрямую, но ESP шлет свои метрики)
- [[FAIRY-DOCKER]] — мониторинг ресурсов внутри контейнеров
- [[HELM]] / [[KUBERNETES]] — мониторинг всего кластера (через `htop` на нодах)
- [[HUGGINGFACE-TRANSFORMERS]] — мониторинг VRAM при загрузке тяжелых моделей
