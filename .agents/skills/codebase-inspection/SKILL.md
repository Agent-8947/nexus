---
name: codebase-inspection
description: |
  Analyze codebases using pygount for LOC counting, language breakdown, and code-vs-comment ratios.
  Use when asked to check lines of code, repo size, language composition, or codebase stats.

  USE FOR:
  - Lines of code (LOC) counts across a project
  - Language breakdown and percentages
  - File counts per language
  - Code vs comment ratios
  - "How big is this repo?" questions
  - Pre-refactor codebase audits

version: 1.0.0
author: NousResearch/hermes-agent (ported to NEXUS by Antigravity)
license: MIT
metadata:
  hermes:
    tags: [LOC, code-analysis, pygount, codebase, metrics, repository, audit]
    category: software-development
---

# Codebase Inspection with pygount

Analyze repositories for lines of code, language breakdown, file counts, and code-vs-comment ratios.

## When to Use

- "Сколько строк кода в проекте?"
- "Какие языки используются в репозитории?"
- "Размер кодовой базы?"
- "Соотношение кода к комментариям?"
- Pre-refactor baseline measurement
- NEXUS project health audits

## Prerequisites

```powershell
pip install pygount
```

## 1. Basic Summary (Most Common)

```powershell
cd "e:\Downloads\--ANTIGRAVITY store\IDE-optimus\PROJECT\<project-name>"

pygount --format=summary `
  --folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,.eggs,*.egg-info" `
  .
```

**CRITICAL:** Always use `--folders-to-skip` — without it pygount crawls all dependencies and may take minutes or hang.

## 2. Common Folder Exclusions by Project Type

```powershell
# Python projects
--folders-to-skip=".git,venv,.venv,__pycache__,.cache,dist,build,.tox,.eggs,.mypy_cache"

# JavaScript / TypeScript / Node projects
--folders-to-skip=".git,node_modules,dist,build,.next,.cache,.turbo,coverage"

# General catch-all (use this when unsure)
--folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,vendor,third_party"
```

## 3. Filter to Specific Language

```powershell
# Only Python files
pygount --suffix=py --format=summary .

# Python + YAML
pygount --suffix=py,yaml,yml --format=summary .

# JavaScript + TypeScript
pygount --suffix=js,ts,jsx,tsx --format=summary .
```

## 4. Detailed File-by-File Output

```powershell
# Per-file breakdown
pygount --folders-to-skip=".git,node_modules,venv" .

# Top 20 largest files by code lines (PowerShell sort)
pygount --folders-to-skip=".git,node_modules,venv" . | Sort-Object -Descending | Select-Object -First 20
```

## 5. Output Formats

```powershell
# Summary table (recommended)
pygount --format=summary .

# JSON for programmatic use
pygount --format=json . | ConvertFrom-Json

# Cloc-compatible format
pygount --format=cloc-xml .
```

## 6. Interpreting Results

Summary table columns:
- **Language** — detected programming language
- **Files** — number of files
- **Code** — executable/declarative lines
- **Comment** — comment/doc lines
- **%** — percentage of total

Special pseudo-languages:
- `__empty__` — empty files
- `__binary__` — binary files (images, compiled)
- `__generated__` — auto-generated files
- `__duplicate__` — files with identical content
- `__unknown__` — unrecognized extensions

## Pitfalls

1. **Always exclude `.git`, `node_modules`, `venv`** — critical on large projects
2. **Markdown shows 0 code lines** — pygount classifies all Markdown as comments (expected)
3. **JSON files show low code counts** — use `wc -l` / `(Get-Content file).Count` for raw line counts
4. **Large monorepos** — use `--suffix` to target specific languages

## NEXUS Integration

Quick audit of entire NEXUS project:

```powershell
cd "e:\Downloads\--ANTIGRAVITY store\IDE-optimus\PROJECT"
pygount --format=summary `
  --folders-to-skip=".git,node_modules,venv,.venv,__pycache__,dist,build,.firecrawl" `
  .
```

---
*Ported from NousResearch/hermes-agent by Antigravity NEXUS*
