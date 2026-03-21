import os
from pathlib import Path
import random

def generate_ransom_cinematic():
    print("🎬 NEXUS Design Engine: Ransom Dada [9:16]...")
    
    project_root = Path("e:/Downloads/--ANTIGRAVITY store/IDE-optimus")
    output_path = project_root / "PROJECT" / "outputs" / "Cinematic_Ransom_9x16.html"
    
    # Helper to randomize ransom note letters
    def ransom_word(word, base_size=8):
        fonts = ['Special Elite', 'Creepster', 'Staatliches', 'VT323', 'Impact', 'Courier New']
        bgs = ['#f4ecdf', '#e0d8c8', '#d91c1c', '#00ddff', '#ffffff']
        colors = ['#111111', '#111111', '#ffffff', '#111111', '#111111']
        
        html = ""
        for char in word:
            if char == " ":
                html += f'<span style="display:inline-block; width: 2rem;"></span>'
                continue
                
            font = random.choice(fonts)
            bg_idx = random.randint(0, len(bgs)-1)
            bg = bgs[bg_idx]
            color = colors[bg_idx]
            
            # Text transform
            case = random.choice(['uppercase', 'lowercase'])
            rotate = random.uniform(-15, 15)
            scale = random.uniform(0.9, 1.3)
            padding = random.uniform(0.1, 0.4)
            size_offset = random.uniform(-1, 2)
            
            html += f'<span class="r-char" style="font-family: \'{font}\'; background-color: {bg}; color: {color}; text-transform: {case}; transform: rotate({rotate}deg) scale({scale}); padding: {padding}rem; font-size: {base_size + size_offset}rem;">{char}</span>'
            
        return f'<div class="ransom-word">{html}</div>'

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1080, height=1920, initial-scale=1.0">
    <title>NEXUS | Ransom Dada 10s</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Creepster&family=Special+Elite&family=Staatliches&family=VT323&display=swap" rel="stylesheet">
    
    <style>
        :root {{
            --red: #d91c1c;
            --cyan: #00ddff;
            --bg: #f4ecdf;
            --paper: #e0d8c8;
            --ink: #111111;
        }}

        * {{ box-sizing: border-box; cursor: none !important; }}
        
        body, html {{ 
            margin: 0; padding: 0; width: 1080px; height: 1920px; 
            background-color: var(--bg); overflow: hidden; 
            background-image: url('data:image/svg+xml,%3Csvg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="noiseFilter"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23noiseFilter)" opacity="0.15"/%3E%3C/svg%3E');
        }}

        .scene {{ position: absolute; width: 100%; height: 100%; z-index: 10; display: none; }}
        
        /* Ransom Note Style */
        .ransom-word {{ display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 5px; margin-bottom: 2rem; }}
        .r-char {{ 
            display: inline-block; 
            box-shadow: 8px 8px 0px rgba(17,17,17,0.8); /* Hard outset shadow */
            border: 2px solid var(--ink); /* jagged cut look */
            line-height: 1;
            border-radius: 0px !important;
        }}

        /* Tape */
        .tape {{ 
            position: absolute; background: rgba(255, 255, 255, 0.6); 
            box-shadow: 0 1px 3px rgba(0,0,0,0.2); backdrop-filter: opacity(0.5);
            width: 300px; height: 60px; z-index: 50;
            border-left: 2px dashed rgba(0,0,0,0.1); border-right: 2px dashed rgba(0,0,0,0.1);
        }}

        /* Background elements */
        .scratch {{ position: absolute; background: var(--ink); opacity: 0.1; width: 150vw; height: 10px; transform: rotate(45deg); }}
        .scribble-text {{ font-family: 'Special Elite', cursive; color: var(--red); font-size: 5rem; position: absolute; transform: rotate(-15deg); font-weight: bold; mix-blend-mode: multiply; }}

        /* Block containers */
        .cut-box {{ 
            background: var(--paper); border: 10px solid var(--ink); 
            box-shadow: 30px 30px 0 var(--red); padding: 50px; 
            position: absolute; transform-origin: center;
        }}

        /* SCENE 1 */
        #scene-msg {{ display: block; }}
        
        /* SCENE 2 */
        #scene-identity {{ display: none; align-items: center; justify-content: center; flex-direction: column;}}
        
        /* SCENE 3 */
        #scene-action {{ display: none; }}
        
        /* SCENE 4 */
        #scene-end {{ display: none; align-items: center; justify-content: center; }}

    </style>
