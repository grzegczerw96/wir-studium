"""Do elements overlap while they move? (the main page's hero, or lab/hero.html and its entrances; and the scroll of the window)
Every ~40 ms of an entrance and at 21 scroll positions it reads the live boxes and reports:
  window-letter  the black window (the moving oval, or the O growing) over a visible letter of the title
  note-title     a line of the note over a visible letter
  stripes        a visible letter or note line over a visible stripe
  header         the logo or the menu button over a visible letter or note line
  window-note    the window over the note
  off-screen     a visible letter or note line past the left/right edge
  letter-letter  two visible letters over each other (more than a quarter of the narrower one's width and a third of its
                 height: neighbours touch by the -.04em tracking, lines by the .84 leading — that is not an overlap)
'visible' = turned less than 75° (the flip), opacity of its block above .3 (times data-vis, set by effects that hide text
with a filter or a mask). The O's own window next to its letters is
not an overlap (tolerance 3 px), nor the window over letters that are already fading (scroll: by design, they blur away).
usage: py -I tools/overlap.py [main|lab|url] [--shots] [--w=CDEFG]   (phones and desktops, real scrollbar)"""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _env
from playwright.sync_api import sync_playwright
args = [a for a in sys.argv[1:] if not a.startswith('--')]
url, PR = _env.page(args[0] if args else None)
SHOTS = '--shots' in sys.argv
WS = next((a[4:] for a in sys.argv if a.startswith('--w=')), PR['entrances'])
out = os.path.join(_env.OUT, 'overlap'); os.makedirs(out, exist_ok=True)
READ = r"""()=>{
 const deg=el=>{const v=el.style.getPropertyValue('--rx');return v?Math.abs(parseFloat(v)):0};
 const op=el=>{let o=1;for(let e=el;e&&e!==document.body;e=e.parentElement)o*=+getComputedStyle(e).opacity;return o};
 const box=e=>{const r=e.getBoundingClientRect();return [r.left,r.top,r.right,r.bottom]};
 const st=document.getElementById('stage'),cp=st.style.clipPath||'',sr=st.getBoundingClientRect();
 const m=cp.match(/inset\(([-\d.]+)px ([-\d.]+)px ([-\d.]+)px ([-\d.]+)px round ([-\d.]+)px \/ ([-\d.]+)px\)/);
 const win=m?{b:[sr.left+ +m[4],sr.top+ +m[1],sr.right- +m[2],sr.bottom- +m[3]],rx:+m[5],ry:+m[6]}:null;
 const O=document.getElementById('winIn');const ob=O?box(O):null;
 // (data-vis: effects that hide text with a filter or a mask, not opacity, say how much of it shows)
 const vis=(el,host)=>+(el.dataset.vis??host.dataset.vis??1),T=document.getElementById('title'),N=document.getElementById('note');
 const letters=[...document.querySelectorAll('#title .ch')].map(c=>({c,o:op(c)*vis(c,T)})).filter(x=>deg(x.c)<75&&x.o>.3).map(x=>({t:x.c.textContent,b:box(x.c),o:x.o}));
 const wop=w=>{const ls=w.querySelectorAll('.nl');return (ls.length?Math.max(...[...ls].map(op)):op(w))*vis(w,N)};
 const lines={};document.querySelectorAll('#note .w').forEach(w=>{if(deg(w)>=75||wop(w)<=.3)return;const b=box(w),k=Math.round(b[1]);
   lines[k]=lines[k]?[Math.min(lines[k][0],b[0]),Math.min(lines[k][1],b[1]),Math.max(lines[k][2],b[2]),Math.max(lines[k][3],b[3])]:b});
 const stripes=[...document.querySelectorAll('.stripes i')].filter(i=>op(i)>.3).map(box);
 const hd=document.querySelector('.hd'),head=op(hd)>.3?[box(document.querySelector('.logo')),box(document.querySelector('.dots'))]:[];
 return {win,ob,letters,lines:Object.values(lines),stripes,head,W:document.documentElement.clientWidth,P:window.__o?0:0,titleOp:op(document.getElementById('title'))}}"""
TOL = 3
def inter(a, b, tol=TOL):
    return min(a[2], b[2]) - max(a[0], b[0]) > tol and min(a[3], b[3]) - max(a[1], b[1]) > tol
def in_window(win, b):
    """does box b reach into the window (an inset rect with elliptic corners)?"""
    w = win['b']
    if not inter(w, b): return False
    rx, ry = win['rx'], win['ry']
    if rx < 12 and ry < 12: return True
    # nearest point of b to the window's middle must be inside the ellipse/rounded rect
    cx, cy = (w[0] + w[2]) / 2, (w[1] + w[3]) / 2
    px = min(max(cx, b[0] + TOL), b[2] - TOL); py = min(max(cy, b[1] + TOL), b[3] - TOL)
    hx, hy = (w[2] - w[0]) / 2, (w[3] - w[1]) / 2
    dx, dy = abs(px - cx), abs(py - cy)
    if dx <= hx - rx or dy <= hy - ry: return dx < hx and dy < hy
    ex, ey = (dx - (hx - rx)) / max(rx, 1e-3), (dy - (hy - ry)) / max(ry, 1e-3)
    return ex * ex + ey * ey < 1
