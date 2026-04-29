---
tags: [nexus-vault, system-admin, troubleshooting, debugging, maintenance, reliability, disaster-recovery]
category: Operations / Universal Troubleshooting & Debugging Guide (The Repair Manual)
language: Language Agnostic / Linux Shell / Python / SQL
github: https://github.com/nno-tech/awesome-troubleshooting (Master List) / https://github.com/fatedier/frp (Fast Reverse Proxy - Debug Tool)
---

# TROUBLESHOOTING — The Universal Guide to Problem Solving & System Recovery

## Описание
**Troubleshooting** — это не просто поиск ошибок, это системная дисциплина о том, как за минимальное время вернуть систему NEXUS к жизни после любого сбоя. В мире, где работают 1400+ ИИ-агентов, микросервисы и облачные базы данных, ошибки неизбежны. Этот раздел Wiki является вашим "Финальным Инструктажем": он учит отделять симптомы от причин, использовать инструменты мониторинга [[GRAFANA]] и логи [[KIBANA]], чтобы любая проблема — от падения сети [[NATS]] до ошибки в [[PYTHON]] коде — была исправлена за считанные минуты.

## Технический Стек (The Debugging Arsenal)
| Слой сбоя | Основные инструменты | Что проверяем? |
|-----------|----------------------|----------------|
| **Infrastructure** | [[HTOP]], [[DOCKER]], `systemctl`, `journalctl` | CPU/RAM/Disk, падение контейнеров, статусы служб |
| **Networking** | `ping`, `curl`, `dig`, `tcpdump`, [[NMAP]] | Состояние портов, DNS, задержки (Latency), Firewall |
| **Application** | [[SENTRY]], [[PYLINT]], `strace`, `gdb`, Chrome DevTools | Ошибки в логике, утечки памяти, зависания потоков |
| **Database** | `EXPLAIN ANALYZE`, [[REDIS]] `monitor`, [[POSTGRESQL]] logs | Медленные запросы [[SQL]], блокировки таблиц |
| **AI / NLP** | [[LANGCHAIN]] logs, [[OLLAMA]] logs | Галлюцинации моделей, неверные промпты, VRAM OOM (Out Of Memory) |

## Почему это Killer-App
1. **Critical Thinking Mastery**— Учит алгоритмическому поиску: "Если а) не работает, проверьте б), если б) работает — проблема в в)". Это исключает панику и хаос.
2. **Root Cause Analysis (RCA) Power**— Вы находите не "почему программа упала", а "какой именно байт вызвал это падение неделю назад", предотвращая повторение проблемы навсегда.
3. **Advanced Log Mastery**— Умение читать между строк в гигабайтах логов [[ELASTICSEARCH]], мгновенно выхватывая ключевую ошибку.
4. **Resiliency Design Mastery**— Хороший траблшутинг учит вас строить системы, которые сами исправляют свои ошибки (Self-healing via [[KUBERNETES]]).
5. **Universal Repair Manual Power**— Подходит для всего: от ремонта серверного железа до исправления сложной юридической логики в автоматизациях.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Протокол Самоисцеления (The Self-Healing Protocol). Набор инструкций для ИИ-агентов, как им чинить самих себя при обнаружении сбоя в [[SENTRY]].
- **Интеграция:** Модуль NEXUS Sentry — автоматизация исправления: если [[NATS]] шина перегружена, система сама перезапускает ноды.
- [[CRASH DETECTED]] -> [[TROUBLESHOOTING LOGIC]] -> [[SYSTEM RESTORED]] стабильность.

## Золотые правила Траблшутинга (Greeks Style)
- **Rule #1: Is it plugged in?** (Проверь самое простое — сеть, питание, API-ключи).
- **Rule #2: Binary Search.** (Отключай половины системы, чтобы сузить круг поиска виновника).
- **Rule #3: Change one thing at a time.** (Никогда не меняй две настройки сразу — ты не поймешь, что именно помогло).
- **Rule #4: Logs don't lie.** (Верь только фактам в файлах, а не предположениям).

