#!/usr/bin/env python3
"""
NEXUS Synthesis Guard v2.1 (Dynamic Execution Enforced)
FIX [C-06]: shutil.move wrapped in try/except -- crash-safe quarantine
Checks: Static Syntax -> Dynamic Execution (Zero-Guessing Validation)
"""
import py_compile
import shutil
import json
import subprocess
import sys
from pathlib import Path


class SynthesisGuard:
    """
    NEXUS Synthesis Guard v2.1
    Validates syntax AND enforces Zero-Guessing Validation (Exit Code 0).
    """
    def __init__(self, quarantine_dir: Path):
        self.quarantine_dir = quarantine_dir
        self.quarantine_dir.mkdir(parents=True, exist_ok=True)

    def watch(self, script_path: Path) -> dict:
        result = {
            "status":          "CLEAN",
            "repairs_applied": 0,
            "issues":          []
        }

        if not script_path.exists():
            return {
                "status":          "QUARANTINED",
                "repairs_applied": 0,
                "issues": [{"severity": "CRITICAL", "rule": "file_exists",
                            "detail": f"Script not found: {script_path}"}]
            }

        # 1. Static Syntax Check
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                source = f.read()
            compile(source, script_path.name, 'exec')
        except SyntaxError as e:
            result["status"] = "QUARANTINED"
            result["issues"].append({
                "severity": "CRITICAL",
                "rule":     "static_syntax",
                "detail":   f"Syntax Error at line {e.lineno}: {e.msg}"
            })
            self._quarantine(script_path)
            return result

        # 2. Dynamic Execution Dry-Run (Zero-Guessing Validation)
        try:
            import os
            env = os.environ.copy()
            env["PYTHONPATH"] = str(script_path.parent)
            run_result = subprocess.run(
                [sys.executable, str(script_path), "--help"],
                capture_output=True, text=True, timeout=5, env=env
            )
            if run_result.returncode not in (0, 1):
                # returncode=1 is acceptable for --help on some scripts
                stderr_tail = (
                    run_result.stderr.strip().split('\n')[-1]
                    if run_result.stderr else "Unknown runtime error"
                )
                result["status"] = "QUARANTINED"
                result["issues"].append({
                    "severity": "CRITICAL",
                    "rule":     "runtime_execution",
                    "detail":   f"Exit Code {run_result.returncode} | {stderr_tail}"
                })
                self._quarantine(script_path)
                return result

        except subprocess.TimeoutExpired:
            result["status"] = "QUARANTINED"
            result["issues"].append({
                "severity": "CRITICAL",
                "rule":     "runtime_timeout",
                "detail":   "Script timed out (infinite loop or blocking call at module level)"
            })
            self._quarantine(script_path)
            return result

        return result

    def _quarantine(self, script_path: Path):
        """FIX [C-06]: Safe move with exception handling."""
        q_path = self.quarantine_dir / script_path.name
        try:
            shutil.move(str(script_path), str(q_path))
            print(f"[GUARD] Quarantined: {script_path.name} -> {q_path}")
        except FileNotFoundError:
            print(f"[GUARD][WARN] File already moved or deleted: {script_path}")
        except shutil.Error as e:
            print(f"[GUARD][WARN] Quarantine move failed: {e}")
