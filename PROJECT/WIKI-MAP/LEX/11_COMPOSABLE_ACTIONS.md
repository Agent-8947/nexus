# LEX-NEXUS 11: LAW OF COMPOSABLE ACTIONS
**Status**: DRAFT (AWAITING APPROVAL)
**Domain**: ARCHITECTURE
**Derived from**: [ArduPilot, AutoGen]

### 1. DIRECTIVE
Агенты не должны писать уникальный код под каждую подзадачу. Вместо этого они обязаны использовать и пополнять библиотеку "Composable Actions" (Тулз). Каждое действие в библиотеке должно быть атомарным и иметь четкое описание для LLM (Docstring). Создание "монолитных функций" внутри агента является дефектом.

**Обоснование:** В ArduPilot (8k stars) функционал разбит на мелкие `libraries` (AP_GPS, AP_Math), которые переиспользуются во всех типах техники (Copter, Plane). В AutoGen это реализовано через `tools`.

### 2. SYMMETRY / PATTERN
**VIOLATION:**
```python
def run_agent():
    # 200 строк кода парсинга PDF внутри агента
    pass
```

**COMPLIANCE:**
```python
from nexus_tools import pdf_parser
def run_agent():
    data = pdf_parser.extract(file) # Использование общей библиотеки
```
