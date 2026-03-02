"""
NEXUS DTF BUILDER v2.0 (Consolidated)
Replaces: build_pageflip_dtf_module.py, build_peel_loop_module.py,
          build_full_hero_module.py, build_transparent_hero_module.py,
          build_master_block.py, fix_peel_loop.py, fix_visibility_v3.py

Usage:
  python dtf_builder.py --effect peel         # Peel & Stick loop
  python dtf_builder.py --effect pageflip     # Film peel-off reveal
  python dtf_builder.py --effect inkjet-hero  # Hero with inkjet print loop
  python dtf_builder.py --effect laser        # Laser scan studio block
  python dtf_builder.py --layout hero         # Full hero layout with CTA
  python dtf_builder.py --layout studio       # Compact studio card
  python dtf_builder.py --bg transparent      # Transparent background
  python dtf_builder.py --bg white            # White background with blobs
"""
import argparse
import base64
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = PROJECT_ROOT / "frontend" / "nexus-v2" / "public" / "assets"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

# ─── ASSET LOADER ───────────────────────────────────────

def image_to_base64(path: Path) -> str:
    if not path.exists():
        print(f"[!] Asset not found: {path}")
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ─── EFFECT ENGINES ─────────────────────────────────────

EFFECTS = {
    "peel": {
        "title": "PEEL & STICK",
        "elements": """
            <div class="peel-line"></div>
            <img id="logo" src="data:image/png;base64,{logo_b64}" class="logo-img" alt="Print">
        """,
        "extra_css": """
            .peel-line {{
                position: absolute; width: 150%%; height: 4px;
                background: rgba(255,255,255,0.8);
                box-shadow: 0 0 20px rgba(255,255,255,0.5), 0 0 40px rgba(56,189,248,0.3);
                z-index: 50; top: 0; left: -25%%; transform: rotate(-15deg); opacity: 0;
            }}
            .logo-img {{
                width: 90%%; height: 90%%; margin: 5%% auto; object-fit: contain;
                mix-blend-mode: multiply; opacity: 0;
                clip-path: polygon(0 0, 0 0, 0 100%%, 0 100%%);
                filter: contrast(1.1) brightness(1.1);
            }}
        """,
        "js": """
            const logo = document.getElementById('logo');
            const peelLine = document.querySelector('.peel-line');

            function startCycle() {{
                const tl = gsap.timeline({{ onComplete: () => gsap.delayedCall(1.5, startCycle) }});

                // STICK
                tl.set(logo, {{ opacity: 1, clipPath: "polygon(0 0, 0 0, 0 100%, 0 100%)" }});
                tl.set(peelLine, {{ top: "-10%", opacity: 0 }});
                tl.to(peelLine, {{ duration: 0.3, opacity: 1 }});
                tl.to(peelLine, {{ duration: 1.2, top: "110%", ease: "power2.inOut" }});
                tl.to(logo, {{ duration: 1.2, clipPath: "polygon(0 0, 100% 0, 100% 100%, 0 100%)", ease: "power2.inOut" }}, "-=1.2");
                tl.to(peelLine, {{ duration: 0.3, opacity: 0 }});

                // HOLD
                tl.to({{}}, {{ duration: 3 }});

                // PEEL
                tl.to(peelLine, {{ duration: 0.3, opacity: 1 }});
                tl.to(peelLine, {{ duration: 1.2, top: "-10%", ease: "power2.inOut" }});
                tl.to(logo, {{ duration: 1.2, clipPath: "polygon(0 0, 0 0, 0 100%, 0 100%)", ease: "power2.inOut" }}, "-=1.2");
                tl.to(peelLine, {{ duration: 0.3, opacity: 0 }});
            }}
            window.onload = startCycle;
        """
    },
    "pageflip": {
        "title": "PAGE FLIP DTF",
        "elements": """
            <div id="film" class="film-box"><div class="film-skin"></div><div id="sheen" class="film-sheen"></div></div>
            <img id="logo" src="data:image/png;base64,{logo_b64}" class="logo-img" alt="Print">
        """,
        "extra_css": """
            .logo-img {{
                width: 100%%; height: 100%%; object-fit: contain;
                mix-blend-mode: multiply; opacity: 0;
                filter: contrast(1.1) brightness(1.05); transform: scale(0.98);
            }}
            .film-box {{
                position: absolute; inset: -4px; z-index: 30;
                transform-origin: right center; transform-style: preserve-3d; pointer-events: none;
            }}
            .film-skin {{
                position: absolute; inset: 0;
                background: linear-gradient(135deg, rgba(255,255,255,0.7) 0%%, rgba(230,240,255,0.2) 50%%, rgba(255,255,255,0.4) 100%%);
                backdrop-filter: blur(4px); border-radius: 4px;
                border: 0.5px solid rgba(255,255,255,0.4);
                box-shadow: 0 4px 15px rgba(0,0,0,0.05); backface-visibility: hidden;
            }}
            .film-sheen {{
                position: absolute; top: 0; left: 0; width: 10%%; height: 100%%;
                background: linear-gradient(to right, transparent 0%%, rgba(255,255,255,0.8) 50%%, transparent 100%%);
                opacity: 0; z-index: 31;
            }}
        """,
        "js": """
            function runCycle() {{
                const tl = gsap.timeline({{ onComplete: () => gsap.delayedCall(3, restart) }});
                gsap.set("#logo", {{ opacity: 0, scale: 0.98 }});
                gsap.set("#film", {{ rotateY: 0, x: 0, opacity: 1 }});
                tl.to("#film", {{ duration: 2.2, rotateY: -105, x: 80, opacity: 0, ease: "power2.inOut" }});
                tl.fromTo("#sheen", {{ left: "0%", opacity: 0 }}, {{ duration: 1.5, left: "100%", opacity: 1, ease: "none" }}, "-=2");
                tl.to("#logo", {{ duration: 1.2, opacity: 1, scale: 1, ease: "power1.out" }}, "-=1.8");
            }}
            function restart() {{
                const tl = gsap.timeline({{ onComplete: runCycle }});
                tl.to("#logo", {{ duration: 1, opacity: 0, ease: "power2.inOut" }});
                tl.to("#film", {{ duration: 1.5, rotateY: 0, x: 0, opacity: 1, ease: "power3.inOut" }}, "-=0.5");
            }}
            window.onload = runCycle;
        """
    },
    "inkjet-hero": {
        "title": "INKJET HERO",
        "elements": """
            <div class="carriage"></div>
            <img id="logo" src="data:image/png;base64,{logo_b64}" class="logo-img" alt="Print">
        """,
        "extra_css": """
            .carriage {{
                position: absolute; width: 45px; height: 10px; background: #1e293b;
                border-bottom: 3px solid #38bdf8; border-radius: 2px; z-index: 50; opacity: 0;
                box-shadow: 0 5px 15px rgba(56,189,248,0.4);
            }}
            .logo-img {{
                width: 90%%; height: 90%%; margin: 5%% auto; object-fit: contain;
                mix-blend-mode: multiply; clip-path: inset(100%% 0 0 0);
                filter: contrast(1.1) brightness(1.1);
            }}
            .vibrate {{ animation: shake 0.1s infinite; }}
            @keyframes shake {{ 0%% {{ transform: translate(0,0); }} 50%% {{ transform: translate(1px,-1px); }} 100%% {{ transform: translate(0,0); }} }}
        """,
        "js": """
            function startCycle() {{
                const logo = document.getElementById('logo');
                const carriage = document.querySelector('.carriage');
                const passes = 22;
                const tl = gsap.timeline({{
                    onComplete: () => {{
                        gsap.to(carriage, {{ duration: 0.5, opacity: 0 }});
                        carriage.classList.remove('vibrate');
                        gsap.delayedCall(4, () => {{
                            gsap.to(logo, {{ duration: 1.5, opacity: 0, filter: "blur(10px) brightness(1.5)", onComplete: startCycle }});
                        }});
                    }}
                }});
                gsap.set(logo, {{ clipPath: 'inset(100% 0 0 0)', opacity: 1, filter: "none" }});
                gsap.set(carriage, {{ top: '95%', left: '0%', opacity: 1 }});
                carriage.classList.add('vibrate');
                for (let i = 0; i < passes; i++) {{
                    const vPos = 95 - (i * (95 / passes));
                    const side = i % 2 === 0 ? '85%' : '5%';
                    tl.to(carriage, {{ duration: 0.35, left: side, top: vPos + '%', ease: "power1.inOut" }});
                    tl.to(logo, {{ duration: 0.35, clipPath: `inset(${{vPos}}% 0 0 0)`, ease: "none" }}, "-=0.35");
                }}
            }}
            window.onload = startCycle;
        """
    },
    "laser": {
        "title": "LASER STUDIO",
        "elements": """
            <div class="laser-line"></div>
            <img id="logo" src="data:image/png;base64,{logo_b64}" class="logo-img" alt="Print">
        """,
        "extra_css": """
            .laser-line {{
                position: absolute; top: 0; left: -15%%; right: -15%%; height: 3px;
                background: #38bdf8; box-shadow: 0 0 15px #38bdf8; opacity: 0; z-index: 20;
            }}
            .logo-img {{
                width: 90%%; height: 90%%; margin: 5%% auto; object-fit: contain;
                mix-blend-mode: multiply; clip-path: inset(100%% 0 0 0); opacity: 0;
                filter: contrast(1.1) brightness(1.1) blur(10px); transform: scale(1.1);
            }}
        """,
        "js": """
            function startCycle() {{
                const logo = document.getElementById('logo');
                const laser = document.querySelector('.laser-line');
                const tl = gsap.timeline({{ onComplete: () => {{
                    gsap.delayedCall(4, () => {{
                        gsap.to(logo, {{ duration: 1, opacity: 0, filter: 'blur(10px)', onComplete: () => {{
                            gsap.set(laser, {{ top: '0' }});
                            startCycle();
                        }} }});
                    }});
                }} }});
                gsap.set(logo, {{ opacity: 0, scale: 1.1, filter: 'blur(10px)', clipPath: 'inset(100% 0 0 0)' }});
                tl.to(laser, {{ duration: 0.2, opacity: 1 }});
                tl.to(laser, {{ duration: 3, top: '100%', ease: 'power2.inOut' }});
                tl.to(logo, {{ duration: 3, opacity: 1, scale: 1, filter: 'blur(0px)', clipPath: 'inset(0% 0 0 0)', ease: 'power2.inOut' }}, "-=3");
                tl.to(laser, {{ duration: 0.2, opacity: 0 }});
            }}
            window.onload = startCycle;
        """
    }
}

