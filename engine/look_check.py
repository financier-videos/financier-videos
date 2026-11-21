#!/usr/bin/env python3
"""look_check.py - "does this video LOOK like the previous ones?" gate (Shohjahon 2026-11-21 20:26:
"videolar yana bir xil: yozuvlar, grafikalar, lavhalar, stillar").

Usage:  python3 -I engine/look_check.py NEW.mp4 PREV1.mp4 [PREV2.mp4 ...]     -> exit 1 if NEW is too similar to any PREV
        python3 -I engine/look_check.py --matrix A.mp4 B.mp4 C.mp4 ...        -> pairwise table (diagnostics)

Signature per video (12 frames spread over the video, 90x160):
  layout  - where the "ink" is: edge-density map 9x16, averaged over frames (same template => same map)
  palette - hue histogram (18 bins) of saturated, bright pixels + share of such pixels (accent colours)
  tone    - brightness histogram (8 bins) (always-dark vs light/colourful)
Similarity 0..1 = 0.45*layout + 0.35*palette + 0.20*tone.  FAIL if >= LIMIT (default 0.70; 2026-11-21 dagi 8 ta "bir xil" video o'zaro 0.77-0.91 chiqdi).
"""
import sys, subprocess, colorsys
import numpy as np

W, H, N, LIMIT = 90, 160, 12, 0.70

def frames(path):
    d = float(subprocess.check_output(["ffprobe", "-v", "0", "-show_entries", "format=duration", "-of", "csv=p=0", path]).strip())
    raw = subprocess.check_output(["ffmpeg", "-v", "0", "-i", path, "-vf", f"fps={N}/{d},scale={W}:{H}", "-frames:v", str(N),
                                   "-f", "rawvideo", "-pix_fmt", "rgb24", "-"])
    a = np.frombuffer(raw, np.uint8)
    n = len(a) // (W * H * 3)
    return a[:n * W * H * 3].reshape(n, H, W, 3).astype(np.float32) / 255.0

def signature(path):
    f = frames(path)
    g = f.mean(axis=3)
    ex = np.abs(np.diff(g, axis=2))[:, :-1, :]; ey = np.abs(np.diff(g, axis=1))[:, :, :-1]
    e = (ex + ey)                                                    # n, H-1, W-1
    e = e[:, :150, :80].reshape(len(f), 15, 10, 8, 10).mean(axis=(2, 4)).mean(axis=0)   # 15x8 map
    layout = e / (np.linalg.norm(e) + 1e-9)
    mx, mn = f.max(axis=3), f.min(axis=3)
    sat = (mx - mn) / (mx + 1e-6)
    mask = (sat > 0.45) & (mx > 0.45)
    r, gg, b = f[..., 0], f[..., 1], f[..., 2]
    hue = np.zeros_like(mx); d = mx - mn + 1e-6
    hue = np.where(mx == r, ((gg - b) / d) % 6, np.where(mx == gg, (b - r) / d + 2, (r - gg) / d + 4)) / 6.0
    hh = np.histogram(hue[mask], bins=18, range=(0, 1))[0].astype(np.float32)
    hh = hh / (hh.sum() + 1e-9)
    tone = np.histogram(g, bins=8, range=(0, 1))[0].astype(np.float32); tone /= tone.sum()
    return {"layout": layout.ravel(), "hue": hh, "accent_share": float(mask.mean()), "tone": tone, "luma": float(g.mean())}

def sim(a, b):
    lay = float((a["layout"] * b["layout"]).sum())
    lay = max(0.0, (lay - 0.5) / 0.5)                                  # cosine of two non-negative maps is rarely < 0.5
    pal = float(np.minimum(a["hue"], b["hue"]).sum())
    tone = float(np.minimum(a["tone"], b["tone"]).sum())
    return 0.45 * lay + 0.35 * pal + 0.20 * tone, lay, pal, tone

def main():
    args = sys.argv[1:]
    if not args: print(__doc__); return 2
    if args[0] == "--matrix":
        sigs = [(p, signature(p)) for p in args[1:]]
        for i, (p, s) in enumerate(sigs):
            print(f"{i}: {p.split('/')[-1]:38s} luma {s['luma']:.2f} accent {s['accent_share']:.3f} top-hue-bin {int(s['hue'].argmax())}")
        print("     " + " ".join(f"{j:5d}" for j in range(len(sigs))))
        for i, (_, a) in enumerate(sigs):
            print(f"{i:3d}: " + " ".join("  -  " if i == j else f"{sim(a, b)[0]:.2f} " for j, (_, b) in enumerate(sigs)))
        return 0
    new = signature(args[0]); bad = 0
    for p in args[1:]:
        s, lay, pal, tone = sim(new, signature(p))
        flag = "FAIL" if s >= LIMIT else "ok"
        bad += s >= LIMIT
        print(f"{flag}  {s:.2f}  (layout {lay:.2f}, palette {pal:.2f}, tone {tone:.2f})  vs {p.split('/')[-1]}")
    print("LOOK_CHECK:", "FAIL - too similar; change the look (docs/looks.md)" if bad else "PASS")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
