import os
from pathlib import Path

def generate_variable_cinematic():
    print("🎬 NEXUS Design Engine: Variable Repetition (Strict Bounds) [9:16]...")
    
    project_root = Path("e:/Downloads/--ANTIGRAVITY store/IDE-optimus")
    output_path = project_root / "PROJECT" / "outputs" / "Cinematic_Variable_9x16.html"

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1080, height=1920, initial-scale=1.0">
    <title>Legal DevOps - Strict Variable</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Anton&family=Bebas+Neue&family=Inter:wght@900&family=Playfair+Display:ital,wght@1,900&family=Space+Mono:ital,wght@0,700;1,700&family=Syncopate:wght@700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --bg: #050505;
            --c1: #ff003c; /* Red */
            --c2: #00f2ff; /* Cyan */
            --c3: #caff00; /* Acid */
            --c4: #ffffff; /* White */
        }

        * { box-sizing: border-box; cursor: none !important; margin: 0; padding: 0; }
        
        body, html { 
            width: 1080px; height: 1920px; 
            background-color: var(--bg); overflow: hidden; 
            display: flex; align-items: center; justify-content: center;
        }

        /* Abstract Noise */
        .noise {
            position: absolute; width: 100%; height: 100%; top: 0; left: 0;
            background: url('data:image/svg+xml,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="noiseFilter"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23noiseFilter)" opacity="0.1"/%3E%3C/svg%3E');
            mix-blend-mode: overlay; z-index: 100; pointer-events: none;
        }

        /* Containers - STRICT BOUNDARIES */
        .layer { 
            position: absolute; width: 1000px; height: 1840px; /* 40px padding from edges */
            display: flex; align-items: center; justify-content: center; flex-direction: column; opacity: 0; 
        }
        
        /* Grid constrained inside screen */
        .layer-box { 
            position: absolute; width: 900px; height: 1700px; 
            display: flex; flex-wrap: wrap; align-content: center; justify-content: center; gap: 20px; opacity: 0;
        }

        .layer-circle { 
            position: absolute; width: 900px; height: 900px; border-radius: 50%; 
            display: flex; align-items: center; justify-content: center; opacity: 0;
        }

        /* Typography Styles */
        .f-anton { font-family: 'Anton', sans-serif; text-transform: uppercase; }
        .f-bebas { font-family: 'Bebas Neue', sans-serif; text-transform: uppercase; }
        .f-inter { font-family: 'Inter', sans-serif; font-weight: 900; text-transform: uppercase; }
        .f-playfair { font-family: 'Playfair Display', serif; font-weight: 900; font-style: italic; }
        .f-space { font-family: 'Space Mono', monospace; font-weight: 700; text-transform: uppercase; }
        .f-synco { font-family: 'Syncopate', sans-serif; font-weight: 700; text-transform: uppercase; }

        .outline { color: transparent; -webkit-text-stroke: 3px var(--c4); }
        .outline-cyan { color: transparent; -webkit-text-stroke: 4px var(--c2); }

        /* Helpers - Sized to fit perfectly within 1080px width */
        .giant { font-size: 11rem; line-height: 0.9; text-align: center; width: 100vw; }
        .huge { font-size: 10rem; line-height: 0.9; text-align: center; width: 100vw; }
        .large { font-size: 8rem; line-height: 1; text-align: center; width: 100vw; }
        .medium { font-size: 5rem; line-height: 1; text-align: center; }

    </style>
