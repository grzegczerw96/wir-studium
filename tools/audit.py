"""Automatic visual audit of the page on many screen sizes (see CLAUDE.md, "Kontrola jakości").
usage: py -I tools/audit.py [--devices quick|phones|all|se,m15,...] [--section #id] [--from N --to N] [--step S] [--src file]
At every stop (snapping and auto-scroll off) it checks:
  overflow  a real (non-fixed) element sticking out sideways
  edge      a thin bright column at ONE side edge, or a bright band at the bottom, next to a dark frame (pixel check)
  overlap   visible text of two different blocks covering each other (text hidden by a clipping box is ignored)
  cut       text running off the left/right edge (the sliding contact line and form lines are exempt)
  clipped   a picture cut by the edge of its clipping box in the middle of the screen (e.g. the manifesto squares)
  bar-*     phones: the same after the screen grows by an address bar (height-only resize)
Flagged stops are saved to OUT/audit_<dev>_<n>.png and composed into OUT/audit_sheet_<dev>.png (one image to review).
Known false alarms: the emulator 4px scrollbar on tablets (right margin of the intro window), the white page margin under the
clients box, the header mid-way through hiding, intro letters hidden behind the black window."""
import os, io, sys, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # (python -I leaves the script's folder out)
import _env
from playwright.sync_api import sync_playwright
from PIL import Image

DEVICES = {  # name: (width, height with the address bar shown, mobile, bar height)
    'se': (320, 568, True, 56), 'm15': (360, 649, True, 56), 'i14': (390, 664, True, 89), 'pixel7': (412, 839, True, 56),
    'land': (844, 390, True, 40), 'ipad': (768, 1024, True, 0), 'ipadpro': (1024, 1366, True, 0),
    'd1025': (1025, 700, False, 0), 'desk': (1280, 620, False, 0), 'd1440': (1440, 900, False, 0), 'd1920': (1920, 1080, False, 0)}
PRESETS = {'quick': ['m15', 'ipad', 'desk'], 'phones': ['se', 'm15', 'i14', 'pixel7'], 'all': list(DEVICES)}
ap = argparse.ArgumentParser(); ap.add_argument('--devices', default='quick'); ap.add_argument('--section')
ap.add_argument('--from', dest='y0', type=float); ap.add_argument('--to', dest='y1', type=float)
ap.add_argument('--step', type=float, default=.5); ap.add_argument('--src'); A = ap.parse_args()
pick = PRESETS.get(A.devices) or A.devices.split(',')
URL = _env.local_page(A.src)

TEXT_JS = r"""(()=>{const W=innerWidth,H=innerHeight,out={overlap:[],cut:[]};const op=new Map();
const opac=e=>{if(!e||e===document.documentElement)return 1;if(op.has(e))return op.get(e);const cs=getComputedStyle(e);
  const v=(cs.visibility==='hidden'?0:+cs.opacity)*opac(e.parentElement);op.set(e,v);return v};
const block=e=>{while(e&&e!==document.body){const d=getComputedStyle(e).display;if(!d.startsWith('inline')&&d!=='contents')return e;e=e.parentElement}return document.body};
const cbm=new Map();const clipBox=e=>{let l=-1e9,r=1e9,t=-1e9,b=1e9;for(let a=e.parentElement;a&&a!==document.body;a=a.parentElement){const cs=getComputedStyle(a);if(cs.overflowX!=='visible'||cs.overflowY!=='visible'){const c=a.getBoundingClientRect();if(cs.overflowX!=='visible'){l=Math.max(l,c.left);r=Math.min(r,c.right)}if(cs.overflowY!=='visible'){t=Math.max(t,c.top);b=Math.min(b,c.bottom)}}}return {l,r,t,b}};const items=[];const tw=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
while(n=tw.nextNode()){if(!n.textContent.trim())continue;const el=n.parentElement;if(!el||el.closest('script,style,.menu:not(.open),.toast,.motion-pill'))continue;
  if(opac(el)<.2)continue;const r=document.createRange();r.selectNodeContents(n);
  // (tight leading: a text rect is the font's full height, about 1.2em, while the lines stand .84em apart; the rects of
  //  neighbouring lines then cover each other though no letters touch — the rect is cut to the line's own height)
  const lh=parseFloat(getComputedStyle(el).lineHeight),cut=q0=>{const h=q0.bottom-q0.top;if(!(lh>0)||h<=lh)return q0;const m=(q0.top+q0.bottom)/2;return {left:q0.left,right:q0.right,top:m-lh/2,bottom:m+lh/2}};
  const cb=clipBox(el);for(const q1 of r.getClientRects()){const q0=cut(q1),q={left:Math.max(q0.left,cb.l),right:Math.min(q0.right,cb.r),top:Math.max(q0.top,cb.t),bottom:Math.min(q0.bottom,cb.b),raw:q1};q.width=q.right-q.left;q.height=q.bottom-q.top;
    if(q.width<3||q.height<4||q.bottom<=0||q.top>=H||q.right<=0||q.left>=W)continue;items.push({q,el,b:block(el)})}}
for(let i=0;i<items.length;i++){const A=items[i];
  if((A.q.raw.left<-1&&A.q.left<1||A.q.raw.right>W+1&&A.q.right>W-1)&&!A.el.closest('.tk-title,.tk-line'))out.cut.push((A.el.textContent||'').trim().slice(0,24)+' ['+Math.round(A.q.left)+'..'+Math.round(A.q.right)+']');
  for(let j=i+1;j<items.length;j++){const B=items[j];if(A.b===B.b||A.b.contains(B.b)||B.b.contains(A.b))continue;
    const x=Math.min(A.q.right,B.q.right)-Math.max(A.q.left,B.q.left),y=Math.min(A.q.bottom,B.q.bottom)-Math.max(A.q.top,B.q.top);
    if(x<=2||y<=2)continue;const s=Math.min(A.q.width*A.q.height,B.q.width*B.q.height);if(x*y<.3*s)continue;
    out.overlap.push((A.el.textContent||'').trim().slice(0,18)+' × '+(B.el.textContent||'').trim().slice(0,18))}}
out.overlap=[...new Set(out.overlap)].slice(0,6);out.cut=[...new Set(out.cut)].slice(0,6);return out})()"""

