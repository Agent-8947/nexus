# LEX-NEXUS 07: LAW OF IDEMPOTENT TASKS
**Status**: DRAFT (AWAITING APPROVAL)
**Domain**: DATA_ENGINEERING
**Derived from**: [Apache Airflow]

### 1. DIRECTIVE
Любая операция, выполняемая агентом (создание файла, вызов API, патч кода), должна быть идемпотентной. Повторный запуск того же агента с теми же входными данными не должен приводить к дублированию или порче данных.

**Обоснование:** Airflow (35k stars) построен на принципе идемпотентности тасок. Если "переливка данных" упала на середине, ее можно перезапустить без страха создать дубликаты. В NEXUS это критично: если агент упал при модификации `README.md`, повторный запуск не должен вставить одну и ту же секцию дважды.

### 2. SYMMETRY / PATTERN
**VIOLATION:**
```python
with open("WIKI.md", "a") as f:
    f.write(new_knowledge) # Вставит дважды при перезапуске
```

**COMPLIANCE:**
```python
content = read_file("WIKI.md")
if new_knowledge_hash not in content:
    patch_file("WIKI.md", new_knowledge)
```
