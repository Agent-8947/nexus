---
name: synth
description: "Автономный синтез уникальных агентов DNA из spec-контрактов. Агент IDE генерирует код, скрипт валидирует."
---

# /synth — NEXUS DNA Autonomous Synthesis

Полностью автономный конвейер синтеза агентов. Встроенная модель IDE генерирует код, скрипт `synth_engine_v3.py` валидирует уникальность.

## Шаг 1. Загрузить спеки
// turbo
```
python synth_protocol_v2.py register
```
Результат: JSON-контракты в `agent_specs/`.

## Шаг 2. Получить список несинтезированных спеков
// turbo
```
python -c "
import json
from pathlib import Path

specs_dir = Path('agent_specs')
osint_dir = Path('DNA_OSINT')

existing = {f.stem.split('_', 1)[1].rsplit('_synthesized', 1)[0] for f in osint_dir.glob('*.py')}
pending = []
for sf in specs_dir.glob('*.json'):
    spec = json.loads(sf.read_text(encoding='utf-8'))
    if spec['agent_id'] not in existing:
        pending.append(spec['agent_id'])
print(json.dumps(pending, indent=2))
"
```

## Шаг 3. Для КАЖДОГО спека из pending-списка

Прочитай файл `agent_specs/<AGENT_ID>.json`.
Сгенерируй **полный production-ready Python-скрипт** строго по контракту:
- Используй **указанные API endpoints** (не заменяй на другие)
- Создай **SQLite таблицу** с колонками из `data_model`
- Реализуй **core_algorithm** как реальную логику
- Включи все `logic_markers` как строковые литералы в код
- Имя класса = `<AgentId>Agent`, таблица = `<agent_id>` (lowercase)

Сохрани файл: `DNA_OSINT/<NN>_<AGENT_ID>_synthesized_agent.py`
где `<NN>` — следующий порядковый номер.

## Шаг 4. Валидация после каждого файла
// turbo
```
python synth_engine_v3.py --validate DNA_OSINT
```
Если обнаружен CLONE — удали файл и перегенерируй с другой структурой.

## Шаг 5. Пересборка рейтинга
// turbo
```
python llm_evaluator.py
python generate_dashboard.py
```

## Шаг 6. Финальный отчёт
Выведи таблицу: Agent ID | Tier | Score | Status (saved/rejected).
