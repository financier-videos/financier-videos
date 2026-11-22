#!/usr/bin/env python3
"""Measure a cartoon short against the viral benchmarks (docs/viral_cartoon_study.md).

usage: cartoon_metrics.py VIDEO [--json]
Reports: first speech onset, average shot length, cuts in the first 3 s, longest dead-air gap,
dialogue gap distribution, colour saturation / brightness, loudness. Exit 1 when a HARD target fails.
"""
import json, re, subprocess, sys
import numpy as np

T = {  # target: (op, value, hard)  — from Pip&Rue 6.7M, Zovi 491K (239x), fruit story 2.3M, mole 50M
    "first_speech_s": ("<=", 0.8, True),     # first word by 0.65 s (Pip&Rue); never a silent title card
    "asl_s": ("<=", 2.6, True),              # 1.2-2.5 s per shot in dialogue, 0.8 s in montage
    "max_shot_s": ("<=", 6.0, False),
    "dead_air_s": ("<=", 1.2, True),         # longest silence (no voice and no ambience) inside the story
    "sat_mean": (">=", 0.30, False),         # saturated, warm palettes
    "luma_mean": (">=", 0.40, False),
    "lufs": (">=", -16.0, False),
}


def run(cmd): return subprocess.run(cmd, capture_output=True, text=True)


def dur(v): return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", v]).stdout.strip() or 0)


def cuts(v):
    o = run(["ffmpeg", "-hide_banner", "-i", v, "-vf", "scale=270:480,scdet=threshold=12", "-f", "null", "-"]).stderr
    return [float(x) for x in re.findall(r"lavfi\.scd\.time:\s*([\d.]+)", o)]


def silences(v, db=-45, d=0.25):
    o = run(["ffmpeg", "-hide_banner", "-i", v, "-af", f"silencedetect=n={db}dB:d={d}", "-f", "null", "-"]).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", o)]; en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", o)]
    return list(zip(st, en + [None] * (len(st) - len(en))))


def speech_onset(v):
    o = run(["ffmpeg", "-hide_banner", "-t", "4", "-i", v, "-af", "highpass=f=200,lowpass=f=3500,silencedetect=n=-30dB:d=0.12", "-f", "null", "-"]).stderr
    st = re.findall(r"silence_start: ([\d.]+)", o); en = re.findall(r"silence_end: ([\d.]+)", o)
    if st and float(st[0]) < 0.05 and en: return float(en[0])
    return 0.0


def colour2(v, n=12):
    D = dur(v); S = []; L = []
    for i in range(n):
        p = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{D * (i + .5) / n:.2f}", "-i", v, "-frames:v", "1", "-vf", "scale=90:160",
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
        a = np.frombuffer(p.stdout, np.uint8).reshape(-1, 3).astype(np.float32) / 255
        if not len(a): continue
        mx, mn = a.max(1), a.min(1); S.append(float(np.mean((mx - mn) / (mx + 1e-6)))); L.append(float(np.mean(a @ [0.2126, 0.7152, 0.0722])))
    return float(np.mean(S)), float(np.mean(L))


def lufs(v):
    o = run(["ffmpeg", "-hide_banner", "-i", v, "-af", "ebur128", "-f", "null", "-"]).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", o); return float(m[-1]) if m else None


def main():
    v = sys.argv[1]; D = dur(v); c = cuts(v); b = [0.0] + c + [D]; shots = np.diff(b)
    sil = [(a, (e if e is not None else D)) for a, e in silences(v)]; sil_in = [e - a for a, e in sil if a > 0.3 and (e or D) < D - 2.5]
    sat, lum = colour2(v)
    r = {"duration_s": round(D, 2), "first_speech_s": round(speech_onset(v), 2), "shots": len(shots), "asl_s": round(float(shots.mean()), 2),
         "max_shot_s": round(float(shots.max()), 2), "cuts_first_3s": sum(1 for x in c if x < 3), "dead_air_s": round(max(sil_in or [0]), 2),
         "sat_mean": round(sat, 3), "luma_mean": round(lum, 3), "lufs": lufs(v)}
    fails = []
    for k, (op, val, hard) in T.items():
        x = r.get(k)
        if x is None: continue
        ok = x <= val if op == "<=" else x >= val
        if not ok: fails.append(("FAIL " if hard else "warn ") + f"{k}={x} (target {op} {val})")
    r["verdict"] = "FAIL" if any(f.startswith("FAIL") for f in fails) else "PASS"; r["notes"] = fails
    print(json.dumps(r, indent=None if "--json" in sys.argv else 1))
    sys.exit(1 if r["verdict"] == "FAIL" else 0)


if __name__ == "__main__":
    main()
