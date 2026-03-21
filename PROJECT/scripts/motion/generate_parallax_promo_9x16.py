import os
from pathlib import Path

def generate_parallax_cinematic():
    print("🎬 NEXUS Design Engine: Parallax 3D Image [9:16]...")
    
    project_root = Path("e:/Downloads/--ANTIGRAVITY store/IDE-optimus")
    output_path = project_root / "PROJECT" / "outputs" / "Cinematic_Parallax_9x16.html"
    
    # We will assume both images are placed in assets
    # Image 1 (Scales of Justice): nexus_logo.png
    # Image 2 (City Network): nexus_city.png
    local_img1 = "file:///e:/Downloads/--ANTIGRAVITY store/IDE-optimus/PROJECT/assets/images/nexus_logo.png"
    local_img2 = "file:///e:/Downloads/--ANTIGRAVITY store/IDE-optimus/PROJECT/assets/images/nexus_city.png"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1080, height=1920, initial-scale=1.0">
    <title>NEXUS | Parallax Render</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Space+Mono&display=swap" rel="stylesheet">
    
    <style>
        :root {{
            --bg: #030408;
            --accent: #00f2ff;
        }}

        * {{ box-sizing: border-box; cursor: none !important; }}
        
        body, html {{ 
            margin: 0; padding: 0; width: 1080px; height: 1920px; 
            background-color: var(--bg); overflow: hidden; 
        }}

        .parallax-container {{
            position: absolute; width: 100%; height: 100%;
            perspective: 1200px; overflow: hidden;
        }}

        .parallax-layer {{
            position: absolute; width: 120%; height: 120%;
            top: -10%; left: -10%;
            display: flex; align-items: center; justify-content: center;
            opacity: 0;
        }}

        #layer1 {{ z-index: 5; mix-blend-mode: screen; }} /* Scales of Justice */
        #layer2 {{ z-index: 2; }} /* City Grid */

        img {{ width: 100%; height: 100%; object-fit: cover; }}

        /* Technical Overlays */
        .overlay-mask {{
            position: absolute; top:0; left:0; width:100%; height:100%;
            background: radial-gradient(circle, transparent 40%, rgba(3,4,8,0.95) 100%);
            z-index: 10;
        }}

        .hud-element {{
            position: absolute; font-family: 'Space Mono', monospace;
            color: var(--accent); font-size: 1.5rem; z-index: 20;
            text-transform: uppercase; letter-spacing: 5px; opacity: 0.6;
        }}

        .scanline {{
            position: absolute; width:100%; height: 2px; background: rgba(0,242,255,0.2);
            box-shadow: 0 0 10px var(--accent); z-index: 30; top: 0;
        }}

        .manifesto {{
            position: absolute; bottom: 15rem; left: 80px; width: 920px;
            z-index: 40; color: #fff; transform: translateZ(50px);
        }}
        .m-title {{ font-family: 'Syncopate', sans-serif; font-size: 9rem; margin:0; line-height:0.9; }}
        .m-sub {{ font-size: 3rem; color: var(--accent); letter-spacing: 12px; margin-top: 1rem; }}

    </style>
</head>
<body>
    <div class="parallax-container">
        <div class="parallax-layer" id="layer2">
            <img src="{local_img2}">
        </div>
        <div class="parallax-layer" id="layer1">
            <img src="{local_img1}">
        </div>
        <div class="overlay-mask"></div>
    </div>

    <div class="scanline" id="scan"></div>

    <div class="hud-element" style="top:50px; left:50px;">DECODING_VISUAL_STREAM//04</div>
    <div class="hud-element" style="bottom:50px; left:50px;">NEXUS_CORE_RUNNING</div>

    <div class="manifesto">
        <h1 class="m-title" id="mt">LEGAL</h1>
        <h1 class="m-title" id="mt2">DEVOPS</h1>
        <div class="m-sub" id="ms">INNOVATIVE TECHNOLOGY</div>
    </div>

    <script>
        const tl = gsap.timeline();

        // Initial Reveal
        tl.to("#layer2", {{ opacity: 1, duration: 1.5, scale: 1.2, ease: "power2.out" }})
          .to("#layer1", {{ opacity: 0.8, duration: 1, scale: 1.1, ease: "power4.out" }}, "-=0.5")
          
          // 3D Parallax Motion
          .to("#layer2", {{ x: -50, rotationY: 5, duration: 10, ease: "none" }}, 0)
          .to("#layer1", {{ x: 80, rotationY: -10, scale: 1.3, duration: 10, ease: "none" }}, 0)
          
          // HUD Scan
          .fromTo("#scan", {{ top: "0%" }}, {{ top: "100%", duration: 2, repeat: 4, ease: "none" }}, 0)
          
          // Typography
          .fromTo("#mt", {{ opacity:0, y: 50 }}, {{ opacity:1, y:0, duration: 0.5 }}, 1)
          .fromTo("#mt2", {{ opacity:0, y: 50 }}, {{ opacity:1, y:0, duration: 0.5 }}, 1.3)
          .fromTo("#ms", {{ opacity:0, clipPath: "inset(0 100% 0 0)" }}, {{ opacity:1, clipPath: "inset(0 0 0 0)", duration: 1 }}, 1.8)

          // Glitch Burst
          .to(".parallax-container", {{ x: 20, skewX: 5, duration: 0.05, yoyo: true, repeat: 10, delay: 5 }})
          .to("#layer1", {{ filter: "hue-rotate(180deg)", duration: 0.1, yoyo:true, repeat: 5 }}, "-=0.5")

          // Final Shutdown
          .to("body", {{ filter: "brightness(0)", duration: 0.5, delay: 2 }});

    </script>
</body>
</html>"""
    
    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Parallax 3D Cinematic generated: {output_path}")

if __name__ == "__main__":
    generate_parallax_cinematic()
