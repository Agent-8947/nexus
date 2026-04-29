---
tags: [nexus-vault, security, password, cracking, hashing, pentest, recovery, high-performance]
category: Security / Password Recovery & Hashing (High Performance)
language: C / C++ / OpenCL / CUDA
github: https://github.com/hashcat/hashcat
---

# HASHCAT — The World's Fastest Password Recovery Tool

## Описание
**Hashcat** — это абсолютный мировой лидер среди инструментов для **восстановления (взлома) паролей**. Главная особенность: использование мощи вашей **видеокарты (GPU)** (через OpenCL/CUDA) для перебора миллионов паролей в секунду. Hashcat поддерживает более 350 типов хешей (MD5, SHA, WPA/WPA2, Microsoft Office, ZIP, RAR, PDF), делая его незаменимым инструментом в арсенале любого специалиста по кибербезопасности.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Core Engine | C / C++ (High Performance Kernels) |
| Acceleration | OpenCL, CUDA, Metal (macOS), SYCL |
| Platforms | Linux, Windows, macOS |
| Hash Types | 350+ (MD5, SHA1, SHA256, Bcrypt, Scrypt) |
| Attack Modes | Brute-force, Combinator, Dictionary, Mask, Rule-based |

## Почему это Killer-App
1. **Insane Performance**— Современная GPU (напр. RTX 4090) позволяет Hashcat перебирать сотни миллиардов MD5 хешей в секунду.
2. **Rule-based Attacks**— Мощнейшая система правил (Rules), которые позволяют автоматически преобразовывать слова из словаря (напр. `Password` -> `P@ssw0rd123!`).
3. **Multi-GPU / Cluster**— Можно объединять десятки видеокарт в один гигантский кластер для взлома сверхсложных паролей.
4. **Resumable**— Вы можете остановить перебор в любой момент и продолжить с той же точки через неделю.
5. **Autotune**— Инструмент сам находит оптимальные параметры для вашего железа.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Аудит Криптостойкости (Password Audit & Recovery). Проверка надежности паролей в вашей сети. Если Hashcat взломал его за час — пароль плохой.
- **Интеграция:** Модуль NEXUS Key Cracker — восстановление забытых доступов к зашифрованным архивам или базам данных.
- [[PASSWORD HASH]] -> [[HASHCAT]] -> [[CLEAR TEXT]] востановление доступов.

## Пример запуска (CLI)
```bash
# 1. Взлом MD5 хеша методом перебора маски (все 8 символов строчные)
hashcat -m 0 -a 3 hash.txt ?l?l?l?l?l?l?l?l

# 2. Атака по словарю с применением хитрых правил (Rules)
hashcat -m 1000 -a 0 ntlm_hashes.txt my_dictionary.txt -r best64.rule

# 3. Узнать производительность вашей GPU
hashcat -b
```

## Связанные Репозитории
- [[GPG]] — защита ключей (Hashcat не должен их взломать!)
- [[CRYPTOGRAPHY]] / [[BOTAN]] — создание этих самых хешей
- [[ETHICAL-HACKING-NOTES]] — методики получения доступа к хешам
- [[GRAFANA]] — мониторинг температуры и нагрузки GPU во время взлома
- [[DNA-FARM]] — источник наших данных (репозиториев)
- [[DEEPSEARCH]] — если в отчетах нужен ИИ-поиск
- [[ANYTHING-LLM]] — хранение и поиск в Obsidian отчетов о взломе
- [[CRAWL4AI]] — сборщик словарей паролей из сети (топливо для взлома)
- [[ALLUXIO]] — кэширование огромных файлов словарей
- [[ELECTRON]] — десктопное приложение для управления Hashcat
- [[FFMPEG]] — если нужно извлекать пароли из видео-контейнеров
- [[FACE-RECOGNITION]] — если пароль связан с лицом
- [[ESP32]] — если микроконтроллеры шлют Wi-Fi хеши для взлома
- [[FAIRY-DOCKER]] — если нужно упаковать Hashcat в контейнер
- [[GIN]] — скоростной веб-шлюз для хакерских сервисов
- [[XLM]] / [[GENSIM]] — если пароли основаны на иностранных языках
- [[FORCE-DIRECTED-GRAPH]] — визуализация связей между пользователями и паролями
- [[GBDT]] — если вероятность взлома - это ФИЧА для предсказания уязвимости
- [[ELASTICSEARCH]] — база для хранения слитых паролей
- [[ANYTHING-LLM]] — хранение и поиск в Obsidian отчетов
- [[BLACK-HAT-RUST]] — наступательная инженерия для получения хешей
- [[APPLICATIONINSPECTOR]] — анализ кода софта на предмет дыр в хешировании
- [[CLEAN-CODE-JAVASCRIPT]] — чистота кода
- [[ASTRO]] — для создания фронтенда к Hashcat
- [[DOCS]] — документация по всему вышеперечисленному
- [[FASTCHAT]] / [[FASTAPI]] — если взлом управляет диалогом
- [[ENG-INTERVIEW]] — уметь объяснить структуру криптографии
- [[EMOTION]] / [[CHAKRA-UI]] — интерфейс для хакерского дашборда
- [[GSM-SECURITY]] — взлом паролей в мобильных сетях через Hashcat
- [[HELM]] / [[HARBOR]] — куда деплоятся результаты атак
