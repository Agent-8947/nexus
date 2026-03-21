import asyncio
import os
from playwright.async_api import async_playwright

def get_next_folder(base_dir):
    """Find the next sequential folder number (001, 002, 003...)"""
    os.makedirs(base_dir, exist_ok=True)
    existing = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d.isdigit()]
    next_num = max([int(d) for d in existing], default=0) + 1
    return os.path.join(base_dir, f"{next_num:03d}")

async def run():
    async with async_playwright() as p:
        print("[>] Запускаю headless-браузер (Chromium)...")
        browser = await p.chromium.launch(headless=True)
        
        base_dir = "outputs/videos/"
        output_dir = get_next_folder(base_dir)
        os.makedirs(output_dir, exist_ok=True)
        print(f"[>] Папка записи: {output_dir}")
        
        print("[>] Настраиваю запись видео (1920x1080)...")
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=output_dir,
            record_video_size={"width": 1920, "height": 1080}
        )
        page = await context.new_page()
        
        print(f"[>] Открываю локальный файл Hero-блока...")
        url = "file:///e:/Downloads/--ANTIGRAVITY store/IDE-optimus/PROJECT/military-hero/slider.html"
        await page.goto(url)
        
        print("[>] Идет запись анимации (12 секунд)...")
        await page.wait_for_timeout(12000)
        
        video_path = await page.video.path()
        print(f"[>] Сохраняю видео...")
        
        await context.close()
        await browser.close()
        
        final_path = os.path.join(output_dir, "desktop_16x9.webm")
        if os.path.exists(final_path):
            os.remove(final_path)
        os.rename(video_path, final_path)
        
        print(f"\n[OK] Desktop видео сохранено: {final_path}")

if __name__ == "__main__":
    asyncio.run(run())
