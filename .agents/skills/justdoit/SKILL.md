---
name: justdoit
description: "Master execution-planning skill. [NEXUS Hardened v5.0] Implements the Understand-Act-Verify loop with built-in context management, pagination requirements, and zero-preamble directives."
---

# 🏛️ NEXUS JustDoIt (v5.0): Hardened Edition

Этот навык — основной движок исполнения задач в NEXUS. Он преобразует абстрактную цель в проверяемый результат, исключая «дрейф контекста» и галлюцинации.

## 🧬 Core Operational Framework

Заменяет стандартный цикл разработки на **Understand → Plan → Act → Verify**.

### Phase 1: Understand (Context Recovery)

1. **Pagination First**: Если файл >300 строк, использовать только `view_file` с `StartLine/EndLine`. Чтение гигантских файлов целиком запрещено.
2. **Scan Patterns**: Искать существующие архитектурные решения. Не изобретать велосипед.
3. **Implicit Search**: Использовать `grep_search` для поиска связей между модулями до начала правок.

### Phase 2: Plan (State Definition)

1. **Create/Update `docs/plans.md`**:
   - Мильстоуны должны быть атомарными (один коммит/правка = один пункт).
   - Для каждого шага указать **Command-Based Validation** (тест или линтинг).
2. **Create/Update `docs/status.md`**:
   - Точка входа для агента после прерывания. Должна содержать "Last Successful Action" и "Next Pending Action".

### Phase 3: Act (Execution)

1. **Zero-Preamble Response**: При предложении плана ЗАПРЕЩЕНО использовать вводные слова. Сразу выдавать блок "Ready to execute".
2. **Multi-Tool Batching**: Объединять независимые правки в один вызов `multi_replace_file_content`.
3. **Atomic Commits**: Каждая успешно завершенная миля в `plans.md` должна сопровождаться фиксацией (если Git доступен).

### Phase 4: Verify (Adversarial Check)

1. **Cross-Check**: Проверять результат не по своим логам, а по файловой системе (`view_file` после правки).
2. **Static Analysis**: Запуск тестов/линтера обязателен после каждого изменения кода.

---

## 🛠 Usage Format (Proposal)

Когда план готов, агент выдает строго структурированное предложение:

```md
## ⚡️ Ready to execute (v5.0)
- **Objective**: <Краткая цель в 1 строку>
- **Plan**: `docs/plans.md`
- **First Milestone**: <имя первого этапа>
- **Validation**: <конкретная команда, например `npm run test`>
- **Blockers**: <потенциальные риски>

Подтвердите запуск (Start/Go). Любые обсуждения плана запрещены в этом блоке.
```

## 🚨 Critical Constraints

- **Anti-Preamble**: Не говорите, что вы собираетесь сделать — просто предоставьте план.
- **Context Protection**: Если контекстное окно заполнено на 80%, агент обязан инициировать процедуру суммирования (Checkpoint в `status.md`).
- **No Path Hallucination**: Все пути должны быть АБСОЛЮТНЫМИ и проверенными командой `find_by_name` или `list_dir`.

---
**Status**: ACTIVE | **Protocol**: NEXUS-V5-HARDENED
