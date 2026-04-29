---
tags: [nexus-vault, ai, automation, search-engine, rag, deep-search]
category: AI / Intelligent Search (Deep Search)
language: Python / TypeScript
github: https://github.com/vllm-project/deepsearch (or equivalent LLM-Search repo)
---

# DEEPSEARCH — AI-Powered Intelligent Document Retrieval

## Описание
**DeepSearch** — это современная технология (и репозиторий) для создания **интеллектуального поиска** по документам. В отличие от обычного "Ctrl+F" (поиск по словам), DeepSearch понимает **суть (Semantic Search)**. Он превращает текст в "числа" (эмбеддинги) и ищет похожие по смыслу куски данных, даже если слова не совпадают. Это основа для RAG (Retrieval Augmented Generation).

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Core Engine | Vector DB (Faiss, ChromaDB, Pinecone) |
| Embedder | BERT, BGE-large, HuggingFace Models |
| LLM | GPT-4o, Claude 3.5, Llama 3 (for synthesis) |
| UI | Next.js / Python Streamlit |
| API | REST API (FastAPI) |

## Как это устроено (Поток данных)
1. **Ingest**— Загружаем 1400+ репозиториев (текст, код).
2. **Chunk**— Разрезаем на маленькие кусочки по 500-1000 токенов.
3. **Embed**— Превращаем каждый кусок в вектор (напр. 1536 измерений).
4. **Index**— Сохраняем векторы в базу данных.
5. **Search**— Когда вы спрашиваете "Как взломать камеру?", DeepSearch находит самый подходящий по смыслу кусок в `CAMERADAR.md`.
6. **Synthesize**— LLM пишет ответ на базе найденных фактов.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Поиск Знаний в Хаосе (Knowledge in Chaos). Это "сердце" вашего NEXUS Brain.
- **Интеграция:** Модуль NEXUS Oracle — инструмент, который позволяет вам "разговаривать" со своей Obsidian-базой.
- **Ключевое:** Поддержка Hybrid Search (Keyword + Semantic) для максимальной точности.

## Пример компонента (Python/Pseudo)
```python
# Поиск в базе знаний по смыслу
query = "How to automate Shodan scans for legal audits?"
results = vector_db.similarity_search(query, k=5)

# Результаты будут содержать AWESOME-SHODAN-QUERIES и AUTOSPLOIT
for doc in results:
    print(f"Source: {doc.metadata['source']}")
    print(f"Snippet: {doc.page_content[:100]}...")
```

## Связанные Репозитории
- [[ANYTHING-LLM]] — самая удобная готовая оболочка для DeepSearch
- [[CRAWL4AI]] — сборщик данных (топливо для поиска)
- [[DATASCIENCEPYTHON]] — подготовка данных (пре-процессинг)
- [[D3]] — визуализация того, что мы нашли
- [[DNA-FARM]] — источник наших данных
- [[AUTOGEN]] — агенты, которые будут пользоваться этим поиском
- [[CHRONOS-FORECASTING]] — прогнозы на основе найденных фактов
- [[DEEPLEARNING-500-QUESTIONS]] — теория (чтобы понимать, как это работает)
