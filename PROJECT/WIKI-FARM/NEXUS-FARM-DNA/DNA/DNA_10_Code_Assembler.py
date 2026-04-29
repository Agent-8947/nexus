#!/usr/bin/env python3
"""
NEXUS AGENTIC ASSEMBLER v5.0 [WEAK-MODEL OPTIMIZED]
=====================================================
FIX [M-03]: Returns success=False on IOError
FIX [S-01]: Integrates DNA_21_Scaffold_Generator (v3.0, 8 roles)
FIX [S-02]: Ollama auto-fill with constrained prompts for weak models
FIX [S-03]: Falls back to scaffold-only mode if Ollama is offline
FIX [S-06]: Self-Repair Loop — validate → fix errors → revalidate (max 3 passes)
FIX [S-07]: Improved markdown cleaning (handles all model output quirks)
"""

import ast
import json
import sys
import requests
from pathlib import Path
from datetime import datetime

# ── Config ──────────────────────────────────────────────────────────────
DNA_DIR        = Path(__file__).resolve().parent
SYNTHESIS_CORE = DNA_DIR / "DNA_04_Synthesis_Core.json"
RENDER_DIR     = DNA_DIR / "DNA_12_AST_RENDER"
PORTAL_DIR     = DNA_DIR / "DNA_PORTAL"
LOG_FILE       = DNA_DIR / "assembler_log.jsonl"
OLLAMA_URL     = "http://localhost:11434/api/generate"
OLLAMA_MODEL   = "qwen2.5-coder:3b"
MAX_REPAIR_ATTEMPTS = 3
# ────────────────────────────────────────────────────────────────────────

sys.path.insert(0, str(DNA_DIR))

sys.path.insert(0, str(DNA_DIR))
from DNA_Utils import sort_and_number_agent


def _ollama_available() -> bool:
    """Check if Ollama is reachable."""
    try:
        resp = requests.get("http://localhost:11434", timeout=2)
        return resp.status_code == 200
    except Exception:
        return False


def _call_ollama(prompt: str, timeout: int = 180) -> str | None:
    """Call Ollama with error handling."""
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"num_ctx": 8000, "temperature": 0.15}
        }
        resp = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
        if resp.status_code == 200:
            return resp.json().get("response", "")
    except Exception as e:
        print(f"  [!] Ollama error: {e}")
    return None


def _clean_code_output(raw: str) -> str:
    """Strip all markdown wrappers, explanatory text, and extract pure Python.

    Handles these weak-model quirks:
    - ```python ... ``` wrappers
    - Leading/trailing explanations
    - Multiple code blocks (takes the largest)
    - Accidental HTML tags
    """
    text = raw.strip()

    # Strategy 1: Extract from ```python ... ``` block (take largest)
    import re
    blocks = re.findall(r'```(?:python)?\s*\n(.*?)```', text, re.DOTALL)
    if blocks:
        return max(blocks, key=len).strip()

    # Strategy 2: Find the line starting with #!/usr/bin or import
    lines = text.split('\n')
    start_idx = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(('#!/', 'import ', 'from ', '"""', "'''")):
            start_idx = i
            break

    # Find last meaningful Python line (ignore trailing explanation)
    end_idx = len(lines)
    for i in range(len(lines) - 1, start_idx, -1):
        stripped = lines[i].strip()
        if stripped and not stripped.startswith(('Note:', 'This ', 'The above', '---', '**')):
            end_idx = i + 1
            break

    return '\n'.join(lines[start_idx:end_idx]).strip()


def _quick_syntax_check(code: str) -> tuple[bool, str]:
    """Fast syntax validation. Returns (ok, error_message)."""
    try:
        ast.parse(code)
        return True, ""
    except SyntaxError as e:
        return False, f"SyntaxError line {e.lineno}: {e.msg}"


def _generate_scaffold(request: dict) -> str:
    """Generate code scaffold from DNA_21_Scaffold_Generator v3.0."""
    try:
        from DNA_21_Scaffold_Generator import generate_scaffold
        return generate_scaffold(request)
    except ImportError:
        print("  [!] DNA_21_Scaffold_Generator not found. Using minimal template.")
        child_id = request.get("child_id", "UNKNOWN_AGENT")
        return f'''#!/usr/bin/env python3
"""
{child_id} [NEXUS SYNTHESIZED]
"""
import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("{child_id}")

def main():
    parser = argparse.ArgumentParser(description="{child_id}")
    parser.add_argument("--target", default=".", help="Target")
    args = parser.parse_args()
    logger.info("[*] Agent started")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {{e}}")
        sys.exit(1)
'''


