"""Motion QA from pixels (lab/hero.html, entrance C): records the entrance frame by frame (CDP screencast, PNG) and looks for
  pop    a 16x16 px tile that changes abruptly (mean |change| > 26/255 per 16 ms) while it was still in the 3 frames
         before and after it, and so were its 8 neighbours (< 5/255 per 16 ms; a moving edge changes the neighbours): something
         jumping in or out, e.g. a sliver of the last letter when a mask
         comes off. (Per 16 ms: the screencast drops frames, and a .6 s fade seen across a 100 ms gap is not a jump.)
  edge   a visible straight border of an effect layer (.smoke): along a side, pixels 2 px inside differ from 2 px outside
         by more than 6/255 along more than a quarter of its length (a real border is a long line; a round object crossing
         the side differs only where its curve does), in more than 2 frames
  order  (smoke versions, run with ?dbg=smoke, which paints the smoke red and the black stage dark blue) a letter whose box
         shows ink before it showed any smoke: the title must come out of the smoke, never ahead of it
  spread (with --origin=SELECTOR, effect painted red by the debug mode) the effect must be born at that element and grow
         out of it: its first red pixels must lie inside the element (within its radius of its centre), and no later frame may
         add red pixels far beyond the farthest red of the frame before (60 px + 600 px/s) — smoke ahead of its front
         --origin=SELECTOR@bottom (or @top/@left/@right): the effect must be born at that point of the element's edge,
         within 60 % of its radius
usage: py -I tools/motion.py [url] --fx=3,5,7,7b,7c,d1,d2,d3 [--dev=d|m|both] [--t=6.5] [--origin=#winIn[@bottom]]
The lab's own controls (label, switch panel) are left out. Crops of every finding go to out/motion/."""
import os, sys, time, base64, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _env
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
args = [a for a in sys.argv[1:] if not a.startswith('--')]
opt = lambda k, d: next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--' + k + '=')), d)
url = args[0] if args else 'file:///' + os.path.join(_env.REPO, 'lab', 'hero.html').replace('\\', '/')
FXS = opt('fx', '3,5,7,7b,7c,d1,d2,d3').split(',')
DEVS = {'d': dict(viewport={'width': 1280, 'height': 620}), 'm': dict(viewport={'width': 360, 'height': 649}, is_mobile=True, has_touch=True)}
devs = list(DEVS) if opt('dev', 'both') == 'both' else [opt('dev', 'd')]
DUR = float(opt('t', '6.5'))
out = os.path.join(_env.OUT, 'motion'); os.makedirs(out, exist_ok=True)
TILE, POP, CALM = 16, 26, 5
ORIGIN = opt('origin', None)
RED = lambda r, g, b_: r - g > 30   # the debug smoke (red over white or over the dark-blue debug stage)
INFO = """()=>{const R=e=>{const r=e.getBoundingClientRect();return [r.left,r.top,r.right,r.bottom]};
 const sm=document.querySelector('.smoke'),skip=[...document.querySelectorAll('.ctl,.lbl')].map(R);
 return {letters:[...document.querySelectorAll('#title .ch')].map(c=>({t:c.textContent,b:R(c)})),
   smoke:sm&&getComputedStyle(sm).display!=='none'?R(sm):null,skip}}"""
