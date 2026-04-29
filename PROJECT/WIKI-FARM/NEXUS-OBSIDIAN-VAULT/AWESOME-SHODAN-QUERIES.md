---
tags: [nexus-vault, security, shodan, osint, reconnaissance, queries]
category: Security / OSINT
language: Markdown / DSL
github: https://github.com/jakejarvis/awesome-shodan-queries
---

# AWESOME-SHODAN-QUERIES — Shodan OSINT Master List

## Описание
**Awesome Shodan Queries** — это крупнейшая коллекция проверенных поисковых запросов для поисковика **Shodan**. Список охватывает всё: от незащищенных баз данных и вебкамер до критической инфраструктуры (электростанции, котельные, системы управления светофорами), которые случайно оказались в открытом интернете.

## Что можно найти (Категории)
1. **IoT Devices**— Wi-Fi роутеры, смарт-холодильники, принтеры (часто с дефолтными паролями).
2. **Infrastructure**— Системы ICS/SCADA, контроллеры Modbus, BACnet (управление зданиями).
3. **Databases**— MongoDB, Elasticsearch, Redis без авторизации.
4. **Vulnerabilities**— Хосты, отвечающие на CVE-запросы (напр. BlueKeep, Heartbleed).
5. **Video Surveillance**— RTSP-потоки камер, видеорегистраторы (DVR).

## Архитектурная Ценность для NEXUS
- **Паттерн:** Автоматизированная Разведка (Reconnaissance-as-a-Code). Это "топливо" для OSINT-агентов NEXUS.
- **Интеграция:** Модуль NEXUS Recon — автоматический прогон этих запросов через Shodan API для поиска целей.
- **Ключевое:** Позволяет за секунды оценить поверхность атаки или защищенность периметра организации.

## Топ-3 Примера Запросов
```bash
# 1. Поиск открытых баз данных MongoDB
"MongoDB Server Information" port:27017 -authentication

# 2. Поиск веб-камер с заголовком "Server: Camera"
"Server: SQ-WEBCAM" port:80

# 3. Индустриальные системы (Modbus)
port:502 "unit id"
```

## Связанные Репозитории
- [[AUTOSPLOIT]] — автоматизация эксплуатации по результатам Shodan
- [[CAMERADAR]] — взлом найденных RTSP-потоков
- [[ATTACKSURFACEANALYZER]] — анализ поверхности атаки
- [[AWESOME-SHODAN-QUERIES]] — база и пример в одном
- [[DNA-FARM]] — где мы изыскали эти данные
