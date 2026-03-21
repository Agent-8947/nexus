import os
from pathlib import Path

def generate_blueprint_cinematic():
    print("🎬 NEXUS Design Engine: Technical Blueprint [9:16]...")
    
    project_root = Path("e:/Downloads/--ANTIGRAVITY store/IDE-optimus")
    output_path = project_root / "PROJECT" / "outputs" / "Cinematic_Blueprint_9x16.html"

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1080, height=1920, initial-scale=1.0">
    <title>NEXUS | Technical Blueprint</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --bp-blue: #1a4a9e;
            --bp-line: rgba(255, 255, 255, 0.8);
            --bp-grid: rgba(255, 255, 255, 0.1);
            --bp-dim: rgba(255, 255, 255, 0.4);
            --bp-text: #ffffff;
        }

        * { box-sizing: border-box; cursor: none !important; font-family: 'Space Mono', monospace; }
        
        body, html { 
            margin: 0; padding: 0; width: 1080px; height: 1920px; 
            background-color: var(--bp-blue); overflow: hidden; 
            color: var(--bp-text);
        }

        /* Blueprint Grid */
        .blueprint-bg {
            position: absolute; width: 100%; height: 100%;
            background-image: 
                linear-gradient(var(--bp-grid) 1px, transparent 1px),
                linear-gradient(90deg, var(--bp-grid) 1px, transparent 1px),
                linear-gradient(rgba(255,255,255,0.05) 2px, transparent 2px),
                linear-gradient(90deg, rgba(255,255,255,0.05) 2px, transparent 2px);
            background-size: 20px 20px, 20px 20px, 100px 100px, 100px 100px;
            z-index: 0;
        }

        .container {
            position: absolute; width: 100%; height: 100%; z-index: 10;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            padding: 100px;
        }

        /* Technical Elements */
        .measure-line { position: absolute; background: var(--bp-line); opacity: 0; }
        .h-line { height: 1px; width: 0; }
        .v-line { width: 1px; height: 0; }
        
        .dim-label {
            position: absolute; font-size: 1.2rem; color: var(--bp-dim);
            text-transform: uppercase; white-space: nowrap; opacity: 0;
        }

        .border-corner {
            position: absolute; width: 150px; height: 150px;
            border: 2px solid var(--bp-line); opacity: 0;
        }
        .tl { top: 40px; left: 40px; border-right: none; border-bottom: none; }
        .tr { top: 40px; right: 40px; border-left: none; border-bottom: none; }
        .bl { bottom: 40px; left: 40px; border-right: none; border-top: none; }
        .br { bottom: 40px; right: 40px; border-left: none; border-top: none; }

        /* Typography */
        .title-block { text-align: center; position: relative; }
        .main-title { font-size: 12rem; font-weight: 700; line-height: 0.8; letter-spacing: -5px; opacity: 0; }
        .sub-title { font-size: 4rem; opacity: 0; background: var(--bp-text); color: var(--bp-blue); padding: 5px 20px; margin-top: 20px; }

        /* SVG Components */
        .svg-container { position: absolute; width: 100%; height: 100%; top: 0; left: 0; z-index: 5; pointer-events: none; }
        .draw-path { fill: none; stroke: var(--bp-line); stroke-width: 2; stroke-dasharray: 2000; stroke-dashoffset: 2000; }

        /* Scanning effect */
        .scanner {
            position: absolute; width: 100%; height: 4px; background: #fff;
            box-shadow: 0 0 20px #fff, 0 0 40px var(--bp-blue);
            top: -10px; z-index: 100; display: none;
        }

        /* Callouts */
        .callout {
            position: absolute; display: flex; align-items: center; opacity: 0;
        }
        .callout-box { border: 1px solid var(--bp-line); padding: 10px 20px; font-size: 1.5rem; background: rgba(0,0,0,0.2); }
        .callout-line { width: 100px; height: 1px; background: var(--bp-line); position: relative; }
        .callout-dot { width: 8px; height: 8px; background: var(--bp-text); border-radius: 50%; position: absolute; right: -4px; top: -4px; }

    </style>
