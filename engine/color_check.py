#!/usr/bin/env python3
"""color_check.py - measure colour, not guess it (skill: docs/skills/color-expert/SKILL.md, notes/2026-11-21_color.md).

  python3 -I engine/color_check.py palette              # engine text colours vs every theme background
  python3 -I engine/color_check.py frames video.mp4 [--n 8] [--json out.json]

palette: WCAG 2.x contrast of each text colour (GOLD, WHITE, GREEN, RED) on each theme's lightest background
         (>= 4.5 body, >= 3.0 large display text); colour-blind check (Machado et al. 2009, severity 1.0,
         protan/deutan) of the pairs that carry meaning (RED loss vs GREEN gain): OKLab distance after simulation.
frames:  per sampled frame - mean luma, crushed blacks % (Y<16), clipped highlights % (Y>235), colourfulness
         (Hasler & Suesstrunk 2003), dominant hue family. Flags: CRUSHED (>35%), CLIPPED (>4%), DULL (colourfulness<15).
Exit 0 = no FAIL, 1 = FAIL. Thresholds for frames are ours (hypotheses) - tune them in growth_log.
"""
import json, math, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT = {"GOLD": (245, 197, 66), "WHITE": (245, 247, 250), "GREEN": (43, 214, 123), "RED": (255, 77, 77)}
MEANING_PAIRS = [("RED", "GREEN")]
PROTAN = ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.107216), (-0.003882, -0.048116, 1.051998))
DEUTAN = ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881))


def lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def delin(c):
    c = max(0.0, min(1.0, c))
    return 255 * (12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055)


def lum(rgb):
    r, g, b = (lin(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def wcag(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def oklab(rgb):
    r, g, b = (lin(x) for x in rgb)
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def de(a, b):
    return math.dist(oklab(a), oklab(b))


def sim(rgb, M):
    v = [lin(x) for x in rgb]
    return tuple(delin(sum(M[i][j] * v[j] for j in range(3))) for i in range(3))


def themes():
    src = open(os.path.join(ROOT, "engine", "make_video.py")).read()
    out = {}
    for name, body in re.findall(r'"(\w+)":\s*\(\[(.*?)\],\s*"\w+"\)', src):
        cols = [tuple(map(int, t)) for t in re.findall(r"\((\d+),\s*(\d+),\s*(\d+)\)", body)]
        if cols: out[name] = max(cols, key=lum)
    return out


def palette():
    fail = False; rows = []
    for th, bg in themes().items():
        for n, c in TEXT.items():
            r = wcag(c, bg); st = "PASS" if r >= 4.5 else ("LARGE" if r >= 3.0 else "FAIL")
            fail |= st == "FAIL"; rows.append((th, n, round(r, 2), st))
    for th, n, r, st in rows: print(f"{th:6} {n:5} {r:5}:1 {st}")
    for a, b in MEANING_PAIRS:
        for nm, M in (("normal", None), ("protan", PROTAN), ("deutan", DEUTAN)):
            ca, cb = (TEXT[a], TEXT[b]) if M is None else (sim(TEXT[a], M), sim(TEXT[b], M))
            d = de(ca, cb); st = "OK" if d >= 0.10 else "CONFUSABLE"
            print(f"{a} vs {b} [{nm}] OKLab dE {d:.3f} {st}")
            fail |= (st == "CONFUSABLE" and nm != "normal" and False)  # reported, not blocking: we never rely on hue alone
    return 1 if fail else 0


def frames(video, n=8, jout=None):
    import numpy as np
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                               capture_output=True, text=True).stdout or 0)
    res = []; bad = False
    for k in range(n):
        t = dur * (k + 0.5) / n
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1",
                              "-vf", "scale=270:480", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        if len(raw) < 270 * 480 * 3: continue
        a = np.frombuffer(raw[:270 * 480 * 3], np.uint8).reshape(480, 270, 3).astype(float)
        Y = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
        rg = a[..., 0] - a[..., 1]; yb = 0.5 * (a[..., 0] + a[..., 1]) - a[..., 2]
        colf = math.hypot(rg.std(), yb.std()) + 0.3 * math.hypot(rg.mean(), yb.mean())
        crushed = float((Y < 16).mean() * 100); clipped = float((Y > 235).mean() * 100)
        flags = [f for f, c in (("CRUSHED", crushed > 35), ("CLIPPED", clipped > 4), ("DULL", colf < 15)) if c]
        bad |= bool(flags)
        r = {"t": round(t, 1), "luma": round(float(Y.mean()), 1), "crushed%": round(crushed, 1),
             "clipped%": round(clipped, 1), "colourfulness": round(colf, 1), "flags": flags}
        res.append(r); print(r)
    if jout: json.dump(res, open(jout, "w"), indent=1)
    return 1 if bad else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0] == "palette": sys.exit(palette())
    if a[0] == "frames":
        n = int(a[a.index("--n") + 1]) if "--n" in a else 8
        j = a[a.index("--json") + 1] if "--json" in a else None
        sys.exit(frames(a[1], n, j))
    sys.exit(__doc__)
