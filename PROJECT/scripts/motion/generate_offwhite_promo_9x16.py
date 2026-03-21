import os
from pathlib import Path

def generate_offwhite_cinematic():
    print("🎬 NEXUS Design Engine: Off-White Industrial Quotes [9:16]...")
    
    project_root = Path("e:/Downloads/--ANTIGRAVITY store/IDE-optimus")
    output_path = project_root / "PROJECT" / "outputs" / "Cinematic_OffWhite_9x16.html"

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1080, height=1920, initial-scale=1.0">
    <title>"MOBILE_PROMO_10S"</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    
    <style>
        :root {
            --off-white: #fefefe;
            --raw-muslin: #e5dfd1;
            --zip-orange: #f47920;
            --ind-green: #00ff00;
            --blueprint: #0000ff;
            --black: #050505;
        }

        * { 
            box-sizing: border-box; cursor: none !important; 
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            text-transform: uppercase;
        }
        
        body, html { 
            margin: 0; padding: 0; width: 1080px; height: 1920px; 
            background-color: var(--raw-muslin); overflow: hidden; 
            color: var(--black);
        }

        /* Labels and Quotes */
        .literal-label {
            font-size: 1.5rem; color: var(--black); opacity: 0.5;
            position: absolute; font-weight: 500; letter-spacing: 2px;
        }

        .quote-text { font-weight: 700; line-height: 0.9; }
        .quote-text::before { content: '"'; }
        .quote-text::after { content: '"'; }

        /* Hazard Stripes */
        .hazard-bar {
            position: absolute; width: 100%; height: 80px;
            background: repeating-linear-gradient(
                -45deg,
                var(--black),
                var(--black) 20px,
                var(--zip-orange) 20px,
                var(--zip-orange) 40px
            );
            z-index: 100; opacity: 0;
        }
        .hazard-top { top: 0; left: 0; }
        .hazard-bottom { bottom: 0; left: 0; }
        
        /* Dashed Cutouts */
        .cutout-box {
            border: 4px dashed var(--black); background: transparent;
            padding: 40px; position: absolute;
        }
        
        /* Hard Shadows */
        .misaligned-shadow {
            box-shadow: 15px 15px 0 var(--blueprint);
        }
        .misaligned-shadow-green {
            box-shadow: -20px 20px 0 var(--ind-green);
        }

        /* Zip Tie */
        .zip-tie {
            width: 300px; height: 40px; background: var(--zip-orange);
            border-radius: 5px; position: absolute; transform: rotate(-15deg);
            display: flex; align-items: center; padding: 0 20px;
            font-size: 1.5rem; font-weight: bold; color: var(--black);
            z-index: 90; box-shadow: 10px 10px 0 rgba(0,0,0,0.3);
            border: 2px solid var(--black);
            opacity: 0;
        }
        .zip-tie::before { 
            content: ''; width: 20px; height: 20px; border-radius: 50%;
            background: var(--off-white); border: 4px solid var(--black); margin-right: 15px;
        }

        .scene { position: absolute; width: 100%; height: 100%; z-index: 10; display: none; }

        /* --- SCENE 1 --- */
        #scene-init { display: block; padding: 100px; }
        .init-box {
            width: 100%; height: 80%; background: var(--off-white);
            border: 6px solid var(--black); padding: 50px;
            display: flex; flex-direction: column; justify-content: center;
        }
        .init-text { font-size: 8rem; margin: 0; opacity: 0; }
        
        /* --- SCENE 2 --- */
        #scene-core { display: none; flex-direction: column; align-items: center; justify-content: center; }
        .hero-bold { font-size: 15rem; color: var(--off-white); background: var(--black); padding: 20px 50px; margin: 20px; opacity: 0; display: inline-block; }
        
        /* --- SCENE 3 --- */
        #scene-data { display: none; align-items: center; justify-content: center;}
        .data-card {
            width: 80%; background: var(--off-white); border: 8px solid var(--black);
            padding: 100px 50px; text-align: center; position: absolute; opacity: 0;
        }
        .data-val { font-size: 12rem; margin: 0;}
        .data-lbl { font-size: 4rem; margin-top: 20px;}

        /* --- SCENE 4 --- */
        #scene-logo { display: none; align-items: center; justify-content: center; background: var(--zip-orange); }
        .final-logo { font-size: 16rem; color: var(--black); margin: 0;}
        .final-box { background: var(--off-white); border: 10px solid var(--black); padding: 50px 100px; display: flex; flex-direction: column; align-items: center;}
        
        /* Universal background markings */
        .bg-cross { position: absolute; width: 50px; height: 50px; opacity: 0.3; }
        .bg-cross::before { content:''; position: absolute; width:100%; height:2px; background:var(--black); top:24px; left:0; }
        .bg-cross::after { content:''; position: absolute; height:100%; width:2px; background:var(--black); left:24px; top:0; }

        .c-tl { top: 50px; left: 50px; }
        .c-tr { top: 50px; right: 50px; }
        .c-bl { bottom: 50px; left: 50px; }
        .c-br { bottom: 50px; right: 50px; }

    </style>
