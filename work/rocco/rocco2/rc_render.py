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
VOICE = {"R": "hYvMKGEmKYHZz9qvD8oj", "P": "XeHmOH0wYkEbMfZqbCws", "S": "sKpya0iNfGuRwEz634c4"}  # S = Slick, the scammer fox
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
    if sender == "Slick": fox_avatar(im, x + 100, y + 86, 42)
    else: d.ellipse([x + 58, y + 44, x + 142, y + 128], fill=(52, 120, 246)); d.text((x + 100, y + 86), "$", font=F(56), fill=(255, 255, 255), anchor="mm")
    d.text((x + 160, y + 86), sender, font=F(52), fill=INK, anchor="lm")
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


def slick(im, cx, cy, s, mood="sly", talk=0.0, t=0.0):
    """Slick the scammer fox (always the butt of the joke). mood: sly|panic|laugh. Holds a phone."""
    d = ImageDraw.Draw(im, "RGBA"); u = s / 400; O = (255, 132, 50); OD = (214, 96, 30); CREAM = (250, 236, 214); SUIT = (118, 70, 170)
    cy = cy + (math.sin(t * 40) * 6 * u if mood == "panic" else 0)
    d.ellipse([cx - 170 * u, cy + 330 * u, cx + 170 * u, cy + 360 * u], fill=(0, 0, 0, 60))
    d.rounded_rectangle([cx - 150 * u, cy + 120 * u, cx + 150 * u, cy + 345 * u], 70 * u, fill=SUIT, outline=INK, width=int(8 * u))  # shady suit
    d.polygon([(cx - 40 * u, cy + 125 * u), (cx, cy + 230 * u), (cx + 40 * u, cy + 125 * u)], fill=CREAM, outline=INK)
    d.polygon([(cx - 14 * u, cy + 140 * u), (cx + 14 * u, cy + 140 * u), (cx + 8 * u, cy + 215 * u), (cx - 8 * u, cy + 215 * u)], fill=(230, 60, 60))  # tie
    for sx in (-1, 1):  # ears
        d.polygon([(cx + sx * 150 * u, cy - 70 * u), (cx + sx * 175 * u, cy - 235 * u), (cx + sx * 60 * u, cy - 135 * u)], fill=O, outline=INK)
        d.polygon([(cx + sx * 140 * u, cy - 95 * u), (cx + sx * 158 * u, cy - 195 * u), (cx + sx * 85 * u, cy - 135 * u)], fill=INK)
    d.ellipse([cx - 175 * u, cy - 155 * u, cx + 175 * u, cy + 145 * u], fill=O, outline=INK, width=int(8 * u))
    d.polygon([(cx - 165 * u, cy + 10 * u), (cx, cy + 150 * u), (cx + 165 * u, cy + 10 * u), (cx, cy + 40 * u)], fill=CREAM)  # muzzle
    d.ellipse([cx - 22 * u, cy + 20 * u, cx + 22 * u, cy + 52 * u], fill=INK)  # nose
    ey = cy - 45 * u
    for sx in (-1, 1):
        ex = cx + sx * 72 * u
        if mood == "panic":
            r = 34 * u; d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(240, 240, 240), outline=INK, width=int(6 * u)); d.ellipse([ex - 8 * u, ey - 8 * u, ex + 8 * u, ey + 8 * u], fill=INK)
        else:  # half-closed sly eyes
            d.ellipse([ex - 32 * u, ey - 20 * u, ex + 32 * u, ey + 20 * u], fill=(250, 230, 120), outline=INK, width=int(6 * u))
            d.ellipse([ex - 9 * u + sx * 8 * u, ey - 9 * u, ex + 9 * u + sx * 8 * u, ey + 9 * u], fill=INK)
            d.rectangle([ex - 34 * u, ey - 24 * u, ex + 34 * u, ey - 4 * u], fill=O); d.line([(ex - 34 * u, ey - 4 * u), (ex + 34 * u, ey - 4 * u)], fill=INK, width=int(6 * u))
    mo = talk * 40 * u + (30 * u if mood == "panic" else 0)
    if mo > 4 * u: d.ellipse([cx - 40 * u, cy + 70 * u, cx + 40 * u, cy + 76 * u + mo], fill=INK)
    else: d.arc([cx - 70 * u, cy + 40 * u, cx + 70 * u, cy + 110 * u], 15, 165, fill=INK, width=int(8 * u))  # grin
    if mood == "panic":
        for sx in (-1, 1): d.ellipse([cx + sx * 175 * u, cy - 150 * u, cx + sx * 175 * u + 26 * u, cy - 112 * u], fill=(140, 210, 255), outline=INK, width=int(4 * u))
    # phone in hand
    px, py = cx + 150 * u, cy + 150 * u
    d.rounded_rectangle([px - 45 * u, py - 80 * u, px + 45 * u, py + 80 * u], 16 * u, fill=INK); d.rounded_rectangle([px - 36 * u, py - 70 * u, px + 36 * u, py + 70 * u], 12 * u, fill=(120, 220, 140))
    d.ellipse([px - 70 * u, py + 20 * u, px - 10 * u, py + 80 * u], fill=O, outline=INK, width=int(6 * u))  # paw


