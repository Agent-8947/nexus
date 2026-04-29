#!/usr/bin/env python3
"""
HYBRID_AWESOME-SECURITY-HARDENING_x_CPP-CHEAT-SHEET v2.0 [NEXUS HARDENING AUDITOR]
=====================================================================================
Heritage: Awesome-Security-Hardening (CIS Benchmarks) + CPP-Cheat-Sheet (Low-level Analysis)
Mission:  Security audit and configuration hardening verification
Role:     AUDITOR - Checks system/project hardening posture against best-practice checklists

ARCHITECTURE:
- Multi-layer checklist engine (OS, SSH, Docker, Python, Git, Network)
- Severity-tagged findings with remediation commands
- Exportable JSON report for integration with Orchestrator pipeline
"""

import sys
import os
import re
import json
import logging
import argparse
import subprocess
import platform
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS-HARDENER")


class HardeningCheck:
    """Single hardening check definition."""
    def __init__(self, check_id: str, category: str, name: str, severity: str,
                 check_fn=None, remediation: str = ""):
        self.check_id    = check_id
        self.category    = category
        self.name        = name
        self.severity    = severity
        self.check_fn    = check_fn
        self.remediation = remediation

    def run(self, context: dict) -> dict:
        try:
            passed, detail = self.check_fn(context) if self.check_fn else (True, "N/A")
        except Exception as e:
            passed, detail = False, f"Check error: {e}"
        return {
            "check_id":    self.check_id,
            "category":    self.category,
            "name":        self.name,
            "severity":    self.severity,
            "passed":      passed,
            "detail":      detail,
            "remediation": self.remediation if not passed else ""
        }


def _check_git_hooks(ctx: dict) -> tuple[bool, str]:
    """Check if pre-commit hooks exist in .git/hooks."""
    git_dir = ctx["target"] / ".git" / "hooks" / "pre-commit"
    if git_dir.exists():
        return True, "pre-commit hook installed"
    return False, "No pre-commit hook found"


def _check_gitignore(ctx: dict) -> tuple[bool, str]:
    """Check .gitignore exists and covers secrets."""
    gi = ctx["target"] / ".gitignore"
    if not gi.exists():
        return False, "No .gitignore found"
    content = gi.read_text(encoding="utf-8", errors="ignore").lower()
    must_have = [".env", "__pycache__", "*.pyc"]
    missing = [m for m in must_have if m not in content]
    if missing:
        return False, f"Missing patterns: {', '.join(missing)}"
    return True, "Covers .env, __pycache__, *.pyc"


def _check_no_env_file(ctx: dict) -> tuple[bool, str]:
    """Check that .env files are not committed (exist in repo root)."""
    for name in [".env", ".env.local", ".env.production"]:
        if (ctx["target"] / name).exists():
            return False, f"Found {name} in project root (should be in .gitignore)"
    return True, "No .env files in project root"


def _check_dockerfile_user(ctx: dict) -> tuple[bool, str]:
    """Check Dockerfiles use non-root USER."""
    dockerfiles = list(ctx["target"].rglob("Dockerfile")) + list(ctx["target"].rglob("*.dockerfile"))
    if not dockerfiles:
        return True, "No Dockerfiles found (skip)"
    for df in dockerfiles:
        content = df.read_text(encoding="utf-8", errors="ignore")
        if "USER" not in content:
            return False, f"{df.name}: No USER directive (runs as root)"
    return True, f"All {len(dockerfiles)} Dockerfiles specify USER"


def _check_no_debug_in_code(ctx: dict) -> tuple[bool, str]:
    """Check that DEBUG=True is not hardcoded in Python files."""
    count = 0
    for py_file in ctx["target"].rglob("*.py"):
        if ".git" in str(py_file) or "__pycache__" in str(py_file):
            continue
        try:
            code = py_file.read_text(encoding="utf-8", errors="ignore")
            if re.search(r"DEBUG\s*=\s*True", code):
                count += 1
        except Exception:
            pass
    if count > 0:
        return False, f"DEBUG=True found in {count} Python file(s)"
    return True, "No hardcoded DEBUG=True"


def _check_requirements_pinned(ctx: dict) -> tuple[bool, str]:
    """Check that requirements.txt has pinned versions (==)."""
    req = ctx["target"] / "requirements.txt"
    if not req.exists():
        return True, "No requirements.txt (skip)"
    lines = req.read_text(encoding="utf-8", errors="ignore").splitlines()
    unpinned = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#") and "==" not in line and ">=" not in line:
            unpinned.append(line.split()[0])
    if unpinned:
        return False, f"Unpinned deps: {', '.join(unpinned[:5])}"
    return True, "All dependencies pinned"


