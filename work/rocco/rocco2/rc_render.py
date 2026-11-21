#!/usr/bin/env python3
"""Rocco style v2 renderer (docs/rocco_style_v2.md): bright cartoon sets, Rocco + Penny dialogue, own props, 1-3 word captions.
Audio = ElevenLabs Text-to-Dialogue (eleven_v3, emotion tags) -> real acting, not a narrator.

  python3 -I work/rocco/rocco2/rc_render.py SPEC.json OUT.mp4
SPEC: {"lines": [[speaker "R"|"P", "text with [tags]"], ...], "shots": [...], "end": {...}, "sfx": [...]} (see rc04.json)
Shot: {"line": i, "from": 0.0, "to": 1.0, "kind": "two|cu_r|cu_p|phone|flags|fact|trap|store|end", ...params}
  "from"/"to" = fraction of that line's time; the shot list must cover the whole timeline in order.
Characters: Rocco = sprite library (env FIN_BUCK3D or /tmp/fin_rocco_lib, work/rocco/rocco_sprites.py), Penny = drawn here.
Voices: Rocco v2 hYvMKGEmKYHZz9qvD8oj, Penny XeHmOH0wYkEbMfZqbCws (designed 2026-11-22, Shohjahon chose 7 and 11).
"""
import base64, hashlib, json, math, os, re, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, "engine"))
W, H, FPS = 1080, 1920, 30
INK = (35, 39, 45)
FONT = os.path.join(ROOT, "assets/fonts/LilitaOne-Regular.ttf")
LIB = os.environ.get("FIN_BUCK3D", "/tmp/fin_rocco_lib")
VOICE = {"R": "hYvMKGEmKYHZz9qvD8oj", "P": "XeHmOH0wYkEbMfZqbCws"}
SETS = {"yellow": ((255, 214, 64), (255, 170, 40)), "teal": ((64, 201, 198), (30, 150, 170)), "green": ((178, 236, 120), (96, 200, 110)),
        "pink": ((255, 170, 205), (214, 120, 230)), "sky": ((120, 200, 255), (70, 150, 240)), "peach": ((255, 196, 150), (255, 140, 110))}
_FC = {}


def F(s):
    s = int(s)
    if s not in _FC: _FC[s] = ImageFont.truetype(FONT, s)
    return _FC[s]


# ---------------- audio: Text-to-Dialogue with timestamps (cached) ----------------
def dialogue(lines, cache):
    body = {"inputs": [{"text": t, "voice_id": VOICE[s]} for s, t in lines], "model_id": "eleven_v3"}
    h = hashlib.sha1(json.dumps(body, sort_keys=True).encode()).hexdigest()[:14]
    f = os.path.join(cache, f"dlg_{h}.json")
    if not os.path.exists(f):
        bf = f + ".body"; json.dump(body, open(bf, "w"))
        r = subprocess.run(["curl", "-sS", "-X", "POST", "https://api.elevenlabs.io/v1/text-to-dialogue/with-timestamps?output_format=mp3_44100_128",
                            "-H", "xi-api-key: proxy-injected", "-H", "Content-Type: application/json", "--data-binary", "@" + bf,
                            "-o", f + ".part", "-w", "%{http_code}"], capture_output=True, text=True)
        if r.stdout != "200": sys.exit("dialogue http " + r.stdout + " " + open(f + ".part").read()[:300])
        os.replace(f + ".part", f)
    d = json.load(open(f))
    mp3 = f[:-5] + ".mp3"
    if not os.path.exists(mp3): open(mp3, "wb").write(base64.b64decode(d["audio_base64"]))
    return d, mp3


def words_from(d, lines):
    """[(word, t0, t1, line_index)] without [tags]; times from the character alignment."""
    al = d["alignment"]; ch = al["characters"]; st = al["character_start_times_seconds"]; en = al["character_end_times_seconds"]
    segs = d["voice_segments"]; out = []
    for sg in segs:
        i = sg["dialogue_input_index"]; a, b = sg["character_start_index"], sg["character_end_index"]
        cur = ""; t0 = t1 = None; depth = 0
        for k in range(a, min(b, len(ch))):
            c = ch[k]
            if c == "[": depth += 1
            if depth:
                if c == "]": depth -= 1
                continue
            if c.isspace():
                if cur.strip(".…"): out.append((cur, t0, t1, i))
                cur = ""; continue
            if not cur: t0 = st[k]
            cur += c; t1 = en[k]
        if cur.strip(".…"): out.append((cur, t0, t1, i))
    return out


