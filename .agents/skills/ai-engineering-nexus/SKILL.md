---
name: ai-engineering-nexus
description: Unified production blueprint for AI Agents and LLM systems. Synthesized from "AI Engineering" (Chip Huyen), "LLM Engineering Handbook" (Iusztin), and "Building Agentic AI Systems" (Biswas).
when_to_use: AI engineering, LLM production, RAG optimization, agent orchestration, evaluation, AI-as-a-judge, self-reflection, multi-agent, feature pipeline, production-ready AI, MLOps, LLMOps
allowed-tools: Read Grep
argument-hint: [topic, architecture, or framework]
---

# AI Engineering: NEXUS Master Blueprint
**Sources**: Huyen, Iusztin, Labonne, Biswas | **Version**: 2025.05

## 🧬 Core Architecture: The 3-Layer Stack

### 1. Application Layer (Agent Intelligence)
- **Focus**: Prompt Engineering, UI/UX, and Reasoning.
- **Rule**: Start with prompting -> add RAG -> finetune only as a last resort.
- **Agentic Logic**: Use **Reflection and Introspection loops** for self-correction.

### 2. Model Layer (Optimization)
- **Focus**: Finetuning, quantization, and inference optimization.
- **Method**: Use SFT (Supervised Fine-Tuning) and DPO (Direct Preference Optimization) for brand alignment.
- **Separation**: Business logic (FastAPI) must be decoupled from heavy inference (SageMaker/TGI).

### 3. Infrastructure Layer (Serving & Data)
- **Focus**: Latency, cost, and stability.
- **Pipeline**: Implement **Feature Pipelines** for real-time RAG context.
- **Stability**: Design for "Graceful Degradation" when the model fails.

---

## 🤖 Agentic Orchestration Patterns

### Coordinator-Worker-Delegator (CWD)
- **Use**: For complex, multi-step tasks in Solara/NEXUS.
- **Pattern**: A master agent decomposes the goal and delegates to specialized sub-agents (Layout, Motion, Brand).

### Self-Improvement Loops
- **Process**: Agent generates -> Agent reviews -> Agent refines.
- **Tool**: Use an "AI-as-a-judge" model for objective output scoring.

---

## 📊 Evaluation & Production
- **Metrics**: Measure Latency vs. Accuracy, Cost vs. Capability.
- **Evaluation**: Use pairwise comparisons and functional benchmarks.
- **Monitoring**: Track model drift and token usage in real-time.

---

## 🛠 Usage in NEXUS

- **/ai-engineering-nexus** — Load the master blueprint.
- **/ai-engineering-nexus eval** — Load evaluation frameworks.
- **/ai-engineering-nexus agent** — Load multi-agent orchestration patterns.

---

## 📁 Supporting Files
- [patterns.md](patterns.md) — Implementation blueprints.
- [evaluations.md](evaluations.md) — Scoring and testing guides.
- [cheatsheet.md](cheatsheet.md) — Deployment constraints.
