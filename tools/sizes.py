"""Does a layout hold at every window size? Goes through a grid of sizes (widths 320–1920 × heights 500–1080, the real
scrollbar on desktops) in one page, resizing it, and in the settled state checks that the given groups of elements do not
overlap each other, that nothing visible leaves the screen sideways and that nothing scrolls sideways.
usage: py -I tools/sizes.py [main|lab|url] --groups="title=#title .ch;note=#note;stripes=.stripes i;header=.logo,.dots" [--gap=4]
       [--wait=250] [--sizes=WxH,WxH…]
  groups: name=CSS selector; every pair of different groups is checked (boxes of visible elements, more than --gap px into
          each other). Good for any section: list what must stay apart.
  The page should settle by itself after a resize (lab/hero.html: add ?still=1, which skips the entrance).
Output: one line per size with a problem, and a summary of the sizes that pass."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _env
from playwright.sync_api import sync_playwright
args = [a for a in sys.argv[1:] if not a.startswith('--')]
opt = lambda k, d: next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--' + k + '=')), d)
url, PR = _env.page(args[0] if args else None)
if PR is _env.PAGES['lab'] and 'still=1' not in url: url = _env.with_q(url, 'still=1')
groups = dict(g.split('=', 1) for g in opt('groups', f"title=#{PR['title']} .ch;note=#{PR['note']};stripes=.stripes i;header=.logo,.dots").split(';'))
GAP, WAIT = float(opt('gap', '4')), int(opt('wait', '250'))
if opt('sizes', ''):
    SIZES = [tuple(map(int, s.split('x'))) for s in opt('sizes', '').split(',')]
else:
    SIZES = [(w, h) for w in (320, 360, 375, 390, 412, 480, 540, 600, 700, 768, 820, 900, 1000, 1024, 1025, 1100, 1180, 1280, 1366, 1440, 1536, 1680, 1920)
             for h in (500, 568, 620, 700, 768, 850, 900, 1080) if not (w <= 480 and h < 568)]
CHK = """(groups)=>{const W=document.documentElement.clientWidth,res=[];
 if(document.documentElement.scrollWidth>W+1)res.push('sideways scroll '+document.documentElement.scrollWidth+' > '+W);
 const vis=e=>{for(let x=e;x&&x!==document.body;x=x.parentElement){const s=getComputedStyle(x);if(s.display==='none'||s.visibility==='hidden'||+s.opacity<.3)return false}return true};
 const B={};for(const [n,sel] of Object.entries(groups))B[n]=[...document.querySelectorAll(sel)].filter(vis).map(e=>{const r=e.getBoundingClientRect();return [r.left,r.top,r.right,r.bottom]}).filter(b=>b[2]-b[0]>0&&b[3]-b[1]>0);
 for(const [n,bs] of Object.entries(B))bs.forEach(b=>{if(b[0]<-1||b[2]>W+1)res.push(n+' off-screen '+Math.round(b[0])+'..'+Math.round(b[2]))});
 const ns=Object.keys(B);
 for(let i=0;i<ns.length;i++)for(let j=i+1;j<ns.length;j++){let worst=0;
   for(const a of B[ns[i]])for(const c of B[ns[j]]){const ox=Math.min(a[2],c[2])-Math.max(a[0],c[0]),oy=Math.min(a[3],c[3])-Math.max(a[1],c[1]);if(ox>__GAP__&&oy>__GAP__)worst=Math.max(worst,Math.min(ox,oy))}
   if(worst)res.push(ns[i]+' × '+ns[j]+' by '+Math.round(worst)+'px')}
 return [...new Set(res)]}""".replace('__GAP__', str(GAP))
bad = 0
with sync_playwright() as p:
    b = _env.launch(p, scrollbars=True)
    pg = b.new_page(viewport={'width': SIZES[0][0], 'height': SIZES[0][1]})
    if PR['init']: pg.add_init_script(PR['init'])
    # (the main page plays its entrance once, on load: the sizes are checked after it)
    pg.goto(url); pg.wait_for_timeout(3500 if PR is _env.PAGES['lab'] else PR['center_wait'])
    for w, h in SIZES:
        pg.set_viewport_size({'width': w, 'height': h}); pg.wait_for_timeout(WAIT)
        r = pg.evaluate(CHK, groups)
        if r: bad += 1; print(f'{w}x{h}:', '; '.join(r[:5]))
    b.close()
print(f'{len(SIZES) - bad} of {len(SIZES)} sizes clean')
