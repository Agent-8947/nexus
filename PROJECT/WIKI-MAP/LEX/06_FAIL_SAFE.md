# LEX-NEXUS 06: LAW OF FAIL-SAFE DEFAULTS
**Status**: DRAFT (AWAITING APPROVAL)
**Domain**: ROBOTICS / AGENTIC CONTROL
**Derived from**: [ArduPilot]

### 1. DIRECTIVE
В случае потери связи с управляющим узлом, таймаута LLM более чем на 60 секунд или получения неоднозначной команды, агент обязан прервать выполнение и перейти в состояние "FAIL-SAFE" (сохранение текущего прогресса и остановка всех активных процессов). Продолжение выполнения на базе "предположений" при отсутствии связи — критический дефект.

**Обоснование:** ArduPilot (8k stars) имеет сложнейшую систему Fail-safe для всех типов техники. Если пульт потерян — дрон не летит дальше, он летит домой (Return-to-Launch). В агентских системах это предотвращает бесконечные циклы генерации (галлюцинации) при обрыве контекста.

### 2. SYMMETRY / PATTERN
**VIOLATION:**
```python
def execute_task(task):
    result = llm.ask(task) # Ждет вечно или падает, оставляя процесс открытым
    save_result(result)
```

**COMPLIANCE:**
```python
def execute_task(task):
    try:
        with timeout(60):
            result = llm.ask(task)
    except TimeoutError:
        log_incident("FAIL_SAFE_TRIGGERED")
        abort_and_lock_state() # Возврат к безопасному состоянию
```
