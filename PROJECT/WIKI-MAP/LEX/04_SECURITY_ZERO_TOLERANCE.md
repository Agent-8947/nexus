# LEX-NEXUS 04: LAW OF SECRET ZERO-TOLERANCE
**Status**: DRAFT (AWAITING APPROVAL)
**Domain**: SECURITY
**Derived from**: [Gitleaks, TruffleHog, Personal-Security-Checklist]

### 1. DIRECTIVE
Запрещено хранить любые секреты (API ключи, токены, пароли) в исходном коде, конфигах, markdown-файлах или JSON-артефактах. Все секреты должны загружаться исключительно из переменных окружения (`.env`) через `dotenv` или аналог. Перед каждым коммитом в репозиторий NEXUS обязателен автоматический Pre-Commit хук с `gitleaks` или `trufflehog`. Коммит, содержащий секрет, является критическим инцидентом безопасности.

**Обоснование:** Gitleaks (18k stars) и TruffleHog (18k stars) — два главных инструмента индустрии для обнаружения утечек секретов. Оба проекта предоставляют Pre-Commit хуки и CI/CD интеграцию. TruffleHog дополнительно выполняет **верификацию** найденных секретов (проверяет, активен ли ключ), что критически отличает его от простого regex-сканирования.

### 2. SYMMETRY / PATTERN

**VIOLATION (Текущее состояние NEXUS `.env`):**
```python
# Хардкод в скрипте
API_KEY = "sk-ant-api03-xxxx"
client = anthropic.Anthropic(api_key=API_KEY)
```

**COMPLIANCE (Как требует этот закон):**
```python
import os
from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
# Ключ живет ТОЛЬКО в .env, который находится в .gitignore
```

**Pre-Commit (.pre-commit-config.yaml):**
```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.24.2
    hooks:
      - id: gitleaks
```
