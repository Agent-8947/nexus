import asyncio
import os
from playwright.async_api import async_playwright
from pathlib import Path

async def record_legal_hero():
    print("🎬 Initializing NEXUS Motion Recorder [LEGAL DEVOPS PURE HERO]...")
    
    # Setup paths
    project_root = Path("e:/Downloads/--ANTIGRAVITY store/IDE-optimus")
    url = f"file:///{project_root.as_posix()}/PROJECT/outputs/Legal_DevOps_Pure_Hero.html"
    
    output_dir = project_root / "PROJECT" / "outputs" / "videos" / "legal_hero"
    os.makedirs(output_dir, exist_ok=True)
    
    async with async_playwright() as p:
        print("[>] Запускаю headless Chromium...")
        browser = await p.chromium.launch(headless=True)
        
        print("[>] Настраиваю запись (1920x1080, 60 FPS target)...")
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(output_dir),
            record_video_size={"width": 1920, "height": 1080}
        )
        page = await context.new_page()
        
        # Инжектируем легкое движение мышью для 3D Float эффекта (параллакс карточек и WebGL)
        print(f"[>] Открываю сцену: {url}")
        await page.goto(url)
        
        print("[>] Записываю анимацию (10 секунд) и эмулирую движение курсора...")
        
        # Делаем пару плавных движений мыши
        await page.mouse.move(960, 540) # Центр
        await page.wait_for_timeout(2000)
        
        await page.mouse.move(500, 300, steps=50) # Влево вверх
        await page.wait_for_timeout(3000)
        
        await page.mouse.move(1400, 800, steps=50) # Вправо вниз
        await page.wait_for_timeout(3000)
        
        await page.mouse.move(960, 540, steps=50) # Обратно в центр
        await page.wait_for_timeout(2000)
        
        video_path = await page.video.path()
        print(f"[>] Сохраняю WebM видео...")
        
        await context.close()
        await browser.close()
        
        final_path = output_dir / "legal_hero_desktop_1080p.webm"
        if final_path.exists():
            final_path.unlink()
            
        os.rename(video_path, final_path)
        
        print(f"[>] Conversion to MP4 initialized...")
        mp4_path = output_dir / "legal_hero_desktop_1080p.mp4"
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
        
        print(f"\n[OK] Video Successfully Rendered in MP4: {mp4_path}")

if __name__ == "__main__":
    asyncio.run(record_legal_hero())
