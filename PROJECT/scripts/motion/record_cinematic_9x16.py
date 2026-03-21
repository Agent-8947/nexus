import asyncio
import os
from playwright.async_api import async_playwright
from pathlib import Path

async def record_mobile_cinematic():
    print("🎬 Initializing NEXUS Cinematic Video Renderer [9:16 MOBILE]...")
    
    project_root = Path("e:/Downloads/--ANTIGRAVITY store/IDE-optimus")
    url = f"file:///{project_root.as_posix()}/PROJECT/outputs/Cinematic_Promo_9x16.html"
    
    output_dir = project_root / "PROJECT" / "outputs" / "videos" / "cinematic_promo"
    os.makedirs(output_dir, exist_ok=True)
    
    async with async_playwright() as p:
        print("[>] Запускаю Chromium (Headless Video Node)...")
        browser = await p.chromium.launch(headless=True)
        
        print("[>] Конфигурация записи: 1080x1920 (Mobile Strict Mode)")
        context = await browser.new_context(
            viewport={"width": 1080, "height": 1920},
            record_video_dir=str(output_dir),
            record_video_size={"width": 1080, "height": 1920}
        )
        page = await context.new_page()
        
        print(f"[>] Загрузка секвенции. URL: {url}")
        
        await page.goto(url)
        
        print("[>] Начата гипер-запись таймлайна GSAP (Длительность: 11 секунд)...")
        await page.wait_for_timeout(11000)
        
        video_path = await page.video.path()
        print(f"[>] Рендеринг завершен, сохраняю файл...")
        
        await context.close()
        await browser.close()
        
        final_path = output_dir / "NEXUS_Legal_DevOps_Promo_Mobile_9x16.webm"
        if final_path.exists():
            final_path.unlink()
            
        os.rename(video_path, final_path)
        
        print(f"[>] Conversion to MP4 initialized...")
        mp4_path = output_dir / "NEXUS_Legal_DevOps_Promo_Mobile_9x16.mp4"
        if mp4_path.exists():
            mp4_path.unlink()
            
        import subprocess
        subprocess.run([
            "ffmpeg", "-y", "-i", str(final_path),
            "-c:v", "libx264", "-preset", "slow", "-crf", "18",
            "-pix_fmt", "yuv420p", str(mp4_path)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Clean up the .webm file
        if final_path.exists():
            final_path.unlink()
        
        print(f"\n[OK] 📱 Mobile Cinematic Promo Rendered in MP4: {mp4_path}")

if __name__ == "__main__":
    asyncio.run(record_mobile_cinematic())
