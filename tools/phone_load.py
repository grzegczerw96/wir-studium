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
    cdp.send('Page.startScreencast', {'format': 'jpeg', 'quality': 60, 'maxWidth': 360, 'everyNthFrame': 1})
    pg.wait_for_timeout(300); frames.clear()
    t0 = time.time()
    pg.goto(BASE + '?' + '&'.join(x for x in (Q, 'v=%d' % int(time.time())) if x), wait_until='commit')
    pg.wait_for_timeout(int(DUR * 1000))
    cdp.send('Page.stopScreencast')
    marks = pg.evaluate("({reveal:Math.round((performance.getEntriesByName('wir-reveal')[0]||{}).startTime||-1),"
                        "paint:performance.getEntriesByType('paint').map(e=>e.name+' '+Math.round(e.startTime))})")
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
