---
tags: [nexus-vault, privacy, frontend, osint, open-source, web-apps, self-hosted, bypassing-tracking, decentralization, search-engines]
category: Privacy / Communication
language: Markdown
github: https://github.com/digitalblossom/alternative-frontends
---

# ALTERNATIVE-FRONTENDS — Реестр Приватных Фронтендов для Популярных Cepвисов

## Описание
Этот репозиторий представляет собой исчерпывающий список альтернативных, ориентированных на приватность фронтендов для таких гигантов, как YouTube, Twitter, Reddit, Instagram и др. Все представленные проекты являются кроссплатформенными веб-приложениями, которые блокируют отслеживание, рекламу и часто не требуют JavaScript на стороне клиента.

## Ключевые Проекты в Списке
1. **YouTube** — Invidious (легковесный, без JS), Piped (с поддержкой 4K и SponsorBlock).
2. **Twitter** — Nitter (минималистичный, поддержка RSS).
3. **Reddit** — Teddit (без рекламы и JS), Libreddit (быстрый, проксирование всех запросов).
4. **Search Engines** — Whoogle (Google без кук), SearX/SearXNG (метапоиск по 70+ источникам).
5. **Wikipedia** — Wikiless (доступ в странах с цензурой).
6. **Translation** — Lingva (Google Translate без слежки), SimplyTranslate.

## Почему это Killer-App
- **Privacy First** — позволяет пользоваться привычными сервисами, не отдавая данные рекламным сетям.
- **Performance** — альтернативные фронтенды значительно быстрее оригиналов из-за отсутствия тяжелых скриптов.
- **Self-Hostable** — большинство проектов можно развернуть на своем сервере (YunoHost, Docker).
- **Decentralized Options** — поддержка Onion (Tor), I2P и Loki для максимальной анонимности.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Privacy-Preserving Proxy — стандарт для NEXUS-агентов при сборе OSINT-данных без раскрытия IP-адреса и отпечатков системы.
- **Интеграция:** Автоматическое перенаправление всех запросов к соцсетям через инструменты типа `LibRedirect`, интегрированные в NEXUS Browser.
- **Ключевое:** Использование `Whoogle` и `SearXNG` в качестве основных поисковых движков для NEXUS-ядра.

## Инструменты Автоматизации
- **Farside:** Авто-редирект на рабочие инстансы фронтендов.
- **UntrackMe:** Android-приложение для очистки ссылок от трекинговых параметров.
- **LibRedirect:** Браузерное расширение для автоматического переключения на альтернативы.

## Связанные Репозитории
- [[INVIDIOUS]] — ядро приватного YouTube
- [[NITTER]] — ядро приватного Twitter
- [[SEARXNG]] — фундаментальный метапоиск
- [[WHOOGLE-SEARCH]] — чистый поиск Google
