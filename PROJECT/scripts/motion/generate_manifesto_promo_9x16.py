import os
from pathlib import Path

def generate_manifesto_cinematic():
    print("🎬 NEXUS Design Engine: Typography Manifesto [9:16]...")
    
    project_root = Path("e:/Downloads/--ANTIGRAVITY store/IDE-optimus")
    output_path = project_root / "PROJECT" / "outputs" / "Cinematic_Manifesto_9x16.html"

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1080, height=1920, initial-scale=1.0">
    <title>NEXUS | Manifesto Video Format</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&family=Syncopate:wght@400;700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --bg: #030408;
            --accent: #ff003c;
            --tech: #00f2ff;
            --text-main: #f0f4f8;
            --text-dim: #64748b;
        }

        * { box-sizing: border-box; cursor: none !important; }
        
        body, html { 
            margin: 0; padding: 0; width: 1080px; height: 1920px; 
            background-color: var(--bg); overflow: hidden; 
            font-family: 'Inter', sans-serif; color: var(--text-main);
        }

        /* Ambient Grid */
        .ambient-grid {
            position: absolute; width: 100vw; height: 100vh;
            background-image: 
                linear-gradient(rgba(255,255,255,0.03) 2px, transparent 2px),
                linear-gradient(90deg, rgba(255,255,255,0.03) 2px, transparent 2px);
            background-size: 80px 80px; z-index: 1; opacity: 0.5;
            mask-image: linear-gradient(to bottom, rgba(0,0,0,1) 30%, rgba(0,0,0,0) 100%);
            -webkit-mask-image: linear-gradient(to bottom, rgba(0,0,0,1) 30%, rgba(0,0,0,0) 100%);
        }

        #webgl-canvas { position: absolute; top:0; left:0; width: 100%; height: 100%; z-index: 0; opacity: 0.6; }

        .scene { 
            position: absolute; width: 100%; height: 100%; z-index: 10; 
            display: flex; flex-direction: column; justify-content: center; 
            padding: 100px;
        }

        /* Decor */
        .cross { position: absolute; width: 60px; height: 60px; opacity: 0.3; }
        .cross::before { content:''; position: absolute; width:100%; height:2px; background:var(--tech); top:29px; left:0; }
        .cross::after { content:''; position: absolute; height:100%; width:2px; background:var(--tech); left:29px; top:0; }

        /* Scene 1: Title */
        #s1 { align-items: center; }
        .s1-text { font-family: 'Syncopate', sans-serif; font-size: 13rem; font-weight: 700; margin: 0; line-height: 0.9; text-transform: uppercase; text-align: center;}
        .word-legal { color: transparent; -webkit-text-stroke: 4px var(--text-main); }
        .word-devops { color: var(--text-main); text-shadow: 0 0 50px rgba(0, 242, 255, 0.4); margin-top: 1rem; }

        /* Scene 2 & 3: Typography Manifesto */
        #s2, #s3 { display: none; padding-top: 15rem; justify-content: flex-start;}
        
        .question-header { 
            font-family: 'Syncopate', sans-serif; font-size: 5rem; color: var(--accent); 
            border-bottom: 4px solid var(--accent); padding-bottom: 2rem; margin-bottom: 4rem;
            width: fit-content; text-transform: uppercase;
        }

        .manifesto-block { font-size: 4rem; line-height: 1.4; font-weight: 300; }
        .line-wrapper { overflow: hidden; margin-bottom: 10px; }
        .m-line { display: block; opacity: 0; transform: translateY(100%); }
        .highlight { font-weight: 700; color: #fff; text-shadow: 0 0 30px rgba(255,255,255,0.4); }
        .highlight-cyan { font-weight: 700; color: var(--tech); text-shadow: 0 0 30px rgba(0,242,255,0.4); }

        /* Scene 4: Logo */
        #s4 { display: none; align-items: center; text-align: center; }
        .logo-box { padding: 4rem 6rem; border: 8px solid #fff; position: relative;}
        .logo-text { font-family: 'Syncopate', sans-serif; font-size: 9rem; font-weight: 700; margin:0; letter-spacing: 20px;}
        .logo-sub { color: var(--tech); font-size: 2.5rem; letter-spacing: 15px; margin-top: 2rem;}

    </style>
</head>
<body>
    <div class="ambient-grid"></div>
    <div id="webgl-canvas"></div>
    
    <div class="cross" style="top:80px; left:80px;"></div>
    <div class="cross" style="bottom:80px; right:80px;"></div>

    <!-- S1 -->
    <div class="scene" id="s1">
        <h1 class="s1-text word-legal">LEGAL</h1>
        <h1 class="s1-text word-devops">DEVOPS</h1>
    </div>

    <!-- S2 -->
    <div class="scene" id="s2">
        <div class="question-header">WHAT IS THIS?</div>
        <div class="manifesto-block">
            <div class="line-wrapper"><span class="m-line l2">A specialized high-tech framework</span></div>
            <div class="line-wrapper"><span class="m-line l2">that transforms legal representation</span></div>
            <div class="line-wrapper"><span class="m-line l2">into a precise engineering process.</span></div>
            
            <div class="line-wrapper" style="margin-top: 3rem;"><span class="m-line l2">We replace chaotic paperwork</span></div>
            <div class="line-wrapper"><span class="m-line l2">with a robust, automated</span></div>
            <div class="line-wrapper"><span class="m-line l2 highlight-cyan">Multi-Agent System (MAS).</span></div>
        </div>
    </div>

    <!-- S3 -->
    <div class="scene" id="s3">
        <div class="question-header">WHY DO WE NEED IT?</div>
        <div class="manifesto-block">
            <div class="line-wrapper"><span class="m-line l3">To manage dozens of active cases</span></div>
            <div class="line-wrapper"><span class="m-line l3">simultaneously without expanding</span></div>
            <div class="line-wrapper"><span class="m-line l3">headcount.</span></div>
            
            <div class="line-wrapper" style="margin-top: 3rem;"><span class="m-line l3">To strictly enforce accountability</span></div>
            <div class="line-wrapper"><span class="m-line l3">using <span class="highlight">relentless, algorithmic</span></span></div>
            <div class="line-wrapper"><span class="m-line l3 highlight">pressure</span> that never sleeps.</div>
        </div>
    </div>

    <!-- S4 -->
    <div class="scene" id="s4">
        <div class="logo-box">
            <h1 class="logo-text">NEXUS</h1>
            <div class="logo-sub">MAS ENGINE</div>
        </div>
    </div>

    <script>
        // Subtle Cyberpunk Data Particles
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, 1080/1920, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(1080, 1920);
        document.getElementById('webgl-canvas').appendChild(renderer.domElement);

        const particles = new THREE.BufferGeometry();
        const count = 400;
        const posArray = new Float32Array(count * 3);
        for(let i=0; i < count*3; i+=3) {
            posArray[i] = (Math.random() - 0.5) * 30; // x
            posArray[i+1] = (Math.random() - 0.5) * 40; // y
            posArray[i+2] = (Math.random() - 0.5) * 20 - 10; // z
        }
        particles.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
        const material = new THREE.PointsMaterial({ size: 0.1, color: 0x00f2ff, transparent: true, opacity: 0.5 });
        const particleMesh = new THREE.Points(particles, material);
        scene.add(particleMesh);
        camera.position.z = 15;

        function animateWebGL() {
            requestAnimationFrame(animateWebGL);
            particleMesh.rotation.y += 0.0005;
            particleMesh.rotation.x += 0.0002;
            renderer.render(scene, camera);
        }
        animateWebGL();

        // 18-SECOND MANIFESTO TIMELINE
        const tl = gsap.timeline();

        // [0.0s - 2.5s] Scene 1: LEGAL DEVOPS
        tl.fromTo(".word-legal", { y: -200, opacity: 0 }, { y: 0, opacity: 1, duration: 1, ease: "power4.out" })
          .fromTo(".word-devops", { y: 200, opacity: 0 }, { y: 0, opacity: 1, duration: 1, ease: "power4.out" }, "-=0.8")
          .to(".word-legal", { scale: 1.1, opacity: 0, duration: 0.5, ease: "power2.in", delay: 1 })
          .to(".word-devops", { scale: 1.1, opacity: 0, duration: 0.5, ease: "power2.in" }, "-=0.4")
          .set("#s1", { display: "none" })

        // [2.5s - 9.5s] Scene 2: WHAT IS THIS? (7 Seconds)
          .set("#s2", { display: "flex" })
          .fromTo(".question-header", { width: 0, opacity: 0 }, { width: "100%", opacity: 1, duration: 0.8, ease: "power4.out" })
          .to(".l2", { y: 0, opacity: 1, duration: 0.8, stagger: 0.15, ease: "power3.out" })
          
          .to("#s2", { y: -100, opacity: 0, duration: 0.5, ease: "power2.in", delay: 4.0 }) // read time
          .set("#s2", { display: "none" })

        // [9.5s - 15.5s] Scene 3: WHY DO WE NEED IT? (6 Seconds)
          .set("#s3", { display: "flex", y: 100 })
          .to("#s3", { y: 0, opacity: 1, duration: 0.5, ease: "power3.out" })
          .to(".l3", { y: 0, opacity: 1, duration: 0.8, stagger: 0.15, ease: "power3.out" })
          
          .to("#s3", { y: -100, opacity: 0, duration: 0.5, ease: "power2.in", delay: 3.0 }) // read time
          .set("#s3", { display: "none" })

        // [15.5s - 18.0s] Scene 4: FINAL LOGO (2.5 Seconds)
          .set("#s4", { display: "flex" })
          .fromTo(".logo-box", { scale: 0.8, opacity: 0 }, { scale: 1, opacity: 1, duration: 1, ease: "elastic.out(1, 0.4)" })
          .fromTo(".logo-sub", { letterSpacing: "50px", opacity: 0 }, { letterSpacing: "15px", opacity: 1, duration: 0.5, ease: "power4.out" }, "-=0.5")
          
          // Final fade
          .to("body, #webgl-canvas", { backgroundColor: "#020202", opacity: 0, duration: 0.5, delay: 0.5 });

    </script>
</body>
</html>"""
    
    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Manifesto Cinematic Promo (9x16) generated: {output_path}")

if __name__ == "__main__":
    generate_manifesto_cinematic()
