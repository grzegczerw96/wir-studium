"""Where is the coil and how big is it? The original (cappen.com, a Spline model in a WebGL canvas) and ours, measured
from pixels: everything but the coil's layer is hidden, and the box of the bright pixels is read at chosen places of the
page. One table, the original next to ours, in px and as a share of the screen.
usage: py -I tools/coil.py [--dev=d|m|both] [--shots]
  places (the same moments in both pages): hero end (the window is the whole screen), manifesto start, footer: three
  points of its last scroll (end − 1 screen, end − .5, the very end)"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _env
from playwright.sync_api import sync_playwright
from PIL import Image
opt = lambda k, d: next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--' + k + '=')), d)
SHOTS = '--shots' in sys.argv
DEVS = {'d': dict(viewport={'width': 1280, 'height': 620}), 'm': dict(viewport={'width': 375, 'height': 812}, is_mobile=True, has_touch=True, device_scale_factor=2)}
devs = list(DEVS) if opt('dev', 'both') == 'both' else [opt('dev', 'd')]
out = os.path.join(_env.OUT, 'coil'); os.makedirs(out, exist_ok=True)
SITES = {
    'cappen': dict(url='https://cappen.com/', init=None,
                   ready='window.main && window.main.introFinished',
                   stop='window.main.scroller.stop()',
                   scroll='y=>window.main.scroller.scrollTo(y,{immediate:true,force:true})',
                   places="""(()=>{const H=innerHeight,top=e=>e.getBoundingClientRect().top+scrollY,h=document.querySelector('.hero'),s=document.querySelector('.sub-hero'),c=document.querySelector('.talk'),
                     max=document.documentElement.scrollHeight-H;
                     return {'hero end':top(h)+h.offsetHeight-H,'manifesto start':top(s),'contact top':top(c),'contact +1.5H':top(c)+1.5*H,'contact +3H':top(c)+3*H,'footer −1H':max-H,'footer −.5H':max-H*.5,'footer end':max}})()""",
                   keep='.scene'),
    'ours': dict(url=None, init=_env.NO_CARRY,
                 ready="document.querySelector('#heroT .ch') && !document.documentElement.classList.contains('wait')",
                 stop='0',
                 scroll='y=>window.__lenis?window.__lenis.scrollTo(y,{immediate:true,force:true}):scrollTo(0,y)',
                 places="""(()=>{const H=innerHeight,top=e=>e.getBoundingClientRect().top+scrollY,h=document.getElementById('intro'),s=document.getElementById('mani'),c=document.getElementById('contact'),
                     max=document.documentElement.scrollHeight-H;
                     return {'hero end':top(h)+h.offsetHeight-H,'manifesto start':top(s),'contact top':top(c),'contact +1.5H':top(c)+1.5*H,'contact +3H':top(c)+3*H,'footer −1H':max-H,'footer −.5H':max-H*.5,'footer end':max}})()""",
                 keep='#box,#stage3'),
}
HIDE = """keep=>{const K=[...document.querySelectorAll(keep)];window.__hid=[];document.querySelectorAll('body *').forEach(e=>{
  if(K.some(k=>k===e||k.contains(e)||e.contains(k)))return;window.__hid.push([e,e.style.getPropertyValue('visibility'),e.style.getPropertyPriority('visibility')]);
  e.style.setProperty('visibility','hidden','important')});
  document.documentElement.style.background=document.body.style.background='#000'}"""
# (the page's own inline visibility comes back as it was: the coil layer of the contact is shown by the page itself)
UNHIDE = "()=>{(window.__hid||[]).forEach(([e,v,p])=>v?e.style.setProperty('visibility',v,p):e.style.removeProperty('visibility'))}"
rows = {}
with sync_playwright() as p:
    b = _env.launch(p, scrollbars=True)
    for dev in devs:
        for site, S in SITES.items():
            pg = b.new_context(**DEVS[dev]).new_page()
            if S['init']: pg.add_init_script(S['init'])
            pg.goto(S['url'] or _env.local_page(), wait_until='load', timeout=90000)
            pg.wait_for_function(S['ready'], timeout=90000); pg.wait_for_timeout(2500)
            pg.evaluate(S['stop'])
            places = pg.evaluate(S['places'])
            W, H = pg.evaluate('[document.documentElement.clientWidth,innerHeight]')
            cur = 0
            for name, y in places.items():
                # (step by a quarter of a screen, as a real scroll: a jump left the original's scrubbed scene in a stale state)
                step = H * .25 * (1 if y >= cur else -1)
                while abs(y - cur) > abs(step):
                    cur += step; pg.evaluate(f"({S['scroll']})({cur})"); pg.wait_for_timeout(70)
                cur = y; pg.evaluate(f"({S['scroll']})({y})"); pg.wait_for_timeout(1800)
                pg.evaluate(f"({HIDE})({json.dumps(S['keep'])})"); pg.wait_for_timeout(250)
                f = os.path.join(out, f"{dev}_{site}_{name.replace(' ', '_').replace('−', 'm')}.png"); pg.screenshot(path=f)
                pg.evaluate(UNHIDE)
                im = Image.open(f).convert('L')
                k = im.width / DEVS[dev]['viewport']['width']
                px = im.load(); xs, ys = [], []
                # (not the scrollbar: only the page's own width)
                for yy in range(0, im.height, 2):
                    for xx in range(0, int(W * k), 2):
                        if px[xx, yy] > 55: xs.append(xx); ys.append(yy)
                if len(xs) < 30:
                    rows.setdefault((dev, name), {})[site] = None; continue
                xs.sort(); ys.sort(); n = len(xs); lo, hi = int(n * .005), int(n * .995) - 1   # (a few stray pixels off)
                bx = [xs[lo] / k, ys[lo] / k, xs[hi] / k, ys[hi] / k]
                rows.setdefault((dev, name), {})[site] = dict(w=bx[2] - bx[0], h=bx[3] - bx[1], cx=(bx[0] + bx[2]) / 2, cy=(bx[1] + bx[3]) / 2, W=W, H=H)
            pg.context.close()
    b.close()
fmt = lambda r: '—' if not r else f"{r['w']:4.0f}×{r['h']:3.0f} px ({r['w'] / max(r['W'], r['H']) * 100:3.0f}% dł. boku) środek {r['cx']:4.0f},{r['cy']:4.0f} ({r['cx'] / r['W'] * 100:3.0f}%, {r['cy'] / r['H'] * 100:3.0f}%)"
for (dev, name), r in rows.items():
    print(f"{dev} {name:16s} | cappen {fmt(r.get('cappen'))} | nasza {fmt(r.get('ours'))}")
print('shots in', out)
