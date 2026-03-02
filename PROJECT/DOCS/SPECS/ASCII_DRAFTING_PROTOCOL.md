# NEXUS ASCII Architecture Tooling

v1.0 | Status: ACTIVE

## 🎨 Overview

ASCIIFlow allows for creating clean, text-based diagrams that are perfect for:

- Terminal-based documentation.
- Embedding in `CONSTITUTION.md` and `SPECS/`.
- Git-friendly architecture maps.

## 🛠 Integration into NEXUS

Instead of just "using" the website, we integrate ASCII diagramming into our agentic workflow.

### 1. The Skill: `nexus-ascii-draw`

- **Location**: `PROJECT/skills/nexus-ascii-draw/`
- **Standard**: All diagrams in `SPECS/` should have an ASCII version for CLI viewing.

### 2. Implementation Pattern

When a new architectural component is proposed, the agent generates an ASCII representation.

#### Example: NEXUS Memory Flow

```text
+----------------+       +-------------------+       +-----------------+
|  Hot Memory    | <---> | NEXUS Orchestrator| <---> |  Cold Memory    |
| (CONSTITUTION) |       |   (Polymorphic)   |       |  (SPECS Repository)
+----------------+       +-------------------+       +-----------------+
           ^                        |                        ^
           |                        v                        |
           |             +-------------------+               |
           +-------------|   memory.json     |---------------+
                         |   (State Sync)    |
                         +-------------------+
```

## 🚀 Deployment Plan

1. **Local Tooling**: If bazel is available, we can run a private instance.
2. **Template Library**: Create `PROJECT/templates/ascii/` for common blocks (Database, API, Worker).
3. **CLI Bridge**: Use ASCII generators to visualize state in the terminal.
