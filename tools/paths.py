"""Rule checks during real wheel scrolling, without screenshots: an in-page recorder samples the state every frame while
the wheel goes down, back up and down again (the bugs that only show after a change of direction), and every frame is
checked against rules taken from CLAUDE.md. Prints the frames that break a rule.
usage: py -I tools/paths.py [d|m] [--src file]
Rules (add new ones to RULES):
  footer-over-form  a letter of the footer title visible (more than 10% turned in) while the form is still above 5% opacity
  title-over-form   phones: the contact line visible while a form box is in
  low-contrast      the contact line, the footer title or an award name on a background with contrast below 3:1"""
import os, sys, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _env
from playwright.sync_api import sync_playwright
ap = argparse.ArgumentParser(); ap.add_argument('mode', nargs='?', default='d'); ap.add_argument('--src'); A = ap.parse_args()
REC = r"""(()=>{const R=window.__rec=[];const form=document.getElementById('tkForm'),title=document.getElementById('tkTitle'),
 ch=[...document.querySelectorAll('#ftTitle .ch')],lines=[...document.querySelectorAll('.tk-line')],H=innerHeight,W=innerWidth;
 const lum=c=>{const m=c.match(/\d+(\.\d+)?/g);if(!m)return 1;const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};return .2126*f(+m[0])+.7152*f(+m[1])+.0722*f(+m[2])};
 const bgAt=el=>{for(let e=el;e;e=e.parentElement){const b=getComputedStyle(e).backgroundColor;if(b&&!/rgba\(.*,\s*0\)$|transparent/.test(b))return b}return 'rgb(252,252,252)'};
 const contrast=el=>{const a=lum(getComputedStyle(el).color),b=lum(bgAt(el));return (Math.max(a,b)+.05)/(Math.min(a,b)+.05)};
 (function f(){if(!window.__recOn)return;const rx=ch.map(c=>parseFloat(c.style.getPropertyValue('--rx'))||-90);
  const tr=title.getBoundingClientRect(),tVis=tr.right>0&&tr.left<W&&tr.bottom>0&&tr.top<H&&+getComputedStyle(title).opacity>.05;
  const fr=form.getBoundingClientRect(),fVis=fr.bottom>0&&fr.top<H;
  R.push({y:+(scrollY/H).toFixed(3),formOp:fVis?+getComputedStyle(form).opacity:0,letters:Math.max(...rx.map(v=>1-Math.abs(v)/90)),
   boxIn:lines.some(l=>{const r=l.getBoundingClientRect();return r.right>0&&r.left<W&&r.bottom>0&&r.top<H}),tVis,
   tC:tVis?+contrast(title).toFixed(2):99,fC:+contrast(document.getElementById('ftTitle')).toFixed(2),
   awC:(()=>{const v=[...document.querySelectorAll('.aw-name')].filter(n=>{const r=n.getBoundingClientRect();return r.bottom>0&&r.top<H&&r.height>4});return v.length?+Math.min(...v.map(contrast)).toFixed(2):99})(),
   awGrey:(()=>{const v=[...document.querySelectorAll('.aw-name')].some(n=>{const r=n.getBoundingClientRect();return r.bottom>8&&r.top<H&&r.height>4});
     const g=+(bgAt(document.querySelector('.aw-name')).match(/\d+/)||[252])[0];return v&&g>70&&g<200})(),
   coilGrey:(()=>{const s=document.getElementById('stage3'),o=+(s.style.opacity||0),g=+(bgAt(document.getElementById('contact')).match(/\d+/)||[0])[0];return o>.25&&g>70})()});requestAnimationFrame(f)})()})()"""
RULES = [
    ('footer-over-form', lambda s: s['letters'] > .1 and s['formOp'] > .05),
    ('title-over-form', lambda s: A.mode == 'm' and s['tVis'] and s['boxIn']),
    ('low-contrast', lambda s: (s['tVis'] and s['tC'] < 3) or (s['letters'] > .1 and s['fC'] < 3) or s.get('awC', 99) < 3),
    ('list-on-grey', lambda s: s.get('awGrey')),     # Grzegorz 10.10.2026: the award list must not sit on the mid-grey of the change
    ('coil-on-grey', lambda s: s.get('coilGrey')),   # the contact coil must not show (over 25%) on a light/mid-grey page
]
VIEW = dict(viewport={'width': 1280, 'height': 620}) if A.mode == 'd' else dict(viewport={'width': 360, 'height': 649}, is_mobile=True, has_touch=True)
with sync_playwright() as p:
    b = _env.launch(p); pg = b.new_context(**VIEW).new_page()
    pg.goto(_env.local_page(A.src)); pg.wait_for_timeout(2500)
    H = pg.evaluate('innerHeight')
    ft = pg.evaluate("(document.getElementById('footer').getBoundingClientRect().top+scrollY)/innerHeight")
    ct = pg.evaluate("(document.getElementById('contact').getBoundingClientRect().top+scrollY)/innerHeight")
    def go(y): pg.evaluate(f"window.__lenis?__lenis.scrollTo({round(y*H)},{{immediate:true,force:true}}):scrollTo(0,{round(y*H)})"); pg.wait_for_timeout(800)
    def wheel(dy, n, ms=35):
        pg.mouse.move(640 if A.mode == 'd' else 180, 300)
        for _ in range(n): pg.mouse.wheel(0, dy); pg.wait_for_timeout(ms)
    go(ct - 2.5); pg.evaluate('window.__recOn=true;' + REC)   # from the award list on
    span = int((ft + 1.6 - ct + 2.5) * H / 100)        # from the award list to deep in the footer
    wheel(100, span); pg.wait_for_timeout(1500)        # down (snapping may carry it)
    wheel(-100, int(1.8 * H / 100)); pg.wait_for_timeout(1500)   # back up to the form
    wheel(100, int(1.2 * H / 100), 60); pg.wait_for_timeout(2500)   # down again, slower
    wheel(-100, int(1.0 * H / 100)); wheel(100, int(1.0 * H / 100)); pg.wait_for_timeout(2500)   # a quick flick up and down
    pg.evaluate('window.__recOn=false'); rec = pg.evaluate('window.__rec'); b.close()
bad = {}
for i, s in enumerate(rec):
    for name, rule in RULES:
        if rule(s): bad.setdefault(name, []).append((i, s))
print(f'{len(rec)} frames recorded, contact at {ct:.2f}, footer at {ft:.2f} screens')
for name, hits in bad.items():
    print(f'!! {name}: {len(hits)} frames, e.g.:')
    for i, s in hits[:: max(1, len(hits) // 6)][:6]: print(f'   frame {i}: {json.dumps(s)}')
if not bad: print('all rules hold')
