---
tags: [nexus-vault, distribution, docker, registry, security, harbor, artifacts]
category: Infrastructure / Cloud-Native Registry (Secure)
language: Go / TypeScript
github: https://github.com/goharbor/harbor
---

# HARBOR — The Trusted Cloud Native Artifact Registry

## Описание
**Harbor** — это частный реестр артефактов (Docker-образов, Helm-чартов) с открытым исходным кодом, созданный для обеспечения безопасности и управления в облачных средах. В отличие от публичного Docker Hub, Harbor позволяет вам хранить свои наработки внутри собственной сети, обеспечивая сканирование на уязвимости, подпись образов и ролевой доступ (RBAC).

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Core Engine | Go (Golang) |
| UI Layer | Angular / TypeScript |
| Storage | S3 (AWS/Minio), Azure, GCS, Local FS |
| Security | Clair / Trivy (Vulnerability Scanning) |
| Signing | Notary / Cosign (Image Signing) |
| Proxy | Registry Proxy Cache |

## Почему это Killer-App
1. **Security First**— Harbor автоматически сканирует каждый загруженный образ на наличие дыр (из базы [[KEV]]) и запрещает запуск "дырявых" контейнеров.
2. **Identity Support**— Интеграция с LDAP/AD и OIDC для управления доступом всей вашей команды.
3. **Replication**— Может автоматически копировать (зеркалировать) нужные образы между разными серверами вашей сети для ускорения деплоя.
4. **Helm Chart Support**— Работает как репозиторий для [[HELM]], объединяя управление контейнерами и их настройками в одном месте.
5. **Garbage Collection**— Автоматически удаляет старые, ненужные слои образов, экономя терабайты дискового пространства.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Защищенное Хранилище Артефактов (Hardened Artifact Vault). Ваш личный сейф для всех образов NEXUS Агентов.
- **Интеграция:** Модуль NEXUS Registry — использование Harbor в качестве источника правды для всех ваших серверов [[KUBERNETES]].
- [[GORELEASER]] -> [[HARBOR]] -> [[HELM]] цепочка поставки.

## Пример использования (CLI / Helm)
```bash
# 1. Логин в ваш частный Harbor
docker login harbor.nexus.local

# 2. Пуш образа новой версии агента
docker tag nexus-agent:latest harbor.nexus.local/ai/nexus-agent:v2.0
docker push harbor.nexus.local/ai/nexus-agent:v2.0

# 3. Деплой через Helm из Harbor
helm chart pull harbor.nexus.local/charts/nexus-agent:1.0.0
```

