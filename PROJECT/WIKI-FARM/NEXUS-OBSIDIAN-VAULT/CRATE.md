---
tags: [nexus-vault, databases, distributed, sql, postgresql-compat, real-time]
category: Infrastructure / Distributed SQL & Storage
language: Java / Presto / Lucene
github: https://github.com/crate/crate
---

# CRATE — Distributed SQL Database for Real-time Analytics

## Описание
**CrateDB (Crate)** — это распределенная, масштабируемая **SQL-база данных**, которая сочетает в себе простоту SQL и мощь поискового инженерии (Elasticsearch-like). Она разработана для работы с огромными объемами структурированных и неструктурированных данных (IoT, логи, сенсоры) в реальном времени. Если PostgreSQL — это швейцарский нож, то CrateDB — это ракетная установка для данных.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Core Engine | Lucene (Full-text search) / Elasticsearch logic |
| Language | SQL (PostgreSQL protocol compliant) |
| Architecture | Master-less (Shared-nothing), Auto-cluster |
| Distributed | Distributed Querying, Aggregation |
| Integration | Postgres drivers, Grafana, Tableau |

## Почему это Killer-App
1. **Master-less Cluster**— любая нода в кластере может принимать запросы. Нет единой точки отказа.
2. **Search + SQL**— полнотекстовый поиск внутри SQL-запроса (`WHERE match(title, 'nexus')`).
3. **Dynamic Schemas**— поддержка вложенных JSON-объектов прямо в колонках SQL.
4. **IoT Native**— база оптимизирована для записи миллионов строк в секунду с устройств.
5. **Postgres Wire Protocol**— любой софт, который умеет работать с Postgres, умеет работать с CrateDB.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Масштабируемое Аналитическое Хранилище (Analytical Lake). Использование CrateDB для хранения гигантских баз OSINT-сканирований (миллионов IP и доменов).
- **Интеграция:** Модуль NEXUS Insights — мгновенный поиск по всем когда-либо собранным данным.
- **Ключевое:** Работает одинаково на 1 и на 1000 серверах.

## Пример запроса (SQL)
```sql
-- Таблица с вложенными данными (артефакты NEXUS)
CREATE TABLE nexus_scans (
  domain STRING PRIMARY KEY,
  timestamp TIMESTAMP,
  vulns OBJECT(DYNAMIC) -- Гибкий JSON объект
);

-- Полнотекстовый поиск по уязвимостям
SELECT domain FROM nexus_scans 
WHERE match(vulns['CVE'], 'Heartbleed') 
ORDER BY timestamp DESC;
```

## Связанные Репозитории
- [[CLOUDQUERY]] — сбор данных в SQL (CrateDB - отличная цель)
- [[ALLUXIO]] — супер-кэширование данных
- [[AIRFLOW]] — наполнение базы данными
- [[ASTRO]] — визуализация этой базы
- [[ALGS4]] — алгоритмы поиска
- [[BORG]] — бэкап этой базы
