# LEX-NEXUS 14: LAW OF AUTOMATED REGRESSION
**Status**: DRAFT (AWAITING APPROVAL)
**Domain**: QA / REPRODUCIBILITY
**Derived from**: [ArduPilot, Apache Airflow]

### 1. DIRECTIVE
Ни одна новая функциональность, закон или исправление архитектуры не считается принятой в NEXUS без наличия соответствующего автоматизированного теста (Unit или Integration). Если закон или фича ломают существующие тесты (Regression), они отклоняются до исправления дефекта.

**Обоснование:** ArduPilot (8k stars) имеет "Autotest" систему, которая гоняет тысячи SITL (Software In The Loop) тестов на каждый коммит. Airflow требует 100% покрытия тестами для провайдеров. В NEXUS это залог стабильности всей фабрики.

### 2. SYMMETRY / PATTERN
**VIOLATION:**
```bash
# "Я проверил руками, скрипт работает"
# (Через неделю другой закон ломает этот скрипт, никто не замечает)
```

**COMPLIANCE:**
```python
def test_law_idempotency():
    # Тест запускает агента дважды и проверяет, что файл не изменился
    assert run_agent(input) == run_agent(input)
```
