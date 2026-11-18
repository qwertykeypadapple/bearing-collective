"""Render hero.html (canvas animation) to a seamless looping MP4 + WebM + poster.

Usage: python3 render.py   (needs the site served at http://localhost:5199)
"""
import base64, pathlib, shutil, subprocess, sys
from playwright.sync_api import sync_playwright

FPS = 30
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "video"
FRAMES = HERE / "frames"
URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5199/video-src/hero.html"

shutil.rmtree(FRAMES, ignore_errors=True)
FRAMES.mkdir()
OUT.mkdir(exist_ok=True)

with sync_playwright() as pw:
    try:
        b = pw.chromium.launch()
    except Exception:  # Python Playwright may expect a different browser build than the one cached
        cached = sorted(pathlib.Path.home().glob(
            "Library/Caches/ms-playwright/chromium-*/chrome-mac*/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"))
        b = pw.chromium.launch(executable_path=str(cached[-1]), args=["--headless=new"])
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto(URL)
    pg.wait_for_function("window.ready === true")
    T = pg.evaluate("window.T")
    n = int(T * FPS)
    for i in range(n):  # frame n would equal frame 0, so stop before it
        data = pg.evaluate(f"(draw({i / FPS}), document.getElementById('c').toDataURL('image/png'))")
        (FRAMES / f"f{i:04d}.png").write_bytes(base64.b64decode(data.split(",", 1)[1]))
    b.close()

src = ["-framerate", str(FPS), "-i", str(FRAMES / "f%04d.png")]
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *src, "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-crf", "20", "-preset", "slow", "-movflags", "+faststart", str(OUT / "hero.mp4")], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *src, "-c:v", "libvpx-vp9", "-b:v", "0",
                "-crf", "34", "-row-mt", "1", "-pix_fmt", "yuv420p", str(OUT / "hero.webm")], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(FRAMES / "f0000.png"),
                "-q:v", "3", str(OUT / "hero-poster.jpg")], check=True)
shutil.rmtree(FRAMES)
print("done", n, "frames ->", OUT)
