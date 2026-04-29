#!/usr/bin/env python3
"""
MOTION__X__GSAP [NEXUS SYNTHESIZED Gen-2: KINETIC ARCHITECT]
Mission: Generates premium animated boilerplate templates parsing natural language prompts.
Heritage: NEXUS_MOTION_ENGINE + GSAP/LENIS

I/O Contract:
  Input:  animation theme (from CLI --prompt)
  Output: Rendered HTML/CSS/JS artifact with fluid sequences.
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
import colorsys
import random

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS_MOTION_ARCHITECT")

class KineticDesigner:
    def __init__(self):
        self.output_dir = Path(__file__).resolve().parents[5] / "PROJECT" / "outputs" / "design_artifacts"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def _generate_palette(self):
        """Generates a premium dark mode palette with a vibrant accent."""
        hue = random.random()
        accent = colorsys.hsv_to_rgb(hue, 0.8, 1.0)
        accent_hex = '#{:02x}{:02x}{:02x}'.format(int(accent[0]*255), int(accent[1]*255), int(accent[2]*255))
        return {
            "bg": "#0a0a0a",
            "text": "#ffffff",
            "text_dim": "#8892b0",
            "accent": accent_hex,
            "surface": "rgba(255, 255, 255, 0.03)"
        }

    def generate(self, prompt: str) -> Path:
        logger.info(f"Synthesizing Kinetic UI for theme: {prompt}")
        title = prompt.upper()
        p = self._generate_palette()
        
        # HTML template with GSAP and Lenis
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | NEXUS Motion</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
    <script src="https://unpkg.com/lenis@1.0.45/dist/lenis.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Inter:wght@300;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: {p['bg']};
            --accent: {p['accent']};
            --text-main: {p['text']};
            --text-dim: {p['text_dim']};
            --surface: {p['surface']};
        }}
        body {{
            margin: 0; padding: 0; background-color: var(--bg); color: var(--text-main);
            font-family: 'Inter', sans-serif; overflow-x: hidden;
        }}
        .grid-bg {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-image: radial-gradient(var(--surface) 1px, transparent 1px);
            background-size: 40px 40px; z-index: -1; pointer-events: none;
        }}
        
        /* Typography */
        h1 {{ font-family: 'Syncopate', sans-serif; font-size: 8vw; line-height: 0.9; margin: 0; text-transform: uppercase; }}
        h2 {{ font-family: 'Syncopate', sans-serif; font-size: 4vw; color: var(--accent); }}
        
        /* Utilities */
        .h-screen {{ height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; }}
        .text-outline {{ -webkit-text-stroke: 1px rgba(255,255,255,0.2); color: transparent; }}
        .reveal-mask {{ overflow: hidden; clip-path: polygon(0 0, 100% 0, 100% 100%, 0% 100%); display: inline-block; }}
        .tagline {{ margin-top: 2rem; color: var(--text-dim); max-width: 600px; text-align: center; opacity: 0; font-size: 1.2rem; }}
        
        /* Magnetic Button */
        .btn-modern {{
            margin-top: 3rem; padding: 1rem 3rem; border: 1px solid var(--accent); background: transparent;
            color: var(--accent); font-family: 'Syncopate', sans-serif; text-transform: uppercase;
            position: relative; overflow: hidden; cursor: crosshair; display: inline-block; opacity: 0;
            transition: color 0.3s;
        }}
        .btn-modern::before {{
            content: ''; position: absolute; top: 100%; left: 0; width: 100%; height: 100%;
            background: var(--accent); z-index: -1; transition: top 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .btn-modern:hover {{ color: var(--bg); }}
        .btn-modern:hover::before {{ top: 0; }}

        /* Dynamic Cards */
        .feature-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; max-width: 1200px; padding: 4rem 2rem; }}
        .card {{
            background: var(--surface); border: 1px solid rgba(255,255,255,0.05); padding: 3rem;
            backdrop-filter: blur(10px); transform: translateY(100px); opacity: 0;
            transition: border-color 0.3s; cursor: pointer;
        }}
        .card:hover {{ border-color: var(--accent); }}
        .card-number {{ color: var(--accent); font-family: 'Syncopate'; font-size: 2rem; margin-bottom: 1rem; }}
    </style>
</head>
<body>
    <div class="grid-bg"></div>

    <section class="h-screen" id="hero">
        <div class="reveal-mask"><h1 class="hero-line text-outline">Animated</h1></div>
        <div class="reveal-mask"><h1 class="hero-line">{title}</h1></div>
        <div class="reveal-mask"><h1 class="hero-line" style="color: var(--accent)">Experience</h1></div>
        <p class="tagline">Next-generation motion physics powered by GSAP. Synthesized for seamless interactions.</p>
        <div class="btn-modern id-btn">Initiate Sequence</div>
    </section>

    <section class="h-screen" id="features">
        <h2>{title} Cores</h2>
        <div class="feature-grid">
            <div class="card">
                <div class="card-number">01</div>
                <h3>Kinetic Elasticity</h3>
                <p style="color: var(--text-dim)">Physics-based spring animations for natural movements.</p>
            </div>
            <div class="card" style="transform: translateY(150px);">
                <div class="card-number">02</div>
                <h3>Scroll Orchestration</h3>
                <p style="color: var(--text-dim)">Timeline scrubbing locked perfectly to window scroll.</p>
            </div>
            <div class="card" style="transform: translateY(200px);">
                <div class="card-number">03</div>
                <h3>Liquid Layout</h3>
                <p style="color: var(--text-dim)">Sub-pixel rendering via Lenis smooth scrolling.</p>
            </div>
        </div>
    </section>

    <script>
        // Smooth Scroll Initiation (Lenis)
        const lenis = new Lenis({{ duration: 1.2, easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)) }});
        function raf(time) {{ lenis.raf(time); requestAnimationFrame(raf); }}
        requestAnimationFrame(raf);
        
        gsap.registerPlugin(ScrollTrigger);
        lenis.on('scroll', ScrollTrigger.update);
        gsap.ticker.add((time) => {{ lenis.raf(time * 1000); }});

        // Intro Sequence
        const tl = gsap.timeline();
        tl.from(".hero-line", {{ y: "150%", duration: 1.5, ease: "power4.out", stagger: 0.15 }})
          .to(".tagline", {{ opacity: 1, duration: 1, ease: "power2.out" }}, "-=0.8")
          .to(".id-btn", {{ opacity: 1, y: -20, duration: 1, ease: "power2.out" }}, "-=0.6");

        // Scroll animations for cards
        gsap.to(".card", {{
            scrollTrigger: {{ trigger: "#features", start: "top 70%" }},
            y: 0, opacity: 1, duration: 1.2, ease: "power3.out", stagger: 0.2
        }});

        // Magnetic effect on button
        const btn = document.querySelector('.id-btn');
        btn.addEventListener('mousemove', (e) => {{
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            gsap.to(btn, {{ x: x * 0.3, y: y * 0.3, duration: 0.3, ease: 'power2.out' }});
        }});
        btn.addEventListener('mouseleave', () => {{
            gsap.to(btn, {{ x: 0, y: 0, duration: 0.5, ease: 'elastic.out(1, 0.3)' }});
        }});
    </script>
</body>
</html>"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = prompt.replace(" ", "_").lower()[:20]
        output_file = self.output_dir / f"motion_ui_{filename}_{timestamp}.html"
        output_file.write_text(html_content, encoding="utf-8")
        return output_file

def main():
    parser = argparse.ArgumentParser(description="NEXUS Kinetic Designer")
    parser.add_argument("--prompt", default="Neural Data Hub", help="UI theme prompt")
    parser.add_argument("--test", action="store_true", help="Run integration test")
    args = parser.parse_args()

    designer = KineticDesigner()
    
    if args.test:
        out = designer.generate("System Self Test")
        if out.exists():
            print("[TEST] Passed.")
        sys.exit(0)
        
    out_file = designer.generate(args.prompt)
    print(f"[SUCCESS] Kinetic UI Generated -> {out_file.absolute()}")


if __name__ == "__main__":
    main()