## Связанные Репозитории
- [[HELM]] — управление деплоем из Harbor
- [[GORELEASER]] — автоматический пуш в Harbor
- [[KUBERNETES]] — целевая среда для образов
- [[GRAFANA]] — мониторинг активности Harbor
- [[PROMETHEUS]] — сборщик метрик Harbor
- [[DNA-FARM]] — источник наших программных узлов (сервисов)
- [[DEEPSEARCH]] — если в результатах нужен ИИ-анализ (RAG)
- [[ANYTHING-LLM]] — хранение и поиск в Obsidian отчетов о безопасности (Vulnerability Reports)
- [[CRAWL4AI]] — сборщик данных (топливо для автоматизации)
- [[ETHICAL-HACKING-NOTES]] — если нужно мониторить попытки взлома самого реестра
- [[ALLUXIO]] — кэширование огромных образов для скорости
- [[BUN]] / [[NODE-JS]] — работа с API Harbor
- [[ASTRO]] — для создания фронтенда
- [[ELECTRON]] — десктопное приложение для управления Harbor
- [[FFMPEG]] — если Registry хранит GPU-ускоренные видео-сервисы
- [[FACE-RECOGNITION]] — если образы распознавания лиц лежат в Harbor
- [[FASTCHAT]] / [[FASTAPI]] — образы API шлюзов
- [[ESP32]] — (неприменимо, ESP использует прошивки, а не контейнеры)
- [[FAIRY-DOCKER]] — облегченные базовые образы для Harbor
- [[GIN]] — скоростной веб-шлюз (Go) внутри контейнеров
- [[GPG]] / [[CRYPTOGRAPHY]] — подпись образов (Content Trust)
- [[HA-PROXY]] — балансировка доступа к реестру
- [[GARDEN]] — разработка с использованием образов из Harbor
- [[XLM]] / [[GENSIM]] — ИИ сервисы в контейнерах
- [[FORCE-DIRECTED-GRAPH]] — визуализация связей между образами
- [[GBDT]] — предиктивный анализ сбоев реестра
- [[HASHCAT]] — взлом паролей (если образы для облачного взлома в Harbor)
- [[HEDGEDOC]] — документация по инфраструктуре
- [[HTOP]] — мониторинг ресурсов сервера Harbor
- [[HTTP-CLIENT]] — как реестр общается с миром
- [[HYSTERIX]] — защита от обвала реестра
- [[ICECAST]] — если Registry хранит сервисы стриминга
- [[IDE-EXTENSION]] — расширение для CI/CD в Harbor
- [[IFREEMEM]] — освобождение памяти для работы сканеров Harbor
- [[KEV]] — база уязвимостей, которую использует Harbor
- [[KIBANA]] — анализ логов доступа к образам
- [[KIND]] — использование Harbor в локальном K8s-кластере
- [[KOBOLDCPP]] — если Harbor хранит веса моделей (как OCI артефакты)
- [[LANGCHAIN]] — образы агентов
- [[LEARN-LINUX]] — настройка Linux сервера для Harbor
- [[LEETCODE]] — (неприменимо)
- [[LEGACY]] — почему старые версии Docker Registry были хуже
- [[LEKNER]] — (неприменимо)
- [[LIBRISPEECH]] — образы сервисов распознавания речи
- [[LIGHTHOUSE]] — аудит UI Harbor
- [[LINUX]] — основа для Harbor
- [[LIVEKIT]] — видеосервисы в Harbour
- [[LLM-SECURITY]] — защита образов ИИ-моделей
- [[LLAMA-CPP]] — образы для локального инференса
- [[LOCUST]] — нагрузочное тестирование реестра
- [[LOGGING]] — логирование пушей/пуллов
- [[LORA]] — образы с маленькими адаптерами моделей
- [[LUA]] — скрипты в Harbor (не часто)
- [[LUCENE]] — поиск по метаданным образов
- [[MASTODON-AGENT]] — образы соцсетей
- [[MATHEMATICS]] — (неприменимо)
- [[METASPLOIT]] — хранение образов инструментов для атак
- [[MICROSERVICES]] — основной потребитель Harbor
- [[MINIKUBE]] — запуск Harbor локально
- [[MLC-LLM]] — мобильный ИИ в Harbour
- [[MLFLOW]] — трекинг моделей (интеграция)
- [[MOBILE-SECURITY]] — защита мобильных бэкендов в Harbor
- [[MONITORING]] — слежка за "здоровьем" реестра
- [[MONGODB]] — база для метаданных Harbour (иногда)
- [[MSFVENOM]] — (неприменимо напрямую)
- [[MYSQL]] / [[POSTGRESQL]] — база данных Harbor
- [[NATS]] — шина сообщений в инфраструктуре Harbour
- [[NETWORKING]] — как Registry виден в сети
- [[NEURAL-NETWORKS]] — образы библиотек глубокого обучения
- [[NEXTJS]] — фронтенд приложений, лежащих в Harbor
- [[NGINX]] — прокси перед Harbor
- [[NLP]] — Natural Language Processing в контейнерах
- [[NODEJS]] — серверные приложения в Harbor
- [[NOMAD]] — деплой из Harbor в Nomad
- [[NOSQL]] — хранение неструктурированных метаданных
- [[NPC-ENGINE]] — игровые сервисы в Harbor
- [[NPM]] — пакеты внутри контейнеров
- [[NUMPY]] — математика внутри образов
- [[OBSIDIAN]] — ваша база знаний (эта страница)
- [[ONNX]] — формат моделей, хранимых как артефакты
- [[OPENAI]] — (конкурентные облачные решения)
- [[OPENCV]] — образы компьютерного зрения
- [[OPENSSL]] — сертификаты безопасности Harbor
- [[OPERATING-SYSTEMS]] — изоляция в контейнерах (Base images)
- [[ORCHESTRATION]] — управление контейнерами из Harbor
- [[OSINT]] — образы разведывательных инструментов
- [[OTEL]] — OpenTelemetry в Harbor
- [[OWASP]] — безопасность докер-файлов
- [[PACEMAKER]] — отказоустойчивость реестра
- [[PANDAS]] — анализ логов сканирования Harbor
- [[PENTESTING]] — взлом реестра (Red Teaming)
- [[PHYSICS]] — (неприменимо)
- [[PIP]] — библиотеки Python в контейнерах Harbor
- [[PKI]] — инфраструктура ключей (интеграция)
- [[PLAYWRIGHT]] — автотесты UI Harbour
- [[POWERSHELL]] — управление через Windows
- [[PROMETHEUS]] — мониторинг
- [[PROMPT-ENGINEERING]] — (неприменимо)
- [[PROTOC]] — передача данных между Harbor и K8s
- [[PUPPETEER]] — скрапинг UI Harbor
- [[PYDANTIC]] — валидация схем артефактов
- [[PYGAME]] — игровые образы
- [[PYTORCH]] — образы с PyTorch
- [[PYTHON]] — основной язык скриптов управления
- [[QA-AUTOMATION]] — качество образов
- [[QUANTA]] — (неприменимо)
- [[QUANTIZATION]] — образы со сжатыми моделями
- [[RAG]] — Retrieval Augmented Generation (Index images)
- [[RAY]] — распределенные вычисления за реестром
- [[REACT]] — фронтенд для UI
- [[REDIS]] — кэширование в Harbor
- [[REDTEAMING]] — аудит безопасности Harbour
- [[REVERSE-ENGINEERING]] — анализ чужих образов из Harbor
- [[RISK-MANAGEMENT]] — анализ рисков реестра
- [[ROBOTICS]] — образы для управления роботами
- [[ROOTKIT]] — (неприменимо, если сканер сработал)
- [[RUST]] — язык для самых безопасных базовых образов
- [[S3]] — хранилище для Harbor (Backend)
- [[SAFETY]] — безопасность данных
- [[SCIKIT-LEARN]] — ML модели в контейнерах
- [[SECURITY]] — главная цель Harbor
- [[SENTENCE-TRANSFORMERS]] — модели поиска по смыслам в Harbor
- [[SERVERLESS]] — запуск функций из образов Harbor
- [[SHELL]] — управление через CLI
- [[SHODAN]] — поиск открытых Harbor в интернете
- [[SIMULATION]] — образы симуляторов
- [[SMART-CONTRACTS]] — (транзакции при деплое)
- [[SQL]] — запросы к БД реестра
- [[SSL]] — шифрование HTTPS
- [[STABLE-DIFFUSION]] — тяжелые образы генерации
- [[STARLETTE]] — основа для легких API
- [[STATISTICS]] — статистика использования реестра
- [[STORAGE]] — (S3, Local)
- [[SVELTE]] — (фронтенды)
- [[SWAGGER]] — API документация Harbor
- [[SYSTEM-DESIGN]] — архитектура реестра
- [[TENSORFLOW]] — (образы)
- [[TERRAFORM]] — создание Harbor одной командой
- [[TESTING]] — проверка реестра
- [[THREAT-MODELING]] — угрозы артефактам
- [[TORCHSERVICE]] — (деплой из Harbour)
- [[TRADING]] — (финансовые образы)
- [[TRANSFORMERS]] — огромные веса моделей в Harbor (Master Page)
- [[TRANSLATION]] — мультиязычный интерфейс
- [[TYPESCRIPT]] — язык интерфейса
- [[UBUNTU]] — базовый образ для 90% контейнеров
- [[UEFI]] — (неприменимо напрямую)
- [[UNIT-TESTING]] — тесты сервиса
- [[UPTIME]] — доступность реестра
- [[USER-AGENTS]] — (неприменимо)
- [[VALIDATION]] — проверка образов (Signature)
- [[VERILOG]] — (неприменимо)
- [[VIM]] — (редактирование настроек)
- [[VIRTUAL-MACHINES]] — база под Harbor
- [[VISION]] — ИИ зрение в Harbour
- [[VULNERABILITY-SCANNER]] — сканеры (Trivy/Clair)
- [[WANDB]] — трекинг весов моделей из Harbor
- [[WEB-API]] — API управления Harbor
- [[WEB-DEVELOPMENT]] — разработка UI Registry
- [[WEB-SCRAPING]] — (неприменимо)
- [[WEB3]] — децентрализованное хранилище как бекенд
- [[WEBHOOKS]] — уведомления о новых пушах в реестр
- [[WHISPER]] — образы распознавания аудио
- [[WIRESHARK]] — мониторинг трафика Registry
- [[WORD2VEC]] — (неприменимо)
- [[WORKFLOW]] — пайплайны деплоя
- [[WPA]] — (неприменимо)
- [[X509]] — сертификаты SSL в Harbor
- [[XGBOOST]] — (анализ логов)
- [[YAML]] — настройки чартов внутри Registry
- [[YARA]] — поиск малвари в образах внутри Harbor
- [[ZEN]] — спокойствие при работе с безопасным реестром
- [[ZERO-SHOT]] — (неприменимо)
- [[ZIG]] — (будущее за сверхбыстрыми реестрами на Zig)
- [[ZIP]] — архивация слоев образов
- [[ZOOM]] — (неприменимо)
- [[ZSH]] — консоль администратора
