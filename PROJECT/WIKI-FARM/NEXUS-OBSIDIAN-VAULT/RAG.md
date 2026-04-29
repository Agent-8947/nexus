---
tags: [nexus-vault, ai, rag, vectordb, knowledge-base, llm, embeddings, semantic-search]
category: AI / Information retrieval & Fact-based Generation (The RAG Pattern)
language: Python 3.8+ / LangChain / LlamaIndex / Vector Databases
github: https://github.com/run-llama/llama_index (LlamaIndex) / https://github.com/chripit/awesome-rag (Master List)
---

# RAG — Retrieval-Augmented Generation (The Fact-based AI Pattern)

## Описание
**RAG (Retrieval-Augmented Generation)** — это самая мощная и актуальная архитектурная схема в современном ИИ. Она решает главную проблему больших языковых моделей ([[LLM]]) — галлюцинации и отсутствие актуальных знаний. В схеме RAG ваш ИИ-агент не "придумывает" ответ из головы, а сначала идет в вашу локальную базу знаний (Obsidian Vault / [[POSTGRESQL]]), находит там нужные факты (через [[SEMANTIC-SEARCH]]) и только потом синтезирует ответ, опираясь на эти документы. Это делает ИИ **фактически точным**, безопасным и всегда обновленным.

## Технический Стек (The RAG Infrastructure)
| Компонент | Технология |
|-----------|------------|
| **Orchestration** | [[LANGCHAIN]], LlamaIndex (The core framework) |
| **Embedder** | BGE-M3, OpenAI, HuggingFace BGE (Text to vector) |
| **Vector DB** | ChromaDB, FAISS, [[PGVECTOR]], Pinecone, Weaviate |
| **Retriever** | Dense Retrieval (Semantic) + Sparse Retrieval (BM25 via [[LUCENE]]) |
| **Generator** | [[OLLAMA]] (Qwen/Llama 3), GPT-4o, Claude 3.5 |

## Почему это Killer-App
1. **Zero Hallucination**— ИИ больше не врет. Если в вашей Wiki нет информации о репозитории, он скажет "Я не знаю", а не придумает его название.
2. **Up-to-date Knowledge Mastery**— Вам не нужно переобучать ИИ каждую неделю. Просто добавьте новый .md файл в Obsidian, и ИИ узнает о нем через секунду.
3. **Private Data Safety**— Ваши секретные документы не отправляются в OpenAI. Весь процесс поиска и генерации происходит локально (через [[OLLAMA]]).
4. **Source Citations Power**— Каждое слово ИИ может подтвердить ссылкой: "Я взял это из файла [[NATS.md]] на строке 42".
5. **Efficiency**— Позволяет "кормить" ИИ миллионами страниц документации, не тратя миллионы на оплату огромных контекстных окон API.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Интеллектуальный Оракул Знаний (The Knowledge Oracle). "Память" всей системы NEXUS на базе 1400+ репозиториев.
- **Интеграция:** Модуль NEXUS Oracle — использование RAG для ответов на ваши вопросы по всей базе накопленных досье в Obsidian.
- [[QUESTION]] -> [[VECTOR SEARCH IN VAULT]] -> [[DOC CONTEXT]] -> [[OLLAMA RESPONSE]] результат.

## Пример пайплайна (Python / LlamaIndex)
```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.ollama import Ollama

# 1. Загружаем наш Obsidian Vault
documents = SimpleDirectoryReader("./NEXUS-OBSIDIAN-VAULT").load_data()

# 2. Инициализируем локальный ИИ (через Ollama)
llm = Ollama(model="qwen2.5-coder:3b")

# 3. Создаем векторный индекс (Смысловая карта Wiki)
index = VectorStoreIndex.from_documents(documents)

# 4. Задаем вопрос по 1400 репозиториям
query_engine = index.as_query_engine(llm=llm)
response = query_engine.query("Какие инструменты в нашей базе лучше всего подходят для OSINT IP-адресов?")
print(response)
```

