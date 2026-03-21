# 🧠 NEXUS ARCHITECTURAL FINDINGS

## 🏛️ Decision Log

### [FIND-001] React-PDF v4 Migration

- **Context**: The existing `msedge --print-to-pdf` method was unreliable for "Luxury Tech" aesthetics.
- **Decision**: Switched to `@react-pdf/renderer` v4.3.2.
- **Impact**: True vector rendering, sub-millisecond generation, and component-based layouts.
- **Risk**: Requires `Yoga Layout` compatibility and explicit font registration for non-system fonts.

### [FIND-002] IPC Performance Strategy

- **Context**: Target throughput is 100,000 msg/s on 6GB RAM hardware.
- **Decision**: Utilize Windows Named Pipes (IPC) to bypass interpreter-level network overhead.
- **Impact**: Provides "Metal-level" communication speed while maintaining Python/TS flexibility.

### [FIND-003] Persistent Planning (Manus-style)

- **Context**: AI context window limitations for long-term project management.
- **Decision**: Implementation of `task_plan.md`, `findings.md`, and `progress.md`.
- **Impact**: Guarantees project state continuity across sessions.

## ⚠️ Known Issues / Gotchas

- **Font Registration**: Calling `Font.register` with URLs can fail in restricted environments; prefer local TTF/WOFF2.
- **Node.js Versions**: Using node v24.13.0 - ensure compatibility with all native PDF modules.
