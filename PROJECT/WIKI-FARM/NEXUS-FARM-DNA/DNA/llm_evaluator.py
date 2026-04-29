import glob
import json
import ast
import re
from pathlib import Path

# Domains and weights
DOMAINS = {
    "DNA_SECURITY_ADV": {
        "security": 0.30, "error_handling": 0.20, "no_mock_logic": 0.15,
        "syntax_and_output_validity": 0.15, "gene_expression_rate": 0.10, "real_io": 0.05, "logging_observability": 0.05
    },
    "DNA_AI_ML": {
        "gene_expression_rate": 0.30, "real_io": 0.20, "logging_observability": 0.15,
        "syntax_and_output_validity": 0.15, "no_mock_logic": 0.10, "error_handling": 0.05, "security": 0.05
    },
    "DNA_INFRA": {
        "error_handling": 0.25, "real_io": 0.25, "logging_observability": 0.20,
        "syntax_and_output_validity": 0.10, "gene_expression_rate": 0.10, "no_mock_logic": 0.05, "security": 0.05
    },
    "DNA_WEB": {
        "syntax_and_output_validity": 0.25, "gene_expression_rate": 0.25, "no_mock_logic": 0.20,
        "real_io": 0.10, "error_handling": 0.10, "security": 0.05, "logging_observability": 0.05
    }
}
DEFAULT_WEIGHTS = {
    "syntax_and_output_validity": 0.15, "gene_expression_rate": 0.20, "no_mock_logic": 0.10,
    "real_io": 0.15, "error_handling": 0.15, "security": 0.15, "logging_observability": 0.10
}

TIERS = [
    (0.95, 1.00, "S (Production-ready)"),
    (0.85, 0.95, "A (High quality)"),
    (0.70, 0.85, "B (Good with gaps)"),
    (0.55, 0.70, "C (Functional)"),
    (0.30, 0.55, "D (Prototype only)"),
    (0.00, 0.30, "F (Failed)"),
]

def get_tier(score):
    for low, high, label in TIERS:
        if low <= score <= high:
            return label
    return "F (Failed)"

class LLMEvaluator:
    def __init__(self):
        self.security_keywords = ["fernet", "sha256", "cryptography", "hashlib", "getpass", "sanitize", "pbkdf2", "argon2", "bcrypt"]
        self.io_keywords = ["open(", "requests.", "subprocess.", "sqlite3.", "pd.read_", "connect(", "session.get"]

    def evaluate(self, script_path, domain):
        code = script_path.read_text(encoding='utf-8', errors='ignore')
        scores = {}
        issues = []
        
        # 1. Syntax Valid
        try:
            tree = ast.parse(code)
            scores["syntax_and_output_validity"] = 1.0
        except SyntaxError as e:
            scores["syntax_and_output_validity"] = 0.0
            issues.append(f"Syntax Error: {e}")
            tree = None
            
        # 2. Gene Expression (Mock logic for framework detect)
        expected_libs = ["logging", "asyncio", "pydantic", "sklearn", "requests", "fastapi"]
        expressed = sum(1 for lib in expected_libs if lib in code.lower())
        expr_score = expressed / 3.0
        scores["gene_expression_rate"] = min(1.0, expr_score)
        if expr_score == 0:
             issues.append("Low expected framework usage")

        # 3. No Mock Logic (time.sleep in retry/backoff context is legitimate)
        has_random = bool(re.search(r'random\.|np\.random', code))
        has_sleep_mock = bool(re.search(r'time\.sleep', code)) and not re.search(r'(retry|backoff|rate.limit|attempt)', code, re.IGNORECASE)
        has_stubs = bool(re.search(r'\bTODO\b|(?<!=\s)pass\s*\n|(?<!\w)mock(?!\w)|(?<!\w)dummy(?!\w)', code))
        has_mock_calls = has_random or has_sleep_mock or has_stubs
        scores["no_mock_logic"] = 0.0 if has_mock_calls else 1.0
        if has_mock_calls:
            issues.append("Detected mock logic or placeholders")

        # 4. Real I/O
        has_io = any(kw in code for kw in self.io_keywords)
        scores["real_io"] = 1.0 if has_io else 0.0
        if not has_io:
             issues.append("No real I/O operations")

        # 5. Error handling
        if tree:
            try_blocks = [n for n in ast.walk(tree) if isinstance(n, ast.Try)]
            if len(try_blocks) > 2:
                scores["error_handling"] = 1.0
            elif try_blocks:
                scores["error_handling"] = 0.75
            else:
                scores["error_handling"] = 0.0
                issues.append("Missing or weak error handling")
        else:
             scores["error_handling"] = 0.0

        # 6. Security
        has_sec = any(kw in code.lower() for kw in self.security_keywords)
        scores["security"] = 1.0 if has_sec else 0.0

        # 7. Logging
        has_log = "logging." in code or "logger." in code
        if "logging.basicConfig" in code or "setLevel" in code:
            scores["logging_observability"] = 1.0
        elif has_log:
            scores["logging_observability"] = 0.75
        else:
            scores["logging_observability"] = 0.0
            issues.append("No logging")

        weights = DOMAINS.get(domain, DEFAULT_WEIGHTS)
        
        if scores["syntax_and_output_validity"] == 0.0:
             overall_fitness = 0.0
        else:
             overall_fitness = sum(scores[k] * weights.get(k, 0.1) for k in scores)

        return overall_fitness, scores, issues

def main():
    root = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI-FARM\NEXUS-FARM-DNA\DNA")
    evaluator = LLMEvaluator()
    reports = {}

    for domain_dir in root.glob("DNA_*"):
        if not domain_dir.is_dir():
             continue
        domain_name = domain_dir.name
        reports[domain_name] = []
        for py_file in domain_dir.glob("*.py"):
            fitness, scores, issues = evaluator.evaluate(py_file, domain_name)
            reports[domain_name].append({
                 "file": py_file.name,
                 "fitness": fitness,
                 "tier": get_tier(fitness),
                 "issues": issues,
                 "scores": scores
            })

    output_lines = ["# 🧬 NEXUS DNA LLM Model Rating Report\n"]
    output_lines.append("*Based on DNA_20_SPAWNER/engine/evaluator.py principles.*\n")
    
    for domain, items in reports.items():
        if not items:
             continue
        output_lines.append(f"## {domain}")
        avg_fitness = sum(i["fitness"] for i in items) / len(items) if items else 0
        output_lines.append(f"**Domain Average Fitness:** {avg_fitness:.3f} ({get_tier(avg_fitness)})\n")
        
        for item in sorted(items, key=lambda x: x["fitness"], reverse=True):
             output_lines.append(f"### {item['file']} → Tier: **{item['tier']}** | Score: `{item['fitness']:.3f}`")
             if item["issues"]:
                  output_lines.append(f"  - **Issues:** {', '.join(item['issues'])}")
        output_lines.append("\n")

    report_path = root / "DNA_RATING_REPORT.md"
    report_path.write_text("\n".join(output_lines), encoding="utf-8")
    print(f"Report generated successfully at:\n{report_path}")

if __name__ == "__main__":
    main()
