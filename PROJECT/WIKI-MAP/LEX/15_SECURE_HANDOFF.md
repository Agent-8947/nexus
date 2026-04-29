# LEX-NEXUS 15: LAW OF SECURE HANDOFF
**Status**: DRAFT (AWAITING APPROVAL)
**Domain**: SECURITY / AGENTIC_FLOW
**Derived from**: [Microsoft AutoGen, Gitleaks, TruffleHog]

### 1. DIRECTIVE
При передаче задачи (Handoff) от одного агента к другому, контекст безопасности (права доступа, API токены, временные сессии) должен передаваться только через зашифрованные метаданные или защищенные "Handshake" токены. Передача секретов открытым текстом в промптах или JSON-сообщениях между агентами — критическое нарушение безопасности.

**Обоснование:** В AutoGen передача управления между агентами — ключевой риск. Если Агент-А дает Агенту-Б доступ к диску, Б не должен получить доступ ко всей системе. В NEXUS мы используем принцип "Least Privilege" при каждой передаче задачи.

### 2. SYMMETRY / PATTERN
**VIOLATION:**
```json
{ "task": "scan domain", "api_key": "sk-123..." } # Токен в открытом виде
```

**COMPLIANCE:**
```json
{ 
  "task": "scan domain", 
  "secure_context_id": "ctx-990-sha256", # Ссылка на защищенный Vault
  "permissions": ["READ_ONLY", "DOMAIN_X"]
}
```
