# NEXUS CONSTITUTION

v1.0 | Status: ACTIVE | Invariant Enforcement: MANDATORY

## 1. Core Principles

- **Agnostic Excellence**: All logic must be decoupled from specific hardware where possible.
- **Agentic Integrity**: Every action must be logged in `memory.json`. No silent changes.
- **Fail-Fast Protocol**: If uncertainty > 30%, stop and trigger Ambiguity Gate.

## 2. Architectural Invariants

- **Stack Purity**:
  - Frontend: Astro v5 (Statics) / Next.js 15 (Dynamic).
  - Backend: FastAPI (Main) / Python 3.13.
  - Automation: nexus-system-control skills.
- **Communication**: Use `api_bridge.py` for cross-context data exchange.
- **File System**: Absolute paths only. Project root is `PROJECT/`.

## 3. Memory & Documentation (arXiv:2602.20478)

- **Hot Memory**: This file (`CONSTITUTION.md`). Read at start of EVERY session.
- **Cold Memory**: `PROJECT/DOCS/SPECS/*.md`. One spec per major feature.
- **State**: `PROJECT/memory.json`. Key-value store for current system state.

## 4. 3D Forge Standards (NEW)

- **Language**: Python (`build123d`) or OpenSCAD for parametric design.
- **Output**: `.stl` or `.step` files saved in `PROJECT/outputs/3d/`.
- **Optimization**: All designs must consider FDM printing constraints (overhangs, bed adhesion).

## 5. Fault Management

- Every error must be documented in `PROJECT/fault_registry.json` via `/+` workflow.
- Critical architectural changes require manual override in `memory.json`.

## 6. Visual Standards (ASCII)

- **Tooling**: Use `asciiflow` standards for all documentation diagrams.
- **Requirement**: Every `SPECS/` document must contain an ASCII architecture map for terminal-based review.
- **Consistency**: Use `+--+` for boxes and `|` for lines. No "fancy" unicode characters that might break in older shells.
