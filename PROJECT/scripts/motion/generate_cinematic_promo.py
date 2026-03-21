import os
from pathlib import Path

def generate_desktop_cinematic():
    print("🎬 NEXUS V4 Engine: 10-Second Hyper-Cinematic [16:9]...")
    
    project_root = Path("e:/Downloads/--ANTIGRAVITY store/IDE-optimus")
    output_path = project_root / "PROJECT" / "outputs" / "Cinematic_Promo_16x9.html"
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1920, height=1080, initial-scale=1.0">
    <title>NEXUS | Desktop Cinematic Video 10s</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        :root { --bg: #020202; --accent: #ff003c; --accent-alt: #00f2ff; --glow: #ff003c66; }
        * { box-sizing: border-box; cursor: none !important; }
        body, html { margin: 0; padding: 0; width: 1920px; height: 1080px; background: var(--bg); overflow: hidden; font-family: 'Space Mono', monospace; color: #fff; display: flex; align-items: center; justify-content: center; }

        .crt-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 100;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.1) 50%); background-size: 100% 6px; pointer-events: none; opacity: 0.5; }
        
        #webgl-bg { position: absolute; top:0; left:0; width: 100%; height: 100%; z-index: 1; opacity: 0; filter: contrast(1.5); }
        .scene { position: absolute; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 10; }
        
        /* Scene 1: Boot */
        #scene-boot { text-align: left; width: 80%; align-items: flex-start; padding-left: 10%; }
        .boot-line { font-size: 2.5rem; color: var(--accent-alt); margin-bottom: 20px; opacity: 0; width: 100%; font-weight: 700; }
        .glitch-flash { width: 100%; height: 100%; background: #fff; opacity: 0; mix-blend-mode: overlay; position: absolute; z-index: 90; }

        /* Scene 2: Hyper Slam */
        #scene-slam { perspective: 2000px; display: none; }
        .slam-text { font-family: 'Syncopate', sans-serif; font-size: 16rem; font-weight: 700; text-transform: uppercase; line-height: 0.8; text-align: center; transform-style: preserve-3d; margin: 0; }
        .slam-text span { display: block; opacity: 0; }
        .text-outline { color: transparent; -webkit-text-stroke: 6px var(--accent); }
        .text-solid { color: #fff; text-shadow: 0 0 100px var(--glow); margin-top: 1rem;}

        /* Scene 3: Glitch Cards */
        #scene-scan { display: none; width: 1920px; height: 1080px; flex-direction: row; align-items: center; justify-content: center; gap: 50px;}
        .data-card { width: 30%; border: 4px solid var(--accent-alt); padding: 4rem 2rem; opacity: 0; background: rgba(0,242,255,0.05); backdrop-filter: blur(10px); text-align: center;}
        .dc-title { font-family: 'Syncopate', sans-serif; font-size: 2.5rem; color: var(--accent-alt); margin: 0 0 1rem 0; }
        .dc-val { font-size: 6rem; font-family: 'Space Mono'; font-weight: bold; margin: 0; }

        /* Scene 4: Minimal Logo */
        #scene-final { display: none; }
        .logo-box { padding: 4rem 8rem; border: 8px solid #fff; opacity: 0; text-align: center; position: relative;}
        .logo-text { font-family: 'Syncopate', sans-serif; font-size: 10rem; font-weight: 700; margin:0; letter-spacing: 20px;}
        .logo-sub { color: var(--accent); font-size: 3rem; letter-spacing: 15px; margin-top: 2rem;}
        
        .barcode { width: 100%; height: 60px; background: repeating-linear-gradient(90deg, #fff, #fff 5px, transparent 5px, transparent 15px, #fff 15px, #fff 25px, transparent 25px, transparent 40px); margin-top: 3rem; opacity: 0.5;}

    </style>
</head>
<body>
    <div class="crt-overlay"></div>
    <div class="glitch-flash" id="flash"></div>
    <div id="webgl-bg"></div>

    <div class="scene" id="scene-boot">
        <div class="boot-line">&gt; SYSTEM PURGE... [OK]</div>
        <div class="boot-line">&gt; INJECTING LEGAL_DEVOPS</div>
        <div class="boot-line">&gt; OVERRIDE: TRUE</div>
        <div class="boot-line" style="color:var(--accent); font-size: 3.5rem;">&gt; EXECUTE.</div>
    </div>

    <div class="scene" id="scene-slam">
        <h1 class="slam-text">
            <span class="text-outline line1">LEGAL</span>
            <span class="text-solid line2">DEVOPS</span>
        </h1>
    </div>

    <div class="scene" id="scene-scan">
        <div class="data-card dc1" style="transform: rotate(-3deg); border-color: var(--accent);"><h2 class="dc-title" style="color:var(--accent)">ERRORS</h2><p class="dc-val">0.00%</p></div>
        <div class="data-card dc2" style="transform: rotate(2deg);"><h2 class="dc-title">SPEED</h2><p class="dc-val">1200X</p></div>
        <div class="data-card dc3" style="transform: rotate(-1deg); border-color: #fff;"><h2 class="dc-title" style="color:#fff">AGENTS</h2><p class="dc-val" style="color:var(--accent)">ACTIVE</p></div>
    </div>

    <div class="scene" id="scene-final">
        <div class="logo-box">
            <h1 class="logo-text">NEXUS</h1>
            <div class="logo-sub">MAS ENGINE</div>
            <div class="barcode"></div>
        </div>
    </div>

    <script>
        // WebGL High-Speed Tunnel
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(90, 1920 / 1080, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(1920, 1080);
        document.getElementById('webgl-bg').appendChild(renderer.domElement);

        const group = new THREE.Group();
        for(let i=0; i<3; i++) {
            const grid = new THREE.GridHelper(200, 40, 0xff003c, 0x111111);
            grid.position.y = -30;
            grid.position.z = -i * 100;
            const gridTop = new THREE.GridHelper(200, 40, 0x00f2ff, 0x111111);
            gridTop.position.y = 30;
            gridTop.position.z = -i * 100;
            group.add(grid); group.add(gridTop);
        }
        scene.add(group);
        camera.position.z = 10;
        
        let speed = 1.0;

        function animateWebGL() {
            requestAnimationFrame(animateWebGL);
            group.position.z += speed;
            if(group.position.z > 100) group.position.z = 0;
            
            // Random camera shake on high speed
            if(speed > 5) {
                camera.position.x = (Math.random() - 0.5) * 4;
                camera.position.y = (Math.random() - 0.5) * 4;
            } else {
                camera.position.x = 0; camera.position.y = 0;
            }
            renderer.render(scene, camera);
        }
        animateWebGL();

        // 10-SECOND HYPER TIMELINE
        const tl = gsap.timeline();

        // 0.0 - 1.5s: Boot Sequence
        tl.to(".boot-line", { opacity: 1, duration: 0.1, stagger: 0.15, ease: "steps(1)" })
          .to("#flash", { opacity: 0.9, duration: 0.05, yoyo: true, repeat: 5 }, "-=0.2")
          .set("#scene-boot", { display: "none" })
          .set("#scene-slam", { display: "flex" })
          .to("#webgl-bg", { opacity: 1, duration: 0.1 })
          .add(() => speed = 8.0) // Warp speed!

        // 1.5 - 4.0s: The Slam with Chaos
          .fromTo(".line1", { z: -1500, opacity: 0, rotateY: 90 }, { z: 0, opacity: 1, rotateY: 0, duration: 0.8, ease: "back.out(2)" })
          .fromTo(".line2", { z: 1500, opacity: 0, rotateX: -90 }, { z: 0, opacity: 1, rotateX: 0, duration: 0.6, ease: "back.out(2)" }, "-=0.5")
          
          .to(".slam-text", { scale: 1.05, duration: 0.05, yoyo: true, repeat: 7 }, "+=0.2")
          .to(".line1", { x: -30, duration: 0.02, yoyo: true, repeat: 10 }, "-=0.2") // Glitch shake
          .to(".slam-text", { z: 1000, opacity: 0, duration: 0.5, ease: "power4.in", delay: 0.5 })
          .set("#scene-slam", { display: "none" })
          .add(() => speed = 1.0) // Normal speed

        // 4.0 - 7.0s: Feature Cards Sequence
          .set("#scene-scan", { display: "flex" })
          
          .fromTo(".dc1", { scale: 2, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.2, ease: "power4.out" })
          .to("#flash", { opacity: 0.8, duration: 0.05, yoyo: true, repeat: 1 })
          
          .fromTo(".dc2", { scale: 1.5, opacity: 0, y: 100 }, { scale: 1, opacity: 1, y: 0, duration: 0.2, ease: "power4.out", delay: 0.5 })
          .to("#flash", { opacity: 0.8, duration: 0.05, yoyo: true, repeat: 1 })
          
          .fromTo(".dc3", { scale: 0.5, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.2, ease: "elastic.out(1, 0.5)", delay: 0.5 })
          
          .to(".dc1, .dc2, .dc3", { scale: 0, opacity: 0, duration: 0.4, stagger: 0.1, ease: "back.in(2)", delay: 0.5 })
          .set("#scene-scan", { display: "none" })

        // 7.0 - 10.0s: Final Logo
          .set("#scene-final", { display: "flex" })
          .to("#webgl-bg", { opacity: 0.3, duration: 0.5 })
          .fromTo(".logo-box", { scale: 0.5, opacity: 0 }, { scale: 1, opacity: 1, duration: 1.2, ease: "expo.out" })
          .fromTo(".logo-sub", { letterSpacing: "50px", opacity: 0 }, { letterSpacing: "15px", opacity: 1, duration: 0.8, ease: "power3.out" }, "-=0.8")
          .fromTo(".barcode", { opacity: 0 }, { opacity: 0.5, duration: 0.5 }, "-=0.5")
          
          // Glitch Logo
          .to(".logo-box", { x: 10, duration: 0.02, yoyo: true, repeat: 5, delay: 0.4 })

          // Final fade to black at 9.5s
          .to("body", { backgroundColor: "#000", duration: 0.5, delay: 1 })
          .to("#scene-final, #webgl-bg, .crt-overlay", { opacity: 0, duration: 0.5 }, "-=0.5");

    </script>
</body>
</html>"""
    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ V4 10-Second Cinematic Promo 16x9 generated: {output_path}")

if __name__ == "__main__":
    generate_desktop_cinematic()
