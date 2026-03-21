import os
from pathlib import Path

def generate_manifesto_premium():
    print("💎 NEXUS Premium Engine: Upgrading Manifesto to Elite Standards...")
    
    project_root = Path("e:/Downloads/--ANTIGRAVITY store/IDE-optimus")
    output_path = project_root / "PROJECT" / "outputs" / "Cinematic_Manifesto_9x16_PREMIUM.html"

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1080, height=1920, initial-scale=1.0">
    <title>NEXUS | Premium Manifesto</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;700&family=Syncopate:wght@400;700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --bg: #000B18; /* Deep Navy */
            --accent: #D4AF37; /* Gold */
            --tech: #00f2ff;
            --text-main: #f0f4f8;
            --text-dim: #64748b;
        }

        * { box-sizing: border-box; cursor: none !important; }
        
        body, html { 
            margin: 0; padding: 0; width: 1080px; height: 1920px; 
            background-color: var(--bg); overflow: hidden; 
            font-family: 'Outfit', sans-serif; color: var(--text-main);
        }

        #webgl-canvas { position: absolute; top:0; left:0; width: 100%; height: 100%; z-index: 0; }

        .scene { 
            position: absolute; width: 100%; height: 100%; z-index: 10; 
            display: flex; flex-direction: column; justify-content: center; 
            padding: 100px;
        }

        /* Scene 1: Title */
        #s1 { align-items: center; }
        .s1-text { font-family: 'Syncopate', sans-serif; font-size: 13rem; font-weight: 700; margin: 0; line-height: 0.9; text-transform: uppercase; text-align: center;}
        .word-legal { color: transparent; -webkit-text-stroke: 4px var(--accent); opacity: 0.8; }
        .word-devops { color: #fff; text-shadow: 0 0 50px rgba(212, 175, 55, 0.4); margin-top: 1rem; }

        /* Generic Manifesto Styling */
        .question-header { 
            font-family: 'Syncopate', sans-serif; font-size: 5rem; color: var(--accent); 
            border-left: 10px solid var(--accent); padding-left: 2rem; margin-bottom: 4rem;
            width: fit-content; text-transform: uppercase;
        }

        .manifesto-block { font-size: 4.5rem; line-height: 1.3; font-weight: 300; letter-spacing: -2px;}
        .line-wrapper { overflow: hidden; margin-bottom: 12px; }
        .m-line { display: block; opacity: 0; transform: translateY(100%); }
        .highlight { font-weight: 700; color: var(--accent); text-shadow: 0 0 30px rgba(212, 175, 55, 0.3); }

        #s2, #s3, #s4 { display: none; }

        /* Scene 4: Logo */
        #s4 { align-items: center; text-align: center; }
        .logo-box { padding: 4rem 6rem; background: rgba(255,255,255,0.05); backdrop-filter: blur(20px); border: 2px solid var(--accent); position: relative;}
        .logo-text { font-family: 'Syncopate', sans-serif; font-size: 9.5rem; font-weight: 700; margin:0; letter-spacing: 25px; color: var(--accent);}
        .logo-sub { color: #fff; font-size: 2.5rem; letter-spacing: 15px; margin-top: 2rem; opacity: 0.6;}

        /* HUD */
        .hud { position: absolute; z-index: 100; font-family: monospace; font-size: 1.2rem; color: var(--accent); opacity: 0.4; }
    </style>
</head>
<body>
    <div id="webgl-canvas"></div>
    
    <div class="hud" style="top:50px; left:50px;">NEXUS_SYSTEM_STATUS: OPTIMAL</div>
    <div class="hud" style="top:50px; right:50px;">UI_VERSION: 2.0_PREMIUM</div>
    <div class="hud" style="bottom:50px; left:50px;">COORD: 50.4501, 30.5234</div>

    <!-- S1 -->
    <div class="scene" id="s1">
        <h1 class="s1-text word-legal">LEGAL</h1>
        <h1 class="s1-text word-devops">DEVOPS</h1>
    </div>

    <!-- S2 -->
    <div class="scene" id="s2">
        <div class="question-header">WHAT IS THIS?</div>
        <div class="manifesto-block">
            <div class="line-wrapper"><span class="m-line l2">A <span class="highlight">High-Tier Framework</span></span></div>
            <div class="line-wrapper"><span class="m-line l2">that transforms litigation</span></div>
            <div class="line-wrapper"><span class="m-line l2">into precise engineering.</span></div>
        </div>
    </div>

    <!-- S4 -->
    <div class="scene" id="s4">
        <div class="logo-box">
            <h1 class="logo-text">NEXUS</h1>
            <div class="logo-sub">PREMIUM OS</div>
        </div>
    </div>

    <script id="vshader" type="x-shader/x-vertex">
        varying vec2 vUv;
        void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    </script>
    <script id="fshader" type="x-shader/x-fragment">
        varying vec2 vUv;
        uniform float u_time;
        void main() {
            vec2 uv = vUv;
            vec3 color = vec3(0.003, 0.04, 0.1); // Deep Navy Base
            
            float grid = sin(uv.x * 40.0 + u_time) * cos(uv.y * 40.0 + u_time);
            grid = smoothstep(0.95, 0.98, grid);
            
            color += grid * vec3(0.83, 0.68, 0.21) * 0.4; // Gold highlights
            gl_FragColor = vec4(color, 0.8);
        }
    </script>

    <script>
        // PREMIUM SHADER BACKGROUND
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, 1080/1920, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(1080, 1920);
        document.getElementById('webgl-canvas').appendChild(renderer.domElement);

        const geometry = new THREE.PlaneGeometry(30, 60);
        const material = new THREE.ShaderMaterial({
            vertexShader: document.getElementById('vshader').textContent,
            fragmentShader: document.getElementById('fshader').textContent,
            uniforms: { u_time: { value: 0 } }
        });
        const mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);
        camera.position.z = 10;

        function animate(t) {
            requestAnimationFrame(animate);
            material.uniforms.u_time.value = t * 0.001;
            renderer.render(scene, camera);
        }
        animate(0);

        // TIMELINE
        const tl = gsap.timeline();
        tl.fromTo(".word-legal", { y: 100, opacity: 0 }, { y: 0, opacity: 0.8, duration: 1.5, ease: "expo.out" })
          .fromTo(".word-devops", { x: -100, opacity: 0 }, { x: 0, opacity: 1, duration: 1.5, ease: "expo.out" }, "-=1.2")
          .to(".scene", { opacity: 0, filter: "blur(20px)", duration: 1, delay: 1 })
          .set("#s1", { display: "none" })
          .set("#s2", { display: "flex", opacity: 1, filter: "blur(0px)" })
          .to(".l2", { y: 0, opacity: 1, duration: 1, stagger: 0.2, ease: "power4.out" })
          .to("#s2", { scale: 1.2, opacity: 0, filter: "blur(20px)", duration: 1, delay: 2 })
          .set("#s2", { display: "none" })
          .set("#s4", { display: "flex", opacity: 1, filter: "blur(0px)" })
          .fromTo(".logo-box", { rotateX: 90, opacity: 0 }, { rotateX: 0, opacity: 1, duration: 2, ease: "elastic.out(1, 0.5)" });

    </script>
</body>
</html>"""
    
    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"💎 PREMIUM Manifesto (9x16) generated: {output_path}")

if __name__ == "__main__":
    generate_manifesto_premium()
