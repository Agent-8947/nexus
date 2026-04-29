# 🛰️ NVIDIA Catalog Assistant [/nvidia-catalog]

Запуск режима консультации по архитектуре ИИ и выбору моделей из каталога NVIDIA (134+ модели).

## 🧬 Описание
Этот воркфлоу активирует **NVIDIA Infra Consultant**. Агент использует **Llama 3.1 405B** для глубокого анализа ваших задач и подбора оптимальных весов, NIM-контейнеров или стратегий развертывания.

## 🛠️ Доступные действия

### 1. Консультация по модели
Запустите скрипт консультанта, чтобы получить рекомендацию:
`python "e:\Downloads\--ANTIGRAVITY store\agent design video\PROJECT\AD-FACTORY\agents\NVIDIA_CONSULTANT.py"`

### 2. Просмотр реестра моделей
Список всех ID моделей доступен здесь:
[NVIDIA_MODEL_REGISTRY.md](file:///e:/Downloads/--ANTIGRAVITY%20store/IDE-NEXUS/.agents/skills/nvidia-catalog/resources/NVIDIA_MODEL_REGISTRY.md)

### 3. Прямой вызов (Python Snippet)
Используйте навык `nvidia-catalog` в коде:
```python
from nvidia_connector import NVIDIAConnector
nv = NVIDIAConnector()
response = nv.chat(model="meta/llama-3.1-405b-instruct", messages=[{"role": "user", "content": "..."}])
```

---

## 🚨 Инструкция для Агента (NEXUS)
При вызове этой команды:
1.  **Анализировать** текущий контекст проекта.
2.  **Запустить** `NVIDIA_CONSULTANT.py` с вопросом пользователя (если он был передан).
3.  **Предложить** конкретную модель для текущего шага реализации.
4.  **Проверить** наличие `NVIDIA_API_KEY` в системном `.env`.

---
**Status**: ACTIVE | **Command**: /nvidia-catalog