# ---------------- drawing ----------------
_BG = {}


def setbg(name, rays=True):
    key = (name, rays)
    if key not in _BG:
        c1, c2 = SETS[name]
        a = np.linspace(0, 1, H)[:, None, None]
        arr = (np.array(c1)[None, None, :] * (1 - a) + np.array(c2)[None, None, :] * a).repeat(W, axis=1).astype(np.uint8)
        im = Image.fromarray(arr).convert("RGBA")
        if rays:
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov); cx, cy = W / 2, H * 0.42
            for k in range(0, 360, 20):
                a1, a2 = math.radians(k), math.radians(k + 10); R = 2600
                od.polygon([(cx, cy), (cx + R * math.cos(a1), cy + R * math.sin(a1)), (cx + R * math.cos(a2), cy + R * math.sin(a2))],
                           fill=tuple(min(255, x + 40) for x in c1) + (70,))
            im.alpha_composite(ov)
        d = ImageDraw.Draw(im, "RGBA")
        for yy in range(0, H, 54):
            for xx in range((yy // 54 % 2) * 27, W, 54):
                r = 5 + 7 * (yy / H); d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=(255, 255, 255, 55))
        a_ = np.asarray(im.convert("RGB"), np.float32); Y = a_ @ np.array([0.299, 0.587, 0.114], np.float32)
        a_ *= np.minimum(1.0, 226.0 / np.maximum(Y, 1.0))[..., None]  # bright, but under broadcast white (no "burnt" sky)
        im = Image.fromarray(a_.clip(0, 255).astype(np.uint8)).convert("RGBA")
        _BG[key] = im
    return _BG[key].copy()


def txt(im, xy, s, size, fill=(232, 232, 234), sw=10, anchor="mm", ang=0, stroke=INK, maxw=W * 0.92):
    f = F(size)
    while ImageDraw.Draw(im).textlength(s, font=f) > maxw and f.size > 30: f = F(f.size * 0.93)
    if ang:
        tmp = Image.new("RGBA", (W, int(size * 2.4)), (0, 0, 0, 0))
        ImageDraw.Draw(tmp).text((W / 2, tmp.height / 2), s, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke, anchor="mm")
        tmp = tmp.rotate(ang, expand=True, resample=Image.BICUBIC); im.alpha_composite(tmp, (int(xy[0] - tmp.width / 2), int(xy[1] - tmp.height / 2)))
    else:
        ImageDraw.Draw(im).text(xy, s, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke, anchor=anchor)


_SPR = {}


def sprite(name, size):
    key = (name, int(size))
    if key not in _SPR:
        p = os.path.join(LIB, name + ".webp")
        if not os.path.exists(p): return None
        sp = Image.open(p).convert("RGBA").resize((int(size), int(size)), Image.LANCZOS)
        a_ = np.asarray(sp, np.float32); Y = a_[..., :3] @ np.array([0.299, 0.587, 0.114], np.float32)
        a_[..., :3] *= np.minimum(1.0, 228.0 / np.maximum(Y, 1.0))[..., None]  # white fur under broadcast white
        _SPR[key] = Image.fromarray(a_.clip(0, 255).astype(np.uint8), "RGBA")
    return _SPR[key]


def rocco(im, cx, base_y, size, mood="happy", talk=0.0, t=0.0, act=None, act_t=0.0, flip=False):
    """Rocco standing on base_y (feet), centred on cx. talk 0..1 -> mouth sprite t1..t3. act = clip name played once."""
    fi = int(t * 15) % 15
    if act:
        n = len([f for f in os.listdir(LIB) if f.startswith(act + "_")]) or 1
        name = f"{act}_{min(n - 1, int(act_t * 15)):02d}"
    else:
        lvl = 0 if talk < 0.12 else (1 if talk < 0.4 else (2 if talk < 0.7 else 3))
        name = f"{mood}_{fi:02d}" if lvl == 0 else f"{mood}_t{lvl}_{fi:02d}"
    sp = sprite(name, size) or sprite(f"{mood}_{fi:02d}", size) or sprite(f"happy_{fi:02d}", size)
    if flip: sp = sp.transpose(Image.FLIP_LEFT_RIGHT)
    sq = 1 + 0.035 * talk  # talking bounce
    if abs(sq - 1) > 1e-3: sp = sp.resize((int(sp.width / math.sqrt(sq)), int(sp.height * sq)), Image.BILINEAR)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([cx - size * 0.26, base_y - size * 0.03, cx + size * 0.26, base_y + size * 0.035], fill=(0, 0, 0, 70)); im.alpha_composite(sh)
    im.alpha_composite(sp, (int(cx - sp.width / 2), int(base_y - sp.height * 0.81)))


def penny(im, cx, cy, s, mood="happy", talk=0.0, t=0.0):
    """Penny the piggy bank (pink), drawn. mood: happy|shock|sad|hope|nervous. talk 0..1 opens the mouth."""
    d = ImageDraw.Draw(im, "RGBA"); P = (255, 143, 171); PD = (232, 104, 140); u = s / 400
    cy = cy - abs(math.sin(t * 9)) * 14 * u * talk  # excited hop while talking
    d.ellipse([cx - 150 * u, cy + 150 * u, cx + 150 * u, cy + 178 * u], fill=(0, 0, 0, 60))
    for sx in (-1, 1):
        d.rounded_rectangle([cx + sx * 80 * u - 34 * u, cy + 90 * u, cx + sx * 80 * u + 34 * u, cy + 165 * u], 18 * u, fill=PD, outline=INK, width=int(7 * u))
    d.ellipse([cx - 185 * u, cy - 140 * u, cx + 185 * u, cy + 130 * u], fill=P, outline=INK, width=int(8 * u))
    for sx in (-1, 1):
        d.polygon([(cx + sx * 120 * u, cy - 110 * u), (cx + sx * 170 * u, cy - 190 * u), (cx + sx * 60 * u, cy - 135 * u)], fill=PD, outline=INK)
    d.rounded_rectangle([cx - 45 * u, cy - 150 * u, cx + 45 * u, cy - 136 * u], 6 * u, fill=INK)  # coin slot
    d.ellipse([cx - 62 * u, cy - 10 * u, cx + 62 * u, cy + 70 * u], fill=PD, outline=INK, width=int(7 * u))  # snout
    for sx in (-1, 1): d.ellipse([cx + sx * 24 * u - 11 * u, cy + 18 * u, cx + sx * 24 * u + 11 * u, cy + 44 * u], fill=INK)
    ey = cy - 62 * u; big = mood in ("shock", "nervous")
    blink = (int(t * 10) % 37) == 0
    for sx in (-1, 1):
        ex = cx + sx * 78 * u; r = (36 if big else 28) * u
        if blink: d.line([(ex - r, ey), (ex + r, ey)], fill=INK, width=int(7 * u)); continue
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(255, 255, 255), outline=INK, width=int(6 * u))
        pr = (10 if big else 13) * u; d.ellipse([ex - pr, ey - pr, ex + pr, ey + pr], fill=INK); d.ellipse([ex - 2 * u, ey - 9 * u, ex + 5 * u, ey - 2 * u], fill=(255, 255, 255))
        if mood == "sad": d.line([(ex - 30 * u, ey - 44 * u + sx * 8 * u), (ex + 30 * u, ey - 44 * u - sx * 8 * u)], fill=INK, width=int(7 * u))
        if mood == "hope": d.arc([ex - 30 * u, ey - 60 * u, ex + 30 * u, ey - 30 * u], 200, 340, fill=INK, width=int(6 * u))
    mo = talk * 34 * u + (14 * u if mood == "shock" else 0)
    if mo > 3 * u:  # open mouth
        d.ellipse([cx - (26 + talk * 10) * u, cy + 82 * u, cx + (26 + talk * 10) * u, cy + 82 * u + mo + 10 * u], fill=INK)
        d.ellipse([cx - 14 * u, cy + 82 * u + mo * 0.5 + 4 * u, cx + 14 * u, cy + 82 * u + mo + 8 * u], fill=(232, 90, 120))
    elif mood in ("happy", "hope"): d.arc([cx - 40 * u, cy + 60 * u, cx + 40 * u, cy + 110 * u], 10, 170, fill=INK, width=int(8 * u))
    elif mood == "nervous": d.line([(cx - 36 * u, cy + 98 * u), (cx - 12 * u, cy + 90 * u), (cx + 12 * u, cy + 100 * u), (cx + 36 * u, cy + 92 * u)], fill=INK, width=int(7 * u))
    else: d.arc([cx - 36 * u, cy + 86 * u, cx + 36 * u, cy + 126 * u], 190, 350, fill=INK, width=int(8 * u))
    for sx in (-1, 1): d.ellipse([cx + sx * 140 * u - 24 * u, cy - 6 * u, cx + sx * 140 * u + 24 * u, cy + 26 * u], fill=(255, 180, 200, 200))
    if mood == "nervous":  # sweat drop
        d.ellipse([cx + 150 * u, cy - 120 * u, cx + 180 * u, cy - 80 * u], fill=(140, 210, 255), outline=INK, width=int(4 * u))


