---
name: nvidia-catalog
description: "Direct integration with NVIDIA API Catalog [NEXUS v5.1]. Provides access to 130+ models (Llama 3.1 405B, Nemotron, Gemma 3, etc.) with OpenAI-compatible interface."
---

# 🛰️ NVIDIA Catalog Skill (v5.1): Hardened Edition

Этот навык дает NEXUS доступ к практически неограниченным вычислительным мощностям NVIDIA через облачные эндпоинты. 

## 🧬 Operational Philosophy

NEXUS использует NVIDIA Catalog как **"Outer Brain"** для задач, требующих экстремальных параметров (например, архитектурный анализ на 405B модели) или специфической оптимизации (NIM).

## 🛠️ NEXUS Implementation Patterns

### 1. Model Selection Logic
Использовать `meta/llama-3.1-405b-instruct` только для критических решений. Для кодинга предпочитать `qwen/qwen3-coder-480b`.

### 2. Implementation Core
Вся логика взаимодействия инкапсулирована в `nvidia-connector.py`.
*Путь: [nvidia-connector.py](file:///e:/Downloads/--ANTIGRAVITY%20store/IDE-NEXUS/.agents/skills/nvidia-catalog/logic/nvidia-connector.py)*

### 3. Registry Reference
Полный список доступных моделей находится в `NVIDIA_MODEL_REGISTRY.md`.
*Путь: [NVIDIA_MODEL_REGISTRY.md](file:///e:/Downloads/--ANTIGRAVITY%20store/IDE-NEXUS/.agents/skills/nvidia-catalog/resources/NVIDIA_MODEL_REGISTRY.md)*

---

## 🚨 Operational Protocol

- **Auth**: Ключ `NVIDIA_API_KEY` должен быть прописан в системном `.env` NEXUS.
- **Fallback**: Если NVIDIA API недоступен, NEXUS должен автоматически переключиться на локальный Ollama или основной облачный провайдер.
- **Cost Control**: Помнить о лимитах бесплатных кредитов (5000) при тестировании тяжелых моделей.

---
**Status**: DEPLOYED | **Protocol**: NEXUS-V5.1-NIM
