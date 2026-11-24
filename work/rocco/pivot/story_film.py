#!/usr/bin/env python3
"""Cinematic story Short renderer (Rocco pivot, format B "historical con", 2026-11-23).

Still images -> Ken Burns shots (a new shot every ~1.5-2 s), film grade, grain,
vignette, 1-3 word synced captions, optional big "tag" text, synthesized ambience
(room / sea / rain / drone) and hits. No music.

usage: python3 story_film.py spec.json out.mp4
spec: {"vo": dir with <key>.mp3/.json, "img": dir, "gap": 0.25,
       "lines": [{"key": "l01", "amb": "room|sea|rain|none", "tag": "1822 · LONDON",
                  "hit": true, "shots": [[img, [x0,y0,z0], [x1,y1,z1]], ...]}]}
x,y = crop centre (0..1 of image), z = zoom (1 = full width).
"""
import json, math, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H, FPS, SR = 1080, 1920, 30, 44100
FD = "/usr/share/fonts/opentype/inter/"
AF = os.path.dirname(os.path.abspath(__file__)) + "/../../../assets/fonts/"
F_CAP = ImageFont.truetype(FD + "Inter-Black.otf", 88)
F_TAG = ImageFont.truetype(AF + "BebasNeue-Regular.ttf", 120)
F_BRAND = ImageFont.truetype(FD + "Inter-Black.otf", 30)


def dur(fp):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", fp]).decode())


def words(al, t0):
    out, cur, cs, pe = [], "", None, 0
    for c, s, e in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
        if c.isspace():
            if cur:
                out.append((cur, t0 + cs, t0 + pe))
            cur, cs = "", None
        else:
            cs = s if cs is None else cs
            cur += c
            pe = e
    if cur:
        out.append((cur, t0 + cs, t0 + pe))
    return out


def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


_IMG = {}


def load(path):
    if path not in _IMG:
        im = Image.open(path).convert("RGB")
        # upscale once so zooms stay sharp
        s = max(W * 1.0 / im.width, H * 1.0 / im.height) * 1.6
        _IMG[path] = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    return _IMG[path]


def crop(im, x, y, z):
    # visible window keeps 9:16; z=1 -> full image width
    cw = im.width / z
    ch = cw * H / W
    if ch > im.height:
        ch = im.height
        cw = ch * W / H
    cx = min(max(x * im.width, cw / 2), im.width - cw / 2)
    cy = min(max(y * im.height, ch / 2), im.height - ch / 2)
    box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
    return im.resize((W, H), Image.BICUBIC, box=box)


VIG = None


def vignette():
    global VIG
    if VIG is None:
        yy, xx = np.mgrid[0:H, 0:W]
        d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        VIG = np.clip(1 - 0.32 * np.clip(d - 0.55, 0, 1) ** 1.4 * 2, 0.55, 1)[:, :, None]
    return VIG


def grade(img, rng):
    a = np.asarray(img).astype(np.float32)
    a = (a - 128) * 1.06 + 128  # contrast
    a *= vignette()
    a += rng.normal(0, 5.5, (H // 2, W // 2, 1)).repeat(2, 0).repeat(2, 1)  # grain
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def caption(img, caps, t):
    cur = [c for c in caps if c[1] - 0.04 <= t <= c[2] + 0.15]
    if not cur:
        return
    i = caps.index(cur[-1])
    # groups of <=3 words that never cross a sentence end
    groups, g = [], []
    for j, w in enumerate(caps):
        g.append(j)
        if len(g) == 3 or w[0][-1] in ".?!" or w[0].endswith("..."):
            groups.append(g); g = []
    if g:
        groups.append(g)
    gi = next(gg for gg in groups if i in gg)
    grp = [caps[j] for j in gi if caps[j][1] <= t + 0.02]
    ws = [w[0].upper() for w in grp]
    d = ImageDraw.Draw(img)
    f = F_CAP
    gap = f.size * 0.3
    tw = sum(d.textlength(w, font=f) for w in ws) + gap * (len(ws) - 1)
    while tw > W - 120 and f.size > 48:
        f = ImageFont.truetype(FD + "Inter-Black.otf", f.size - 6)
        gap = f.size * 0.3
        tw = sum(d.textlength(w, font=f) for w in ws) + gap * (len(ws) - 1)
    x, y = (W - tw) / 2, 1330
    for k, w in enumerate(ws):
        last = k == len(ws) - 1
        d.text((x, y), w, font=f, fill=(255, 214, 90) if last else (255, 255, 255), stroke_width=10,
               stroke_fill=(10, 10, 12))
        x += d.textlength(w, font=f) + gap


# ---------------------------------------------------------------- audio
def noise(n, rng):
    return rng.uniform(-1, 1, n)


def lowpass(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")


def amb(kind, d, rng):
    n = int(SR * d)
    if kind == "room":  # murmur
        x = lowpass(noise(n, rng), 40) * 0.5
        x *= 0.7 + 0.3 * np.sin(np.arange(n) / SR * 2 * np.pi * 0.3)
        return x * 0.35
    if kind == "sea":
        t = np.arange(n) / SR
        x = lowpass(noise(n, rng), 12) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.15 * t) ** 2)
        return x * 0.5
    if kind == "rain":
        x = noise(n, rng) - lowpass(noise(n, rng), 6)
        return x * 0.12 + lowpass(noise(n, rng), 60) * 0.25
    if kind == "drone":
        t = np.arange(n) / SR
        return 0.12 * np.sin(2 * np.pi * 55 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.2 * t))
    return np.zeros(n)


