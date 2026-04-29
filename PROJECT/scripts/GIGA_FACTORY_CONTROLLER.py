import sys
import os
import subprocess
import base64
import time

# --- CONFIGURATION ---
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
RECORDER_PATH = os.path.join(BASE_PATH, "PROJECT/WIKI-FARM/NEXUS-FARM-DNA/DNA/DNA_12_AST_RENDER/WEB_MOTION_RECORDER_synthesized_agent.py")
ARTIFACTS_DIR = os.path.join(BASE_PATH, "PROJECT/outputs/omni_artifacts")
OUTPUT_DIR = os.path.join(BASE_PATH, "PROJECT/outputs/motion_recordings")
LOGO_PATH = r'C:\Users\MAC\.gemini\antigravity\brain\5f0742a1-4510-42e6-a1a3-716c2b387257\media__1775854782076.jpg'

def generate_v11_hyper(brand_name="PRINTIVO", tag="EVOLUTION", subtext="DYNAMIC SPEED", duration=10):
    """Generates the V11 Hyper-Kinetic HTML with embedded logo."""
    print(f"[*] Generating Cinematic Asset: {brand_name}...")
    
    with open(LOGO_PATH, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>GIGA PRODUCTION | {brand_name}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@900&display=swap');
        body {{ background: #000; color: #fff; font-family: 'Syncopate', sans-serif; overflow: hidden; }}
        #viewport {{ width: 100%; height: 100vh; perspective: 2000px; }}
        #rig {{ width: 100%; height: 100%; position: absolute; transform-style: preserve-3d; }}
        .scene {{ position: absolute; width: 100vw; height: 100vh; display: flex; align-items: center; justify-content: center; transform-style: preserve-3d; }}
        .giant {{ font-size: 12vw; line-height: 0.8; font-weight: 700; text-transform: uppercase; }}
        .stroke {{ color: transparent; -webkit-text-stroke: 2px #fff; }}
        #particles {{ position: fixed; inset: 0; background: radial-gradient(circle, #222 0%, #000 100%); z-index: -1; }}
    </style>
</head>
<body>
    <div id="particles"></div>
    <div id="viewport"><div id="rig">
        <section class="scene">
            <div class="flex flex-col items-center">
                <img src="data:image/jpeg;base64,{b64}" style="width:500px; filter:invert(1) brightness(2);" id="logo">
                <h1 class="giant" id="t1">{tag}</h1>
            </div>
        </section>
        <section class="scene" style="transform: translateY(100vh) rotateX(90deg) translateZ(-500px);">
            <h2 class="giant stroke">{subtext}</h2>
        </section>
    </div></div>
    <script>
        gsap.registerPlugin(ScrollTrigger);
        const rig = document.querySelector("#rig");
        const tl = gsap.timeline({{scrollTrigger: {{trigger:"body", start:"top top", end:"bottom bottom", scrub:1 }}}});
        tl.to(rig, {{ y:"-100vh", rotationX:-90, z:800, duration:1, ease:"expo.inOut" }});
        gsap.from("#logo", {{ scale:0, rotation:720, duration:2, ease:"elastic.out(1,0.3)" }});
    </script>
    <div style="height:500vh;"></div>
</body>
</html>"""
    
    file_path = os.path.join(ARTIFACTS_DIR, f"prod_line_{brand_name.lower()}.html")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    return file_path

def run_recorder(html_path, duration=10):
    """Triggers the Python CDP Recorder Agent."""
    print(f"[*] Starting Video Synthesis for {html_path}...")
    cmd = [
        "python", RECORDER_PATH,
        "--url", f"file:///{html_path}",
        "--duration", str(duration),
        "--mode", "linear",
        "--format", "both"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    # ONE CLICK PRODUCTION
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    target_brand = "PRINTIVO"
    target_duration = 5 # Заданный тобой хронометраж
    
    html_file = generate_v11_hyper(brand_name=target_brand, duration=target_duration)
    run_recorder(html_file, duration=target_duration)
    
    print("\n[SUCCESS] GIGA-FACTORY CYCLE COMPLETE.")
    print(f"[LOCATION] Outputs are in {OUTPUT_DIR}")
