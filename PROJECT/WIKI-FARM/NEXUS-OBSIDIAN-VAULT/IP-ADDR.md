---
tags: [nexus-vault, python, ipaddress, networking, cidr, subnetting, validation]
category: Networking / IP Address Manipulation & Logic
language: Python 3.3+ (Standard Library)
github: https://github.com/python/cpython/blob/main/Lib/ipaddress.py (Official Standard)
---

# IP-ADDR — The Science of IP Address Manipulation (Standard Python Lib)

## Описание
**ipaddress** — это стандартная библиотека на языке **Python**, предназначенная для создания, управления и манипулирования IPv4 и IPv6 адресами, а также целыми подсетями (Subnets). Она позволяет программистам работать с IP-адресами не как с "просто строками", а как с полноценными объектами, что предотвращает ошибки при расчете сетевых масок, проверке вхождения хоста в подсеть и переборе всех доступных IP в диапазоне.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Core Engine | Python Standard Library (`import ipaddress`) |
| Types | IPv4Address, IPv6Address, IPv4Network, IPv6Network |
| Logic | CIDR parsing, Binary representation, Overlap checking |
| Validation | Built-in strict mode (Exception on invalid IP) |
| Performance | Optimized C-routines (в современных версиях Python) |

## Почему это Killer-App
1. **Network Calculation**— Одной строчкой кода можно получить широковещательный адрес (Broadcast), адрес сети и количество доступных хостов.
2. **Subnet Overlap Detection**— Библиотека сама скажет, если одна ваша подсеть (напр. `10.0.0.0/24`) пересекается с другой (напр. `10.0.0.0/16`).
3. **CIDR Mastery**— Легкое преобразование диапазонов (напр. `192.168.1.0-192.168.1.255`) в стандартный CIDR формат (`/24`).
4. **Validation**— Мгновенная проверка, является ли строка валидным IP-адресом, и к какой версии (v4/v6) он относится.
5. **Private vs Public**— Встроенные методы для проверки, является ли адрес "частным" (локальным, напр. `192.168.x.x`) или "публичным" в интернете.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Математический Сетевой Движок (Network Engine). Ваши агенты используют его для анализа "карты мишеней" после [[IP-RECON]].
- **Интеграция:** Модуль NEXUS IP Filter — автоматическая фильтрация локальных IP из результатов внешней разведки, чтобы агенты не атаковали "сами себя".
- [[RAW IP STRING]] -> [[IP-ADDR OBJECT]] -> [[NETWORK LOGIC]] обработка.

## Пример кода (Python / ipaddress)
```python
import ipaddress

# 1. Создаем объект подсети (CIDR)
net = ipaddress.ip_network("192.168.1.0/24")

# 2. Узнаем параметры сети
print(f"Mask: {net.netmask}")
print(f"Total hosts: {net.num_addresses - 2}") # (Минус Network & Broadcast)

# 3. Проверка вхождения IP в подсеть
ip = ipaddress.ip_address("192.168.1.100")
if ip in net:
    print("NEXUS: Таргет внутри периметра!")
```

