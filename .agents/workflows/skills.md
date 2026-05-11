---
description: Синхронизация и управление навыками через Autoskills
---
// turbo-all

1. Запускаем сканирование проекта и установку недостающих навыков.

```powershell
npx autoskills -y
```

2. Проверяем установленные навыки в `.agents/skills`.

```powershell
Get-ChildItem -Path ".agents\skills" -Directory | Select-Object Name
```

3. Проверка актуальности lock-файла.

```powershell
Get-Content "skills-lock.json" | ConvertFrom-Json
```
