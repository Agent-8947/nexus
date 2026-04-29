#!/usr/bin/env python3
"""
NEXUS Evaluator v1.1
FIX [H-07]: gene_expression_rate checks libs from DNA_08 renderer_map for node's traits,
             NOT a hardcoded list.
"""
import ast
import json
import re
import sys
from pathlib import Path

# Locate DNA_08_Engine_Config.json relative to engine dir
ENGINE_DIR  = Path(__file__).resolve().parent
DNA_DIR     = ENGINE_DIR.parent.parent.parent   # .../DNA/
CONFIG_PATH = DNA_DIR / "DNA_08_Engine_Config.json"


def _get_expected_frameworks(child_traits: dict) -> list[str]:
    """
    FIX [H-07]: Read expected frameworks from DNA_08 renderer_map
    based on child's actual traits.
    """
    try:
        if CONFIG_PATH.exists():
            config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            for renderer in config.get("renderer_map", []):
                cond = renderer.get("condition", {})
                # Check if all condition keys match child traits
                if all(child_traits.get(k) == v for k, v in cond.items()):
                    return renderer.get("frameworks", [])
    except Exception:
        pass
    # Fallback: generic quality libs
    return ["logging", "argparse"]


class NexusEvaluator:
    """Audit engine for generated agents."""

    def __init__(self):
        self.security_keywords = ["fernet", "sha256", "cryptography", "hashlib", "getpass", "sanitize"]
        self.io_keywords = ["open(", "requests.", "subprocess.", "sqlite3.", "pd.read_", "connect("]

    def evaluate(self, script_path: Path, child_json_path: Path) -> dict:
        with open(child_json_path, 'r', encoding='utf-8') as f:
            child = json.load(f)
        child_traits = child.get("traits", {})

        code = script_path.read_text(encoding='utf-8')
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            msg = f"Syntax Error: {str(e)}"
            print(f"[EVALUATOR] CRITICAL: {msg}")
            report = {
                "child_id":       child["child_id"],
                "generation":     child.get("generation", 0),
                "scores":         {"syntax_valid": 0.0},
                "failures":       [msg],
                "improvements":   [],
                "overall_fitness": 0.0
            }
            report_path = script_path.parent / f"EVAL_{script_path.stem}.json"
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
            return report

        scores       = {}
        failures     = []
        improvements = []

        # 1. Gene Expression Rate -- FIX [H-07]: use traits-specific frameworks
        expected_libs = _get_expected_frameworks(child_traits)
        expressed = sum(1 for lib in expected_libs if lib.lower() in code.lower())
        scores["gene_expression_rate"] = expressed / max(len(expected_libs), 1)
        if expressed < len(expected_libs):
            missing = [l for l in expected_libs if l.lower() not in code.lower()]
            failures.append(f"Expected libraries not found: {', '.join(missing)}")
        else:
            improvements.append(f"All expected frameworks expressed ({', '.join(expected_libs)})")

        # 2. Mock detection
        has_mock_calls = bool(re.search(r'random\.|np\.random|time\.sleep', code))
        scores["has_mocks"] = 0.0 if has_mock_calls else 1.0
        if has_mock_calls:
            failures.append("Detected mock/stub logic (random/sleep calls)")
        else:
            improvements.append("Zero mock logic detected")

        # 3. Real I/O
        has_io = any(kw in code for kw in self.io_keywords)
        scores["has_real_io"] = 1.0 if has_io else 0.0
        if not has_io:
            failures.append("No real I/O operations found")
        else:
            improvements.append("Real I/O implemented")

        # 4. Error Handling
        try_blocks = [n for n in ast.walk(tree) if isinstance(n, ast.Try)]
        scores["has_error_handling"] = 1.0 if try_blocks else 0.0
        if not try_blocks:
            failures.append("Missing try/except blocks")
        else:
            improvements.append("Error handling present")

        # 5. Security
        sec_level = child_traits.get("security", child.get("traits", {}).get("security", "none"))
        if sec_level != "none":
            has_sec = any(kw in code.lower() for kw in self.security_keywords)
            scores["security_implemented"] = 1.0 if has_sec else 0.0
            if not has_sec:
                failures.append(f"Security={sec_level} required but no security primitives found")
        else:
            scores["security_implemented"] = 1.0

        # 6. Logging
        has_log = "logging." in code or "logger." in code
        scores["has_logging"] = 1.0 if has_log else 0.0
        if not has_log:
            failures.append("No logging infrastructure")
        else:
            improvements.append("Logging implemented")

        overall = sum(scores.values()) / len(scores)

        report = {
            "child_id":       child["child_id"],
            "generation":     child.get("generation", 0),
            "scores":         scores,
            "failures":       failures,
            "improvements":   improvements,
            "overall_fitness": round(overall, 3)
        }

        report_path = script_path.parent / f"EVAL_{script_path.stem}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        print(f"[EVALUATOR] Report: {report_path.name} | Fitness: {overall:.3f}")
        return report


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: evaluator.py <script_path> <child_json_path>")
        sys.exit(1)
    evaluator = NexusEvaluator()
    evaluator.evaluate(Path(sys.argv[1]), Path(sys.argv[2]))
