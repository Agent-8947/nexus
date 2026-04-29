# LEX-NEXUS 03: LAW OF TYPE CONTRACTS
**Status**: DRAFT (AWAITING APPROVAL)
**Domain**: CODE
**Derived from**: [FastAPI, Clean-Code-JavaScript, PythonRobotics]

### 1. DIRECTIVE
Каждый агент NEXUS, генерирующий Python-код, обязан использовать типизацию (type hints) на входе и выходе всех публичных функций. Для валидации структур данных на границе API или межагентного обмена обязательно использовать Pydantic BaseModel. Передача сырых словарей (`dict`) между агентами или в LLM — архитектурный дефект.

**Обоснование:** FastAPI (228k stars) построен целиком на принципе "Declare once with types, get validation + docs + editor support for free". Clean-Code-JavaScript (93k stars) предписывает: "Function arguments (2 or fewer ideally)". Объединив оба принципа, мы получаем контракт: данные между модулями передаются как типизированные объекты, а не как позиционные аргументы или анонимные словари.

### 2. SYMMETRY / PATTERN

**VIOLATION (Как делает стандартная LLM):**
```python
def process(data):
    name = data["name"]
    result = {"status": "ok", "output": name.upper()}
    return result
```

**COMPLIANCE (Как требует этот закон):**
```python
from pydantic import BaseModel

class AgentInput(BaseModel):
    name: str
    domain: str = "GENERAL"

class AgentOutput(BaseModel):
    status: str
    output: str

def process(data: AgentInput) -> AgentOutput:
    return AgentOutput(status="ok", output=data.name.upper())
```