def callout(im, cx, cy, r, lt, label=None, at=0.15):
    """Red hand-drawn circle that draws itself (0.3 s) + label pill: the 'look HERE' device of PSA winners."""
    q = max(0.0, min(1.0, (lt - at) / 0.3))
    if q <= 0: return
    d = ImageDraw.Draw(im)
    d.arc([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8], -90, -90 + 360 * q, fill=(255, 40, 40), width=16)
    if label and q >= 1:
        f = F(70); tw = d.textlength(label, font=f); lx = min(W - tw - 70, max(40, cx - tw / 2)); ly = cy + r * 0.8 + 30
        d.rounded_rectangle([lx - 26, ly - 10, lx + tw + 26, ly + 86], 30, fill=(255, 40, 40), outline=INK, width=6)
        d.text((lx, ly + 38), label, font=f, fill=(240, 240, 240), anchor="lm")


def footage_img(frames, fsz, k, n, kb="in", bright=1.0, blur=0):
    BW, BH = fsz; fr = Image.frombytes("RGB", (BW, BH), frames[min(k, len(frames) - 1)])
    p = k / max(1, n - 1); z = 1.0 + 0.06 * (p if kb == "in" else 1 - p)
    cw, ch = int(BW / z / 1.1), int(BH / z / 1.1); x0 = (BW - cw) // 2; y0 = (BH - ch) // 2
    im = fr.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BILINEAR)
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    a_ = np.asarray(im, np.float32) * bright; Y = a_ @ np.array([0.299, 0.587, 0.114], np.float32)
    a_ *= np.minimum(1.0, 226.0 / np.maximum(Y, 1.0))[..., None]
    return Image.fromarray(a_.clip(0, 255).astype(np.uint8)).convert("RGBA")


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
        who[a:b] = next((k for k, v in VOICE.items() if v == s["voice_id"]), "R")
    return e, who


