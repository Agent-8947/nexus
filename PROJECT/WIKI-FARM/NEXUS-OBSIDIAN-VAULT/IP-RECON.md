---
tags: [nexus-vault, security, network, osint, scanning, recon, infrastructure]
category: OSINT / Network Reconnaissance (Advanced IP Analysis)
language: Python / Bash / Go
github: https://github.com/v1s10n-1/IP-Recon (or equivalent IP Recon tool)
---

# IP-RECON — Advanced Network Reconnaissance & Target OSINT

## Описание
**IP-Recon** — это класс инструментов и методологий для глубокой **сетевой разведки (Reconnaissance)** инфраструктуры цели по её IP-адресу или доменному имени. Это не просто "пинг", а комплексный анализ: обнаружение открытых портов, определение операционной системы (OS Fingerprinting), поиск привязанных доменов и поддоменов, а также выявление географического положения серверов. Это первый и самый важный этап любого OSINT-исследования или тестирования на проникновение.

## Технический Стек (Recon Stack)
| Компонент | Технология |
|-----------|------------|
| Scanner | Nmap, Masscan, ZMap |
| Enumeration | Subfinder, Amass, Assetfinder |
| OSINT API | Shodan, Censys, SecurityTrails, VirusTotal |
| Analysis | Python (Scapy, Requests), Go (Net-package) |
| Visualization | [[GRAFANA]], [[FORCE-DIRECTED-GRAPH]] |

## Почему это Killer-App
1. **Target Visibility**— Вы видите не просто "сайт", а всю серверную мощь противника: какие базы данных открыты, какие VPN используются.
2. **Reverse Mapping**— Поиск всех сайтов, "живущих" на одном IP (Shared hosting discovery).
3. **Subdomain Brute-force**— Нахождение скрытых панелей управления (напр. `admin.nexus.local`), которые не индексируются поисковиками.
4. **Whois & ASN Analysis**— Определение владельца сети, провайдера и юридической привязки.
5. **Real-time Monitoring**— Возможность настроить алерты: "На сервере цели открылся новый порт 22 (SSH)".

## Архитектурная Ценность для NEXUS
- **Паттерн:** Постоянное Сканирование Периметра (Continuous Perimeter Scan). Ваши агенты-разведчики живут в этом модуле.
- **Интеграция:** Модуль NEXUS Sentry — автоматическая проверка вашего собственного IP-адреса на наличие "дыр" и утечек данных.
- [[UNKNOWN IP]] -> [[IP-RECON]] -> [[INTEL REPORT]] формирование улик.

## Пример пайплайна (Bash / CLI)
```bash
# 1. Быстрый скан всех портов (Masscan)
masscan -p1-65535 1.2.3.4 --rate=1000

# 2. Детальный анализ найденных портов (Nmap)
nmap -sV -sC -A -p 80,443,8080 1.2.3.4

# 3. Поиск связанных доменов (Shodan API)
shodan host 1.2.3.4
```

## Связанные Репозитории
- [[ETHICAL-HACKING-NOTES]] — методики того, что делать после Recon
- [[GEOLOCATION]] — привязка найденных IP к карте мира
- [[GRAFANA]] — мониторинг открытых портов в реальном времени
- [[ELASTICSEARCH]] — база для хранения результатов сканирования
- [[DNA-FARM]] — источник наших данных (репозиториев)
- [[DEEPSEARCH]] — если в отчетах нужен ИИ-поиск
- [[ANYTHING-LLM]] — хранение и поиск в Obsidian отчетов разведки
- [[CRAWL4AI]] — сборщик данных (топливо для рекона)
- [[ALLUXIO]] — кэширование огромных дампов сканирования
- [[FFMPEG]] — (неприменимо)
- [[FACE-RECOGNITION]] — если IP связан с веб-камерой человека
- [[FASTCHAT]] / [[FASTAPI]] — API управления сканерами
- [[ESP32]] — (неприменимо)
- [[FAIRY-DOCKER]] — запуск сканеров в изолированных контейнерах
- [[GIN]] — скоростной веб-шлюз для результатов рекона
- [[GPG]] / [[CRYPTOGRAPHY]] — шифрование секретных отчето
- [[HA-PROXY]] — если вы сканируете через цепочку прокси
- [[GARDEN]] — разработка сканеров в облаке
- [[XLM]] / [[GENSIM]] — перевод названий сервисов
- [[GBDT]] — предиктивный анализ уязвимости порта
- [[HASHCAT]] — если найден порт с хешами
- [[HELM]] / [[KUBERNETES]] — запуск сканеров в кластере
- [[HTOP]] — мониторинг ресурсов сканирующей ноды
- [[HARBOR]] — реестр для образов сканеров
- [[HEDGEDOC]] — документация по целям
- [[INTERPRETABLE-ML]] — почему IP признан опасным
- [[IMAGE-PROCESSING]] — распознавание скриншотов сайтов на IP
- [[IMAGES-PYTHON]] — рисование топологии сети
- [[IMMLIB]] — низкоуровневая отладка в Windows
- [[INFRASTRUCTURE]] — как всё связано
- [[IP-ADDR]] — чистая работа с IP в коде
- [[BLACK-HAT-RUST]] — наступательная сетевая инженерия
- [[SHODAN]] — глобальный поиск серверов
- [[MASSCAN]] — сверхбыстрый скан портов
- [[NMAP]] — микроскоп сетевого инженера
- [[BEYOND-RECON]] — высшая лига разведки
