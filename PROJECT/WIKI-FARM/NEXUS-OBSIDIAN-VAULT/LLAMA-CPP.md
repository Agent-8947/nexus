---
tags: [nexus-vault, ai, models, gguf, local-llm, llamacpp, inference, C++]
category: AI / High-Performance Local Inference (LLM on CPU/GPU Meta)
language: C++ (Core) / Python (Bindings)
github: https://github.com/ggerganov/llama.cpp
---

# LLAMA-CPP — High-Performance Inference of Meta's Llama in C/C++

## Описание
**llama.cpp** — это одно из самых значимых достижений в мире открытого ИИ. Этот проект (созданный Георгием Гергановым) позволил запускать мощнейшие языковые модели (LLM), такие как Llama 3, Mistral, Gemma и Qwen, на обычном потребительском железе: от MacBook Pro до старых ПК с Windows и даже на Raspberry Pi. Это достигается за счет переписывания нейросетей на чистом **С++** с глубокой оптимизацией под современные процессоры (AVX, NEON) и интеграцией с GPU (CUDA, Metal, Vulkan).

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Core Engine | pure C/C++ (no dependencies) |
| Optimization | SIMD (AVX, AVX2, AVX-512), NEON (Apple Silicon) |
| Accelerators | CUDA (NVIDIA), Metal (Apple), ROCm (AMD), Sycl (Intel), Vulkan |
| Data Format | GGUF (Optimized binary format) |
| Quantization | 1.5-bit to 8-bit (K-Quants, IQ-Quants) |
| Bindings | Python, Node.js, Rust, Go, C#, Java |

## Почему это Killer-App
1. **Unrivaled Efficiency**— Позволяет запускать модель весом в 40 Гб на компьютере с 8 Гб памяти за счет квантования (сжатия) без значительной потери "ума".
2. **True Privacy**— Вашему ИИ больше не нужен интернет. Все рассуждения происходят локально, на вашем диске, исключая утечку данных в OpenAI или Google.
3. **Speed of Light**— На процессорах Apple Silicon (M1/M2/M3) скорость генерации текста достигает сотен токенов в секунду, что сравнимо с облачными API.
4. **Server Mode**— Включает в себя легкий веб-сервер, совместимый с API OpenAI, что позволяет подключать к нему любые внешние инструменты (напр. [[LANGCHAIN]]).
5. **Universal Hardware**— Работает везде, где есть компилятор С++, делая ИИ доступным для каждого.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Локальный Когнитивный Якорь (Local Cognitive Anchor). Фундамент вашей независимости от корпоративных облаков.
- **Интеграция:** Модуль NEXUS Local Brain — использование `llama.cpp` через [[OLLAMA]] или напрямую для анализа всех ваших 1400+ репозиториев (Wiki-farming).
- [[GGUF MODEL]] -> [[LLAMA-CPP]] -> [[LOCAL AI RESPONSE]] инференс.

## Пример использования (CLI / Python)
```bash
# 1. Запуск инференса в терминале (Interactive mode)
./main -m llama-3-8b-instruct.Q4_K_M.gguf -n 512 --repeat_penalty 1.0 -i -r "User:"

# 2. Запуск сервера (OpenAI-compatible)
./server -m models/7B/ggml-model-q4_0.gguf -c 2048 --port 8080
```

## Связанные Репозитории (Key Integrations)
- [[OLLAMA]] — удобная обертка над llama.cpp (то, что мы сейчас используем)
- [[LANGCHAIN]] — фреймворк для создания агентов на базе llama.cpp
- [[HUGGINGFACE-TRANSFORMERS]] — источник моделей (перед их конвертацией в GGUF)
- [[KOBOLDCPP]] — продвинутый интерфейс для llama.cpp (для писателей и RP)
- [[LM-STUDIO]] — GUI приложение для Windows на базе этого движка
- [[DNA-FARM]] — источник наших данных (репозиториев)
- [[DEEPSEARCH]] — если в отчетах нужен ИИ-поиск
- [[ANYTHING-LLM]] — локальный интерфейс базы знаний (использует llama.cpp)
- [[FASTCHAT]] — API для работы с моделями
- [[KUBERNETES]] / [[HELM]] — деплой локальных моделей в кластер
- [[GRAFANA]] / [[PROMETHEUS]] — мониторинг нагрузки на GPU/VRAM
- [[CRAWL4AI]] — сборщик данных (топливо для анализа в моделях)
- [[ETHICAL-HACKING-NOTES]] — если модели используются для анализа атак
- [[ALLUXIO]] — кэширование огромных GGUF файлов (в десятки Гб)
- [[BUN]] / [[NODE-JS]] — работа с биндингами
- [[ASTRO]] — для создания фронтенда
- [[ELECTRON]] — десктопное приложение для управления локальным ИИ
- [[FFMPEG]] — если модели анализируют видео-кадры
- [[FACE-RECOGNITION]] — если распознавание лиц встроено в систему
- [[FASTAPI]] — API управления инференсом
- [[ESP32]] — (неприменимо напрямую, слишком тяжел)
- [[FAIRY-DOCKER]] — легкие контейнеры для llama.cpp
- [[GIN]] — скоростной веб-шлюз
- [[GPG]] — подпись моделей и их весов
- [[HA-PROXY]] — нагрузка на кластер видеокарт
- [[GARDEN]] — разработка в облаке
- [[XLM]] / [[GENSIM]] — семантический анализ в моделях
- [[GBDT]] — предиктивный анализ (как инструмент внутри ИИ)
- [[HASHCAT]] — использование GPU совместно с моделями
- [[HTOP]] — мониторинг ресурсов CPU/RAM при работе моделей
- [[HARBOR]] — реестр образов для контейнеров с ИИ
- [[HEDGEDOC]] — документация промптов
- [[INTERPRETABLE-ML]] — объяснение того, почему модель так ответила
- [[D3]] / [[FORCE-DIRECTED-GRAPH]] — визуализация графа весов модели
- [[IP-ADDR]] — работа с сетевыми адресами в ответах ИИ
- [[IP-RECON]] — разведка IP источников атак через ИИ
- [[MASTER-PLAN]] — архитектурная основа (Инфраструктура)
- [[ZEN]] — спокойствие админа (100% локально)
- [[TERRAFORM]] — создание GPU серверов
- [[JUPYTER]] — отладка промптов для локальных моделей
- [[KIBANA]] — анализ логов ответов ИИ
- [[PANDAS]] — работа с данными внутри ИИ ответа
- [[LOCUST]] — нагрузочное тестирование скорости генерации (TPS)
- [[LOGGING]] — запись каждого промпта и ответа
- [[STABLE-DIFFUSION]] / [[INVOKEAI]] — генерация картинок (соседняя область ИИ)
- [[RUST]] — язык для самых быстрых биндингов к llama.cpp
- [[ZIG]] — использование Zig для ускорения математики в будущем
- [[CUDA]] / [[METAL]] — аппаратные ускорители для llama.cpp
