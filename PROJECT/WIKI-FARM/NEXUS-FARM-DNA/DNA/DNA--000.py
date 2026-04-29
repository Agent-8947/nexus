#!/usr/bin/env python3
"""
NEXUS DNA MASTER ORCHESTRATOR v2.0
====================================
FIX [L-04]: All components now accessible from menu:
  - DNA_18 (AST Renderer) -> menu [6]
  - DNA_20_SPAWNER -> menu [7]
  - DNA_14 (Reliable Tools) -> merged into [2] flow
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────
DNA_DIR      = Path(__file__).resolve().parent
PROJECT_ROOT = DNA_DIR.parent.parent.parent
SPAWNER_DIR  = DNA_DIR / "DNA_20_SPAWNER" / "engine"
# ────────────────────────────────────────────────────────────────────────

# Карта компонентов
COMPONENTS = {
    "01": "DNA_01_Global_Docs.md",
    "02": "DNA_02_Master_Harvester.py",
    "03": "DNA_03_Core_Builder.py",
    "04": "DNA_04_Synthesis_Core.json",
    "05": "DNA_05_Core_Manifest.md",
    "06": "DNA_06_Active_State.json",
    "07": "DNA_07_Evolution_Logic.py",
    "08": "DNA_08_Engine_Config.json",
    "09": "DNA_09_Mission_Control.py",
    "10": "DNA_10_Code_Assembler.py",
    "11": "DNA_11_Check_Validator.py",
    "12": "DNA_12_AST_RENDER",
    "13": "DNA_13_Obsidian_DNA.json",
    "14": "DNA_14_Reliable_Tools.py",
    "15": "DNA_15_Resynth_Engine.py",
    "16": "DNA_16_Vault_Bridge.py",
    "17": "DNA_17_Manifest_Generator.py",
    "18": "DNA_18_Legacy_Renderer.py",
    "19": "DNA_19_SYSTEM_CONTEXT.md",
    "20": "DNA_20_SPAWNER",
}


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    print(f"\033[96m" + "="*60)
    print("   _   _ _______  ___   _ ____    ____  _   _    _ ")
    print("  | \\ | | ____\\ \\/ / | | / ___|  |  _ \\| \\ | |  / \\ ")
    print("  |  \\| |  _|  \\  /| | | \\___ \\  | | | |  \\| | / _ \\ ")
    print("  | |\\  | |___ /  \\| |_| |___) | | |_| | |\\  |/ ___ \\ ")
    print("  |_| \\_|_____/_/\\_\\\\___/|____/  |____/|_| \\_/_/   \\_\\")
    print("\n              NEXUS DNA EVOLUTIONARY SYSTEM v2.0")
    print("="*60 + "\033[0m")


def check_integrity():
    print(f"\n[SYSTEM] Component integrity check...")
    missing = 0
    for idx, name in COMPONENTS.items():
        path   = DNA_DIR / name
        status = "[V]" if path.exists() else "[X]"
        if not path.exists():
            missing += 1
        print(f"  [{idx:>2}] {status} {name}")

    if missing == 0:
        print("\033[92m[INTEGRITY] All 20 components present.\033[0m")
    else:
        print(f"\033[91m[WARNING] {missing} component(s) missing!\033[0m")


def get_stats():
    core_path  = DNA_DIR / COMPONENTS["04"]
    render_dir = DNA_DIR / COMPONENTS["12"]
    pending_f  = DNA_DIR / "pending_synthesis.jsonl"
    evol_log   = DNA_DIR / "evolution_history.jsonl"

    nodes_count = 0
    gen1_count  = 0
    if core_path.exists():
        try:
            data = json.loads(core_path.read_text(encoding="utf-8"))
            nodes_count = len(data.get("NODES", []))
            gen1_count  = sum(1 for n in data.get("NODES", [])
                              if n["evolution_matrix"]["lineage"]["generation"] == 1)
        except Exception:
            pass

    renders_count  = len(list(render_dir.glob("*.py"))) if render_dir.exists() else 0
    pending_count  = sum(1 for _ in open(pending_f, encoding="utf-8")) if pending_f.exists() else 0
    accepted_count = sum(1 for _ in open(evol_log,  encoding="utf-8")) if evol_log.exists() else 0

    print(f"\n[STATS]")
    print(f"  DNA Pool:       {nodes_count} nodes (Gen-0: {nodes_count - gen1_count} | Gen-1: {gen1_count})")
    print(f"  AST Renders:    {renders_count} synthesized agents")
    print(f"  Evolution Log:  {accepted_count} accepted events")
    print(f"  Pending Synth:  {pending_count} waiting for agent")


def run_script(script_name: str, args: list = None, cwd: Path = None):
    script_path = DNA_DIR / script_name
    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)

    print(f"\n\033[93m[EXEC] Running {script_name}...\033[0m")
    try:
        subprocess.run(cmd, check=True, cwd=str(cwd or DNA_DIR))
    except subprocess.CalledProcessError as e:
        print(f"\033[91m[ERROR] Script exited with code {e.returncode}\033[0m")
    except FileNotFoundError:
        print(f"\033[91m[ERROR] Script not found: {script_path}\033[0m")
    input("\nPress Enter to continue...")


def run_spawner():
    """FIX [L-04]: Launch DNA_20_SPAWNER orchestrator from master menu."""
    run_py = SPAWNER_DIR / "run.py"
    if not run_py.exists():
        print(f"\033[91m[ERROR] SPAWNER run.py not found: {run_py}\033[0m")
        input("\nPress Enter to continue...")
        return

    print(f"\n\033[93m[EXEC] Launching DNA_20_SPAWNER/engine/run.py...\033[0m")
    try:
        subprocess.run(
            [sys.executable, str(run_py)],
            check=True,
            cwd=str(SPAWNER_DIR)
        )
    except subprocess.CalledProcessError as e:
        print(f"\033[91m[ERROR] SPAWNER exited with code {e.returncode}\033[0m")
    input("\nPress Enter to continue...")


def show_pending():
    """Display pending synthesis requests."""
    pending_f = DNA_DIR / "pending_synthesis.jsonl"
    if not pending_f.exists() or pending_f.stat().st_size == 0:
        print("\n[*] No pending synthesis requests.")
    else:
        print("\n[PENDING SYNTHESIS REQUESTS]")
        with open(pending_f, encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                try:
                    entry = json.loads(line)
                    print(f"  {i}. {entry['child_id']} | Mission: {entry['mission']} | {entry['ts'][:19]}")
                except Exception:
                    pass
    input("\nPress Enter to continue...")


def select_mission() -> str:
    missions = {
        "1": "osint",
        "2": "security",
        "3": "ai_monitor",
        "4": "iot_recon",
        "5": "infra",
    }
    print("\n[SELECT MISSION]")
    for k, v in missions.items():
        print(f"  [{k}] {v}")
    choice = input("Mission > ").strip()
    return missions.get(choice, "osint")


def main_menu():
    while True:
        clear()
        print_header()
        get_stats()

        print("\n\033[1mAVAILABLE OPERATIONS:\033[0m")
        print("  [1] RUN EVOLUTION      (DNA_09 -- Synthesize new agents)")
        print("  [2] UPDATE DNA CORE    (DNA_02 -- Re-scan repositories)")
        print("  [3] VALIDATE CODE      (DNA_11 -- Check AST_RENDER agents)")
        print("  [4] EXPORT TO OBSIDIAN (DNA_16 -- Vault Sync)")
        print("  [5] GENERATE MANIFEST  (DNA_17 -- Update DNA_05)")
        print("  [6] AST RENDER         (DNA_18 -- Render Gen-0 agents)")
        print("  [7] SPAWNER CYCLE      (DNA_20 -- Evolution via SPAWNER engine)")
        print("  [8] REBUILD DNA CORE   (DNA_03 -- Full rebuild from Vault)")
        print("  [9] PENDING SYNTHESIS  (View waiting requests)")
        print("  [0] EXIT")

        choice = input("\nSelect action > ").strip()

        if choice == "1":
            mission = select_mission()
            run_script(COMPONENTS["09"], ["--mission", mission])
        elif choice == "2":
            run_script(COMPONENTS["02"])
        elif choice == "3":
            run_script(COMPONENTS["11"], ["--all"])
        elif choice == "4":
            run_script(COMPONENTS["16"])
        elif choice == "5":
            run_script(COMPONENTS["17"])
        elif choice == "6":
            # FIX [L-04]: DNA_18 now accessible
            print("\n[AST RENDER] Options:")
            print("  [a] All Gen-0 nodes")
            print("  [b] Limited sample (first 10)")
            sub = input("Choice > ").strip()
            if sub == "b":
                run_script(COMPONENTS["18"], ["--gen", "0", "--max", "10"])
            else:
                run_script(COMPONENTS["18"], ["--gen", "0"])
        elif choice == "7":
            # FIX [L-04]: DNA_20_SPAWNER now accessible
            run_spawner()
        elif choice == "8":
            print("\n\033[93m[WARN] This will rebuild DNA_04 from scratch.\033[0m")
            confirm = input("Confirm? [y/N] > ").strip().lower()
            if confirm == "y":
                run_script(COMPONENTS["03"])
        elif choice == "9":
            show_pending()
        elif choice == "0":
            print("\nShutting down NEXUS DNA...")
            break
        else:
            print("Invalid choice.")
            time.sleep(0.8)


if __name__ == "__main__":
    main_menu()
