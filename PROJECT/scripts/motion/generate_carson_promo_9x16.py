import os
from pathlib import Path

def generate_carson_cinematic():
    print("🎬 NEXUS Design Engine: Carson Grunge [9:16]...")
    
    project_root = Path("e:/Downloads/--ANTIGRAVITY store/IDE-optimus")
    output_path = project_root / "PROJECT" / "outputs" / "Cinematic_Carson_9x16.html"
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1080, height=1920, initial-scale=1.0">
    <title>NEXUS | Carson Grunge 10s</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@700&family=Permanent+Marker&family=Courier+Prime:ital,wght@0,400;1,700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --ray-ink: #1c1b18;
            --ray-dirt: #e8e5d9;
            --ray-acid: #caff00;
        }

        * { box-sizing: border-box; cursor: none !important; }
        
        body, html { 
            margin: 0; padding: 0; width: 1080px; height: 1920px; 
            background-color: var(--ray-dirt); overflow: hidden; 
        }

        /* SVG Noise Filter */
        .noise-bg {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; pointer-events: none;
            background: url('data:image/svg+xml,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="noiseFilter"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23noiseFilter)" opacity="0.4"/%3E%3C/svg%3E');
            mix-blend-mode: overlay;
        }

        .scene { position: absolute; width: 100%; height: 100%; z-index: 10; display: none; }
        
        /* Typography Elements */
        .font-grunge { font-family: 'Oswald', sans-serif; text-transform: uppercase; }
        .font-marker { font-family: 'Permanent Marker', cursive; }
        .font-typewriter { font-family: 'Courier Prime', monospace; }

        .giant-bg-text {
            position: absolute; font-size: 200vw; color: var(--ray-ink); 
            opacity: 0.05; white-space: nowrap; line-height: 0.7; z-index: 0;
            user-select: none;
        }

        /* TORN PAPER CLIPS */
        .torn-clip-1 { clip-path: polygon(0% 0%, 100% 5%, 98% 95%, 2% 100%, 5% 50%); }
        .torn-clip-2 { clip-path: polygon(5% 0%, 95% 2%, 100% 100%, 0% 98%, 2% 40%); }
        .torn-clip-3 { clip-path: polygon(0 10%, 100% 0, 90% 100%, 10% 90%); }

        .glass-box {
            position: absolute; background: rgba(255, 255, 255, 0.5); backdrop-filter: blur(5px);
            border: 4px solid var(--ray-ink); box-shadow: 15px 15px 0 var(--ray-acid);
            display: flex; flex-direction: column; align-items: center; justify-content: center;
        }

        /* ---- SCENE 1: Chaos Boot ---- */
        #scene-chaos { display: block; mix-blend-mode: multiply; }
        .chaos-word {
            position: absolute; color: var(--ray-ink); opacity: 0;
            transform-origin: center;
        }

        /* ---- SCENE 2: The Magazine Slam ---- */
        #scene-mag { perspective: 1000px; display: none; }
        .legal-word {
            font-size: 14rem; position: absolute; letter-spacing: -10px; line-height: 0.8;
            top: 25%; left: 0; width: 100%; text-align: center; opacity: 0;
            color: var(--ray-ink); text-shadow: -10px 10px 0 var(--ray-acid);
            mix-blend-mode: multiply;
        }
        .devops-word {
            font-size: 16rem; position: absolute; top: 45%; left: -10%; 
            color: var(--ray-dirt); -webkit-text-stroke: 4px var(--ray-ink); opacity: 0;
        }

        .scribble { color: var(--ray-ink); font-size: 8rem; position: absolute; z-index: 50; opacity: 0; }
        
        /* ---- SCENE 3: Torn Data Cards ---- */
        #scene-torn { display: none; }
        .torn-card { width: 800px; height: 500px; padding: 80px; text-align: center; opacity: 0;}
        .c1 { top: 15%; left: 10%; transform: rotate(-8deg); }
        .c2 { top: 40%; left: 15%; transform: rotate(12deg); border-color: var(--ray-acid); box-shadow: -15px -15px 0 var(--ray-ink); }
        .c3 { top: 70%; left: 5%; transform: rotate(-5deg); background: var(--ray-acid); border: 8px solid var(--ray-ink); box-shadow: 25px 25px 0 rgba(255,255,255,0.8); }
        
        .c-title { font-size: 6rem; letter-spacing: -5px; line-height: 0.8; margin:0;}
        .c-mark { font-size: 8rem; color: var(--ray-ink); line-height: 0.6; margin:0;}

        /* ---- SCENE 4: Carson Outro ---- */
        #scene-outro { display: none; }
        .outro-container {
            width: 900px; height: 1200px; position: absolute;
            top: 50%; left: 50%; transform: translate(-50%, -50%);
            background: var(--ray-ink); color: var(--ray-dirt);
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            opacity: 0;
        }
        .vertical-text { position: absolute; right: 2rem; top: 2rem; writing-mode: vertical-rl; text-orientation: mixed; font-size: 3rem; color: var(--ray-acid); }
        .o-title { font-size: 16rem; line-height: 0.8; margin-top: 100px; z-index: 10; padding: 40px;}
        .o-desc { font-size: 2.5rem; text-align: center; width: 70%; margin-top: 40px;}

        /* Random elements */
        .circle-stamp { position: absolute; width: 300px; height: 300px; border-radius: 50%; background: var(--ray-acid); opacity: 0; mix-blend-mode: multiply; z-index: -1; }
        .tape { position: absolute; width: 400px; height: 100px; background: rgba(255,255,255,0.4); backdrop-filter: blur(2px); transform: rotate(-25deg); top: -20px; left: 100px; opacity: 0; z-index: 60;}

    </style>
