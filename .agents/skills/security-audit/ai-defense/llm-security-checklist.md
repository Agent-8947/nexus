# LLM Security Checklist

## Critical: Prompt Injection
1. [ ] System prompt separated from user input
2. [ ] User input treated as untrusted data
3. [ ] Input validation before LLM
4. [ ] Output validation after LLM

## Critical: Cost Protection
5. [ ] Per-request token limits
6. [ ] Per-user rate limiting
7. [ ] Daily/monthly spend caps
8. [ ] Alerts on unusual usage

## High: Data Protection
9. [ ] No PII in prompts
10. [ ] No secrets in system prompts
11. [ ] Audit logging for AI interactions

## High: Model Access
12. [ ] API keys secured (not in frontend)
13. [ ] Proxy AI calls through your backend

## Medium: Scope & Permissions
14. [ ] LLM has limited scope
15. [ ] Function calling permissions restricted
16. [ ] No direct database access via LLM