## Связанные Репозитории (The Recovery Grid)
- [[SENTRY]] — главный источник уведомлений о проблемах
- [[GRAFANA]] / [[PROMETHEUS]] — визуализация "симптомов" на графиках
- [[KIBANA]] — глубокий поиск "улик" в логах
- [[HTOP]] — первичный осмотр "здоровья" процессоров
- [[DNA-FARM]] — источник наших данных (репозиториев) — где может быть ошибка
- [[DEEPSEARCH]] — если для поиска решения нужен ИИ-поиск
- [[ANYTHING-LLM]] — поиск в Obsidian решений прошлых проблем
- [[CRAWL4AI]] — сборщик данных (топливо для разведки сбоев)
- [[ETHICAL-HACKING-NOTES]] — если сбой вызван атакой взломщиков
- [[ALLUXIO]] — (неприменимо напрямую)
- [[ASTRO]] / [[NEXTJS]] — современные фронтенды для отладки UI (DevTools)
- [[ELECTRON]] — десктопное приложение для мониторинга и ремонта
- [[FFMPEG]] — если сбой в обработке видео
- [[FACE-RECOGNITION]] — (неприменимо напрямую)
- [[FASTCHAT]] / [[FASTAPI]] — API управления (отладка через Swagger/Redoc)
- [[ESP32]] — (неприменимо напрямую)
- [[FAIRY-DOCKER]] — отладка через `docker logs / inspect`
- [[GIN]] — скоростной веб-шлюз
- [[GPG]] — (неприменимо напрямую)
- [[HA-PROXY]] — если проблема в балансировке трафика
- [[GARDEN]] — разработка в облаке
- [[XLM]] / [[GENSIM]] — перевод текстов ошибок (i18n)
- [[GBDT]] — предиктивный анализ сбоев (до их появления)
- [[HASHCAT]] — (неприменимо напрямую)
- [[HELM]] / [[KUBERNETES]] — отладка кластера: `kubectl logs / describe`
- [[HTOP]] — (повторно)
- [[HARBOR]] — если проблема в образах контейнеров
- [[HEDGEDOC]] — документация инцидентов (Post-mortem)
- [[INTERPRETABLE-ML]] — объяснение ошибок ИИ
- [[D3]] / [[FORCE-DIRECTED-GRAPH]] — визуализация графа зависимостей сбоя
- [[IMAGE-PROCESSING]] — (неприменимо напрямую)
- [[IMAGES-PYTHON]] — рисование графиков частоты сбоев
- [[INFRASTRUCTURE]] — как всё связано (Мастер-чертеж)
- [[IP-ADDR]] — чистая работа с IP (Field type "string")
- [[IP-RECON]] — разведка IP источников атак
- [[JAVA]] — (JVM Troubleshooting: JStack, JMap)
- [[JAVASCRIPT-ALGORITHMS]] — ИИ на JS (в браузере)
- [[JENKINS]] — отладка пайплайнов деплоя
- [[JINJA2]] — (неприменимо напрямую)
- [[JOB-INTEL]] — OSINT бот по вакансиям SRE/Troubleshooting Engineers
- [[JUPYTER]] — лаборатория анализа (использование Python для разбора логов)
- [[KIBANA]] — мастер-поиск по логам
- [[KIND]] — запуск локального кластера
- [[KUBERNETES]] — фундамент (повторно)
- [[LANGCHAIN]] — (отладка цепочек агентов через LangSmith)
- [[LEARN-LINUX]] — ОС для запуска инструментов ремонта
- [[MASTER-PLAN]] — архитектурная основа (Инфраструктура)
- [[ZEN]] — спокойствие админа (Система восстановлена)
- [[POSTGRESQL]] — (Explain Analyze SQL queries)
- [[REDIS]] — (Slowlog команды)
- [[NGINX]] — (Error logs анализ)
- [[UML]] — рисование схем сбоев
- [[STRACE]] — отладка системных вызовов в Linux
- [[TCPDUMP]] — перехват сетевых пакетов для анализа ("Слушайте провода")
- [[LSOF]] — "кто открыл этот файл/порт?"
- [[NETSTAT]] / [[SS]] — анализ сетевых соединений