</head>
<body>
    <div class="blueprint-bg"></div>
    <div class="scanner" id="scan-line"></div>

    <svg class="svg-container">
        <!-- Large Circle Frame -->
        <circle id="circ-frame" class="draw-path" cx="540" cy="960" r="450" />
        <!-- Crosshairs -->
        <line class="draw-path" x1="0" y1="960" x2="1080" y2="960" opacity="0.3" />
        <line class="draw-path" x1="540" y1="0" x2="540" y2="1920" opacity="0.3" />
        
        <rect id="rect-frame" class="draw-path" x="90" y="460" width="900" height="1000" />
    </svg>

    <!-- Corners -->
    <div class="border-corner tl"></div>
    <div class="border-corner tr"></div>
    <div class="border-corner bl"></div>
    <div class="border-corner br"></div>

    <!-- Dimensions -->
    <div class="dim-label" style="top: 20px; left: 50%; transform: translateX(-50%);">SCALE: 1:1 [ENGINEERING_MODE]</div>
    <div class="dim-label" style="bottom: 20px; right: 60px;">ID: NEXUS-V2026.1-MAS</div>

    <div class="container">
        <!-- Scene 1: Initial Plot -->
        <div class="title-block" id="s1">
            <h1 class="main-title" id="t1">LEGAL</h1>
            <h1 class="main-title" id="t2">DEVOPS</h1>
            <div class="sub-title" id="st1">SYST_STRUCT_V04</div>
        </div>

        <!-- CALLOUTS -->
        <div class="callout" id="c1" style="top: 25%; left: 100px;">
            <div class="callout-box">AUTO_CORE</div>
            <div class="callout-line"><div class="callout-dot"></div></div>
        </div>

        <div class="callout" id="c2" style="bottom: 25%; right: 100px; flex-direction: row-reverse;">
            <div class="callout-box">ALGO_PRESSURE</div>
            <div class="callout-line"><div class="callout-dot" style="left:-4px;"></div></div>
        </div>
    </div>

    <script>
        const tl = gsap.timeline();

        // 1. Initial Measurement Construction (0-3s)
        tl.to(".border-corner", { opacity: 1, duration: 0.1, stagger: 0.1 })
          .to(".dim-label", { opacity: 0.5, duration: 0.3, stagger: 0.2 })
          
          .to(".draw-path", { strokeDashoffset: 0, duration: 1.5, ease: "power2.inOut", stagger: 0.2 })
          
          .fromTo("#t1", { clipPath: "inset(0 100% 0 0)", opacity: 1 }, { clipPath: "inset(0 0% 0 0)", duration: 0.8, ease: "power1.inOut" })
          .fromTo("#t2", { clipPath: "inset(0 100% 0 0)", opacity: 1 }, { clipPath: "inset(0 0% 0 0)", duration: 0.8, ease: "power1.inOut" }, "-=0.4")
          .to("#st1", { opacity: 1, y: 10, duration: 0.3, ease: "back.out(2)" })

        // 2. Callout Deployment (3-6s)
          .to(".callout", { opacity: 1, duration: 0.5, stagger: 0.3 })
          .to(".callout-line", { width: 150, duration: 0.5, ease: "power4.out" }, "-=0.6")
          
          // Technical Shake
          .to(".container", { x: 5, rotateZ: 0.5, duration: 0.05, yoyo: true, repeat: 5 })

        // 3. System Scan (6-8.5s)
          .set("#scan-line", { display: "block" })
          .fromTo("#scan-line", { top: "0%" }, { top: "100%", duration: 1.5, ease: "none" })
          .to("body", { filter: "hue-rotate(90deg)", duration: 0.1, yoyo: true, repeat: 1 }, "-=1.0")
          
          // Data glitch update
          .to("#t1, #t2", { textContent: "DECODING...", duration: 0.1, delay: 0.5 })
          .to("#t1", { textContent: "LEGAL", duration: 0.1 })
          .to("#t2", { textContent: "DEVOPS", duration: 0.1 })

        // 4. Outro Collapse (8.5-10s)
          .to(".callout, .sub-title", { opacity: 0, scale: 0, duration: 0.3 })
          .to(".draw-path", { strokeDashoffset: 2000, duration: 0.8, ease: "power4.in" })
          .to(".main-title", { scale: 0.5, opacity: 0, duration: 0.4, ease: "power4.in" }, "-=0.4")
          
          .to("body", { backgroundColor: "#000", duration: 0.2 })
          .to(".blueprint-bg, .border-corner", { opacity: 0, duration: 0.2 }, "-=0.1");

    </script>
</body>
</html>"""
    
    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Technical Blueprint 10s Promo (9x16) generated: {output_path}")

if __name__ == "__main__":
    generate_blueprint_cinematic()
