import base64
import os

def image_to_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_white_laser_inkjet():
    tshirt_path = r"e:\Downloads\--ANTIGRAVITY store\IDE-optimus\PROJECT\frontend\nexus-v2\public\assets\tshirt.png"
    logo_path = r"e:\Downloads\--ANTIGRAVITY store\IDE-optimus\PROJECT\frontend\nexus-v2\public\assets\logo_transparent.png"
    
    tshirt_b64 = image_to_base64(tshirt_path)
    logo_b64 = image_to_base64(logo_path)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXUS | WHITE LASER INKJET SIM</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;600&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <style>
        body {{ background: #ffffff; min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: 'Outfit', sans-serif; overflow: hidden; }}
        .stage {{ position: relative; width: 100%; max-width: 900px; aspect-ratio: 1; background: #fff; display: flex; align-items: center; justify-content: center; }}
        
        /* 🖨️ THE PRINT CARRIAGE UNIT */
        .print-unit {{
            position: absolute;
            top: 17%; 
            left: 50%;
            width: 33%; 
            height: 48%;
            transform: translateX(-50%);
            pointer-events: none;
            overflow: hidden;
            /* background: rgba(0,0,0,0.02); /* Debug: shows the placement rectangle */
        }}

        .carriage {{
            position: absolute;
            width: 50px;
            height: 10px;
            background: #cbd5e1; /* Silver/White metal look */
            border-bottom: 3px solid #ffffff;
            border-radius: 4px;
            z-index: 50;
            opacity: 0;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }}
        
        /* THE WHITE LASER / JET FLARE */
        .white-flare {{
            position: absolute;
            width: 100%; height: 3px;
            background: #ffffff;
            bottom: -3px;
            box-shadow: 0 0 20px #ffffff, 0 0 40px rgba(255,255,255,0.8), 0 0 5px #fff;
            opacity: 0;
        }}

        .logo-print {{
            width: 92%;
            height: 92%;
            margin: 4% auto;
            object-fit: contain;
            mix-blend-mode: multiply;
            clip-path: inset(100% 0 0 0); /* Bottom-up reveal */
            opacity: 1;
            filter: contrast(1.1) brightness(1.05);
        }}

        .status-badge {{
            position: absolute;
            top: 40px;
            left: 40px;
            display: flex;
            align-items: center;
            gap: 12px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 10px;
            color: #94a3b8;
            letter-spacing: 0.1em;
        }}
        
        .dot {{ width: 8px; height: 8px; background: #cbd5e1; border-radius: 50%; }}
        .active-dot {{ background: #10b981; box-shadow: 0 0 10px #10b981; }}

    </style>
</head>
<body>
    <div class="stage">
        <div class="status-badge italic uppercase font-bold">
            <div id="status-dot" class="dot"></div>
            NEXUS // PHOTONIC_STUDIO // V5
        </div>

        <div class="relative w-[85%]">
            <img src="data:image/png;base64,{tshirt_b64}" class="w-full select-none" alt="Macro T-Shirt">
            
            <!-- Centered Print Unit -->
            <div class="print-unit">
                <div class="carriage">
                    <div class="white-flare"></div>
                </div>
                <img id="logo" src="data:image/png;base64,{logo_b64}" class="logo-print block" alt="NEXUS Print">
            </div>
        </div>

        <!-- Inline Controls for ease of use -->
        <div class="absolute bottom-12 right-12 text-right">
            <div id="pass-count" class="text-[9px] font-mono text-slate-300 uppercase tracking-widest mb-4">Pass Count: 000</div>
            <button onclick="startCycle()" id="mainBtn" class="bg-slate-900 text-white px-10 py-5 rounded-3xl text-[10px] uppercase font-bold tracking-[0.2em] hover:bg-slate-800 transition-all shadow-xl active:scale-95">Launch Print</button>
        </div>
    </div>

    <script>
        let running = false;
        function startCycle() {{
            if(running) return;
            running = true;
            
            const btn = document.getElementById('mainBtn');
            const logo = document.getElementById('logo');
            const carriage = document.querySelector('.carriage');
            const flare = document.querySelector('.white-flare');
            const passTxt = document.getElementById('pass-count');
            const dot = document.getElementById('status-dot');

            btn.disabled = true;
            btn.classList.add('opacity-30');
            dot.classList.add('active-dot');
            
            const totalPasses = 24; // High fidelity
            const tl = gsap.timeline({{
                onComplete: () => {{
                    running = false;
                    btn.disabled = false;
                    btn.classList.remove('opacity-30');
                    dot.classList.remove('active-dot');
                    gsap.to(carriage, {{ duration: 0.4, opacity: 0 }});
                }}
            }});

            // Reset
            gsap.set(logo, {{ clipPath: 'inset(100% 0 0 0)', opacity: 1 }});
            gsap.set(carriage, {{ top: '96%', left: '0%', opacity: 1 }});

            // Inkjet Loop
            for (let i = 0; i < totalPasses; i++) {{
                const verticalPos = 96 - (i * (96 / totalPasses));
                const sidePosition = i % 2 === 0 ? '85%' : '2%'; // Swapping sides
                
                tl.to(carriage, {{
                    duration: 0.35,
                    left: sidePosition,
                    top: verticalPos + '%',
                    ease: "power1.inOut",
                    onStart: () => {{
                        passTxt.innerText = "Pass Count: " + (i + 1).toString().padStart(3, '0');
                        gsap.to(flare, {{ duration: 0.1, opacity: 1 }});
                    }},
                    onComplete: () => {{
                         gsap.to(flare, {{ duration: 0.1, opacity: 0 }});
                    }}
                }});

                // Smooth reveal for each pass
                tl.to(logo, {{
                    duration: 0.35,
                    clipPath: `inset(${{verticalPos}}% 0 0 0)`,
                    ease: "none"
                }}, "-=0.35");
            }}
        }}
    </script>
</body>
</html>"""
    
    file_path = r"e:\Downloads\--ANTIGRAVITY store\IDE-optimus\PROJECT\outputs\TShirt_Final_White_Laser.html"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[*] Final White Laser Block created: {file_path}")

if __name__ == "__main__":
    generate_white_laser_inkjet()
