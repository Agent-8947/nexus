# LEX-NEXUS 10: LAW OF SEMANTIC VERSIONING FOR AGENTS
**Status**: DRAFT (AWAITING APPROVAL)
**Domain**: AGENTIC_COMMUNICATION
**Derived from**: [Microsoft AutoGen, Airflow]

### 1. DIRECTIVE
Взаимодействие между агентами (Handoff) должно осуществляться строго через типизированные схемы данных (Pydantic/JSON Schema). Любое изменение в формате передаваемых данных обязано сопровождаться инкрементом семантической версии (SemVer) в заголовке сообщения. Агенты должны поддерживать обратную совместимость (N-1) при чтении входящих задач.

**Обоснование:** AutoGen (30k stars) и его расширения (Extensions API) полагаются на жесткие контракты. Без этого обновление одного агента (например, Researcher) сломает пайплайн Агенту-Analyst. Мы внедряем стандарт: "Данные — это API".

### 2. SYMMETRY / PATTERN
**VIOLATION:**
```json
{ "data": "raw text from old agent" } 
// Новый агент ждет JSON, падает с ошибкой парсинга
```

**COMPLIANCE:**
```json
{
  "protocol": "NEXUS-V2",
  "version": "2.1.0",
  "payload": { ... }
}
```