## Связанные Репозитории
- [[IP-RECON]] — разведка IP источников атак
- [[ETHICAL-HACKING-NOTES]] — методики того, что делать после Recon
- [[GEOLOCATION]] — привязка найденных IP к карте мира
- [[GRAFANA]] — мониторинг IP в реальном времени
- [[ELASTICSEARCH]] — база для хранения IP-логов (Mapping: ip_point)
- [[DNA-FARM]] — источник наших данных (репозиториев)
- [[DEEPSEARCH]] — если в отчетах нужен ИИ-поиск по IP
- [[ANYTHING-LLM]] — хранение и поиск в Obsidian отчетов о сетях
- [[CRAWL4AI]] — сборщик данных (топливо для рекона)
- [[ALLUXIO]] — кэширование огромных дампов сканирования
- [[FFMPEG]] — извлечение IP-метаданных из видео-потоков
- [[FACE-RECOGNITION]] — если IP связан с веб-камерой человека
- [[FASTCHAT]] / [[FASTAPI]] — API управления сетевыми фильтрами
- [[FAIRY-DOCKER]] — запуск сетевых служб в контейнерах
- [[GIN]] — скоростной веб-шлюз
- [[GPG]] — защита секретов
- [[HA-PROXY]] — балансировка IP-запросов
- [[GARDEN]] — разработка сканеров в облаке
- [[XLM]] / [[GENSIM]] — перевод названий сервисов
- [[GBDT]] — предиктивный анализ уязвимости IP-диапазона
- [[HASHCAT]] — если найден порт с хешами
- [[HELM]] / [[KUBERNETES]] — запуск сканеров в кластере
- [[HTOP]] — мониторинг ресурсов сканирующей ноды
- [[HARBOR]] — реестр для образов сканеров
- [[HEDGEDOC]] — документация по целям
- [[INTERPRETABLE-ML]] — почему IP признан опасным
- [[IMAGE-PROCESSING]] — распознавание скриншотов сайтов на IP
- [[IMAGES-PYTHON]] — рисование топологии сети
- [[INFRASTRUCTURE]] — как всё связано (Мастер-чертеж)
- [[SHODAN]] — глобальный поиск по IP
- [[NMAP]] — микроскоп сетевого инженера
- [[BEYOND-RECON]] — разведка за пределами IP
- [[ESP32]] — Wi-Fi девайсы с IP в вашей сети
- [[D3]] — визуализация графа связей между IP
- [[DOCS]] — документация по всему вышеперечисленному
- [[DNA-FARM]] — источник наших данных
- [[DRF]] — архитектура API
- [[DRY-PYTHON]] — чистый код (использование ipaddress)
- [[DUPE-DETECTION]] — удаление одинаковых IP логов
- [[EB-INTELLIGENCE]] — анализ поведения в сети
- [[EDGE-AI]] — связь с периферией по IP
- [[ELASTICSEARCH]] — поиск в логах
- [[ELECTRON]] — десктопное приложение для управления сетью
- [[EMBEDDING-MODELS]] — семантический поиск по описаниям сетей
- [[EMOTION]] — стиль для панели управления сетью
- [[ENERGY-FORECASTING]] — предсказание потребления питания серверами
- [[ENG-INTERVIEW]] — уметь говорить с целью
- [[ENHANCEMENT-LLM]] — "умное" расширение сети
- [[ESP32]] — Wi-Fi девайсы
- [[ETHEREUM-PRACTICE]] — децентрализованная инфраструктура
- [[EXCEL-PYTHON]] — экспорт IP реестра в Excel
- [[EXPLAIN-VISUALIZE-ML]] — объяснение работы сети
- [[FAIRY-DOCKER]] — облегченные образы
- [[FASTAPI]] — API управления
- [[FASTCHAT]] — чат-бот для управления
- [[FFMPEG]] — если обрабатываются видео-потоки
- [[FLASK]] — микро-сервисы
- [[FLUTTER]] — мобильное приложение
- [[FORCE-DIRECTED-GRAPH]] — визуализация топологии
- [[FSST]] — сжатие логов в облаке
- [[GARDEN]] — разработка в облаке
- [[GBDT]] — предиктивный анализ сбоев
- [[GENSIM]] — семантический анализ документации
- [[GEOLOCATION]] — мониторинг гео-распределенных IP
- [[GIN]] — входной шлюз для API
- [[GOLANG-ALGORITHMS]] — алгоритмы внутри системы
- [[GPT-API]] — ИИ помощник
- [[GRAFANA]] — мониторинг
- [[GORELEASER]] — выпуск новых версий
- [[GPG]] — подпись конфигураций
- [[GSM-SECURITY]] — взлом паролей в мобильных сетях
- [[GUI-ENGINE]] — создание интерфейса для управления
- [[GUM]] — красивые скрипты для управления
- [[HA-PROXY]] — нагрузка на вдохе
- [[HARBOR]] — реестр образов
- [[HASHCAT]] — взлом в облаке
- [[HEDGEDOC]] — документация
- [[HELM]] — деплой
- [[HTOP]] — мониторинг ресурсов
- [[HYSTERIX]] — защита от обвала
- [[ICECAST]] — вещание аудио
- [[IDE-EXTENSION]] — расширение среды
- [[IP-RECON]] — разведка сети
- [[MASTER-PLAN]] — архитектурная основа
- [[ZEN]] — спокойствие админа
