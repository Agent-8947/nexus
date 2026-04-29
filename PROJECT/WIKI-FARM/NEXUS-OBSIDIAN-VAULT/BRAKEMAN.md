---
title: BRAKEMAN
type: security_scanner
domain: Static Analysis, Ruby on Rails, Security
tags: [gene_source, ast_analysis, vuln_scanning]
genetic_traits: [static_analysis_vuln_scanning, security_confidence_scoring]
---

# 🧬 BRAKEMAN: Security Guardian

Статический анализатор уязвимостей для Ruby on Rails. Источник генов для **контроля безопасности кода на этапе синтеза**.

## 🕹 Генетический Профиль
- **AST Pattern Matching**: Поиск опасных конструкций (SQLi, XSS) через анализ абстрактного синтаксического дерева.
- **Confidence Scoring**: Умная фильтрация ложных срабатываний на основе глубины анализа.

## 🛠 Применение в NEXUS
- **Code Synthesis Auditor**: Проверка кода, сгенерированного другими агентами NEXUS, на соответствие стандартам безопасности.
- **Legacy Code Scanner**: Инструментарий для поиска "забытых" дыр в старых проектах.

## 🔗 Cross-Links
- [[BANDIT]]
- [[BEARER]]
- [[BLACK-HAT-RUST]]