def _build_fill_prompt(scaffold: str, request: dict) -> str:
    """Build a highly constrained prompt optimized for weak (3B) models.

    Key principles for weak model prompts:
    1. Show EXACT input → EXACT expected output format
    2. Minimize creative freedom — fill small gaps only
    3. Repeat constraints multiple times
    4. Use short, direct sentences
    """
    child_id = request.get("child_id", "UNKNOWN")
    mission  = request.get("mission", "")
    parent_a = request.get("parent_a", {}).get("node_id", "?")
    parent_b = request.get("parent_b", {}).get("node_id", "?")

    # Count [FILL:*] blocks to tell model exactly how many to replace
    import re
    fill_blocks = re.findall(r'\[FILL:\w+\]', scaffold)
    fill_count = len(fill_blocks)

    return f"""TASK: Complete this Python file by replacing {fill_count} [FILL:*] comments.

AGENT: {child_id}
PARENTS: {parent_a} + {parent_b}
MISSION: {mission}

CRITICAL RULES:
- Inject specific domain-related packages (e.g., requests, bs4, socket, pandas).
- Prefer using `@dataclass` for state representation or output mapping.
- Make sure variables have at least generic type annotations (`list[dict]`, `str`, `Path`).
- Output ONLY Python code. No explanations. No markdown.
- Keep ALL existing code exactly as-is.
- Replace each [FILL:*] comment with 3-10 lines of Python.
- Do NOT use eval(), exec(), pickle, os.system().
- Do NOT remove any import, function, or class.
- Start output with #!/usr/bin/env python3

INPUT FILE:
{scaffold}

OUTPUT (complete Python file):"""


def _build_repair_prompt(broken_code: str, error: str) -> str:
    """Build a repair prompt after validation failure.

    Even weaker models can fix a specific syntax error when told exactly what's wrong.
    """
    return f"""FIX this Python file. It has an error:

ERROR: {error}

Fix ONLY the error. Do not change anything else. Output the complete fixed file.
Start with #!/usr/bin/env python3

BROKEN FILE:
{broken_code}

FIXED FILE:"""


def _fill_and_repair(scaffold: str, request: dict) -> tuple[str, str]:
    """Fill scaffold with Ollama + self-repair loop.

    Returns (final_code, status).
    Status: CODE_GENERATED | SCAFFOLD_REPAIRED | SCAFFOLD_ONLY
    """
    # Phase 1: Initial fill
    prompt = _build_fill_prompt(scaffold, request)
    raw_result = _call_ollama(prompt, timeout=180)

    if not raw_result:
        return scaffold, "SCAFFOLD_ONLY"

    code = _clean_code_output(raw_result)

    # Phase 2: Validate + Self-Repair Loop
    for attempt in range(1, MAX_REPAIR_ATTEMPTS + 1):
        ok, error = _quick_syntax_check(code)
        if ok:
            status = "CODE_GENERATED" if attempt == 1 else "SCAFFOLD_REPAIRED"
            print(f"  [REPAIR] Attempt {attempt}: PASS ✓")
            return code, status

        print(f"  [REPAIR] Attempt {attempt}: FAIL — {error}")

        if attempt < MAX_REPAIR_ATTEMPTS:
            repair_prompt = _build_repair_prompt(code, error)
            repair_result = _call_ollama(repair_prompt, timeout=120)
            if repair_result:
                code = _clean_code_output(repair_result)
            else:
                break  # Ollama failed, use scaffold fallback

    # All repair attempts failed — return scaffold (guaranteed valid)
    print(f"  [REPAIR] All {MAX_REPAIR_ATTEMPTS} attempts failed. Using scaffold.")
    return scaffold, "SCAFFOLD_ONLY"