</head>
<body>
    <div class="scratch" style="top:20%; left:-20%;"></div>
    <div class="scratch" style="top:70%; left:-50%; transform: rotate(-30deg); height: 20px;"></div>

    <div class="scene" id="scene-msg">
        <div class="tape" style="top: 15%; left: 10%; transform: rotate(-10deg);"></div>
        <div class="tape" style="top: 18%; right: -5%; transform: rotate(25deg);"></div>
        
        <div style="position: absolute; top: 25%; width: 100%;" class="msg-block">
            {ransom_word("WE HAVE", 7)}
            {ransom_word("THE", 6)}
            {ransom_word("SYSTEM", 11)}
        </div>
        
        <div class="scribble-text s1" style="top: 60%; left: 15%;">PAY ATTENTION</div>
        <div class="cut-box s2" style="top: 75%; left: 10%; transform: rotate(-5deg); background: var(--ink); border: none; box-shadow: 15px -15px 0 var(--cyan);">
            <div style="color:var(--bg); font-family:'VT323'; font-size:6rem;">NO NEGOTIATIONS</div>
        </div>
    </div>

    <div class="scene" id="scene-identity">
        <div class="tape" style="top: 45%; left: 30%; width: 500px; transform: rotate(2deg);"></div>
        <div class="cut-box" id="id-box" style="transform: rotate(8deg); background: var(--bg);">
            <div style="font-family:'Staatliches'; font-size:12rem; color:var(--ink); line-height: 0.9;">LEGAL</div>
            <div style="font-family:'Creepster'; font-size:15rem; color:var(--red); line-height: 0.9;">DEVOPS</div>
        </div>
        <div class="scribble-text" id="id-scr" style="top: 30%; right: 5%; font-size: 8rem; color:var(--cyan); -webkit-text-stroke: 3px var(--ink);">AUTOMATED</div>
    </div>

    <div class="scene" id="scene-action">
        <div style="position: absolute; top: 10%; width: 100%; text-align:center;">
            {ransom_word("1200X", 10)}
            <div class="tape" style="top: 0%; left: 40%; transform: rotate(-85deg);"></div>
        </div>
        
        <div style="position: absolute; top: 40%; width: 100%; text-align:center;">
            {ransom_word("EFFICIENCY", 9)}
        </div>
        
        <div style="position: absolute; top: 75%; width: 100%; text-align:center;">
            {ransom_word("NOW", 15)}
            <div class="tape" style="bottom: 0%; right: 10%; transform: rotate(45deg);"></div>
        </div>
    </div>

    <div class="scene" id="scene-end">
        <div class="cut-box final-box" style="transform: rotate(-3deg); background: var(--ink); color: var(--paper); border: 5px solid var(--paper); box-shadow: 40px 40px 0 var(--red);">
            <div style="font-family:'Staatliches'; font-size:16rem; letter-spacing: 10px;">NEXUS</div>
            <div style="font-family:'VT323'; font-size:5rem; color:var(--cyan); text-align:center; transform:rotate(-5deg);">MAS ENGINE</div>
        </div>
        <div class="scribble-text final-scr" style="top: 20%; left: 0%; font-size: 15rem; opacity:0.2;">END</div>
        <div class="scribble-text final-scr" style="bottom: 10%; right: 0%; font-size: 8rem; color:var(--ink);">V_2026.1</div>
    </div>

    <script>
        const tl = gsap.timeline();
        
        // --- 0.0s - 3.0s: The Message ---
        tl.fromTo(".r-char", 
            {{ scale: 5, opacity: 0, rotate: "random(-180, 180)" }},
            {{ scale: 1, opacity: 1, rotate: "random(-15, 15)", duration: 0.2, stagger: 0.05, ease: "bounce.out" }}
        )
        .fromTo(".tape", {{ opacity: 0, scale: 2 }}, {{ opacity: 1, scale: 1, duration: 0.1, stagger: 0.2, ease: "steps(1)" }}, "-=1")
        .fromTo(".s1", {{ x: -500, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.1, ease: "steps(1)" }}, "-=0.5")
        .fromTo(".s2", {{ y: 800 }}, {{ y: 0, duration: 0.3, ease: "power4.out" }}, "-=0.2") // Hard slide in
        // Jitter the words
        .to(".msg-block", {{ x: 15, y: -15, duration: 0.05, yoyo:true, repeat:3, ease: "steps(1)" }}, "+=0.3")
        .to("#scene-msg", {{ rotateZ: 90, scale: 3, opacity: 0, duration: 0.3, ease: "power2.in", delay: 0.5 }})

        // --- 3.0s - 6.0s: Target Identity ---
        .set("#scene-identity", {{ display: "flex" }})
        .fromTo("#id-box", 
            {{ scale: 0.1, rotate: -45, opacity: 0 }}, 
            {{ scale: 1.2, rotate: 8, opacity: 1, duration: 0.4, ease: "back.out(1.5)" }}
        )
        // Hard drop shadow slam
        .fromTo("#id-box", {{ boxShadow: "0px 0px 0 var(--cyan)" }}, {{ boxShadow: "50px 50px 0 var(--cyan)", duration: 0.1, ease: "steps(1)" }})
        .fromTo("#id-scr", {{ opacity: 0, scale: 3 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "expo.out" }}, "+=0.2")
        .to(".tape", {{ opacity: 1, duration: 0.1 }})
        .to("#id-box", {{ rotate: -10, duration: 0.05, yoyo:true, repeat: 5, ease:"steps(1)", delay: 0.5 }})
        .to("#scene-identity", {{ x: -1500, duration: 0.3, ease: "power4.in" }})

        // --- 6.0s - 8.5s: Action Demands ---
        .set("#scene-action", {{ display: "block" }})
        .fromTo("#scene-action .r-char", 
            {{ y: -1000, opacity: 0 }},
            {{ y: 0, opacity: 1, duration: 0.3, stagger: 0.02, ease: "power4.out" }}
        )
        .fromTo("#scene-action .tape", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1, stagger:0.1, ease:"steps(1)" }})
        // Quick scaling pulses
        .to("#scene-action .ransom-word", {{ scale: 1.1, duration: 0.1, yoyo:true, repeat: 3, stagger: 0.2 }}, "+=0.3")
        .to("#scene-action", {{ opacity: 0, scale: 0.5, duration: 0.2, ease:"steps(2)", delay:0.3 }})

        // --- 8.5s - 10.0s: The Signature ---
        .set("#scene-end", {{ display: "flex" }})
        .fromTo(".final-box", 
            {{ y: -2000, rotate: 45 }},
            {{ y: 0, rotate: -3, duration: 0.4, ease: "bounce.out" }}
        )
        .fromTo(".final-scr", {{ opacity: 0 }}, {{ opacity: 0.8, duration: 0.1, stagger: 0.2, ease:"steps(1)" }})
        // Final jitter
        .to(".final-box", {{ x: 20, duration: 0.03, yoyo:true, repeat:7 }}, "+=0.5")
        
        // Blank cut at end
        .to("body", {{ backgroundColor: "#000", backgroundImage: "none", duration: 0.1 }}, "+=0.2")
        .to(".scene, .scratch", {{ opacity: 0, duration: 0.1 }}, "-=0.1");

    </script>
</body>
</html>"""
    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Ransom Dada 10s Promo (9x16) generated: {output_path}")

if __name__ == "__main__":
    generate_ransom_cinematic()
