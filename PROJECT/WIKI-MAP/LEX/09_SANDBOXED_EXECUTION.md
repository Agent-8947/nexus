# LEX-NEXUS 09: LAW OF CONSTRAINED EXECUTION
**Status**: DRAFT (AWAITING APPROVAL)
**Domain**: SECURITY / CODE_EXECUTION
**Derived from**: [Apache Airflow, Gitleaks, PythonRobotics]

### 1. DIRECTIVE
Запуск любого внешнего процесса (shell, python script, binary) агентом обязан происходить в изолированном окружении (Venv или временная директория) с явным ограничением по времени (timeout) и логированием всех потоков (stdout/stderr). Агент не имеет права запускать команды напрямую в корневой среде NEXUS без предварительной проверки на вредоносные паттерны (`rm -rf`, `curl | bash`).

**Обоснование:** Airflow (35k stars) использует воркеры с четкой изоляцией тасок. Gitleaks (18k stars) напоминает о рисках утечек при сканировании. В NEXUS это закон выживания: агент-программист может случайно сгенерировать `os.system("rm -rf /")`. Контракт требует обертки `SafeRun`.

### 2. SYMMETRY / PATTERN
**VIOLATION:**
```python
os.system(f"python {generated_script}") # Прямой запуск без контроля
```

**COMPLIANCE:**
```python
subprocess.run(
    ["python", script_path],
    timeout=30,
    capture_output=True,
    cwd="/tmp/agent_sandbox" # Изоляция директории
)
```
