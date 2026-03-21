import os
from pathlib import Path

def generate_pure_hero():
    print("🎬 Initializing NEXUS Motion Engine [PURE HERO MODULE]...")
    
    project_root = Path("e:/Downloads/--ANTIGRAVITY store/IDE-optimus")
    output_path = project_root / "PROJECT" / "outputs" / "Legal_DevOps_Pure_Hero.html"
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXUS | Pure Hero</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #050508;
            --accent: #00f2ff;
            --accent-dim: rgba(0, 242, 255, 0.15);
            --text-main: #ffffff;
            --text-dim: #8b9bb4;
            --danger: #cc0000;
        }
        * { box-sizing: border-box; cursor: none; }
        
        /* STRICT HERO CONTAINER: Fix to exactly 100vh and block scrolling */
        body { 
            margin: 0; padding: 0; background: var(--bg); color: var(--text-main); 
            font-family: 'Inter', sans-serif; overflow: hidden; /* NO SCROLL */
            height: 100vh; width: 100vw;
        }
        
        .cursor-dot, .cursor-outline {
            position: fixed; top: 0; left: 0; transform: translate(-50%, -50%);
            border-radius: 50%; z-index: 9999; pointer-events: none;
        }
        .cursor-dot { width: 6px; height: 6px; background-color: var(--accent); box-shadow: 0 0 10px var(--accent); }
        .cursor-outline {
            width: 40px; height: 40px; border: 1px solid var(--accent-dim);
            transition: width 0.2s, height 0.2s, background-color 0.2s;
        }

        #webgl-container {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            z-index: -2; opacity: 0.4; pointer-events: none;
        }
        
        .grid-overlay {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-image: 
                linear-gradient(to right, rgba(255,255,255,0.02) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(255,255,255,0.02) 1px, transparent 1px);
            background-size: 40px 40px; z-index: -1; pointer-events: none;
            mask-image: radial-gradient(ellipse at center, black 40%, transparent 80%);
            -webkit-mask-image: radial-gradient(ellipse at center, black 40%, transparent 80%);
        }

        .nav-bar {
            position: fixed; top: 0; width: 100%; padding: 2rem 4rem;
            display: flex; justify-content: space-between; align-items: center;
            z-index: 100; border-bottom: 1px solid rgba(255,255,255,0.05);
            background: rgba(5,5,8,0.3); backdrop-filter: blur(10px);
        }
        .logo { font-family: 'Syncopate', sans-serif; font-weight: 700; font-size: 1.2rem; letter-spacing: 4px; display: flex; align-items: center;}
        .logo span { color: var(--accent); margin-left: 10px; font-size: 0.8rem; border: 1px solid var(--accent); padding: 2px 6px; border-radius: 2px;}
        .status-indicator { display: flex; align-items: center; font-size: 0.7rem; letter-spacing: 2px; text-transform: uppercase; color: var(--accent); }
        .pulse { width: 6px; height: 6px; background: var(--accent); border-radius: 50%; margin-right: 10px; box-shadow: 0 0 10px var(--accent); animation: pulse 2s infinite; }
        @keyframes pulse { 0% { opacity: 0.5; box-shadow: 0 0 5px var(--accent); } 50% { opacity: 1; box-shadow: 0 0 15px var(--accent); } 100% { opacity: 0.5; box-shadow: 0 0 5px var(--accent); } }

        .section {
            height: 100vh; display: flex; flex-direction: column;
            align-items: center; justify-content: center; position: relative;
        }
        
        .hero-layout {
            display: grid; grid-template-columns: 1fr 1fr; max-width: 1400px; width: 100%; padding: 0 4rem; gap: 4rem; align-items: center;
        }

        .hero-left { text-align: left; }
        .tagline { font-family: 'Syncopate', sans-serif; font-size: 0.8rem; color: var(--accent); letter-spacing: 4px; margin-bottom: 2rem; display: block; opacity: 0; transform: translateY(20px); }
        
        .reveal-wrapper { display: inline-block; overflow: hidden; clip-path: polygon(0 0, 100% 0, 100% 100%, 0% 100%); line-height: 1.1; }
        .hero-title {
            font-family: 'Syncopate', sans-serif; font-size: 6vw; font-weight: 700; 
            margin: 0; text-transform: uppercase; letter-spacing: -2px;
        }
        .text-outline { color: transparent; -webkit-text-stroke: 1px rgba(255,255,255,0.4); }
        
        .hero-desc {
            color: var(--text-dim); font-size: 1.1rem; font-weight: 300;
            margin-top: 2rem; max-width: 500px; line-height: 1.8; opacity: 0; border-left: 2px solid var(--accent); padding-left: 1.5rem;
        }
        
        .hero-desc strong { color: var(--text-main); font-weight: 400; }

        .action-group { margin-top: 3rem; display: flex; gap: 1.5rem; opacity: 0; transform: translateY(20px); }
        
        .btn-primary {
            padding: 1rem 2rem; background: var(--accent); color: var(--bg);
            font-family: 'Syncopate', sans-serif; font-size: 0.8rem; font-weight: 700; letter-spacing: 2px;
            border: none; text-transform: uppercase; position: relative; overflow: hidden;
            box-shadow: 0 0 20px rgba(0,242,255,0.3); transition: 0.3s;
        }
        .btn-primary:hover { box-shadow: 0 0 30px rgba(0,242,255,0.6); transform: translateY(-2px); }
        
        .btn-secondary {
            padding: 1rem 2rem; background: transparent; color: var(--text-main);
            font-family: 'Syncopate', sans-serif; font-size: 0.8rem; font-weight: 700; letter-spacing: 2px;
            border: 1px solid rgba(255,255,255,0.2); text-transform: uppercase; transition: 0.3s;
        }
        .btn-secondary:hover { border-color: var(--text-main); background: rgba(255,255,255,0.05); }

        .hero-right { position: relative; height: 500px; perspective: 1000px; }
        .data-card {
            background: rgba(20,20,25,0.6); border: 1px solid rgba(255,255,255,0.05);
            padding: 2rem; border-radius: 8px; backdrop-filter: blur(20px);
            position: absolute; width: 350px; box-shadow: 0 20px 40px rgba(0,0,0,0.5);
            transform-style: preserve-3d; opacity: 0;
        }
        .card-1 { top: 10%; right: 10%; z-index: 2; border-top: 2px solid var(--accent); }
        .card-2 { bottom: 10%; left: 0; z-index: 1; border-top: 2px solid var(--danger); }

        .data-row { display: flex; justify-content: space-between; margin-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 0.5rem; }
        .data-label { color: var(--text-dim); font-size: 0.8rem; font-family: 'Syncopate'; letter-spacing: 1px;}
        .data-value { color: var(--text-main); font-family: monospace; font-size: 0.9rem;}
        .data-value.active { color: var(--accent); }

    </style>
