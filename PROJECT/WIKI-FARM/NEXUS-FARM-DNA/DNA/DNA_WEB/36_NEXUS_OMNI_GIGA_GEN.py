#!/usr/bin/env python3
"""
NEXUS_OMNI_GIGA_GEN [NEXUS SYNTHESIZED Gen-9: THE UNIFIED ORCHESTRATOR]
Mission: Absolute Creative Control. Unifies Vision, Content, and Motion into one Giga-Agent.

Features:
1.  Screenshot Reference: Analyze visual styles from any image.
2.  Custom Text: Inject specific marketing copy.
3.  Custom Assets: Use specific brand images in the final render.
4.  Motion Capture: Output cinematic video in multiple formats.

Heritage: OMNI-AD-GEN (Gen-8) + VISUAL_AUDITOR (Gen-5)
"""

import sys
import os
import json
import urllib.request
import urllib.error
import argparse
import base64
import re
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Optional

class GigaOrchestrator:
    def __init__(self):
        self.gemini_key = os.environ.get("GEMINI_API_KEY")
        self.base_dir = Path(__file__).resolve().parents[5]
        self.dna_dir = self.base_dir / "PROJECT" / "WIKI-FARM" / "NEXUS-FARM-DNA" / "DNA" / "DNA_12_AST_RENDER"
        self.output_dir = self.base_dir / "PROJECT" / "outputs" / "omni_artifacts"
        self.video_dir = self.base_dir / "PROJECT" / "outputs" / "motion_recordings"
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.video_dir.mkdir(parents=True, exist_ok=True)
        
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={self.gemini_key}"
        self.recorder_script = self.dna_dir / "WEB_MOTION_RECORDER_synthesized_agent.py"

    def _call_gemini(self, payload: dict) -> str:
        req = urllib.request.Request(self.api_url, data=json.dumps(payload).encode('utf-8'), 
                                     headers={'Content-Type': 'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                data = json.loads(response.read().decode())
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except urllib.error.HTTPError as e:
            err_body = e.read().decode()
            raise RuntimeError(f"LLM API Error: HTTP {e.code}\\n{err_body}")

    def _get_b64_image(self, path: Path) -> dict:
        mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
        ext = path.suffix.lower()
        if ext not in mime_map: return None
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode('utf-8')
        return {"inlineData": {"mimeType": mime_map[ext], "data": data}}

    def analyze_and_synthesize(self, url: Optional[str], ref_img: Optional[str], 
                              custom_text: Optional[str], asset_paths: List[str],
                              style: str, anchors: int) -> Path:
        print(f"[NEXUS GIGA-GEN] INITIATING UNIFIED SYNTHESIS...")
        
        # --- PHASE 1: Build Multi-Modal Prompt ---
        parts = []
        
        system_prompt = f"""You are a Visionary Creative Director and Master UI Architect.
Task: Generate a single premium HTML/CSS/JS file for a high-converting Advertising Landing Page.

DIRECTIVES:
1. STYLE: {style.upper()}. 
2. STRUCTURE: {anchors} full-screen sections (anchors).
3. ANIMATION: GSAP & Lenis required. Every element must animate. Use ScrollTrigger timelines.
4. BRANDING: 
   - If a URL is provided, extract its core identity/colors.
   - If a Reference Screenshot is provided, use its VISUAL STYLE (spacing, typography vibe, color depth) as a primary reference.
   - MANDATORY TEXT: {custom_text if custom_text else 'Invent disruptive marketing copy based on the source.'}
   - MANDATORY ASSETS: Use provided images for main visual elements.

Tech Stack: Tailwind CSS, GSAP, Lenis Smooth Scroll.
Output: ONLY raw valid HTML wrapped in ```html ... ```."""

        parts.append({"text": system_prompt})
        
        if url:
            print(f"[*] Scraping Brand Metadata from {url}...")
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    html = resp.read().decode('utf-8', errors='ignore')[:50000]
                    parts.append({"text": f"WEBSITE DOM REFERENCE:\\n{html}"})
            except Exception as e:
                print(f"[!] Warning: URL scrape failed: {e}")

        if ref_img:
            print(f"[*] Analyzing Reference Style from {ref_img}...")
            img_part = self._get_b64_image(Path(ref_img))
            if img_part: parts.append(img_part)

        if asset_paths:
            print(f"[*] Integrating {len(asset_paths)} custom assets...")
            asset_info = "CUSTOM ASSETS TO USE:\\n"
            for i, p in enumerate(asset_paths):
                # We mention the paths so the LLM can reference them if they are local, 
                # but for preview we can also base64 them if needed. 
                # For now, we assume local paths relative to the generated HTML.
                asset_info += f"- Asset {i+1}: {Path(p).name}\\n"
                # Optionally b64 them for Gemini to see what they are
                img_data = self._get_b64_image(Path(p))
                if img_data: parts.append(img_data)
            parts.append({"text": asset_info})

        # --- PHASE 2: Generate HTML ---
        print("[*] Generating Code Architecture...")
        payload = {"contents": [{"parts": parts}], "generationConfig": {"temperature": 0.3}}
        raw_response = self._call_gemini(payload)
        
        match = re.search(r'```html\\s*(.*?)\\s*```', raw_response, re.DOTALL | re.IGNORECASE)
        html_code = match.group(1).strip() if match else raw_response
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_file = self.output_dir / f"giga_campaign_{timestamp}.html"
        out_file.write_text(html_code, encoding="utf-8")
        print(f"[SUCCESS] HTML synthesized: {out_file.name}")
        
        return out_file

    def record_motion(self, html_path: Path, duration: int):
        print(f"\n--- PHASE 3: KINETIC MOTION CAPTURE ---")
        browser_url = f"file:///{html_path.absolute().as_posix()}"
        
        cmd = [
            sys.executable, str(self.recorder_script),
            "--url", browser_url,
            "--duration", str(duration),
            "--mode", "anchors",
            "--format", "both"
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"[SUCCESS] Video rendered in {self.video_dir}")
        except Exception as e:
            print(f"[ERROR] Motion Capture failed: {e}")

    def run(self, url=None, screenshot=None, text=None, images=[], style="luxury", anchors=3, duration=20):
        html_path = self.analyze_and_synthesize(url, screenshot, text, images, style, anchors)
        self.record_motion(html_path, duration)
        print(f"\n[GIGA-GEN COMPLETE] Final Campaign Artifacts ready.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NEXUS GIGA-GEN: The Unified Video Ad Factory")
    parser.add_argument("-u", "--url", help="Target URL for brand extraction")
    parser.add_argument("-s", "--screenshot", help="Style reference screenshot")
    parser.add_argument("-t", "--text", help="Custom marketing copy")
    parser.add_argument("-i", "--images", nargs="+", default=[], help="Custom image assets to use")
    parser.add_argument("--style", default="luxury", choices=["luxury", "cyber", "brutalist", "kinetic", "playful"])
    parser.add_argument("--anchors", type=int, default=3)
    parser.add_argument("--duration", type=int, default=20)
    
    args = parser.parse_args()
    
    # Validation
    if not args.url and not args.screenshot:
        parser.error("At least --url or --screenshot is required for analysis.")
        
    giga = GigaOrchestrator()
    giga.run(url=args.url, screenshot=args.screenshot, text=args.text, 
             images=args.images, style=args.style, anchors=args.anchors, duration=args.duration)