</head>
<body>
    <div class="noise"></div>

    <!-- S1: Clean Inter Reveal -->
    <div class="layer" id="s1">
        <div class="huge f-inter ld-text" style="color:var(--c4)">LEGAL</div>
        <div class="huge f-inter ld-text" style="color:var(--c1)">DEVOPS</div>
    </div>

    <!-- S2: Syncopate Outline Expand (Smaller so it doesn't clip) -->
    <div class="layer" id="s2">
        <div class="giant f-synco outline ld-text" style="position:absolute; top:30%;">LEGAL</div>
        <div class="giant f-synco outline ld-text" style="position:absolute; bottom:30%;">DEVOPS</div>
    </div>

    <!-- S3: Constrained Grid (Random fonts inside the box) -->
    <div class="layer-box" id="s3">
        <!-- JS generated -->
    </div>

    <!-- S4: Serif Italic Elegance (Fits in box) -->
    <div class="layer" id="s4" style="background:var(--c1); border: 20px solid var(--bg); border-radius: 40px; height: 1600px;">
        <div class="huge f-playfair ld-text" style="color:var(--bg)">Legal</div>
        <div class="huge f-playfair ld-text" style="color:var(--bg)">DevOps</div>
    </div>

    <!-- S5: Space Mono Code Block -->
    <div class="layer" id="s5">
        <div class="large f-space ld-text" style="color:var(--c2); text-align: center;">
            > LEGAL_<br>> DEVOPS.EXE
        </div>
    </div>

    <!-- S6: Circular Anton (Exactly fits screen width) -->
    <div class="layer-circle" id="s6" style="background:var(--c3);">
        <div class="large f-anton ld-text" style="color:var(--bg); text-align: center; line-height: 0.8;">LEGAL<br>DEVOPS</div>
    </div>

    <!-- S7: Final Flash (Sized to fit exactly) -->
    <div class="layer" id="s7">
        <div class="f-bebas ld-text" id="s7-legal" style="font-size: 16rem; color:var(--c4); line-height:0.8;">LEGAL</div>
        <div class="f-bebas ld-text" id="s7-devops" style="font-size: 16rem; color:var(--c1); line-height:0.8;">DEVOPS</div>
    </div>

    <script>
        // Generate constrained items for S3
        const grid = document.getElementById('s3');
        const fonts = ['f-anton', 'f-bebas', 'f-inter', 'f-playfair', 'f-space', 'f-synco'];
        const colors = ['var(--c1)', 'var(--c2)', 'var(--c3)', 'var(--c4)'];
        // Generate exactly enough items to fill the 900px box without spilling over
        for(let i=0; i<35; i++) {
            const font = fonts[Math.floor(Math.random() * fonts.length)];
            const color = colors[Math.floor(Math.random() * colors.length)];
            const size = Math.floor(Math.random() * 2) + 2.5; // 2.5 to 4.5 rem
            grid.innerHTML += `<div class="${font}" style="color:${color}; font-size:${size}rem; padding: 5px;">LEGAL DEVOPS</div>`;
        }

        const tl = gsap.timeline();

        // [0.0 - 1.0s] Clean Inter Reveal
        tl.to("#s1", { opacity: 1, duration: 0.1 })
          .fromTo("#s1 .ld-text", { y: 100, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, stagger: 0.1, ease: "power4.out" })
          .to("#s1 .ld-text", { scale: 0.8, opacity: 0, duration: 0.4, ease: "power2.in", delay: 0.1 })
          .set("#s1", { display: "none" })

        // [1.0 - 2.5s] Syncopate Outline (Jitter inside bounds)
          .set("#s2", { opacity: 1 })
          .fromTo("#s2 .ld-text", { scale: 0, rotate: -15 }, { scale: 1, rotate: 0, duration: 0.5, stagger: 0.2, ease: "back.out(2)" })
          .to("#s2 .ld-text", { x: "random(-20, 20)", y: "random(-20, 20)", duration: 0.05, yoyo: true, repeat: 10 })
          .to("#s2", { opacity: 0, duration: 0.1 })

        // [2.5 - 4.5s] Grid Chaos (Pulse inside bounds rather than scrolling out of screen)
          .set("#s3", { opacity: 1 })
          .fromTo("#s3", { scale: 0.5, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: "elastic.out(1, 0.5)" })
          .to("body", { backgroundColor: "var(--c4)", duration: 0.1, yoyo: true, repeat: 5 }, "+=0.5") // Strobe
          .to("#s3", { scale: 1.2, opacity: 0, duration: 0.3, ease: "power2.in" })
          .set("#s3", { display: "none" })

        // [4.5 - 6.0s] Playfair Serif (Sudden Elegance)
          .set("#s4", { opacity: 1 })
          .fromTo("#s4 .ld-text", { filter: "blur(20px)", opacity: 0 }, { filter: "blur(0px)", opacity: 1, duration: 0.5, stagger: 0.2 })
          .to("#s4", { rotateX: 90, duration: 0.4, ease: "power4.in", delay: 0.4 })
          .set("#s4", { display: "none" })

        // [6.0 - 7.5s] Space Mono Code
          .set("#s5", { opacity: 1 })
          .to("body", { backgroundColor: "var(--bg)", duration: 0.1 })
          .fromTo("#s5 .ld-text", { scale: 0.5, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.1, ease: "steps(1)" })
          .to("#s5 .ld-text", { opacity: 0, duration: 0.1, yoyo: true, repeat: 10, ease: "steps(1)" }) // flicker
          .set("#s5", { display: "none" })

        // [7.5 - 9.0s] Circular Yellow Anton
          .set("#s6", { opacity: 1 })
          .fromTo("#s6", { scale: 0 }, { scale: 1, duration: 0.7, ease: "elastic.out(1, 0.5)" })
          .to("#s6 .ld-text", { opacity: 0.5, duration: 0.1, yoyo: true, repeat: 3 }, "+=0.5")  // Flicker text instead of growing offscreen
          .to("#s6", { scale: 0, duration: 0.3, ease: "power4.in" })

        // [9.0 - 10.0s] Final Giant Bebas Flash
          .set("#s7", { opacity: 1 })
          .fromTo("#s7-legal", { scale: 2, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.2, ease: "power4.out" })
          .fromTo("#s7-devops", { scale: 2, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.2, ease: "power4.out" })
          .to("body", { filter: "invert(1)", duration: 0.05, yoyo: true, repeat: 5 }) // Final strobe
          
          .to("#s7", { opacity: 0, duration: 0.1 })
          .to("body", { filter: "none", backgroundColor: "var(--bg)", duration: 0.1 });

    </script>
</body>
</html>"""
    
    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Strict Variable Repetition 10s Promo (9x16) generated: {output_path}")

if __name__ == "__main__":
    generate_variable_cinematic()
