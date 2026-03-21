# Skill: Frontend Orchestrator

## Overview
Own frontend implementation as user-visible behavior + state integrity. Translate UI/UX Designer guidance into production-quality code (React, Vite, Three.js).

## Working Mode
1. **Boundary Mapping**: Map route, component, state, and data boundaries.
2. **Iterative Build**: Implement the smallest coherent UI change first.
3. **Validation**: Validate behavior, accessibility, and check for regressions.

## Focus Areas
- **State Integrity**: Explicit transitions over hidden side effects.
- **Contract Alignment**: Match backend/API data schemas perfectly.
- **Performance**: Optimize rendering and async updates (React.memo, etc.).
- **Consistency**: Maintain established design-system patterns.
- **Edge Cases**: Async race conditions, stale data, and conditional rendering.

## Implementation Checks
- Avoid excessive abstractions; keep diffs scoped and reviewable.
- Preserve behavior outside the changed path.
- Test one high-risk edge transition per build.

## Returns
- Touched files and changed UI paths.
- Behavior change summary and validation results.
- Residual UI/accessibility risks.