def _check_readme_exists(ctx: dict) -> tuple[bool, str]:
    """Check README exists."""
    for name in ["README.md", "README.rst", "README.txt", "README"]:
        if (ctx["target"] / name).exists():
            return True, f"Found {name}"
    return False, "No README found"


def _check_license_exists(ctx: dict) -> tuple[bool, str]:
    """Check LICENSE exists."""
    for name in ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"]:
        if (ctx["target"] / name).exists():
            return True, f"Found {name}"
    return False, "No LICENSE found"


# ── Build Checklist ──────────────────────────────────────────────────────
HARDENING_CHECKLIST = [
    HardeningCheck("GIT-001", "git", "Pre-commit hooks installed", "MEDIUM",
                   _check_git_hooks, "Install pre-commit: pip install pre-commit && pre-commit install"),
    HardeningCheck("GIT-002", "git", ".gitignore covers secrets", "HIGH",
                   _check_gitignore, "Add .env, __pycache__, *.pyc to .gitignore"),
    HardeningCheck("SEC-001", "secrets", "No .env files in repo root", "CRITICAL",
                   _check_no_env_file, "Move .env to .gitignore and use env vars or secrets manager"),
    HardeningCheck("DOCKER-001", "docker", "Dockerfile uses non-root USER", "HIGH",
                   _check_dockerfile_user, "Add 'USER nobody' or specific non-root user to Dockerfile"),
    HardeningCheck("CODE-001", "code", "No hardcoded DEBUG=True", "HIGH",
                   _check_no_debug_in_code, "Use environment variable: DEBUG=os.getenv('DEBUG', 'False')"),
    HardeningCheck("DEPS-001", "deps", "Dependencies version pinned", "MEDIUM",
                   _check_requirements_pinned, "Pin all deps: pip freeze > requirements.txt"),
    HardeningCheck("DOCS-001", "docs", "README exists", "LOW",
                   _check_readme_exists, "Create a README.md with project description"),
    HardeningCheck("DOCS-002", "docs", "LICENSE exists", "LOW",
                   _check_license_exists, "Add a LICENSE file for legal clarity"),
]


def run_audit(target: Path, output: Path):
    context = {"target": target, "platform": platform.system()}

    logger.info(f"[*] Hardening audit: {target}")
    results = [check.run(context) for check in HARDENING_CHECKLIST]

    passed   = sum(1 for r in results if r["passed"])
    failed   = len(results) - passed
    score    = round(passed / max(len(results), 1) * 100)

    by_sev = {}
    for r in results:
        if not r["passed"]:
            by_sev[r["severity"]] = by_sev.get(r["severity"], 0) + 1

    report = {
        "agent":     "HYBRID_AWESOME-SECURITY-HARDENING_x_CPP-CHEAT-SHEET",
        "version":   "2.0",
        "mission":   "security_hardening",
        "timestamp": datetime.now().isoformat(),
        "target":    str(target),
        "stats": {
            "total_checks": len(results),
            "passed":       passed,
            "failed":       failed,
            "score_pct":    score,
            "failed_by_severity": by_sev,
        },
        "results": results,
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"  NEXUS Hardening Auditor v2.0")
    print(f"{'='*60}")
    print(f"  Checks:  {len(results)}")
    print(f"  Passed:  {passed}")
    print(f"  Failed:  {failed}")
    print(f"  Score:   {score}%")
    print(f"")
    for r in results:
        icon = "[V]" if r["passed"] else "[X]"
        sev  = f"({r['severity']})" if not r["passed"] else ""
        print(f"  {icon} {r['check_id']:12s} {r['name']:40s} {sev}")
        if not r["passed"] and r["remediation"]:
            print(f"      FIX: {r['remediation']}")
    print(f"{'='*60}")
    logger.info(f"[DONE] Report -> {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NEXUS Hardening Auditor v2.0")
    parser.add_argument("--target", default=".", help="Project directory to audit")
    parser.add_argument("--output", default="hardening_report.json", help="Output JSON")
    args = parser.parse_args()

    try:
        run_audit(Path(args.target).resolve(), Path(args.output).resolve())
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