# pictures that must be either whole or hidden: cut by the edge of a clipping box in the middle of the screen = bug
CLIP_JS = r"""(()=>{const H=innerHeight,W=innerWidth,out=[];
document.querySelectorAll('.thumb,.case .pic,.ab-fig,.ab-vid,.aw-fig,.pr-fig,.cl-box,.tk-line').forEach(el=>{
  const r=el.getBoundingClientRect();if(r.width<4||r.height<4||r.bottom<=0||r.top>=H||r.right<=0||r.left>=W)return;
  if(+getComputedStyle(el).opacity<.2)return;
  let a=el.parentElement;while(a&&a!==document.body){const cs=getComputedStyle(a);if(cs.overflow!=='visible'||cs.overflowY!=='visible'||cs.overflowX!=='visible')break;a=a.parentElement}
  if(!a||a===document.body)return;const c=a.getBoundingClientRect();
  const cuts=[];if(r.top<c.top-1&&r.bottom>c.top+1&&c.top>8)cuts.push('top@'+Math.round(c.top));
  if(r.bottom>c.bottom+1&&r.top<c.bottom-1&&c.bottom<H-8)cuts.push('bottom@'+Math.round(c.bottom));
  if(cuts.length)out.push((el.className||el.tagName).toString().split(' ')[0]+' '+cuts.join(','))});
return [...new Set(out)].slice(0,5)})()"""


OVF_JS = r"""(()=>{const cw=document.documentElement.clientWidth,out=[];
const fixedIn=e=>{for(let a=e;a&&a!==document.body;a=a.parentElement){if(getComputedStyle(a).position==='fixed')return true}return false};
const clipped=e=>{for(let a=e.parentElement;a&&a!==document.body;a=a.parentElement){const cs=getComputedStyle(a);if(cs.overflowX!=='visible')return a}return null};
document.querySelectorAll('body *').forEach(e=>{const r=e.getBoundingClientRect();if(r.width===0||r.right<=cw+.5)return;if(fixedIn(e))return;const c=clipped(e);if(c&&c.getBoundingClientRect().right<=cw+.5)return;
 out.push((e.id?'#'+e.id:'')+'.'+((typeof e.className==='string'?e.className:'').split(' ')[0])+'<'+e.tagName.toLowerCase()+'> '+Math.round(r.left)+'..'+Math.round(r.right))});
return {iw:innerWidth,cw,sw:document.documentElement.scrollWidth,bodySW:document.body.scrollWidth,n:out.length,first:out.slice(0,12),clip:document.getElementById('box').style.clipPath}})()"""
OVF_JS = '(()=>{const o=' + OVF_JS + ';return o.first})()'

def lum(p): return .2126 * p[0] + .7152 * p[1] + .0722 * p[2]

def edges(png, bottom_only=False):
    """thin bright edge next to a dark frame: returns list of 'right', 'left', 'bottom' found"""
    im = Image.open(io.BytesIO(png)).convert('RGB')
    if CW[0]: im = im.crop((0, 0, CW[0], im.size[1]))
    w, h = im.size; px = im.load(); found = []
    def col(x, y0, y1): return [lum(px[x, y]) for y in range(y0, y1, 3)]
    def row(y, x0, x1): return [lum(px[x, y]) for x in range(x0, x1, 3)]
    y0, y1 = int(h * .15), int(h * .85)
    if not bottom_only:
        for side, xe, xi in (('right', w - 2, w - 12), ('left', 1, 11)):
            e, i_ = col(xe, y0, y1), col(xi, y0, y1)
            bad = sum(1 for a, b in zip(e, i_) if a > 200 and b < 40)
            if bad > .3 * len(e): found.append(side)
        if 'left' in found and 'right' in found: found = []   # both sides at once = a window still growing, not a sliver
    e, i_ = row(h - 2, int(w * .1), int(w * .9)), row(h - 16, int(w * .1), int(w * .9))
    bad = sum(1 for a, b in zip(e, i_) if a > 200 and b < 40)
    if bad > .5 * len(e): found.append('bottom')
    return found

