---
description: Запуск тестов и проверка качества кода
---
// turbo-all

1. Поиск и запуск тестов Python в папке PROJECT.

```powershell
python -m unittest discover -s "e:\Downloads\--ANTIGRAVITY store\IDE-optimus\PROJECT" -p "test_*.py"
```

2. Если тестов еще нет, выполнение базовой проверки синтаксиса.

```powershell
python -m py_compile "e:\Downloads\--ANTIGRAVITY store\IDE-optimus\PROJECT\*.py"
```

3. Проверка выполнена.
