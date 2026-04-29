#!/usr/bin/env python3
"""
NEXUS FUNCTIONAL TESTER v1.0 (L5)
===================================
Layer 2: Executes synthesized agents in a sandbox to verify they actually work.
Adds L5 (Functional) on top of DNA_11's L1-L4 (Static) checks.

Tests:
  L5a: --help exits 0 (argparse works)
  L5b: Dry-run with test args exits 0 (basic execution)
  L5c: stdout is not empty (produces output)
  L5d: Minimum LOC check (not a trivial stub)
  L5e: Has real I/O operations (not just print)
"""

import sys
import json
import subprocess
import tempfile
import logging
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS-L5")

DNA_DIR    = Path(__file__).resolve().parent
RENDER_DIR = DNA_DIR / "DNA_12_AST_RENDER"

MIN_LOC          = 40       # Minimum lines of code (excluding blanks/comments)
TIMEOUT_SECONDS  = 15       # Max execution time
MAX_STDERR_LINES = 10       # Lines of stderr to capture


@dataclass
class L5Result:
    file:        str
    passed:      bool          = True
    tests:       dict          = field(default_factory=dict)
    errors:      list          = field(default_factory=list)
    stdout_len:  int           = 0
    exit_code:   int           = -1
    loc:         int           = 0
    has_real_io: bool          = False


def count_loc(code: str) -> int:
    """Count logical lines of code (non-blank, non-comment)."""
    count = 0
    for line in code.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            count += 1
    return count


def check_real_io(code: str) -> bool:
    """Check if code contains real I/O beyond print()."""
    io_markers = [
        "open(",            # File I/O
        ".read_text(",      # Pathlib read
        ".write_text(",     # Pathlib write
        "json.load",        # JSON I/O
        "json.dump",        # JSON write
        "requests.",        # HTTP
        "subprocess.",      # Process
        "os.walk(",         # Directory traversal
        ".rglob(",          # Recursive glob
        ".glob(",           # Glob
        "socket.",          # Network
        "urllib.",           # URL
        "hashlib.",         # Crypto
        "sqlite3.",         # Database
    ]
    return any(marker in code for marker in io_markers)


