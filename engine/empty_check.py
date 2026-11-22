#!/usr/bin/env python3
"""Empty-panel check (night_order BUYURTMA 8 #2, docs/footage_bank.md "bo'sh panel TAQIQ").

A frame fails when one flat area of a single colour (or a flat colour with thin stripes) covers more than 15 % of it.
12 frames are sampled evenly; any failing frame fails the video.

How: the frame is cut into a 12 x 20 grid of blocks. A block is "flat" when its pixel spread is low (std < STD_MAX
after a light blur that melts thin stripes). Flat blocks whose mean colours are close (< COL_TOL) and that touch
each other form one area; the largest area is reported as a share of the frame.

usage: empty_check.py VIDEO [--limit 0.15] [--n 12]      exit 1 = FAIL
"""
import argparse, json, os, shutil, subprocess, sys, tempfile

import numpy as np
from PIL import Image, ImageFilter

GX, GY = 12, 20
STD_MAX = 7.0
COL_TOL = 14.0
DARK = 60.0  # mean RGB below this = night sky / space / dark clothing in real footage, not a drawn panel


def frames(video, n):
    o = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                       capture_output=True, text=True).stdout.strip()
    dur = float(o or 0); out = []
    tmp = tempfile.mkdtemp(prefix="empty_")
    for i in range(n):
        t = dur * (i + 0.5) / n; f = os.path.join(tmp, f"{i}.png")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1",
                        "-vf", "scale=360:640", f])
        if os.path.exists(f): out.append((t, f))
    return out


def largest_flat(path):
    im = Image.open(path).convert("RGB").filter(ImageFilter.GaussianBlur(3))
    a = np.asarray(im, np.float32); H, W, _ = a.shape; bh, bw = H // GY, W // GX
    flat = np.zeros((GY, GX), bool); mean = np.zeros((GY, GX, 3), np.float32)
    for y in range(GY):
        for x in range(GX):
            b = a[y * bh:(y + 1) * bh, x * bw:(x + 1) * bw].reshape(-1, 3)
            mean[y, x] = b.mean(0); flat[y, x] = float(b.std(0).mean()) < STD_MAX
    seen = np.zeros_like(flat); best = 0; best_col = None
    for y in range(GY):
        for x in range(GX):
            if not flat[y, x] or seen[y, x]: continue
            stack = [(y, x)]; seen[y, x] = True; n = 0; c0 = mean[y, x]
            while stack:
                cy, cx = stack.pop(); n += 1
                for ny, nx in ((cy + 1, cx), (cy - 1, cx), (cy, cx + 1), (cy, cx - 1)):
                    if 0 <= ny < GY and 0 <= nx < GX and flat[ny, nx] and not seen[ny, nx] \
                            and np.abs(mean[ny, nx] - c0).max() < COL_TOL:
                        seen[ny, nx] = True; stack.append((ny, nx))
            if 12.0 < float(c0.mean()) < DARK: n = n * 15 // 35  # pure black (< 12) stays a hard 15 %  # night sky / space in real footage: allowed up to 35 %
            if n > best: best, best_col = n, c0
    return best / (GX * GY), (best_col.round().astype(int).tolist() if best_col is not None else None)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("--limit", type=float, default=0.15)
    ap.add_argument("--n", type=int, default=12); a = ap.parse_args()
    rows = []; worst = 0.0
    fr = frames(a.video, a.n)
    for t, f in fr:
        share, col = largest_flat(f); worst = max(worst, share)
        rows.append({"t": round(t, 1), "flat": round(share, 3), "rgb": col})
    if fr: shutil.rmtree(os.path.dirname(fr[0][1]), ignore_errors=True)
    if not rows:
        print("SKIP: no frames could be read (video missing or still rendering)"); sys.exit(2)
    bad = [r for r in rows if r["flat"] > a.limit]
    print(json.dumps({"worst": round(worst, 3), "limit": a.limit, "bad_frames": bad, "frames": rows}))
    print(("FAIL" if bad else "PASS") + f": largest one-colour flat area {worst:.0%} of the frame (limit {a.limit:.0%})"
          + (f"; {len(bad)} frame(s) over: " + ", ".join(f"{r['t']}s={r['flat']:.0%}" for r in bad) if bad else ""))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
