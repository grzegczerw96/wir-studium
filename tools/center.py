"""Is the coil in the middle of the black O? (lab/hero.html, layout 2) — measured from pixels only, never from the page's
own numbers, on several window sizes and pixel densities, with the real scrollbar shown (Playwright hides it by default)
and the mouse parked at the bottom right (the coil once followed the mouse).
usage: py -I tools/center.py [url] [--all]
  url: default the local lab/hero.html; --all also saves a close-up of every case (otherwise only failures)
The oval: dark runs along rows/columns at 42 % of its radius from the middle (clear of the coil); the coil: everything
not black inside the oval. Pass: both centres within 1 % of the O's width (at least 1 css px): the metal's shaded right
edge is darker than the threshold, so a centred coil measures ~0.8 % to the left at every size."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _env
from playwright.sync_api import sync_playwright
from PIL import Image
args = [a for a in sys.argv[1:] if not a.startswith('--')]
url = args[0] if args else 'file:///' + os.path.join(_env.REPO, 'lab', 'hero.html').replace('\\', '/')
SAVE_ALL = '--all' in sys.argv
CASES = [(w, h, d, False) for (w, h) in ((1280, 620), (1366, 768), (1440, 900), (1536, 742), (1920, 1080)) for d in (1, 1.25, 1.5)]
CASES += [(768, 1024, 2, True), (360, 649, 3, True), (412, 915, 2.6, True)]
out = os.path.join(_env.OUT, 'center'); os.makedirs(out, exist_ok=True)
fails = 0
with sync_playwright() as p:
    b = _env.launch(p, scrollbars=True)
    for W, H, dpr, mobile in CASES:
        ctx = b.new_context(viewport={'width': W, 'height': H}, device_scale_factor=dpr, is_mobile=mobile, has_touch=mobile)
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:100]))
        pg.goto(url + ('&' if '?' in url else '?') + 'v=2&f=1&x=1&w=A'); pg.wait_for_timeout(2800)
        if not mobile: pg.mouse.move(W - 40, H - 20)
        pg.wait_for_timeout(1200)
        r = pg.evaluate("(()=>{const r=document.getElementById('winIn').getBoundingClientRect();return [r.left,r.top,r.width,r.height]})()")
        sb = pg.evaluate("innerWidth-document.documentElement.clientWidth")
        f = os.path.join(out, f'{W}x{H}@{dpr}.png'); pg.screenshot(path=f); ctx.close()
        im = Image.open(f).convert('L'); px = im.load(); k = im.width / W
        cx0, cy0, rx0, ry0 = (r[0] + r[2] / 2) * k, (r[1] + r[3] / 2) * k, r[2] / 2 * k, r[3] / 2 * k
        dark = lambda x, y: 0 <= x < im.width and 0 <= y < im.height and px[x, y] < 70
        def run_x(y):
            a = c = int(cx0)
            while dark(a - 1, y): a -= 1
            while dark(c + 1, y): c += 1
            return a, c
        def run_y(x):
            a = c = int(cy0)
            while dark(x, a - 1): a -= 1
            while dark(x, c + 1): c += 1
            return a, c
        rows = [run_x(int(cy0 + s * .42 * ry0)) for s in (-1, 1)]
        cols = [run_y(int(cx0 + s * .42 * rx0)) for s in (-1, 1)]
        ox = sum((a + c) / 2 for a, c in rows) / 2; oy = sum((a + c) / 2 for a, c in cols) / 2
        orx = max(c - a for a, c in rows) / 2 / (1 - .42 ** 2) ** .5; ory = max(c - a for a, c in cols) / 2 / (1 - .42 ** 2) ** .5
        pts = [(x, y) for y in range(int(oy - ory), int(oy + ory)) for x in range(int(ox - orx), int(ox + orx))
               if ((x + .5 - ox) / orx) ** 2 + ((y + .5 - oy) / ory) ** 2 < .7 and px[x, y] >= 70]
        if not pts:
            print(f'{W}x{H}@{dpr}: no coil found'); fails += 1; continue
        xs = [x for x, _ in pts]; ys = [y for _, y in pts]
        dx = ((min(xs) + max(xs) + 1) / 2 - ox) / k; dy = ((min(ys) + max(ys) + 1) / 2 - oy) / k
        tol = max(1, .01 * 2 * orx / k)
        ok = abs(dx) <= tol and abs(dy) <= tol
        fails += not ok
        print(f"{'OK  ' if ok else 'FAIL'} {W}x{H}@{dpr} scrollbar {sb}px | coil - O centre {dx:+.1f} {dy:+.1f} px"
              f" | O {2 * orx / k:.0f}x{2 * ory / k:.0f} (page says {r[2]:.0f}x{r[3]:.0f}) | coil {(max(xs) - min(xs)) / k:.0f}px" + (f' | errors {errs[:2]}' if errs else ''))
        if SAVE_ALL or not ok:
            im.crop((int(ox - orx * 1.4), int(oy - ory * 1.4), int(ox + orx * 1.4), int(oy + ory * 1.4))).save(os.path.join(out, f'O_{W}x{H}@{dpr}.png'))
    b.close()
print('fails', fails, '| crops in', out)
