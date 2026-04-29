#!/usr/bin/env python3
"""
NEXUS_AD_VIDEO_SYNTHESIZER [NEXUS SYNTHESIZED Gen-8: OMNI-AD-GEN]
Mission: Total Automation. High-level orchestrator that consumes a brand source (URL/Image) and directly outputs finished cinematic MP4 ad campaigns.
Heritage: MASTER_DESIGNER (Gen-6) + KINETIC_RECORDER (Gen-7)

I/O Contract:
  Input:  Website URL (--url) OR Mockup path (--input)
  Output: Fully rendered Ad Videos in 16:9 and 9:16 (PROJECT/outputs/final_campaigns/)
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

class AdVideoSynthesizer:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parents[5]
        self.dna_dir = self.base_dir / "PROJECT" / "WIKI-FARM" / "NEXUS-FARM-DNA" / "DNA" / "DNA_12_AST_RENDER"
        self.output_dir = self.base_dir / "PROJECT" / "outputs" / "final_campaigns"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Internal script paths
        self.designer_script = self.dna_dir / "NEXUS_MASTER_DESIGN_ORCHESTRATOR.py"
        self.recorder_script = self.dna_dir / "WEB_MOTION_RECORDER_synthesized_agent.py"

    def execute(self, url=None, file_input=None, duration=20, style="classic", anchors=3):
        print(f"[NEXUS OMNI-AD-GEN] INITIATING FULL CYCLE SYNTHESIS...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # --- PHASE 1: Generate Design (HTML) ---
        print(f"\n--- PHASE 1: BRAND AUDIT & UI SYNTHESIS [STYLE: {style.upper()} | ANCHORS: {anchors}] ---")
        cmd_design = [sys.executable, str(self.designer_script)]
        if url: cmd_design.extend(["--url", url])
        else: cmd_design.extend(["--input", file_input])
        cmd_design.extend(["--style", style, "--anchors", str(anchors)])
        
        try:
            result = subprocess.run(cmd_design, capture_output=True, text=True, check=False, env=os.environ, encoding='utf-8', errors='ignore')
            
            if "[FATAL ERROR]" in result.stdout or result.returncode != 0:
                print(f"[ERROR] Phase 1 Component Failed:\n{result.stdout}\n{result.stderr}")
                return

            # Find the path in the output
            html_path = None
            for line in result.stdout.splitlines():
                if "rendered at:" in line:
                    html_path = line.split("->")[1].strip()
                    break
            
            if not html_path:
                print("[ERROR] Could not find synthesized HTML path in output.")
                return
            
            print(f"[SUCCESS] Design synthesized: {html_path}")
        except Exception as e:
            print(f"[ERROR] Phase 1 Execution Failed: {e}")
            return

        # --- PHASE 2: Record Motion (Video) ---
        print("\n--- PHASE 2: KINETIC MOTION CAPTURE ---")
        # Format path for browser
        browser_url = f"file:///{Path(html_path).absolute().as_posix()}"
        
        cmd_record = [
            sys.executable, str(self.recorder_script),
            "--url", browser_url,
            "--duration", str(duration),
            "--mode", "anchors",
            "--format", "both"
        ]
        
        try:
            subprocess.run(cmd_record, check=True, env=os.environ)
            print(f"[SUCCESS] Motion Capture complete.")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Phase 2 Failed.")
            return

        # --- FINAL: Reporting ---
        print("\n--- [CAMPAIGN SYNTHESIZED SUCCESSFULLY] ---")
        motion_dir = self.base_dir / "PROJECT" / "outputs" / "motion_recordings"
        latest_videos = sorted(motion_dir.glob("*.mp4"), key=os.path.getmtime)[-2:]
        
        print(f"Total Campaign Assets created at {timestamp}:")
        for v in latest_videos:
            print(f"-> {v.absolute()}")
        
        print("\n[FINISH] Your autonomous advertising campaign is ready.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NEXUS Omni-Ad-Gen: URL/Image to Finished Video Campaign")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-i", "--input", help="Path to brand mockup")
    group.add_argument("-u", "--url", help="URL of live brand website")
    parser.add_argument("--duration", type=int, default=20, help="Duration of the generated ad")
    parser.add_argument("--style", choices=["classic", "cyber", "brutalist", "luxury", "kinetic", "spatial", "playful", "random"], default="classic")
    parser.add_argument("--anchors", type=int, default=3, help="Number of sections")
    
    args = parser.parse_args()
    gen = AdVideoSynthesizer()
    gen.execute(url=args.url, file_input=args.input, duration=args.duration, style=args.style, anchors=args.anchors)
