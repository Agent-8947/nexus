# SPEC-001: NEXUS HOLISTIC ARCHITECTURE MAP

v1.0 | Status: DRAFT | Created: 2026-03-02

## 🗺 System Overview

This is the primary architectural map of the NEXUS ecosystem, integrating the unified stack, memory persistence, and the new 3D-Forge capability.

```text
                               +-----------------------------+
                               |      NEXUS CONSTITUTION     |
                               |    (Hot Memory / Laws)      |
                               +--------------+--------------+
                                              |
                                              v
      +-----------------------+    +-----------------------+    +-----------------------+
      |      FRONTEND         |    |   NEXUS ORCHESTRATOR  |    |        BACKEND        |
      |   (Astro v5 / Next)   | <->|   (Polymorphic AI)    | <->|   (FastAPI / Python)  |
      +-----------+-----------+    +-----------+-----------+    +-----------+-----------+
                  |                            |                            |
                  v                            v                            v
      +-----------------------+    +-----------------------+    +-----------------------+
      |      VISUALS          |    |      MEMORY.JSON      |    |       DATABASE        |
      |   (GSAP / Threlte)    |    |   (Sync State / FS)   |    | (Supabase / SQLite)   |
      +-----------------------+    +-----------+-----------+    +-----------------------+
                                               |
                  +----------------------------+----------------------------+
                  |                                                         |
                  v                                                         v
      +-----------------------+                                 +-----------------------+
      |       3D-FORGE        |                                 |      COLD MEMORY      |
      |  (OpenSCAD / Python)  |                                 |  (DOCS/SPECS/*.md)    |
      +-----------+-----------+                                 +-----------------------+
                  |
                  v
      +-----------------------+
      |   OUTPUTS/3D/*.STL    |
      | (Physical Realization)|
      +-----------------------+
```

## 🛠 Component breakdown

### 1. Control Layer

- **Orchestrator**: Handles task decomposition and agent tool-calling.
- **Constitution**: Enforces architectural invariants (no legacy code, etc).

### 2. Execution Layer

- **Frontend**: Modern web stack (Astro/Next) focused on high-performance visuals.
- **Backend**: Python-driven logic for heavy lifting and hardware interaction.

### 3. Physical Layer (Forge)

- **Parametric Design**: Logic-based 3D modeling for industrial components.

### 4. Persistence Layer

- **State Sync**: Real-time tracking of what is "online".
- **Documentation**: On-demand specs to prevent context window bloat.
