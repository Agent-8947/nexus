import base64
import os

img_path = r'C:\Users\MAC\.gemini\antigravity\brain\5f0742a1-4510-42e6-a1a3-716c2b387257\media__1775854782076.jpg'
b64 = base64.b64encode(open(img_path, 'rb').read()).decode('utf-8')

# FIXING JS SYNTAX (The f-string was breaking curly braces)
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PRINTIVO | HYPER-KINETIC</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Inter:wght@900&display=swap');
        
        body {{
            background-color: #000;
            color: #fff;
            font-family: 'Syncopate', sans-serif;
            overflow: hidden;
            margin: 0;
            perspective: 2000px;
        }}

        #viewport {{
            width: 100%;
            height: 100vh;
            position: relative;
            transform-style: preserve-3d;
        }}

        #camera-rig {{
            width: 100%;
            height: 100%;
            position: absolute;
            transform-style: preserve-3d;
            will-change: transform;
        }}

        .scene {{
            position: absolute;
            width: 100vw;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            backface-visibility: hidden;
            transform-style: preserve-3d;
        }}

        .giant-text {{
            font-size: 10vw;
            line-height: 0.8;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: -0.05em;
        }}

        .highlight {{
            color: transparent;
            -webkit-text-stroke: 2px #fff;
        }}

        .brand-logo {{
            width: 500px;
            filter: invert(1) brightness(2);
        }}

        #particles {{
            position: fixed;
            inset: 0;
            z-index: -1;
            background: radial-gradient(circle at center, #222 0%, #000 100%);
        }}

        /* DISTORTION CONTAINER */
        #distort-container {{
            width: 100%;
            height: 100%;
            filter: url(#gooey);
        }}
    </style>
</head>
<body>

    <div id="particles"></div>

    <div id="viewport">
        <div id="camera-rig">
            
            <section id="anchor-1" class="scene" style="transform: translateZ(0px);">
                <div class="flex flex-col items-center justify-center">
                    <img src="data:image/jpeg;base64,{b64}" alt="Logo" class="brand-logo mb-12" id="hero-logo">
                    <h1 class="giant-text">MODERN<br><span class="highlight">PRINT</span></h1>
                </div>
            </section>

            <section id="anchor-2" class="scene" style="transform: translateY(100vh) rotateX(90deg) translateZ(-500px);">
                <div class="max-w-6xl text-center">
                    <h2 class="giant-text highlight">INSANE</h2>
                    <h2 class="giant-text">SPD</h2>
                </div>
            </section>

            <section id="anchor-3" class="scene" style="transform: translateX(100vw) rotateY(-90deg) translateZ(-500px);">
                <div class="text-left p-20 border-l-8 border-white bg-white/5">
                    <h2 class="text-7xl font-black mb-4 uppercase">PRECISION</h2>
                </div>
            </section>

        </div>
    </div>

    <script>
        gsap.registerPlugin(ScrollTrigger);
        const rig = document.querySelector("#camera-rig");
        
        const tl = gsap.timeline({{
            scrollTrigger: {{
                trigger: "body",
                start: "top top",
                end: "bottom bottom",
                scrub: 1
            }}
        }});

        // Animation Steps
        tl.to(rig, {{
            y: "-100vh",
            rotationX: -90,
            z: 800,
            duration: 1,
            ease: "expo.inOut"
        }});

        tl.to(rig, {{
            x: "-100vw",
            rotationX: -90,
            rotationY: 90,
            z: 0,
            duration: 1,
            ease: "expo.inOut"
        }});

        // Intro
        gsap.from("#hero-logo", {{ scale: 0, rotation: 360, duration: 2, ease: "elastic.out(1, 0.3)" }});

    </script>
    
    <div style="height: 500vh;"></div>

</body>
</html>"""

out_path = 'PROJECT/outputs/omni_artifacts/giga_printivo_v11_hyper.html'
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("V11 Hyper-Kinetic Variant generated successfully!")
