"""Render assets/images/social-card.png (1200×630, the Open Graph / link-preview image).

The card is laid out as HTML with the site's own fonts and rendered with headless Chromium
(Playwright). Run from the repository root or from tools/:

    python3 tools/social_card.py

Requires: pip install playwright && playwright install chromium (or an installed Chrome at CHROME)."""
import asyncio, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = next(p for p in (os.path.join(HERE, ".."), os.path.join(HERE, "..", "Portfolio")) if os.path.exists(os.path.join(p, "index.html")))
OUT = os.path.join(SITE, "assets", "images", "social-card.png")
CHROME = os.environ.get("CHROME", "/usr/bin/google-chrome")

HEX = []
for row in range(-1, 9):
    for col in range(-1, 14):
        x = 95 * col + (47.5 if row % 2 else 0)
        y = 82 * row
        HEX.append(f'<path d="M{x} {y+55} l27.5-47.6 h55 l27.5 47.6 -27.5 47.6 h-55z"/>')

HTML = f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="file://{os.path.abspath(os.path.join(SITE, 'styles.css'))}">
<style>
  html, body {{ margin: 0; }}
  .card {{ position: relative; width: 1200px; height: 630px; overflow: hidden; color: #eef6f1;
    background: radial-gradient(circle at 78% 22%, rgba(80,170,119,0.16), transparent 30%),
                linear-gradient(135deg, #07100e 0%, #0b1814 58%, #08110f 100%); }}
  .hex {{ position: absolute; inset: 0; fill: none; stroke: rgba(121,227,225,0.085); stroke-width: 1; }}
  .fade {{ position: absolute; inset: 0; background: linear-gradient(90deg, rgba(8,17,15,0.1) 0%, rgba(8,17,15,0) 55%),
           linear-gradient(0deg, #08110f 0%, rgba(8,17,15,0) 45%); }}
  .kicker {{ position: absolute; left: 84px; top: 118px; margin: 0; color: #79e3e1; font-family: var(--mono); font-size: 19px; letter-spacing: 0.3em; text-transform: uppercase; }}
  .kicker::before {{ display: inline-block; width: 34px; height: 1px; margin: 0 16px 6px 0; content: ""; background: currentColor; vertical-align: middle; }}
  h1 {{ position: absolute; left: 80px; top: 178px; margin: 0; font-family: var(--display); font-size: 128px; font-weight: 500; letter-spacing: -0.03em; line-height: 1; }}
  .sub {{ position: absolute; left: 84px; top: 340px; margin: 0; max-width: 1040px; color: #d7e3dd; font-family: var(--text); font-size: 30px; font-weight: 300; letter-spacing: -0.005em; line-height: 1.3; }}
  .sub b {{ color: #eef6f1; font-weight: 400; }}
  .foot {{ position: absolute; left: 84px; right: 84px; bottom: 64px; display: flex; justify-content: space-between; align-items: baseline;
           color: #8f9d97; font-family: var(--mono); font-size: 19px; letter-spacing: 0.14em; text-transform: uppercase; }}
  .foot .url {{ color: #eef6f1; }}
  .rule {{ position: absolute; left: 84px; right: 84px; bottom: 118px; height: 1px; background: rgba(220,245,231,0.17); }}
  .motif {{ position: absolute; right: 92px; top: 92px; }}
</style></head><body>
<div class="card">
  <svg class="hex" viewBox="0 0 1200 630" width="1200" height="630">{''.join(HEX)}</svg>
  <div class="fade"></div>
  <svg class="motif" width="150" height="120" viewBox="0 0 150 120" fill="none">
    <path d="M18 98 L48 46 L104 46 L134 98" stroke="rgba(121,227,225,0.55)" stroke-width="1.6" stroke-dasharray="4 6"/>
    <path d="M48 46 L76 98" stroke="rgba(121,227,225,0.3)" stroke-width="1.2"/>
    <circle cx="48" cy="46" r="4.5" fill="#79e3e1"/><circle cx="104" cy="46" r="4.5" fill="#79e3e1"/>
    <circle cx="18" cy="98" r="3.5" fill="rgba(121,227,225,0.7)"/><circle cx="134" cy="98" r="3.5" fill="rgba(121,227,225,0.7)"/><circle cx="76" cy="98" r="3.5" fill="rgba(121,227,225,0.7)"/>
  </svg>
  <p class="kicker">Theoretical &amp; Computational Quantum Physics</p>
  <h1>Yaman Evkaya</h1>
  <p class="sub"><b>Lattice gauge dynamics</b> · quantum many-body simulation · scientific computing</p>
  <div class="rule"></div>
  <div class="foot"><span class="url">yevkaya.com</span><span>M.Sc. Physics · LMU Munich</span></div>
</div>
</body></html>"""


async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        kw = {"args": ["--no-sandbox"]}
        if os.path.exists(CHROME):
            kw["executable_path"] = CHROME
        b = await p.chromium.launch(**kw)
        pg = await b.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
        await pg.set_content(HTML, wait_until="load")
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(300)
        await pg.screenshot(path=OUT, clip={"x": 0, "y": 0, "width": 1200, "height": 630})
        await b.close()
    try:  # palette-quantise: ~3.5× smaller, visually identical on the dark gradient
        from PIL import Image
        im = Image.open(OUT).convert("RGB")
        im.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).save(OUT, optimize=True)
    except ImportError:
        pass
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    asyncio.run(main())