def sheet(dev, shots, W, H):
    """all flagged frames of one device in one small image (cheaper to review than many screenshots)"""
    shots = shots[:24]; cw = 220 if W < H else 300; ch = int(cw * H / W); cols = 4 if W < H else 3; rows = (len(shots) + cols - 1) // cols
    im = Image.new('RGB', (cols * (cw + 4), rows * (ch + 4)), (40, 40, 40))
    from PIL import ImageDraw
    d = ImageDraw.Draw(im)
    for i, (y, png) in enumerate(shots[:24]):
        t = Image.open(io.BytesIO(png)).convert('RGB').resize((cw, ch)); x0, y0 = (i % cols) * (cw + 4), (i // cols) * (ch + 4)
        im.paste(t, (x0, y0)); d.rectangle([x0, y0, x0 + 46, y0 + 14], fill=(220, 0, 0)); d.text((x0 + 3, y0 + 2), f'{y:.2f}', fill=(255, 255, 255))
    im.save(os.path.join(_env.OUT, f'audit_sheet_{dev}.png'))

report = {}
CW = [0]
with sync_playwright() as p:
    b = _env.launch(p)
    for dev in pick:
        W, H, mob, bar = DEVICES[dev]
        ctx = b.new_context(viewport={'width': W, 'height': H}, is_mobile=mob, has_touch=mob)
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
        pg.goto(URL); pg.wait_for_timeout(2500)
        pg.evaluate(_env.NO_CARRY)
        total = pg.evaluate('document.documentElement.scrollHeight/innerHeight')
        flags = []; k = 0; shots = []
        y0, y1 = A.y0 or 0.0, A.y1 if A.y1 is not None else total
        if A.section:
            y0, y1 = pg.evaluate(f'(()=>{{const e=document.querySelector("{A.section}"),r=e.getBoundingClientRect(),H=innerHeight;return [Math.max(0,(r.top+scrollY)/H-1),(r.bottom+scrollY)/H]}})()')
        y = y0
        while y <= y1:
            pg.evaluate(f'(()=>{{const t=Math.round({y}*innerHeight);window.__lenis?__lenis.scrollTo(t,{{immediate:true,force:true}}):scrollTo(0,t)}})()')
            pg.wait_for_timeout(450)
            f = []
            CW[0] = pg.evaluate('document.documentElement.clientWidth')
            ov = pg.evaluate(OVF_JS)
            if ov: f.append('overflow: ' + ' | '.join(ov))
            shot = pg.screenshot(); view = shot; e = edges(shot); f += ['edge:' + s for s in e]
            t = pg.evaluate(TEXT_JS)
            if t['overlap']: f.append('overlap: ' + ' | '.join(t['overlap']))
            if t['cut']: f.append('cut: ' + ' | '.join(t['cut']))
            c = pg.evaluate(CLIP_JS)
            if c: f.append('clipped: ' + ' | '.join(c))
            if mob and bar:
                pg.set_viewport_size({'width': W, 'height': H + bar}); pg.wait_for_timeout(250)
                s2 = pg.screenshot(); e2 = edges(s2, bottom_only=True); c2 = pg.evaluate(CLIP_JS)
                if e2: f.append('bar:bottom')
                if c2: f.append('bar-clipped: ' + ' | '.join(c2))
                if e2 or c2: view = s2; open(os.path.join(_env.OUT, f'audit_{dev}_{k:03d}_bar.png'), 'wb').write(s2)
                pg.set_viewport_size({'width': W, 'height': H}); pg.wait_for_timeout(150)
            if f:
                open(os.path.join(_env.OUT, f'audit_{dev}_{k:03d}.png'), 'wb').write(shot)
                flags.append(f'{y:5.2f}  ' + '  ;  '.join(f)); shots.append((y, view))
            y = round(y + (A.step / 5 if y < 2.5 else A.step), 3); k += 1   # the intro changes fast: 5× denser there
        if shots: sheet(dev, shots, W, H)
        report[dev] = {'size': f'{W}x{H}', 'screens': round(total, 1), 'stops': k, 'flags': flags, 'errors': errs[:3]}
        print(f'== {dev} {W}x{H}  {round(total,1)} screens, {k} stops, {len(flags)} flagged' + (f', errors: {errs[:2]}' if errs else ''))
        for line in flags: print('   ' + line)
        ctx.close()
    b.close()
json.dump(report, open(os.path.join(_env.OUT, 'audit.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
