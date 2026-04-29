#!/usr/bin/env python3
"""
VISION_TO_PROMPT [NEXUS SYNTHESIZED Gen-5: VISUAL AUDITOR/CREATIVE DIRECTOR]
Mission: Analyze input content (JPG, PNG, PDF, or URLs) and invent radically new, high-converting advertising/marketing designs.
Heritage: Multi-modal Vision Pipeline + Prompt Engineering

I/O Contract:
  Input:  File path to mockup (--input) OR Website URL (--url)
  Output: Structured text prompt optimized for NEXUS_UI_GENERATOR
"""

import sys
import os
import json
import urllib.request
import urllib.error
import argparse
import base64
from pathlib import Path

class VisualAuditor:
    def __init__(self):
        self.gemini_key = os.environ.get("GEMINI_API_KEY")
        
    def _read_file_as_base64_and_mime(self, file_path: Path) -> tuple[str, str]:
        ext = file_path.suffix.lower()
        mime_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
            ".heic": "image/heic",
            ".heif": "image/heif",
            ".pdf": "application/pdf"
        }
        
        if ext not in mime_map:
            raise ValueError(f"Unsupported file format: {ext}. Only images and PDFs are allowed.")
            
        with open(file_path, "rb") as f:
            b64_data = base64.b64encode(f.read()).decode('utf-8')
            
        return b64_data, mime_map[ext]

    def analyze(self, file_path: str) -> str:
        target = Path(file_path)
        if not target.exists():
            raise FileNotFoundError(f"Target file not found: {target}")
            
        if not self.gemini_key:
            raise EnvironmentError("GEMINI_API_KEY is not set. Visual Auditing requires LLM Vision access.")

        print(f"[*] NEXUS VISUAL AUDITOR extracting data from: {target.name}...")
        
        b64_data, mime_type = self._read_file_as_base64_and_mime(target)
        
        system_prompt = """You are a Native Brand Advertising Director and UI/UX Mastermind.
Your task is to completely redesign the layout into a high-converting Advertising/Marketing Landing Page, WHILE STRICTLY PRESERVING THE ORIGINAL BRAND STYLE.
You must define:
1. A bold, highly creative Hero Section concept with disruptive marketing copy, but it MUST feel native to the original brand identity.
2. The EXACT color palette extracted from the source image (DO NOT invent new colors, strictly extract and reuse the brand's hex codes).
3. The exact typography hierarchy implied by the original design.
4. Aggressive, modern interactions and GSAP motion concepts that enhance the existing style without betraying it (e.g. "fluid brand-colored reveals", "magnetic styled CTAs").

Based on your native advertising concept, output a HIGHLY DETAILED text prompt that can be fed into an AI Code Generator to build this brand-accurate marketing layout.
DO NOT output boilerplate text, just the final Genesis Prompt ready to be piped to the next agent."""

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={self.gemini_key}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": system_prompt},
                        {"inlineData": {"mimeType": mime_type, "data": b64_data}}
                    ]
                }
            ],
            "generationConfig": {"temperature": 0.2} # Low temp for strict analysis
        }
        
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), 
                                     headers={'Content-Type': 'application/json'}, method='POST')
        
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                data = json.loads(response.read().decode())
                extracted_prompt = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                return extracted_prompt
        except urllib.error.HTTPError as e:
            err_body = e.read().decode()
            raise RuntimeError(f"Vision API Error: HTTP {e.code}\\n{err_body}")

    def analyze_url(self, target_url: str) -> str:
        if not self.gemini_key:
            raise EnvironmentError("GEMINI_API_KEY is not set. Visual Auditing requires LLM Vision access.")
            
        print(f"[*] NEXUS VISUAL AUDITOR extracting DOM from: {target_url}...")
        
        req_html = urllib.request.Request(target_url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req_html, timeout=15) as response:
                html_data = response.read().decode('utf-8', errors='ignore')
                # Strict cutoff to prevent token overflow
                html_data = html_data[:75000] 
        except Exception as e:
            raise RuntimeError(f"Failed to fetch URL {target_url}: {e}")

        system_prompt = """You are a Native Brand Advertising Director and UI/UX Mastermind.
Your task is to analyze the provided raw DOM structure of a live website to understand their product, copy, and visual identity (CSS/Classes).
DO NOT copy their current boring structural layout. Instead, INVENT a high-converting Advertising Landing Page concept that STRICTLY USES THEIR EXACT BRAND ASSETS.
You must define:
1. A bold, highly creative Hero Section concept with disruptive marketing copy, but it MUST feel native to the original brand identity.
2. The EXACT color palette extracted from the DOM (CSS variables, tailwind classes, inline hex codes). Do not invent new brand colors.
3. The exact typography families used by the site.
4. Aggressive, modern interactions and GSAP motion concepts that enhance the existing style (e.g. "fluid brand-colored reveals").

Based on your native advertising concept, output a HIGHLY DETAILED text prompt that can be fed into an AI Code Generator to build this brand-accurate marketing layout.
DO NOT output boilerplate text, just the final Genesis Prompt ready to be piped to the next agent."""

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={self.gemini_key}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": system_prompt},
                        {"text": f"WEBSITE SOURCE CODE (Truncated):\\n\\n{html_data}"}
                    ]
                }
            ],
            "generationConfig": {"temperature": 0.2} 
        }
        
        req_llm = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), 
                                     headers={'Content-Type': 'application/json'}, method='POST')
        
        try:
            with urllib.request.urlopen(req_llm, timeout=120) as response:
                data = json.loads(response.read().decode())
                extracted_prompt = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                return extracted_prompt
        except urllib.error.HTTPError as e:
            err_body = e.read().decode()
            raise RuntimeError(f"LLM API Error: HTTP {e.code}\\n{err_body}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="True AI Visual Design Auditor")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-i", "--input", help="Path to JPG/PNG/PDF mockup")
    group.add_argument("-u", "--url", help="URL of a live website to reverse-engineer")
    parser.add_argument("-o", "--output", help="Save the generated prompt to a text file")
    
    args = parser.parse_args()
    
    auditor = VisualAuditor()
    try:
        if args.input:
            final_prompt = auditor.analyze(args.input)
        elif args.url:
            final_prompt = auditor.analyze_url(args.url)
            
        print("\\n" + "="*60)
        print("GENESIS PROMPT (Ready for NEXUS_UI_GENERATOR):\\n")
        print(final_prompt)
        print("="*60 + "\\n")
        
        if args.output:
            Path(args.output).write_text(final_prompt, encoding="utf-8")
            print(f"[+] Saved to: {args.output}")
            
    except Exception as e:
        print(f"\\n[FATAL ERROR] Analysis failed: {e}")
        sys.exit(1)
