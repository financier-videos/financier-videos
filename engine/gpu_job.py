#!/usr/bin/env python3
"""Run a job bundle on a rented Runpod GPU and download its frames (generic version of gpu_render.py, 2026-11-22).
    python3 engine/gpu_job.py --bundle job.tar --out /tmp/result_dir [--expect 3800] [--max-min 120] [--gpu "NVIDIA GeForce RTX 4090"]
The bundle is a tar with run.sh at its root; run.sh writes PNGs under $OUT. The pod ALWAYS gets terminated at the end
(and a leftover pod named fin-job is terminated at the start). No API key here: the environment's proxy adds it for api.runpod.io.
"""
import argparse, json, os, secrets, subprocess, sys, tarfile, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gpu_render import GPUS, curl, gql, pods, terminate

NAME = "fin-job"
SERVER = "https://raw.githubusercontent.com/financier-videos/financier-videos/media/engine/gpu_job_server.py"
BOOT = ("bash -c 'apt-get update -qq && apt-get install -y -qq curl libgl1 libxrender1 libxi6 libxkbcommon0 libsm6 "
        "libxxf86vm1 libxfixes3 libice6 libegl1 >/dev/null; pip install -q bpy==5.3.0 numpy pillow; mkdir -p /workspace; "
        f"curl -sSfL -o /workspace/server.py {SERVER} && python3 /workspace/server.py'")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True); ap.add_argument("--out", required=True); ap.add_argument("--expect", type=int, default=0)
    ap.add_argument("--gpu", default="NVIDIA GeForce RTX 4090"); ap.add_argument("--max-min", type=int, default=120)
    a = ap.parse_args()
    for p in pods():
        if p["name"] == NAME: terminate(p["id"])
    tok = secrets.token_urlsafe(24); pid = None; t0 = time.time()
    try:
        inp = {"cloudType": "ALL", "gpuCount": 1, "gpuTypeId": a.gpu, "name": NAME, "imageName": "python:3.13-slim",
               "containerDiskInGb": 40, "volumeInGb": 0, "ports": "8000/http", "dockerArgs": BOOT,
               "env": [{"key": "JOB_TOKEN", "value": tok}, {"key": "JOB_MAX_MIN", "value": str(a.max_min + 10)}]}
        pod = None; tried = []
        for g in [a.gpu] + [x for x in GPUS if x != a.gpu]:
            inp["gpuTypeId"] = g
            try:
                pod = gql("mutation($i:PodFindAndDeployOnDemandInput){podFindAndDeployOnDemand(input:$i){id costPerHr machineId}}", {"i": inp})["podFindAndDeployOnDemand"]
            except SystemExit as e:
                tried.append(f"{g}: {str(e)[:120]}"); continue
            if pod: print("gpu type:", g, flush=True); break
        if not pod: raise SystemExit("no GPU available right now:\n" + "\n".join(tried))
        pid = pod["id"]; base = f"https://{pid}-8000.proxy.runpod.net"; H = ["-H", f"X-Token: {tok}"]
        print("pod", pid, "cost/hr", pod.get("costPerHr"), flush=True)

        def status():
            try: return json.loads(curl(H + [base + "/status"], 40))
            except Exception: return None
        while status() is None:
            if time.time() - t0 > 15 * 60: raise SystemExit("pod did not come up in 15 min")
            time.sleep(20)
        print("pod ready after", int(time.time() - t0), "s; uploading bundle", flush=True)
        print(curl(H + ["-X", "PUT", "-T", a.bundle, base + "/bundle"], 900)[:200], flush=True)
        print(curl(H + ["-X", "POST", base + "/start"], 60)[:200], flush=True)
        last = -1; lastlog = None
        while True:
            s = status()
            if s:
                if s["frames"] != last: last = s["frames"]; print(f"{s['frames']}/{a.expect or '?'} running={s['running']} {round((time.time() - t0) / 60, 1)} min", flush=True)
                if s["log"] != lastlog: lastlog = s["log"]; print("  | " + "\n  | ".join(s["log"][-3:]), flush=True)
                if s["packed"]: break
            if time.time() - t0 > a.max_min * 60: raise SystemExit(f"time limit {a.max_min} min reached")
            time.sleep(20)
        os.makedirs(a.out, exist_ok=True); tp = os.path.join(a.out, "result.tar")
        subprocess.run(["curl", "-sSf", "--max-time", "1800", "-H", f"X-Token: {tok}", "-o", tp + ".part", base + "/result"], check=True)
        os.replace(tp + ".part", tp)
        with tarfile.open(tp) as t: t.extractall(a.out, filter="data"); n = len(t.getnames())
        os.remove(tp)
        print(json.dumps({"ok": True, "frames": n, "minutes": round((time.time() - t0) / 60, 1), "out": a.out}), flush=True)
    finally:
        if pid:
            try: terminate(pid)
            except BaseException as e: print("!!! COULD NOT TERMINATE POD", pid, "- delete it in the Runpod console:", e, flush=True)
        print("leftover fin-job pods:", len([p for p in pods() if p["name"] == NAME]), flush=True)


if __name__ == "__main__":
    main()