def synthesize(parent_a: dict, parent_b: dict, mission: str = "", dry_run: bool = False) -> dict:
    """
    Creates an agent synthesis request AND generates code.
    v5.0: Scaffold → Ollama Fill → Self-Repair → Write file.
    """
    child_id = f"{parent_a['node_id']}__X__{parent_b['node_id']}"
    print(f"\n[ASSEMBLER v5.0] Synthesis: {child_id}")

    try:
        PORTAL_DIR.mkdir(exist_ok=True, parents=True)
        RENDER_DIR.mkdir(exist_ok=True, parents=True)

        request = {
            "child_id":  child_id,
            "parent_a":  parent_a,
            "parent_b":  parent_b,
            "mission":   mission,
            "ts":        datetime.now().isoformat()
        }

        # Save request JSON
        req_file = PORTAL_DIR / f"REQ_{child_id}.json"
        req_file.write_text(
            json.dumps(request, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        # Phase 1: Generate scaffold (90%+ complete code)
        print(f"  [1/4] Scaffold generation (8-role templates)...")
        scaffold = _generate_scaffold(request)

        # Phase 2+3: Ollama fill + self-repair
        ollama_ok = _ollama_available()
        if ollama_ok and not dry_run:
            print(f"  [2/4] Ollama fill + repair loop (max {MAX_REPAIR_ATTEMPTS} passes)...")
            final_code, status = _fill_and_repair(scaffold, request)
        else:
            reason = "dry_run" if dry_run else "ollama_offline"
            # v6.0: Use Domain Block Composer instead of generic scaffold
            try:
                from DNA_23_Domain_Blocks import compose_agent
                traits_a = parent_a.get("evolution_matrix", {}).get("traits_fixed", {})
                traits_b = parent_b.get("evolution_matrix", {}).get("traits_fixed", {})
                domain_a = traits_a.get("domain", "infra")
                domain_b = traits_b.get("domain", "infra")
                role = traits_a.get("role", "collector")
                gen_a = parent_a.get("evolution_matrix", {}).get("lineage", {}).get("generation", 0)
                gen_b = parent_b.get("evolution_matrix", {}).get("lineage", {}).get("generation", 0)
                gen = max(gen_a, gen_b) + 1
                final_code = compose_agent(
                    child_id=child_id,
                    mission=mission,
                    parent_a=parent_a["node_id"],
                    parent_b=parent_b["node_id"],
                    domain_a=domain_a,
                    domain_b=domain_b,
                    role=role,
                    generation=gen,
                )
                status = f"DOMAIN_COMPOSED({domain_a}+{domain_b})"
                print(f"  [2/4] Domain Block Composer ({domain_a}+{domain_b}, {reason}).")
            except Exception as e:
                print(f"  [2/4] Scaffold only ({reason}, composer error: {e}).")
                final_code = scaffold
                status = "SCAFFOLD_ONLY"

        # Phase 4: Write synthesized agent
        agent_file = RENDER_DIR / f"HYBRID_{parent_a['node_id']}_x_{parent_b['node_id']}_synthesized_agent.py"
        agent_file.write_text(final_code, encoding="utf-8")
        
        # FIX [SORT]: Automatic categorization and renumbering
        try:
            sorted_path = sort_and_number_agent(agent_file)
            agent_file = sorted_path
            print(f"  [3/4] Sorted & Numbered: {agent_file.parent.name}/{agent_file.name}")
        except Exception as e:
            print(f"  [3/4] Written (Sort failed: {e}): {agent_file.name}")

        print(f"  [4/4] Status: {status}")

        # Phase 5: Validation & Pattern Bank
        test_pass = False
        errors = []
        try:
            import subprocess
            res = subprocess.run(["python", str(agent_file), "--test"], capture_output=True, text=True, timeout=15)
            if res.returncode == 0:
                test_pass = True
            else:
                errors.append(res.stderr.strip()[:200])
        except Exception as e:
            errors.append(str(e))

        try:
            from DNA_26_Pattern_Bank import PatternBank, SynthesisRecord, compute_code_hash, compute_fitness
            bank = PatternBank()
            code_hash = compute_code_hash(final_code)
            fitness = compute_fitness(final_code, test_pass, errors)
            
            import re
            patterns_used = ""
            if "(" in status:
                matches = re.findall(r"\((.*?)\)", status)
                if matches:
                    patterns_used = matches[0]

            blocks_used = []
            if "DOMAIN_COMPOSED" in status:
                # rough extraction of called blocks
                blocks_used = list(set(
                    re.findall(r"\[([a-z_]+)] \d+ findings", final_code) + 
                    re.findall(r"\[([a-z_]+)] OK", final_code) + 
                    re.findall(r"\[([a-z_]+)] stats collected", final_code)
                ))

            rec = SynthesisRecord(
                child_id=child_id,
                parent_a=parent_a["node_id"],
                parent_b=parent_b["node_id"],
                domain_a=parent_a.get("evolution_matrix", {}).get("traits_fixed", {}).get("domain", "infra"),
                domain_b=parent_b.get("evolution_matrix", {}).get("traits_fixed", {}).get("domain", "infra"),
                role=parent_a.get("evolution_matrix", {}).get("traits_fixed", {}).get("role", "collector"),
                generation=parent_a.get("evolution_matrix", {}).get("lineage", {}).get("generation", 0) + 1,
                status=status,
                fitness_score=fitness,
                fill_coverage=1.0 - (final_code.count("[FILL:") / max(len(final_code.splitlines()), 1)),
                test_pass=test_pass,
                schema_valid=True,
                code_hash=code_hash,
                code_lines=len(final_code.splitlines()),
                patterns_used=json.dumps(blocks_used) if "DOMAIN_COMPOSED" in status else "[]",
                errors=json.dumps(errors),
                timestamp=datetime.now().isoformat(),
            )
            bank.record_synthesis(rec)
            bank.close()
        except ImportError:
            pass

        # Log
        log_entry = {
            "ts": request["ts"],
            "child_id": child_id,
            "status": status,
            "file": str(agent_file),
            "ollama_used": ollama_ok and not dry_run,
            "test_pass": test_pass,
            "version": "6.0"
        }
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

        return {
            "success":   True,
            "child_id":  child_id,
            "status":    status,
            "file_path": str(agent_file),
            "req_file":  str(req_file)
        }

    except OSError as e:
        print(f"\033[91m[ASSEMBLER] IOError: {e}\033[0m")
        return {"success": False, "child_id": child_id, "error": str(e)}


if __name__ == "__main__":
    print("[NEXUS] DNA_10_Code_Assembler v5.0 [Weak-Model Optimized]")
    print("  Use DNA_09_Mission_Control.py to launch synthesis.")
    print(f"  Scaffold roles: 8 | Self-repair passes: {MAX_REPAIR_ATTEMPTS}")
    print(f"  Ollama target: {OLLAMA_MODEL}")