def compose(shot, lt, t, talkR, talkP, extra, talkS=0.0, fimg=None, fimg2=None):
    k = shot["kind"]; im = fimg.copy() if fimg is not None else setbg(shot.get("set", "yellow"))
    moodR = shot.get("r", "happy"); moodP = shot.get("p", "happy")
    act = shot.get("act"); act_t = lt - shot.get("act_at", 0)
    if act and not (0 <= act_t < shot.get("act_len", 1.0)): act = None
    if k == "slick":  # the scammer in his lair
        slick(im, W * (0.40 if shot.get("r_peek") else 0.5), H * 0.50, 760, shot.get("s", "sly"), talkS, t)
        if shot.get("r_peek"): rocco(im, W * 0.84, H * 1.0, 820, moodR, talkR, t, act, act_t)  # Rocco stays on screen (preflight #12)
        if shot.get("msg") and lt >= shot.get("msg_at", 0): txt(im, (W * 0.5, H * 0.17), shot["msg"], 96, (255, 226, 60), sw=12, ang=-5)
    elif k == "insert":  # real footage + red circle callout (+ reacting character); the callout is drawn ON TOP of the character
        who = shot.get("who")
        if who == "r": rocco(im, W * shot.get("rx", 0.76), H * 1.0, 1000, moodR, talkR, t, act, act_t, flip=shot.get("rx", 0.76) < 0.5)
        elif who == "p": penny(im, W * 0.80, H * 0.86, 330, moodP, talkP, t)
        elif who == "s": slick(im, W * 0.78, H * 0.80, 330, shot.get("s", "sly"), talkS, t)
        c = shot.get("circle")
        if c: callout(im, c[0] * W, c[1] * H, c[2] * W, lt, shot.get("label"), shot.get("circle_at", 0.15))
        if shot.get("card"): txt(im, (W * 0.5, H * 0.16), shot["card"], 104, (255, 226, 60), sw=14, ang=-4)
    elif k == "split":  # two places at once: top = fimg2 (e.g. the scammer), bottom = fimg (the victim)
        top = (fimg2 if fimg2 is not None else setbg("sky")).crop((0, int(H * 0.2), W, int(H * 0.7))).resize((W, H // 2))
        im.alpha_composite(top.convert("RGBA"), (0, 0)); dd = ImageDraw.Draw(im); dd.rectangle([0, H // 2 - 6, W, H // 2 + 6], fill=(232, 232, 234))
        slick(im, W * 0.5, H * 0.26, 420, shot.get("s", "sly"), talkS, t)
        penny(im, W * 0.30, H * 0.80, 400, moodP, talkP, t)
        c = shot.get("circle")
        if c: callout(im, c[0] * W, c[1] * H, c[2] * W, lt, shot.get("label"), shot.get("circle_at", 0.15))
    elif k == "call":  # phone-call skit (vcPnUMJNdkw format): top = scammer's place, bottom = victim's place, live call bar + timer
        top = (fimg2 if fimg2 is not None else setbg("sky")).crop((0, int(H * 0.15), W, int(H * 0.65))).resize((W, H // 2))
        im.alpha_composite(top.convert("RGBA"), (0, 0))
        slick(im, W * 0.5, H * 0.27, 440, shot.get("s", "sly"), talkS, t)
        penny(im, W * (0.36 if shot.get("r_whisper") else 0.5), H * 0.76, 470, moodP, talkP, t)
        if shot.get("r_whisper"):  # Rocco coaching Penny from the side
            rocco(im, W * 0.80, H * 1.0, 760, moodR, talkR, t, act, act_t)
            if talkR > 0.05: txt(im, (W * 0.80, H * 0.60), "psst...", 54, (255, 226, 60), sw=8, ang=6)
        d = ImageDraw.Draw(im); by = H // 2
        d.rounded_rectangle([40, by - 58, W - 40, by + 58], 58, fill=(20, 22, 28, 235))
        d.ellipse([70, by - 30, 130, by + 30], fill=(52, 199, 89)); d.text((160, by), shot.get("caller", 'CALLER: "YOUR BANK"'), font=F(46), fill=(232, 232, 234), anchor="lm")
        secs = int(t - shot.get("_call_t0", 0)); d.text((W - 80, by), f"{secs // 60:02d}:{secs % 60:02d}", font=F(46), fill=(232, 232, 234), anchor="rm")
        if shot.get("msg") and lt >= shot.get("msg_at", 0): txt(im, (W * 0.5, H * 0.08), shot["msg"], 84, (255, 226, 60), sw=12, ang=-4)
    elif k == "two":
        penny(im, W * 0.30, H * 0.60, 440, moodP, talkP, t)
        rocco(im, W * 0.70, H * 0.76, 700, moodR, talkR, t, act, act_t)
    elif k == "cu_r":
        rocco(im, W * 0.52, H * 0.93, 1250, moodR, talkR, t, act, act_t)
    elif k == "cu_p":  # Penny big, Rocco reacting from the right edge (Rocco on screen >= 70% of the frames)
        penny(im, W * 0.42, H * 0.52, 760, moodP, talkP, t)
        rocco(im, W * 0.88, H * 0.99, 700, moodR, talkR, t, act, act_t)
    elif k == "phone":
        phone(im, 120, 200, 840, 1000, shot["msgs"], lt, shot.get("sender", "Slick"))
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
    elif k == "math":  # damage math (winner moment #3): rows pop in on their word, total stamps last
        d = ImageDraw.Draw(im); d.rounded_rectangle([102, 236, 990, 1000], 60, fill=(0, 0, 0, 60)); d.rounded_rectangle([90, 220, 978, 984], 60, fill=(230, 233, 238), outline=INK, width=10)
        txt(im, (534, 300), shot.get("title", "YOUR MONEY"), 70, INK, sw=0)
        for j, (lab, val, good) in enumerate(shot["rows"]):
            at = shot.get(f"r{j}_at", 0.2 + 0.6 * j)
            if lt < at: break
            q = min(1.0, (lt - at) / 0.15); yy = 420 + j * 150
            d.text((150, yy), lab, font=F(62), fill=INK, anchor="lm")
            txt(im, (930, yy), val, int(84 + 30 * (1 - q)), (40, 170, 70) if good else (220, 40, 40), sw=0, anchor="rm")
        if lt >= shot.get("total_at", 99):
            q = min(1.0, (lt - shot["total_at"]) / 0.15); d.line([(150, 860), (930, 860)], fill=INK, width=8)
            txt(im, (534, 925), shot.get("total", "TOTAL: -$1,000"), int(96 + 50 * (1 - q)), (220, 40, 40), sw=0, ang=-3)
        rocco(im, W * 0.70, H * 0.99, 760, moodR, talkR, t, act, act_t)
        if shot.get("penny"): penny(im, W * 0.22, H * 0.80, 300, moodP, talkP, t)
    elif k == "end":
        txt(im, (W / 2, H * 0.15), shot["l1"], 92, (255, 255, 255), sw=12)
        txt(im, (W / 2, H * 0.24), shot["l2"], 120, (255, 230, 60), sw=14)
        penny(im, W * 0.30, H * 0.62, 430, "happy", 0, t); rocco(im, W * 0.70, H * 0.78, 700, "thumbsup", 0, t)
        txt(im, (W / 2, H * 0.88), shot.get("l3", "Send this to someone who'd click it."), 58, (255, 255, 255), sw=8)
    if shot.get("src"):  # source line on a small dark plate (Review 2 #6)
        d = ImageDraw.Draw(im); f_ = F(34); tw = d.textlength(shot["src"], font=f_)
        d.rounded_rectangle([W / 2 - tw / 2 - 20, H * 0.785 - 28, W / 2 + tw / 2 + 20, H * 0.785 + 28], 16, fill=(0, 0, 0, 150))
        d.text((W / 2, H * 0.785), shot["src"], font=f_, fill=(232, 232, 234), anchor="mm")
    txt(im, (W - 50, 70), "RED FLAG ROCCO", 44, (255, 59, 59), sw=6, anchor="rm")
    return im


LINE_SPK = []  # speaker letter per dialogue line (set in main)
HOT = set()     # extra spec words drawn yellow
DANGER = {"STOLEN", "SCAM", "SCAMMER", "MINUS", "NEVER", "DON'T", "DONT", "BLOCKED", "FAKE", "RED", "FLAG", "FLAGS", "PASSWORDS", "MOUSETRAP", "NO"}
SPK_COL = {"P": (255, 226, 60), "S": (120, 220, 255), "R": (232, 232, 234)}  # victim yellow, scammer cyan, Rocco white


def caption(im, chunk, active):
    """1-3 words; colour by speaker (winner moment #10); $/money green, danger red, active word pops yellow-white."""
    if not chunk: return
    words = [w.upper() for w, *_ in chunk]; f = F(104); d = ImageDraw.Draw(im)
    spk = LINE_SPK[chunk[0][3]] if LINE_SPK and chunk[0][3] < len(LINE_SPK) else "R"
    sp = d.textlength(" ", font=f); ws = [d.textlength(w, font=f) for w in words]; tot = sum(ws) + sp * (len(ws) - 1)
    while tot > W * 0.9 and f.size > 60:
        f = F(f.size * 0.9); ws = [d.textlength(w, font=f) for w in words]; sp = d.textlength(" ", font=f); tot = sum(ws) + sp * (len(ws) - 1)
    x = (W - tot) / 2; y = H * 0.885
    for j, w in enumerate(words):
        core = re.sub(r"[^A-Z0-9$']", "", w)
        if "$" in w or core in ("THOUSAND", "MONEY", "CASH", "DOLLARS", "RICH"): col = (90, 230, 120)
        elif core in DANGER: col = (255, 80, 80)
        elif core in HOT: col = (255, 226, 60)
        else: col = SPK_COL.get(spk, (232, 232, 234))
        if j == active: col = tuple(min(255, int(c * 0.6 + 255 * 0.4)) for c in col)
        d.text((x, y), w, font=f, fill=col, stroke_width=12, stroke_fill=INK, anchor="ls"); x += ws[j] + sp


def main():
    spec = json.load(open(sys.argv[1])); out = sys.argv[2]
    import datetime as _dt
    _sha = hashlib.sha1(open(os.path.abspath(__file__), "rb").read()).hexdigest()[:12]  # stamp at START (qc_gate step 0)
    cache = os.environ.get("FIN_TTS_CACHE", os.path.join(tempfile.gettempdir(), "fin_tts_cache")); os.makedirs(cache, exist_ok=True)
    lines = [tuple(x) for x in spec["lines"]]
    LINE_SPK[:] = [a for a, _ in lines]; HOT.update(w.upper() for w in spec.get("hot", []))
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
            _ln, _w = (int(sh[key].split(":")[0]), sh[key].split(":")[1]) if ":" in sh[key] else (sh["line"], sh[key])  # "11:keeps" = a word of another line
            sh[key[:-5] + "_at"] = word_t(_ln, _w) - t0
        shots.append(sh)
    for j in range(len(shots) - 1): shots[j]["_t1"] = shots[j + 1]["_t0"]  # no gaps
    _c0 = next((x["_t0"] for x in shots if x["kind"] == "call"), 0.0)
    for x in shots: x["_call_t0"] = _c0
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
    import make_video as mv2
    def load(sh):  # decode one shot's real footage when it starts (bg = main picture, bg2 = top half of a split)
        n_ = int((sh["_t1"] - sh["_t0"]) * FPS) + 2
        for key in ("bg", "bg2"):
            if sh.get(key) and os.path.exists(sh[key]):
                fr_, fsz_ = mv2.broll_frames(sh[key], W, H, n_, sh.get(key + "_start", 0))
                sh["_" + key] = (fr_, fsz_, n_) if fr_ else None
    _cur = None
    nfr = int(total * FPS); cuts = []
    for fi in range(nfr):
        t = fi / FPS
        sh = next((s for s in shots if s["_t0"] <= t < s["_t1"]), shots[-1])
        if sh is not _cur:  # free the previous shot's frames (a 60 s video no longer holds every clip in memory)
            if _cur is not None: _cur.pop("_bg", None); _cur.pop("_bg2", None)
            load(sh); _cur = sh
        if not cuts or cuts[-1] != round(sh["_t0"], 2): cuts.append(round(sh["_t0"], 2))
        lt = t - sh["_t0"]
        e = float(env[min(fi, len(env) - 1)]); w_ = who[min(fi, len(who) - 1)]
        kk = int(lt * FPS)
        fimg = footage_img(*sh["_bg"][:2], kk, sh["_bg"][2], sh.get("kb", "in"), sh.get("bright", 1.1), sh.get("blur", 0)) if sh.get("_bg") else None
        fimg2 = footage_img(*sh["_bg2"][:2], kk, sh["_bg2"][2], "in", sh.get("bright2", 1.2), 0) if sh.get("_bg2") else None
        im = compose(sh, lt, t, e if w_ == "R" else 0.0, e if w_ == "P" else 0.0, None, e if w_ == "S" else 0.0, fimg, fimg2)
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