def check(s, scrolling):
    bad = []
    win, ob = s['win'], s['ob']
    near_o = win and ob and abs(win['b'][0] - ob[0]) < 4 and abs(win['b'][2] - ob[2]) < 4   # the window is the O itself
    for L in s['letters']:
        # (a letter that is still fading in or out — the blur exit, entrances E/F, letters leaving the O in G — is let off)
        if win and in_window(win, L['b']) and L['o'] >= .95:
            if near_o:
                # the O's neighbours: only if a letter reaches into the oval by more than the tolerance
                shrink = {'b': [win['b'][0] + TOL, win['b'][1] + TOL, win['b'][2] - TOL, win['b'][3] - TOL], 'rx': win['rx'], 'ry': win['ry']}
                if not in_window(shrink, L['b']): continue
            bad.append(('window-letter', L['t']))
        if L['b'][0] < -1 or L['b'][2] > s['W'] + 1: bad.append(('off-screen', L['t']))
        for n in s['lines']:
            if inter(n, L['b']): bad.append(('note-title', L['t']))
        for st in s['stripes']:
            if inter(st, L['b'], 0): bad.append(('stripes', L['t']))
        for h in s['head']:
            if inter(h, L['b']): bad.append(('header', L['t']))
    Ls = s['letters']
    for i in range(len(Ls)):
        for j in range(i + 1, len(Ls)):
            a, c = Ls[i]['b'], Ls[j]['b']
            ow, oh = min(a[2], c[2]) - max(a[0], c[0]), min(a[3], c[3]) - max(a[1], c[1])
            if ow > .25 * min(a[2] - a[0], c[2] - c[0]) and oh > .34 * min(a[3] - a[1], c[3] - c[1]):
                bad.append(('letter-letter', Ls[i]['t'] + Ls[j]['t']))
    for n in s['lines']:
        if win and in_window(win, n) and not scrolling: bad.append(('window-note', ''))
        if n[0] < -1 or n[2] > s['W'] + 1: bad.append(('off-screen', 'note'))
        for st in s['stripes']:
            if inter(st, n, 0): bad.append(('stripes', 'note'))
        for h in s['head']:
            if inter(h, n): bad.append(('header', 'note'))
    return bad
DEV = {'phone 360x649': dict(viewport={'width': 360, 'height': 649}, is_mobile=True, has_touch=True),
       'phone 412x915': dict(viewport={'width': 412, 'height': 915}, is_mobile=True, has_touch=True),
       'tablet 768x1024': dict(viewport={'width': 768, 'height': 1024}, is_mobile=True, has_touch=True),
       'desk 1280x620': dict(viewport={'width': 1280, 'height': 620}),
       'desk 1536x742': dict(viewport={'width': 1536, 'height': 742}),
       'desk 1920x1080': dict(viewport={'width': 1920, 'height': 1080})}
total = 0
with sync_playwright() as p:
    b = _env.launch(p, scrollbars=True)
    for dev, opts in DEV.items():
        ctx = b.new_context(**opts); pg = ctx.new_page(); errs = []
        if PR['init']: pg.add_init_script(PR['init'])
        pg.on('pageerror', lambda e: errs.append(str(e)[:100]))
        for w in WS:
            pg.evaluate('scrollTo(0,0)')   # (a reload keeps the scroll position: start every entrance at the top)
            pg.goto(_env.with_q(url, PR['enter_q'](w)))
            pg.wait_for_function(_env.adapt('window.gsap&&document.querySelector("#title .ch")&&document.getElementById("stage").style.clipPath', PR), timeout=20000)
            t0 = time.time(); found = {}
            while time.time() - t0 < float(next((a[4:] for a in sys.argv if a.startswith("--t=")), "4.8")):
                s = pg.evaluate(_env.adapt(READ, PR)); t = round(time.time() - t0, 2)
                for kind, what in check(s, False):
                    found.setdefault(kind, []).append((t, what))
                    if SHOTS and len(found[kind]) == 1: pg.screenshot(path=os.path.join(out, f"{dev.split()[1]}_{w}_{kind}.png"))
            # the scroll: the window grows to the screen
            scr = {}
            for i in range(21):
                pg.evaluate(f"(()=>{{const h=document.querySelector('.hero');scrollTo(0,(h.offsetHeight-innerHeight)*{i / 20})}})()".replace('.hero', PR['section'])); pg.wait_for_timeout(PR['settle'])
                for kind, what in check(pg.evaluate(_env.adapt(READ, PR)), True):
                    scr.setdefault(kind, []).append((i / 20, what))
            msg = '; '.join(f"{k}: {len(v)}× from {v[0][0]}s ({', '.join(sorted(set(x[1] for x in v)))[:30]})" for k, v in found.items()) or 'clean'
            msg2 = '; '.join(f"{k}: {len(v)}× at P {v[0][0]}–{v[-1][0]} ({', '.join(sorted(set(x[1] for x in v)))[:30]})" for k, v in scr.items()) or 'clean'
            total += len(found) + len(scr)
            print(f'{dev} | entrance {w}: {msg} | scroll: {msg2}')
        if errs: print('  errors', errs[:2])
        ctx.close()
    b.close()
print('kinds of overlap found:', total)
