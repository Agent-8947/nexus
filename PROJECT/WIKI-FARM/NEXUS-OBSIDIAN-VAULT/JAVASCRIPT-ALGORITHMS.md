---
tags: [nexus-vault, javascript, typescript, algorithms, data-structures, leetcode, interview]
category: Programming / CS Foundations (JavaScript Algorithmic Mastery)
language: JavaScript / TypeScript
github: https://github.com/trekhleb/javascript-algorithms (Master Collection)
---

# JAVASCRIPT-ALGORITHMS — Algorithms and Data Structures for Everyone (JS)

## Описание
**JavaScript Algorithms** — это колоссальный репозиторий с открытым исходным кодом, который содержит почти все известные **алгоритмы и структуры данных**, реализованные на чистом **JavaScript/TypeScript**. Это не просто "код", а полноценная учебная энциклопедия с детальными объяснениями, видеоуроками и временной сложностью (Big O). Это фундамент для создания любого сложного интерфейса, ИИ-модуля на стороне клиента или высоконагруженного Node.js сервиса.

## Основные Разделы (The Knowledge Segments)
| Группа | Примеры | Для чего в NEXUS? |
|--------|---------|-------------------|
| **Structures** | Linked Lists, Trees, Graphs, Hash Tables | Архитектура внутреннего мозга графа Obsidian |
| **Sorting** | QuickSort, MergeSort, HeapSort | Группировка 1400+ репозиториев по дате/звездам |
| **Searching** | Binary Search, Jump Search | Мгновенный поиск по вашей базе знаний |
| **Graphs** | Dijkstra, BFS, DFS, A* | Поиск связей между технологиями и IP адресами |
| **Math** | Prime numbers, Fast Fourier, Power set | Криптография и сжатие данных в системе |
| **Sets**| Combinations, Permutations | Математический подбор хакерских паролей |

## Почему это Killer-App
1. **Interactive Visualization**— Почти каждый алгоритм можно запустить в браузере и увидеть визуально, как он работает "под капотом".
2. **Interview Prep**— Золотой стандарт для подготовки к собеседованиям в Google, Meta или Amazon (идеально для [[ENG-INTERVIEW]]).
3. **Optimized Code**— Все реализации проверены тысячами разработчиков на максимальную производительность (CPU/RAM).
4. **TypeScript Support**— Строгая типизация позволяет избежать глупых ошибок при работе с данными.
5. **Universal**— Эти алгоритмы работают везде: в браузере, на мобильных телефонах, на серверах [[NODEJS]] и даже в роботах [[DART]].

## Архитектурная Ценность для NEXUS
- **Паттерн:** Клиентский Когнитивный Слой (Client-side Intelligence). Возможность проводить сложные вычисления (напр. расчет связей графа) прямо в браузере пользователя, не нагружая сервер.
- **Интеграция:** Модуль NEXUS Frontend Brain — использование графовых алгоритмов (Dijkstra/BFS) для отрисовки карты знаний [[FORCE-DIRECTED-GRAPH]].
- [[RAW DATA]] -> [[JS-ALGORITHM]] -> [[SORTED KNOWLEDGE]] аналитика.

## Пример кода (JavaScript / BFS Graph Search)
```javascript
// Поиск связей между технологиями в NEXUS Graph
import Graph from './data-structures/graph/Graph';
import breadthFirstSearch from './algorithms/graph/breadth-first-search/breadthFirstSearch';

const graph = new Graph();
graph.addEdge('Python', 'FastAPI');
graph.addEdge('FastAPI', 'Uvicorn');
graph.addEdge('Uvicorn', 'Nginx');

// Находим связь от Python до Nginx
breadthFirstSearch(graph, 'Python', {
  enterVertex: ({ currentVertex }) => {
    console.log(`Nexus: Проверяем узел ${currentVertex.getKey()}`);
  }
});
```

## Связанные Репозитории
- [[ALGS4]] — база алгоритмов на Java (Princeton)
- [[ALGORITHM-VISUALIZER]] — живая визуализация этих алгоритмов
- [[D3]] / [[FORCE-DIRECTED-GRAPH]] — визуализация графов
- [[NODEJS]] — серверная среда для запуска JS алгоритмов
- [[BUN]] — сверхбыстрая альтернатива Node.js
- [[DNA-FARM]] — источник наших данных (репозиториев)
- [[DEEPSEARCH]] — если в результатах нужен ИИ-поиск
- [[ANYTHING-LLM]] — хранение и поиск в Obsidian отчетов о коде
- [[CRAWL4AI]] — сборщик данных (топливо для анализа)
- [[ETHICAL-HACKING-NOTES]] — использование алгоритмов для взлома
- [[ALLUXIO]] — кэширование огромных массивов данных
- [[ASTRO]] / [[NEXTJS]] — современные фронтенды
- [[ELECTRON]] — десктопное приложение
- [[FFMPEG]] — если алгоритмы обрабатывают кадры видео
- [[FACE-RECOGNITION]] — математика за распознаванием
- [[FASTCHAT]] / [[FASTAPI]] — API управления
- [[ESP32]] — (неприменимо напрямую)
- [[FAIRY-DOCKER]] — упаковка в контейнеры
- [[GIN]] — скоростной веб-шлюз
- [[GPG]] — подпись артефактов
- [[HA-PROXY]] — нагрузка на кластер
- [[GARDEN]] — разработка в облаке
- [[XLM]] / [[GENSIM]] — семантический анализ документации
- [[GBDT]] — (неприменимо напрямую)
- [[HASHCAT]] — реализация алгоритмов перебора на JS
- [[HELM]] / [[KUBERNETES]] — запуск нод в кластере
- [[HTOP]] — мониторинг ресурсов CPU/RAM
- [[HARBOR]] — реестр образов
- [[HEDGEDOC]] — документация по коду
- [[INTERPRETABLE-ML]] — объяснение работы алгоритмов
- [[IMAGES-PYTHON]] — рисование ИИ графиков
- [[IMMLIB]] — низкоуровневая отладка в Windows
- [[INFRASTRUCTURE]] — как всё связано
- [[IP-ADDR]] — чистая работа с IP
- [[IP-RECON]] — разведка IP
- [[JAVA]] — промышленный стандарт (аналогии)
- [[JENKINS]] — автоматизация CI/CD
- [[JINJA2]] — шаблоны для генерации отчетов
- [[JOB-INTEL]] — OSINT бот по вакансиям Frontend-архитекторов
- [[JUPYTER]] — лаборатория анализа алгоритмов
- [[LEETCODE]] — упражнения и задачи
- [[CTCI-6TH-EDITION]] — классика подготовки к собеседованиям
- [[CODEFORCES-GO]] — олимпиадное программирование
- [[CLEVERALGORITHMS]] — роевой интеллект и эволюция
- [[ZEN]] — спокойствие разработчика при 100% покрытии тестами
