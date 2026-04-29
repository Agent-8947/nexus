#!/usr/bin/env python3
"""
NEXUS SYNTHESIS VALIDATOR v1.1
================================
FIX [H-05]: Auto-detect is_critical from DNA_04 node metadata
FIX [M-04]: L4 DANGER_PATTERNS scoped correctly -- FastAPI allowed for api-interface nodes
Levels:
  L1 -- Syntax (ast.parse)
  L2 -- Imports (static analysis)
  L3 -- Structure (main, argparse, error handling)
  L4 -- Security (dangerous patterns, context-aware)
"""

import ast
import json
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime

DNA_DIR        = Path(__file__).resolve().parent
RENDER_DIR     = DNA_DIR / "DNA_12_AST_RENDER"
VALIDATION_LOG = DNA_DIR / "validation_log.jsonl"
SYNTHESIS_CORE = DNA_DIR / "DNA_04_Synthesis_Core.json"

# FIX [M-04]: Separated into context-aware rule sets
# These patterns are ALWAYS forbidden regardless of node type
ALWAYS_DANGER = [
    r"eval\s*\(",                    # No uncontrolled eval
    r"pickle\.loads",                # No deserialization
    r"exec\s*\(",                    # No exec
]

# These patterns are forbidden ONLY for critical security_level nodes with CLI interface
# (i.e., they must NOT expose public network endpoints)
CRITICAL_CLI_DANGER = [
    r"BaseHTTPServer|HTTPServer",    # No raw HTTP servers in critical CLI tools
    r"uvicorn\.run.*host\s*=\s*[\"']0\.0\.0\.0",  # No public binding in critical tools
]

# OS shell injection -- forbidden for critical nodes, warning for others
SHELL_INJECTION = [
    r"os\.system\s*\(",
    r"subprocess\.Popen.*shell\s*=\s*True",
]

QUALITY_CHECKS = {
    "has_main_guard":    r'if\s+__name__\s*==\s*["\']__main__["\']',
    "has_argparse":      r"argparse|ArgumentParser",
    "has_error_handling": r"try:|except\s+\w+|except\s*:",
    "has_logging":       r"logging\.|loguru|logger\.",
}


@dataclass
class ValidationResult:
    file:          str
    passed:        bool  = True
    level:         str   = ""
    errors:        list  = field(default_factory=list)
    warnings:      list  = field(default_factory=list)
    quality_score: float = 0.0
    details:       dict  = field(default_factory=dict)


def _load_node_metadata(file_path: Path) -> dict:
    """FIX [H-05]: Load node metadata from DNA_04 to auto-detect security context."""
    try:
        if not SYNTHESIS_CORE.exists():
            return {}
        dna = json.loads(SYNTHESIS_CORE.read_text(encoding="utf-8"))
        node_id = file_path.stem.replace("_synthesized_agent", "").upper()
        for node in dna.get("NODES", []):
            if node["node_id"] == node_id:
                return node["evolution_matrix"]["traits_fixed"]
    except Exception:
        pass
    return {}


def _is_critical_node(file_path: Path, explicit_critical: bool) -> tuple[bool, str]:
    """
    FIX [H-05]: Auto-determine criticality from DNA metadata.
    Returns (is_critical, interface_type).
    """
    if explicit_critical:
        return True, "unknown"
    traits = _load_node_metadata(file_path)
    security_level = traits.get("security_level", "none")
    interface      = traits.get("interface", "cli")
    is_critical    = security_level in ("critical", "high")
    return is_critical, interface


def validate_syntax(code: str, result: ValidationResult) -> bool:
    """L1: Syntax check via ast.parse."""
    try:
        ast.parse(code)
        result.details["syntax"] = "OK"
        return True
    except SyntaxError as e:
        result.errors.append(f"SyntaxError (line {e.lineno}): {e.msg}")
        result.level = "L1"
        return False


