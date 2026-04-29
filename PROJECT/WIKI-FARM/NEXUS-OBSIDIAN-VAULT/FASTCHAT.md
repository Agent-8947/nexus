---
tags: [nexus-vault, ai, chat-models, lmsys, vllm, evaluation, finetuning]
category: AI / LLM Training & Evaluation (Chat-specific)
language: Python
github: https://github.com/lm-sys/FastChat
---

# FASTCHAT — Open Platform for Training, Distributing, and Evaluating Chat LLMs

## Описание
**FastChat** — это мощная и современная платформа на **Python** от команды **LMSYS** (создатели Vicuna и Chatbot Arena), предназначенная для обучения, развертывания и оценки больших языковых моделей (LLM) с упором на **чат-взаимодействие**. Это основа для создания собственных локальных "Альтернатив ChatGPT", обеспечивающая высокую скорость работы и совместимость с HuggingFace.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Core Engine | vLLM (сверхбыстрый инференс) / HuggingFace Transformers |
| UI Layer | Web UI (Gradio-based) |
| Architecture | Controller, Model Workers, API Server |
| Interface | OpenAI-compatible API (JSON) |
| Training | DeepSpeed / FlashAttention support |

## Почему это Killer-App
1. **OpenAI Compatibility**— Вы запускаете FastChat, и любые ваши старые скрипты, написанные под OpenAI API, начинают работать с вашей локальной моделью (напр. Llama 3 или Vicuna).
2. **vLLM Integration**— Использование технологии PagedAttention для ускорения вывода текста в 10-20 раз на той же GPU.
3. **Multi-model serving**— Можно запускать сразу несколько разных моделей на одном сервере и сравнивать их ответы (как в Arena).
4. **Fine-tuning Pipeline**— Понятный и надежный процесс дообучения моделей на ваших специфических данных.
5. **Distributed Workers**— Распределение моделей по нескольким видеокартам или серверам.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Автономный Центр Инференса (Autonomous LLM Serving). Позволяет вашим агентам общаться с локальными моделями через стандартный API-интерфейс.
- **Интеграция:** Модуль NEXUS Agent Brain — использование FastChat для превращения сырых моделей (как Llama 3) в умных, структурированных собеседников.
- **Ключевое:** Поддержка 8-битного и 4-битного квантования (через BitsAndBytes) для запуска на домашних GPU.

## Пример запуска (CLI)
```bash
# 1. Запуск контроллера
python3 -m fastchat.serve.controller

# 2. Запуск воркера с моделью Llama 3
python3 -m fastchat.serve.vllm_worker --model-path /models/Llama-3-8B

# 3. Запуск веб-интерфейса (или OpenAI API сервера)
python3 -m fastchat.serve.openai_api_server --host localhost --port 8000
```

## Связанные Репозитории
- [[ANYTHING-LLM]] — локальный интерфейс (может использовать FastChat как бекенд)
- [[DEEPLEARNING-500-QUESTIONS]] — теория (понимание слоев Трансформера)
- [[AUTOGPTQ]] / [[AUTOAWQ]] — сжатие моделей для FastChat
- [[DNA-FARM]] — источник наших данных
- [[DESIGN-PATTERNS]] — паттерны для структуры сервера
- [[DRF]] / [[FASTAPI]] — если API нужно кастомизировать
- [[CRAWL4AI]] — сборщик данных (топливо для обучения чат-ботов)
- [[ETHICAL-HACKING-NOTES]] — как ломают "умные" боты (Prompt Injection)
- [[D3]] — визуализация качества ответов
- [[CLEANLAB]] — очистка данных перед дообучением в FastChat
