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

def launch(p):
    # Playwright's own Chromium does not start on this Windows ("side-by-side" error): use the installed Chrome
    return p.chromium.launch(channel='chrome', args=['--use-gl=angle', '--ignore-gpu-blocklist'])
