import os
from pathlib import Path

def generate_balenciaga_cinematic():
    print("🎬 NEXUS Design Engine: Balenciaga / Ugly Chic [9:16]...")
    
    project_root = Path("e:/Downloads/--ANTIGRAVITY store/IDE-optimus")
    output_path = project_root / "PROJECT" / "outputs" / "Cinematic_Balenciaga_9x16.html"

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1080, height=1920, initial-scale=1.0">
    <title>untitled document</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    
    <style>
        :root {
            --black: #000000;
            --red: #FF0000;
            --white: #FFFFFF;
            --gray: #F5F5F5;
            --blue-link: #0000EE;
            --purple-link: #551A8B;
        }

        * { 
            box-sizing: border-box; cursor: none !important; 
            border-radius: 0px !important;
        }
        
        body, html { 
            margin: 0; padding: 0; width: 1080px; height: 1920px; 
            background-color: var(--white); overflow: hidden; 
            color: var(--black);
        }

        /* Typography */
        .sans { font-family: Arial, Helvetica, sans-serif; text-transform: lowercase; }
        .serif { font-family: "Times New Roman", Times, serif; }
        .link-text { color: var(--blue-link); text-decoration: underline; }
        .visited-link { color: var(--purple-link); text-decoration: underline; }

        /* Scuffed Layouts */
        .marquee-container {
            width: 100%; overflow: hidden; white-space: nowrap; 
            border-top: 1px dashed var(--black);
            border-bottom: 1px dashed var(--black);
            background: var(--gray); padding: 10px 0;
            position: absolute; z-index: 50;
        }
        .marquee-top { top: 15%; transform: rotate(2deg); }
        .marquee-bottom { bottom: 10%; transform: rotate(-5deg); background: var(--black); color: var(--white); border-color: var(--red); }
        
        .marquee-content {
            display: inline-block; font-size: 3rem; font-family: Arial, Helvetica, sans-serif; text-transform: lowercase;
        }

        .scene { position: absolute; width: 100%; height: 100%; z-index: 10; display: none; }

        /* Borders and Bizarre Boxes */
        .ugly-box {
            border: 1px solid var(--black); background: var(--gray);
            padding: 40px; position: absolute;
        }

        /* SCENE 1 */
        #s1 { display: block; }
        .s1-title { 
            font-size: 14rem; position: absolute; left: -20px; top: 30%; 
            width: 120%; text-align: left; line-height: 0.8; word-wrap: break-word;
        }
        .bg-img-placeholder {
            width: 500px; height: 600px; border: 1px solid var(--black);
            position: absolute; right: 20px; top: 10%;
            display: flex; align-items: center; justify-content: center;
            background: var(--gray); color: var(--red); font-family: Arial;
        }

        /* SCENE 2 */
        #s2 { display: none; padding: 50px; }
        .q-header { font-size: 8rem; margin: 0; position: absolute; top: 150px; left: 50px; }
        .body-text { font-size: 4rem; position: absolute; top: 400px; left: 100px; width: 800px; line-height: 1.2; }
        .error-box { 
            position: absolute; bottom: 300px; right: 50px; width: 600px; 
            background: var(--white); border: 2px solid var(--red); padding: 20px;
            color: var(--red); font-family: Arial; font-size: 2rem;
            text-transform: uppercase;
        }

        /* SCENE 3 */
        #s3 { display: none; }
        .s3-text-1 { font-size: 5.5rem; position: absolute; top: 20%; left: 0; padding: 0 50px; line-height: 1.1; }
        .s3-text-2 { font-size: 5rem; position: absolute; bottom: 25%; right: 50px; width: 800px; background: var(--black); color: var(--white); padding: 40px; line-height: 1.2; border: 1px solid var(--red); }

        /* SCENE 4 */
        #s4 { display: none; align-items: center; justify-content: center; background: var(--gray); }
        .final-logo { font-size: 15rem; border: 1px solid var(--black); padding: 50px; background: var(--white);  transform: rotate(-3deg); }
        .sub-link { font-size: 3rem; margin-top: 50px; position: absolute; bottom: 400px; }
        
        .default-button {
            background-color: #EFEFEF; border: 2px solid #767676; padding: 10px 40px;
            font-family: Arial; font-size: 3rem; color: var(--black);
            position: absolute; top: 50px; right: 50px;
        }

    </style>
