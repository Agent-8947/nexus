---
tags: [nexus-vault, ai, agents, autonomous-agents, search, local-llm, ollama, web-browsing, coding-assistant, voice-ui, manus-alternative]
category: AI / Autonomous Agents
language: Python, JavaScript
github: https://github.com/Fosowl/agenticSeek
---

# AGENTICSEEK — Локальная Альтернатива Manus AI и Агентский Посковик

## Описание
100% локальный автономный ИИ-ассистент с голосовым управлением. Является прямой альтернативой проприетарным решениям вроде Manus AI. Умеет самостоятельно просматривать веб-страницы (через SearxNG и Selenium), писать и запускать код на различных языках, а также планировать сложные многошаговые задачи. Весь функционал (LLM, TTS/STT, поиск) работает на оборудовании пользователя, обеспечивая полную приватность.

## Основные Разделы
1. **Smart Web Browsing** — поиск, извлечение информации и заполнение форм без участия человека.
2. **Autonomous Coding** — написание, отладка и выполнение программ (Python, C, Go, Java).
3. **Agent Orchestration** — автоматический выбор лучшего "агента" под конкретную задачу.
4. **Voice-Enabled UI** — футуристичное голосовое управление (STT через Whisper, TTS локально).
5. **Local Provider Support** — интеграция с Ollama, LM Studio и кастомными LLM-серверами.

## Почему это Killer-App
- **Data Sovereignty** — данные не покидают устройство, что критично для работы с личными файлами.
- **Zero API Cost** — не требует платных подписок при наличии достаточного "железа" (минимум 12GB VRAM для 14B моделей).
- **Tool Use Excellence** — оптимизирован под DeepSeek-R1 и другие "рассуждающие" модели (Reasoning Models).
- **Multimodal Interaction** — голос + текст + браузер.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Local Agentic Hub — AGENTICSEEK является эталонной реализацией того, чем должен стать NEXUS на финальной стадии.
- **Интеграция:** Использование SearxNG как "мозга" для OSINT-агентов NEXUS.
- **Ключевое:** Система сессий (`recover_last_session`) позволяет NEXUS-агентам сохранять контекст между перезагрузками IDE.

## Системные требования (NEXUS Benchmark)
- **Minimum:** RTX 3060 (12GB) для моделей 14B (может тормозить на планировании).
- **Recommended:** RTX 4090 (24GB) для моделей 32B.
- **Professional:** 48GB+ VRAM для моделей 70B+.

## Связанные Репозитории
- [[OLLAMA]] — основной бэкенд для моделей
- [[SEARXNG]] — приватный поисковый движок
- [[BROWSER-USE]] — библиотека для управления браузером
- [[OPEN-WEBUI]] — интерфейс для взаимодействия с моделями
- [[MANUS-AI]] — проприетарный конкурент
