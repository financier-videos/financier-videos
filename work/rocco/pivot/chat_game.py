#!/usr/bin/env python3
""""SCAM OR LEGIT?" chat-game Short renderer (Rocco pivot, format P1, 2026-11-23).

No characters: a phone chat screen, incoming texts, 3-2-1 countdown, a stamp
reveal, the tell highlighted and zoomed, 1-3 word synced captions, synth SFX.

usage: python3 chat_game.py spec.json vo_dir out.mp4
spec: {"title": "SCAM OR LEGIT?", "sub": "3 texts - only 1 is real",
       "rounds": [{"q": "r1q", "a": "r1a", "sender": "...",
                   "msgs": ["..."], "verdict": "scam|real", "tell": "substring"}],
       "hook": "hook", "end": "end", "brand": "RED FLAG ROCCO"}
vo_dir holds <key>.mp3 + <key>.json (ElevenLabs with-timestamps alignment).
"""
import json, math, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
SR = 44100
FD = "/usr/share/fonts/opentype/inter/"
ROOT = os.path.dirname(os.path.abspath(__file__)) + "/../../.."
AF = ROOT + "/assets/fonts/"


def font(name, size):
    p = FD + name if os.path.exists(FD + name) else AF + name
    return ImageFont.truetype(p, size)


F_TITLE = font("BebasNeue-Regular.ttf", 190)
F_SUB = font("Inter-SemiBold.otf", 46)
F_MSG = font("Inter-Regular.otf", 44)
F_SENDER = font("Inter-SemiBold.otf", 40)
F_CAP = font("Inter-Black.otf", 92)
F_COUNT = font("Inter-Black.otf", 260)
F_STAMP = font("BebasNeue-Regular.ttf", 250)
F_BRAND = font("Inter-Black.otf", 34)
F_SCORE = font("Inter-Black.otf", 44)

RED, GREEN, INK = (232, 48, 48), (28, 170, 90), (24, 24, 30)


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def pop(t, d=0.25):  # overshoot scale-in
    if t <= 0:
        return 0.0
    if t >= d:
        return 1.0
    x = t / d
    return 1 + 0.18 * math.sin(math.pi * x) * (1 - x) * 2 - (1 - ease(x))


def dur(fp):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                   "-of", "csv=p=0", fp]).decode()
    return float(out)


def words_from_alignment(al, t0):
    chars, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    words, cur, cs = [], "", None
    for c, s, e in zip(chars, st, en):
        if c.isspace():
            if cur:
                words.append((cur, t0 + cs, t0 + pe))
            cur, cs = "", None
        else:
            if cs is None:
                cs = s
            cur += c
            pe = e
    if cur:
        words.append((cur, t0 + cs, t0 + pe))
    return words


def wrap(text, f, maxw, d):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- SFX
def tone(freq, d, vol=0.4, decay=18.0):
    t = np.arange(int(SR * d)) / SR
    return vol * np.sin(2 * np.pi * freq * t) * np.exp(-decay * t)


def sfx_pop():
    a = tone(880, 0.12, 0.35, 30)
    b = tone(1320, 0.08, 0.2, 40)
    a[: b.size] += b
    return a


def sfx_tick():
    t = np.arange(int(SR * 0.05)) / SR
    return 0.5 * np.random.uniform(-1, 1, t.size) * np.exp(-90 * t)


def sfx_stamp(good):
    t = np.arange(int(SR * 0.45)) / SR
    thud = 0.8 * np.sin(2 * np.pi * 70 * t) * np.exp(-12 * t) + 0.25 * np.random.uniform(-1, 1, t.size) * np.exp(-30 * t)
    if good:
        bell = tone(1046, 0.45, 0.25, 6)[: t.size] + tone(1568, 0.45, 0.15, 7)[: t.size]
    else:
        bell = 0.22 * np.sign(np.sin(2 * np.pi * 150 * t)) * np.exp(-6 * t)
    return thud + bell


def sfx_whoosh():
    n = int(SR * 0.35)
    x = np.random.uniform(-1, 1, n)
    k = np.hanning(n)
    x = np.convolve(x, np.ones(30) / 30, mode="same")
    return 0.5 * x * k


