#!/usr/bin/env python3
"""Runs ON a rented GPU pod (generic job runner, 2026-11-22). Token-protected HTTP server on port 8000:
  PUT  /bundle   upload a .tar job bundle (it must contain run.sh); extracted to /workspace/job
  POST /start    run `bash run.sh` inside /workspace/job (env OUT=/workspace/out)
  GET  /status   JSON: frames (*.png under OUT), running, rc, last log lines, packed
  GET  /result   tar of OUT, PNGs converted to WebP (alpha kept), when the job has finished
Every request needs header X-Token == env JOB_TOKEN. The server exits by itself after JOB_MAX_MIN minutes (default 120).
Private files in the bundle live only on this pod, which the client terminates at the end.
"""
import glob, json, os, subprocess, tarfile, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TOKEN = os.environ.get("JOB_TOKEN", ""); J = "/workspace/job"; OUT = "/workspace/out"; LOG = "/workspace/job.log"
ST = {"proc": None, "packed": False, "t0": time.time(), "packing": False}
os.makedirs(J, exist_ok=True); os.makedirs(OUT, exist_ok=True)


def tail(n=8):
    try: return open(LOG, errors="replace").read().splitlines()[-n:]
    except Exception: return []


def pack():
    ST["packing"] = True
    from PIL import Image
    tar = "/workspace/result.tar"
    with tarfile.open(tar + ".part", "w") as t:
        for p in sorted(glob.glob(OUT + "/**/*.png", recursive=True)):
            wp = p[:-4] + ".webp"; Image.open(p).save(wp, "WEBP", quality=93, method=4)
            t.add(wp, arcname=os.path.relpath(wp, OUT))
    os.replace(tar + ".part", tar); ST["packed"] = True; ST["packing"] = False


def run():
    with open(LOG, "w") as lf:
        ST["proc"] = subprocess.Popen(["bash", "run.sh"], cwd=J, stdout=lf, stderr=subprocess.STDOUT, env=dict(os.environ, OUT=OUT))
        ST["proc"].wait()
    pack()


class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def ok(self, body, code=200):
        b = json.dumps(body).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

    def auth(self):
        if TOKEN and self.headers.get("X-Token") == TOKEN: return True
        self.ok({"error": "forbidden"}, 403); return False

    def do_GET(self):
        if not self.auth(): return
        if self.path.startswith("/status"):
            p = ST["proc"]
            self.ok({"frames": len(glob.glob(OUT + "/**/*.png", recursive=True)), "running": bool(p and p.poll() is None),
                     "rc": (p.poll() if p else None), "packed": ST["packed"], "packing": ST["packing"],
                     "bundle": os.path.exists(J + "/run.sh"), "log": tail()})
        elif self.path.startswith("/result") and ST["packed"]:
            f = "/workspace/result.tar"; self.send_response(200); self.send_header("Content-Length", str(os.path.getsize(f))); self.end_headers()
            with open(f, "rb") as fh:
                while True:
                    b = fh.read(1 << 20)
                    if not b: break
                    self.wfile.write(b)
        else: self.ok({"error": "not ready"}, 404)

    def do_PUT(self):
        if not self.auth(): return
        n = int(self.headers.get("Content-Length", 0)); left = n; tp = "/workspace/bundle.tar"
        with open(tp, "wb") as fh:
            while left > 0:
                b = self.rfile.read(min(1 << 20, left))
                if not b: break
                fh.write(b); left -= len(b)
        if left == 0:
            with tarfile.open(tp) as t: t.extractall(J, filter="data")
        self.ok({"saved": left == 0, "bytes": n - left, "run_sh": os.path.exists(J + "/run.sh")})

    def do_POST(self):
        if not self.auth(): return
        if ST["proc"] is None and os.path.exists(J + "/run.sh"):
            threading.Thread(target=run, daemon=True).start(); self.ok({"started": True})
        else: self.ok({"started": False}, 409)


def watchdog():
    lim = float(os.environ.get("JOB_MAX_MIN", "120")) * 60
    while time.time() - ST["t0"] < lim: time.sleep(20)
    os._exit(0)


threading.Thread(target=watchdog, daemon=True).start()
ThreadingHTTPServer(("0.0.0.0", 8000), H).serve_forever()
