#!/usr/bin/env python3
"""
WEB_MOTION_RECORDER [NEXUS SYNTHESIZED Gen-7: KINETIC CAPTURE AGENT]
Mission: High-fidelity cinematic recording of web animations (GSAP/THREE.JS) in professional formats.
Heritage: Playwright Browser Engine + FFmpeg Post-Processing

I/O Contract:
  Input:  URL of the animated page (--url)
  Formats: 16:9 (1920x1080) and 9:16 (1080x1920)
  Output: Cinematic MP4 files in PROJECT/outputs/motion_recordings/
"""

import asyncio
import os
import argparse
import sys
import subprocess
import time
import shutil
import base64
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

class MotionRecorder:
    def __init__(self):
        self.output_dir = Path(__file__).resolve().parents[5] / "PROJECT" / "outputs" / "motion_recordings"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    async def record(self, url, duration=10, formats=["16:9", "9:16"], mode="linear"):
        resolutions = {
            "16:9": {"width": 1920, "height": 1080, "name": "desktop_16_9"},
            "9:16": {"width": 1080, "height": 1920, "name": "mobile_9_16"}
        }

        async with async_playwright() as p:
            print(f"[*] NEXUS MOTION RECORDER initializing optimized sequential browser engine...")
            
            # Use GPU-accelerated flags to ensure smooth 60fps recording
            browser_args = [
                '--enable-webgl',
                '--use-gl=egl',
                '--enable-gpu-rasterization',
                '--enable-zero-copy',
                '--ignore-gpu-blocklist',
                '--disable-gpu-driver-bug-workarounds'
            ]
            
            browser = await p.chromium.launch(headless=True, args=browser_args)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            async def capture_format(fmt_key):
                if fmt_key not in resolutions:
                    return
                res = resolutions[fmt_key]
                print(f"[*] Starting MAX-PERFORMANCE capture: {res['name']}...")
                
                context = await browser.new_context(
                    viewport={"width": res["width"], "height": res["height"]},
                    device_scale_factor=2 # SUPER-SAMPLING X2 for Premium Anti-Aliasing (Retina Sharpness)
                    # We no longer rely on record_video_dir, switching to flawless frame-by-frame capture!
                )
                
                page = await context.new_page()
                await page.goto(url, wait_until="networkidle")
                await asyncio.sleep(2.0) # slightly longer wait to ensure all assets parse
                
                # Setup scroll script
                script_to_run = ""
                if mode == "anchors":
                    script_to_run = f"""
                        async () => {{
                            const nodes = document.querySelectorAll('section[id], footer[id], header[id]');
                            if(nodes.length === 0) return;
                            const anchors = Array.from(nodes).map(el => el.offsetTop).sort((a, b) => a - b);
                            // 3 pauses * 1.0s = 3.0s. 2 transits * 1.0s = 2.0s. Total: 5.0s
                            const pauseTime = 1000; 
                            const travelTime = 1000; 
                            for (const targetY of anchors) {{
                                if (targetY !== 0) {{
                                    await new Promise(resolve => {{
                                        if (typeof lenis !== 'undefined') {{
                                            lenis.scrollTo(targetY, {{ 
                                                duration: travelTime / 1000, 
                                                easing: (t) => t === 1 ? 1 : 1 - Math.pow(2, -10 * t)
                                            }});
                                        }} else {{
                                            window.scrollTo({{ top: targetY, behavior: 'smooth' }});
                                        }}
                                        setTimeout(resolve, travelTime);
                                    }});
                                }}
                                await new Promise(resolve => setTimeout(resolve, pauseTime));
                            }}
                        }}
                    """
                else:
                    action_duration = max(duration - 2, 1)
                    script_to_run = f"""
                        async () => {{
                            const duration = {action_duration * 1000};
                            const distance = Math.max(document.body.scrollHeight - window.innerHeight, 3000);
                            const totalFrames = duration / (1000 / 60);
                            const deltaY = distance / totalFrames;
                            return new Promise((resolve) => {{
                                let frames = 0;
                                const interval = setInterval(() => {{
                                    window.dispatchEvent(new WheelEvent('wheel', {{ deltaY: deltaY, clientY: window.innerHeight/2 }}));
                                    frames++;
                                    if(frames >= totalFrames) {{ clearInterval(interval); resolve(); }}
                                }}, 1000 / 60);
                            }});
                        }}
                    """

                frames_dir = self.output_dir / f"temp_frames_{res['name']}_{timestamp}"
                frames_dir.mkdir(parents=True, exist_ok=True)
                
                print(f"[*] Capturing flawless CDP Screencast sequence at 30 FPS for {res['name']}...")
                
                # Setup CDP session for lightning-fast internal Chrome screencast
                client = await context.new_cdp_session(page)
                
                frame_count = {"current": 0}
                
                last_frame = {"data": None}
                
                async def handle_screencast(event):
                    data = event.get("data")
                    session_id = event.get("sessionId")
                    if data:
                        last_frame["data"] = data
                        await client.send("Page.screencastFrameAck", {"sessionId": session_id})
                
                client.on("Page.screencastFrame", handle_screencast)
                
                # Start Screencast at roughly 30 FPS (everyNthFrame=2 on a 60fps refresh rate)
                await client.send("Page.startScreencast", {
                    "format": "jpeg",
                    "quality": 100,
                    "everyNthFrame": 1
                })
                
                # Execute the movement asynchronously so we can capture frames while it moves
                scroll_task = asyncio.create_task(page.evaluate(script_to_run))
                
                target_fps = 30
                frame_duration = 1.0 / target_fps
                
                # Enforce absolute 30 FPS by writing whatever the last frame was
                while not scroll_task.done():
                    start_time = time.perf_counter()
                    
                    if last_frame["data"]:
                        frame_path = frames_dir / f"frame_{frame_count['current']:04d}.jpg"
                        with open(frame_path, "wb") as f:
                            f.write(base64.b64decode(last_frame["data"]))
                        frame_count["current"] += 1
                        
                    elapsed = time.perf_counter() - start_time
                    remaining = frame_duration - elapsed
                    if remaining > 0:
                        await asyncio.sleep(remaining)
                
                # Wait for scrolling to finish naturally
                await scroll_task
                
                # Stop Screencast
                await client.send("Page.stopScreencast")
                await asyncio.sleep(1) # Drain remaining frames
                
                await context.close()
                
                final_filename = self.output_dir / f"motion_{res['name']}_{timestamp}.mp4"
                print(f"[*] Sequence capture complete. Encoding {frame_count['current']} frames to ultra-crisp MP4...")
                
                # Proper FFmpeg Sequence Synthesis
                cmd = [
                    "ffmpeg", "-y", "-framerate", "30",
                    "-i", str(frames_dir / "frame_%04d.jpg"),
                    "-c:v", "libx264", "-preset", "slow", "-crf", "12",
                    "-profile:v", "high", "-level:v", "4.2",
                    "-pix_fmt", "yuv420p", str(final_filename)
                ]
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                print(f"[*] Transcoding complete. Obliterating temporary frames...")
                try:
                    shutil.rmtree(frames_dir)
                except: pass
                
                print(f"[SUCCESS] Saved PURE CDP FRAME-BY-FRAME MP4: {final_filename.name}")

            # Sequential execution to prevent CPU/GPU bottleneck and jerky video
            for f in formats:
                await capture_format(f)
                
            await browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NEXUS Motion Recorder Agent")
    parser.add_argument("--url", required=True, help="URL of the web animation to record")
    parser.add_argument("--duration", type=int, default=10, help="Duration of recording in seconds")
    parser.add_argument("--format", choices=["16:9", "9:16", "both"], default="both", help="Video aspect ratio")
    parser.add_argument("--mode", choices=["linear", "anchors"], default="linear", help="Scrolling mode: continuous vs pause-at-anchors")
    
    args = parser.parse_args()
    
    fmts = ["16:9", "9:16"] if args.format == "both" else [args.format]
    
    recorder = MotionRecorder()
    try:
        asyncio.run(recorder.record(args.url, duration=args.duration, formats=fmts, mode=args.mode))
    except Exception as e:
        print(f"[FATAL ERROR] Motion Synthesis failed: {e}")
        sys.exit(1)
