import asyncio
import os
from playwright.async_api import async_playwright

def get_latest_folder(base_dir):
    """Find the latest (highest number) existing folder to pair with desktop recording."""
    os.makedirs(base_dir, exist_ok=True)
    existing = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d.isdigit()]
    if not existing:
        num = 1
    else:
        num = max(int(d) for d in existing)
    return os.path.join(base_dir, f"{num:03d}")

async def run():
    async with async_playwright() as p:
        print("[>] Запускаю headless-браузер (Chromium) для мобильного формата...")
        browser = await p.chromium.launch(headless=True)
        
        base_dir = "outputs/videos/"
        output_dir = get_latest_folder(base_dir)
        os.makedirs(output_dir, exist_ok=True)
        print(f"[>] Папка записи: {output_dir}")
        
        # Вертикальный формат 1080 (ширина) x 1920 (высота)
        width, height = 1080, 1920
        
        print(f"[>] Настраиваю запись видео ({width}x{height})...")
        context = await browser.new_context(
            viewport={"width": width, "height": height},
            record_video_dir=output_dir,
            record_video_size={"width": width, "height": height}
        )
        page = await context.new_page()
        
        print(f"[>] Открываю локальный файл Hero-блока...")
        url = "file:///e:/Downloads/--ANTIGRAVITY store/IDE-optimus/PROJECT/military-hero/slider.html"
        await page.goto(url)
        
        print("[>] Идет запись анимации (12 секунд)...")
        await page.wait_for_timeout(12000)
        
        video_path = await page.video.path()
        
        await context.close()
        await browser.close()
        
        final_path = os.path.join(output_dir, "mobile_9x16.webm")
        if os.path.exists(final_path):
            os.remove(final_path)
        os.rename(video_path, final_path)
        
        print(f"\n[OK] Mobile видео сохранено: {final_path}")

if __name__ == "__main__":
    asyncio.run(run())
