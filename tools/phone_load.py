"""What does the visitor see while the page loads on the real phone? Records the screen frame by frame (CDP screencast)
from a first visit (through about:blank) and saves a strip of frames with their times from the navigation, plus the
moment of the reveal (performance.mark('wir-reveal')) and the first paint. Same set-up as phone.py (USB debugging,
only the tab with our page is touched).
usage: py -I tools/phone_load.py [--local] [--q=fx=5] [--t=4]"""
import os, sys, time, base64, io, subprocess, shutil, threading, functools, http.server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _env
from playwright.sync_api import sync_playwright
from PIL import Image
opt = lambda k, d: next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--' + k + '=')), d)
LOCAL, Q, DUR = '--local' in sys.argv, opt('q', ''), float(opt('t', '4'))
# --letters: does any letter of the title jump? For every letter box, the change between consecutive frames; a jump is a
# frame whose change is many times that of the frames around it. Prints the strongest and saves close-ups (prev/this/next)
LETTERS = '--letters' in sys.argv
ADB = shutil.which('adb') or os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe')
devs = [l.split()[0] for l in subprocess.run([ADB, 'devices'], capture_output=True, text=True).stdout.splitlines()[1:]
        if l.strip().endswith('device') and not l.startswith('emulator')]
if not devs: sys.exit('no phone: plug it in, unlock it and allow USB debugging')
DEV = devs[0]
subprocess.run([ADB, '-s', DEV, 'forward', 'tcp:9222', 'localabstract:chrome_devtools_remote'], capture_output=True)
BASE = 'https://grzegczerw96.github.io/wir-studium/'
if LOCAL:
    root = _env.local_page(rel=True)
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 8765), functools.partial(http.server.SimpleHTTPRequestHandler, directory=root))
    srv.RequestHandlerClass.log_message = lambda *a: None
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    subprocess.run([ADB, '-s', DEV, 'reverse', 'tcp:8765', 'tcp:8765'], capture_output=True); BASE = 'http://127.0.0.1:8765/'
out = os.path.join(_env.OUT, 'phone_load'); os.makedirs(out, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
    pg = next((x for c in b.contexts for x in c.pages if 'wir-studium' in x.url or '127.0.0.1:8765' in x.url), None)
    if not pg: sys.exit('open our page in a tab on the phone first')
    cdp = pg.context.new_cdp_session(pg); frames = []
    def on_frame(ev):
        frames.append((time.time(), ev['data'])); cdp.send('Page.screencastFrameAck', {'sessionId': ev['sessionId']})
    cdp.on('Page.screencastFrame', on_frame)
    pg.goto('about:blank'); pg.wait_for_timeout(500)
    cdp.send('Page.startScreencast', {'format': 'jpeg', 'quality': 90 if LETTERS else 60, 'maxWidth': 720 if LETTERS else 360, 'everyNthFrame': 1})
    pg.wait_for_timeout(300); frames.clear()
    t0 = time.time()
    pg.goto(BASE + '?' + '&'.join(x for x in (Q, 'v=%d' % int(time.time())) if x), wait_until='commit')
    pg.wait_for_timeout(int(DUR * 1000))
    cdp.send('Page.stopScreencast')
    marks = pg.evaluate("({reveal:Math.round((performance.getEntriesByName('wir-reveal')[0]||{}).startTime||-1),"
                        "paint:performance.getEntriesByType('paint').map(e=>e.name+' '+Math.round(e.startTime))})")
    # the title's letters at rest (css px) and the width of the screen they were drawn on
    LET = pg.evaluate("({W:innerWidth,ch:[...document.querySelectorAll('#heroT .ch')].map(c=>{const r=c.getBoundingClientRect();"
                      "return [c.textContent.toUpperCase(),r.left,r.top,r.right,r.bottom]})})")
    if LOCAL: pg.goto('https://grzegczerw96.github.io/wir-studium/?v=%d' % int(time.time()), wait_until='load')
print('marks (ms from navigation start):', marks)
ims = [(round(t - t0, 2), Image.open(io.BytesIO(base64.b64decode(d))).convert('RGB')) for t, d in frames]
print('frames', len(ims), 'times', [t for t, _ in ims][:40])
# a strip: one frame every ~.25 s, labelled
pick, last = [], -1
for t, im in ims:
    if t - last >= .25: pick.append((t, im)); last = t
w, h = pick[0][1].size; k = 160 / w
sheet = Image.new('RGB', (int(w * k) * min(len(pick), 10), int(h * k) * ((len(pick) + 9) // 10)), 'white')
from PIL import ImageDraw
for i, (t, im) in enumerate(pick):
    x, y = (i % 10) * int(w * k), (i // 10) * int(h * k)
    sheet.paste(im.resize((int(w * k), int(h * k))), (x, y)); ImageDraw.Draw(sheet).text((x + 4, y + 4), f'{t:.2f}s', fill=(255, 0, 0))
f = os.path.join(out, 'strip.png'); sheet.save(f); print('strip', f)
if LETTERS:
    from PIL import ImageChops, ImageStat
    k = w / LET['W']
    boxes = [(c[0], tuple(int(round(v * k)) for v in (c[1] - 2, c[2] - 2, c[3] + 2, c[4] + 2))) for c in LET['ch']]
    gray = [(t, im.convert('L')) for t, im in ims]
    ev = []
    for li, (ch, bx) in enumerate(boxes):
        d = [0.0]
        for i in range(1, len(gray)):
            dt = max(gray[i][0] - gray[i - 1][0], .008)
            d.append(ImageStat.Stat(ImageChops.difference(gray[i][1].crop(bx), gray[i - 1][1].crop(bx))).mean[0] / (dt / .016))
        for i in range(1, len(d)):
            around = sorted(d[max(1, i - 5):i] + d[i + 1:i + 6]) or [0]
            ratio = d[i] / (around[len(around) // 2] + .5)
            # (only where a letter's ink is: the smoke's front alone, moving fast over an empty box, is not a jump)
            ink = min(ImageStat.Stat(gray[j][1].crop(bx)).extrema[0][0] for j in (i - 1, i)) < 60
            if d[i] > 4 and ratio > 4 and ink: ev.append((ratio, d[i], gray[i][0], li, ch, i))
    ev.sort(reverse=True)
    print('letter jumps (time from navigation, letter, change per 16 ms, times its neighbours):')
    for r, dv, t, li, ch, i in ev[:10]: print(f'  {t:5.2f}s  {ch} (#{li})  {dv:5.1f}  ×{r:4.1f}')
    if not ev: print('  none')
    shots = []
    for r, dv, t, li, ch, i in ev[:4]:
        bx = boxes[li][1]; pad = int(10 * k); b2 = (bx[0] - pad, bx[1] - pad, bx[2] + pad, bx[3] + pad)
        shots.append([ims[j][1].crop(b2).resize(((b2[2] - b2[0]) * 3, (b2[3] - b2[1]) * 3)) for j in (i - 1, i, i + 1)])
    if shots:
        cw = max(s[0].width for s in shots) * 3 + 20; chh = sum(s[0].height + 10 for s in shots)
        sh = Image.new('RGB', (cw, chh), 'red'); y = 0
        for s in shots:
            x = 0
            for im in s: sh.paste(im, (x, y)); x += im.width + 10
            y += s[0].height + 10
        f = os.path.join(out, 'letter_jumps.png'); sh.save(f); print('close-ups (frame before, the jump, after):', f)
