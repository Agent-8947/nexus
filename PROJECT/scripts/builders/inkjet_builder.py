"""
NEXUS INKJET BUILDER v2.0 (Consolidated)
Replaces: build_inkjet_block.py, build_looping_inkjet.py,
          build_realistic_inkjet.py, build_ultimate_inkjet.py

Usage:
  python inkjet_builder.py --mode loop      # Auto-looping version
  python inkjet_builder.py --mode click     # Button-triggered version
  python inkjet_builder.py --passes 30      # Custom pass count
  python inkjet_builder.py --speed 0.2      # Fast sweep
"""
import argparse
import base64
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = PROJECT_ROOT / "frontend" / "nexus-v2" / "public" / "assets"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

def image_to_base64(path: Path) -> str:
    if not path.exists():
        print(f"[!] Asset not found: {path}")
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def build_css(mode: str) -> str:
    return """
        :root { --accent: #38bdf8; --dark: #1e293b; }
        body { background: #fff; min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: 'Outfit', sans-serif; overflow: hidden; }
        .stage { position: relative; width: 100%%; max-width: 900px; aspect-ratio: 1; display: flex; align-items: center; justify-content: center; }
        .print-unit { position: absolute; top: 17%%; left: 50%%; width: 32.8%%; height: 48.5%%; transform: translateX(-50%%); pointer-events: none; overflow: hidden; }
        .carriage { position: absolute; width: 45px; height: 12px; background: var(--dark); border-bottom: 3px solid var(--accent); border-radius: 2px; z-index: 50; opacity: 0; box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4); }
        .blue-flare { position: absolute; width: 100%%; height: 3px; background: var(--accent); bottom: -3px; box-shadow: 0 0 20px var(--accent), 0 0 40px rgba(56, 189, 248, 0.8); opacity: 0; }
        .logo-print { width: 90%%; height: 90%%; margin: 5%% auto; object-fit: contain; mix-blend-mode: multiply; clip-path: inset(100%% 0 0 0); filter: contrast(1.1) brightness(1.1); }
        .vibrate { animation: shake 0.1s infinite; }
        @keyframes shake { 0%% { transform: translate(0,0); } 50%% { transform: translate(1px, -1px); } 100%% { transform: translate(0,0); } }
        .telemetry { position: absolute; bottom: 40px; left: 40px; font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.2em; }
    """

def build_js_loop(passes: int, speed: float) -> str:
    return f"""
        const logo = document.getElementById('logo');
        const carriage = document.querySelector('.carriage');
        const flare = document.querySelector('.blue-flare');
        const statusLine = document.getElementById('status-line');
        const passLine = document.getElementById('pass-line');

        function startCycle() {{
            statusLine.innerText = "● Inkjet_Active";
            statusLine.style.color = "#38bdf8";
            passLine.style.opacity = 1;

            const passes = {passes};
            const tl = gsap.timeline({{
                onComplete: () => {{
                    statusLine.innerText = "● Complete // Stabilizing";
                    statusLine.style.color = "#10b981";
                    carriage.classList.remove('vibrate');
                    gsap.to(carriage, {{ duration: 0.5, opacity: 0 }});
                    gsap.delayedCall(3, () => {{
                        statusLine.innerText = "● Resetting";
                        statusLine.style.color = "#94a3b8";
                        gsap.to(logo, {{
                            duration: 1.2, opacity: 0, filter: "blur(8px) brightness(2)",
                            onComplete: () => {{ passLine.style.opacity = 0; setTimeout(startCycle, 500); }}
                        }});
                    }});
                }}
            }});

            gsap.set(logo, {{ clipPath: 'inset(100% 0 0 0)', opacity: 1, filter: "contrast(1.1) brightness(1.1) blur(0px)" }});
            gsap.set(carriage, {{ top: '95%', left: '0%', opacity: 1 }});
            carriage.classList.add('vibrate');

            for (let i = 0; i < passes; i++) {{
                const vPos = 95 - (i * (95 / passes));
                const side = i % 2 === 0 ? '88%' : '2%';
                tl.to(carriage, {{
                    duration: {speed}, left: side, top: vPos + '%', ease: "power1.inOut",
                    onStart: () => {{
                        gsap.to(flare, {{ duration: 0.1, opacity: 1 }});
                        passLine.innerText = "Pass: " + (i+1).toString().padStart(3, '0') + " / " + passes.toString().padStart(3, '0');
                    }},
                    onComplete: () => {{ gsap.to(flare, {{ duration: 0.1, opacity: 0 }}); }}
                }});
                tl.to(logo, {{ duration: {speed}, clipPath: `inset(${{vPos}}% 0 0 0)`, ease: "none" }}, "-={speed}");
            }}
        }}
        window.onload = () => setTimeout(startCycle, 800);
    """

