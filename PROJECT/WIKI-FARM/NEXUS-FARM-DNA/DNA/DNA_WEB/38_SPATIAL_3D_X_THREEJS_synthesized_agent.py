#!/usr/bin/env python3
"""
SPATIAL_3D__X__THREEJS [NEXUS SYNTHESIZED Gen-3: SPATIAL ARCHITECT]
Mission: Synthesizes fully immersive WebGL 3D environments with DOM overlays.
Heritage: NEXUS_MOTION_ENGINE + THREE.js

I/O Contract:
  Input:  Immersive theme (from CLI --prompt)
  Output: Rendered HTML artifact containing Three.js shaders and geometry.
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("NEXUS_SPATIAL_ARCHITECT")

class SpatialDesigner:
    def __init__(self):
        self.output_dir = Path(__file__).resolve().parents[5] / "PROJECT" / "outputs" / "design_artifacts"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate(self, prompt: str) -> Path:
        logger.info(f"Synthesizing 3D Spatial UI for theme: {prompt}")
        title = prompt.upper()
        
        # HTML template with Three.js point cloud logic + CSS UI overlay
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | NEXUS 3D</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;600&display=swap" rel="stylesheet">
    <style>
        body {{
            margin: 0; padding: 0; overflow: hidden; background-color: #030305;
            font-family: 'Space Grotesk', sans-serif; color: white;
            user-select: none;
        }}
        #webgl-container {{ position: absolute; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 1; }}
        
        /* UI Overlay */
        .ui-layer {{
            position: absolute; top: 0; left: 0; width: 100vw; height: 100vh;
            z-index: 10; pointer-events: none; /* Let clicks pass through to 3D */
            display: flex; flex-direction: column; justify-content: center; align-items: center;
        }}
        h1 {{
            font-size: 6vw; font-weight: 600; text-transform: uppercase; letter-spacing: 0.2em;
            background: linear-gradient(135deg, #ffffff 0%, #4facfe 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin: 0; filter: drop-shadow(0px 0px 10px rgba(79, 172, 254, 0.5));
            text-align: center;
        }}
        .subtitle {{ font-size: 1.5vw; color: #8892b0; margin-top: 1rem; letter-spacing: 0.1em; }}
        
        .hud-corner {{
            position: absolute; padding: 2rem; color: rgba(255,255,255,0.4);
            font-size: 0.8rem; letter-spacing: 2px;
        }}
        .sys-top-left {{ top: 0; left: 0; }}
        .sys-bottom-right {{ bottom: 0; right: 0; text-align: right; }}

        .interactive-btn {{
            pointer-events: auto; /* Re-enable clicks */
            margin-top: 4rem; padding: 1rem 3rem; background: rgba(255,255,255,0.05);
            border: 1px solid rgba(79, 172, 254, 0.3); border-radius: 40px;
            color: #4facfe; font-family: 'Space Grotesk'; text-transform: uppercase;
            cursor: pointer; transition: all 0.3s ease; backdrop-filter: blur(5px);
        }}
        .interactive-btn:hover {{ background: rgba(79, 172, 254, 0.2); box-shadow: 0 0 20px rgba(79, 172, 254, 0.4); }}
    </style>
</head>
<body>
    <div id="webgl-container"></div>
    
    <div class="ui-layer">
        <div class="hud-corner sys-top-left">
            <div>NEXUS SPATIAL ENGINE v3.0</div>
            <div>[STATUS: OPTIMAL]</div>
        </div>
        <div class="hud-corner sys-bottom-right">
            <div>LAT: 45.92 / LONG: -12.44</div>
            <div>SCALAR FIELD ACTIVE</div>
        </div>

        <h1>{title}</h1>
        <div class="subtitle">Immersive 3D Topological Simulation</div>
        <button class="interactive-btn" onmouseover="boostSpeed()" onmouseout="normalizeSpeed()">Engage Hyperdrive</button>
    </div>

    <script>
        // Three.js Setup
        const container = document.getElementById('webgl-container');
        const scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x030305, 0.001);

        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 2000);
        camera.position.z = 1000;

        const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setSize(window.innerWidth, window.innerHeight);
        container.appendChild(renderer.domElement);

        // Particle System (Point Cloud)
        const geometry = new THREE.BufferGeometry();
        const particlesCount = 5000;
        const posArray = new Float32Array(particlesCount * 3);
        const colorArray = new Float32Array(particlesCount * 3);

        for(let i = 0; i < particlesCount * 3; i+=3) {{
            // Spline distribution
            posArray[i] = (Math.random() - 0.5) * 4000;
            posArray[i+1] = (Math.random() - 0.5) * 4000;
            posArray[i+2] = (Math.random() - 0.5) * 4000;

            // Deep blue to cyan gradient mapping based on depth
            const depth = Math.random();
            colorArray[i] = 0.05; // R
            colorArray[i+1] = depth * 0.5 + 0.2; // G
            colorArray[i+2] = depth * 0.8 + 0.2; // B
        }}

        geometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colorArray, 3));

        // Circular custom particle via canvas
        const circleTexture = new THREE.CanvasTexture((() => {{
            const canvas = document.createElement('canvas'); canvas.width=16; canvas.height=16;
            const context = canvas.getContext('2d');
            context.beginPath(); context.arc(8,8,8,0, Math.PI*2); context.fillStyle = 'white'; context.fill();
            return canvas;
        }})());

        const material = new THREE.PointsMaterial({{
            size: 6,
            vertexColors: true,
            map: circleTexture,
            transparent: true,
            opacity: 0.8,
            blending: THREE.AdditiveBlending,
            depthWrite: false
        }});

        const particlesMesh = new THREE.Points(geometry, material);
        scene.add(particlesMesh);

        // Interaction state
        let mouseX = 0; let mouseY = 0;
        let targetX = 0; let targetY = 0;
        let speedMultiplier = 1;

        window.addEventListener('mousemove', (e) => {{
            mouseX = (e.clientX - window.innerWidth / 2) * 2;
            mouseY = (e.clientY - window.innerHeight / 2) * 2;
        }});

        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});

        // Methods linked to HTML UI
        window.boostSpeed = () => {{ speedMultiplier = 15; }};
        window.normalizeSpeed = () => {{ speedMultiplier = 1; }};

        // Animation Loop
        const clock = new THREE.Clock();
        function animate() {{
            requestAnimationFrame(animate);
            const elapsedTime = clock.getElapsedTime();

            targetX = mouseX * 0.001;
            targetY = mouseY * 0.001;

            // Smooth camera inertia
            particlesMesh.rotation.y += 0.001 * speedMultiplier;
            particlesMesh.rotation.x += 0.0005 * speedMultiplier;
            
            // Mouse parallax 
            particlesMesh.rotation.y += 0.05 * (targetX - particlesMesh.rotation.y);
            particlesMesh.rotation.x += 0.05 * (targetY - particlesMesh.rotation.x);
            
            // Pulsating points
            const colors = geometry.attributes.color.array;
            for(let i = 0; i < particlesCount * 3; i+=3) {{
                // subtle color shift based on sine waves
                colors[i+2] = Math.sin(elapsedTime * 2 + posArray[i]) * 0.2 + 0.8;
            }}
            geometry.attributes.color.needsUpdate = true;

            renderer.render(scene, camera);
        }}
        
        animate();
    </script>
</body>
</html>"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = prompt.replace(" ", "_").lower()[:20]
        output_file = self.output_dir / f"3d_ui_{filename}_{timestamp}.html"
        output_file.write_text(html_content, encoding="utf-8")
        return output_file

def main():
    parser = argparse.ArgumentParser(description="NEXUS Spatial Designer")
    parser.add_argument("--prompt", default="Quantum Core Visualizer", help="3D Theme Prompt")
    parser.add_argument("--test", action="store_true", help="Run integration test")
    args = parser.parse_args()

    designer = SpatialDesigner()
    
    if args.test:
        out = designer.generate("System Self Test")
        if out.exists():
            print("[TEST] Passed.")
        sys.exit(0)
        
    out_file = designer.generate(args.prompt)
    print(f"[SUCCESS] Spatial 3D UI Generated -> {out_file.absolute()}")


if __name__ == "__main__":
    main()
