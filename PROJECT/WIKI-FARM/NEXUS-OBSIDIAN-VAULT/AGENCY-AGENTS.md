---
tags: [nexus-vault, ai-agents, multi-agent, llm, orchestration, agentic-framework, claude, cursor, gemini, antigravity]
category: AI / Multi-Agent Framework
language: Markdown, Bash, YAML
github: https://github.com/msitarzewski/agency-agents
---

# AGENCY-AGENTS — Библиотека из 144 Специализированных AI-Агентов

## Описание
Коллекция из 144 тщательно разработанных AI-агентов с уникальными личностями, рабочими процессами и измеримыми результатами. Охватывает 12 отделов: Engineering (26 агентов), Design (8), Marketing (28), Sales (8), Product (5), Testing (8), Game Development (20+), Spatial Computing (6), Academic (5). Поддерживает все AI-инструменты: Claude Code, GitHub Copilot, **Antigravity**, Gemini CLI, Cursor, Aider, Windsurf, Kimi Code.

## Основные Разделы
1. **Engineering Division** — Frontend, Backend, AI Engineer, DevOps, Security, SRE, Embedded
2. **Design Division** — UI, UX, Brand, Whimsy Injector, Image Prompt Engineer
3. **Marketing Division** — 28 специалистов включая China market, Douyin, Bilibili
4. **Testing Division** — Evidence Collector, Reality Checker, Performance, Accessibility
5. **Specialized Division** — Agents Orchestrator, Blockchain, Compliance, MCP Builder
6. **Multi-Tool Integration** — скрипты `convert.sh`/`install.sh` для любого AI-инструмента

## Почему это Killer-App
- **144 Premium Agents** — не generic промпты; каждый — отдельная система с метриками успеха.
- **Официально поддерживает Antigravity** — установка одной командой в `~/.gemini/antigravity/skills/`.
- **Personality-first Design** — агенты имеют характер, т.е. предсказуемое поведение.
- **Production-tested** — 50+ запросов за первые 12 часов на Reddit.

## Архитектурная Ценность для NEXUS
- **Паттерн:** NEXUS может импортировать агентов напрямую через `install.sh --tool antigravity`.
- **Интеграция:** Каталог агентов = расширение NEXUS DNA библиотеки (trait library++).
- **Ключевое:** `Agents Orchestrator` и `Agentic Identity Architect` — прямые кандидаты на интеграцию в NEXUS Mission Control.

## Топ-3 примера

```bash
# Установка в Antigravity
./scripts/install.sh --tool antigravity

# Активация Security Engineer в Gemini
@agency-security-engineer review this Python code for vulnerabilities

# Batch install для CI
./scripts/install.sh --no-interactive --parallel --tool all
```

## Связанные Репозитории
- [[AGENTICSEEL]] — другой multi-agent фреймворк (AgenticSeek)
- [[OPENAI-SWARM]] — lightweight orchestration framework
- [[AUTOGEN]] — Microsoft multi-agent framework
- [[CREWAI]] — role-based agent teams
- [[NEXUS-FARM-DNA]] — внутренний NEXUS агентный движок
