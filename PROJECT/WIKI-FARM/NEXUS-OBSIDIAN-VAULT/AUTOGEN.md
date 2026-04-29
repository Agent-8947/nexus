---
tags: [nexus-vault, ai, multi-agent, llm, python]
category: AI / Agentic Systems
language: Python
github: https://github.com/microsoft/autogen
---

# AUTOGEN — Multi-Agent AI Framework

## Описание
Фреймворк от **Microsoft Research** для создания **мультиагентных AI-приложений**. Агенты могут общаться друг с другом, делегировать задачи, использовать инструменты и выполнять код — всё это автономно или с участием человека в цикле (Human-in-the-Loop).

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Язык | Python 3.10+ |
| LLM Backend | OpenAI, Azure, Ollama, Anthropic |
| Execution | Docker-sandboxed code execution |
| Patterns | GroupChat, Sequential, Two-Agent |
| State | JSON-сериализуемый |

## Ключевые Концепции
1. **ConversableAgent** — базовый агент с возможностью диалога
2. **AssistantAgent** — агент-исполнитель (пишет код, анализирует)
3. **UserProxyAgent** — прокси для человека (может автоматически исполнять код)
4. **GroupChat** — многоагентный чат с менеджером
5. **Tool Use** — агенты вызывают функции Python как инструменты
6. **Code Execution** — безопасное исполнение в Docker/IPython

## Архитектурная Ценность для NEXUS
- **Паттерн:** Прямой аналог NEXUS Orchestrator — агенты общаются и делегируют задачи
- **Интеграция:** Можно обернуть каждого WIKI-агента (Brain, Constructor, Deployer) в AutoGen Agent
- **Ключевое:** `GroupChat` = NEXUS Mission. `GroupChatManager` = NEXUS Оркестратор

## Пример: Мультиагентный NEXUS Pipeline
```python
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# Агент-Разведчик
scout = AssistantAgent(
    name="NEXUS_Scout",
    system_message="Ты — OSINT-разведчик. Собирай информацию о доменах.",
    llm_config={"model": "gpt-4o"}
)

# Агент-Аналитик
analyst = AssistantAgent(
    name="NEXUS_Analyst",
    system_message="Ты — аналитик. Обрабатывай данные от разведчика.",
    llm_config={"model": "gpt-4o"}
)

# Прокси для исполнения кода
executor = UserProxyAgent(
    name="Executor",
    code_execution_config={"work_dir": "output", "use_docker": True}
)

# Групповой чат (миссия)
group = GroupChat(agents=[scout, analyst, executor], messages=[], max_round=10)
manager = GroupChatManager(groupchat=group)

executor.initiate_chat(manager, message="Проанализируй домен example.com")
```

## Связанные Репозитории
- [[AIRFLOW]] — DAG-оркестрация
- [[ANYTHING-LLM]] — локальный LLM-чат
- [[AUTOGLUON]] — AutoML
- [[CRAWL4AI]] — веб-скрапинг для агентов
