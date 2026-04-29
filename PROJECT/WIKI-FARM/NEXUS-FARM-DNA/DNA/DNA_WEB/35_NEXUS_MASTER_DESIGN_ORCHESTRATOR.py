#!/usr/bin/env python3
"""
MASTER_DESIGN_ORCHESTRATOR [NEXUS SYNTHESIZED Gen-6: OMNI-ARCHITECT]
Mission: Unified pipeline. Autonomously analyzes external inputs (URLs/Mockups) and directly compiles them into natively styled, high-converting premium HTML.
Heritage: VISUAL_AUDITOR (Gen-5) + TRUE-AI_GENERATOR (Gen-4)

I/O Contract:
  Input:  Website URL (--url) OR Mockup path (--input)
  Output: Fully rendered HTML Ad Campaign file (One-Click Execute)
"""

import sys
import os
import json
import urllib.request
import urllib.error
import argparse
import base64
import re
from pathlib import Path
from datetime import datetime

class OmniArchitect:
    def __init__(self):
        self.gemini_key = os.environ.get("GEMINI_API_KEY")
        self.output_dir = Path(__file__).resolve().parents[5] / "PROJECT" / "outputs" / "omni_artifacts"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        # Using gemini-1.5-pro for both vision and heavy coding tasks
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={self.gemini_key}"

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

    # ================= PHASE 1: ANALYSIS (AUDITOR) =================
    
    def analyze_source(self, url: str = None, file_input: str = None) -> str:
        if not self.gemini_key:
            raise EnvironmentError("GEMINI_API_KEY is not set. The Omni-Architect requires LLM access.")

        system_prompt = """You are a Native Brand Advertising Director and UI/UX Mastermind.
Your task is to completely redesign the provided source into a high-converting Advertising/Marketing Landing Page, WHILE STRICTLY PRESERVING THE ORIGINAL BRAND STYLE.
You must define:
1. A bold, highly creative Hero Section concept with disruptive marketing copy (native to their identity).
2. The EXACT color palette extracted from the source (Do NOT invent new colors, extract Hex/CSS vars if possible).
3. The exact typography implied by the source.
4. Aggressive, modern interactions and GSAP motion concepts that enhance the existing style.

DO NOT output boilerplate text, just the final Genesis Prompt ready for HTML generation."""

        payload = {
            "contents": [{"parts": [{"text": system_prompt}]}],
            "generationConfig": {"temperature": 0.2}
        }

        if url:
            print(f"[*] PHASE 1: Scraping DOM from {url}...")
            req_html = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            try:
                with urllib.request.urlopen(req_html, timeout=15) as response:
                    html_data = response.read().decode('utf-8', errors='ignore')[:75000]
                payload["contents"][0]["parts"].append({"text": f"WEBSITE SOURCE CODE:\\n\\n{html_data}"})
            except Exception as e:
                raise RuntimeError(f"Failed to fetch URL {url}: {e}")
                
        elif file_input:
            print(f"[*] PHASE 1: Analyzing Visual Mockup from {file_input}...")
            target = Path(file_input)
            ext = target.suffix.lower()
            mime_map = {".pdf": "application/pdf", ".png": "image/png", ".jpg": "image/jpeg"}
            if ext not in mime_map: raise ValueError("Unsupported file format for visual analysis.")
            
            with open(target, "rb") as f:
                b64_data = base64.b64encode(f.read()).decode('utf-8')
            payload["contents"][0]["parts"].append({"inlineData": {"mimeType": mime_map[ext], "data": b64_data}})

        print("[*] Inferring Native Brand Identity & Marketing Structure...")
        return self._call_gemini(payload)

    # ================= PHASE 2: GENERATION =================

    def generate_html(self, genesis_prompt: str, style: str = "classic", anchors: int = 3) -> Path:
        print(f"\n[*] PHASE 2: Initiating Raw Code Assembly [Style: {style.upper()} | Anchors: {anchors}]...")
        
        style_directives = {
            "classic": "Clean, high-converting professional marketing landing page. Modern sans-serif, white/blue palette.",
            "cyber": "Dark mode, aggressive neon accents, heavy glassmorphism, glowing borders, mono fonts, tech-interface feel.",
            "brutalist": "Industrial, raw grids, massive bold typography, high-contrast black/white with one punchy accent, no rounded corners.",
            "luxury": "Apple-style minimalist editorial, huge white space, thin serif typography, subtle airy animations, extremely premium feel.",
            "kinetic": "One-page narrative, motion-centric elements, large kinetic typography that follows scroll, mouse-tracking effects.",
            "spatial": "3D-like layering, frosted glass cards (blur 40px), deep radial gradients, floating elements, spatial depth.",
            "playful": "Organic fluid shapes, soft pastel colors, bouncy elastic GSAP animations, friendly rounded corners (100px)."
        }
        
        selected_style = style_directives.get(style, style_directives["classic"])

    def generate_html(self, genesis_prompt: str, style: str = "classic", anchors: int = 3) -> Path:
        print(f"\n[*] PHASE 2: Initiating Raw Code Assembly [Style: {style.upper()} | Anchors: {anchors}]...")
        
        style_directives = {
            "classic": "Clean, high-converting professional marketing landing page. Modern sans-serif, white/blue palette.",
            "cyber": "Dark mode, aggressive neon accents, heavy glassmorphism, glowing borders, mono fonts, tech-interface feel.",
            "brutalist": "Industrial, raw grids, massive bold typography, high-contrast black/white with one punchy accent, no rounded corners.",
            "luxury": "Apple-style minimalist editorial, huge white space, thin serif typography, subtle airy animations, extremely premium feel.",
            "kinetic": "One-page narrative, motion-centric elements, large kinetic typography that follows scroll, mouse-tracking effects.",
            "spatial": "3D-like layering, frosted glass cards (blur 40px), deep radial gradients, floating elements, spatial depth.",
            "playful": "Organic fluid shapes, soft pastel colors, bouncy elastic GSAP animations, friendly rounded corners (100px)."
        }
        
        selected_style = style_directives.get(style, style_directives["classic"])

        system_prompt = f"""You are a world-class Motion UI Architect. 
Generate a single HTML file containing a premium, high-fidelity animated UI.

EXTREME ANIMATION DIRECTIVE:
1. NO STATIC ELEMENTS: Every single component (text, button, card, border) MUST have an entrance animation.
2. MICRO-STAGGERING: Use GSAP `stagger` for every list, grid of cards, or group of icons. Appearance must feel sequential and fluid.
3. ENTRANCE SEQUENCES: Use GSAP `ScrollTrigger` and `Timelines` to chain animations for each block. When a section enters the viewport, it must "unfold" (e.g., Background shifts first -> Title slides in -> Text fades in -> Action buttons bounce).
4. AMBIENT MOTION: Implement subtle continuous animations (floating particles, breathing gradients, or rotating glyphs) to ensure the page feels "alive" at all times.
5. EXOTIC EASING: Prioritize `expo.out`, `back.out(1.7)`, and `elastic.out(1, 0.5)` for punchy, professional movement.

VISUAL STYLE DIRECTIVE: {selected_style}

Tech Stack strictly required:
1. Tailwind CSS (via CDN)
2. GSAP & Lenis for animations (via CDN)
3. Internal <style> for custom aesthetics.

CRITICAL ARCHITECTURE RULE:
Structure as exactly {anchors} full-screen sections (`min-h-screen`). 
Each MUST have a distinct ID: `<section id="anchor-1">`, ..., `<section id="anchor-{anchors}">`. 
Vertical {anchors}-slide cinematic presentation only.

Output ONLY raw valid HTML code wrapped in ```html ... ```. No explanations."""

        payload = {
            "contents": [{"parts": [{"text": f"{system_prompt}\\n\\nGENESIS PROMPT: {genesis_prompt}"}]}],
            "generationConfig": {"temperature": 0.4}
        }

        print("[*] Synthesizing HTML DOM, GSAP Logic, and Tailwind Utility Classes...")
        raw_response = self._call_gemini(payload)
        
        # Extract HTML
        match = re.search(r'```html\\s*(.*?)\\s*```', raw_response, re.DOTALL | re.IGNORECASE)
        html_code = match.group(1).strip() if match else raw_response
        if html_code.startswith("<!DOCTYPE html>") is False and raw_response.find("<!DOCTYPE html>") != -1:
            html_code = raw_response[raw_response.find("<!DOCTYPE html>"):]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_file = self.output_dir / f"omni_campaign_{timestamp}.html"
        out_file.write_text(html_code, encoding="utf-8")
        return out_file

    def execute_pipeline(self, url: str = None, file_input: str = None, style: str = "classic", anchors: int = 3):
        print("====== OMNI-ARCHITECT PIPELINE INITIATED =====\n")
        try:
            genesis_prompt = self.analyze_source(url, file_input)
            print("\n--- GENERATED GENESIS PROMPT ---")
            print(genesis_prompt)
            print("--------------------------------\n")
            
            final_artifact = self.generate_html(genesis_prompt, style=style, anchors=anchors)
            print(f"\n[SUCCESS] Pipeline Complete! Executive Design rendered at:")
            print(f"-> {final_artifact.absolute()}")
        except Exception as e:
            print(f"\n[FATAL ERROR] Omni-Pipeline failed: {e}")
            sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NEXUS Omni-Architect: Direct Input-to-HTML Pipeline")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-i", "--input", help="Path to JPG/PNG/PDF mockup")
    group.add_argument("-u", "--url", help="URL of a live website to reverse-engineer")
    parser.add_argument("--style", choices=["classic", "cyber", "brutalist", "luxury", "kinetic", "spatial", "playful", "random"], default="classic")
    parser.add_argument("--anchors", type=int, default=3, help="Number of full-screen sections to generate")
    
    args = parser.parse_args()
    
    import random
    selected_style = args.style
    if selected_style == "random":
        selected_style = random.choice(["classic", "cyber", "brutalist", "luxury", "kinetic", "spatial", "playful"])
        
    architect = OmniArchitect()
    architect.execute_pipeline(url=args.url, file_input=args.input, style=selected_style, anchors=args.anchors)
