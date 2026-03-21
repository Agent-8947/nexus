---
name: github-pr-workflow
description: |
  Complete GitHub Pull Request lifecycle management.
  Branch creation → commits → push → PR creation → CI monitoring → merge.
  Uses `gh` CLI when available, falls back to `git` + `curl` API calls.

  USE FOR:
  - Creating feature/fix branches and PRs
  - Monitoring CI status after push
  - Auto-fixing CI failures and re-pushing
  - Merging PRs (squash/merge/rebase)
  - Full automated PR lifecycle without leaving the terminal

version: 1.0.0
author: NousResearch/hermes-agent (ported to NEXUS by Antigravity)
license: MIT
metadata:
  hermes:
    tags: [github, git, pr, pull-request, ci, workflow, automation]
    category: software-development
    related_skills: [codebase-inspection]
---

# GitHub Pull Request Workflow

Complete guide for managing the PR lifecycle.
`gh` CLI first, `git` + `curl` fallback for environments without `gh`.

## Prerequisites

- Authenticated with GitHub (`gh auth login` OR `GITHUB_TOKEN` env var)
- Inside a git repository with a GitHub remote

## Quick Auth Detection

```powershell
# Detect available auth method
if (Get-Command gh -ErrorAction SilentlyContinue) {
    gh auth status 2>$null
    $AUTH = "gh"
} else {
    $AUTH = "git"
    # Fallback: use GITHUB_TOKEN env var
}
Write-Host "Using: $AUTH"
```

## Extract Owner/Repo

```powershell
# Works for both HTTPS and SSH remotes
$REMOTE_URL = git remote get-url origin
$OWNER_REPO = $REMOTE_URL -replace '.*github\.com[:/]', '' -replace '\.git$', ''
$OWNER = $OWNER_REPO.Split('/')[0]
$REPO  = $OWNER_REPO.Split('/')[1]
Write-Host "Owner: $OWNER, Repo: $REPO"
```

## 1. Branch Creation

```powershell
# Update main first
git fetch origin
git checkout main; git pull origin main

# Create feature branch (naming conventions below)
git checkout -b feat/add-user-authentication
```

Branch naming:
- `feat/description` — new features
- `fix/description` — bug fixes
- `refactor/description` — code restructuring
- `docs/description` — documentation
- `ci/description` — CI/CD changes

## 2. Making Commits

```powershell
# Stage and commit with Conventional Commits format
git add src/auth.py tests/test_auth.py
git commit -m "feat: add JWT-based user authentication

- Add login/register endpoints
- Add User model with password hashing
- Add auth middleware for protected routes"
```

Commit types: `feat`, `fix`, `refactor`, `docs`, `test`, `ci`, `chore`, `perf`

## 3. Push and Create PR

```powershell
# Push branch
git push -u origin HEAD
```

**With gh:**
```powershell
gh pr create `
  --title "feat: add JWT authentication" `
  --body "## Summary
- Adds login/register API endpoints
- JWT token generation and validation

## Test Plan
- [ ] Unit tests pass

Closes #42"
```

Options: `--draft`, `--reviewer user1,user2`, `--label enhancement`, `--base develop`

**With curl fallback:**
```powershell
$BRANCH = git branch --show-current
$body = @{
    title = "feat: add JWT authentication"
    body  = "Adds login and register API endpoints.`n`nCloses #42"
    head  = $BRANCH
    base  = "main"
} | ConvertTo-Json

Invoke-RestMethod `
  -Method POST `
  -Uri "https://api.github.com/repos/$OWNER/$REPO/pulls" `
  -Headers @{ Authorization = "token $env:GITHUB_TOKEN"; Accept = "application/vnd.github.v3+json" } `
  -Body $body `
  -ContentType "application/json"
```

## 4. Monitor CI Status

**With gh:**
```powershell
gh pr checks          # one-shot
gh pr checks --watch  # poll until complete
```

**With curl:**
```powershell
$SHA = git rev-parse HEAD
$status = Invoke-RestMethod `
  -Uri "https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/status" `
  -Headers @{ Authorization = "token $env:GITHUB_TOKEN" }
Write-Host "Overall: $($status.state)"
$status.statuses | ForEach-Object { Write-Host "  $($_.context): $($_.state)" }
```

## 5. Merging

**With gh:**
```powershell
gh pr merge --squash --delete-branch       # squash merge, clean up
gh pr merge --auto --squash --delete-branch # auto-merge when CI passes
```

**With curl:**
```powershell
$PR_NUMBER = 42
$mergeBody = @{
    merge_method = "squash"
    commit_title = "feat: add authentication (#$PR_NUMBER)"
} | ConvertTo-Json

Invoke-RestMethod `
  -Method PUT `
  -Uri "https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/merge" `
  -Headers @{ Authorization = "token $env:GITHUB_TOKEN" } `
  -Body $mergeBody `
  -ContentType "application/json"
```

Merge methods: `merge` (merge commit), `squash`, `rebase`

## 6. Useful PR Commands Reference

| Action             | gh                                      | curl / PowerShell                             |
|--------------------|------------------------------------------|----------------------------------------------|
| List my PRs        | `gh pr list --author @me`               | `GET /repos/$OWNER/$REPO/pulls?state=open`   |
| View PR diff       | `gh pr diff`                            | `git diff main...HEAD`                       |
| Add comment        | `gh pr comment N --body "..."`          | `POST /repos/$OWNER/$REPO/issues/N/comments` |
| Request review     | `gh pr edit N --add-reviewer user`      | `POST .../pulls/N/requested_reviewers`       |
| Close PR           | `gh pr close N`                         | `PATCH .../pulls/N` `{state: closed}`        |
| Check out PR       | `gh pr checkout N`                      | `git fetch origin pull/N/head:pr-N`          |

## Complete Workflow Example

```powershell
# 1. Start clean
git checkout main; git pull origin main

# 2. Branch
git checkout -b fix/login-redirect-bug

# 3. Make changes (edit files)

# 4. Commit
git add src/auth/login.py tests/test_login.py
git commit -m "fix: correct redirect URL after login"

# 5. Push
git push -u origin HEAD

# 6. Create PR
gh pr create --title "fix: correct redirect URL" --body "Closes #57"

# 7. Monitor CI
gh pr checks --watch

# 8. Merge
gh pr merge --squash --delete-branch
```

---
*Ported from NousResearch/hermes-agent by Antigravity NEXUS*
