#!/usr/bin/env python3
import json
import sys
from pathlib import Path

class NexusMutator:
    """Evolutionary mutation engine."""

    def __init__(self, memory_path: Path):
        self.memory_path = memory_path

    def mutate(self, child_json_path: Path, report_path: Path):
        with open(child_json_path, 'r', encoding='utf-8') as f:
            child = json.load(f)
        with open(report_path, 'r', encoding='utf-8') as f:
            report = json.load(f)

        # 1. Update Lineage Memory
        with open(self.memory_path, 'r', encoding='utf-8') as f:
            memory = json.load(f)
        
        fitness_delta = report["overall_fitness"] - child.get("fitness", 0.5)
        
        lineage_entry = {
            "child_id": child["child_id"],
            "generation": child.get("generation", 0),
            "failures": report["failures"],
            "improvements": report["improvements"],
            "fitness_delta": round(fitness_delta, 3),
            "overall_fitness": report["overall_fitness"]
        }
        
        memory["lineage"].append(lineage_entry)
        with open(self.memory_path, 'w', encoding='utf-8') as f:
            json.dump(memory, f, indent=2)

        # 2. Mutate Child for Next Gen
        new_child = child.copy()
        new_child["generation"] += 1
        new_child["fitness"] = report["overall_fitness"]
        
        # Penalize traits that failed
        # (This is where more complex mutation logic would go)
        
        new_child_path = child_json_path.parent / f"GEN_{new_child['generation']}_{child['child_id']}.json"
        with open(new_child_path, 'w', encoding='utf-8') as f:
            json.dump(new_child, f, indent=2)

        print(f"[MUTATOR] Mutation complete. Next gen child: {new_child_path}")
        return new_child_path

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: mutator.py <child_json_path> <report_path>")
        sys.exit(1)
    # Correct memory path relative to engine in DNA_20_SPAWNER
    engine_dir = Path(__file__).resolve().parent
    mem = engine_dir.parent / "memory" / "lineage.json"
    mutator = NexusMutator(mem)
    mutator.mutate(Path(sys.argv[1]), Path(sys.argv[2]))
