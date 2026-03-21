---
name: adversarial-reviewer
description: AI-driven autonomous code and architecture critique tool. Forces the agent to attack its own solutions before finalizing.
---

# 🕵️ Adversarial Reviewer [NEXUS Edition]

**Rule**: NEVER skip the Adversarial Review phase for new architectural solutions.

## Concept
Before you (the Agent) output final code or modify critical logic, you must draft your code locally in a temporary space (e.g. `tmp/`) and run this rigorous Static Analysis/Review bot. It acts as the "Devil's Advocate" to find anti-patterns, fatal logic flaws, and weak spots.

## Usage
Run the python script to analyze complexity and potential failures before writing code to disk.

```bash
python "e:/Downloads/--ANTIGRAVITY store/IDE-NEXUS/PROJECT/skills/adversarial-reviewer/scripts/reviewer.py" "path_to_draft_file.py"
```

## Logic Gate
- If the reviewer returns **Exit Code 0**: The code is S-Tier. You may proceed and assemble it into the working project.
- If it returns **Warnings**: You MUST refine the code until it passes. Zero-Guessing Validation.
