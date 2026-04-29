#!/usr/bin/env python3
"""
NEXUS DNA MISSION CONTROL v3.0 -- Главный Оркестратор Эволюции (ANTI-COLLAPSE)
==============================================================================
FIX [H-01]: Gen-1 fitness evaluated via real NexusEvaluator before registration
FIX [H-02]: WAITING_FOR_AGENT nodes go to pending_synthesis.jsonl, NOT DNA Core
FIX [M-02]: --seed argument for reproducibility
FIX [V3-09]: Adaptive novelty threshold based on population statistics
FIX [V3-10]: Dimension-mismatch safe crossover (handles 6-dim + 10-dim parents)
FIX [V3-11]: Increased synthesis batch (5), lower thresholds for 10-dim space
Flow: Selection -> Crossover -> Synthesis -> GUARD -> Evaluate -> Registration
"""


import json
import sys
import random
import itertools
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional

# ── Пути ────────────────────────────────────────────────────────────────
DNA_DIR        = Path(__file__).resolve().parent
SYNTHESIS_CORE = DNA_DIR / "DNA_04_Synthesis_Core.json"
RENDER_DIR     = DNA_DIR / "DNA_12_AST_RENDER"
EVOLUTION_LOG  = DNA_DIR / "evolution_history.jsonl"
PENDING_FILE   = DNA_DIR / "pending_synthesis.jsonl"   # FIX [H-02]
# ────────────────────────────────────────────────────────────────────────

sys.path.insert(0, str(DNA_DIR))
from DNA_07_Evolution_Logic import calculate_compatibility, calculate_novelty
from DNA_10_Code_Assembler  import synthesize

# ── Константы ────────────────────────────────────────────────────────────
# FIX [V3-11]: Lowered thresholds for 10-dim DNA space
NOVELTY_THRESHOLD   = 0.12   # Was 0.28 — 10-dim space has lower baseline distances
FITNESS_MIN         = 0.45   # Was 0.5 — allow slightly weaker parents to participate
COMPATIBILITY_MIN   = 0.15   # Was 0.35 — 10-dim cosine distances are smaller
MAX_CANDIDATES      = 100    # Was 20 — wider search for hybrids

MAX_SYNTHESIS_PER_RUN = 5    # Was 3

MISSIONS = {
    "osint":      "Build an OSINT intelligence gathering and analysis pipeline",
    "security":   "Build a security audit and vulnerability detection tool",
    "ai_monitor": "Build an AI model monitoring and anomaly detection system",
    "iot_recon":  "Build an IoT device reconnaissance and firmware analysis tool",
    "infra":      "Build an infrastructure monitoring and distributed orchestration agent",
}
# ────────────────────────────────────────────────────────────────────────