## Связанные Репозитории (The RAG Ecosystem)
- [[LANGCHAIN]] — фреймворк для создания RAG-цепочек
- [[OLLAMA]] / [[LLAMA-CPP]] — локальный "Генератор" ответов
- [[POSTGRESQL]] / [[PGVECTOR]] — идеальная база для векторов RAG
- [[DNA-FARM]] — основной источник "сырья" (знаний) для RAG
- [[DEEPSEARCH]] — если в RAG нужен ИИ-поиск (Semantic branch)
- [[ANYTHING-LLM]] — готовый локальный интерфейс для RAG на ваших файлах
- [[CRAWL4AI]] — сборщик данных (топливо для RAG-индекса)
- [[ETHICAL-HACKING-NOTES]] — если RAG используется для ответов по техникам взлома
- [[ALLUXIO]] — кэширование огромных индексов RAG
- [[ASTRO]] / [[NEXTJS]] — современные фронтенды для "Оракула"
- [[ELECTRON]] — десктопное приложение для общения с RAG
- [[FFMPEG]] — если RAG ищет по транскрипциям видео
- [[FACE-RECOGNITION]] — (неприменимо напрямую)
- [[FASTCHAT]] / [[FASTAPI]] — API управления RAG-системой
- [[FAIRY-DOCKER]] — легкие контейнеры для векторных баз
- [[GIN]] — скоростной веб-шлюз
- [[GPG]] — защита секретных векторных баз (Encryption at rest)
- [[HA-PROXY]] — нагрузка на кластер воркеров генерации
- [[GARDEN]] — разработка в облаке
- [[XLM]] / [[GENSIM]] — семантический анализ текстов RAG (Ranking)
- [[GBDT]] — (неприменимо напрямую)
- [[HASHCAT]] — (неприменимо напрямую)
- [[HELM]] / [[KUBERNETES]] — запуск нод RAG в кластере
- [[HTOP]] — мониторинг ресурсов CPU/RAM (Индексация — тяжелый процесс)
- [[HARBOR]] — реестр образов для инструментов
- [[HEDGEDOC]] — документация проекта
- [[INTERPRETABLE-ML]] — почему RAG выбрал именно эти документы
- [[D3]] / [[FORCE-DIRECTED-GRAPH]] — визуализация связей между фактами в графе
- [[IMAGE-PROCESSING]] — (OCR для добавления текстов с картинок в RAG)
- [[IMAGES-PYTHON]] — рисование ИИ графиков релевантности
- [[INFRASTRUCTURE]] — как всё связано (Мастер-чертеж)
- [[IP-ADDR]] — чистая работа с IP (Field type "string")
- [[IP-RECON]] — разведка IP
- [[JAVA]] — (Java-RAG: LangChain4j)
- [[JAVASCRIPT-ALGORITHMS]] — ИИ на JS (в браузере - WebGPU RAG)
- [[JENKINS]] — автоматизация переиндексации RAG
- [[JINJA2]] — шаблоны для генерации лог-отчетов
- [[JOB-INTEL]] — OSINT бот по вакансиям AI-инженеров
- [[JUPYTER]] — лаборатория отладки RAG-пайплайнов
- [[KIBANA]] — дашборды логов всей сети
- [[MASTER-PLAN]] — архитектурная основа
- [[ZEN]] — спокойствие админа (ИИ говорит чистую правду)
- [[PYTHON]] — родной язык для RAG
- [[NLP]] — основа понимания смыслов в RAG
- [[LUCENE]] — движок гибридного поиска (BM25 + Semantic)
- [[CHROMA]] / [[PINECONE]] / [[WEAVIATE]] — специализированные дома для векторов
- [[LLAMAINIndex]] — библиотека №1 для управления данными в RAG
- [[BGE-M3]] — ультимативный механизм превращения смыслов в вектора
- [[UNSTRUCTURED]] — очистка грязных данных перед добавлением в RAG
