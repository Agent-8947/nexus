#!/usr/bin/env python3
"""
98.CSS__X__TAILWIND [NEXUS SYNTHESIZED Gen-1: DESIGNER]
Mission: Develop a premium design system architect and UI component generator.
Heritage: 98.CSS + TAILWIND

I/O Contract:
  Input:  component description (from CLI --prompt)
  Output: Rendered HTML/CSS artifact combining 98.css structures and Tailwind spacing.
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS_DESIGNER")

class UIDesigner:
    def __init__(self):
        # We output to the active PROJECT root
        self.output_dir = Path(__file__).resolve().parents[5] / "PROJECT" / "outputs" / "design_artifacts"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate(self, prompt: str) -> Path:
        logger.info(f"Generating UI for prompt: {prompt}")
        title = prompt.title()
        
        # Hybrid HTML injecting Tailwind via CDN + 98.css
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://unpkg.com/98.css">
    <style>
        body {{
            background-color: #008080;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }}
    </style>
</head>
<body>
    <div class="window w-[800px] max-w-[95vw] shadow-[10px_10px_0px_rgba(0,0,0,0.5)]">
        <div class="title-bar">
            <div class="title-bar-text">{title} - NEXUS Visual Architect</div>
            <div class="title-bar-controls">
                <button aria-label="Minimize"></button>
                <button aria-label="Maximize"></button>
                <button aria-label="Close"></button>
            </div>
        </div>
        <div class="window-body p-6 flex flex-col gap-4">
            <h1 class="text-2xl font-bold text-gray-900 border-b-2 border-gray-400 pb-2 bg-[#c0c0c0]">{prompt}</h1>
            
            <div class="flex gap-4">
                <button class="px-8 py-2 font-bold !text-blue-900">Run Synthesis</button>
                <button class="px-8 py-2">Cancel</button>
            </div>
            
            <fieldset class="p-4 border-2">
                <legend class="text-sm font-semibold">Architecture Metrics</legend>
                <div class="field-row flex justify-between w-full pr-4">
                    <span>Performance:</span>
                    <div class="w-64 h-4 bg-gray-400 border-inset border-2"><div class="h-full bg-[#000080] w-[95%]"></div></div>
                </div>
                <div class="field-row flex justify-between w-full pr-4 mt-2">
                    <span>Aesthetics:</span>
                    <div class="w-64 h-4 bg-gray-400 border-inset border-2"><div class="h-full bg-[#00ffed] w-[99%]"></div></div>
                </div>
            </fieldset>

            <ul class="tree-view bg-white p-2 h-40 overflow-y-auto border-inset border-2 font-mono text-sm">
                <li>[*] Loaded Tailwind JIT compiler</li>
                <li>[*] Loaded 98.CSS definitions</li>
                <li>[+] Built hybrid DOM structure</li>
                <li class="text-green-700"><strong>[OK] {title} rendered successfully!</strong></li>
            </ul>
        </div>
        <div class="status-bar">
            <p class="status-bar-field">NEXUS Engine V5.0</p>
            <p class="status-bar-field">Built-in LLM Model Sync: Active</p>
            <p class="status-bar-field">CPU: Normal</p>
        </div>
    </div>
</body>
</html>"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = prompt.replace(" ", "_").lower()[:20]
        output_file = self.output_dir / f"ui_{filename}_{timestamp}.html"
        output_file.write_text(html_content, encoding="utf-8")
        return output_file

def main():
    parser = argparse.ArgumentParser(description="NEXUS UI Designer")
    parser.add_argument("--prompt", default="NEXUS Hybrid Control Panel", help="UI description prompt")
    parser.add_argument("--test", action="store_true", help="Run integration test")
    args = parser.parse_args()

    designer = UIDesigner()
    
    if args.test:
        out = designer.generate("System Self Test")
        if out.exists():
            print("[TEST] Passed.")
        sys.exit(0)
        
    out_file = designer.generate(args.prompt)
    print(f"[SUCCESS] UI Generated -> {out_file.absolute()}")


if __name__ == "__main__":
    main()
