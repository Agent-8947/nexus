import os
import json
from pathlib import Path

def generate_motion_demo():
    print("🎬 Initializing NEXUS Motion Engine [ULTRA-PREMIUM TIER]...")
    
    project_root = Path("e:/Downloads/--ANTIGRAVITY store/IDE-optimus")
    output_path = project_root / "PROJECT" / "outputs" / "Motion_Premium_Showcase.html"
    
    # HTML template with embedded nexus-visual-motion patterns (GSAP + Three.js + Lenis)
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXUS | MOTION PREMIUM</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
    <script src="https://unpkg.com/lenis@1.0.45/dist/lenis.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #030303;
            --accent: #00ffed;
            --accent-dim: rgba(0, 255, 237, 0.2);
            --text-main: #ffffff;
            --text-dim: #8892b0;
        }
        * { box-sizing: border-box; cursor: none; }
        body { 
            margin: 0; padding: 0; background: var(--bg); color: var(--text-main); 
            font-family: 'Inter', sans-serif; overflow-x: hidden;
        }
        
        /* Custom Cursor */
        .cursor-dot, .cursor-outline {
            position: fixed; top: 0; left: 0; transform: translate(-50%, -50%);
            border-radius: 50%; z-index: 9999; pointer-events: none;
        }
        .cursor-dot { width: 8px; height: 8px; background-color: var(--accent); }
        .cursor-outline {
            width: 40px; height: 40px; border: 1px solid var(--accent-dim);
            transition: width 0.2s, height 0.2s, background-color 0.2s;
        }

        #webgl-container {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            z-index: -2; opacity: 0.6; pointer-events: none;
        }
        
        /* Grid Background Pattern */
        .grid-bg {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-image: 
                linear-gradient(to right, rgba(255,255,255,0.03) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(255,255,255,0.03) 1px, transparent 1px);
            background-size: 50px 50px; z-index: -1; pointer-events: none;
            mask-image: radial-gradient(circle at center, black 20%, transparent 80%);
            -webkit-mask-image: radial-gradient(circle at center, black 20%, transparent 80%);
        }

        .nav-bar {
            position: fixed; top: 0; width: 100%; padding: 2rem 4rem;
            display: flex; justify-content: space-between; align-items: center;
            z-index: 100; mix-blend-mode: difference;
        }
        .logo { font-family: 'Syncopate', sans-serif; font-weight: 700; font-size: 1.5rem; letter-spacing: 2px; }
        .nav-links span { margin-left: 2rem; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; }

        .section {
            height: 100vh; display: flex; flex-direction: column;
            align-items: center; justify-content: center; position: relative;
        }
        
        .hero-container { position: relative; text-align: center; }
        .reveal-wrapper { display: inline-block; overflow: hidden; clip-path: polygon(0 0, 100% 0, 100% 100%, 0% 100%); }
        .reveal-text {
            font-family: 'Syncopate', sans-serif; font-size: 9vw; font-weight: 700; 
            line-height: 0.9; margin: 0; text-transform: uppercase; letter-spacing: -2px;
        }
        .text-outline { color: transparent; -webkit-text-stroke: 1px rgba(255,255,255,0.2); }
        .text-accent { color: transparent; -webkit-text-stroke: 1px var(--accent); position: relative; }
        .text-accent::after {
            content: 'MOTION'; position: absolute; left: 0; top: 0;
            color: var(--accent); opacity: 0; filter: blur(10px);
            transition: opacity 0.5s;
        }
        .text-accent:hover::after { opacity: 0.5; }

        .sub-text {
            color: var(--text-dim); font-size: 1.2rem; font-weight: 300;
            margin-top: 2rem; max-width: 600px; text-align: center;
            line-height: 1.6; opacity: 0;
        }

        .magnetic-btn {
            margin-top: 3rem; padding: 1rem 3rem; border: 1px solid var(--accent);
            background: transparent; color: var(--accent); font-family: 'Syncopate', sans-serif;
            font-size: 0.9rem; letter-spacing: 2px; text-transform: uppercase;
            position: relative; overflow: hidden; transition: color 0.3s;
            display: inline-block; opacity: 0; transform: translateY(20px);
        }
        .btn-bg {
            position: absolute; top: 100%; left: 0; width: 100%; height: 100%;
            background: var(--accent); z-index: -1; transition: top 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .magnetic-btn:hover { color: var(--bg); }
        .magnetic-btn:hover .btn-bg { top: 0; }

        .scroll-indicator {
            position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%);
            display: flex; flex-direction: column; align-items: center; opacity: 0.5;
        }
        .scroll-text { font-size: 0.7rem; font-family: 'Syncopate'; letter-spacing: 4px; margin-bottom: 10px; }
        .scroll-line { width: 1px; height: 40px; background: linear-gradient(to bottom, var(--text-main) 50%, transparent 50%); background-size: 100% 200%; }

        /* Feature Section */
        .feature-grid {
            display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem;
            max-width: 1200px; padding: 0 2rem; w-full
        }
        .card {
            background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05);
            padding: 3rem 2rem; border-radius: 4px; position: relative; overflow: hidden;
            backdrop-filter: blur(10px);
        }
        .card::before {
            content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
            background: linear-gradient(to right, transparent, rgba(0, 255, 237, 0.1), transparent);
            transform: skewX(-20deg); transition: 0.5s;
        }
        .card:hover::before { left: 150%; }
        .card h3 { font-family: 'Syncopate', sans-serif; font-size: 1.5rem; margin-top: 0; margin-bottom: 1rem; }
        .card p { color: var(--text-dim); font-size: 0.95rem; line-height: 1.6; }
        .card .icon { color: var(--accent); font-size: 2rem; margin-bottom: 1.5rem; }

        .marquee-container {
            width: 100vw; overflow: hidden; white-space: nowrap; padding: 4rem 0;
            border-top: 1px solid rgba(255,255,255,0.1); border-bottom: 1px solid rgba(255,255,255,0.1);
            background: #000;
        }
        .marquee-content {
            display: inline-block; animation: marquee 20s linear infinite;
            font-family: 'Syncopate', sans-serif; font-size: 4vw; font-weight: 700;
            color: transparent; -webkit-text-stroke: 1px rgba(255,255,255,0.2);
        }
        @keyframes marquee { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
        .marquee-content span { margin: 0 2vw; }
        .marquee-content span.highlight { color: var(--text-main); -webkit-text-stroke: 0; }
    </style>
</head>
<body>
    <div class="cursor-dot" id="cursor-dot"></div>
    <div class="cursor-outline" id="cursor-outline"></div>

    <div id="webgl-container"></div>
    <div class="grid-bg"></div>

    <nav class="nav-bar">
        <div class="logo">NEXUS</div>
        <div class="nav-links">
            <span class="hover-target">Vision</span>
            <span class="hover-target">Architecture</span>
            <span class="hover-target">System</span>
        </div>
    </nav>

    <div class="section" id="hero">
        <div class="hero-container">
            <div class="reveal-wrapper"><h1 class="reveal-text text-outline hero-text">Cognitive</h1></div><br>
            <div class="reveal-wrapper"><h1 class="reveal-text hero-text">Architectural</h1></div><br>
            <div class="reveal-wrapper"><h1 class="reveal-text text-accent hero-text">Motion</h1></div>
            
            <p class="sub-text">Experience the convergence of rigorous functionalism and hyper-fluid digital art. Nexus V2026 rendering pipeline.</p>
            
            <div class="magnetic-btn hover-target">
                Initialize Sequence
                <div class="btn-bg"></div>
            </div>
        </div>
        
        <div class="scroll-indicator">
            <div class="scroll-text">SCROLL</div>
            <div class="scroll-line" id="scroll-line"></div>
        </div>
    </div>

    <div class="marquee-container" id="marquee-section">
        <div class="marquee-content">
            120FPS RENDERING <span>✦</span> <span class="highlight">ZERO LATENCY</span> <span>✦</span> 
            FLUID DYNAMICS <span>✦</span> <span class="highlight">GSAP MASTERY</span> <span>✦</span> 
            120FPS RENDERING <span>✦</span> <span class="highlight">ZERO LATENCY</span> <span>✦</span> 
            FLUID DYNAMICS <span>✦</span> <span class="highlight">GSAP MASTERY</span> <span>✦</span>
        </div>
    </div>

    <div class="section" id="features" style="height: 120vh;">
        <div style="text-align: center; margin-bottom: 5rem;">
            <div class="reveal-wrapper"><h2 class="reveal-text" style="font-size: 5vw; -webkit-text-stroke: 1px var(--accent); color: transparent;">Ecosystem</h2></div>
        </div>
        
        <div class="feature-grid">
            <div class="card card-reveal hover-target">
                <div class="icon">01</div>
                <h3>Kinetic Type</h3>
                <p>Advanced typography manipulation using GSAP timelines. Synchronized multi-layered text reveals that obey physical laws of inertia.</p>
            </div>
            <div class="card card-reveal hover-target">
                <div class="icon">02</div>
                <h3>WebGL Shaders</h3>
                <p>Custom GLSL fragment shaders injected directly into the DOM background, reacting to scroll momentum and pointer vectors.</p>
            </div>
            <div class="card card-reveal hover-target">
                <div class="icon">03</div>
                <h3>Liquid Layouts</h3>
                <p>Lenis virtual scroll integration providing a sub-pixel smooth experience, detached from native browser clunkiness.</p>
            </div>
        </div>
    </div>

    <script>
        // --- 1. Custom Cursor & Magnetic Effects ---
        const cursorDot = document.getElementById('cursor-dot');
        const cursorOutline = document.getElementById('cursor-outline');
        const hoverTargets = document.querySelectorAll('.hover-target, .magnetic-btn');

        window.addEventListener('mousemove', (e) => {
            const posX = e.clientX;
            const posY = e.clientY;

            cursorDot.style.left = `${posX}px`;
            cursorDot.style.top = `${posY}px`;

            // Adding slight delay to outline for smooth trailing effect
            cursorOutline.animate({
                left: `${posX}px`,
                top: `${posY}px`
            }, { duration: 150, fill: "forwards" });
        });

        hoverTargets.forEach(target => {
            target.addEventListener('mouseenter', () => {
                cursorOutline.style.width = '60px';
                cursorOutline.style.height = '60px';
                cursorOutline.style.backgroundColor = 'rgba(0, 255, 237, 0.1)';
            });
            target.addEventListener('mouseleave', () => {
                cursorOutline.style.width = '40px';
                cursorOutline.style.height = '40px';
                cursorOutline.style.backgroundColor = 'transparent';
            });
        });

        // Magnetic Button Logic
        const magnBtn = document.querySelector('.magnetic-btn');
        magnBtn.addEventListener('mousemove', (e) => {
            const rect = magnBtn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            gsap.to(magnBtn, { x: x * 0.4, y: y * 0.4, duration: 0.3, ease: 'power2.out' });
        });
        magnBtn.addEventListener('mouseleave', () => {
            gsap.to(magnBtn, { x: 0, y: 0, duration: 0.5, ease: 'elastic.out(1, 0.3)' });
        });

        // --- 2. Lenis Smooth Scroll Setup ---
        const lenis = new Lenis({
            duration: 1.2,
            easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
            direction: 'vertical',
            gestureDirection: 'vertical',
            smooth: true,
            mouseMultiplier: 1,
            smoothTouch: false,
            touchMultiplier: 2,
            infinite: false,
        });

        function raf(time) {
            lenis.raf(time);
            requestAnimationFrame(raf);
        }
        requestAnimationFrame(raf);

        // --- 3. Three.js Wireframe WebGL Background ---
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.getElementById('webgl-container').appendChild(renderer.domElement);

        // Creating a dynamic wireframe terrain
        const geometry = new THREE.PlaneGeometry(100, 100, 40, 40);
        const material = new THREE.MeshBasicMaterial({ 
            color: 0x00ffed, 
            wireframe: true,
            transparent: true,
            opacity: 0.05
        });
        
        // Displace vertices to make mountainous
        const vertices = geometry.attributes.position.array;
        for (let i = 0; i < vertices.length; i += 3) {
            vertices[i+2] = Math.random() * 2; // Z axis
        }
        
        const plane = new THREE.Mesh(geometry, material);
        plane.rotation.x = -Math.PI / 2; // Lay flat
        plane.position.y = -5;
        scene.add(plane);

        camera.position.z = 10;
        camera.position.y = 2;

        // Render Loop for WebGL
        const clock = new THREE.Clock();
        function animateWebGL() {
            requestAnimationFrame(animateWebGL);
            const time = clock.getElapsedTime();
            
            // Wavy animation
            const verts = geom.attributes.position.array;
            for (let i = 0; i < verts.length; i += 3) {
                // Wave logic could act here, keeping it simple for performance
            }
            
            plane.position.z = (time * 2) % 2.5; // Moving forward illusion
            
            // Mouse parallax effect
            camera.position.x += (mouseX * 5 - camera.position.x) * 0.05;
            camera.position.y += (-mouseY * 5 - camera.position.y + 2) * 0.05;
            
            renderer.render(scene, camera);
        }
        
        let mouseX = 0; let mouseY = 0;
        window.addEventListener('mousemove', (e) => {
            mouseX = (e.clientX / window.innerWidth) * 2 - 1;
            mouseY = (e.clientY / window.innerHeight) * 2 - 1;
        });
        
        // Geometry fix for wave animation
        const geom = plane.geometry;

        animateWebGL();

        // Responsive WebGL
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

        // --- 4. GSAP Timelines ---
        gsap.registerPlugin(ScrollTrigger);

        // Connect Lenis with ScrollTrigger
        lenis.on('scroll', ScrollTrigger.update);
        gsap.ticker.add((time) => { lenis.raf(time * 1000); });
        gsap.ticker.lagSmoothing(0);

        // Initial Load Sequence
        const tl = gsap.timeline();
        tl.from(".hero-text", {
            y: 200, duration: 1.5, ease: "power4.out", stagger: 0.15, delay: 0.2
        })
        .to(".sub-text", { opacity: 1, y: -20, duration: 1, ease: "power2.out" }, "-=0.8")
        .to(".magnetic-btn", { opacity: 1, y: 0, duration: 1, ease: "power2.out" }, "-=0.6");

        // Scroll Indicator Line Animation
        gsap.to("#scroll-line", {
            backgroundPosition: "0 100%", duration: 1.5, repeat: -1, ease: "linear"
        });

        // Parallax Hero Section out
        gsap.to(".hero-container", {
            scrollTrigger: { trigger: "#hero", start: "top top", end: "bottom top", scrub: 1 },
            y: 150, opacity: 0
        });

        // Features Reveal
        gsap.from(".card-reveal", {
            scrollTrigger: { trigger: "#features", start: "top 70%" },
            y: 100, opacity: 0, duration: 1.2, ease: "power4.out", stagger: 0.2
        });

        // Marquee Rotate Parallax
        gsap.to(".marquee-container", {
            scrollTrigger: { trigger: "#marquee-section", start: "top bottom", scrub: true },
            rotate: -2, scale: 1.05
        });

    </script>
</body>
</html>"""
    
    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"✅ Motion Ultra-Premium Showcase generated: {output_path}")

if __name__ == "__main__":
    generate_motion_demo()