def mix(buf, clip, at):
    i = int(at * SR)
    j = min(buf.size, i + clip.size)
    if i < buf.size:
        buf[i:j] += clip[: j - i]


# ---------------------------------------------------------------- timeline
def build(spec, vo):
    T = []  # events
    t = 0.0
    voice = []  # (key, start)
    caps = []
    def say(key, at):
        d = dur(f"{vo}/{key}.mp3")
        voice.append((key, at))
        caps.extend(words_from_alignment(json.load(open(f"{vo}/{key}.json")), at))
        return d
    hook_d = say(spec["hook"], 0.25)
    t = 0.25 + hook_d + 0.15
    rounds = []
    for i, r in enumerate(spec["rounds"]):
        R = {"i": i, "r": r, "start": t}
        R["typing"] = t + 0.05
        R["msg_at"] = [t + 0.45 + 0.55 * k for k in range(len(r["msgs"]))]
        qd = say(r["q"], t + 0.35)
        cstart = max(R["msg_at"][-1] + 0.4, t + 0.35 + qd + 0.1)
        R["count"] = cstart
        R["reveal"] = cstart + 2.0
        ad = say(r["a"], R["reveal"] + 0.25)
        R["zoom_in"] = R["reveal"] + 0.9
        R["end"] = R["reveal"] + 0.25 + ad + 0.35
        R["zoom_out"] = R["end"] - 0.45
        rounds.append(R)
        t = R["end"]
    end_at = t + 0.1
    ed = say(spec["end"], end_at)
    total = end_at + ed + 0.6
    return rounds, voice, caps, end_at, total


# ---------------------------------------------------------------- drawing
def bg_frame(t):
    img = Image.new("RGB", (W, H))
    a = np.linspace(0, 1, H)[:, None]
    shift = 0.08 * math.sin(t * 0.6)
    top = np.array([255, 214, 120]) * (1 - shift) + np.array([255, 170, 150]) * shift
    bot = np.array([255, 120, 110])
    g = (top * (1 - a) + bot * a)[:, None, :].repeat(W, axis=1)
    return Image.fromarray(g.astype(np.uint8)[:, :, :] if g.shape[1] == W else g[:, 0, :].astype(np.uint8))


_BG = None


def background(t):
    global _BG
    if _BG is None:
        a = np.linspace(0, 1, H)[:, None, None]
        top = np.array([255, 221, 140], float)
        bot = np.array([255, 138, 120], float)
        g = top * (1 - a) + bot * a
        g = np.repeat(g, W, axis=1)
        # soft diagonal stripes
        yy, xx = np.mgrid[0:H, 0:W]
        s = ((xx + yy) // 90) % 2
        g = g * (1 - 0.035 * s[:, :, None])
        _BG = Image.fromarray(g.clip(0, 255).astype(np.uint8))
    return _BG.copy()


def phone_layer(R, t, rects_out):
    """Chat screen image (phone body) for round R at time t; returns RGBA, plus tell rect."""
    pw, ph = 860, 1000
    img = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, pw - 1, ph - 1], 70, fill=(20, 20, 26, 255))
    d.rounded_rectangle([18, 18, pw - 19, ph - 19], 56, fill=(250, 250, 252, 255))
    # header
    d.rectangle([18, 90, pw - 19, 210], fill=(244, 244, 247, 255))
    d.ellipse([pw / 2 - 34, 100, pw / 2 + 34, 168], fill=(176, 180, 190, 255))
    r = R["r"]
    sw = d.textlength(r["sender"], font=F_SENDER)
    d.text(((pw - sw) / 2, 168), r["sender"], font=F_SENDER, fill=(40, 40, 48, 255))
    d.rounded_rectangle([pw / 2 - 80, 40, pw / 2 + 80, 66], 13, fill=(20, 20, 26, 255))
    y = 260
    tell_rect = None
    for k, m in enumerate(r["msgs"]):
        at = R["msg_at"][k]
        if t < at - 0.4:
            break
        if t < at:  # typing dots
            bx0, by0 = 50, y
            d.rounded_rectangle([bx0, by0, bx0 + 170, by0 + 90], 45, fill=(229, 229, 234, 255))
            for j in range(3):
                ph_ = (t * 6 + j * 0.8) % (2 * math.pi)
                rr = 11 + 4 * max(0, math.sin(ph_))
                cx = bx0 + 50 + j * 36
                d.ellipse([cx - rr, by0 + 45 - rr, cx + rr, by0 + 45 + rr], fill=(140, 140, 150, 255))
            break
        lines = wrap(m, F_MSG, pw - 230, d)
        lh = 58
        bh = 40 + lh * len(lines)
        bw = max(d.textlength(l, font=F_MSG) for l in lines) + 64
        s = pop(t - at)
        bub = Image.new("RGBA", (int(bw), int(bh)), (0, 0, 0, 0))
        bd = ImageDraw.Draw(bub)
        bd.rounded_rectangle([0, 0, bw - 1, bh - 1], 38, fill=(229, 229, 234, 255))
        for li, l in enumerate(lines):
            bd.text((32, 20 + li * lh), l, font=F_MSG, fill=(20, 20, 24, 255))
            tl = r.get("tell")
            if tl and tl in l and t >= R["reveal"]:
                x0 = 32 + bd.textlength(l[: l.index(tl)], font=F_MSG)
                x1 = x0 + bd.textlength(tl, font=F_MSG)
                col = GREEN if r["verdict"] == "real" else RED
                k_ = ease((t - R["reveal"] - 0.15) / 0.35)
                bd.rounded_rectangle([x0 - 8, 20 + li * lh - 4, x0 - 8 + (x1 - x0 + 16) * k_, 20 + li * lh + 56],
                                     10, outline=col + (255,), width=6)
                tell_rect = (50 + x0, y + 20 + li * lh, 50 + x1, y + 20 + li * lh + 52)
        if s > 0:
            sb = bub.resize((max(1, int(bw * s)), max(1, int(bh * s))))
            img.alpha_composite(sb, (50, int(y + bh * (1 - s) / 2)))
        y += bh + 24
    rects_out.append(tell_rect)
    return img


