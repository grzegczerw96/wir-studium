"""Measure a page (the original, cappen.com, or ours) at chosen scroll positions — the source of every number in CLAUDE.md.
usage: py -I tools/probe.py <m|l|d> <url|local> <positions-js> <eval-js | @file.js> [--shots]
  m = phone 375×812, l = phone landscape 844×390, d = desktop 1280×620
  positions-js: JS returning absolute scroll Y values (px), evaluated once after load, e.g. "[0, innerHeight*2]"
  eval-js: JS evaluated at every position (return a string/object); @file.js reads it from a file
The original: its own snapping is switched off with window.main.scroller.stop() (its snapTo then keeps the position);
ours: snapping/auto-scroll off. Letters of the original carry --rotateX in their style, ours --rx."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _env
from playwright.sync_api import sync_playwright
mode, url, posjs, evjs = sys.argv[1:5]
shots = '--shots' in sys.argv
if evjs.startswith('@'): evjs = open(evjs[1:], encoding='utf8').read()
if url == 'local': url = _env.local_page()
SCROLL = """y=>{if(window.main&&window.main.scroller)window.main.scroller.scrollTo(y,{immediate:true,force:true});
  else if(window.__lenis)window.__lenis.scrollTo(y,{immediate:true,force:true});else scrollTo(0,y)}"""
VIEW = {'m': dict(viewport={'width': 375, 'height': 812}, is_mobile=True, has_touch=True),
        'l': dict(viewport={'width': 844, 'height': 390}, is_mobile=True, has_touch=True),
        'd': dict(viewport={'width': 1280, 'height': 620})}[mode]
with sync_playwright() as p:
    b = _env.launch(p); pg = b.new_context(**VIEW).new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
    pg.goto(url, wait_until='load', timeout=60000); pg.wait_for_timeout(1500)
    try: pg.wait_for_function('!window.main || window.main.introFinished', timeout=30000)   # the original's preloader
    except Exception as e: errs.append('intro wait: ' + str(e)[:60])
    pg.wait_for_timeout(1500)
    pg.evaluate('window.main&&window.main.scroller?window.main.scroller.stop():(' + _env.NO_CARRY + ')')
    for i, y in enumerate(pg.evaluate(posjs)):
        pg.evaluate(f'({SCROLL})({y})'); pg.wait_for_timeout(int(os.environ.get('WAIT', '900')))
        print(json.dumps(pg.evaluate(evjs), ensure_ascii=False))
        if shots: pg.screenshot(path=os.path.join(_env.OUT, f'probe_{i:02d}.png'))
    print('errors', errs[:5]); b.close()