</head>
<body>
    <div class="bg-cross c-tl"></div>
    <div class="bg-cross c-tr"></div>
    <div class="bg-cross c-bl"></div>
    <div class="bg-cross c-br"></div>
    <div class="literal-label" style="top:2rem; left: 50%; transform:translateX(-50%);">"TOP_CENTER"</div>
    <div class="literal-label" style="top:50%; left: -60px; transform:rotate(-90deg) translateY(-50%);">"LEFT_MARGIN_AREA"</div>

    <div class="hazard-bar hazard-top" id="hz-top"></div>
    <div class="hazard-bar hazard-bottom" id="hz-bot"></div>

    <div class="zip-tie" id="zt-1" style="top: 25%; right: -50px;">"ZIP_TIE_1"</div>

    <div class="scene" id="scene-init">
        <div class="init-box misaligned-shadow">
            <div class="literal-label" style="top: 20px; left: 20px;">"BOOT_SEQUENCE"</div>
            <h1 class="quote-text init-text" style="color:var(--blueprint);">SYSTEM</h1>
            <h1 class="quote-text init-text" style="color:var(--black);">PURGE</h1>
            <h1 class="quote-text init-text" style="color:var(--zip-orange); margin-top:100px; font-size: 6rem;">ACTIVE_TRUE</h1>
        </div>
    </div>

    <div class="scene" id="scene-core">
        <div class="literal-label" style="top: 15%; left: 10%;">"MAIN_HEADING_WRAPPER"</div>
        <div class="hero-bold quote-text misaligned-shadow-green" style="transform: rotate(-2deg);">LEGAL</div>
        <div class="hero-bold quote-text misaligned-shadow" style="transform: rotate(3deg); margin-top: 50px;">DEVOPS</div>
        <div class="cutout-box cbox-scene2" style="width: 900px; height: 1000px; top: 25%; left: 90px; z-index: -1;">
            <div class="literal-label" style="bottom: 20px; right: 20px;">"CUT_HERE"</div>
        </div>
    </div>

    <div class="scene" id="scene-data">
        <div class="data-card dc1 misaligned-shadow">
            <div class="literal-label" style="top: 20px; left: 20px;">"DATA_1"</div>
            <h1 class="quote-text data-val">1200X</h1>
            <h2 class="quote-text data-lbl" style="color:var(--blueprint);">EFFICIENCY</h2>
        </div>
        <div class="data-card dc2 misaligned-shadow-green" style="border-color: var(--blueprint);">
            <div class="literal-label" style="top: 20px; left: 20px; color:var(--blueprint);">"DATA_2"</div>
            <h1 class="quote-text data-val">ZERO</h1>
            <h2 class="quote-text data-lbl" style="color:var(--zip-orange);">MISTAKES</h2>
        </div>
    </div>

    <div class="scene" id="scene-logo">
        <div class="literal-label" style="color:var(--off-white); top:300px;">"BRAND_IDENTITY"</div>
        <div class="final-box misaligned-shadow" style="transform: rotate(-5deg); box-shadow: 20px 20px 0 var(--blueprint);">
            <h1 class="quote-text final-logo">NEXUS</h1>
            <h2 class="quote-text" style="font-size:3rem; margin-top:20px; margin-bottom:0; color:var(--ind-green); background:var(--black); padding: 10px 20px;">MAS_V2026.1</h2>
        </div>
        <div class="zip-tie" id="zt-2" style="bottom: 25%; left: -50px; transform: rotate(15deg); background: var(--ind-green);">"SEAL_TAG"</div>
    </div>

    <script>
        const tl = gsap.timeline();
        
        // --- 0.0s - 2.5s: "INIT" ---
        tl.to("#hz-top, #hz-bot", { opacity: 1, duration: 0.1, yoyo:true, repeat:3, ease:"steps(1)" })
          .to("#hz-top, #hz-bot", { opacity: 1, duration: 0.1 })
          .fromTo(".init-text", 
              { y: 50, opacity: 0 }, 
              { y: 0, opacity: 1, duration: 0.3, stagger: 0.3, ease: "power4.out" }
          )
          .to("#zt-1", { opacity: 1, x: -100, duration: 0.3, ease: "back.out(2)" }, "-=0.3")
          
          .to(".init-box", { scale: 0.9, duration: 0.2, yoyo:true, repeat: 1, ease: "steps(1)", delay: 0.8 })
          .to("#scene-init", { x: -1500, duration: 0.4, ease: "power4.in" })
          .to("#zt-1", { opacity: 0, duration: 0.1 }, "-=0.2")

        // --- 2.5s - 5.5s: "MAIN CONTENT" ---
          .set("#scene-core", { display: "flex" })
          .fromTo(".cbox-scene2", { scale: 0.8, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.2, ease: "power2.out" })
          
          // Hard impact popups
          .fromTo(".hero-bold", 
              { scale: 3, opacity: 0 }, 
              { scale: 1, opacity: 1, duration: 0.4, stagger: 0.4, ease: "steps(4)" }
          )
          // Rough jitter
          .to(".hero-bold", { x: 10, y: 10, duration: 0.05, yoyo: true, repeat: 3, ease: "steps(1)", delay: 0.5 })
          .to("#scene-core", { opacity: 0, scale: 1.2, duration: 0.4, ease: "expo.in", delay: 0.2 })

        // --- 5.5s - 8.0s: "DATA CARDS" ---
          .set("#scene-data", { display: "flex" })
          // Swap background color dynamically
          .to("body", { backgroundColor: "var(--off-white)", duration: 0.1 })
          .to("#hz-top, #hz-bot", { filter: "invert(1)", duration: 0.1 }, "-=0.1")
          
          .fromTo(".dc1", 
              { y: -1500, rotateZ: -10 },
              { y: -100, rotateZ: -5, opacity: 1, duration: 0.4, ease: "bounce.out" }
          )
          .fromTo(".dc2", 
              { y: 1500, rotateZ: 10 },
              { y: 100, rotateZ: 5, opacity: 1, duration: 0.4, ease: "bounce.out", delay: 0.5 }
          )
          .to(".dc1, .dc2", { scale: 0.5, opacity: 0, duration: 0.3, ease: "back.in(2)", delay: 0.5 })

        // --- 8.0s - 10.0s: "LOGO" ---
          .set("#scene-logo", { display: "flex" })
          .to("body", { backgroundColor: "var(--zip-orange)", duration: 0.1 })
          .to("#hz-top, #hz-bot", { filter: "none", opacity: 0, duration: 0.1 }, "-=0.1") // hide hazards
          
          .fromTo(".final-box", 
              { scale: 0.1, opacity: 0 },
              { scale: 1, opacity: 1, duration: 0.5, ease: "elastic.out(1, 0.4)" }
          )
          .to("#zt-2", { opacity: 1, x: 100, duration: 0.3, ease: "back.out(2)" }, "-=0.2")
          
          // Slight mechanical shakes
          .to(".final-box", { rotation: -3, duration: 0.1, yoyo:true, repeat:5, ease:"steps(1)", delay: 0.5 })

          // End Cut
          .to("body", { backgroundColor: "var(--black)", duration: 0.1, delay: 0.3 })
          .to(".scene, .literal-label, .bg-cross, .zip-tie", { opacity: 0, duration: 0.1 }, "-=0.1");

    </script>
</body>
</html>"""
    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Off-White / Quotes 10s Promo (9x16) generated: {output_path}")

if __name__ == "__main__":
    generate_offwhite_cinematic()