</head>
<body>
    <div class="cursor-dot" id="cursor-dot"></div>
    <div class="cursor-outline" id="cursor-outline"></div>

    <div id="webgl-container"></div>
    <div class="grid-overlay"></div>

    <nav class="nav-bar">
        <div class="logo">NEXUS <span>MAS</span></div>
        <div class="status-indicator hover-target">
            <div class="pulse"></div> SYSTEM ACTIVE
        </div>
    </nav>

    <div class="section" id="hero">
        <div class="hero-layout">
            <div class="hero-left">
                <span class="tagline">v2026.1 // SYSTEM INITIALIZED</span>
                
                <div class="reveal-wrapper"><h1 class="reveal-text hero-text">Legal</h1></div><br>
                <div class="reveal-wrapper"><h1 class="reveal-text text-outline hero-text">DevOps</h1></div>
                
                <p class="hero-desc">
                    What is this? A specialized high-tech framework that transforms <strong>legal representation</strong> into a precise engineering process. <br><br>We replace chaotic paperwork with a robust, automated <strong>Multi-Agent System (MAS)</strong>.
                </p>
                
                <div class="action-group">
                    <button class="btn-primary hover-target">Initialize MAS</button>
                    <button class="btn-secondary hover-target">View Docs</button>
                </div>
            </div>
            
            <div class="hero-right">
                <div class="data-card card-1 card-float">
                    <div class="data-row"><span class="data-label">AGENT</span><span class="data-value active">NEXUS-PRIME</span></div>
                    <div class="data-row"><span class="data-label">MODE</span><span class="data-value">AUTONOMOUS</span></div>
                    <div class="data-row"><span class="data-label">LEGAL RAM</span><span class="data-value">128 TB</span></div>
                    <div class="data-row" style="border:none;"><span class="data-label">STATUS</span><span class="data-value">PROCESSING</span></div>
                </div>
                
                <div class="data-card card-2 card-float-delayed">
                    <div class="data-row"><span class="data-label">CHAOS LEVEL</span><span class="data-value" style="color:var(--danger)">DETECTED</span></div>
                    <div class="data-row"><span class="data-label">PAPERWORK</span><span class="data-value">PURGING</span></div>
                    <div class="data-row" style="border:none;"><span class="data-label">EFFICIENCY</span><span class="data-value active">+940%</span></div>
                </div>
            </div>
        </div>
    </div>

    <!-- Removed scroll spacers and Lenis logic completely -->

    <script>
        // 1. Cursor Engine
        const cursorDot = document.getElementById('cursor-dot');
        const cursorOutline = document.getElementById('cursor-outline');
        const hoverTargets = document.querySelectorAll('.hover-target, button');

        window.addEventListener('mousemove', (e) => {
            const posX = e.clientX;
            const posY = e.clientY;
            cursorDot.style.left = `${posX}px`;
            cursorDot.style.top = `${posY}px`;
            cursorOutline.animate({ left: `${posX}px`, top: `${posY}px` }, { duration: 100, fill: "forwards" });
        });

        hoverTargets.forEach(target => {
            target.addEventListener('mouseenter', () => {
                cursorOutline.style.width = '50px'; cursorOutline.style.height = '50px';
                cursorOutline.style.backgroundColor = 'rgba(0, 242, 255, 0.1)';
                cursorOutline.style.borderColor = 'rgba(0, 242, 255, 0.5)';
            });
            target.addEventListener('mouseleave', () => {
                cursorOutline.style.width = '40px'; cursorOutline.style.height = '40px';
                cursorOutline.style.backgroundColor = 'transparent';
                cursorOutline.style.borderColor = 'var(--accent-dim)';
            });
        });

        // 2. WebGL Cyberpunk Data Particles (Three.js)
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.getElementById('webgl-container').appendChild(renderer.domElement);

        const particleCount = 1000;
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        
        for(let i=0; i < particleCount * 3; i+=3) {
            positions[i] = (Math.random() - 0.5) * 40; 
            positions[i+1] = (Math.random() - 0.5) * 40; 
            positions[i+2] = (Math.random() - 0.5) * 20 - 10; 
        }
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        
        const material = new THREE.PointsMaterial({ size: 0.05, color: 0x00f2ff, transparent: true, opacity: 0.6 });
        const particles = new THREE.Points(geometry, material);
        scene.add(particles);
        camera.position.z = 5;

        let mouseX = 0; let mouseY = 0;
        window.addEventListener('mousemove', (e) => {
            mouseX = (e.clientX / window.innerWidth) * 2 - 1;
            mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
        });

        function animateWebGL() {
            requestAnimationFrame(animateWebGL);
            particles.rotation.y += 0.0005;
            particles.rotation.x += 0.0002;
            
            camera.position.x += (mouseX * 2 - camera.position.x) * 0.05;
            camera.position.y += (mouseY * 2 - camera.position.y) * 0.05;
            camera.lookAt(scene.position);
            renderer.render(scene, camera);
        }
        animateWebGL();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

        // 3. GSAP Timelines (Pure Entrance, No ScrollTrigger needed)
        
        const tl = gsap.timeline();
        tl.to(".tagline", { opacity: 1, y: 0, duration: 1, ease: "power4.out", delay: 0.2 })
          .from(".hero-text", { y: 150, duration: 1.2, ease: "power4.out", stagger: 0.15 }, "-=0.8")
          .to(".hero-desc", { opacity: 1, duration: 1.5, ease: "power2.out" }, "-=0.6")
          .to(".action-group", { opacity: 1, y: 0, duration: 1, ease: "power4.out" }, "-=1.2")
          .to(".card-1", { opacity: 1, y: -20, rotationY: -15, rotationX: 10, duration: 1.5, ease: "power3.out" }, "-=1")
          .to(".card-2", { opacity: 1, y: 20, rotationY: 15, rotationX: -10, duration: 1.5, ease: "power3.out" }, "-=1.2");

        // 3D Card Hover Float Effect
        document.addEventListener("mousemove", (e) => {
            const x = (window.innerWidth / 2 - e.pageX) / 50;
            const y = (window.innerHeight / 2 - e.pageY) / 50;
            
            gsap.to(".card-1", { rotationY: -15 + x, rotationX: 10 + y, ease: "power1.out", duration: 1 });
            gsap.to(".card-2", { rotationY: 15 + x, rotationX: -10 + y, ease: "power1.out", duration: 1 });
        });

    </script>
</body>
</html>"""
    
    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"✅ Pure Legal DevOps Hero generated: {output_path}")

if __name__ == "__main__":
    generate_pure_hero()
