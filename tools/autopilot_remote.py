#!/usr/bin/env pythonw
"""WNL Autopilot — phone / LAN remote dashboard.

A tiny stdlib web server so you can watch the autonomous grind and hit STOP from your phone
(phone + this PC on the same wifi). It shows autopilot ON/OFF, the turn count, and recent
progress; the STOP button removes the sentinel the hooks read — the exact same kill switch as
the desktop panel. LAN-only (no internet exposure), token-gated, and it exposes NO secrets
(only autopilot status + CHANGELOG headings). Auto-launched when autopilot engages.

Run: pythonw .uvrun/autopilot_remote.py   (exits quietly if already running / port busy)
"""
import os
import json
import html
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

UVRUN = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(UVRUN)
SENTINEL = os.path.join(UVRUN, ".autopilot")
CTR = os.path.join(UVRUN, ".autopilot_turns")
TOKENF = os.path.join(UVRUN, ".autopilot_remote_token")
URLF = os.path.join(UVRUN, ".autopilot_remote_url")
CHANGELOG = os.path.join(ROOT, "_dev", "CHANGELOG.md")
TRAIL = os.path.join(ROOT, "_dev", ".change-trail.log")
PORT = 8899
CAP = 1000


def get_token():
    try:
        if os.path.exists(TOKENF):
            t = open(TOKENF).read().strip()
            if t:
                return t
    except Exception:
        pass
    t = os.urandom(4).hex()
    try:
        open(TOKENF, "w").write(t)
    except Exception:
        pass
    return t


TOKEN = get_token()


def engaged():
    return os.path.exists(SENTINEL)


def turns():
    try:
        return int(open(CTR).read().strip() or "0")
    except Exception:
        return 0


def set_engaged(on):
    try:
        if on:
            open(SENTINEL, "w").write("engaged\n")
            open(CTR, "w").write("0")
        elif os.path.exists(SENTINEL):
            os.remove(SENTINEL)
    except Exception:
        pass


def recent_progress(n=8):
    lines = []
    try:
        for line in open(CHANGELOG, encoding="utf-8", errors="replace"):
            if line.startswith("## ") or line.startswith("### "):
                lines.append(line.strip().lstrip("# "))
            if len(lines) >= n:
                break
    except Exception:
        pass
    if not lines:
        try:
            tail = open(TRAIL, encoding="utf-8", errors="replace").read().splitlines()[-n:]
            lines = [t.strip() for t in tail]
        except Exception:
            pass
    return lines[:n]


def lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


PAGE = """<!doctype html><html><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<meta http-equiv=refresh content=4>
<title>WNL Autopilot</title>
<style>
 body{{background:#141414;color:#eee;font-family:'Segoe UI',system-ui,sans-serif;margin:0;padding:16px;}}
 .banner{{border-radius:12px;padding:20px;text-align:center;font-size:22px;font-weight:700;margin-bottom:12px;}}
 .on{{background:#7a1f1f;color:#ffdede;}} .off{{background:#1f5a2e;color:#dcffe4;}}
 .sub{{font-size:13px;font-weight:400;opacity:.85;margin-top:6px;}}
 a.btn{{display:block;text-align:center;text-decoration:none;padding:22px;border-radius:12px;
        font-size:26px;font-weight:800;margin:10px 0;color:#fff;}}
 .stop{{background:#e74c3c;}} .start{{background:#2ecc71;}}
 h3{{color:#9a9a9a;font-size:12px;text-transform:uppercase;letter-spacing:.06em;margin:18px 0 6px;}}
 ul{{padding-left:0;margin:0;}} li{{font-size:13px;color:#cfcfcf;margin:4px 0;list-style:none;}}
 code{{color:#8ec7ff;}}
</style></head><body>
<div class="banner {cls}">{state}<div class=sub>{sub}</div></div>
{button}
<h3>Recent progress</h3><ul>{progress}</ul>
<h3>Kill switches (any works)</h3>
<ul><li>this page's STOP · the desktop panel · AUTOPILOT-STOP.bat · <code>autopilot.py off</code></li></ul>
</body></html>"""


class H(BaseHTTPRequestHandler):
    def _auth(self, q):
        return q.get("t", [""])[0] == TOKEN

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if not self._auth(q):
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"forbidden (bad or missing token)")
            return
        if u.path == "/stop":
            set_engaged(False)
            self._redirect()
            return
        if u.path == "/start":
            set_engaged(True)
            self._redirect()
            return
        if u.path == "/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"engaged": engaged(), "turns": turns(), "cap": CAP}).encode())
            return
        on = engaged()
        btn = ('<a class="btn stop" href="/stop?t=%s">&#128721; STOP</a>' % TOKEN) if on else \
              ('<a class="btn start" href="/start?t=%s">&#9654; START</a>' % TOKEN)
        prog = "".join("<li>%s</li>" % html.escape(x) for x in recent_progress()) or "<li>(no recent entries)</li>"
        body = PAGE.format(
            cls=("on" if on else "off"),
            state=("&#9679; AUTOPILOT ON" if on else "&#9675; autopilot off"),
            sub=("grinding hands-free &middot; turn %d/%d" % (turns(), CAP)) if on else "normal mode &middot; stops when idle",
            button=btn, progress=prog)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def _redirect(self):
        self.send_response(303)
        self.send_header("Location", "/?t=%s" % TOKEN)
        self.end_headers()

    def log_message(self, *a):
        pass  # keep it quiet


if __name__ == "__main__":
    try:
        srv = ThreadingHTTPServer(("0.0.0.0", PORT), H)
    except OSError:
        raise SystemExit(0)  # already running / port busy
    try:
        open(URLF, "w").write("http://%s:%d/?t=%s\n" % (lan_ip(), PORT, TOKEN))
    except Exception:
        pass
    srv.serve_forever()
