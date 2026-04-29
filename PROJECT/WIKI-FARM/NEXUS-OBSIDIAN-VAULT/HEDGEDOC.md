---
tags: [nexus-vault, collaboration, markdown, hedgedoc, realtime, team-editor]
category: Collaboration / Document Real-time Editor (Open Source)
language: JavaScript / Node.js
github: https://github.com/hedgedoc/hedgedoc
---

# HEDGEDOC — Collaborative Markdown Editor (Real-time)

## Описание
**HedgeDoc** (ранее CodiMD) — это платформа с открытым исходным кодом для совместной работы над документами в формате **Markdown** в режиме реального времени. Это "Google Docs для разработчиков", где вы и ваши агенты (или коллеги) можете одновременно писать отчеты, фиксировать идеи и проектировать архитектуру, видя изменения друг друга мгновенно. HedgeDoc поддерживает вставку диаграмм (Mermaid, Graphviz), формулы LaTeX и имеет режим презентации.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Backend | Node.js / Express |
| Frontend | React / Bootstrap |
| Database | PostgreSQL / MySQL / SQLite |
| Protocol | WebSockets (Socket.io) for real-time Sync |
| Auth | LDAP, OAuth2 (GitHub, Google), SAML |

## Почему это Killer-App
1. **Zero-Lag Collaboration**— Видно курсор каждого участника и его правки в реальном времени.
2. **Rich Visuals**— Поддержка `mermaid` диаграмм прямо внутри текста (идеально для [[FORCE-DIRECTED-GRAPH]] описаний).
3. **Presentation Mode**— Любой Markdown-файл превращается в слайд-шоу одной кнопкой (через Reveal.js).
4. **History & Versions**— Полная история изменений с возможностью отката (Snapshot-система).
5. **No Data Lock-in**— Все документы хранятся в чистом Markdown, их легко экспортировать и перенести в ваш [[OBSIDIAN]].

## Архитектурная Ценность для NEXUS
- **Паттерн:** Совместный Операционный Журнал (Shared Ops Log). Место, где вы и ИИ-агенты вместе пишете "Военный дневник" операции.
- **Интеграция:** Модуль NEXUS Collab Lab — автоматическое создание документов в HedgeDoc по результатам OSINT-разведки для "живого" обсуждения.
- [[AGENTS]] -> [[HEDGEDOC]] -> [[OBSIDIAN]] поток знаний.

## Топ-3 Примера использования
- **Live Tech Specs**— Проектирование API вместе с командой.
- **Incident Response**— Коллективное ведение логов взлома или защиты в реальном времени.
- **Daily Scrums**— Быстрая фиксация задач (TODO) всей сети агентов.

## Связанные Репозитории
- [[OBSIDIAN]] — финальное хранилище знаний после HedgeDoc
- [[NEXTJS]] / [[NODEJS]] — база для фронтенда и бекенда
- [[D3]] / [[FORCE-DIRECTED-GRAPH]] — визуализация через Mermaid внутри
- [[ANYTHING-LLM]] — если ИИ пишет прямо в HedgeDoc
- [[GRAFANA]] — мониторинг нагрузки на сервер совместной работы
- [[DNA-FARM]] — источник наших данных (репозиториев)
- [[DEEPSEARCH]] — если в документах нужен ИИ-поиск
- [[CRAWL4AI]] — сборщик данных (топливо для отчетов)
- [[ETHICAL-HACKING-NOTES]] — ведение заметок во время пентеста
- [[ALLUXIO]] — кэширование данных
- [[ASTRO]] — создание фронтенда
- [[ELECTRON]] — десктопное приложение для доступа к HedgeDoc
- [[FFMPEG]] — если нужно вставлять видео-превью в документы
- [[FACE-RECOGNITION]] — если отчеты связаны с людьми
- [[FASTCHAT]] / [[FASTAPI]] — API управления документами
- [[ESP32]] — (неприменимо)
- [[FAIRY-DOCKER]] — если нужно упаковать HedgeDoc в контейнер
- [[GIN]] — скоростной веб-шлюз
- [[GPG]] / [[CRYPTOGRAPHY]] — подпись документов (Content Trust)
- [[HA-PROXY]] — нагрузка на кластер совместной работы
- [[GARDEN]] — разработка в облаке
- [[XLM]] / [[GENSIM]] — перевод документов на лету
- [[GBDT]] — (неприменимо)
- [[HASHCAT]] — (неприменимо)
- [[HELM]] / [[KUBERNETES]] — деплой HedgeDoc в облако
- [[HTOP]] — мониторинг ресурсов сервера
- [[HARBOR]] — реестр для образов HedgeDoc
- [[INTERNAL-DOCUMENTATION]] — главная папка для этих файлов