def hit(rng):
    t = np.arange(int(SR * 1.6)) / SR
    return 0.9 * np.sin(2 * np.pi * 48 * t) * np.exp(-3 * t) + 0.25 * lowpass(noise(t.size, rng), 20) * np.exp(-6 * t)


def whoosh(rng):
    n = int(SR * 0.4)
    return 0.3 * lowpass(noise(n, rng), 25) * np.hanning(n)


def render(spec, out):
    rng = np.random.default_rng(7)
    vo, gap = spec["vo"], spec.get("gap", 0.25)
    t = 0.2
    plan, caps = [], []
    for L in spec["lines"]:
        d = dur(f"{vo}/{L['key']}.mp3")
        caps += words(json.load(open(f"{vo}/{L['key']}.json")), t)
        plan.append({"L": L, "t0": t, "d": d})
        t += d + gap + L.get("pause", 0)
    total = t + spec.get("tail", 1.4)
    # shots timeline
    shots = []
    for i, P in enumerate(plan):
        s0 = P["t0"] - (0.2 if i == 0 else gap / 2)
        s1 = (plan[i + 1]["t0"] - gap / 2) if i + 1 < len(plan) else total
        sh = P["L"]["shots"]
        w = [s[3] if len(s) > 3 else 1 for s in sh]
        acc = s0
        for s, wi in zip(sh, w):
            e = acc + (s1 - s0) * wi / sum(w)
            shots.append({"img": s[0], "a": s[1], "b": s[2], "t0": acc, "t1": e, "line": i})
            acc = e
    tmp = out + ".v.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s",
                           f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf",
                           "26", "-tune", "grain", "-maxrate", "7M", "-bufsize", "14M", "-pix_fmt", "yuv420p", "-profile:v", "high", "-colorspace", "bt709",
                           "-color_primaries", "bt709", "-color_trc", "bt709", tmp], stdin=subprocess.PIPE)
    n = int(total * FPS)
    for fi in range(n):
        tt = fi / FPS
        S = next((s for s in shots if s["t0"] <= tt < s["t1"]), shots[-1])
        k = ease((tt - S["t0"]) / max(0.01, S["t1"] - S["t0"]))
        x = S["a"][0] + (S["b"][0] - S["a"][0]) * k
        y = S["a"][1] + (S["b"][1] - S["a"][1]) * k
        z = S["a"][2] + (S["b"][2] - S["a"][2]) * k
        img = crop(load(os.path.join(spec["img"], S["img"])), x, y, z)
        L = plan[S["line"]]["L"]
        if L.get("bw"):
            img = ImageEnhance.Color(img).enhance(0.25)
        img = grade(img, rng)
        # flash on cut into a "hit" line
        if L.get("hit") and abs(tt - plan[S["line"]]["t0"] + gap / 2) < 0.08:
            img = Image.blend(img, Image.new("RGB", (W, H), (255, 255, 255)), 0.55)
        d = ImageDraw.Draw(img)
        tag = L.get("tag")
        if tag:
            P = plan[S["line"]]
            a = min(1, (tt - (P["t0"] - gap / 2)) / 0.3)
            if a > 0:
                tw = d.textlength(tag, font=F_TAG)
                y0 = 210 - 30 * (1 - a)
                d.rectangle([(W - tw) / 2 - 30, y0 - 6, (W + tw) / 2 + 30, y0 + 128], fill=(12, 12, 14))
                d.text(((W - tw) / 2, y0), tag, font=F_TAG, fill=(255, 214, 90))
        caption(img, caps, tt)
        b = spec.get("brand", "RED FLAG ROCCO")
        bw = d.textlength(b, font=F_BRAND)
        d.text(((W - bw) / 2, 1830), b, font=F_BRAND, fill=(255, 255, 255, 200), stroke_width=4,
               stroke_fill=(0, 0, 0))
        ff.stdin.write(img.tobytes())
    ff.stdin.close()
    ff.wait()
    # audio
    buf = np.zeros(int(SR * (total + 1)))
    def mix(c, at, g=1.0):
        i = int(at * SR)
        j = min(buf.size, i + c.size)
        buf[i:j] += c[: j - i] * g
    for i, P in enumerate(plan):
        raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", f"{vo}/{P['L']['key']}.mp3", "-f", "f32le",
                                       "-ac", "1", "-ar", str(SR), "-"])
        mix(np.frombuffer(raw, np.float32).astype(float), P["t0"])
        s0 = P["t0"] - (0.2 if i == 0 else gap / 2)
        s1 = (plan[i + 1]["t0"] - gap / 2) if i + 1 < len(plan) else total
        a = amb(P["L"].get("amb", "none"), s1 - s0, rng)
        fade = np.minimum(1, np.minimum(np.arange(a.size), a.size - np.arange(a.size)) / (0.15 * SR))
        mix(a * fade, s0, 0.5)
        if P["L"].get("hit"):
            mix(hit(rng), s0, 0.8)
    for S in shots[1:]:
        mix(whoosh(rng), S["t0"] - 0.15, 0.35)
    buf = buf[: int(SR * total)]
    buf = buf / (np.max(np.abs(buf)) or 1) * 0.9
    wav = out + ".a.wav"
    with wave.open(wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((buf * 32767).astype(np.int16).tobytes())
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-i", wav, "-filter_complex",
                           "[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,aformat=channel_layouts=stereo[a]", "-map", "0:v",
                           "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                           "-movflags", "+faststart", out])
    os.remove(tmp); os.remove(wav)
    print("OK", out, round(total, 2), "s,", len(shots), "shots, avg", round(total / len(shots), 2), "s/shot")


if __name__ == "__main__":
    render(json.load(open(sys.argv[1])), sys.argv[2])
