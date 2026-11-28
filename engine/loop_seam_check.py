#!/usr/bin/env python3
"""Loop seam check: does the LAST frame flow back into the FIRST frame (invisible loop cut)?

Idea: iart-ai/tiktok-video-skills short-form-video (MIT, 2026) — "match the last frame to the first
(same composition, position, color) so the cut is invisible". Our own code, no copied text.
Usage: python3 -I engine/loop_seam_check.py VIDEO.mp4 [--json]
Measures at 90x160 (first frame at 0.04 s vs last frame at duration-0.08 s):
  seam_diff   mean abs grey difference first vs last          (0 = identical)
  hist_dist   colour histogram distance (L1/2, 8x8x8 bins)      (0 = same palette)
  luma_jump   |mean luma first - mean luma last|
Verdict (calibrated loosely; INFORMATIONAL in qc, not a gate):
  SMOOTH  seam_diff < 0.12 and hist_dist < 0.35
  JUMP    seam_diff > 0.25 or hist_dist > 0.60 or luma_jump > 0.25  (viewer sees a hard reset -> loop is noticed)
  MIXED   otherwise
Exit 0 always when read (it is advice), 2 could not read.
"""
import sys, subprocess, json, io
try:
    import numpy as np
    from PIL import Image
except Exception as e:
    print("SKIP: numpy/PIL missing", e); sys.exit(2)


def duration(v):
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", v],
                       capture_output=True, text=True)
    try:
        return float(p.stdout.strip())
    except ValueError:
        return None


def frame(v, t):
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(t, 0):.3f}", "-i", v, "-frames:v", "1",
                        "-vf", "scale=90:160", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
    if not p.stdout:
        return None
    return np.asarray(Image.open(io.BytesIO(p.stdout)).convert("RGB"), float) / 255


def hist(a):
    q = np.clip((a * 8).astype(int), 0, 7)
    idx = q[..., 0] * 64 + q[..., 1] * 8 + q[..., 2]
    h = np.bincount(idx.ravel(), minlength=512).astype(float)
    return h / h.sum()


def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not a:
        print(__doc__); sys.exit(2)
    v = a[0]
    d = duration(v)
    if not d:
        print("SKIP: no duration"); sys.exit(2)
    f0 = frame(v, 0.04)
    f1 = None
    for back in (0.08, 0.2, 0.4, 0.8):          # some muxes end the video stream a little before the audio
        f1 = frame(v, d - back)
        if f1 is not None:
            break
    if f0 is None or f1 is None:
        print("SKIP: could not read frames"); sys.exit(2)
    g0, g1 = f0.mean(axis=2), f1.mean(axis=2)
    seam = float(np.abs(g0 - g1).mean())
    hd = float(np.abs(hist(f0) - hist(f1)).sum() / 2)
    lj = float(abs(g0.mean() - g1.mean()))
    if seam < 0.12 and hd < 0.35:
        st = "SMOOTH"
    elif seam > 0.25 or hd > 0.60 or lj > 0.25:
        st = "JUMP"
    else:
        st = "MIXED"
    r = {"video": v, "duration": round(d, 2), "seam_diff": round(seam, 3), "hist_dist": round(hd, 3),
         "luma_jump": round(lj, 3), "verdict": st}
    print(json.dumps(r) if "--json" in sys.argv else f"{st}  seam {seam:.3f}  hist {hd:.3f}  luma_jump {lj:.3f}  ({d:.1f} s)")
    sys.exit(0)


if __name__ == "__main__":
    main()
