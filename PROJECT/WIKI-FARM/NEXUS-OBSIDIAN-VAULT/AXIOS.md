---
title: AXIOS
type: communication_interface
domain: HTTP, Web, API
tags: [gene_source, networking, security, middleware]
genetic_traits: [interceptor_chain, request_cancellation, adapter_pattern, xsrf_protection, rate_limiting]
nexus_value: 7/10
---

# 🧬 AXIOS: Agent Communication Layer

Универсальный HTTP-клиент. В экосистеме NEXUS предоставляет гены для организации внешних коммуникаций агентов с внешними API и сервисами.

## 🕹 Генетический Профиль
- **Interceptor Chain**: Middleware-конвейер для модификации запросов (аудит, логирование).
- **Request Cancellation**: Механизм мгновенной остановки сетевых операций (Kill-switch).
- **Adapter Pattern**: Абстракция над транспортом (Node.js http vs Browser Fetch).
- **Rate Limiting**: Контроль полосы пропускания при сборе данных.

## 🛠 Применение в NEXUS
- **OSINT-Harvester**: Безопасный сбор данных с защитой от XSRF и управлением лимитами.
- **Agent Intercom**: Стандартизированный интерфейс для общения агентов через HTTP/REST.

## 🔗 Cross-Links
- [[AWESOME-HACKER-SEARCH-ENGINES]]
- [[WEB-CHECK]]