# ─── LAYOUT TEMPLATES ───────────────────────────────────

def layout_hero(tshirt_b64, effect_html, bg):
    bg_css = "background: transparent !important;" if bg == "transparent" else "background: #fff;"
    blobs = "" if bg == "transparent" else """
        <div style="position:absolute;inset:0;z-index:0;opacity:0.5;filter:blur(100px);">
            <div style="position:absolute;top:-10%;left:-10%;width:50%;height:60%;background:#ebf4ff;border-radius:50%;"></div>
            <div style="position:absolute;top:20%;right:-10%;width:40%;height:50%;background:#f3e8ff;border-radius:50%;"></div>
        </div>"""

    return f"""
    <div style="position:relative;width:100%;height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;{bg_css}">
        {blobs}
        <div style="position:relative;z-index:10;display:flex;flex-direction:column;align-items:center;width:100%;max-width:1280px;padding:0 48px;">
            <h1 style="font-size:clamp(2rem,7vw,4.5rem);font-weight:700;text-align:center;letter-spacing:-0.02em;margin-bottom:64px;line-height:1.05;color:#0f172a;">
                Order a transfer<br>in minutes –<br><span style="color:#e91e63;">easy</span> and simple
            </h1>
            <div style="display:flex;align-items:center;justify-content:space-between;width:100%;gap:64px;flex-wrap:wrap;">
                <div><button style="background:#000;color:#fff;padding:16px 32px;border:none;border-radius:999px;font-size:14px;font-weight:700;cursor:pointer;">order DTF transfer →</button></div>
                <div style="flex:1;display:flex;justify-content:center;">
                    <div id="hero-unit" style="position:relative;width:480px;z-index:10;">
                        <div id="shadow" style="position:absolute;bottom:-30px;left:50%;transform:translateX(-50%);width:60%;height:20px;background:rgba(0,0,0,0.05);border-radius:50%;filter:blur(15px);"></div>
                        <img src="data:image/png;base64,{tshirt_b64}" style="width:100%;position:relative;z-index:10;" alt="T-Shirt">
                        <div class="print-area">{effect_html}</div>
                    </div>
                </div>
                <div><p style="font-size:18px;font-weight:700;color:#1e293b;line-height:1.4;">Printivo offers<br>a premium quality<br>at the best price<br>in Canada</p></div>
            </div>
        </div>
        <div id="badge" style="position:absolute;top:10%;right:15%;width:120px;height:120px;background:linear-gradient(135deg,#3f51b5,#e91e63,#ff9800);border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;text-align:center;box-shadow:0 10px 30px rgba(233,30,99,0.4);transform:rotate(15deg);">
            <span style="font-size:14px;font-weight:700;">50% OFF</span>
            <span style="font-size:10px;font-weight:700;text-transform:uppercase;">first order</span>
        </div>
    </div>"""

