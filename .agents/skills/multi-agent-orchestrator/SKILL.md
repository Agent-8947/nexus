# Skill: Multi-Agent Orchestrator

## Overview
Use when a task needs a concrete multi-agent plan with clear role separation, dependencies, and result integration. Maximize parallel progress without losing integration control.

## Working Mode
1. **Task Mapping**: Map task graph into critical-path work and parallel sidecar opportunities.
2. **Role Assignment**: Assign roles with explicit ownership and disjoint write scopes.
3. **Contracts**: Define dependency and wait points with clear integration contracts.
4. **Reconciliation**: Plan reconciliation of results, conflicts, and follow-up branches.

## Focus Areas
- Local-first handling of immediate blockers before delegation.
- Role fit between task complexity and agent capability.
- Parallelization boundaries to avoid duplicate/conflicting edits.
- Explicit output schemas and wait strategies.
- Merge/conflict risk control for concurrent implementation tasks.

## Quality Checks
- Verify every delegated task is materially useful and non-overlapping.
- Confirm exactly one owner per write-critical scope.
- Check dependency ordering for hidden blocking edges.
- Ensure integration checklist exists before launch.

## Returns
- Multi-agent plan (Local vs Delegated split).
- Per-agent ownership, objective, and output contract.
- Dependency/integration timeline.
- Conflict-resolution strategy.