def validate_imports(code: str, result: ValidationResult) -> bool:
    """L2: Static import analysis via AST."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False

    stdlib_safe = {
        "os", "sys", "re", "json", "time", "datetime", "pathlib", "argparse",
        "subprocess", "logging", "collections", "itertools", "functools",
        "math", "random", "hashlib", "base64", "socket", "urllib", "http",
        "typing", "dataclasses", "abc", "io", "struct", "threading", "asyncio",
        "contextlib", "copy", "enum", "warnings", "inspect", "importlib",
        "shutil", "tempfile", "uuid", "platform",
        "sqlite3", "hmac", "csv", "textwrap", "signal", "glob", "fnmatch",
        "secrets", "configparser", "xml", "html", "email", "unittest",
        "pdb", "cProfile", "traceback", "multiprocessing", "queue",
        "statistics", "decimal", "fractions", "operator", "string",
        "binascii", "codecs", "gzip", "zipfile", "tarfile", "ctypes",
        "array", "bisect", "heapq", "weakref", "types", "pprint",
    }
    pip_allowed = {
        "aiohttp", "requests", "numpy", "rich", "loguru", "scipy", "torch",
        "fastapi", "uvicorn", "pydantic", "httpx", "click", "typer",
        "colorama", "tqdm", "pandas", "sklearn", "scapy", "cryptography",
        "transformers", "accelerate",
        "psutil", "beautifulsoup4", "bs4", "selenium", "Pillow", "PIL",
        "matplotlib", "seaborn", "plotly", "jinja2", "yaml", "toml",
        "dotenv", "paramiko", "docker", "redis", "celery",
    }

    unknown_imports = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.Import):
                names = [alias.name.split(".")[0] for alias in node.names]
            else:
                names = [node.module.split(".")[0]] if node.module else []
            for name in names:
                if name and name not in stdlib_safe and name not in pip_allowed:
                    unknown_imports.append(name)

    if unknown_imports:
        result.warnings.append(f"Unknown imports (may need pip install): {', '.join(set(unknown_imports))}")
    result.details["imports"] = {"unknown": list(set(unknown_imports))}
    return True


def validate_security(code: str, is_critical: bool, interface: str, result: ValidationResult) -> bool:
    """
    L4: Context-aware security check.
    FIX [M-04]: FastAPI/uvicorn NOT forbidden for api-interface nodes.
    """
    found_always = []
    for pattern in ALWAYS_DANGER:
        if re.search(pattern, code, re.IGNORECASE):
            found_always.append(pattern)

    if found_always:
        result.errors.append(f"Security violation (always forbidden): {found_always}")
        result.level = "L4"
        return False

    if is_critical and interface in ("cli", "library", "protocol"):
        # FIX [M-04]: Only check CRITICAL_CLI_DANGER for non-API critical nodes
        found_critical = []
        for pattern in CRITICAL_CLI_DANGER + SHELL_INJECTION:
            if re.search(pattern, code, re.IGNORECASE):
                found_critical.append(pattern)
        if found_critical:
            result.errors.append(f"Security violation (critical+cli node): {found_critical}")
            result.level = "L4"
            return False
    elif is_critical and interface == "api":
        # API nodes: allow FastAPI but warn about shell injection
        for pattern in SHELL_INJECTION:
            if re.search(pattern, code, re.IGNORECASE):
                result.warnings.append(f"Shell injection risk in api node: {pattern}")
    elif not is_critical:
        # Soft check for non-critical: warnings only
        for pattern in SHELL_INJECTION:
            if re.search(pattern, code, re.IGNORECASE):
                result.warnings.append(f"Potential shell injection (use subprocess list form): {pattern}")

    result.details["security"] = f"OK (critical={is_critical}, interface={interface})"
    return True


def calculate_quality(code: str, result: ValidationResult) -> float:
    """L3: Code structure quality score (0.0 – 1.0)."""
    passed_checks = 0
    check_results = {}

    for check_name, pattern in QUALITY_CHECKS.items():
        found = bool(re.search(pattern, code, re.IGNORECASE))
        check_results[check_name] = found
        if found:
            passed_checks += 1

    score = round(passed_checks / len(QUALITY_CHECKS), 2)
    result.details["quality_checks"] = check_results
    result.quality_score = score

    if score < 0.5:
        result.warnings.append(f"Low structure quality: {score:.0%}")

    return score


def validate_file(file_path: Path, is_critical: bool = False) -> ValidationResult:
    """Full 4-level validation of a single file."""
    result = ValidationResult(file=str(file_path))

    if not file_path.exists():
        result.passed = False
        result.errors.append(f"File not found: {file_path}")
        return result

    code = file_path.read_text(encoding="utf-8")

    # FIX [H-05]: Auto-detect criticality and interface from DNA metadata
    auto_critical, interface = _is_critical_node(file_path, is_critical)
    result.details["auto_critical"] = auto_critical
    result.details["interface"]     = interface

    # L1
    if not validate_syntax(code, result):
        result.passed = False
        return result

    # L2
    validate_imports(code, result)

    # L3
    calculate_quality(code, result)

    # L4
    if not validate_security(code, auto_critical, interface, result):
        result.passed = False
        return result

    result.passed = len(result.errors) == 0
    result.level  = "WARN" if result.warnings else ("OK" if result.passed else "FAIL")
    return result


def validate_all_renders(verbose: bool = True) -> dict:
    """Validate all files in DNA_12_AST_RENDER directory."""
    if not RENDER_DIR.exists():
        print(f"[!] AST_RENDER directory not found: {RENDER_DIR}")
        return {"total": 0, "passed": 0, "failed": 0}

    py_files = list(RENDER_DIR.glob("*.py"))
    if not py_files:
        print("[!] No files to validate in AST_RENDER/")
        return {"total": 0, "passed": 0, "failed": 0}

    passed, failed = 0, 0
    results = []

    print(f"\n[VALIDATOR] Checking {len(py_files)} files in AST_RENDER/\n")
    print(f"{'File':<55} {'Status':<10} {'Quality':<10} {'Warnings'}")
    print("-" * 100)

    for f in sorted(py_files):
        r = validate_file(f)   # FIX [H-05]: auto_critical from DNA metadata
        status    = "[V] OK" if r.passed else f"[X] {r.level}"
        warn_count = len(r.warnings)
        print(f"{f.name:<55} {status:<10} {r.quality_score:<10.0%} {warn_count} warn(s)")
        if verbose and r.errors:
            for err in r.errors:
                print(f"  [ERR] {err}")
        if verbose and r.warnings:
            for w in r.warnings:
                print(f"  [WRN] {w}")

        if r.passed:
            passed += 1
        else:
            failed += 1

        results.append({
            "ts":       datetime.now(datetime.timezone.utc).isoformat() if hasattr(datetime, 'timezone') else datetime.utcnow().isoformat(),
            "file":     f.name,
            "passed":   r.passed,
            "level":    r.level,
            "quality":  r.quality_score,
            "errors":   r.errors,
            "warnings": r.warnings
        })

    with open(VALIDATION_LOG, "a", encoding="utf-8") as log:
        for entry in results:
            log.write(json.dumps(entry, ensure_ascii=False) + "\n")

    summary = {"total": len(py_files), "passed": passed, "failed": failed}
    print(f"\n{'='*60}")
    print(f"[VALIDATOR] TOTAL={summary['total']} | [V]={passed} | [X]={failed}")
    print(f"{'='*60}\n")
    return summary


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="NEXUS Synthesis Validator v1.1")
    parser.add_argument("--file",     help="Validate specific file")
    parser.add_argument("--all",      action="store_true", help="Validate all files in AST_RENDER/")
    parser.add_argument("--critical", action="store_true", help="Force L4 critical checks")
    args = parser.parse_args()

    if args.file:
        r = validate_file(Path(args.file), is_critical=args.critical)
        print(json.dumps({
            "file":          r.file,
            "passed":        r.passed,
            "level":         r.level,
            "quality_score": r.quality_score,
            "errors":        r.errors,
            "warnings":      r.warnings,
            "details":       r.details
        }, indent=2, ensure_ascii=False))
    elif args.all:
        validate_all_renders()
    else:
        parser.print_help()