def fox_avatar(im, cx, cy, r):
    d = ImageDraw.Draw(im)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 140, 60), outline=INK, width=6)
    d.polygon([(cx - r * 0.8, cy - r * 0.2), (cx - r * 0.55, cy - r * 1.05), (cx - r * 0.2, cy - r * 0.6)], fill=(255, 140, 60), outline=INK)
    d.polygon([(cx + r * 0.8, cy - r * 0.2), (cx + r * 0.55, cy - r * 1.05), (cx + r * 0.2, cy - r * 0.6)], fill=(255, 140, 60), outline=INK)
    d.ellipse([cx - r * 0.55, cy, cx + r * 0.55, cy + r * 0.85], fill=(255, 245, 230))
    for sx in (-1, 1): d.ellipse([cx + sx * r * 0.35 - 7, cy - r * 0.2 - 7, cx + sx * r * 0.35 + 7, cy - r * 0.2 + 7], fill=INK)
    d.ellipse([cx - 9, cy + r * 0.2, cx + 9, cy + r * 0.38], fill=INK)
    d.arc([cx - r * 0.3, cy + r * 0.2, cx + r * 0.3, cy + r * 0.6], 20, 160, fill=INK, width=4)


def phone(im, x, y, w, h, msgs, lt, sender="Slick"):
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x + 14, y + 18, x + w + 14, y + h + 18], 70, fill=(0, 0, 0, 60))
    d.rounded_rectangle([x, y, x + w, y + h], 70, fill=INK); d.rounded_rectangle([x + 20, y + 20, x + w - 20, y + h - 20], 54, fill=(226, 230, 236))
    d.rounded_rectangle([x + 20, y + 20, x + w - 20, y + 150], 54, fill=(230, 234, 242)); d.rectangle([x + 20, y + 100, x + w - 20, y + 150], fill=(230, 234, 242))
    fox_avatar(im, x + 100, y + 86, 42); d.text((x + 160, y + 86), sender, font=F(52), fill=INK, anchor="lm")
    yy = y + 190
    for m in msgs:
        at = m.get("at", 0)
        if lt < at: break
        k = min(1.0, (lt - at) / 0.18); s = 0.6 + 0.4 * k + 0.08 * math.sin(min(1, k) * math.pi)
        f = F(m.get("size", 96) * s); lines = m["t"].split("\n")
        while max(d.textlength(l, font=f) for l in lines) > w - 190 and f.size > 40: f = F(f.size * 0.92)
        lw = max(d.textlength(l, font=f) for l in lines); lh = f.size * 1.15
        col = tuple(m.get("col", (52, 199, 89)))
        d.rounded_rectangle([x + 50, yy, x + 50 + lw + 60, yy + lh * len(lines) + 40], 40, fill=col)
        for j, l in enumerate(lines): d.text((x + 80, yy + 20 + j * lh + lh / 2), l, font=f, fill=(255, 255, 255), anchor="lm")
        yy += lh * len(lines) + 70


