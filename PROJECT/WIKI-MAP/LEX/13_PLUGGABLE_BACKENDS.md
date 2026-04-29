# LEX-NEXUS 13: LAW OF PLUGGABLE BACKENDS
**Status**: DRAFT (AWAITING APPROVAL)
**Domain**: PORTABILITY
**Derived from**: [Apache Airflow, Microsoft AutoGen]

### 1. DIRECTIVE
Логика агента (Agent Core) не должна иметь жестких зависимостей от конкретного провайдера LLM (OpenAI, Anthropic, Google) или типа хранилища (Postgres, S3, Local). Все зависимости должны быть абстрагированы через интерфейсы (Backends). Переключение с платного API на локальную модель (например, Ollama/DeepSeek) должно осуществляться заменой конфига без правки основного кода.

**Обоснование:** Airflow (35k stars) поддерживает десятки бэкендов для хранения метаданных и выполнения тасок. AutoGen (30k stars) абстрагирует LLM через `ModelClient`. Это страховка NEXUS от "Vendor Lock-in" и возможность полной работы во внутренней сети (Dark Net).

### 2. SYMMETRY / PATTERN
**VIOLATION:**
```python
import openai
client = openai.OpenAI() # Прямая привязка к вендору
```

**COMPLIANCE:**
```python
from nexus_core import LLMConnector
client = LLMConnector.get_provider() # Загружает провайдера из .env (Anthropic/OpenAI/Local)
```
