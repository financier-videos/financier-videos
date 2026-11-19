#!/usr/bin/env python3
"""Render the Buck 3D sprite library on a rented Runpod GPU and publish it as assets/buck3d_v2.tar.

Run from a Claude Code cloud session in the **Default** environment (Runpod key = network secret for api.runpod.io,
*.proxy.runpod.net allowed) inside a clone of financier-videos:
    python3 engine/gpu_render.py --model /path/to/buck_cinema.glb [--fast] [--gpu "NVIDIA GeForce RTX 4090"]
The pod is ALWAYS terminated at the end (and any leftover pod named buck-render is terminated at the start).
No API key appears in this script: the environment's proxy adds it to requests for api.runpod.io.
"""
import argparse, json, os, secrets, subprocess, sys, time

GQL = "https://api.runpod.io/graphql"; NAME = "buck-render"
GPUS = ["NVIDIA GeForce RTX 4090", "NVIDIA GeForce RTX 5090", "NVIDIA RTX A5000", "NVIDIA GeForce RTX 3090", "NVIDIA RTX A6000",
        "NVIDIA A40", "NVIDIA L4", "NVIDIA RTX 4000 Ada Generation", "NVIDIA L40S", "NVIDIA RTX 6000 Ada Generation"]
SERVER = "https://raw.githubusercontent.com/financier-videos/financier-videos/media/engine/gpu_pod_server.py"
BOOT = ("bash -c 'apt-get update -qq && apt-get install -y -qq curl libgl1 libxrender1 libxi6 libxkbcommon0 libsm6 "
        "libxxf86vm1 libxfixes3 libice6 libegl1 >/dev/null; pip install -q bpy==5.3.0 numpy pillow; mkdir -p /workspace/buck; "
        f"curl -sSfL -o /workspace/buck/server.py {SERVER} && python3 /workspace/buck/server.py'")


def curl(args, timeout=120):
    p = subprocess.run(["curl", "-sS", "--max-time", str(timeout)] + args, capture_output=True, timeout=timeout + 20)
    return p.stdout.decode(errors="replace")


def gql(query, variables=None):
    out = curl(["-X", "POST", GQL, "-H", "content-type: application/json", "-d", json.dumps({"query": query, "variables": variables or {}})])
    try: d = json.loads(out)
    except Exception: raise SystemExit(f"Runpod API: unexpected answer: {out[:300]}")
    if d.get("errors"): raise SystemExit(f"Runpod API error: {json.dumps(d['errors'])[:400]}")
    return d["data"]


def pods():
    return gql("query{myself{pods{id name desiredStatus costPerHr}}}")["myself"]["pods"]


def terminate(pid):
    gql("mutation($i:PodTerminateInput!){podTerminate(input:$i)}", {"i": {"podId": pid}}); print("terminated pod", pid, flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True); ap.add_argument("--fast", action="store_true")
    ap.add_argument("--gpu", default="NVIDIA GeForce RTX 4090"); ap.add_argument("--max-min", type=int, default=45)
    ap.add_argument("--out", default="assets/buck3d_v2.tar")
    a = ap.parse_args()
    if not os.path.exists(a.model): raise SystemExit("model file not found")
    for p in pods():
        if p["name"] == NAME: terminate(p["id"])
    tok = secrets.token_urlsafe(24); pid = None; t0 = time.time()
    try:
        inp = {"cloudType": "ALL", "gpuCount": 1, "gpuTypeId": a.gpu, "name": NAME, "imageName": "python:3.13-slim",
               "containerDiskInGb": 20, "volumeInGb": 0, "ports": "8000/http", "dockerArgs": BOOT,
               "env": [{"key": "BUCK_TOKEN", "value": tok}, {"key": "BUCK_MAX_MIN", "value": str(a.max_min + 10)}]}
        pod = None; tried = []
        for g in [a.gpu] + [x for x in GPUS if x != a.gpu]:  # first GPU type with free capacity wins
            inp["gpuTypeId"] = g
            try:
                r = gql("mutation($i:PodFindAndDeployOnDemandInput){podFindAndDeployOnDemand(input:$i){id costPerHr machineId}}", {"i": inp})
                pod = r["podFindAndDeployOnDemand"]
            except SystemExit as e:
                tried.append(f"{g}: {str(e)[:120]}"); continue
            if pod: print("gpu type:", g, flush=True); break
        if not pod: raise SystemExit("no GPU available right now:\n" + "\n".join(tried))
        pid = pod["id"]; base = f"https://{pid}-8000.proxy.runpod.net"
        print("pod", pid, "cost/hr", pod.get("costPerHr"), flush=True)
        H = ["-H", f"X-Token: {tok}"]

        def status():
            try: return json.loads(curl(H + [base + "/status"], 40))
            except Exception: return None
        while status() is None:  # image pull + apt + pip (~3-6 min)
            if time.time() - t0 > 15 * 60: raise SystemExit("pod did not come up in 15 min")
            time.sleep(20)
        print("pod ready after", int(time.time() - t0), "s; uploading model", flush=True)
        print(curl(H + ["-X", "PUT", "-T", a.model, base + "/model"], 600)[:200], flush=True)
        print(curl(H + ["-X", "POST", base + f"/start?fast={1 if a.fast else 0}"], 60)[:200], flush=True)
        last = -1
        while True:
            s = status()
            if s:
                if s["frames"] != last: last = s["frames"]; print(f"{s['frames']}/{s['total']} device={s['device']}", flush=True)
                if s["packed"]: break
                if not s["running"] and s["rc"] not in (None, 0): raise SystemExit("render failed: " + " | ".join(s["log"])[-600:])
            if time.time() - t0 > a.max_min * 60: raise SystemExit(f"time limit {a.max_min} min reached")
            time.sleep(15)
        os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
        subprocess.run(["curl", "-sSf", "--max-time", "900", "-H", f"X-Token: {tok}", "-o", a.out + ".part", base + "/result"], check=True)
        n = len(subprocess.run(["tar", "tf", a.out + ".part"], capture_output=True, text=True).stdout.split())
        if n != 226: raise SystemExit(f"result has {n} frames, expected 226")
        os.replace(a.out + ".part", a.out)
        print(json.dumps({"ok": True, "frames": n, "device": s["device"], "minutes": round((time.time() - t0) / 60, 1), "out": a.out}))
    finally:
        if pid:
            try: terminate(pid)
            except BaseException as e: print("!!! COULD NOT TERMINATE POD", pid, "- delete it in the Runpod console:", e, flush=True)
        left = [p for p in pods() if p["name"] == NAME]
        print("leftover buck-render pods:", len(left), flush=True)


if __name__ == "__main__":
    main()
