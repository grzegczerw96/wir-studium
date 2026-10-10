"""Shared setup for the QA tools (see CLAUDE.md, "Kontrola jakości").
WIR_TOOLS (default %LOCALAPPDATA%/wir-tools) holds: pw/ (playwright 1.47 + pillow, installed with pip --target),
lib/ (local copies of gsap, ScrollTrigger, lenis, three) and out/ (screenshots, reports)."""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ENV = os.environ.get('WIR_TOOLS') or os.path.join(os.environ.get('LOCALAPPDATA', '.'), 'wir-tools')
sys.path.insert(0, os.path.join(ENV, 'pw'))
LIB, OUT = os.path.join(ENV, 'lib'), os.path.join(ENV, 'out')
os.makedirs(OUT, exist_ok=True)
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(REPO, 'index.html')
CDN = [('gsap.min.js', r'https://cdnjs[^"]+/gsap\.min\.js'), ('ScrollTrigger.min.js', r'https://cdnjs[^"]+/ScrollTrigger\.min\.js'),
       ('lenis.min.js', r'https://unpkg[^"]+/lenis\.min\.js'), ('three.min.js', r'https://cdn\.jsdelivr[^"]+/three\.min\.js')]
NO_CARRY = "Object.defineProperty(window,'__autoScrolling',{get(){return true},set(v){}})"   # snapping and auto-scroll off

def local_page(src=None, rel=False):
    """our page with the CDN libraries swapped for local files; rel=True → 'lib/…' paths (for the phone's local server)"""
    html = open(src or PAGE, encoding='utf8').read()
    for name, pat in CDN:
        html = re.sub(pat, ('lib/' + name) if rel else 'file:///' + os.path.join(LIB, name).replace('\\', '/'), html)
    if rel:
        out = os.path.join(ENV, 'srv'); os.makedirs(out, exist_ok=True)
        import shutil
        if not os.path.exists(os.path.join(out, 'lib')): shutil.copytree(LIB, os.path.join(out, 'lib'))
        open(os.path.join(out, 'index.html'), 'w', encoding='utf8').write(html); return out
    p = os.path.join(ENV, 'test.html'); open(p, 'w', encoding='utf8').write(html)
    return 'file:///' + p.replace('\\', '/')

def launch(p, scrollbars=False):
    # Playwright's own Chromium does not start on this Windows ("side-by-side" error): use the installed Chrome.
    # scrollbars=True keeps the real 15px scrollbar (Playwright hides it by default, so a layout that counts the window
    # with the scrollbar, e.g. innerWidth, looks right in the tools and wrong in Grzegorz's browser)
    return p.chromium.launch(channel='chrome', args=['--use-gl=angle', '--ignore-gpu-blocklist'],
                             ignore_default_args=['--hide-scrollbars'] if scrollbars else None)

# The pages the hero tools (center, overlap, motion) know: the main page (index.html, the default) and the hero lab
# (lab/hero.html). Their page JS is written with the lab's ids; adapt() swaps in the page's own, so one tool checks both.
PAGES = {
    'lab': dict(title='title', note='note', stage='stage', section='.hero', smoke='.smoke', settle=120, init=None,
                center_q='v=2&f=1&x=1&w=A', center_wait=4000, entrances='CDEFG', motion_t=6.5,
                enter_q=lambda w: 'w=' + w,
                fx_q=lambda fx: f'w=C&fx={fx}' + ('&dbg=smoke' if fx.startswith('d') else '')),
    # (main: the intro's scroll is scrubbed over .6 s, so a position needs a moment to settle, and its carrying of a
    #  slow scroll to the end is switched off; one entrance, C, with the title d3 or ?fx=5)
    'main': dict(title='heroT', note='heroNote', stage='box', section='#intro', smoke='.hero-smoke', settle=800, init=NO_CARRY,
                 center_q='', center_wait=7500, entrances='C', motion_t=7.5,
                 enter_q=lambda w: '',
                 fx_q=lambda fx: '&'.join(x for x in ('fx=5' if fx == '5' else '', 'dbg=smoke' if fx.startswith('d') else '') if x)),
}

def page(arg=None):
    """'main' or nothing: the local index.html with local libraries; 'lab': the local lab/hero.html; a URL: the
    profile by its path → (url, profile)"""
    if arg in (None, 'main'): return local_page(), PAGES['main']
    if arg == 'lab': return 'file:///' + os.path.join(REPO, 'lab', 'hero.html').replace('\\', '/'), PAGES['lab']
    return arg, PAGES['lab' if 'hero.html' in arg else 'main']

def adapt(js, pr):
    """the lab's ids in a tool's page JS → the page's own"""
    for k in ('stage', 'title', 'note'):
        for q in ("'", '"'):
            js = js.replace(f'getElementById({q}{k}{q})', f'getElementById({q}{pr[k]}{q})')
        js = js.replace(f'#{k} ', f'#{pr[k]} ').replace(f"'#{k}'", f"'#{pr[k]}'")
    return js.replace("querySelector('.hero')", f"querySelector('{pr['section']}')").replace("querySelector('.smoke')", f"querySelector('{pr['smoke']}')")

def with_q(url, q):
    return url + (('&' if '?' in url else '?') + q if q else '')