def layout_studio(tshirt_b64, effect_html, bg):
    return f"""
    <div style="position:fixed;inset:0;background:radial-gradient(circle at center,#f8fafc 0%,#ffffff 100%);z-index:-1;"></div>
    <div style="max-width:900px;width:100%;padding:48px;background:#fff;border-radius:48px;box-shadow:0 25px 50px rgba(0,0,0,0.1);border:1px solid #f8fafc;display:flex;align-items:center;gap:48px;flex-wrap:wrap;">
        <div style="position:relative;width:100%;max-width:400px;aspect-ratio:1;display:flex;align-items:center;justify-content:center;">
            <img src="data:image/png;base64,{tshirt_b64}" style="width:100%;height:100%;object-fit:contain;filter:drop-shadow(0 25px 25px rgba(0,0,0,0.15));" alt="T-Shirt">
            <div class="print-area" style="top:17.5%;">{effect_html}</div>
        </div>
        <div style="flex:1;min-width:200px;">
            <div style="font-size:10px;font-weight:700;letter-spacing:0.4em;color:#38bdf8;margin-bottom:8px;text-transform:uppercase;">NEXUS // DTF_ENGINE</div>
            <h1 style="font-size:2rem;font-weight:700;letter-spacing:-0.02em;margin:0 0 24px;color:#0f172a;line-height:1.2;">PREMIUM<br>FABRICATION</h1>
            <p style="color:#94a3b8;font-size:14px;line-height:1.6;margin-bottom:40px;">Autonomous print visualization module powered by GSAP timeline engine.</p>
        </div>
    </div>"""