class EvolveMission:
    def __init__(self, mission_key: str = "osint", verbose: bool = True, seed: Optional[int] = None):
        self.mission     = MISSIONS.get(mission_key, MISSIONS["osint"])
        self.mission_key = mission_key
        self.verbose     = verbose

        # FIX [M-02]: reproducible randomness
        if seed is not None:
            random.seed(seed)
            self._log(f"[NEXUS] Random seed: {seed}")

        self.dna   = self._load_dna()
        self.nodes = self.dna.get("NODES", [])
        self._log(f"\n{'='*60}")
        self._log(f"[NEXUS] EVOLVE MISSION: {mission_key.upper()}")
        self._log(f"[NEXUS] DNA Pool: {len(self.nodes)} nodes")
        self._log(f"{'='*60}")

    def _log(self, msg: str):
        if self.verbose:
            print(msg)

    def _load_dna(self) -> dict:
        if not SYNTHESIS_CORE.exists():
            print(f"[!] SYNTHESIS_CORE not found: {SYNTHESIS_CORE}")
            sys.exit(1)
        return json.loads(SYNTHESIS_CORE.read_text(encoding="utf-8"))

    def _save_dna(self):
        SYNTHESIS_CORE.write_text(
            json.dumps(self.dna, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    # ── Phase 1: SELECTION (Tournament & Speciation) ────────────────────
    def select_candidates(self) -> list[tuple[dict, dict, float]]:
        self._log("\n[PHASE 1] SELECTION -- Tournament & Speciation")

        if len(self.nodes) < 2:
            return []

        def tournament_select(pool: list, k: int = 5) -> dict:
            """Select best of k random nodes based on overall fitness."""
            competitors = random.sample(pool, min(k, len(pool)))
            return max(competitors, key=lambda n: n["evolution_matrix"]["fitness_score"]["overall"])

        scored_pairs = []
        attempts = 0
        
        while len(scored_pairs) < MAX_SYNTHESIS_PER_RUN and attempts < 1000:
            attempts += 1
            parent_a = tournament_select(self.nodes)
            
            # Speciation: 80% chance to select parent_b from the same primary domain
            domain_a = parent_a["evolution_matrix"]["traits_fixed"].get("domain", "misc")
            if random.random() < 0.80:
                # Intra-species mating
                species_pool = [n for n in self.nodes if n["evolution_matrix"]["traits_fixed"].get("domain") == domain_a and n["node_id"] != parent_a["node_id"]]
                if not species_pool: continue
                parent_b = tournament_select(species_pool)
            else:
                # Inter-species mating (creates diversity)
                other_pool = [n for n in self.nodes if n["node_id"] != parent_a["node_id"]]
                if not other_pool: continue
                parent_b = tournament_select(other_pool)

            score = calculate_compatibility(parent_a, parent_b)
            if score >= COMPATIBILITY_MIN:
                # Ensure uniqueness
                if not any({a["node_id"], b["node_id"]} == {parent_a["node_id"], parent_b["node_id"]} for a, b, _ in scored_pairs):
                    scored_pairs.append((parent_a, parent_b, score))

        scored_pairs.sort(key=lambda x: x[2], reverse=True)
        self._log(f"  Selected pairs via Tournament: {len(scored_pairs)}")
        
        for a, b, _ in scored_pairs[:5]:
            gen_a = a["evolution_matrix"]["lineage"].get("generation", 0)
            gen_b = b["evolution_matrix"]["lineage"].get("generation", 0)
            self._log(f"  [*] MATCH (Gen-{max(gen_a, gen_b)+1}): {a['node_id']} x {b['node_id']}")

        return scored_pairs

    # ── Phase 2: CROSSOVER ───────────────────────────────────────────────
    def crossover(self, parent_a: dict, parent_b: dict, compat_score: float) -> dict:
        dna_a  = list(parent_a["evolution_matrix"]["dna_signature"])
        dna_b  = list(parent_b["evolution_matrix"]["dna_signature"])
        fit_a  = parent_a["evolution_matrix"]["fitness_score"]["overall"]
        fit_b  = parent_b["evolution_matrix"]["fitness_score"]["overall"]

        # FIX [V3-10]: Pad shorter vector
        max_len = max(len(dna_a), len(dna_b))
        while len(dna_a) < max_len: dna_a.append(random.uniform(0.1, 0.5))
        while len(dna_b) < max_len: dna_b.append(random.uniform(0.1, 0.5))

        # Horizontal Gene Transfer (if PatternBank available)
        top_hgt_vector = []
        try:
            from DNA_26_Pattern_Bank import PatternBank
            bank = PatternBank()
            top = bank.get_top_patterns(limit=1)
            bank.close()
            if top and top[0]["fitness"] > 0.8:
                import hashlib
                h = int(hashlib.md5(top[0]["name"].encode()).hexdigest(), 16)
                random.seed(h)
                top_hgt_vector = [random.uniform(0.5, 1.0) for _ in range(max_len)]
                random.seed()  # reset
        except Exception:
            pass

        child_dna = []
        # Two-Point Crossover
        cpt1 = random.randint(1, max_len // 2)
        cpt2 = random.randint(cpt1, max_len - 1)

        for i in range(max_len):
            # Crossover
            if i < cpt1:
                val = dna_a[i]
            elif i < cpt2:
                val = dna_b[i]
            else:
                val = dna_a[i] if fit_a > fit_b else dna_b[i]

            # Horizontal Gene Transfer (10% chance if HGT vector available)
            if top_hgt_vector and random.random() < 0.10:
                val = (val + top_hgt_vector[i]) / 2.0

            # Point Mutation (15% chance to flip/mutate drastically)
            if random.random() < 0.15:
                val += random.uniform(-0.3, 0.3)
            
            child_dna.append(round(min(1.0, max(0.0, val)), 3))

        dominant     = parent_a if fit_a >= fit_b else parent_b
        recessive    = parent_b if fit_a >= fit_b else parent_a
        child_traits = dict(dominant["evolution_matrix"]["traits_fixed"])

        # Role Mutation
        if random.random() < 0.30:
            child_traits["role"] = recessive["evolution_matrix"]["traits_fixed"].get("role", child_traits["role"])
        
        # Domain Speciation / Crossover 
        if random.random() < 0.20:
            dom_a = parent_a["evolution_matrix"]["traits_fixed"].get("domain", "misc")
            dom_b = parent_b["evolution_matrix"]["traits_fixed"].get("domain", "misc")
            if dom_a != dom_b:
                child_traits["domain"] = random.choice([dom_a, dom_b])

        return {
            "node_id": f"HYBRID_{parent_a['node_id']}_x_{parent_b['node_id']}",
            "evolution_matrix": {
                "traits_fixed": child_traits,
                "dna_signature": child_dna,
                "resources": {"compute_cost": "high", "memory_cost": "medium"},
                "mutation_hotspots": {
                    "can_add_capabilities": True,
                    "can_change_interface": True,
                    "mutation_rate": round(compat_score, 2)
                },
                "fitness_score": {
                    "performance": 0.0, "security": 0.0,
                    "novelty": 0.0, "completeness": 0.0, "overall": 0.0
                },
                "lineage": {
                    "parents": [parent_a["node_id"], parent_b["node_id"]],
                    "generation": max(parent_a["evolution_matrix"]["lineage"].get("generation", 0), 
                                      parent_b["evolution_matrix"]["lineage"].get("generation", 0)) + 1,
                    "compat_score": compat_score,
                    "synthesized_at": datetime.now().isoformat(),
                    "hgt_applied": bool(top_hgt_vector)
                }
            }
        }



    # ── Phase 3: SYNTHESIS ───────────────────────────────────────────────
    def run_synthesis(self, parent_a: dict, parent_b: dict) -> dict:
        self._log(f"\n[PHASE 3] SYNTHESIS -- {parent_a['node_id']} x {parent_b['node_id']}")
        return synthesize(parent_a, parent_b, mission=self.mission)

    # ── Phase 4: VALIDATION + REGISTRATION ──────────────────────────────
    def validate_and_register(self, child_node: dict, synth_result: dict, force: bool = False) -> bool:
        self._log(f"\n[PHASE 4] VALIDATION -- {child_node['node_id']}")

        if not synth_result.get("success"):
            self._log(f"  [X] Synthesis failed: {synth_result.get('error', 'Unknown')}")
            return False

        # FIX [S-05]: Handle new CODE_GENERATED status from assembler v4.0
        if synth_result.get("status") == "WAITING_FOR_AGENT":
            self._log(f"  [WAIT] Pending synthesis. Saving to pending_synthesis.jsonl...")
            pending_entry = {
                "ts":        datetime.now().isoformat(),
                "mission":   self.mission_key,
                "child_id":  child_node["node_id"],
                "parents":   child_node["evolution_matrix"]["lineage"]["parents"],
                "req_file":  synth_result.get("req_file"),
                "status":    "WAITING"
            }
            with open(PENDING_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(pending_entry, ensure_ascii=False) + "\n")
            return False
        
        # CODE_GENERATED or SCAFFOLD_ONLY — proceed to validation

        # FIX [V3-09]: Adaptive novelty threshold
        child_dna = child_node["evolution_matrix"]["dna_signature"]
        novelty = calculate_novelty(child_dna, self.nodes)

        # Compute adaptive threshold: median novelty of existing Gen-0 * 0.5
        if len(self.nodes) > 20:
            existing_novelties = [
                n["evolution_matrix"]["fitness_score"].get("novelty", 0)
                for n in self.nodes
                if n["evolution_matrix"]["lineage"]["generation"] == 0
            ]
            if existing_novelties:
                import statistics
                adaptive_threshold = max(0.05, statistics.median(existing_novelties) * 0.3)
            else:
                adaptive_threshold = NOVELTY_THRESHOLD
        else:
            adaptive_threshold = NOVELTY_THRESHOLD

        if force:
            self._log(f"  Novelty Score: {novelty:.3f} (FORCED ACCEPTANCE)")
        else:
            self._log(f"  Novelty Score: {novelty:.3f} (adaptive min: {adaptive_threshold:.3f})")
            if novelty < adaptive_threshold:
                self._log(f"  [X] Rejected: low novelty (clone of existing node)")
                return False


        # FIX [H-01]: Evaluate actual code quality before registering
        code_file = synth_result.get("file_path")
        real_fitness = self._evaluate_code(code_file, child_node) if code_file else None

        if real_fitness is not None:
            # Use real evaluator score
            child_node["evolution_matrix"]["fitness_score"]["novelty"]      = novelty
            child_node["evolution_matrix"]["fitness_score"]["completeness"]  = real_fitness.get("completeness", 0.0)
            child_node["evolution_matrix"]["fitness_score"]["performance"]   = real_fitness.get("performance", 0.7)
            child_node["evolution_matrix"]["fitness_score"]["security"]      = real_fitness.get("security", 0.5)
            child_node["evolution_matrix"]["fitness_score"]["overall"]       = real_fitness.get("overall", 0.0)
        else:
            # Fallback: novelty-only estimate (clearly marked as unvalidated)
            child_node["evolution_matrix"]["fitness_score"]["novelty"]  = novelty
            child_node["evolution_matrix"]["fitness_score"]["overall"]  = round(novelty * 0.5, 3)
            child_node["evolution_matrix"]["fitness_score"]["_unvalidated"] = True
            self._log(f"  [!] No code file found -- fitness is novelty-estimate only.")

        # Register in DNA Core
        self.nodes.append(child_node)
        self.dna["NODES"]       = self.nodes
        self.dna["TOTAL_NODES"] = len(self.nodes)
        self._save_dna()
        gen = child_node["evolution_matrix"]["lineage"].get("generation", 1)
        self._log(f"  [V] Registered in DNA Core (Gen-{gen})")
        self._log(f"  Overall fitness: {child_node['evolution_matrix']['fitness_score']['overall']}")

        self._log_evolution(child_node, synth_result, novelty)
        return True

    def _evaluate_code(self, code_path: str, child_node: dict) -> dict | None:
        """FIX [H-01]: Real code quality evaluation before registration."""
        try:
            sys.path.insert(0, str(DNA_DIR))
            from DNA_11_Check_Validator import validate_file
            result = validate_file(Path(code_path), is_critical=False)
            quality = result.quality_score
            return {
                "completeness": 1.0 if result.passed else 0.5,
                "performance":  0.8,
                "security":     0.9 if result.passed else 0.4,
                "overall":      round(0.5 + quality * 0.5, 3)
            }
        except Exception as e:
            self._log(f"  [!] Evaluator error: {e}")
            return None

    def _log_evolution(self, child: dict, synth: dict, novelty: float):
        entry = {
            "ts":        datetime.now().isoformat(),
            "mission":   self.mission_key,
            "child_id":  child["node_id"],
            "parents":   child["evolution_matrix"]["lineage"]["parents"],
            "novelty":   novelty,
            "code_file": synth.get("file_path"),
            "fitness":   child["evolution_matrix"]["fitness_score"]["overall"],
            "accepted":  True
        }
        with open(EVOLUTION_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # ── Main Run ─────────────────────────────────────────────────────────
    def run(self):
        accepted = 0
        rejected = 0

        candidates = self.select_candidates()
        if not candidates:
            self._log("[!] No candidates for synthesis.")
            return

        self._log(f"\n[NEXUS] {len(candidates)} pairs selected for synthesis:")
        for i, (a, b, score) in enumerate(candidates):
            self._log(f"  {i+1}. {a['node_id']} x {b['node_id']} [compat={score:.3f}]")

        for parent_a, parent_b, compat in candidates:
            child_node   = self.crossover(parent_a, parent_b, compat)
            synth_result = self.run_synthesis(parent_a, parent_b)

            registered = self.validate_and_register(child_node, synth_result)
            if registered:
                accepted += 1
            else:
                rejected += 1

        self._log(f"\n{'='*60}")
        self._log(f"[NEXUS] EVOLUTION COMPLETE")
        self._log(f"  Synthesized: {accepted + rejected}")
        self._log(f"  Accepted:    {accepted}")
        self._log(f"  Rejected:    {rejected}")
        self._log(f"  DNA Core:    {len(self.nodes)} nodes")
        self._log(f"{'='*60}\n")


    # ── Phase 5: PENDING COMPLETION ─────────────────────────────────────
    def process_pending(self):
        self._log("\n[PHASE 5] PROCESSING PENDING SYNTHESIS...")
        if not PENDING_FILE.exists():
            self._log("  [*] No pending file found.")
            return

        with open(PENDING_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        remaining = []
        processed = 0
        
        for line in lines:
            entry = json.loads(line)
            child_id = entry["child_id"]
            
            # Check if file exists in AST_RENDER
            code_file = RENDER_DIR / f"{child_id}_synthesized_agent.py"
            
            if code_file.exists():
                self._log(f"  [+] Found synthesized code for {child_id}")
                
                # Reconstruct child node
                # Expected format: HYBRID_ParentA_x_ParentB
                clean_id = child_id.replace("HYBRID_", "")
                parent_parts = clean_id.split("_x_")
                parent_a_id = parent_parts[0] if len(parent_parts) > 0 else "UNKNOWN"
                parent_b_id = parent_parts[1] if len(parent_parts) > 1 else "UNKNOWN"
                
                # Use traits from first parent found in DNA Core as template
                def find_parent(id):
                    for n in self.nodes:
                        if n["node_id"] == id: return n
                    return None

                p_a = find_parent(parent_a_id)
                p_b = find_parent(parent_b_id)
                
                # Reconstruct signature
                if p_a and p_b:
                    sig_a = p_a["evolution_matrix"]["dna_signature"]
                    sig_b = p_b["evolution_matrix"]["dna_signature"]
                    child_sig = [(a + b) / 2 for a, b in zip(sig_a, sig_b)]
                    traits = p_a["evolution_matrix"]["traits_fixed"]
                else:
                    child_sig = [0.5]*6
                    traits = {"domain": "infra", "role": "library", "interface": "cli"}

                child_node = {
                    "node_id": child_id,
                    "evolution_matrix": {
                        "traits_fixed": traits,
                        "dna_signature": child_sig,
                        "resources": {"compute_cost": "high", "memory_cost": "medium"},
                        "mutation_hotspots": {"mutation_rate": 0.5},
                        "fitness_score": {"performance": 0.0, "security": 0.0, "novelty": 0.0, "completeness": 0.0, "overall": 0.0},
                        "lineage": {"parents": [parent_a_id, parent_b_id], "generation": 1, "synthesized_at": entry["ts"]}
                    }
                }
                
                # Validate and register
                synth_mock = {"success": True, "file_path": str(code_file)}
                if self.validate_and_register(child_node, synth_mock, force=True):
                    processed += 1
                else:
                    remaining.append(line) # Novelty fail or other
            else:
                remaining.append(line)

        # Update pending file
        with open(PENDING_FILE, "w", encoding="utf-8") as f:
            f.writelines(remaining)
        
        self._log(f"\n[PENDING COMPLETED] Processed: {processed} | Remaining: {len(remaining)}")

# ── Entry Point ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="NEXUS Evolution Engine -- evolutionary agent synthesis"
    )
    parser.add_argument(
        "--mission", choices=list(MISSIONS.keys()), default="osint",
        help="Mission type for synthesis context"
    )
    parser.add_argument("--quiet",  action="store_true", help="Suppress output")
    parser.add_argument("--seed",   type=int, default=None,
                        help="Random seed for reproducibility")
    parser.add_argument("--process-pending", action="store_true", help="Process completed synthesis requests")
    args = parser.parse_args()

    engine = EvolveMission(
        mission_key=args.mission,
        verbose=not args.quiet,
        seed=args.seed
    )
    
    if args.process_pending:
        engine.process_pending()
    else:
        engine.run()