def stamp_img(verdict, s, ang):
    txt = "SCAM" if verdict == "scam" else "REAL"
    col = RED if verdict == "scam" else GREEN
    tw = F_STAMP.getlength(txt)
    im = Image.new("RGBA", (int(tw + 120), 330), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([8, 8, im.width - 8, im.height - 8], 40, outline=col + (255,), width=18,
                        fill=(255, 255, 255, 215))
    d.text((60, 30), txt, font=F_STAMP, fill=col + (255,))
    im = im.rotate(ang, expand=True, resample=Image.BICUBIC)
    if s != 1:
        im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))))
    return im


def draw_caption(img, caps, t):
    cur = [c for c in caps if c[1] - 0.05 <= t <= c[2] + 0.12]
    if not cur:
        return
    # group of up to 3 words around the current word
    idx = caps.index(cur[-1])
    g0 = idx - (idx % 3)
    grp = caps[g0: g0 + 3]
    grp = [w for w in grp if w[1] <= t + 0.02 and t <= grp[-1][2] + 0.3]
    txt = " ".join(w[0] for w in grp).upper()
    d = ImageDraw.Draw(img)
    f = F_CAP
    while d.textlength(txt, font=f) + f.size * 0.7 > W - 140 and f.size > 50:
        f = font("Inter-Black.otf", f.size - 6)
    ws = txt.split()
    gap = f.size * 0.32
    tw = sum(d.textlength(w, font=f) for w in ws) + gap * (len(ws) - 1)
    x, y = (W - tw) / 2, 1600
    for w in ws:
        d.text((x, y), w, font=f, fill=(255, 255, 255), stroke_width=12, stroke_fill=INK)
        x += d.textlength(w, font=f) + gap


