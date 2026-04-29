#!/usr/bin/env python3
"""
NEXUS RUN.PY -- Orchestrator with Universal Synthesis Guard v2.1
================================================================
FIX [C-04]: sys.path.insert for local module imports
FIX [M-06]: lineage.json auto-initialized on first run
Flow per generation:
  SPAWN -> GUARD -> EVALUATE -> MUTATE -> loop
"""

import json
import sys
from pathlib import Path

# FIX [C-04]: Ensure engine modules are importable regardless of CWD
ENGINE_DIR   = Path(__file__).resolve().parent
SPAWNER_ROOT = ENGINE_DIR.parent
sys.path.insert(0, str(ENGINE_DIR))

from spawner          import NexusSpawner
from evaluator        import NexusEvaluator
from mutator          import NexusMutator
from synthesis_guard  import SynthesisGuard

GUARD_COLORS = {
    "CLEAN":       "\033[92m",
    "REPAIRED":    "\033[93m",
    "QUARANTINED": "\033[91m",
    "RESET":       "\033[0m",
}


def _print_guard_result(result: dict):
    color = GUARD_COLORS.get(result["status"], "")
    reset = GUARD_COLORS["RESET"]
    print(f"\n[GUARD] {color}{result['status']}{reset} "
          f"| repairs={result['repairs_applied']} "
          f"| issues={len(result['issues'])}")
    for issue in result["issues"]:
        print(f"        [{issue['severity']:8}] {issue['rule']:20} -- {issue['detail']}")


def _ensure_lineage(memory_path: Path):
    """FIX [M-06]: Initialize lineage.json if it doesn't exist."""
    memory_path.parent.mkdir(parents=True, exist_ok=True)
    if not memory_path.exists():
        memory_path.write_text(json.dumps({"lineage": []}, indent=2), encoding="utf-8")
        print(f"[RUN] Initialized lineage.json: {memory_path}")


def orchestrate(child_json_path: Path, max_generations: int = 3):
    memory_path = SPAWNER_ROOT / "memory" / "lineage.json"
    quarantine  = SPAWNER_ROOT / "memory" / "quarantine"

    # FIX [M-06]: Auto-initialize lineage before NexusMutator reads it
    _ensure_lineage(memory_path)

    spawner   = NexusSpawner(ENGINE_DIR)
    evaluator = NexusEvaluator()
    mutator   = NexusMutator(memory_path)
    guard     = SynthesisGuard(quarantine_dir=quarantine)

    current_json = child_json_path

    for gen in range(max_generations):
        print(f"\n{'='*60}")
        print(f" NEXUS EVOLUTION CYCLE: GENERATION {gen}")
        print(f"{'='*60}")

        with open(current_json, encoding="utf-8") as f:
            child_data = json.load(f)
        child_id = child_data["child_id"]

        expected_script = SPAWNER_ROOT / "agents" / f"gen_{gen}" / f"{child_id}.py"

        if expected_script.exists():
            print(f"[RUN] Existing synthesis detected for Gen {gen} -> running guard...")
            agent_script = expected_script
        else:
            agent_script = spawner.spawn(current_json)
            if not agent_script:
                print(f"\n[RUN] [DONE] Awaiting synthesis. Place agent file at:")
                print(f"      {expected_script}")
                return

        # ── SYNTHESIS GUARD ────────────────────────────────────────────
        guard_result = guard.watch(agent_script)
        _print_guard_result(guard_result)

        if guard_result["status"] == "QUARANTINED":
            print(f"\n[RUN] \033[91mQuarantined -- cannot evaluate broken code.\033[0m")
            _record_guard_failure(memory_path, child_id, gen, guard_result["issues"])
            report_path = agent_script.parent / f"EVAL_{agent_script.stem}.json"
            if not report_path.exists():
                _write_guard_failure_report(report_path, child_data, guard_result)
            current_json = mutator.mutate(current_json, report_path)
            continue
        # ── END GUARD ──────────────────────────────────────────────────

        report = evaluator.evaluate(agent_script, current_json)

        if report["overall_fitness"] >= 1.0 and not report["failures"]:
            print(f"[RUN] \033[92mULTIMATE fitness achieved in Gen {gen}!\033[0m")
            break

        report_path  = agent_script.parent / f"EVAL_{agent_script.stem}.json"
        current_json = mutator.mutate(current_json, report_path)

    print(f"\n{'='*60}")
    print(" EVOLUTION COMPLETE.")
    print(f"{'='*60}")


def _record_guard_failure(memory_path: Path, child_id: str, gen: int, issues: list):
    if not memory_path.exists():
        return
    with open(memory_path, encoding="utf-8") as f:
        memory = json.load(f)
    memory["lineage"].append({
        "child_id":       child_id,
        "generation":     gen,
        "failures":       [i["detail"] for i in issues],
        "improvements":   [],
        "fitness_delta":  -1.0,
        "overall_fitness": 0.0,
        "source":         "synthesis_guard"
    })
    with open(memory_path, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)


def _write_guard_failure_report(report_path: Path, child: dict, guard_result: dict):
    report = {
        "child_id":       child["child_id"],
        "generation":     child.get("generation", 0),
        "scores":         {"syntax_valid": 0.0},
        "failures":       [i["detail"] for i in guard_result["issues"]],
        "improvements":   [],
        "overall_fitness": 0.0,
        "source":         "synthesis_guard"
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    seed_json = SPAWNER_ROOT / "agents" / "child_seed.json"

    if not seed_json.exists():
        seed_data = {
            "child_id":   "OSINT_AUDITOR_X",
            "generation": 0,
            "traits": {
                "role":      "analyzer",
                "computing": "agnostic",
                "security":  "high",
                "interface": "cli"
            },
            "fitness": 0.5
        }
        seed_json.parent.mkdir(parents=True, exist_ok=True)
        with open(seed_json, "w", encoding="utf-8") as f:
            json.dump(seed_data, f, indent=2)
        print(f"[RUN] Created seed: {seed_json}")

    orchestrate(seed_json)
