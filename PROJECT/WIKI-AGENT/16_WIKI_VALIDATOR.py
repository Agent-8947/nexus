#!/usr/bin/env python3
"""
NEXUS AGENT 12  VALIDATOR (Torture Mode)
Mission: Stress-test every generated module. Zero tolerance for crashes.
"""

import os
import sys
import json
import importlib.util
from pathlib import Path
from datetime import datetime

# Path Configuration
PROJECT_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI-PROJECT")
BUILD_DIR = PROJECT_ROOT / "BUILD_OUTPUT"

class NexusValidatorAgent:
    def __init__(self):
        self.test_cases = [
            None,                           # NoneType Test
            "",                             # Empty String
            "   ",                          # Whitespace only
            "user@example.com",             # Email handle (extraction test)
            "UPPERCASE_USER",               # Case normalization test
            "https://example.com/path?q=1", # Full URL with path/query
            "127.0.0.1",                    # Raw IP
            "malicious' OR 1=1;--",         # Injection attempt
        ]

    def torture_module(self, mod_path: Path):
        """Tortures a single module with a suite of dirty inputs."""
        mod_name = mod_path.stem
        report = {"module": mod_name, "passed": 0, "failed": 0, "errors": []}
        
        # 1. Static Analysis: Syntax Check
        try:
            with open(mod_path, 'r', encoding='utf-8') as f:
                compile(f.read(), str(mod_path), 'exec')
        except SyntaxError as e:
            return {"module": mod_name, "status": "CRASHED", "error": f"Syntax Error: {e}"}
        except Exception as e:
            return {"module": mod_name, "status": "CRASHED", "error": f"Read Error: {e}"}

        # 2. Dynamic Analysis: Import Check
        try:
            spec = importlib.util.spec_from_file_location(mod_name, str(mod_path))
            mod = importlib.util.module_from_spec(spec)
            sys.path.insert(0, str(mod_path.parent))
            spec.loader.exec_module(mod)
            if not hasattr(mod, "run"):
                return {"module": mod_name, "status": "SKIPPED", "note": "No run() method found"}
        except Exception as e:
            return {"module": mod_name, "status": "CRASHED", "error": f"Import/Runtime Error: {e}"}

        # 3. Torture Chamber (Adversarial Runtime)
        from concurrent.futures import ThreadPoolExecutor
        
        for case in self.test_cases:
            try:
                # Use executor to enforce timeout on the run() call
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(mod.run, case)
                    res = future.result(timeout=30) # 30s limit per case
                
                if isinstance(res, dict):
                    report["passed"] += 1
                else:
                    report["failed"] += 1
                    report["errors"].append(f"Case [{case}] returned {type(res)} instead of dict")
            except Exception as e:
                report["failed"] += 1
                report["errors"].append(f"Case [{case}] ERROR/TIMEOUT: {e}")

        status = "PASSED" if report["failed"] == 0 else "FAILED"
        return {"module": mod_name, "status": status, "stats": report}

    def validate_build(self, build_path: Path) -> bool:
        """Goes through the entire build directory and validates every .py file in src/."""
        src_dir = build_path / "src"
        if not src_dir.exists():
            print(f"[!] Error: src directory not found in {build_path}")
            return False

        print(f"\n============================================================")
        print(f"  NEXUS AGENT 12  VALIDATOR v1.0 (Torture Mode)")
        print(f"  Target: {build_path.name}")
        print(f"============================================================\n")

        all_results = []
        modules = sorted(list(src_dir.glob("*.py")))
        
        for mod_path in modules:
            # Skip orchestrators from input torture, but ensure they exist
            if mod_path.name in ["shadow_cli.py", "__init__.py"]:
                continue
            
            res = self.torture_module(mod_path)
            all_results.append(res)
            
            symbol = "" if res["status"] == "PASSED" else "" if res["status"] == "FAILED" else ""
            print(f"  {symbol} {res['module']:20} | Status: {res['status']}")
            
            if res["status"] in ["FAILED", "CRASHED"]:
                err_msg = res.get("error", "")
                if err_msg: print(f"     [!] {err_msg}")
                for err in res.get("stats", {}).get("errors", []):
                    print(f"     [!] {err}")

        # Final Verdict
        failed = sum(1 for r in all_results if r["status"] == "FAILED")
        crashed = sum(1 for r in all_results if r["status"] == "CRASHED")
        
        print(f"\n============================================================")
        if failed == 0 and crashed == 0:
            print(f"   FINAL VERDICT: BUILD CLEAN / STABLE")
            print(f"============================================================\n")
            return True
        else:
            print(f"   FINAL VERDICT: BUILD REJECTED ({failed} failures, {crashed} crashes)")
            print(f"============================================================\n")
            return False

if __name__ == "__main__":
    validator = NexusValidatorAgent()
    # Check current directory if no specific build provided
    target_build = None
    if len(sys.argv) > 1:
        target_build = Path(sys.argv[1])
    else:
        # Fallback to latest TEST build in BUILD_DIR
        test_builds = sorted(list(BUILD_DIR.glob("TEST_*")), key=os.path.getmtime)
        if test_builds:
            target_build = test_builds[-1]

    if target_build and target_build.exists():
        success = validator.validate_build(target_build)
        # Exit code reflects success for CI/CD integration
        sys.exit(0 if success else 1)
    else:
        print("[!] No build found to validate.")
        sys.exit(1)