# ─── ASSEMBLER ──────────────────────────────────────────

def generate(effect: str, layout: str, bg: str):
    tshirt_b64 = image_to_base64(ASSETS_DIR / "tshirt.png")
    logo_b64 = image_to_base64(ASSETS_DIR / "logo_transparent.png")

    if not tshirt_b64 or not logo_b64:
        print("[!] Missing assets. Aborting.")
        sys.exit(1)

    cfg = EFFECTS[effect]
    effect_html = cfg["elements"].format(logo_b64=logo_b64)

    if layout == "hero":
        body = layout_hero(tshirt_b64, effect_html, bg)
    else:
        body = layout_studio(tshirt_b64, effect_html, bg)

    levitate_js = """
        gsap.to("#hero-unit", { y: -15, duration: 3, ease: "power1.inOut", repeat: -1, yoyo: true });
        gsap.to("#shadow", { scaleX: 0.8, opacity: 0.2, duration: 3, ease: "power1.inOut", repeat: -1, yoyo: true });
        if (document.getElementById('badge')) gsap.to("#badge", { y: -10, rotation: 18, duration: 4, ease: "power1.inOut", repeat: -1, yoyo: true });
    """ if layout == "hero" else ""

    bg_css = "background: transparent !important;" if bg == "transparent" else "background: #fff;"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXUS | {cfg['title']} [{layout.upper()}]</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;700&display=swap" rel="stylesheet">
    <style>
        body, html {{ margin: 0; padding: 0; {bg_css} font-family: 'Outfit', sans-serif; overflow: hidden;
            min-height: 100vh; display: flex; align-items: center; justify-content: center; }}
        .print-area {{
            position: absolute; top: 17.5%%; left: 50%%; width: 33%%; height: 48.5%%;
            transform: translateX(-50%%); pointer-events: none; overflow: visible;
            transform-style: preserve-3d; perspective: 1500px;
        }}
        {cfg['extra_css']}
    </style>
</head>
<body>
    {body}
    <script>
        {levitate_js}
        {cfg['js']}
    </script>
</body>
</html>"""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / f"DTF_{effect}_{layout}.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ DTF [{effect} | {layout} | bg:{bg}] → {out_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NEXUS DTF Builder v2.0")
    parser.add_argument("--effect", choices=list(EFFECTS.keys()), default="peel", help="Animation effect type")
    parser.add_argument("--layout", choices=["hero", "studio"], default="hero", help="Page layout")
    parser.add_argument("--bg", choices=["white", "transparent"], default="white", help="Background type")
    args = parser.parse_args()
    generate(args.effect, args.layout, args.bg)
