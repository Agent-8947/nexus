---
tags: [nexus-vault, ai, rag, local-llm, obsidian-integration, docker]
category: AI / RAG Frameworks
language: JavaScript / Node.js
github: https://github.com/Mintplex-Labs/anything-llm
---

# ANYTHING-LLM — Full-stack Local RAG Platform

## Описание
**Anything-LLM** — это комплексный инструмент для превращения ваших **документов (PDF, TXT, Word, Obsidian)** в базу знаний для локальных и облачных нейросетей. Позволяет создавать изолированные "рабочие пространства" (workspaces) и общаться с ними через чат или API. Идеальная альтернатива облачным сервисам для работы с приватными данными.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Frontend | React (Desktop / Web) |
| Backend | Node.js / Express |
| Vector DB | LanceDB (local) / Pinecone / Chroma / Milvus |
| LLM Support | Ollama, LM Studio, OpenAI, LocalAI |
| Embeddings | Built-in / OpenAI / HuggingFace |

## Почему это Killer-App
1. **Full-stack** — всё от парсинга файлов до векторной базы данных в одном EXE-файле или Docker-контейнере.
2. **Multi-user** — поддержка аккаунтов с разными правами доступа.
3. **Workspace Isolation** — секретные документы по проекту А не "смешиваются" с данными проекта Б.
4. **Agent Modes**— поддержка агентов, которые могут использовать Google Search, калькулятор и поиск по документам.
5. **API & Embedders** — легкая интеграция с вашим софтом.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Персональный NEXUS Brain. Это готовый интерфейс для общения с вашей библиотекой из 1400+ репозиториев.
- **Интеграция:** Использование API Anything-LLM для предоставления агентам NEXUS доступа к WIKI-базе (RAG).
- **Ключевое:** Работает на 100% локально (через [[OLLAMA]]).

## Ключевая фишка: Obsidian Sync
```bash
# Anything-LLM может напрямую "подхватить" вашу папку Obsidian
# Все новые .md файлы будут автоматически индексироваться
# И вы сможете спросить: "В каких репозиториях используется Rust для безопасности?"
```

## Связанные Репозитории
- [[AUTOGEN]] — мультиагентные системы
- [[CRAWL4AI]] — скрапинг данных для RAG
- [[DNA-FARM]] — где мы сейчас создаем эти знания
- [[OLLAMA]] — движок для локальных нейросетей
