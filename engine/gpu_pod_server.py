#!/usr/bin/env python3
"""Runs ON the rented GPU pod. Tiny token-protected HTTP server (port 8000):
  PUT  /model            upload the private Buck GLB (never stored anywhere else; the pod is deleted after the job)
  POST /start?fast=0     start buck3d.py --cinema --gpu over the whole library
  GET  /status           JSON: frames done, finished, device, last log lines
  GET  /result           the finished library as a tar of WebP frames (assets/buck3d_v2.tar layout)
Every request needs header X-Token == env BUCK_TOKEN. The server exits by itself after BUCK_MAX_MIN minutes (default 60).
"""
import glob, json, os, subprocess, sys, tarfile, threading, time, urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TOKEN = os.environ.get("BUCK_TOKEN", ""); W = "/workspace/buck"; OUT = W + "/frames"; LOG = W + "/render.log"
RAW = "https://raw.githubusercontent.com/financier-videos/financier-videos/media/engine/buck3d.py"
TOTAL = 226; ST = {"proc": None, "packed": False, "t0": time.time()}
os.makedirs(OUT, exist_ok=True)


def tail(n=6):
    try: return open(LOG, errors="replace").read().splitlines()[-n:]
    except Exception: return []


def device():
    for ln in tail(400):
        if "RENDER_DEVICE" in ln: return ln.split("RENDER_DEVICE", 1)[1].strip()
    return ""


def pack():
    from PIL import Image
    tar = W + "/buck3d_v2.tar"
    with tarfile.open(tar + ".part", "w") as t:
        for p in sorted(glob.glob(OUT + "/*.png")):
            wp = p[:-4] + ".webp"; Image.open(p).convert("RGBA").save(wp, "WEBP", quality=92, method=4)
            t.add(wp, arcname=os.path.basename(wp))
    os.replace(tar + ".part", tar); ST["packed"] = True


def run(fast):
    subprocess.run(["curl", "-sSfL", "-o", W + "/buck3d.py", RAW], check=True)
    cmd = [sys.executable, W + "/buck3d.py", "--cinema", "--gpu", "--tripo", W + "/buck.glb", "--out", OUT] + (["--fast"] if fast else [])
    with open(LOG, "w") as lf:
        ST["proc"] = subprocess.Popen(cmd, stdout=lf, stderr=subprocess.STDOUT)
        ST["proc"].wait()
    if len(glob.glob(OUT + "/*.png")) >= TOTAL: pack()


class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def ok(self, body, ctype="application/json", code=200):
        b = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code); self.send_header("Content-Type", ctype); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

    def auth(self):
        if TOKEN and self.headers.get("X-Token") == TOKEN: return True
        self.ok({"error": "forbidden"}, code=403); return False

    def do_GET(self):
        if not self.auth(): return
        if self.path.startswith("/status"):
            p = ST["proc"]
            self.ok({"frames": len(glob.glob(OUT + "/*.png")), "total": TOTAL, "running": bool(p and p.poll() is None),
                     "rc": (p.poll() if p else None), "packed": ST["packed"], "device": device(),
                     "model": os.path.exists(W + "/buck.glb"), "log": tail()})
        elif self.path.startswith("/result") and ST["packed"]:
            f = W + "/buck3d_v2.tar"; self.send_response(200); self.send_header("Content-Length", str(os.path.getsize(f))); self.end_headers()
            with open(f, "rb") as fh:
                while True:
                    b = fh.read(1 << 20)
                    if not b: break
                    self.wfile.write(b)
        else: self.ok({"error": "not ready"}, code=404)

    def do_PUT(self):
        if not self.auth(): return
        n = int(self.headers.get("Content-Length", 0)); left = n
        with open(W + "/buck.glb.part", "wb") as fh:
            while left > 0:
                b = self.rfile.read(min(1 << 20, left))
                if not b: break
                fh.write(b); left -= len(b)
        if left == 0: os.replace(W + "/buck.glb.part", W + "/buck.glb")
        self.ok({"saved": left == 0, "bytes": n - left})

    def do_POST(self):
        if not self.auth(): return
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if ST["proc"] is None and os.path.exists(W + "/buck.glb"):
            threading.Thread(target=run, args=(q.get("fast", ["0"])[0] == "1",), daemon=True).start(); self.ok({"started": True})
        else: self.ok({"started": False}, code=409)


def watchdog():
    lim = float(os.environ.get("BUCK_MAX_MIN", "60")) * 60
    while time.time() - ST["t0"] < lim: time.sleep(20)
    os._exit(0)


threading.Thread(target=watchdog, daemon=True).start()
ThreadingHTTPServer(("0.0.0.0", 8000), H).serve_forever()
