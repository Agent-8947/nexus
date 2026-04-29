---
tags: [nexus-vault, ai, models, mobile, browser, webgpu, mlc, transformers, inference]
category: AI / Edge Computing & Mobile Inference (LLM everywhere)
language: C++ (Core) / TypeScript (TVM) / Rust / Swift
github: https://github.com/mlc-ai/mlc-llm
---

# MLC-LLM — LLM On-Device with Hardware Acceleration (Mobile/WebGPU)

## Описание
**MLC-LLM (Machine Learning Compilation for LLMs)** — это мощнейший проект, который поставил перед собой амбициозную цель: сделать запуск больших языковых моделей (LLM) возможным на **любом устройстве** с аппаратным ускорением. Благодаря компилятору Apache TVM, MLC-LLM позволяет запускать модели типа Llama 3, Mistral или Gemma не только на серверах, но и на iPhone, Android-смартфонах, а также прямо в **браузере** (через WebGPU), используя 100% мощности встроенной видеокарты.

## Технический Стек (The Universal Engine)
| Компонент | Технология |
|-----------|------------|
| Core Engine | Apache TVM (TVM Unity) / Relax |
| Acceleration | WebGPU (Browser), Metal (Apple), Vulkan (Android/Windows), CUDA |
| Language | C++, Rust (bindings), TypeScript (for Web), Swift (for iOS) |
| Optimizer | Autotuning for specific device hardware |
| Interface | MLC Chat CLI / Mobile App / Web SDK |

## Почему это Killer-App
1. **Unrivaled Portability**— Вы можете запустить ИИ-агента NEXUS на своем смартфоне в режиме офлайн, без отправки данных на серверы.
2. **WebGPU Magic**— Позволяет пользователям запускать ИИ прямо на вашем сайте без установки какого-либо ПО. Весь расчет идет на их видеокарте.
3. **Hardware-Specific Optimization**— Компилятор TVM анализирует архитектуру чипа (напр. Apple M3 или Snapdragon Gen 3) и создает бинарный код, идеально подходящий под него.
4. **Low Memory Consumption**— Продвинутые методы квантования и управления памятью позволяют "впихнуть" умные модели в смартфоны с 8-12 Гб RAM.
5. **Unified Runtime**— Один и тот же код работает и на MacBook, и на Raspberry Pi, и на игровом ПК с RTX 4090.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Рассредоточенный Краевой Интеллект (Edge Node Intelligence). Разгрузка ваших серверов за счет переноса части вычислений на устройства клиентов.
- **Интеграция:** Модуль NEXUS Mobile Agent — создание полноценного мобильного приложения, которое анализирует данные OSINT прямо в кармане пользователя.
- [[GLOBAL BRAIN]] -> [[MLC-LLM (NODE)]] -> [[USER DEVICE]] децентрализация.

## Пример компонента (TypeScript / WebGPU Chat)
```typescript
import { ChatModule } from "@mlc-ai/web-llm";

// 1. Инициализация ИИ-движка прямо в браузере
const chat = new ChatModule();

// 2. Скачивание и запуск модели (Llama-3-8B-Q4F16)
await chat.reload("Llama-3-8b-instruct-v0.1-q4f16_1-MLC");

// 3. Генерация ответа через WebGPU
const response = await chat.generate("NEXUS: Привет, расшифруй этот лог...");
console.log(response); // (Обработано видеокартой пользователя!)
```

## Связанные Репозитории (The Edge Ecosystem)
- [[LLAMA-CPP]] — основной конкурент/аналог для локального запуска
- [[HUGGINGFACE-TRANSFORMERS]] — источник моделей для подготовки в MLC
- [[OLLAMA]] — упрощенный десктопный вариант
- [[ANYTHING-LLM]] — локальный интерфейс базы знаний (использует локальный инференс)
- [[FASTCHAT]] — API для работы с моделями
- [[DNA-FARM]] — источник наших данных (репозиториев)
- [[DEEPSEARCH]] — если в отчетах нужен ИИ-поиск
- [[CRAWL4AI]] — сборщик данных (топливо для анализа в моделях)
- [[ETHICAL-HACKING-NOTES]] — если модели используются для анализа атак на мобильных
- [[ALLUXIO]] — кэширование огромных файлов моделей
- [[BUN]] / [[NODE-JS]] — работа с биндингами
- [[ASTRO]] / [[NEXTJS]] — современные фронтенды (для WebGPU интеграции)
- [[ELECTRON]] — десктопное приложение c MLC-LLM внутри
- [[FFMPEG]] — если модели анализируют видео-кадры на мобильном
- [[FACE-RECOGNITION]] — если распознавание лиц встроено в телефон
- [[FASTAPI]] — API управления инференсом
- [[ESP32]] — (неприменимо напрямую, но ESP может слать данные в MLC на телефоне)
- [[FAIRY-DOCKER]] — (неприменимо напрямую к мобильным, но к Web-серверам)
- [[GIN]] — скоростной веб-шлюз
- [[GPG]] — защита секретов
- [[HA-PROXY]] — нагрузка на кластер
- [[GARDEN]] — разработка в облаке
- [[XLM]] / [[GENSIM]] — семантический анализ в мобильном ИИ
- [[GBDT]] — (неприменимо напрямую)
- [[HASHCAT]] — использование GPU совместно с моделями
- [[HELM]] / [[KUBERNETES]] — (неприменимо напрямую к телефонам)
- [[HTOP]] — мониторинг ресурсов CPU/RAM/Battery на мобильном
- [[HARBOR]] — реестр образов
- [[HEDGEDOC]] — документация промптов
- [[INTERPRETABLE-ML]] — объяснение того, почему модель ответила именно так
- [[D3]] / [[FORCE-DIRECTED-GRAPH]] — визуализация связей через Web-приложение
- [[IP-ADDR]] — чистая работа с IP
- [[IP-RECON]] — разведка IP
- [[MASTER-PLAN]] — архитектурная основа (Инфраструктура)
- [[ZEN]] — спокойствие админа (100% офлайн работа у клиента)
- [[TERRAFORM]] — (неприменимо напрямую)
- [[JUPYTER]] — лаборатория отладки промптов
- [[KIBANA]] — анализ логов ответов мобильных агентов
- [[PANDAS]] — работа с данными внутри мобильного устройства
- [[LOGGING]] — запись каждой системной мысли
- [[LOCUST]] — нагрузочное тестирование скорости генерации на устройствах
- [[LORA]] — использование дообученных адаптеров (LoRA) в MLC-LLM
- [[VIRTUAL-MACHINES]] / [[EMULATORS]] — запуск MLC на эмулированных Android/iOS
- [[REACT-NATIVE]] / [[FLUTTER]] — фреймворки для создания приложений с MLC-LLM
- [[RUST]] — язык для самых быстрых биндингов к MLC-TVM
- [[MOBILE-SECURITY]] — защита и взлом мобильных приложений (включая ИИ-фичи)
- [[ONNX-RUNTIME]] — конкурентный движок от Microsoft для запуска моделей везде
- [[MEDIAPIPE]] — библиотека Google для ИИ-зрения на мобильных
