import os
from pathlib import Path

def generate_cinematic_v5():
    print("🎬 NEXUS V5 Engine: Image-Driven Cinematic [9:16]...")
    
    project_root = Path("e:/Downloads/--ANTIGRAVITY store/IDE-optimus")
    output_path = project_root / "PROJECT" / "outputs" / "Cinematic_V5_9x16.html"
    
    # Use the image provided by user
    image_path = "https://files.oaiusercontent.com/file-2u2W3Z2u2W3Z2u2W3Z2u2W3Z" # Placeholder or local path if we had it
    # We will assume the image is placed at PROJECT/assets/images/nexus_logo.png
    local_image = "file:///e:/Downloads/--ANTIGRAVITY store/IDE-optimus/PROJECT/assets/images/nexus_logo.png"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1080, height=1920, initial-scale=1.0">
    <title>NEXUS | V5 Image Cinematic</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;900&display=swap" rel="stylesheet">
    
    <style>
        :root {{
            --bg: #030408;
            --accent: #00f2ff;
            --white: #ffffff;
        }}

        * {{ box-sizing: border-box; cursor: none !important; }}
        
        body, html {{ 
            margin: 0; padding: 0; width: 1080px; height: 1920px; 
            background-color: var(--bg); overflow: hidden; 
            font-family: 'Inter', sans-serif;
        }}

        .image-container {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            display: flex; align-items: center; justify-content: center;
            overflow: hidden; z-index: 1;
        }}

        #main-img {{
            width: 100%; height: 100%; object-fit: cover;
            filter: brightness(0.7) contrast(1.2);
            transform: scale(1.1);
        }}

        .overlay {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: radial-gradient(circle at center, transparent 20%, rgba(3,4,8,0.8) 100%);
            z-index: 2;
        }}

        .ui-frame {{
            position: absolute; top: 40px; left: 40px; right: 40px; bottom: 40px;
            border: 2px solid rgba(0, 242, 255, 0.3);
            z-index: 10; pointer-events: none;
        }}

        .corner {{
            position: absolute; width: 40px; height: 40px;
            border: 4px solid var(--accent);
        }}
        .tl {{ top: -2px; left: -2px; border-right: none; border-bottom: none; }}
        .tr {{ top: -2px; right: -2px; border-left: none; border-bottom: none; }}
        .bl {{ bottom: -2px; left: -2px; border-right: none; border-top: none; }}
        .br {{ bottom: -2px; right: -2px; border-left: none; border-top: none; }}

        .text-wrap {{
            position: absolute; bottom: 200px; left: 80px; width: 920px;
            z-index: 20; color: var(--white);
        }}

        .hero-title {{
            font-family: 'Syncopate', sans-serif; font-size: 10rem;
            line-height: 0.9; margin-bottom: 2rem; opacity: 0;
            text-shadow: 0 0 30px rgba(0, 242, 255, 0.5);
        }}

        .hero-sub {{
            font-size: 3rem; font-weight: 400; text-transform: uppercase;
            letter-spacing: 15px; color: var(--accent); opacity: 0;
        }}

        .glitch-slice {{
            position: absolute; width: 100%; height: 100px;
            background: inherit; pointer-events: none;
            z-index: 5; display: none;
        }}

    </style>
</head>
<body>
    <div class="image-container">
        <img id="main-img" src="{local_image}" alt="NEXUS">
        <div class="overlay"></div>
    </div>

    <div class="ui-frame">
        <div class="corner tl"></div>
        <div class="corner tr"></div>
        <div class="corner bl"></div>
        <div class="corner br"></div>
    </div>

    <div class="text-wrap">
        <div class="hero-sub" id="sub1">INITIALIZING MAS...</div>
        <h1 class="hero-title" id="title1">LEGALLY<br>BORN.</h1>
    </div>

    <script>
        const tl = gsap.timeline();

        // 1. Initial Scale & Flicker (0-3s)
        tl.fromTo("#main-img", 
            {{ scale: 1.5, filter: "brightness(0) blur(20px)" }}, 
            {{ scale: 1.1, filter: "brightness(0.7) blur(0px)", duration: 2, ease: "expo.out" }}
        )
        .to("#sub1", {{ opacity: 1, y: -20, duration: 0.5, ease: "power2.out" }}, "-=1")
        .to("#title1", {{ opacity: 1, x: 20, duration: 0.8, ease: "power4.out" }}, "-=0.3")

        // 2. Technical Macro-Vibration (3-6s)
        .to("#main-img", {{ x: 2, y: -2, duration: 0.05, repeat: 20, yoyo: true, ease: "power1.inOut" }})
        .to(".ui-frame", {{ borderColor: "rgba(0, 242, 255, 1)", duration: 0.1, yoyo: true, repeat: 10 }}, "-=1")

        // 3. Zoom-In Destruction (6-9s)
        .to("#main-img", {{ scale: 1.3, duration: 3, ease: "power2.inOut" }}, "-=1")
        .to("#title1", {{ textContent: "DEVOPS", duration: 0.1, delay: 0.5 }})
        .to("#sub1", {{ textContent: "ALGORITHMIC PRESSURE", color: "#ff003c", duration: 0.1 }})

        // 4. Final Cut (9-10s)
        .to("body", {{ filter: "invert(1)", duration: 0.05, yoyo: true, repeat: 5 }})
        .to("body", {{ backgroundColor: "#000", opacity: 0, duration: 0.3, delay: 0.2 }});

    </script>
</body>
</html>"""
    
    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ V5 Image-Driven Cinematic generated: {output_path}")

if __name__ == "__main__":
    generate_cinematic_v5()
