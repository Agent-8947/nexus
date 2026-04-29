---
tags: [nexus-vault, blockchain, privacy, cross-chain, zero-knowledge]
category: Infrastructure / Privacy Protocols
language: Rust / WebAssembly
github: https://github.com/anoma/anoma
---

# ANOMA — Intent-Centric Privacy Protocol

## Описание
**Anoma** — это первый в мире **протокол обмена активами на основе "намерений" (intents)**. Вместо транзакции "A пересылает B токены X", пользователь отправляет "намерение": "Я хочу получить токены Y в обмен на свои токены X к такому-то времени". Протокол находит совпадения и выполняет сделку максимально конфиденциально.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Core Engine | Rust (v1.70+) |
| Consensus | Tendermint-based (Proof-of-Stake) |
| Privacy | Zero-Knowledge Proofs (ZKP), FHE |
| Scripting | WebAssembly (WASM) |
| Identity | Typhon (Shielded Multi-Chain identity) |

## Ключевые Новации
1. **Intents** — декларативный подход к сделкам (описывается "что хочу", а не "как").
2. **Infinite Multi-Chain Aggregation** — находит лучшие пути обмена между любыми блокчейнами.
3. **Shielded Pool** — скрывает отправителя, получателя и сумму сделки от посторонних.
4. **Counterparty Discovery** — узлы сети (solvers) автоматически сводят покупателей и продавцов.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Система управления намерениями (Intent Engine). Это фундамент для автономных агентов. Агент говорит: "Я хочу собрать отчет по X", а NEXUS-солверы ищут способы это сделать.
- **Интеграция:** Использование ZKP (нулевого разглашения) для анонимной оплаты ресурсов OSINT-агентами.
- **Ключевое:** Работает без "наблюдаемого посредника". Полная приватность транзакций.

## Пример "Намерения" (Псевдокод)
```rust
let my_intent = Intent {
    provide: Asset::NEXUS_TOKEN(100),
    wants: Asset::COMPUTE_POWER(10), # Хочу 10 часов вычислений за токен
    expiry: block_height + 500,
    privacy: PrivacyLevel::MAX,
};
anoma.submit(my_intent); # Солверы сети найдут того, кто продаст время за токены
```

## Связанные Репозитории
- [[BLACK-HAT-RUST]] — безопасность систем
- [[ARIEL-OS]] — ОС на Rust (IoT)
- [[CERTIFICATES]] — управление доверием
- [[BRAFT]] — распределенный консенсус
