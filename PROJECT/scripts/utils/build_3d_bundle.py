import base64
import os

def image_to_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_3d_viewer():
    tshirt_path = r"e:\Downloads\--ANTIGRAVITY store\IDE-optimus\PROJECT\frontend\nexus-v2\public\assets\tshirt.png"
    logo_path = r"e:\Downloads\--ANTIGRAVITY store\IDE-optimus\PROJECT\frontend\nexus-v2\public\assets\logo_transparent.png"
    
    tshirt_b64 = image_to_base64(tshirt_path)
    logo_b64 = image_to_base64(logo_path)

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXUS | INDUSTRIAL 3D PRINT SIM (EMBEDDED)</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{ margin: 0; background: #000; overflow: hidden; font-family: monospace; color: #38bdf8; }}
        #canvas-container {{ position: absolute; width: 100%; height: 100%; }}
        .ui-overlay {{ position: absolute; top: 40px; left: 40px; z-index: 100; pointer-events: none; }}
        .controls-hint {{ position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%); color: rgba(255,255,255,0.3); font-size: 10px; letter-spacing: 0.2em; }}
        #loader {{ position: fixed; inset: 0; background: #000; display: flex; align-items: center; justify-content: center; z-index: 1000; }}
    </style>
</head>
<body>
    <div id="loader">
        <div class="animate-pulse tracking-widest text-[10px]">RECONSTRUCTING 3D MESH...</div>
    </div>
    <div class="ui-overlay">
        <div class="text-[10px] opacity-40 uppercase tracking-widest">NEXUS // PHOTONIC_STUDIO</div>
        <div class="text-3xl font-bold italic tracking-tighter">3D_NEXUS_FABRIC_V4</div>
        <div class="text-[10px] mt-4 text-emerald-400">● PORTABLE_MODE_ACTIVE</div>
    </div>
    <div id="canvas-container"></div>
    <div class="controls-hint">DRAG TO ROTATE // SCROLL TO ZOOM</div>

    <script>
        const TSHIRT_DATA = "data:image/png;base64,{tshirt_b64}";
        const LOGO_DATA = "data:image/png;base64,{logo_b64}";

        let scene, camera, renderer, cloth, controls;
        const loader = new THREE.TextureLoader();

        function init() {{
            scene = new THREE.Scene();
            camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.z = 10;

            renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            document.getElementById('canvas-container').appendChild(renderer.domElement);

            scene.add(new THREE.AmbientLight(0xffffff, 0.6));
            const dl = new THREE.DirectionalLight(0xffffff, 1.2);
            dl.position.set(5, 5, 5);
            scene.add(dl);

            const tshirtTex = loader.load(TSHIRT_DATA, () => {{
                document.getElementById('loader').style.display = 'none';
            }});
            const logoTex = loader.load(LOGO_DATA);

            const geometry = new THREE.PlaneGeometry(6, 6, 128, 128);
            const material = new THREE.ShaderMaterial({{
                uniforms: {{
                    tshirtTex: {{ value: tshirtTex }},
                    logoTex: {{ value: logoTex }},
                    time: {{ value: 0 }},
                    revealProgress: {{ value: 0 }}
                }},
                vertexShader: `
                    varying vec2 vUv;
                    uniform sampler2D tshirtTex;
                    uniform float time;
                    
                    void main() {{
                        vUv = uv;
                        vec4 tex = texture2D(tshirtTex, uv);
                        float brightness = (tex.r + tex.g + tex.b) / 3.0;
                        float displacement = (1.0 - brightness) * 0.45;
                        float wave = sin(uv.x * 2.0 + time) * 0.04;
                        vec3 newPos = position + normal * (displacement + wave);
                        gl_Position = projectionMatrix * modelViewMatrix * vec4(newPos, 1.0);
                    }}
                `,
                fragmentShader: `
                    varying vec2 vUv;
                    uniform sampler2D tshirtTex;
                    uniform sampler2D logoTex;
                    uniform float revealProgress;

                    void main() {{
                        vec4 base = texture2D(tshirtTex, vUv);
                        vec2 lUv = (vUv - 0.5) * 3.1 + 0.5;
                        lUv.y += 0.22;
                        
                        vec4 logo = vec4(0.0);
                        if(lUv.x >= 0.0 && lUv.x <= 1.0 && lUv.y >= 0.0 && lUv.y <= 1.0) {{
                            logo = texture2D(logoTex, lUv);
                        }}

                        float mask = smoothstep(1.0 - revealProgress - 0.05, 1.0 - revealProgress, 1.0 - vUv.y);
                        vec3 finalLogo = mix(vec3(0.0), logo.rgb, logo.a * mask);
                        vec3 res = base.rgb * mix(vec3(1.0), finalLogo * 1.4, logo.a * mask);
                        
                        gl_FragColor = vec4(res, base.a);
                        if(gl_FragColor.a < 0.1) discard;
                    }}
                `,
                transparent: true,
                side: THREE.DoubleSide
            }});

            cloth = new THREE.Mesh(geometry, material);
            scene.add(cloth);

            controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.autoRotate = true;
            controls.autoRotateSpeed = 0.5;

            let progress = 0;
            function animate(t) {{
                requestAnimationFrame(animate);
                material.uniforms.time.value = t / 800;
                if(progress < 1) progress += 0.004;
                material.uniforms.revealProgress.value = progress;
                controls.update();
                renderer.render(scene, camera);
            }}
            animate(0);
        }}

        window.onload = init;
        window.onresize = () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }};
    </script>
</body>
</html>"""
    
    output_file = r"e:\Downloads\--ANTIGRAVITY store\IDE-optimus\PROJECT\outputs\TShirt_Industrial_3D.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"[*] 3D Portable Bundle created: {output_file}")

if __name__ == "__main__":
    generate_3d_viewer()