</head>
<body>
    <div class="giant-bg-text font-grunge" id="bg-t1" style="top: 0; left: -50%;">CHAOS</div>
    <div class="giant-bg-text font-grunge" id="bg-t2" style="top: 20%; left: -20%; display:none;">NULL</div>
    <div class="noise-bg"></div>

    <div class="scene" id="scene-chaos">
        <div class="chaos-word font-typewriter" style="top: 10%; left: 5%; font-size: 4rem;">import SYSTEM</div>
        <div class="chaos-word font-typewriter" style="top: 20%; right: 10%; font-size: 3rem;">err_fatal</div>
        <div class="chaos-word font-grunge" style="top: 40%; left: 20%; font-size: 15rem; transform: rotate(-90deg);">BREAK</div>
        <div class="chaos-word font-marker" style="top: 60%; right: 20%; font-size: 8rem; color: var(--ray-acid);">IGNORE.</div>
        <div class="chaos-word font-grunge" style="top: 80%; left: 5%; font-size: 10rem; letter-spacing:-10px;">GRID IS DEAD</div>
    </div>

    <div class="scene" id="scene-mag">
        <div class="circle-stamp" id="stamp-1" style="top: 20%; left: 10%;"></div>
        <div class="circle-stamp" id="stamp-2" style="top: 50%; right: -5%;"></div>
        
        <div class="legal-word font-grunge">LEGAL</div>
        <div class="devops-word font-grunge">DEVOPS</div>
        
        <div class="scribble font-marker" id="scr1" style="top: 35%; right: 5%; transform: rotate(15deg);">NOT SO FAST</div>
        <div class="scribble font-typewriter" id="scr2" style="top: 62%; left: 15%; background: var(--ray-ink); color: #fff; padding: 10px;">> ERROR 404: RULES</div>
        
        <div class="tape" id="tape1"></div>
    </div>

    <div class="scene" id="scene-torn">
        <div class="glass-box torn-card torn-clip-1 font-grunge c1">
            <h2 class="c-title">CHAOS DETECTED</h2>
            <div class="c-mark font-marker" style="margin-top: 50px;">ELIMINATE</div>
        </div>
        <div class="glass-box torn-card torn-clip-2 font-grunge c2">
            <h2 class="c-title" style="color:var(--ray-ink);">EFFICIENCY</h2>
            <div class="c-mark font-marker" style="color:var(--ray-acid); font-size: 10rem; -webkit-text-stroke: 2px var(--ray-ink);">1200X</div>
        </div>
        <div class="glass-box torn-card torn-clip-3 font-grunge c3">
            <h2 class="c-title" style="color:var(--ray-ink);">AGENTS</h2>
            <div class="c-mark font-typewriter">>_ACTIVE</div>
        </div>
    </div>

    <div class="scene" id="scene-outro">
        <div class="glass-box outro-container torn-clip-1 font-grunge">
            <div class="vertical-text font-typewriter">AUTO.MAS.V2026.1</div>
            <h1 class="o-title" style="background:var(--ray-acid); color:var(--ray-ink); transform:rotate(-5deg)">NEXUS</h1>
            <div class="o-desc font-typewriter">ARCHITECTURAL LAW REBUILT</div>
            <div class="font-marker" style="position: absolute; bottom: 50px; right: 50px; font-size: 5rem; color: var(--ray-acid); transform:rotate(-15deg);">DONE.</div>
        </div>
        <div class="tape" id="tape2" style="top:250px; left:10px; transform:rotate(12deg); background: var(--ray-acid);"></div>
        <div class="tape" id="tape3" style="bottom:250px; right:120px; transform:rotate(-50deg);"></div>
    </div>

    <script>
        // CARSON GRUNGE TIMELINE (10 Seconds, Chaotic, Unpredictable)
        const tl = gsap.timeline();

        // 0.0 - 2.5s: Typographic Chaos
        tl.fromTo(".chaos-word", 
            { y: 50, scale: 0.5, rotate: "random(-45, 45)" },
            { opacity: 1, y: 0, scale: 1, duration: 0.1, stagger: 0.1, ease: "steps(2)" }
        )
        .to(".chaos-word", { rotate: "random(-90, 90)", x: "random(-200, 200)", duration: 0.1, yoyo: true, repeat: 5, ease: "steps(1)" })
        .to("#scene-chaos", { opacity: 0, duration: 0.1, delay: 0.2 })
        
        // Background Glitch
        .to("#bg-t1", { x: -500, opacity: 0, duration: 0.1 })
        .set("#bg-t2", { display: "block" })
        .to("#bg-t2", { opacity: 0.05, duration: 0.1 })
        
        // 2.5 - 5.0s: The Magazine Cover Slam
        .set("#scene-mag", { display: "block" })
        .to("#stamp-1", { opacity: 1, scale: "random(0.8, 1.5)", duration: 0.1 })
        
        .fromTo(".legal-word",
            { scale: 5, opacity: 0, rotateZ: 25 },
            { scale: 1, opacity: 1, rotateZ: -5, duration: 0.3, ease: "none" }
        )
        // Hard jitter (Carson style isn't smooth)
        .to(".legal-word", { x: 20, y: -20, duration: 0.05, yoyo: true, repeat: 3, ease: "steps(1)" })
        
        .to("#stamp-2", { opacity: 1, scale: "random(0.5, 2)", duration: 0.1 }, "-=0.2")
        
        .fromTo(".devops-word",
            { x: -1000, opacity: 0, rotateZ: -10 },
            { x: 0, opacity: 1, rotateZ: 5, duration: 0.3, ease: "none" }, "-=0.1"
        )
        .to(".devops-word", { letterSpacing: "20px", duration: 0.1, yoyo: true, repeat: 2, ease: "steps(1)" })
        
        .to("#scr1", { opacity: 1, scale: 1.2, duration: 0.1 }, "-=0.2")
        .to("#scr2", { opacity: 1, x: 50, duration: 0.1 }, "+=0.2")
        .to("#tape1", { opacity: 1, duration: 0.1 })
        
        .to("#scene-mag", { opacity: 0, duration: 0.1, delay: 0.5 })

        // 5.0 - 7.5s: Torn Cards (Stacking over each other aggressively)
        .set("#scene-torn", { display: "block" })
        .to("#bg-t2", { opacity: 0, duration: 0.1 }) // clear bg text
        
        .fromTo(".c1", { y: -1000, opacity: 0 }, { y: 0, opacity: 1, duration: 0.2, ease: "power4.inOut" })
        .to(".c1", { transform: "rotate(3deg) scale(1.05)", duration: 0.1, yoyo: true, repeat: 1 })
        
        .fromTo(".c2", { x: 1000, opacity: 0 }, { x: 0, opacity: 1, duration: 0.2, ease: "power4.inOut" }, "+=0.2")
        .fromTo(".c3", { y: 1000, opacity: 0 }, { y: 0, opacity: 1, duration: 0.2, ease: "back.out(1.5)" }, "+=0.2")
        
        .to("#scene-torn", { rotateZ: -90, scale: 2, opacity: 0, duration: 0.4, ease: "expo.in", delay: 0.5 })
        
        // 7.5 - 10.0s: The Outro Punch
        .set("#scene-outro", { display: "block" })
        
        // Slam container down
        .fromTo(".outro-container", 
            { scale: 5, rotateZ: 45, opacity: 0 },
            { scale: 1, rotateZ: -2, opacity: 1, duration: 0.3, ease: "steps(4)" }
        )
        .to("#tape2", { opacity: 1, duration: 0.1 })
        .to("#tape3", { opacity: 1, duration: 0.1 }, "+=0.2")
        
        // Chaotic screen jitter before death
        .to("body", { x: "random(-20, 20)", y: "random(-20, 20)", duration: 0.05, yoyo: true, repeat: 10, delay: 0.5 })
        
        // Hard cut to black at 9.7s
        .to("body", { backgroundColor: "#1c1b18", duration: 0.1, delay: 0.1 })
        .to(".outro-container, .tape", { opacity: 0, duration: 0.1 }, "-=0.1");

    </script>
</body>
</html>"""
    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Carson Grunge 10s Promo (9x16) generated: {output_path}")

if __name__ == "__main__":
    generate_carson_cinematic()
