#!/usr/bin/env python3
"""
NEXUS AGENT 03 — METAX ORCHESTRATOR (v3.0 Golden Chain Edition)
Mission: Strategic Selection -> Brain -> Eng -> Const -> Val -> Mark -> Deploy.
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path

# Paths
AGENT_DIR = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI-AGENT")
PROJECT_ROOT = Path(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT")
WIKI_PROJECT_DIR = PROJECT_ROOT / "WIKI-PROJECT"
BUILD_DIR = WIKI_PROJECT_DIR / "LEGAL" / "BUILD"

class NexusAutopilot:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries

    def run_cmd(self, cmd, capture=True):
        print(f"[*] Executing Component: {cmd}")
        res = subprocess.run(cmd, capture_output=capture, text=True, shell=True)
        return res

    def process_build(self, target_spec):
        """Full 6-Stage Autonomous Pipeline: Brain -> Eng -> Const -> Val -> Mark -> Deploy"""
        print(f"\n[BUILD START] TARGET: {target_spec}")

        # --- LAYER 0: STRATEGIC BRAIN (00) ---
        print(" [0/6] Brain Strategic Directive (Agent 00)...")
        self.run_cmd(f"python 00_WIKI_BRAIN.py --target {target_spec}")

        # --- LAYER 1: ENGINEERING SPEC (06) ---
        print(" [1/6] Engineering Specification (Agent 06 Synthesis)...")
        self.run_cmd(f"python 06_WIKI_ENGINEER.py --target {target_spec}")

        for attempt in range(1, self.max_retries + 1):
            print(f"  [ATTEMPT {attempt}/{self.max_retries}] ------------------------------")
            
            # --- LAYER 2: CONSTRUCTION (11) ---
            print("  [2/6] Code Construction (Agent 11 Build)...")
            build_res = self.run_cmd(f"python 11_WIKI_CONSTRUCTOR.py --specs {target_spec}")
            
            if "Delivered: " not in build_res.stdout:
                print("  [!] Build Error: No spec artifacts delivered. Retrying...")
                continue
                
            build_name = build_res.stdout.split("Delivered: ")[1].split("\n")[0].strip()
            build_path = BUILD_DIR / build_name

            # --- LAYER 3: TORTURE TESTING (16) ---
            print("  [3/6] Adversarial Validation (Agent 16 Torture)...")
            val_res = self.run_cmd(f"python 16_WIKI_VALIDATOR.py \"{build_path}\"")
            
            if val_res.returncode == 0:
                print(f"  [[WIN]] Success: Build {build_name} is STABLE!")
                
                # --- LAYER 4: BRANDING & PROFILE (13/17) ---
                print("  [4/6] Visual Branding (Agent 13 Landing/Logo)...")
                self.run_cmd(f"python 13_WIKI_MARKETER.py \"{build_path}\"")

                print("  [5/6] Professional Profiling (Agent 17 GitHub Config)...")
                self.run_cmd(f"python 17_WIKI_GITHUB_PROFILE.py \"{build_path}\"")

                # --- LAYER 5: DEPLOYMENT (15) ---
                print("  [6/6] Final Production Launch (Agent 15 Deploy)...")
                self.run_cmd(f"python 15_WIKI_DEPLOYER.py \"{build_path}\"")
                
                print(f"\n[DONE] {build_name} is LIVE and verified.")
                return True
            else:
                print(f"  [[FAIL]] Failure in validation attempt {attempt}.")
                time.sleep(1)
        return False

    def mass_produce(self, count=1, domain="OSINT"):
        print(f"\n{'='*60}\n  NEXUS MASS PRODUCTION: {count} UNITS (Domain: {domain})\n{'='*60}\n")

        for i in range(1, count + 1):
            print(f"\n[UNIT {i}/{count}] Selecting next target from Knowledge Base...")
            # Use Agent 04 (Archivist) to pick a target strategically
            picker_res = self.run_cmd(f"python 04_WIKI_ARCHIVIST.py --pick-next --domain {domain}")
            
            target = "NEXUS-Golden-OSINT"
            if "Target Selected: " in picker_res.stdout:
                target = picker_res.stdout.split("Target Selected: ")[1].split("\n")[0].strip()

            self.process_build(target)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--spec", type=str, default="OSINT")
    args = parser.parse_args()

    pilot = NexusAutopilot(max_retries=3)
    pilot.mass_produce(count=args.count, domain=args.spec)
