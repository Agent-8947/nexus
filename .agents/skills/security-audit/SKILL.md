---
name: security-audit
description: Advanced AI-powered security scanning and defense system for NEXUS projects. Based on Ship Safe v5.0.
---

# 🛡️ Security Audit & AI Defense

This skill provides the NEXUS ecosystem with a comprehensive set of tools for auditing code, hardening AI prompts, and implementing production-grade security patterns.

## 🚀 Core Capabilities

1.  **Automated Auditing**: Run `npx ship-safe audit .` to scan for secrets, injections, vulnerabilities, and misconfigurations.
2.  **AI Hardening**: Protect agents from prompt injection and jailbreaks using `System Prompt Armor`.
3.  **Cost Protection**: Prevent runaway LLM costs with token limits and budget circuit breakers.
4.  **Security Snippets**: Drop-in patterns for Rate Limiting, JWT, CORS, and Input Validation.
5.  **Compliance**: Checklists for launch-day readiness and framework-specific security.

## 🛠️ Usage for NEXUS Agents

### 1. Perform Code Audit
Before finalizing any backend or API-related task, an agent should suggest running:
```powershell
npx ship-safe audit .
```
*Goal: Catch leaked secrets and critical vulnerabilities before they reach the repo.*

### 2. Harden AI Prompts
When designing a new agent or LLM interaction, include the `System Prompt Armor` block.
*Refer to: [.agents/skills/security-audit/ai-defense/system-prompt-armor.md](file:///e:/Downloads/--ANTIGRAVITY%20store/IDE-optimus/.agents/skills/security-audit/ai-defense/system-prompt-armor.md)*

### 3. Implement Rate Limiting
For any public API endpoint, implement throttling.
*Refer to: [.agents/skills/security-audit/snippets/upstash-ratelimit.ts](file:///e:/Downloads/--ANTIGRAVITY%20store/IDE-optimus/.agents/skills/security-audit/snippets/upstash-ratelimit.ts)*

### 4. Direct Injection Check
Use regex patterns to filter untrusted user input before sending to LLM.
*Refer to: [.agents/skills/security-audit/ai-defense/prompt-injection-patterns.js](file:///e:/Downloads/--ANTIGRAVITY%20store/IDE-optimus/.agents/skills/security-audit/ai-defense/prompt-injection-patterns.js)*

## 📂 Skill Contents

- `ai-defense/`: Prompt armor, injection detection, cost protection.
- `snippets/`: Code for Rate Limiting, Auth, API Validation.
- `configs/`: Security headers and .gitignore templates.
- `checklists/`: Manual audit steps for launch day.

---

> [!IMPORTANT]
> Security is a process, not a state. Use these tools as layers of defense (Defense-in-Depth).
