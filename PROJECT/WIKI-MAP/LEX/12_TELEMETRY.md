# LEX-NEXUS 12: LAW OF TELEMETRY BY DESIGN
**Status**: DRAFT (AWAITING APPROVAL)
**Domain**: OBSERVABILITY
**Derived from**: [ArduPilot]

### 1. DIRECTIVE
Каждое критическое решение агента (удаление файла, коммит, запуск команды) обязано сопровождаться записью в телеметрический лог (Trace ID + Context). Телеметрия должна позволять провести полное воспроизведение (Replay) действий агента в случае ошибки.

**Обоснование:** В ArduPilot "DataFlash logs" записывают каждое движение сервопривода. Без этого расследовать "краш" беспилотника невозможно. NEXUS — это беспилотник знаний. Если он совершил ошибку в логике, мы должны видеть Trace цепочки промптов.

### 2. SYMMETRY / PATTERN
**VIOLATION:**
```python
print("Deleting old files...")
os.remove(f) # Нет записи о ПРИЧИНЕ и контексте
```

**COMPLIANCE:**
```python
telemetry.log(
    action="FILE_DELETE",
    reason="Storage quota exceeded",
    trace_id="4f23-99ab",
    metadata={"filename": f, "size": 1024}
)
```
