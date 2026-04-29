# NEXUS Deep Gene Analysis: BANDIT

> **Refined by Antigravity (NEXUS Metamorphic Agent) — 2026-04-09**
> Focus: Static Code Security Analysis

## 🧬 Genetic Registry (Genes Library)

### 1. `GENE_AST_SECURITY_SCANNING` [Audit]
- **Source**: `bandit/core/node_visitor.py` (Abstract Syntax Tree analysis)
- **Logic**: Поиск опасных конструкций (exec, eval, shell=True) через обход дерева AST без выполнения кода.
- **Application**: Встроенный "Security Sentinel" для NEXUS-агентов, проверяющий генерируемый код перед запуском.

### 2. `GENE_VULNERABILITY_SIGNATURES` [Knowledge]
- **Source**: `bandit/plugins/` (B101, B608, etc.)
- **Logic**: База сигнатур известных уязвимостей в Python коде (SQLi, Weak Crypto, Hardcoded passwords).
- **Application**: Автоматический аудит кодовой базы NEXUS на предмет архитектурных дефектов безопасности.

## 📊 Technical Benchmarks
- **Domain**: `Application Security / SAST`
- **NEXUS Value**: ⭐⭐⭐⭐⭐⭐⭐⭐⭐ 9/10 (КРИТИЧЕСКИЙ ген аудита)
- **Status**: `GENE_METADATA_LOCKED`
