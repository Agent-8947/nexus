import os
from pathlib import Path

def generate_braun_cinematic():
    print("🎬 NEXUS Design Engine: Dieter Rams / Functionalism [9:16]...")
    
    project_root = Path("e:/Downloads/--ANTIGRAVITY store/IDE-optimus")
    output_path = project_root / "PROJECT" / "outputs" / "Cinematic_Braun_9x16.html"

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1080, height=1920, initial-scale=1.0">
    <title>NEXUS | Dieter Rams / Functionalism 18s</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --braun-bg: #F2F2F2;
            --braun-panel: #E8E8E8;
            --braun-metal: #C2C2C2;
            --braun-orange: #FF5E00;
            --braun-green: #AEC6A6;
            --braun-text: #222222;
            --muted-text: rgba(34, 34, 34, 0.6);
        }

        * { box-sizing: border-box; cursor: none !important; font-family: 'Inter', sans-serif; }
        
        body, html { 
            margin: 0; padding: 0; width: 1080px; height: 1920px; 
            background-color: var(--braun-bg); overflow: hidden; 
            color: var(--braun-text);
            display: flex; align-items: center; justify-content: center;
        }

        /* Appliance Shell (The "Device") */
        .appliance-shell {
            width: 950px; height: 1800px;
            background: var(--braun-panel);
            border-radius: 4rem; /* large curves */
            box-shadow: 
                30px 30px 60px rgba(0,0,0,0.15), 
                -10px -10px 30px rgba(255,255,255,0.8),
                inset 2px 2px 5px rgba(255,255,255,0.7),
                inset -5px -5px 15px rgba(0,0,0,0.05);
            position: relative;
            padding: 80px 60px;
            display: flex; flex-direction: column;
            border: 1px solid rgba(255,255,255,0.5);
        }

        /* Speaker Grill Texture Top */
        .speaker-grill {
            width: 100%; height: 250px;
            background-image: radial-gradient(var(--braun-metal) 15%, transparent 20%);
            background-size: 12px 12px;
            background-position: 0 0, 6px 6px;
            border-radius: 2rem;
            box-shadow: inset 5px 5px 15px rgba(0,0,0,0.1), inset -5px -5px 10px rgba(255,255,255,0.5);
            margin-bottom: 60px;
            position: relative; overflow: hidden;
        }

        /* The Screen / Display Area */
        .display-screen {
            width: 100%; height: 800px;
            background: #dcdcd6; /* LCD-ish off-white */
            border-radius: 1rem;
            box-shadow: inset 10px 10px 20px rgba(0,0,0,0.1), inset -5px -5px 10px rgba(255,255,255,0.8);
            position: relative; overflow: hidden;
            display: flex; flex-direction: column; justify-content: center; padding: 60px;
            border: 4px solid var(--braun-metal);
        }

        /* Typography inside Display */
        .screen-content { position: absolute; width: 100%; height: 100%; top: 0; left: 0; padding: 60px; display: none; flex-direction: column; justify-content: center;}
        
        #s1 { display: flex; text-align: center; align-items: center; }
        .s1-title { font-size: 8rem; font-weight: 700; margin: 0; letter-spacing: -3px; line-height: 0.9;}
        .s1-sub { font-size: 6rem; font-weight: 500; margin-top: 20px; color: var(--braun-orange); }

        .s-head { font-size: 4rem; font-weight: 700; margin-bottom: 40px; color: var(--braun-text); text-transform: uppercase; letter-spacing: -1px; border-bottom: 4px solid var(--braun-text); width: fit-content; padding-bottom: 15px;}
        .s-body { font-size: 3rem; line-height: 1.4; font-weight: 500; color: var(--muted-text); }
        .s-highlight { color: var(--braun-text); font-weight: 700; background: rgba(0,0,0,0.05); padding: 5px 10px; border-radius: 5px;}
        
        .line-wrap { overflow: hidden; margin-bottom: 15px; }
        .anim-line { display: block; transform: translateY(100%); opacity: 0; }

        /* Hardware Controls (Bottom Area) */
        .controls-area {
            display: flex; justify-content: space-between; align-items: flex-end;
            margin-top: auto; padding: 0 20px;
        }

        /* Rotary Dial */
        .dial-group { display: flex; flex-direction: column; align-items: center; }
        .label-tiny { font-size: 1.2rem; text-transform: uppercase; letter-spacing: 4px; font-weight: 700; color: var(--muted-text); margin-bottom: 20px; }
        
        .rotary-dial {
            width: 150px; height: 150px; border-radius: 50%;
            background: conic-gradient(from 0deg, #dcdcdc, #f0f0f0, #dcdcdc);
            border: 1px solid var(--braun-metal);
            box-shadow: 
                15px 15px 25px rgba(0,0,0,0.15), 
                -5px -5px 15px rgba(255,255,255,0.8),
                inset 2px 2px 5px rgba(255,255,255,0.9);
            position: relative; display: flex; align-items: center; justify-content: center;
        }
        .dial-marker {
            width: 8px; height: 30px; background: var(--braun-orange); position: absolute;
            top: 15px; border-radius: 4px;
        }

        /* Master Switch (Orange Button) */
        .switch-group { display: flex; flex-direction: column; align-items: center; }
        .master-switch {
            width: 180px; height: 180px; border-radius: 50%;
            background: var(--braun-orange);
            box-shadow: 
                10px 10px 20px rgba(0,0,0,0.2), 
                -5px -5px 15px rgba(255,255,255,0.6),
                inset 5px 5px 10px rgba(255,255,255,0.4),
                inset -5px -5px 15px rgba(200,50,0,0.5);
            border: 4px solid var(--braun-panel);
            position: relative; transition: all 0.1s ease;
        }
        .master-switch-pressed {
            box-shadow: 
                inset 10px 10px 20px rgba(200,50,0,0.6),
                inset -5px -5px 10px rgba(255,255,255,0.3) !important;
            transform: scale(0.97);
        }

        /* Status LEDs */
        .led-group { display: flex; flex-direction: column; gap: 30px; }
        .led-item { display: flex; align-items: center; }
        .led-light {
            width: 25px; height: 25px; border-radius: 50%;
            background: #aaa; margin-right: 20px;
            box-shadow: inset 2px 2px 5px rgba(0,0,0,0.3);
            border: 2px solid var(--braun-metal);
        }
        .led-on-green { 
            background: var(--braun-green); 
            box-shadow: 0 0 15px var(--braun-green), inset 2px 2px 5px rgba(255,255,255,0.6); 
        }
        .led-on-orange { 
            background: var(--braun-orange); 
            box-shadow: 0 0 15px var(--braun-orange), inset 2px 2px 5px rgba(255,255,255,0.6); 
        }
        .led-label { font-size: 1.1rem; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; color: var(--muted-text); }

        /* Branding */
        .brand-logo { 
            position: absolute; bottom: 80px; left: 50%; transform: translateX(-50%);
            font-size: 2.5rem; font-weight: 700; letter-spacing: 15px; color: var(--braun-metal);
        }

    </style>
</head>
<body>

    <div class="appliance-shell">
        
        <div class="speaker-grill"></div>
        
        <div class="display-screen">
            <!-- Screen 1 -->
            <div class="screen-content" id="s1">
                <h1 class="s1-title pop">LEGAL</h1>
                <h2 class="s1-sub pop" style="margin-top:0;">DEVOPS</h2>
            </div>

            <!-- Screen 2 -->
            <div class="screen-content" id="s2">
                <div class="s-head">WHAT IS THIS?</div>
                <div class="s-body">
                    <div class="line-wrap"><span class="anim-line l2">A specialized high-tech framework</span></div>
                    <div class="line-wrap"><span class="anim-line l2">that transforms legal representation</span></div>
                    <div class="line-wrap"><span class="anim-line l2">into a precise engineering process.</span></div>
                    <br>
                    <div class="line-wrap"><span class="anim-line l2">We replace chaotic paperwork</span></div>
                    <div class="line-wrap"><span class="anim-line l2">with a robust, automated</span></div>
                    <div class="line-wrap"><span class="anim-line l2 s-highlight">Multi-Agent System (MAS).</span></div>
                </div>
            </div>

            <!-- Screen 3 -->
            <div class="screen-content" id="s3">
                <div class="s-head">WHY DO WE NEED IT?</div>
                <div class="s-body">
                    <div class="line-wrap"><span class="anim-line l3">To manage dozens of active cases</span></div>
                    <div class="line-wrap"><span class="anim-line l3">simultaneously without expanding</span></div>
                    <div class="line-wrap"><span class="anim-line l3">headcount.</span></div>
                    <br>
                    <div class="line-wrap"><span class="anim-line l3">To strictly enforce accountability</span></div>
                    <div class="line-wrap"><span class="anim-line l3">using <span class="s-highlight">relentless, algorithmic</span></span></div>
                    <div class="line-wrap"><span class="anim-line l3 s-highlight">pressure</span> that never sleeps.</div>
                </div>
            </div>
            
            <!-- Screen 4 -->
            <div class="screen-content" id="s4" style="align-items: center;">
                <h1 class="s1-title pop" style="font-size: 9rem; border-bottom: 8px solid var(--braun-text); padding-bottom: 2rem;">NEXUS</h1>
                <h2 class="s1-sub pop" style="color:var(--muted-text); letter-spacing: 5px; font-size: 3rem;">MAS_V2026.1</h2>
            </div>
        </div>

        <div class="controls-area">
            
            <div class="dial-group">
                <div class="label-tiny">PROGRAM</div>
                <div class="rotary-dial" id="dial">
                    <div class="dial-marker"></div>
                </div>
            </div>

            <div class="switch-group">
                <div class="label-tiny">EXECUTE</div>
                <div class="master-switch" id="main-btn"></div>
            </div>

            <div class="led-group">
                <div class="led-item">
                    <div class="led-light" id="led-pwr"></div>
                    <div class="led-label">PWR</div>
                </div>
                <div class="led-item">
                    <div class="led-light" id="led-run"></div>
                    <div class="led-label">RUN</div>
                </div>
                <div class="led-item">
                    <div class="led-light" id="led-mas"></div>
                    <div class="led-label">MAS</div>
                </div>
            </div>

        </div>

        <div class="brand-logo">NEXUS</div>
    </div>

    <script>
        // 18-SECOND FUNCTIONALISM TIMELINE
        const tl = gsap.timeline();

        // Mechanical Button Press Simulator Function
        function pressButton() {
            gsap.to("#main-btn", { scale: 0.95, boxShadow: "inset 10px 10px 20px rgba(200,50,0,0.6), inset -5px -5px 10px rgba(255,255,255,0.3)", duration: 0.1 });
            gsap.to("#main-btn", { scale: 1, boxShadow: "10px 10px 20px rgba(0,0,0,0.2), -5px -5px 15px rgba(255,255,255,0.6), inset 5px 5px 10px rgba(255,255,255,0.4), inset -5px -5px 15px rgba(200,50,0,0.5)", duration: 0.1, delay: 0.2 });
        }

        // [0.0 - 2.5s] Boot & Scene 1
        tl.call(pressButton)
          .to("#led-pwr", { className: "led-light led-on-green", duration: 0.1 })
          .fromTo(".pop", { y: 100, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, stagger: 0.2, ease: "power3.out" }, "+=0.3")
          .to("#s1", { opacity: 0, duration: 0.3, delay: 1.0 })
          .set("#s1", { display: "none" })

        // [2.5 - 9.5s] Scene 2 (What is this?) - Turn Dial
          .to("#dial", { rotation: 45, duration: 0.5, ease: "back.out(1.5)" }) // Mechanical dial turn
          .to("#led-run", { className: "led-light led-on-orange", duration: 0.1 }, "-=0.2")
          .set("#s2", { display: "flex" })
          .fromTo(".s-head", { opacity: 0, x: -50 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" })
          .to(".l2", { y: 0, opacity: 1, duration: 0.5, stagger: 0.15, ease: "power2.out" })
          .to("#s2", { opacity: 0, duration: 0.3, delay: 4.5 }) // read time
          .set("#s2", { display: "none" })

        // [9.5 - 15.5s] Scene 3 (Why do we need it?) - Turn Dial Again
          .to("#dial", { rotation: 90, duration: 0.5, ease: "back.out(1.5)" })
          .set("#s3", { display: "flex" })
          .fromTo("#s3 .s-head", { opacity: 0, x: -50 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" })
          .to(".l3", { y: 0, opacity: 1, duration: 0.5, stagger: 0.15, ease: "power2.out" })
          .to("#s3", { opacity: 0, duration: 0.3, delay: 4.0 }) // read time
          .set("#s3", { display: "none" })

        // [15.5 - 18.0s] Scene 4 (Logo Final) - Big Button Press
          .to("#dial", { rotation: 180, duration: 0.5, ease: "power2.inOut" })
          .call(pressButton)
          .to("#led-mas", { className: "led-light led-on-green", duration: 0.1 }, "+=0.1")
          .set("#s4", { display: "flex" })
          .fromTo("#s4 .pop", { scale: 0.9, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.8, stagger: 0.2, ease: "power3.out" })
          
          // Total shutdown sequence
          .to(".led-light", { className: "led-light", duration: 0.1, delay: 1.0 })
          .to("body", { filter: "brightness(0)", duration: 0.3 });

    </script>
</body>
</html>"""
    
    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Braun / Functionalism 18s Promo (9x16) generated: {output_path}")

if __name__ == "__main__":
    generate_braun_cinematic()
