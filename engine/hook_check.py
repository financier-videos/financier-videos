#!/usr/bin/env python3
"""Visual hook check (docs/visual_hook.md): is something worth looking at ON SCREEN and MOVING in the first second?

Usage: python3 -I engine/hook_check.py VIDEO.mp4 [--sheet out.jpg]
Measures 5 frames (0.04, 0.33, 0.66, 1.0, 1.5 s) at 180x320:
  luma0     mean brightness of the first frame                         FAIL < 0.25, WARN < 0.40
  motion1   largest mean abs frame difference inside the first 1.0 s   FAIL < 0.06 (frozen opening), WARN < 0.10
  text0     share of the first frame's centre band covered by a flat title block (rows 20-45 %)   WARN > 0.55
Thresholds are calibrated on OUR videos (2026-11-27: static Rocco openings 0.03-0.08, Financier 0.11-0.22), not on competitors.
Exit 0 PASS/WARN, 1 FAIL, 2 could not read.
"""
import sys, subprocess, json, io
try:
    import numpy as np
    from PIL import Image
except Exception as e:
    print("SKIP: numpy/PIL missing", e); sys.exit(2)
T = [0.04, 0.33, 0.66, 1.0, 1.5]
def frame(v, t):
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", v, "-frames:v", "1", "-vf", "scale=180:320", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
    if not p.stdout: return None
    return Image.open(io.BytesIO(p.stdout)).convert("RGB")
def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not a: print(__doc__); sys.exit(2)
    fr = [frame(a[0], t) for t in T]
    if any(f is None for f in fr): print("SKIP: could not read frames"); sys.exit(2)
    g = [np.asarray(f.convert("L"), float) / 255 for f in fr]
    luma0 = float(g[0].mean())
    diffs = [float(np.abs(g[i + 1] - g[i]).mean()) for i in range(3)]      # inside 0-1.0 s
    motion1 = max(diffs); span = float(np.abs(g[3] - g[0]).mean())
    band = np.asarray(fr[0], float)[64:144] / 255                            # rows 20-45 %
    flat = float((band.std(axis=2) < 0.06).mean() * (np.abs(np.diff(band.mean(axis=2), axis=1)) < 0.02).mean())
    st = "PASS"; notes = []
    if luma0 < 0.25: st = "FAIL"; notes.append("first frame too dark")
    elif luma0 < 0.40: notes.append("WARN first frame dim")
    if max(motion1, span) < 0.06: st = "FAIL"; notes.append("frozen opening: nothing changes in the first second")
    elif max(motion1, span) < 0.10: notes.append("WARN weak motion in the first second")
    if flat > 0.55: notes.append("WARN a flat title block covers the centre of frame 1")
    if st == "PASS" and any(n.startswith("WARN") for n in notes): st = "WARN"
    if "--sheet" in sys.argv:
        out = sys.argv[sys.argv.index("--sheet") + 1]; S = Image.new("RGB", (180 * 5, 320))
        for i, f in enumerate(fr): S.paste(f, (i * 180, 0))
        S.save(out, quality=85)
    print(json.dumps({"luma0": round(luma0, 2), "motion1": round(max(motion1, span), 3), "title_block": round(flat, 2)}))
    print(f"{st}: " + ("; ".join(notes) if notes else "bright first frame with motion inside the first second"))
    sys.exit(1 if st == "FAIL" else 0)
main()