total = 0
with sync_playwright() as p:
    b = _env.launch(p, scrollbars=True)
    for dev in devs:
        for fx in FXS:
            ctx = b.new_context(**DEVS[dev]); pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg); frames = []
            def on_frame(ev):
                frames.append((time.time(), ev['data'])); cdp.send('Page.screencastFrameAck', {'sessionId': ev['sessionId']})
            cdp.on('Page.screencastFrame', on_frame)
            q = f"w=C&fx={fx}" + ('&dbg=smoke' if fx.startswith('d') else '')
            pg.goto(url + ('&' if '?' in url else '?') + q)
            pg.wait_for_function('window.gsap&&document.querySelector("#title .ch")&&document.getElementById("stage").style.clipPath', timeout=20000)
            t0 = time.time(); cdp.send('Page.startScreencast', {'format': 'png', 'everyNthFrame': 1})
            info = pg.evaluate(INFO); smoke = None
            sel, _, at = (ORIGIN or '').partition('@')
            org = pg.evaluate(f"""(()=>{{const e=document.querySelector({sel!r});if(!e)return null;const r=e.getBoundingClientRect(),a={at!r};
              const x=a==='left'?r.left:a==='right'?r.right:r.left+r.width/2,y=a==='top'?r.top:a==='bottom'?r.bottom:r.top+r.height/2;
              return [x,y,Math.max(r.width,r.height)/2*(a?.6:1)]}})()""") if ORIGIN else None
            while time.time() - t0 < DUR:
                if smoke is None and fx.startswith('d'):
                    smoke = pg.evaluate(INFO)['smoke']
                pg.wait_for_timeout(150)
            cdp.send('Page.stopScreencast'); ctx.close()
            ims = [(t - t0, Image.open(io.BytesIO(base64.b64decode(d))).convert('RGB')) for t, d in frames]
            if len(ims) < 5:
                print(dev, fx, 'too few frames', len(ims)); continue
            W, H = ims[0][1].size; vw = DEVS[dev]['viewport']['width']; k = W / vw
            skipb = [[v * k for v in r] for r in info['skip']]
            inskip = lambda x, y: any(r[0] - 8 <= x <= r[2] + 8 and r[1] - 8 <= y <= r[3] + 8 for r in skipb)
            # ---- pop: abrupt, isolated change of a tile
            gw, gh = W // TILE, H // TILE
            D = []
            for i in range(1, len(ims)):
                d = ImageChops.difference(ims[i - 1][1], ims[i][1]).convert('L').resize((gw, gh), Image.BOX)
                f = .016 / max(.016, ims[i][0] - ims[i - 1][0])
                D.append([v * f for v in d.getdata()])
            pops = []
            for i in range(len(D)):
                for j, val in enumerate(D[i]):
                    if val <= POP: continue
                    x, y = (j % gw) * TILE + TILE // 2, (j // gw) * TILE + TILE // 2
                    if inskip(x, y): continue
                    # (still around it in time and space: a moving object's edge passing one tile changes its neighbours
                    #  in the frames before and after, a pop does not)
                    gx, gy = j % gw, j // gw
                    nb = [yy * gw + xx for yy in range(max(0, gy - 1), min(gh, gy + 2)) for xx in range(max(0, gx - 1), min(gw, gx + 2))]
                    near = [D[n][m] for n in range(max(0, i - 3), min(len(D), i + 4)) if n != i for m in nb]
                    if near and max(near) < CALM:
                        pops.append((round(ims[i + 1][0], 2), int(x / k), int(y / k), round(val), i))
            # ---- edge: the smoke layer's border
            edges = []
            if smoke:
                L, T, R_, B = [v * k for v in smoke]
                for t, im in ims:
                    px = im.convert('L').load(); bad = []
                    def side(name, pts):
                        ds = [abs(px[a] - px[c]) for a, c in pts if 0 <= a[0] < W and 0 <= c[0] < W and 0 <= a[1] < H and 0 <= c[1] < H]
                        if len(ds) > 20 and sum(1 for d in ds if d > 6) / len(ds) > .25: bad.append(name)
                    side('left', [((int(L) + 2, y), (int(L) - 3, y)) for y in range(int(T), int(B))])
                    side('right', [((int(R_) - 3, y), (int(R_) + 2, y)) for y in range(int(T), int(B))])
                    side('top', [((x, int(T) + 2), (x, int(T) - 3)) for x in range(int(L), int(R_))])
                    side('bottom', [((x, int(B) - 3), (x, int(B) + 2)) for x in range(int(L), int(R_))])
                    if bad: edges.append((round(t, 2), bad))
            # ---- order: ink before smoke, per letter (red smoke)
            order = []
            if fx.startswith('d') and fx != 'd2':
                for L_ in info['letters']:
                    x0, y0, x1, y1 = [int(v * k) for v in L_['b']]
                    t_ink = t_sm = None
                    for t, im in ims:
                        c = im.crop((x0, y0, x1, y1)); n = c.width * c.height or 1
                        ink = sum(1 for r, g, b_ in c.getdata() if max(r, g, b_) < 70 and abs(r - g) < 20) / n
                        sm = sum(1 for r, g, b_ in c.getdata() if RED(r, g, b_)) / n
                        if t_sm is None and sm > .04: t_sm = t
                        if t_ink is None and ink > .05: t_ink = t
                        if t_ink is not None and t_sm is not None: break
                    if t_ink is not None and (t_sm is None or t_ink < t_sm):
                        order.append((L_['t'], round(t_ink, 2), None if t_sm is None else round(t_sm, 2)))
            # ---- spread: born at the origin, growing out of it (red pixels, on a 4× smaller grid)
            spread = []
            if org and fx.startswith('d'):
                import math
                ox, oy, orad = [v * k for v in org]; g4 = 4; prev = None; maxd = None; tprev = None; born = ''
                for t, im in ims:
                    sm_ = im.resize((W // g4, H // g4))
                    red = {(i % sm_.width, i // sm_.width) for i, (r, g, b_) in enumerate(sm_.getdata()) if RED(r, g, b_)}
                    if len(red) >= 5:
                        dist = {q: math.hypot(q[0] * g4 - ox, q[1] * g4 - oy) for q in red}
                        if maxd is None:
                            near = min(dist.values())
                            born = f'born {near / k:.0f}px from the origin point at {t:.2f}s (radius {orad / k:.0f})'
                            if near > orad: spread.append((round(t, 2), born))
                        else:
                            lim = maxd + (60 + 600 * (t - tprev)) * k
                            ahead = [q for q in red - (prev or set()) if dist[q] > lim]
                            if len(ahead) >= 5: spread.append((round(t, 2), f'{len(ahead)} cells ahead of the front ({max(dist[q] for q in ahead) / k:.0f}px vs {maxd / k:.0f}px)'))
                        maxd = max(dist.values()) if maxd is None else max(maxd, max(dist.values()))
                    prev, tprev = red, t
            found = len(pops) + (len(edges) if len(edges) > 2 else 0) + len(order) + len(spread)
            total += found
            msg = []
            if pops: msg.append(f"pop {len(pops)}× e.g. t={pops[-1][0]}s at ({pops[-1][1]},{pops[-1][2]}) Δ{pops[-1][3]}")
            if len(edges) > 2: msg.append(f"edge in {len(edges)} frames ({', '.join(sorted(set(s for _, e in edges for s in e)))}) from {edges[0][0]}s")
            if spread: msg.append(f"spread: {len(spread)}× e.g. t={spread[0][0]}s {spread[0][1]}")
            if order: msg.append(f"order: ink before smoke in {len(order)} letters ({', '.join(f'{o[0]} ink {o[1]}s smoke {o[2]}s' for o in order[:8])})")
            print(f"{dev} {fx}: {len(ims)} frames | " + ('; '.join(msg) if msg else 'clean') + (f' [{born}]' if org and fx.startswith('d') and maxd is not None else ''))
            for n, (t, x, y, val, i) in enumerate(pops[:6]):
                cx, cy = int(x * k), int(y * k); box = (max(0, cx - 60), max(0, cy - 60), min(W, cx + 60), min(H, cy + 60))
                a, c = ims[i][1].crop(box), ims[i + 1][1].crop(box); s2 = Image.new('RGB', (a.width * 2 + 4, a.height), 'magenta')
                s2.paste(a, (0, 0)); s2.paste(c, (a.width + 4, 0)); s2.resize((s2.width * 2, s2.height * 2)).save(os.path.join(out, f'pop_{dev}_{fx}_{n}.png'))
    b.close()
print('findings:', total, '| crops in', out)
