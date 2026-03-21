---
name: git-native-agent
description: Framework-agnostic, git-native standard for defining AI agents. Based on Open-GitAgent specification.
---

# 🤖 Git-Native Agent Standard

This skill implements the **Open-GitAgent** standard within NEXUS. It allows you to define agents that are portable, version-controlled, and compliant with enterprise standards (SOD, HITL, Audit Trails).

## 🚀 Key Concepts

1.  **Repository as Agent**: The repository *is* the agent. All instructions, tools, and memory are stored in Git.
2.  **Manifest (`agent.yaml`)**: Defines the agent's metadata, model preferences, and capabilities.
3.  **Identity (`SOUL.md`)**: Defines the agent's personality, communication style, and expertise.
4.  **Segregation of Duties (`DUTIES.md`)**: Defines roles (Maker, Checker, Auditor) to ensure compliance and safety.
5.  **Skills Flow**: Agents can inherit skills and compose functionality from other git repositories.

## 🛠️ NEXUS Implementation Patterns

### 1. Project Initialization
When starting a new agentic project, use the `/standard` workflow to create:
- `agent.yaml`
- `SOUL.md`
- `RULES.md`
- `DUTIES.md` (for legal/financial projects)

### 2. Segregation of Duties (SOD)
For high-risk tasks (e.g., executing code, legal filings), define at least two roles:
- **Analyst (Maker)**: Proposes changes/decisions.
- **Reviewer (Checker)**: Validates and approves.
*Refer to: [.agents/skills/git-native-agent/templates/DUTIES.md](file:///e:/Downloads/--ANTIGRAVITY%20store/IDE-optimus/.agents/skills/git-native-agent/templates/DUTIES.md)*

### 3. Identity Hardening
Use `SOUL.md` to specify the "Vibe" and "Edge" of the agent, ensuring consistent output across different LLM models.

## 📂 Skill Contents

- `templates/`: Base templates for `agent.yaml`, `SOUL.md`, `DUTIES.md`.
- `spec/`: Full SPECIFICATION.md for deep reference.

---

> [!TIP]
> Use this standard to make your agents "Enterprise-Ready". A project with a `DUTIES.md` is 10x more trustworthy for legal stakeholders.