def red_flag(im, x, y, s, ang=0, wave=0.0):
    tmp = Image.new("RGBA", (int(s * 1.6), int(s * 1.9)), (0, 0, 0, 0)); d = ImageDraw.Draw(tmp)
    d.rectangle([s * 0.18, s * 0.05, s * 0.26, s * 1.8], fill=(110, 80, 50), outline=INK, width=4)
    pts = []
    for k in range(9):
        px = s * 0.26 + k * s * 1.1 / 8; py = s * 0.1 + math.sin(wave + k * 0.7) * s * 0.06
        pts.append((px, py))
    pts += [(p[0], p[1] + s * 0.62) for p in reversed(pts)]
    d.polygon(pts, fill=(255, 59, 59), outline=INK)
    if ang: tmp = tmp.rotate(ang, expand=True, resample=Image.BICUBIC)
    im.alpha_composite(tmp, (int(x - tmp.width / 2), int(y - tmp.height)))


def card(im, box, title, lines, col=(230, 233, 238), title_col=INK):
    d = ImageDraw.Draw(im); x0, y0, x1, y1 = box
    d.rounded_rectangle([x0 + 12, y0 + 16, x1 + 12, y1 + 16], 50, fill=(0, 0, 0, 70)); d.rounded_rectangle(box, 50, fill=col, outline=INK, width=10)
    d.text(((x0 + x1) / 2, y0 + 90), title, font=F(84), fill=title_col, anchor="mm")
    yy = y0 + 200
    for s, ok in lines:
        mk = "✔" if ok else "✘"
        d.ellipse([x0 + 70, yy - 42, x0 + 154, yy + 42], fill=(52, 199, 89) if ok else (255, 59, 59), outline=INK, width=6)
        d.text((x0 + 112, yy), "OK" if ok else "NO", font=F(40), fill=(255, 255, 255), anchor="mm")
        d.text((x0 + 190, yy), s, font=F(76), fill=INK, anchor="lm"); yy += 130