def render(spec, vo, out):
    rounds, voice, caps, end_at, total = build(spec, vo)
    n = int(total * FPS)
    tmp = out + ".v.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "18", "-pix_fmt", "yuv420p", "-profile:v", "high", "-colorspace", "bt709",
                           "-color_primaries", "bt709", "-color_trc", "bt709", tmp], stdin=subprocess.PIPE)
    for fi in range(n):
        t = fi / FPS
        img = background(t).convert("RGBA")
        d = ImageDraw.Draw(img)
        # header
        cur = None
        for R in rounds:
            if R["start"] <= t < R["end"]:
                cur = R
        title = spec.get("title", "SCAM OR LEGIT?")
        if t < rounds[0]["start"] or t >= end_at:  # hook / end card
            k = ease((t - 0.0) / 0.4) if t < rounds[0]["start"] else ease((t - end_at) / 0.4)
            tw = d.textlength(title, font=F_TITLE)
            y0 = 560 - 60 * (1 - k)
            d.text(((W - tw) / 2, y0), title, font=F_TITLE, fill=INK)
            sub = spec.get("sub", "") if t < rounds[0]["start"] else spec.get("end_sub", "")
            sw = d.textlength(sub, font=F_SUB)
            d.text(((W - sw) / 2, y0 + 220), sub, font=F_SUB, fill=INK)
            # three message icons
            for j in range(3):
                cx = W / 2 + (j - 1) * 230
                s = pop(t - (0.6 + 0.35 * j) if t < rounds[0]["start"] else t - end_at - 0.2 * j)
                if s > 0:
                    rr = 80 * s
                    v = rounds[j]["r"]["verdict"] if t >= end_at else None
                    fill = (255, 255, 255) if v is None else (RED if v == "scam" else GREEN)
                    d.rounded_rectangle([cx - rr, 1000 - rr * 0.8, cx + rr, 1000 + rr * 0.8], int(30 * s), fill=fill,
                                        outline=INK, width=6)
                    lab = "?" if v is None else ("SCAM" if v == "scam" else "REAL")
                    fl = font("Inter-Black.otf", max(10, int((70 if v is None else 40) * s)))
                    lw = d.textlength(lab, font=fl)
                    d.text((cx - lw / 2, 1000 - fl.size * 0.62), lab, font=fl,
                           fill=INK if v is None else (255, 255, 255))
        else:
            # small title + score chips
            ft = font("BebasNeue-Regular.ttf", 120)
            tw = d.textlength(title, font=ft)
            d.text(((W - tw) / 2, 70), title, font=ft, fill=INK)
            for j in range(3):
                cx = W / 2 + (j - 1) * 110
                R2 = rounds[j]
                done = t >= R2["reveal"]
                active = R2 is cur
                fill = (255, 255, 255) if not done else (RED if R2["r"]["verdict"] == "scam" else GREEN)
                rr = 40 if active else 32
                d.ellipse([cx - rr, 250 - rr, cx + rr, 250 + rr], fill=fill, outline=INK, width=5)
                lab = str(j + 1)
                lw = d.textlength(lab, font=F_SCORE)
                d.text((cx - lw / 2, 250 - 28), lab, font=F_SCORE, fill=INK if not done else (255, 255, 255))
            if cur:
                rects = []
                ph = phone_layer(cur, t, rects)
                tell = rects[0]
                # zoom on tell during answer
                z = 1.0
                if tell and cur["zoom_in"] <= t <= cur["zoom_out"] + 0.3:
                    z = 1 + 0.28 * ease((t - cur["zoom_in"]) / 0.35) * (1 - ease((t - cur["zoom_out"]) / 0.3))
                # slow push-in
                z *= 1 + 0.03 * (t - cur["start"]) / max(1, cur["end"] - cur["start"])
                if cur["reveal"] <= t < cur["reveal"] + 0.25:  # shake
                    sh = 14 * math.sin(t * 90)
                else:
                    sh = 0
                pw, phh = ph.size
                ph2 = ph.resize((int(pw * z), int(phh * z)), Image.BICUBIC)
                if tell and z > 1.05:
                    cx_t = (tell[0] + tell[2]) / 2 * z
                    cy_t = (tell[1] + tell[3]) / 2 * z
                    k = (z - 1) / 0.28
                    ox = (W - ph2.width) / 2
                    oy = (900 - cy_t) * k + (360) * (1 - k)
                else:
                    ox, oy = (W - ph2.width) / 2, 360 - (ph2.height - phh) / 2
                shadow = Image.new("RGBA", ph2.size, (0, 0, 0, 0))
                ImageDraw.Draw(shadow).rounded_rectangle([0, 0, ph2.width - 1, ph2.height - 1], int(70 * z),
                                                         fill=(0, 0, 0, 90))
                shadow = shadow.filter(ImageFilter.GaussianBlur(25))
                img.alpha_composite(shadow, (int(ox + sh + 12), int(oy + 24)))
                img.alpha_composite(ph2, (int(ox + sh), int(oy)))
                # countdown
                if cur["count"] <= t < cur["reveal"]:
                    k = (t - cur["count"]) / 2.0
                    num = 3 - int(k * 3)
                    lt = (k * 3) % 1
                    s = 1.25 - 0.25 * ease(lt / 0.3)
                    dd = ImageDraw.Draw(img)
                    cx, cy = W / 2, 1110
                    rr = 120 * s
                    dd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(255, 255, 255), outline=INK, width=12)
                    a0 = -90
                    dd.arc([cx - rr - 26, cy - rr - 26, cx + rr + 26, cy + rr + 26], a0, a0 + 360 * (1 - k),
                           fill=RED, width=20)
                    fc = font("Inter-Black.otf", int(170 * s))
                    nw = dd.textlength(str(num), font=fc)
                    dd.text((cx - nw / 2, cy - fc.size * 0.62), str(num), font=fc, fill=INK)
                    q = "SCAM or REAL?"
                    fq = font("Inter-Black.otf", 70)
                    qw = dd.textlength(q, font=fq)
                    dd.text(((W - qw) / 2, cy + 140), q, font=fq, fill=INK, stroke_width=8,
                            stroke_fill=(255, 255, 255))
                # stamp
                if cur["reveal"] <= t < cur["zoom_in"] + 0.05:
                    lt = t - cur["reveal"]
                    s = 2.2 - 1.2 * ease(lt / 0.18)
                    st = stamp_img(cur["r"]["verdict"], s, 12 if cur["r"]["verdict"] == "scam" else -8)
                    img.alpha_composite(st, (int((W - st.width) / 2), int(930 - st.height / 2)))
        draw_caption(img, caps, t)
        # brand
        b = spec.get("brand", "RED FLAG ROCCO")
        bw = d.textlength(b, font=F_BRAND)
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([(W - bw) / 2 - 22, 1818, (W + bw) / 2 + 22, 1872], 26, fill=RED)
        d.text(((W - bw) / 2, 1824), b, font=F_BRAND, fill=(255, 255, 255))
        ff.stdin.write(img.convert("RGB").tobytes())
    ff.stdin.close()
    ff.wait()
    # audio
    buf = np.zeros(int(SR * (total + 0.5)))
    for key, at in voice:
        raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", f"{vo}/{key}.mp3", "-f", "f32le",
                                       "-ac", "1", "-ar", str(SR), "-"])
        mix(buf, np.frombuffer(raw, np.float32).astype(float) * 1.0, at)
    for j in range(3):
        mix(buf, sfx_pop() * 0.6, 0.6 + 0.35 * j)
    for R in rounds:
        mix(buf, sfx_whoosh() * 0.5, R["start"])
        for at in R["msg_at"]:
            mix(buf, sfx_pop() * 0.7, at)
        for k in range(3):
            mix(buf, sfx_tick() * 0.7, R["count"] + k * 2.0 / 3)
        mix(buf, sfx_stamp(R["r"]["verdict"] == "real") * 0.8, R["reveal"])
        mix(buf, sfx_whoosh() * 0.3, R["zoom_in"])
    mix(buf, sfx_whoosh() * 0.5, end_at)
    for j in range(3):
        mix(buf, sfx_stamp(rounds[j]["r"]["verdict"] == "real") * 0.35, end_at + 0.2 * j)
    buf = buf[: int(SR * total)]
    pk = np.max(np.abs(buf)) or 1
    buf = buf / pk * 0.89
    wav = out + ".a.wav"
    with wave.open(wav, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((buf * 32767).astype(np.int16).tobytes())
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-i", wav, "-filter_complex",
                           "[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,aformat=channel_layouts=stereo[a]", "-map", "0:v",
                           "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                           "-movflags", "+faststart", out])
    os.remove(tmp)
    os.remove(wav)
    json.dump({"duration": total, "rounds": [{k: v for k, v in R.items() if k != "r"} for R in rounds]},
              open(out + ".json", "w"), indent=1)
    print("OK", out, round(total, 2), "s")


if __name__ == "__main__":
    render(json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3])