</head>
<body>

    <button class="default-button">submit query</button>

    <div class="marquee-container marquee-top">
        <div class="marquee-content" id="mq1">legal devops --- algorithmic pressure --- legal devops --- algorithmic pressure --- legal devops --- algorithmic pressure --- legal devops --- </div>
    </div>
    
    <div class="marquee-container marquee-bottom">
        <div class="marquee-content" id="mq2">system error // mas engine engaged // system error // mas engine engaged // system error // mas engine engaged // system error // </div>
    </div>

    <!-- S1 -->
    <div class="scene" id="s1">
        <div class="bg-img-placeholder serif"> image_missing_12.jpg </div>
        <h1 class="s1-title sans link-text pop1">legal<br>devops.</h1>
    </div>

    <!-- S2 -->
    <div class="scene" id="s2">
        <h1 class="q-header sans visited-link">what is this?</h1>
        <div class="body-text serif pop2">
            a specialized high-tech framework that transforms legal representation into a precise engineering process.<br><br>
            we replace chaotic paperwork with a robust, automated <span class="link-text sans">multi-agent system (mas).</span>
        </div>
        <div class="error-box pop2">
            ⚠ warning: legacy systems obsolete.
        </div>
    </div>

    <!-- S3 -->
    <div class="scene" id="s3">
        <h1 class="q-header sans link-text" style="top:50px;">why do we need it?</h1>
        <div class="serif s3-text-1 pop3">
            to manage dozens of active cases simultaneously without expanding headcount.
        </div>
        
        <div class="serif s3-text-2 pop3">
            <span class="sans" style="color:var(--red);">to strictly enforce accountability </span>
            using relentless, algorithmic pressure that never sleeps.
        </div>
    </div>

    <!-- S4 -->
    <div class="scene" id="s4">
        <div class="final-logo sans link-text pop4">nexus®</div>
        <div class="sub-link sans visited-link pop4">return to homepage (mas_v2026.1)</div>
        <div class="ugly-box pop4" style="bottom: 100px; left: 100px; font-family: monospace; font-size: 2rem;">index.html rendered successfully</div>
    </div>

    <script>
        // 18-SECOND BALENCIAGA TIMELINE
        const tl = gsap.timeline();

        // Infinite Marquees
        gsap.to("#mq1", { x: -2000, duration: 20, repeat: -1, ease: "linear" });
        gsap.to("#mq2", { x: -2000, duration: 15, repeat: -1, ease: "linear" });

        // [0.0 - 3.0s] Scene 1: LEGAL DEVOPS
        tl.fromTo(".pop1", { opacity: 0 }, { opacity: 1, duration: 0.1, stagger: 0.1, ease: "steps(1)" })
          .to(".pop1", { opacity: 0, duration: 0.1, delay: 2.5 })
          .set("#s1", { display: "none" })

        // [3.0 - 9.0s] Scene 2: WHAT IS THIS?
          .set("#s2", { display: "block" })
          // Uncomfortable jump cuts
          .fromTo(".q-header", { opacity: 0, x: -50 }, { opacity: 1, x: 0, duration: 0.1, ease: "steps(1)" })
          .fromTo(".pop2", { opacity: 0 }, { opacity: 1, duration: 0.1, stagger: 0.5, ease: "steps(1)" })
          
          .to(".error-box", { backgroundColor: "var(--red)", color: "var(--white)", duration: 0.1, yoyo: true, repeat: 10, ease: "steps(1)", delay: 1 })
          
          .to("#s2", { opacity: 0, duration: 0.1, delay: 1.0 }) 
          .set("#s2", { display: "none" })

        // [9.0 - 15.0s] Scene 3: WHY DO WE NEED IT?
          .set("#s3", { display: "block" })
          .fromTo("#s3 .q-header", { opacity: 0 }, { opacity: 1, duration: 0.1, ease: "steps(1)" })
          .fromTo(".pop3", { opacity: 0 }, { opacity: 1, duration: 0.1, stagger: 1.5, ease: "steps(1)" }) // long read delays
          .to("#s3", { opacity: 0, duration: 0.1, delay: 2.5 }) 
          .set("#s3", { display: "none" })

        // [15.0 - 18.0s] Scene 4: FINAL LOGO
          .set("#s4", { display: "flex" })
          .fromTo(".pop4", { opacity: 0 }, { opacity: 1, duration: 0.1, stagger: 0.2, ease: "steps(1)" })
          
          // Final scuffed fade
          .to("body", { backgroundColor: "var(--black)", duration: 0.1, delay: 1.5 })
          .to(".scene, .marquee-container, .default-button", { opacity: 0, duration: 0.1 }, "-=0.1");

    </script>
</body>
</html>"""
    
    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Balenciaga / Ugly Chic 18s Promo (9x16) generated: {output_path}")

if __name__ == "__main__":
    generate_balenciaga_cinematic()
