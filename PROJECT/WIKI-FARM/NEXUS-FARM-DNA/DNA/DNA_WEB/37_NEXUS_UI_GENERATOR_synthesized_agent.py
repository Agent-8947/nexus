#!/usr/bin/env python3
"""
NEXUS_UI_GENERATOR [NEXUS SYNTHESIZED Gen-4: TRUE-AI ARCHITECT]
Mission: Dynamically generate unique animated CSS/GSAP interfaces using LLM Inference.
Heritage: NEXUS_MOTION_ENGINE + LLM Reasoning

I/O Contract:
  Input:  Prompt context (from CLI --prompt)
  Output: 100% uniquely generated HTML artifact
"""

import sys
import os
import json
import urllib.request
import urllib.error
import argparse
import re
from pathlib import Path
from datetime import datetime

class TrueAIGenerator:
    def __init__(self):
        self.output_dir = Path(__file__).resolve().parents[5] / "PROJECT" / "outputs" / "ai_generated_designs"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.gemini_key = os.environ.get("GEMINI_API_KEY")
        
    def _call_gemini(self, system_prompt: str, user_prompt: str) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.gemini_key}"
        payload = {
            "contents": [{"parts": [{"text": f"{system_prompt}\\n\\nUSER TASK: {user_prompt}"}]}],
            "generationConfig": {"temperature": 0.4}
        }
        
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), 
                                     headers={'Content-Type': 'application/json'}, method='POST')
        with urllib.request.urlopen(req, timeout=60) as response:
            data = json.loads(response.read().decode())
            return data["candidates"][0]["content"]["parts"][0]["text"]

    def _call_ollama(self, system_prompt: str, user_prompt: str) -> str:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "qwen2.5-coder:3b", # Target model from DNA core
            "system": system_prompt,
            "prompt": user_prompt,
            "stream": False,
            "options": {"temperature": 0.4, "num_ctx": 8192}
        }
        
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'),
                                     headers={'Content-Type': 'application/json'}, method='POST')
        with urllib.request.urlopen(req, timeout=120) as response:
            return json.loads(response.read().decode())["response"]

    def extract_html(self, raw_text: str) -> str:
        """Extracts HTML block from LLM markdown output."""
        match = re.search(r'```html\\s*(.*?)\\s*```', raw_text, re.DOTALL | re.IGNORECASE)
        if match: return match.group(1).strip()
        # Fallback if no markdown block
        start = raw_text.find("<!DOCTYPE html>")
        if start != -1: return raw_text[start:]
        return raw_text

    def generate(self, prompt: str) -> Path:
        print(f"[*] Analyzing prompt: '{prompt}'")
        
        system_prompt = """You are a visionary Frontend Architect. 
Your goal is to generate a single HTML file containing a premium, highly original animated UI based on the user's prompt.
Tech Stack strictly required:
1. Tailwind CSS (via CDN: https://cdn.tailwindcss.com)
2. GSAP for animations (via CDN)
3. Internal <style> for custom glassmorphism, dynamic gradients, or layout specifics missing in Tailwind.
Use modern typography (e.g. from Google Fonts).
Output ONLY raw valid HTML code wrapped in ```html ... ```. No explanations. Provide complete code."""

        user_prompt = f"Create a full-screen landing page section for: {prompt}. Apply complex GSAP reveal animations, deep dark-mode colors with vibrant accents, and high-end tech aesthetic."

        # Adaptive LLM routing
        if self.gemini_key:
            print("[*] Reasoning Engine: GEMINI API")
            raw_response = self._call_gemini(system_prompt, user_prompt)
        else:
            print("[*] Reasoning Engine: OLLAMA LOCAL")
            try:
                raw_response = self._call_ollama(system_prompt, user_prompt)
            except urllib.error.URLError:
                print("[!] ERROR: No GEMINI_API_KEY found, and Ollama is offline/unreachable.")
                print("    Please set setxt GEMINI_API_KEY=<your_key> or start Ollama.")
                sys.exit(1)

        print("[*] Inference complete. Parsing payload...")
        html_code = self.extract_html(raw_response)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = re.sub(r'[^a-z0-9]', '_', prompt.lower())[:15]
        out_file = self.output_dir / f"ai_gen_{safe_name}_{timestamp}.html"
        out_file.write_text(html_code, encoding="utf-8")
        
        return out_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="True AI UI Generator")
    parser.add_argument("--prompt", required=True, help="Description of UI to generate")
    args = parser.parse_args()
    
    gen = TrueAIGenerator()
    try:
        res = gen.generate(args.prompt)
        print(f"\\n[SUCCESS] AI Architect finished. Artifact:")
        print(f"-> {res.absolute()}")
    except Exception as e:
        print(f"\\n[FATAL ERROR] Synthesis failed: {e}")
        sys.exit(1)
