"""Drive Chrome on Grzegorz's real phone (USB debugging on, cable in) — only the tab with our page is ever touched;
his other tabs are private. See CLAUDE.md, "Kontrola jakości".
usage: py -I tools/phone.py <steps.json> [--local] [--tag name]
  --local: load the page from this computer (not yet pushed) through adb reverse; the server is started here
steps: {"reload":true} | {"open":"fx=5"} | {"js":"..."} | {"swipe":-600,"speed":900} (CSS px, negative = scroll down, a real touch gesture:
       the address bar hides as with a finger) | {"shot":"name"} (whole screen incl. the address bar, adb screencap)
       | {"wait":ms} | {"fps":"start"} … {"fps":"stop"} (frame times from requestAnimationFrame + main-thread cost)
A plain text page scrolls at an even 11 ms on the Galaxy M15 (90 Hz): anything above that is our cost."""
import os, sys, json, subprocess, shutil, time, threading, functools, http.server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _env
from playwright.sync_api import sync_playwright
steps = json.load(open(sys.argv[1], encoding='utf8'))
LOCAL = '--local' in sys.argv
TAG = sys.argv[sys.argv.index('--tag') + 1] if '--tag' in sys.argv else 'phone'
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
FPS = "window.__fps={t:[],on:true};(function f(n){if(!window.__fps.on)return;window.__fps.t.push(n);requestAnimationFrame(f)})(performance.now())"
FPS_STOP = """(()=>{const F=window.__fps;F.on=false;const d=[];for(let i=1;i<F.t.length;i++)d.push(F.t[i]-F.t[i-1]);d.sort((a,b)=>a-b);
 const q=p=>d.length?d[Math.min(d.length-1,Math.floor(p*d.length))].toFixed(1):'-';return {frames:d.length,avg:(d.reduce((a,b)=>a+b,0)/Math.max(1,d.length)).toFixed(1),p50:q(.5),p90:q(.9),p99:q(.99),over33:d.filter(x=>x>33.4).length,over50:d.filter(x=>x>50).length}})()"""
with sync_playwright() as p:
    b = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
    pg = next((x for c in b.contexts for x in c.pages if 'wir-studium' in x.url or '127.0.0.1:8765' in x.url), None)
    if not pg: sys.exit('open https://grzegczerw96.github.io/wir-studium/ in Chrome on the phone first')
    cdp = pg.context.new_cdp_session(pg); cdp.send('Performance.enable'); base = {}
    metrics = lambda: {m['name']: m['value'] for m in cdp.send('Performance.getMetrics')['metrics']}
    for i, s in enumerate(steps):
        if 'reload' in s: pg.goto(BASE + '?v=%d' % int(time.time()), wait_until='load'); pg.wait_for_timeout(2500)
        # open: load the page with a query (e.g. "fx=5") and count frames from its first moment (the entrance), up to
        # the next {"fps":"stop"}
        elif 'open' in s:
            # (the page marks the moment it is revealed: performance.mark('wir-reveal'), so long frames can be told from
            #  the loading)
            if not getattr(pg, '_fps_init', False): pg.add_init_script(FPS); pg._fps_init = True
            # (through about:blank, as a first visit: reloading from the same site, Chrome keeps the old picture until
            #  the new page paints text or an image — "paint holding" — and the first paint is measured late)
            pg.goto('about:blank')
            pg.goto(BASE + '?' + '&'.join(x for x in (s['open'], 'v=%d' % int(time.time())) if x), wait_until='commit')
            base = metrics()
        elif 'js' in s: print(i, 'js', json.dumps(pg.evaluate(s['js']), ensure_ascii=False))
        elif 'swipe' in s: cdp.send('Input.synthesizeScrollGesture', {'x': s.get('x', 180), 'y': s.get('y', 560), 'yDistance': s['swipe'],
                                    'speed': s.get('speed', 1200), 'gestureSourceType': 'touch'})
        elif 'shot' in s:
            open(os.path.join(_env.OUT, f'{TAG}_{s["shot"]}.png'), 'wb').write(subprocess.run([ADB, '-s', DEV, 'exec-out', 'screencap', '-p'], capture_output=True).stdout)
        elif 'wait' in s: pg.wait_for_timeout(s['wait'])
        elif 'fps' in s:
            if s['fps'] == 'start': pg.evaluate(FPS); base = metrics()
            else:
                m = metrics(); d = {k: round(m[k] - base.get(k, 0), 3) for k in ('ScriptDuration', 'RecalcStyleDuration', 'LayoutDuration', 'TaskDuration')}
                print(i, 'fps', json.dumps(pg.evaluate(FPS_STOP)), 'cost', json.dumps(d))
    if LOCAL: pg.goto('https://grzegczerw96.github.io/wir-studium/?v=%d' % int(time.time()), wait_until='load')   # leave the tab on the live page
    print('url', pg.url)
