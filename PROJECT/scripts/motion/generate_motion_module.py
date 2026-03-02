import os
import json
from pathlib import Path

def generate_motion_demo():
    print("🎬 Initializing NEXUS Motion Engine...")
    
    project_root = Path("e:/Downloads/--ANTIGRAVITY store/IDE-optimus")
    output_path = project_root / "PROJECT" / "outputs" / "Motion_Premium_Showcase.html"
    
    # HTML template with embedded nexus-visual-motion patterns
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXUS | MOTION PREMIUM</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
    <script src="https://unpkg.com/lenis@1.0.45/dist/lenis.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #050505;
            --accent: #ffffff;
            --text-dim: #64748b;
        }
        body { 
            margin: 0; background: var(--bg); color: var(--accent); 
            font-family: 'Outfit', sans-serif; overflow-x: hidden;
        }
        .section {
            height: 100vh; display: flex; flex-direction: column;
            align-items: center; justify-content: center; position: relative;
        }
        .reveal-text {
            font-size: 8vw; font-weight: 700; line-height: 1;
            clip-path: polygon(0 0, 100% 0, 100% 100%, 0% 100%);
            margin: 0; text-transform: uppercase;
        }
        .sub-text {
            color: var(--text-dim); font-size: 1.5vw; font-weight: 300;
            margin-top: 20px; opacity: 0;
        }
        .glow-box {
            width: 300px; height: 300px; border: 1px solid rgba(255,255,255,0.1);
            position: absolute; z-index: -1; transform: rotate(45deg);
            background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%);
        }
        .scroll-indicator {
            position: absolute; bottom: 40px; font-size: 0.8rem;
            letter-spacing: 0.3em; opacity: 0.5;
        }
    </style>
</head>
<body>
    <div class="section" id="hero">
        <div class="glow-box" id="glow"></div>
        <h1 class="reveal-text">Nexus</h1>
        <h1 class="reveal-text" style="color:transparent; -webkit-text-stroke: 1px var(--accent);">Motion</h1>
        <p class="sub-text">Architectural Dynamics v1.0</p>
        <div class="scroll-indicator">SCROLL TO ANALYZE</div>
    </div>

    <div class="section" id="feature">
        <h1 class="reveal-text" style="font-size: 4vw;">Precision</h1>
        <p class="sub-text">120 FPS Rendering Pipeline</p>
    </div>

    <script>
        // 1. Initialize Lenis (Landed Liquid Scroll)
        const lenis = new Lenis();
        function raf(time) {
            lenis.raf(time);
            requestAnimationFrame(raf);
        }
        requestAnimationFrame(raf);

        // 2. GSAP Animations
        gsap.registerPlugin(ScrollTrigger);

        // Hero Reveal
        const tl = gsap.timeline();
        tl.from(".reveal-text", {
            y: 200, duration: 1.5, ease: "power4.out", stagger: 0.2, delay: 0.5
        })
        .to(".sub-text", { opacity: 1, y: -20, duration: 1 }, "-=0.5")
        .from("#glow", { scale: 0, opacity: 0, duration: 2, ease: "elastic.out(1, 0.3)" }, "-=1");

        // Parallax & Scroll Effects
        gsap.to("#glow", {
            scrollTrigger: {
                trigger: "#hero",
                start: "top top",
                end: "bottom top",
                scrub: true
            },
            rotate: 225,
            scale: 2,
            opacity: 0.2
        });

        // Feature Reveal
        gsap.from("#feature .reveal-text", {
            scrollTrigger: {
                trigger: "#feature",
                start: "top 80%",
            },
            y: 100, duration: 1, ease: "power3.out"
        });
    </script>
</body>
</html>"""
    
    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"✅ Motion Showcase generated: {output_path}")

if __name__ == "__main__":
    generate_motion_demo()
