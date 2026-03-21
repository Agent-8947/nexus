import asyncio
import os
from playwright.async_api import async_playwright
from pathlib import Path

async def record_nexus_hero():
    print("STARTING NEXUS HERO RENDERER (9:16)...")
    
    project_root = Path("e:/Downloads/--ANTIGRAVITY store/IDE-optimus")
    url = f"file:///{project_root.as_posix()}/PROJECT/outputs/Nexus_LegalDevOps_Hero.html"
    
    output_dir = project_root / "PROJECT" / "outputs" / "videos"
    os.makedirs(output_dir, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # Defining 9:16 aspect ratio (Mobile Vertical)
        context = await browser.new_context(
            viewport={"width": 1080, "height": 1920},
            record_video_dir=str(output_dir),
            record_video_size={"width": 1080, "height": 1920}
        )
        page = await context.new_page()
        
        await page.goto(url)
        
        print("[>] Capturing 20s Kinetic Timeline (GSAP entrance + Idle Floating)...")
        # Wait for the full entrance to finish (2.5s) + multiple loops (17.5s)
        await asyncio.sleep(20)
        
        # Get the path to the temporary video file
        video_path = await page.video.path()
        print(f"[>] Raw capture complete.")
        
        await context.close()
        await browser.close()
        
        # Pre-cleanup
        webm_path = output_dir / "Nexus_Hero_Promo_9x16.webm"
        if webm_path.exists():
            webm_path.unlink()
            
        os.rename(video_path, webm_path)
        
        print(f"[>] Converting to Premium H.264 MP4 via FFmpeg...")
        mp4_path = output_dir / "Nexus_Hero_Promo_9x16.mp4"
        if mp4_path.exists():
            mp4_path.unlink()
            
        import subprocess
        # Using high-quality settings for premium motion graphics
        subprocess.run([
            "ffmpeg", "-y", "-i", str(webm_path),
            "-c:v", "libx264", "-preset", "slow", "-crf", "18",
            "-pix_fmt", "yuv420p", str(mp4_path)
        ], check=True)
        
        # Cleanup WebM
        if webm_path.exists():
            webm_path.unlink()
        
        print(f"\n[OK] NEXUS Cinematic Hero Rendered: {mp4_path}")

if __name__ == "__main__":
    asyncio.run(record_nexus_hero())
