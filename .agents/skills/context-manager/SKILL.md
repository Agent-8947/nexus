# Skill: Context Manager

## Overview
Own context packaging as signal curation for subagents and complex tasks. Produce compact, execution-ready context that improves accuracy while avoiding noise/bloat.

## Working Mode
1. **Mapping**: Map task-relevant architecture, modules, and ownership boundaries.
2. **Extraction**: Extract constraints, conventions, and invariants from repository evidence.
3. **Compression**: Compress into a minimal packet with file/symbol anchors and open questions.
4. **Highlighting**: Highlight unknowns that can change execution strategy (e.g., missing API keys, env vars).

## Focus Areas
- **Signal vs. Noise**: Omit irrelevant repo details that create context bloat.
- **Terminology Normalization**: Reduce cross-thread/cross-session misunderstanding.
- **Uncertainty Tracking**: Track unresolved design or runtime facts (inferred vs confirmed).
- **Environment Assumptions**: Tooling, OS (Windows), and shell (PowerShell) specific constraints.

## Quality Checks
- Verify each context item directly supports task decisions.
- Confirm references include concrete files/symbols.
- Ensure packet is compact enough for fast "onboarding" of a new task phase.

## Returns
- Concise context packet (Architecture, Constraints, Risks).
- Key files/symbols and why they matter.
- Explicit assumptions and confidence levels.
- Unresolved unknowns and discovery order.
