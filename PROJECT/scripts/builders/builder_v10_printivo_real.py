import base64
import os

img_path = r'C:\Users\MAC\.gemini\antigravity\brain\5f0742a1-4510-42e6-a1a3-716c2b387257\media__1775854782076.jpg'
b64 = base64.b64encode(open(img_path, 'rb').read()).decode('utf-8')

html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PRINTIVO | CAMPAGNE EXPRESS</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/studio-freight/lenis@1.0.19/bundled/lenis.min.js"></script>
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;400;600;800&display=swap');
        
        body {{
            background-color: #fafbfc;
            color: #050505;
            font-family: 'Inter', -apple-system, sans-serif;
            overflow-x: hidden;
            margin: 0;
            padding: 0;
        }}

        /* The Premium Apple-Style Soft Glows */
        .ambient-mesh {{
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100vh;
            z-index: 0;
            pointer-events: none;
            overflow: hidden;
        }}
        .ambient-blur {{
            position: absolute;
            border-radius: 50%;
            filter: blur(140px);
            opacity: 0.8;
            mix-blend-mode: multiply;
        }}
        
        /* Vibrant Colors fitting the Printivo Gradient */
        .mesh-magenta {{ background: #ff007f; width: 80vw; height: 80vw; top: 10%; right: -20%; }}
        .mesh-cyan {{ background: #00e5ff; width: 70vw; height: 70vw; bottom: -20%; left: -20%; }}

        /* The Glass Surface layer to soften everything */
        .glass-surface {{
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(255, 255, 255, 0.4);
            backdrop-filter: blur(50px);
            -webkit-backdrop-filter: blur(50px);
            z-index: 1;
            pointer-events: none;
        }}

        /* Typography */
        .hyper-title {{
            font-size: clamp(3rem, 8vw, 8rem);
            line-height: 0.9;
            letter-spacing: -0.04em;
            font-weight: 800;
        }}
        
        .sub-text {{
            font-size: clamp(1rem, 2vw, 1.5rem);
            line-height: 1.4;
            letter-spacing: -0.01em;
            color: #444;
            max-width: 800px;
        }}

        /* Section Layout */
        .section-anchor {{
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            z-index: 5;
            padding: 2rem;
            text-align: center;
            flex-direction: column;
        }}
        
        /* Gradient Text */
        .text-gradient {{
            background: linear-gradient(135deg, #0ce6ff 0%, #ff007f 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
    </style>
</head>
<body>

    <!-- Hyper-smooth blurred background system (Apple Style) -->
    <div class="ambient-mesh">
        <div class="ambient-blur mesh-magenta" id="mesh-1"></div>
        <div class="ambient-blur mesh-cyan" id="mesh-2"></div>
    </div>
    <div class="glass-surface"></div>

    <div id="lenis-content" class="w-full relative z-10">

        <!-- ANCHOR 1: DTF PREMIUM (HERO) -->
        <section id="anchor-1" class="section-anchor">
            <div class="mb-12 block-anim">
                <img src="data:image/jpeg;base64,{b64}" 
                     alt="Printivo" 
                     class="w-[400px] md:w-[600px] mix-blend-multiply opacity-100 mx-auto"
                     style="filter: invert(1) contrast(150) brightness(0);">
            </div>

            <div class="block-anim">
                <h1 class="hyper-title mb-6">DTF Transfers<br><span class="text-gradient">Premium</span></h1>
                <p class="sub-text mx-auto font-semibold text-black">Vibrance exceptionnelle. Qualité garantie.</p>
            </div>
        </section>

        <!-- ANCHOR 2: SPEED -->
        <section id="anchor-2" class="section-anchor">
            <div class="block-anim w-full max-w-4xl">
                <h1 class="hyper-title mb-6 tracking-tight">Expédition le<br><span class="text-gradient">jour même.</span></h1>
                <p class="sub-text mx-auto font-medium text-gray-700">Commandez avant midi, expédition assurée.</p>
            </div>
        </section>

        <!-- ANCHOR 3: PRICE -->
        <footer id="anchor-3" class="section-anchor">
            <div class="block-anim w-full max-w-5xl">
                <h1 class="hyper-title mb-6">0,017$ <span class="text-3xl text-gray-400">/ sq in</span></h1>
                <p class="sub-text mx-auto text-center mb-10 text-black">
                    Vérification et découpe <span class="text-gradient font-bold">GRATUITES</span>.
                </p>
                <h2 class="text-4xl font-black tracking-widest text-black">PRINTIVO.CA</h2>
            </div>
        </footer>

    </div>

    <script>
        gsap.registerPlugin(ScrollTrigger);

        const lenis = new Lenis({{
            // For a fast 5s video, we make lenis highly responsive
            duration: 0.8, 
            easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
            direction: 'vertical',
            gestureDirection: 'vertical',
            smooth: true
        }});

        function raf(time) {{
            lenis.raf(time);
            requestAnimationFrame(raf);
        }}
        requestAnimationFrame(raf);

        // --- ANIMATIONS --- //
        
        // Fast Mesh Parallax
        gsap.to(".mesh-magenta", {{ y: 300, scale: 1.2, scrollTrigger: {{ scrub: 0 }} }});
        gsap.to(".mesh-cyan", {{ y: -300, scale: 0.9, scrollTrigger: {{ scrub: 0 }} }});

        // Fast Entrance (0.5s instead of 2s because video is 5s)
        const entries = gsap.utils.toArray('.block-anim');
        entries.forEach((el, i) => {{
            const isHero = i < 2; 
            if(isHero) {{
                gsap.from(el, {{ y: 80, opacity: 0, duration: 0.8, ease: "power4.out", delay: i*0.1 }});
            }} else {{
                gsap.from(el, {{
                    scrollTrigger: {{ trigger: el, start: "top 80%" }},
                    y: 100, opacity: 0, duration: 0.8, ease: "power4.out"
                }});
            }}
        }});
        
        // Shrink Hero over fast scroll
        gsap.to("#anchor-1", {{
            scale: 0.7, opacity: 0,
            scrollTrigger: {{ trigger: "#anchor-2", start: "top bottom", end: "top center", scrub: 0 }}
        }});

    </script>
</body>
</html>"""

out_path = 'PROJECT/outputs/omni_artifacts/giga_printivo_v10_real.html'
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("V10 Real Campaign Variant generated successfully!")
