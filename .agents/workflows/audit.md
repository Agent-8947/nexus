---
description: Поиск секретов и потенциальных уязвимостей в коде
---
// turbo-all

1. Проверка на наличие жестко заданных паролей, API-ключей или токенов.

```powershell
grep -rEi "api_key|password|secret|token|auth" "e:\Downloads\--ANTIGRAVITY store\IDE-optimus\PROJECT"
```

2. Анализ структуры проекта на наличие лишних папок (.git, venv).

```powershell
Get-ChildItem -Path "e:\Downloads\--ANTIGRAVITY store\IDE-optimus" -Recurse -Depth 2
```

3. Проверка безопасности завершена.