def mousetrap(im, cx, cy, s, snapped, label="FREE GTA 6"):
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([cx - s, cy - s * 0.32, cx + s, cy + s * 0.32], 30, fill=(214, 160, 96), outline=INK, width=10)
    for k in range(-3, 4): d.line([(cx + k * s * 0.26, cy - s * 0.3), (cx + k * s * 0.26 + 20, cy + s * 0.3)], fill=(190, 136, 80), width=6)
    if not snapped:  # cheese with a price tag
        d.polygon([(cx - s * 0.15, cy - s * 0.05), (cx + s * 0.45, cy - s * 0.05), (cx + s * 0.45, cy - s * 0.45)], fill=(255, 214, 64), outline=INK)
        for (a, b, r) in ((0.25, -0.15, 0.05), (0.35, -0.25, 0.035)): d.ellipse([cx + a * s - r * s, cy + b * s - r * s, cx + a * s + r * s, cy + b * s + r * s], fill=(230, 180, 40))
        d.line([(cx - s * 0.9, cy), (cx - s * 0.9, cy - s * 0.85), (cx - s * 0.2, cy - s * 0.85)], fill=(150, 156, 170), width=16)
        txt(im, (cx + s * 0.1, cy - s * 0.85), label, int(s * 0.17), (255, 255, 255), sw=8, ang=-6)
    else:
        d.line([(cx - s * 0.9, cy), (cx + s * 0.6, cy - s * 0.08)], fill=(150, 156, 170), width=22)
        for k in range(8):
            a = k * math.pi / 4; d.line([(cx + math.cos(a) * s * 0.55, cy - s * 0.45 + math.sin(a) * s * 0.3), (cx + math.cos(a) * s * 0.85, cy - s * 0.45 + math.sin(a) * s * 0.48)], fill=INK, width=10)
        txt(im, (cx, cy - s * 0.65), "SNAP!", int(s * 0.36), (255, 59, 59), sw=12, ang=8)


