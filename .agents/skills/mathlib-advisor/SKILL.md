# Skill: MathLib-Advisor

**Mathematics & Formal Logic Knowledge Base**
*Formal proof search and exploration via Lean 4 Mathlib.*

## Description
This skill integrates the **mathlib4** repository (Lean 4 proof library) into NEXUS. It allows the agent to search for mathematical theorems, find formal definitions, and explain logic based on the world's most comprehensive library of formalized mathematics.

## Capabilities
- **find**: Search for theorems, lemmas, or definitions by name.
- **show**: Display the source code of a specific Lean module.
- **search**: Broad search across the mathematical categories.

## Prerequisites
- No external dependencies required for searching (Python stdlib).
- (Optional) Lean 4 and `lake` for executing/verifying proofs.

## Commands
### Find a Theorem
```powershell
python "e:\Downloads\--ANTIGRAVITY store\IDE-optimus\.agents\skills\mathlib-advisor\scripts\mathlib_search.py" find "Cauchy"
```

### Show Module Content
```powershell
python "e:\Downloads\--ANTIGRAVITY store\IDE-optimus\.agents\skills\mathlib-advisor\scripts\mathlib_search.py" show "Mathlib.Data.Real.Basic"
```

## Structure
- **source/**: Shallow clone of `leanprover-community/mathlib4`.
- **scripts/mathlib_search.py**: Search engine logic.

## Integration for Agents
When the user asks for mathematical proof, definition, or logic, use `find` to locate the relevant Lean 4 theorem, then use its formal name to explain the concept.
