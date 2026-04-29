# LEX-NEXUS 08: LAW OF ASYNCHRONOUS ORCHESTRATION
**Status**: DRAFT (AWAITING APPROVAL)
**Domain**: AGENTIC_SYSTEMS
**Derived from**: [Microsoft AutoGen]

### 1. DIRECTIVE
Взаимодействие между агентами NEXUS должно реализоваться исключительно через асинхронный обмен сообщениями (Message Passing). Прямые синхронные вызовы функций одного агента из другого запрещены.

**Обоснование:** AutoGen (30k stars) использует событийно-ориентированную (Event-driven) архитектуру. Это позволяет системе масштабироваться до сотен агентов без блокировок. Если Агент-А ждет Агента-Б синхронно, и Б завис — вся система NEXUS умирает. Асинхрон позволяет "подхватить" задачу позже.

### 2. SYMMETRY / PATTERN
**VIOLATION:**
```python
# Синхронная зависимость
security_report = researcher.scan(domain)
report = analyst.parse(security_report) 
```

**COMPLIANCE:**
```python
# Асинхронная очередь
await queue.put({"target": domain, "requester": "analyst"})
# Агент Analyst спит или делает другое, пока в очереди нет ответа от Researcher
```