def build_js_click(passes: int, speed: float) -> str:
    return f"""
        let isBusy = false;
        function runCycle() {{
            if(isBusy) return;
            isBusy = true;
            const btn = document.getElementById('btn');
            const logo = document.getElementById('logo');
            const carriage = document.querySelector('.carriage');
            const flare = document.querySelector('.blue-flare');
            const passTxt = document.getElementById('pass-val');

            btn.disabled = true; btn.classList.add('opacity-30');
            const passes = {passes};
            const tl = gsap.timeline({{
                onComplete: () => {{
                    isBusy = false; btn.disabled = false; btn.classList.remove('opacity-30');
                    gsap.to(carriage, {{ duration: 0.5, opacity: 0 }});
                    carriage.classList.remove('vibrate');
                }}
            }});

            gsap.set(logo, {{ clipPath: 'inset(100% 0 0 0)', opacity: 1 }});
            gsap.set(carriage, {{ top: '95%', left: '0%', opacity: 1 }});
            carriage.classList.add('vibrate');

            for (let i = 0; i < passes; i++) {{
                const vPos = 95 - (i * (95 / passes));
                const side = i % 2 === 0 ? '88%' : '2%';
                tl.to(carriage, {{
                    duration: {speed}, left: side, top: vPos + '%', ease: "power1.inOut",
                    onStart: () => {{
                        passTxt.innerText = "Pass: " + (i+1) + " / " + passes;
                        gsap.to(flare, {{ duration: 0.1, opacity: 1 }});
                    }},
                    onComplete: () => {{ gsap.to(flare, {{ duration: 0.1, opacity: 0 }}); }}
                }});
                tl.to(logo, {{ duration: {speed}, clipPath: `inset(${{vPos}}% 0 0 0)`, ease: "none" }}, "-={speed}");
            }}
        }}
    """

def build_body_loop(tshirt_b64: str, logo_b64: str) -> str:
    return f"""
    <div class="stage">
        <div class="telemetry">
            <div id="status-line">● System_Idle</div>
            <div id="pass-line" style="color:#38bdf8; opacity:0; margin-top:8px;">Pass: 000 / 020</div>
        </div>
        <div style="position:relative; width:85%%">
            <img src="data:image/png;base64,{tshirt_b64}" style="width:100%%" alt="T-Shirt">
            <div class="print-unit">
                <div class="carriage"><div class="blue-flare"></div></div>
                <img id="logo" src="data:image/png;base64,{logo_b64}" class="logo-print" alt="Print">
            </div>
        </div>
    </div>
    """

def build_body_click(tshirt_b64: str, logo_b64: str) -> str:
    return f"""
    <div class="stage">
        <div style="position:relative; width:85%%">
            <img src="data:image/png;base64,{tshirt_b64}" style="width:100%%" alt="T-Shirt">
            <div class="print-unit">
                <div class="carriage"><div class="blue-flare"></div></div>
                <img id="logo" src="data:image/png;base64,{logo_b64}" class="logo-print" alt="Print">
            </div>
        </div>
        <div style="position:absolute; bottom:40px; right:40px; text-align:right; font-family:'JetBrains Mono',monospace;">
            <div id="pass-val" style="font-size:10px; color:#38bdf8; font-weight:bold; text-transform:uppercase; letter-spacing:0.2em; margin-bottom:16px;">Pass: 0 / 20</div>
            <button onclick="runCycle()" id="btn" style="background:#1e293b; color:#fff; padding:16px 32px; border:none; border-radius:16px; font-size:10px; text-transform:uppercase; font-weight:bold; letter-spacing:0.2em; cursor:pointer;">Run Production</button>
        </div>
    </div>
    """

def generate(mode: str, passes: int, speed: float):
    tshirt_b64 = image_to_base64(ASSETS_DIR / "tshirt.png")
    logo_b64 = image_to_base64(ASSETS_DIR / "logo_transparent.png")

    if not tshirt_b64 or not logo_b64:
        print("[!] Missing assets. Aborting.")
        sys.exit(1)

    css = build_css(mode)
    body = build_body_loop(tshirt_b64, logo_b64) if mode == "loop" else build_body_click(tshirt_b64, logo_b64)
    js = build_js_loop(passes, speed) if mode == "loop" else build_js_click(passes, speed)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXUS | INKJET v2.0 [{mode.upper()}]</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <style>{css}</style>
</head>
<body>
    {body}
    <script>{js}</script>
</body>
</html>"""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / f"Inkjet_{mode.capitalize()}.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Inkjet [{mode}] generated: {out_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NEXUS Inkjet Builder v2.0")
    parser.add_argument("--mode", choices=["loop", "click"], default="loop", help="Animation mode")
    parser.add_argument("--passes", type=int, default=20, help="Number of print passes")
    parser.add_argument("--speed", type=float, default=0.4, help="Duration per sweep (seconds)")
    args = parser.parse_args()
    generate(args.mode, args.passes, args.speed)