def run_subprocess(cmd: list, timeout: int = TIMEOUT_SECONDS) -> tuple[int, str, str]:
    """Run a command with timeout. Returns (exit_code, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(RENDER_DIR)
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"
    except Exception as e:
        return -1, "", str(e)


def test_agent(file_path: Path) -> L5Result:
    """Run all L5 functional tests on a single agent file."""
    result = L5Result(file=file_path.name)

    code = file_path.read_text(encoding="utf-8", errors="ignore")

    # ── L5d: LOC check ───────────────────────────────────────────────
    result.loc = count_loc(code)
    result.tests["L5d_min_loc"] = result.loc >= MIN_LOC
    if result.loc < MIN_LOC:
        result.errors.append(f"Too few LOC: {result.loc} (min: {MIN_LOC})")

    # ── L5e: Real I/O ────────────────────────────────────────────────
    result.has_real_io = check_real_io(code)
    result.tests["L5e_real_io"] = result.has_real_io
    if not result.has_real_io:
        result.errors.append("No real I/O operations found (only print?)")

    # ── L5a: --help test ─────────────────────────────────────────────
    exit_code, stdout, stderr = run_subprocess(
        [sys.executable, str(file_path), "--help"]
    )
    result.tests["L5a_help_exits_0"] = exit_code == 0
    if exit_code != 0:
        result.errors.append(f"--help failed (exit {exit_code}): {stderr[:200]}")

    # ── L5b: Dry-run test ────────────────────────────────────────────
    # Create a temp target dir for agents that need --target
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create a dummy file so collectors have something to scan
        dummy = Path(tmp_dir) / "test_file.py"
        dummy.write_text('# test\npassword = "secret123"\nDEBUG = True\n', encoding="utf-8")

        tmp_output = Path(tmp_dir) / "test_output.json"

        # Try common arg patterns
        test_args_candidates = [
            ["--target", tmp_dir, "--output", str(tmp_output)],
            ["--input", str(tmp_output), "--output", str(tmp_output)],
            ["--target", tmp_dir],
            [],
        ]

        best_exit = -1
        best_stdout = ""
        for args in test_args_candidates:
            exit_code, stdout, stderr = run_subprocess(
                [sys.executable, str(file_path)] + args
            )
            if exit_code == 0:
                best_exit = 0
                best_stdout = stdout
                break
            elif exit_code != -1 and best_exit == -1:
                best_exit = exit_code
                best_stdout = stdout

        result.exit_code = best_exit
        result.tests["L5b_dryrun_exits_0"] = best_exit == 0
        if best_exit != 0:
            result.errors.append(f"Dry-run failed (exit {best_exit})")

    # ── L5c: Non-empty output ────────────────────────────────────────
    result.stdout_len = len(best_stdout)
    result.tests["L5c_output_nonempty"] = len(best_stdout) > 0
    if len(best_stdout) == 0:
        result.errors.append("Agent produced no stdout output")

    # ── Overall ──────────────────────────────────────────────────────
    result.passed = all(result.tests.values())
    return result


def test_all(verbose: bool = True) -> dict:
    """Test all agents in AST_RENDER."""
    py_files = sorted(RENDER_DIR.glob("HYBRID_*_synthesized_agent.py"))
    if not py_files:
        py_files = sorted(RENDER_DIR.glob("*_synthesized_agent.py"))

    print(f"\n[L5 FUNCTIONAL TESTER] Testing {len(py_files)} agents\n")
    print(f"{'Agent':<55} {'LOC':>5} {'I/O':>4} {'Help':>5} {'Run':>4} {'Out':>4} {'RESULT':>8}")
    print("-" * 95)

    passed, failed = 0, 0
    results = []

    for f in py_files:
        r = test_agent(f)
        icon = "[V]" if r.passed else "[X]"
        t = r.tests
        print(
            f"{f.name:<55} "
            f"{r.loc:>5} "
            f"{'Y' if t.get('L5e_real_io') else 'N':>4} "
            f"{'Y' if t.get('L5a_help_exits_0') else 'N':>5} "
            f"{'Y' if t.get('L5b_dryrun_exits_0') else 'N':>4} "
            f"{'Y' if t.get('L5c_output_nonempty') else 'N':>4} "
            f"{icon:>8}"
        )
        if verbose and r.errors:
            for e in r.errors:
                print(f"  [!] {e}")

        if r.passed:
            passed += 1
        else:
            failed += 1
        results.append({
            "file": r.file, "passed": r.passed, "loc": r.loc,
            "tests": r.tests, "errors": r.errors
        })

    print(f"\n{'='*60}")
    print(f"[L5] TOTAL={len(py_files)} | PASS={passed} | FAIL={failed}")
    print(f"{'='*60}\n")

    # Save log
    log_path = DNA_DIR / "l5_functional_log.jsonl"
    with open(log_path, "a", encoding="utf-8") as f:
        for entry in results:
            entry["ts"] = datetime.now().isoformat()
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    return {"total": len(py_files), "passed": passed, "failed": failed, "results": results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NEXUS L5 Functional Tester")
    parser.add_argument("--file",    help="Test a specific agent file")
    parser.add_argument("--all",     action="store_true", help="Test all agents in AST_RENDER/")
    parser.add_argument("--quiet",   action="store_true", help="Suppress error details")
    args = parser.parse_args()

    if args.file:
        r = test_agent(Path(args.file))
        print(json.dumps({
            "file": r.file, "passed": r.passed, "loc": r.loc,
            "tests": r.tests, "errors": r.errors
        }, indent=2))
    elif args.all:
        test_all(verbose=not args.quiet)
    else:
        parser.print_help()