# ---------------- frame composer ----------------
def env_track(wav, segs):
    import soundfile as sf
    y, sr = sf.read(wav, dtype="float32")
    if y.ndim > 1: y = y.mean(axis=1)
    hop = sr // FPS; n = len(y) // hop + 1
    e = np.array([np.sqrt(np.mean(y[i * hop:(i + 1) * hop] ** 2)) if i * hop < len(y) else 0 for i in range(n)], np.float32)
    e = np.clip(e / (np.percentile(e, 95) + 1e-6), 0, 1.2)
    who = np.full(n, "", dtype=object)
    for s in segs:
        a, b = int(s["start_time_seconds"] * FPS), int(s["end_time_seconds"] * FPS)
        who[a:b] = "P" if s["voice_id"] == VOICE["P"] else "R"
    return e, who


def compose(shot, lt, t, talkR, talkP, extra):
    k = shot["kind"]; im = setbg(shot.get("set", "yellow"))
    moodR = shot.get("r", "happy"); moodP = shot.get("p", "happy")
    act = shot.get("act"); act_t = lt - shot.get("act_at", 0)
    if act and not (0 <= act_t < shot.get("act_len", 1.0)): act = None
    if k == "two":
        penny(im, W * 0.30, H * 0.60, 440, moodP, talkP, t)
        rocco(im, W * 0.70, H * 0.76, 700, moodR, talkR, t, act, act_t)
    elif k == "cu_r":
        rocco(im, W * 0.52, H * 0.93, 1250, moodR, talkR, t, act, act_t)
    elif k == "cu_p":  # Penny big, Rocco reacting from the right edge (Rocco on screen >= 70% of the frames)
        penny(im, W * 0.42, H * 0.52, 760, moodP, talkP, t)
        rocco(im, W * 0.88, H * 0.99, 700, moodR, talkR, t, act, act_t)
    elif k == "phone":
        phone(im, 120, 200, 840, 1000, shot["msgs"], lt)
        penny(im, W * 0.25, H * 0.80, 470, moodP, talkP, t)
        if shot.get("rocco"): rocco(im, W * 0.80, H * 0.99, 560, moodR, talkR, t, act, act_t)
    elif k == "flags":
        n = shot.get("n", 1); n_prev = shot.get("n_prev", 0); pop_at = shot.get("pop_at", 0.2)
        shown = n if lt >= pop_at else n_prev
        for j in range(shown):
            jx = W * (0.14 + 0.18 * (j % 5)); jy = H * (0.36 + 0.06 * (j // 5)) + (j % 2) * 30
            dr = (lt - pop_at) if j >= n_prev else 9
            sc = 1 if dr > 0.2 else 0.4 + 3 * max(0, dr)
            red_flag(im, jx, jy, 170 * min(1.0, sc), ang=(-12 + 8 * (j % 4)), wave=t * 6 + j)
        rocco(im, W * 0.56, H * 0.95, 1100, moodR, talkR, t, act, act_t)
        if shown: txt(im, (W * 0.5, H * 0.12), ("RED FLAG" if shown == 1 else f"{shown} RED FLAGS"), 120, (255, 59, 59), sw=14, ang=-6)
    elif k == "fact":
        card(im, (90, 260, 990, 920), shot.get("title", "GTA 6 IS ON"), [(s, ok) for s, ok in shot["rows"]])
        if lt >= shot.get("stamp_at", 99):
            q = min(1.0, (lt - shot["stamp_at"]) / 0.15); txt(im, (W * 0.5, 800), shot.get("stamp", "NO PC VERSION"), int(110 + 60 * (1 - q)), (255, 59, 59), sw=14, ang=-10)
        rocco(im, W * 0.62, H * 0.98, 900, moodR, talkR, t, act, act_t)
    elif k == "trap":
        snapped = lt >= shot.get("snap_at", 99)
        mousetrap(im, W * 0.5, H * 0.40, 380, snapped, shot.get("label", "FREE GTA 6"))
        rocco(im, W * 0.75, H * 0.97, 760, moodR, talkR, t, act, act_t)
        if shot.get("penny"): penny(im, W * 0.24, H * 0.82, 330, moodP, talkP, t)
    elif k == "store":
        d = ImageDraw.Draw(im); d.rounded_rectangle([102, 276, 990, 836], 60, fill=(0, 0, 0, 60)); d.rounded_rectangle([90, 260, 978, 820], 60, fill=(230, 233, 238), outline=INK, width=10)
        d.ellipse([440, 300, 628, 488], fill=(52, 199, 89), outline=INK, width=10); d.line([(480, 400), (525, 445), (595, 345)], fill=(255, 255, 255), width=22)
        txt(im, (534, 580), shot.get("l1", "BUY IT ONLY IN THE"), 70, INK, sw=0); txt(im, (534, 690), shot.get("l2", "CONSOLE STORE"), 104, (40, 150, 60), sw=0)
        rocco(im, W * 0.55, H * 0.97, 950, moodR, talkR, t, act, act_t)
    elif k == "end":
        txt(im, (W / 2, H * 0.15), shot["l1"], 92, (255, 255, 255), sw=12)
        txt(im, (W / 2, H * 0.24), shot["l2"], 120, (255, 230, 60), sw=14)
        penny(im, W * 0.30, H * 0.62, 430, "happy", 0, t); rocco(im, W * 0.70, H * 0.78, 700, "thumbsup", 0, t)
        txt(im, (W / 2, H * 0.88), shot.get("l3", "Send this to someone who'd click it."), 58, (255, 255, 255), sw=8)
    txt(im, (W - 50, 70), "RED FLAG ROCCO", 44, (255, 59, 59), sw=6, anchor="rm")
    return im


def caption(im, chunk, active):
    if not chunk: return
    words = [w.upper() for w, *_ in chunk]; f = F(104); d = ImageDraw.Draw(im)
    sp = d.textlength(" ", font=f); ws = [d.textlength(w, font=f) for w in words]; tot = sum(ws) + sp * (len(ws) - 1)
    while tot > W * 0.9 and f.size > 60:
        f = F(f.size * 0.9); ws = [d.textlength(w, font=f) for w in words]; sp = d.textlength(" ", font=f); tot = sum(ws) + sp * (len(ws) - 1)
    x = (W - tot) / 2; y = H * 0.885
    for j, w in enumerate(words):
        hot = re.sub(r"[^A-Z]", "", w.upper()) in ("FREE", "RED", "FLAG", "FLAGS", "PC", "PASSWORDS", "MOUSETRAP", "STORE", "NO", "TWO", "WEEK", "CHEESE")
        col = (255, 226, 60) if (hot or j == active) else (232, 232, 234)
        d.text((x, y), w, font=f, fill=col, stroke_width=12, stroke_fill=INK, anchor="ls"); x += ws[j] + sp


def main():
    spec = json.load(open(sys.argv[1])); out = sys.argv[2]
    import datetime as _dt
    _sha = hashlib.sha1(open(os.path.abspath(__file__), "rb").read()).hexdigest()[:12]  # stamp at START (qc_gate step 0)
    cache = os.environ.get("FIN_TTS_CACHE", os.path.join(tempfile.gettempdir(), "fin_tts_cache")); os.makedirs(cache, exist_ok=True)
    lines = [tuple(x) for x in spec["lines"]]
    d, mp3 = dialogue(lines, cache)
    segs = sorted(d["voice_segments"], key=lambda s: s["start_time_seconds"])
    lt_ = {s["dialogue_input_index"]: (s["start_time_seconds"], s["end_time_seconds"]) for s in segs}
    words = words_from(d, lines)
    voice_end = max(e for _, e in lt_.values()); total = voice_end + spec.get("tail", 3.0)
    # ---- audio: dialogue + effects ----
    work = tempfile.mkdtemp(prefix="rc_"); wav = os.path.join(work, "v.wav")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", mp3, "-ar", "48000", "-ac", "1", wav], check=True)
    import soundfile as sf, make_video as mv
    y, sr = sf.read(wav, dtype="float32"); y = np.concatenate([y, np.zeros(int((total - len(y) / sr) * sr) + sr, np.float32)])
    rng = np.random.default_rng(3); fx = np.zeros_like(y)
    def at_line(i, frac): a, b = lt_[i]; return a + (b - a) * frac

    def word_t(i, w):  # start time of the first word in line i that matches w
        for x in words:
            if x[3] == i and re.sub(r"[^a-z]", "", x[0].lower()) == w.lower(): return x[1]
        return at_line(i, 0.5)
    for e in spec.get("sfx", []):
        t0 = (word_t(e["line"], e["word"]) if e.get("word") else at_line(e["line"], e.get("frac", 0))) + e.get("dt", 0)
        clip = getattr(mv, "sfx_" + e["name"])(sr, rng); i0 = int(t0 * sr)
        if clip.ndim > 1: clip = clip.mean(axis=1)
        fx[i0:i0 + len(clip)] += clip[:max(0, len(fx) - i0)] * e.get("gain", 0.35)
    mix = y + fx; mix = mix / max(1.0, np.abs(mix).max() / 0.95)
    sf.write(os.path.join(work, "mix.wav"), mix.astype(np.float32), sr)
    env, who = env_track(wav, segs)
    # ---- shot timeline ----
    shots = []
    for sh in spec["shots"]:
        if "line" in sh: t0, t1 = at_line(sh["line"], sh.get("from", 0)), at_line(sh["line"], sh.get("to", 1))
        else: t0, t1 = sh["t0"], sh["t1"]
        if sh.get("until_end"): t1 = total
        sh = dict(sh, _t0=t0, _t1=t1)
        for key in [k_ for k_ in sh if k_.endswith("_word")]:  # e.g. "snap_word": "mousetrap" -> "snap_at" (s after the shot starts)
            sh[key[:-5] + "_at"] = word_t(sh["line"], sh[key]) - t0
        shots.append(sh)
    for j in range(len(shots) - 1): shots[j]["_t1"] = shots[j + 1]["_t0"]  # no gaps
    shots[0]["_t0"] = 0.0; shots[-1]["_t1"] = total
    # ---- captions: 1-3 word chunks ----
    chunks = []; cur = []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or re.search(r"[.,!?…]$", w[0]) or (len(cur) and w is words[-1]): chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", os.path.join(work, "mix.wav"), "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-maxrate", "12M", "-bufsize", "24M",
                            "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                            "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                           stdin=subprocess.PIPE)
    nfr = int(total * FPS); cuts = []
    for fi in range(nfr):
        t = fi / FPS
        sh = next((s for s in shots if s["_t0"] <= t < s["_t1"]), shots[-1])
        if not cuts or cuts[-1] != round(sh["_t0"], 2): cuts.append(round(sh["_t0"], 2))
        lt = t - sh["_t0"]
        e = float(env[min(fi, len(env) - 1)]); w_ = who[min(fi, len(who) - 1)]
        im = compose(sh, lt, t, e if w_ == "R" else 0.0, e if w_ == "P" else 0.0, None)
        z = 1.0 + 0.035 * min(1.0, lt / max(0.5, sh["_t1"] - sh["_t0"])) + (0.06 * max(0.0, 1 - lt / 0.12))  # slow push + punch on the cut
        if z > 1.001:
            bw, bh = int(W * z), int(H * z); im = im.resize((bw, bh), Image.BILINEAR).crop(((bw - W) // 2, (bh - H) // 2, (bw - W) // 2 + W, (bh - H) // 2 + H))
        ch = next((c for c in chunks if c[0][1] - 0.05 <= t < (c[-1][2] + 0.25)), None)
        if ch and sh["kind"] != "end":
            act = max([j for j, w in enumerate(ch) if w[1] <= t] or [0]); caption(im, ch, act)
        if sh.get("hook") and lt < 2.2: txt(im, (W / 2, H * 0.08), sh["hook"], 104, (255, 255, 255), sw=12)
        enc.stdin.write(im.convert("RGB").tobytes())
    enc.stdin.close(); enc.wait()
    print(json.dumps({"rc": enc.returncode, "out": out, "seconds": round(total, 2), "cuts": cuts,
                      "renderer": "rc_render", "renderer_path": "work/rocco/rocco2/rc_render.py", "engine_sha": _sha,
                      "rendered_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                      "timings": [[round(lt_[i][0], 2), round(lt_[i][1] - lt_[i][0], 2)] for i in range(len(lines))] + [[round(voice_end, 2), round(total - voice_end, 2)]], "voices": VOICE, "model": "eleven_v3 text-to-dialogue",
                      "lines": [[s, tx, round(lt_[i][0], 2), round(lt_[i][1], 2)] for i, (s, tx) in enumerate(lines)]}))


if __name__ == "__main__":
    main()
