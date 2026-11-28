"""Graphic shot kinds for rc_render (2026-11-22): 10+ distinct visual formats for Buck (Financier) and Rocco.
Each kind: fn(im, sh, lt, t, talk, R) draws onto the 1080x1920 RGBA frame `im` (background already there: sh "bg" image/footage,
or sh "set" colour, or the kind paints its own). lt = seconds since the shot started. R = the rc_render module (W, H, buck(), ...).
Common optional keys on every shot:
  "buck": {"x": 0.8, "y": 0.97, "h": 700, "mood": "point", "flip": false}   Buck host (feet at y*H), talks when line speaker is B
  "font": "Anton" | "Bebas" | "Bangers" | "Abril" | "Archivo" | "BlackOps" | "Courier" | "Hand" | "Marker" | "Pixel" | "Typewriter" | "Monoton" | "Lilita"
"""
import math, os, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
FD = os.path.join(ROOT, "assets", "fonts")
FONTS = {"Anton": "/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf", "Bebas": FD + "/BebasNeue-Regular.ttf",
         "Bangers": FD + "/Bangers-Regular.ttf", "Abril": FD + "/AbrilFatface-Regular.ttf", "Archivo": FD + "/ArchivoBlack-Regular.ttf",
         "BlackOps": FD + "/BlackOpsOne-Regular.ttf", "Courier": FD + "/CourierPrime-Bold.ttf", "Hand": FD + "/PatrickHand-Regular.ttf",
         "Marker": FD + "/PermanentMarker-Regular.ttf", "Pixel": FD + "/PressStart2P-Regular.ttf", "Typewriter": FD + "/SpecialElite-Regular.ttf",
         "Monoton": FD + "/Monoton-Regular.ttf", "Lilita": FD + "/LilitaOne-Regular.ttf"}
_FC = {}
W, H = 1080, 1920
INK = (20, 18, 26, 255); WHITE = (232, 232, 234, 255); GOLD = (255, 205, 60, 255); GREEN = (46, 204, 113, 255); RED = (235, 64, 52, 255)


def F(name, size):
    k = (name, int(size))
    if k not in _FC:
        p = FONTS.get(name, FONTS["Anton"]); _FC[k] = ImageFont.truetype(p if os.path.exists(p) else FONTS["Anton"], int(size))
    return _FC[k]


def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3


def back(x):  # ease-out-back (overshoot ~10 %)
    x = max(0.0, min(1.0, x)); c = 1.70158; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def col(c, a=255):
    if isinstance(c, str): c = c.lstrip("#"); c = tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
    return tuple(c[:3]) + (a,)


def text(im, xy, s, font="Anton", size=90, fill=WHITE, stroke=INK, sw=8, anchor="mm", scale=1.0, ang=0, maxw=None):
    """Draw text; scale/ang animate it (pop-ins) by rendering on a temp layer."""
    f = F(font, size)
    if maxw:
        while f.getlength(s) > maxw and size > 20: size -= 4; f = F(font, size)
    if scale == 1.0 and ang == 0:
        ImageDraw.Draw(im).text(xy, s, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke, anchor=anchor); return
    if scale <= 0.01: return
    bb = f.getbbox(s, stroke_width=sw); w_, h_ = bb[2] - bb[0] + 20, bb[3] - bb[1] + 20
    lay = Image.new("RGBA", (w_, h_), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((w_ / 2, h_ / 2), s, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke, anchor="mm")
    lay = lay.resize((max(1, int(w_ * scale)), max(1, int(h_ * scale))), Image.LANCZOS)
    if ang: lay = lay.rotate(ang, resample=Image.BICUBIC, expand=True)
    x, y = xy
    if anchor[0] == "l": x += lay.width / 2
    elif anchor[0] == "r": x -= lay.width / 2
    im.alpha_composite(lay, (int(x - lay.width / 2), int(y - lay.height / 2)))


def panel(im, box, fill=(232, 232, 236, 235), r=40, outline=INK, ow=8, shadow=True):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if shadow: d.rounded_rectangle([box[0] + 12, box[1] + 14, box[2] + 12, box[3] + 14], r, fill=(0, 0, 0, 70))
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=ow); im.alpha_composite(lay)


def money(v, dec=0, unit=""):
    a = abs(v)
    if unit == "auto":
        for d_, u in ((1e12, " TRILLION"), (1e9, " BILLION"), (1e6, " MILLION")):
            if a >= d_:
                x = f"{v / d_:,.{(dec or 1) if v / d_ < 100 else 0}f}"
                if "." in x: x = x.rstrip("0").rstrip(".")
                return "$" + x + u
        return f"${v:,.{dec}f}"
    return f"${v:,.{dec}f}"


SPK = {"rocco": "R", "penny": "P", "slick": "S"}


def cast(im, sh, t, talk, R):
    """3D cast inside a graphic shot: "cast": [{"who": "rocco", "x": .8, "y": .98, "h": 900, "mood": "sideeye", "pose": "point", "flip": false}]"""
    for c in sh.get("cast", []):
        if getattr(R, "LIB3D", ""):
            R.char3d(im, c["who"], W * c.get("x", 0.5), H * c.get("y", 0.98), c.get("h", 900), R.MAP3D.get(c["who"], {}).get(c.get("mood", "happy"), c.get("mood", "happy")) if False else c.get("mood", "happy"),
                     talk.get(SPK[c["who"]], 0.0), t, c.get("flip", False), c.get("pose"))


def host(im, sh, t, talk, R):
    cast(im, sh, t, talk, R)
    b = sh.get("buck")
    if b: R.buck(im, W * b.get("x", 0.8), H * b.get("y", 0.97), b.get("h", 700), b.get("mood", "happy"), talk.get("B", 0.0), t, b.get("flip", False))


def footage(sh): return bool(sh.get("bg"))  # any real background (footage or a 3D-film set image)


def dim(im, a=110):
    im.alpha_composite(Image.new("RGBA", im.size, (0, 0, 0, a)))


def gradient(im, c1, c2, sh=None):
    if sh is not None and footage(sh): dim(im, sh.get("dim", 120)); return
    a = Image.new("RGBA", (1, 2)); a.putpixel((0, 0), col(c1)); a.putpixel((0, 1), col(c2))
    im.alpha_composite(a.resize(im.size, Image.BILINEAR))


# ---------------------------------------------------------------- 1. counter: a number racing up live
def k_counter(im, sh, lt, t, talk, R):
    if sh.get("dim", 90): dim(im, sh.get("dim", 90))
    fnt = sh.get("font", "Anton"); at = sh.get("at", 0.2); dur = sh.get("dur", 2.5)
    p = ease((lt - at) / dur); v = sh.get("start", 0) + (sh["to"] - sh.get("start", 0)) * p
    if sh.get("label"): text(im, (W / 2, H * sh.get("label_y", 0.22)), sh["label"], fnt, 84, col(sh.get("label_col", (232, 232, 234))), maxw=W * 0.9)
    s = sh.get("prefix", "$") + f"{v:,.{sh.get('dec', 0)}f}" + sh.get("suffix", "")
    pop = 1.0 + 0.08 * math.sin(min(1, max(0, (lt - at - dur) / 0.25)) * math.pi)
    text(im, (W / 2, H * sh.get("y", 0.4)), s, fnt, sh.get("size", 170), col(sh.get("color", GOLD)), sw=10, scale=pop, maxw=W * 0.94)
    if sh.get("sub") and lt >= at + dur * 0.6: text(im, (W / 2, H * sh.get("y", 0.4) + 150), sh["sub"], fnt, 64, WHITE, maxw=W * 0.9, scale=back((lt - at - dur * 0.6) / 0.3))
    if sh.get("ticker"):  # "+$43,866" chips flying up every 1/rate s
        rate = sh.get("rate", 1.0)
        for i in range(6):
            tt = (lt * rate - i / 6.0) % 1.0
            text(im, (W * (0.2 + 0.6 * ((i * 37) % 10) / 10), H * (0.75 - 0.25 * tt)), sh["ticker"], fnt, 56, col(GREEN, int(255 * (1 - tt))), sw=5)
    host(im, sh, t, talk, R)


# ---------------------------------------------------------------- 2. scale: money stack climbs a log altitude ruler (clouds -> space -> satellites)
def k_scale(im, sh, lt, t, talk, R):
    fnt = sh.get("font", "Bebas"); at = sh.get("at", 0.2); dur = sh.get("dur", 3.0)
    top_v = sh["stack_m"]; marks = sh.get("marks", [])  # [[value, "LABEL"], ...] in the same unit
    lo = sh.get("lo", 0.1); hi = top_v * 1.6; yb, yt = H * 0.86, H * 0.12
    Y = lambda v: yb - (yb - yt) * (math.log10(max(v, lo)) - math.log10(lo)) / (math.log10(hi) - math.log10(lo))
    p = ease((lt - at) / dur); cur = lo * (top_v / lo) ** p if p > 0 else lo
    sky = max(0.0, min(1.0, (math.log10(cur) - math.log10(lo)) / (math.log10(hi) - math.log10(lo))))
    if footage(sh): dim(im, int(60 + 120 * sky)); d = ImageDraw.Draw(im)
    else:
        gradient(im, tuple(int(a_ + (b_ - a_) * sky) for a_, b_ in zip((10, 12, 40), (2, 2, 10))), tuple(int(a_ + (b_ - a_) * sky) for a_, b_ in zip((110, 190, 255), (20, 30, 70))))
        d = ImageDraw.Draw(im); rnd = random.Random(3)
        for _ in range(int(160 * sky)): x, y = rnd.randrange(W), rnd.randrange(int(H * 0.7)); d.point((x, y), fill=(232, 232, 236, 200))
    d.line([(W * 0.62, yt), (W * 0.62, yb)], fill=(210, 210, 214, 255), width=4)
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay); dec = 10 ** math.floor(math.log10(lo))
    while dec <= hi:  # log-scale grid: one line per decade (0.1, 1, 10, 100 ... km)
        y = Y(dec)
        if yt <= y <= yb:
            for xx in range(30, W - 30, 36): dl.line([(xx, y), (xx + 20, y)], fill=(255, 255, 255, 70), width=3)
            _u = sh.get("unit", "km").upper(); text(lay, (40, y - 22), f"{dec:,.0f} {_u}" if dec >= 1 else f"{dec} {_u}", "Bebas", 34, (255, 255, 255, 150), sw=0, anchor="lm")
        dec *= 10
    im.alpha_composite(lay)
    for v, lab in marks:
        y = Y(v); d.line([(W * 0.6, y), (W * 0.66, y)], fill=WHITE, width=5)
        text(im, (W * 0.68, y), lab, fnt, 50, WHITE if cur >= v else (200, 200, 210, 200), sw=5, anchor="lm", maxw=W * 0.31)
    sx, bw = W * 0.3, W * 0.22; ytop = Y(cur)
    for i, yy in enumerate(range(int(yb), int(ytop), -12)):
        d.rectangle([sx - bw / 2, yy - 11, sx + bw / 2, yy], fill=(60, 170, 90, 255) if i % 2 else (40, 140, 70, 255))
    d.rectangle([sx - bw / 2, ytop, sx + bw / 2, yb], outline=(20, 80, 40, 255), width=4)
    text(im, (sx, ytop - 55), f"{cur:,.0f} {sh.get('unit', 'km')}" if cur >= 10 else f"{cur:,.1f} {sh.get('unit', 'km')}", fnt, 84, GOLD, sw=7)
    text(im, (sx, yb + 55), sh.get("stack_label", "$100 BILLS"), fnt, 52, WHITE, sw=5)
    if sh.get("title"): text(im, (W * 0.44, H * 0.075), sh["title"], fnt, 76, WHITE, sw=8, maxw=W * 0.8)
    host(im, sh, t, talk, R)


# ---------------------------------------------------------------- 3. bars: bar race (ranking)
def k_bars(im, sh, lt, t, talk, R):
    if footage(sh): dim(im, sh.get("dim", 130))
    elif sh.get("bgcol"): gradient(im, sh["bgcol"][0], sh["bgcol"][1])
    fnt = sh.get("font", "Archivo"); items = sh["items"]; mx = max(v for _, v, *_ in items); at = sh.get("at", 0.1)
    if sh.get("title"): text(im, (W / 2, H * 0.1), sh["title"], fnt, 78, GOLD, sw=7, maxw=W * 0.92)
    y0 = H * 0.17; gap = min(300, H * 0.58 / max(1, len(items))); d = ImageDraw.Draw(im); new = sh.get("new", 0)
    for i, it in enumerate(items):
        lab, v = it[0], it[1]; c = col(it[2] if len(it) > 2 else (80 + 30 * i % 170, 140, 230))
        p = ease((lt - at) / sh.get("dur", 1.2)) if i == new else 1.0
        y = y0 + i * gap; bh = gap * 0.5; bl = (W - 140) * v / mx * p
        text(im, (60, y + gap * 0.12), lab, fnt, 58, WHITE, sw=6, anchor="lm", maxw=W - 120)
        d.rounded_rectangle([60, y + gap * 0.28, 60 + max(14, bl), y + gap * 0.28 + bh], 22, fill=c)
        vs = sh.get("fmt", "${:,.0f}").format(v * p) + sh.get("suffix", "")
        inside = bl > W * 0.55
        text(im, (60 + bl - 24 if inside else 80 + bl, y + gap * 0.28 + bh / 2), vs, fnt, 64, WHITE, sw=7, anchor="rm" if inside else "lm")
    if not sh.get("buck"): sh = dict(sh, buck={"x": 0.84, "y": 1.0, "h": 600, "mood": "point"})
    host(im, sh, t, talk, R)


# ---------------------------------------------------------------- 4. line: price/time-lapse line drawing itself
def k_line(im, sh, lt, t, talk, R):
    if sh.get("dim", 140): dim(im, sh.get("dim", 140))
    fnt = sh.get("font", "Bebas"); pts = sh["points"]; at = sh.get("at", 0.2); dur = sh.get("dur", 3.5)
    x0, x1, y0, y1 = 110, W - 90, H * 0.66, H * 0.26
    vs = [v for _, v in pts]; lo, hi = min(0, min(vs)), max(vs) * 1.1
    P = [(x0 + (x1 - x0) * i / (len(pts) - 1), y0 - (y0 - y1) * (v - lo) / (hi - lo)) for i, (_, v) in enumerate(pts)]
    d = ImageDraw.Draw(im); d.line([(x0, y0), (x1, y0)], fill=(210, 210, 214, 255), width=4)
    for i in (0, len(pts) - 1): text(im, (P[i][0], y0 + 50), str(pts[i][0]), fnt, 52, WHITE, sw=5)
    p = ease((lt - at) / dur) * (len(P) - 1); k = int(p); fr = p - k
    seg = P[:k + 1] + ([(P[k][0] + (P[k + 1][0] - P[k][0]) * fr, P[k][1] + (P[k + 1][1] - P[k][1]) * fr)] if k + 1 < len(P) else [])
    if len(seg) > 1:
        poly = seg + [(seg[-1][0], y0), (x0, y0)]; d.polygon(poly, fill=col(sh.get("color", GREEN), 60)); d.line(seg, fill=col(sh.get("color", GREEN)), width=12, joint="curve")
    cx, cy = seg[-1]; d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=WHITE, outline=INK, width=4)
    iv = min(len(pts) - 1, k + (1 if fr > 0.5 else 0))
    text(im, (W / 2, H * 0.16), sh.get("fmt", "${:,.2f}").format(pts[iv][1]), fnt, 150, col(sh.get("color", GOLD)), sw=9)
    text(im, (W / 2, H * 0.16 + 110), str(pts[iv][0]), fnt, 64, WHITE, sw=6)
    if sh.get("title"): text(im, (W / 2, H * 0.06), sh["title"], fnt, 70, WHITE, sw=7, maxw=W * 0.92)
    host(im, sh, t, talk, R)


# ---------------------------------------------------------------- 5. quiz: guess the price / which one (timer + reveal)
def k_quiz(im, sh, lt, t, talk, R):
    if footage(sh): dim(im, sh.get("dim", 130))
    elif sh.get("bgcol"): gradient(im, sh["bgcol"][0], sh["bgcol"][1])
    fnt = sh.get("font", "Archivo"); opts = sh["options"]; ans = sh.get("answer", 0); rv = sh.get("reveal_at", 3.0)
    panel(im, [60, H * 0.07, W - 60, H * 0.24], fill=(232, 232, 236, 245))
    ql = sh["q"].split("\n")
    for qi, qq in enumerate(ql): text(im, (W / 2, H * 0.155 + (qi - (len(ql) - 1) / 2) * 92), qq, fnt, 72, INK, stroke=INK, sw=0, maxw=W * 0.82)
    for i, o in enumerate(opts):
        y = H * 0.30 + i * 210; p = back((lt - sh.get("intro", 0.15) - i * 0.18) / 0.35)
        if p <= 0: continue
        c = (232, 232, 236, 240)
        if lt >= rv: c = (46, 204, 113, 255) if i == ans else (120, 120, 130, 200)
        bx = [80 + (1 - p) * -900, y, W - 80 + (1 - p) * -900, y + 170]
        panel(im, bx, fill=c, r=50)
        text(im, (bx[0] + 90, y + 85), "ABC"[i], fnt, 80, GOLD, sw=7)
        text(im, (bx[0] + 190, y + 85), o, fnt, 62, INK, sw=0, anchor="lm", maxw=W * 0.66)
    if lt < rv and sh.get("timer", True):  # countdown ring
        left = max(0.0, rv - lt); cx, cy, r = W - 150, H * 0.30 - 70, 60; d = ImageDraw.Draw(im)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(20, 20, 30, 220))
        d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * left / rv, fill=GOLD, width=12)
        text(im, (cx, cy), str(int(math.ceil(left))), fnt, 64, WHITE, sw=4)
    elif sh.get("reveal"): text(im, (W / 2, H * 0.30 + len(opts) * 210 + 60), sh["reveal"], fnt, 70, GOLD, sw=7, scale=back((lt - rv) / 0.3), maxw=W * 0.9)
    host(im, sh, t, talk, R)


# ---------------------------------------------------------------- 6. receipt: facts print as receipt lines, total + stamp
def k_receipt(im, sh, lt, t, talk, R):
    gradient(im, (40, 34, 30), (18, 16, 14), sh)
    fnt = sh.get("font", "Courier"); rows = sh["rows"]; step = sh.get("step", 0.55); RH = 150
    done = lt > 0.2 + step * len(rows)
    n = min(len(rows), int(max(0, lt - 0.2) / step) + 1) if rows else 0; h_ = 420 + RH * n + (260 if done else 60)
    x0, x1, y0 = 70, W - 70, H * 0.07
    d = ImageDraw.Draw(im); d.rectangle([x0 + 16, y0 + 16, x1 + 16, y0 + h_ + 16], fill=(0, 0, 0, 90)); d.rectangle([x0, y0, x1, y0 + h_], fill=(232, 228, 218, 255))
    for zx in range(int(x0), int(x1), 36): d.polygon([(zx, y0 + h_), (zx + 18, y0 + h_ + 22), (zx + 36, y0 + h_)], fill=(232, 228, 218, 255))
    text(im, (W / 2, y0 + 110), sh.get("title", "RECEIPT"), fnt, 92, INK, sw=0, maxw=x1 - x0 - 60); d.line([(x0 + 40, y0 + 200), (x1 - 40, y0 + 200)], fill=INK, width=4)
    text(im, (W / 2, y0 + 265), sh.get("sub", ""), fnt, 46, (90, 90, 90, 255), sw=0, maxw=x1 - x0 - 80)
    for i in range(n):
        lab, amt = rows[i]; y = y0 + 400 + RH * i
        text(im, (x0 + 50, y), lab, fnt, 62, INK, sw=0, anchor="lm", maxw=(x1 - x0) * 0.55); text(im, (x1 - 50, y), amt, fnt, 66, INK, sw=0, anchor="rm")
    if done:
        y = y0 + 400 + RH * len(rows) + 20; d.line([(x0 + 40, y - 50), (x1 - 40, y - 50)], fill=INK, width=5)
        text(im, (x0 + 50, y + 50), "TOTAL", fnt, 84, INK, sw=0, anchor="lm"); text(im, (x1 - 50, y + 50), sh["total"], fnt, 92, RED, sw=0, anchor="rm")
        if sh.get("stamp"):
            sp = back((lt - 0.2 - step * len(rows) - 0.4) / 0.25)
            if sp > 0: text(im, (W * 0.62, y + 200), sh["stamp"], "BlackOps", 110, col(RED, 225), stroke=col(RED, 225), sw=3, scale=2.2 - 1.2 * sp, ang=-10)
    b = dict(sh.get("buck") or {"mood": "point"}); b.setdefault("x", 0.18); b.setdefault("y", 1.0); b.setdefault("h", 520)
    R.buck(im, W * b["x"], H * b["y"], b["h"], b.get("mood", "point"), talk.get("B", 0.0), t, b.get("flip", False))
    cast(im, sh, t, talk, R)


# ---------------------------------------------------------------- 7. grid: what $X buys (cards pop in)
def k_grid(im, sh, lt, t, talk, R):
    if sh.get("dim", 120): dim(im, sh.get("dim", 120))
    fnt = sh.get("font", "Bebas"); cells = sh["cells"]; cols = sh.get("cols", 2); cw = (W - 120 - 40 * (cols - 1)) / cols; chh = sh.get("cell_h", 300)
    if sh.get("title"): text(im, (W / 2, H * 0.09), sh["title"], fnt, 96, GOLD, sw=8, maxw=W * 0.92)
    for i, c in enumerate(cells):
        r_, c_ = divmod(i, cols); x = 60 + c_ * (cw + 40); y = H * 0.17 + r_ * (chh + 36); p = back((lt - 0.2 - i * sh.get("stagger", 0.45)) / 0.3)
        if p <= 0: continue
        hl = sh.get("hl") == i and lt > sh.get("hl_at", 99)
        lay = Image.new("RGBA", (int(cw), int(chh)), (0, 0, 0, 0)); panel(lay, [0, 0, cw - 14, chh - 14], fill=(250, 214, 80, 250) if hl else (232, 232, 236, 240), shadow=False)
        text(lay, (cw / 2 - 7, chh * 0.36), c[0], fnt, 68, INK, sw=0, maxw=cw - 50); text(lay, (cw / 2 - 7, chh * 0.7), c[1], fnt, 84, col(c[2]) if len(c) > 2 else RED, sw=0, maxw=cw - 50)
        lay = lay.resize((max(1, int(cw * p)), max(1, int(chh * p))), Image.LANCZOS); im.alpha_composite(lay, (int(x + cw * (1 - p) / 2), int(y + chh * (1 - p) / 2)))
    host(im, sh, t, talk, R)


# ---------------------------------------------------------------- 8. stamp: myth / fact verdict slams onto a claim
def k_stamp(im, sh, lt, t, talk, R):
    if sh.get("dim", 100): dim(im, sh.get("dim", 100))
    fnt = sh.get("font", "Abril"); panel(im, [70, H * 0.2, W - 70, H * 0.48], fill=(232, 228, 218, 250), r=24)
    text(im, (W / 2, H * 0.25), sh.get("kicker", "THEY SAY:"), fnt, 50, (130, 120, 110, 255), sw=0)
    lines = sh["claim"].split("\n")
    for i, ln in enumerate(lines): text(im, (W / 2, H * 0.31 + i * 92), ln, fnt, 78, INK, sw=0, maxw=W * 0.8)
    at = sh.get("at", 1.0)
    if lt >= at:
        ok = sh.get("verdict", "MYTH").upper() in ("FACT", "TRUE", "REAL")
        text(im, (W / 2, H * 0.49), sh.get("verdict", "MYTH"), "BlackOps", 150, col(GREEN if ok else RED, 240), stroke=(232, 232, 236, 255), sw=6, scale=2.4 - 1.4 * back((lt - at) / 0.22), ang=-8, maxw=W * 0.8)
    if sh.get("why") and lt >= at + 0.6: text(im, (W / 2, H * 0.6), sh["why"], fnt, 64, WHITE, sw=7, maxw=W * 0.9)
    host(im, sh, t, talk, R)


# ---------------------------------------------------------------- 9. spend: spend-the-fortune simulator
def k_spend(im, sh, lt, t, talk, R):
    gradient(im, (24, 120, 70), (10, 60, 40), sh)
    d = ImageDraw.Draw(im)
    if not footage(sh):
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        for i in range(0, H, 90): dl.line([(0, i), (W, i + 40)], fill=(255, 255, 255, 14), width=30)
        im.alpha_composite(lay)
    fnt = sh.get("font", "Archivo"); items = sh["items"]; step = sh.get("step", 0.9); bal0 = sh["balance"]
    n = min(len(items), int(max(0, lt - 0.3) / step) + (1 if lt > 0.3 else 0)); spent = sum(p for _, p in items[:n])
    panel(im, [50, 130, W - 50, 420], fill=(15, 30, 20, 235), outline=GOLD, ow=6)
    text(im, (W / 2, 195), sh.get("who", "BALANCE"), fnt, 46, (200, 230, 210, 255), sw=0, maxw=W - 160)
    text(im, (W / 2, 320), money(bal0 - spent, 0), fnt, 104, GOLD, sw=0, maxw=W * 0.86)
    for i in range(n):
        name, pr = items[i]; y = 480 + 190 * (i - max(0, n - 5))
        if y < 470: continue
        p = back((lt - 0.3 - i * step) / 0.25)
        panel(im, [70 + (1 - p) * 900, y, W - 70 + (1 - p) * 900, y + 160], fill=(232, 232, 236, 245), r=34)
        text(im, (W / 2 + (1 - p) * 900, y + 52), name, fnt, 54, INK, sw=0, maxw=W - 200)
        text(im, (W / 2 + (1 - p) * 900, y + 118), "-" + money(pr, 2, "auto"), fnt, 62, RED, sw=0, maxw=W - 200)
    if sh.get("left_note") and n == len(items): text(im, (W / 2, H * 0.62), sh["left_note"], fnt, 64, WHITE, sw=7, maxw=W * 0.9)
    host(im, sh, t, talk, R)


# ---------------------------------------------------------------- 10. chalk: chalkboard explainer, lines appear
_CHALK = {}


def chalk_bg():
    if "bg" not in _CHALK:
        bg = Image.new("RGBA", (W, H), (34, 62, 48, 255)); rnd = random.Random(7)
        for _ in range(420):  # old erased chalk smudges (own layer: ImageDraw would overwrite alpha, not blend)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            x, y = rnd.randrange(-200, W), rnd.randrange(0, int(H * 0.9)); w_ = rnd.randrange(200, 600)
            d.ellipse([x, y, x + w_, y + rnd.randrange(30, 90)], fill=(255, 255, 255, rnd.randrange(8, 24))); bg.alpha_composite(lay)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        for _ in range(2500): x, y = rnd.randrange(W), rnd.randrange(H); d.point((x, y), fill=(255, 255, 255, rnd.randrange(15, 50)))
        bg.alpha_composite(lay); bg = bg.filter(ImageFilter.GaussianBlur(2)).convert("RGB").convert("RGBA"); d = ImageDraw.Draw(bg)
        d.rectangle([0, H * 0.92, W, H], fill=(120, 82, 44, 255)); d.rectangle([0, H * 0.92, W, H * 0.925], fill=(80, 52, 26, 255))
        for i in range(4): d.rounded_rectangle([140 + i * 90, H * 0.905, 200 + i * 90, H * 0.92], 6, fill=(225, 225, 215, 255))
        _CHALK["bg"] = bg
    return _CHALK["bg"]


def k_chalk(im, sh, lt, t, talk, R):
    im.alpha_composite(chalk_bg())
    fnt = sh.get("font", "Hand"); y = H * 0.13; d = ImageDraw.Draw(im)
    for i, ln in enumerate(sh["lines"]):
        a = ln.get("at", 0.3 + i * 0.8)
        if lt < a: break
        p = min(1.0, (lt - a) / 0.45); s_ = ln["t"][:max(1, int(len(ln["t"]) * p))]
        c = {"y": (255, 230, 120, 255), "w": (245, 245, 240, 255), "r": (255, 140, 130, 255)}.get(ln.get("c", "w"))
        sz = int(ln.get("size", 84) * 1.5)
        while F(fnt, sz).getlength(ln["t"]) > W - 140 and sz > 40: sz -= 6
        text(im, (70, y), s_, fnt, sz, c, stroke=(0, 0, 0, 0), sw=0, anchor="lm")
        if ln.get("u") and p >= 1: d.line([(70, y + sz * 0.6), (70 + F(fnt, sz).getlength(ln["t"]), y + sz * 0.66)], fill=c, width=8)
        y += sz * 1.3
    if not sh.get("buck") and not sh.get("cast"): sh = dict(sh, buck={"x": 0.8, "y": 0.99, "h": 760, "mood": "point"})
    elif sh.get("buck"): sh = dict(sh, buck=dict(sh["buck"], h=max(sh["buck"].get("h", 560), 760)))
    host(im, sh, t, talk, R)


# ---------------------------------------------------------------- 11. kinetic: full-screen kinetic typography (words slam)
def k_kinetic(im, sh, lt, t, talk, R):
    if footage(sh): dim(im, sh.get("dim", 100))
    elif sh.get("bgcol"): gradient(im, sh["bgcol"][0], sh["bgcol"][1])
    elif sh.get("dim", 150): dim(im, sh.get("dim", 150))
    fnt = sh.get("font", "Anton"); words = sh["words"]; y = H * sh.get("y", 0.3)
    for i, w in enumerate(words):
        a = w.get("at", 0.15 + i * 0.35)
        if lt < a: continue
        p = back((lt - a) / 0.2); sz = w.get("size", 150)
        text(im, (W / 2 + w.get("dx", 0), y), w["t"], w.get("font", fnt), sz, col(w.get("c", WHITE)), sw=w.get("sw", 9), scale=1.6 - 0.6 * p if p < 1 else 1.0, ang=w.get("ang", 0), maxw=W * 0.94)
        y += sz * 1.12
    host(im, sh, t, talk, R)


# ---------------------------------------------------------------- 12. host: Buck big on screen (skit / POV / talking head) + optional bubble
def k_host(im, sh, lt, t, talk, R):
    if sh.get("dim"): dim(im, sh["dim"])
    b = dict(sh.get("buck") or {}); b.setdefault("x", 0.5); b.setdefault("y", 1.02); b.setdefault("h", 1350)
    R.buck(im, W * b["x"], H * b["y"], b["h"], b.get("mood", "happy"), talk.get("B", 0.0), t, b.get("flip", False))
    if sh.get("bubble"):
        p = back((lt - sh.get("bubble_at", 0.1)) / 0.25)
        if p > 0:
            bx = [80, H * 0.08, W - 80, H * 0.08 + 260]; lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); panel(lay, bx, fill=(232, 232, 236, 245), r=60)
            ImageDraw.Draw(lay).polygon([(W * 0.45, bx[3] - 4), (W * 0.55, bx[3] - 4), (W * 0.5, bx[3] + 70)], fill=(232, 232, 236, 245))
            text(lay, (W / 2, bx[1] + 130), sh["bubble"], sh.get("font", "Lilita"), 72, INK, sw=0, maxw=W - 240)
            if p < 1: lay = lay.resize((W, H)).rotate(0)
            im.alpha_composite(lay)
    if sh.get("prop"):  # big floating number/label next to Buck
        text(im, (W * 0.5, H * 0.38), sh["prop"], sh.get("font", "Anton"), 150, GOLD, sw=10, scale=back((lt - sh.get("prop_at", 0.3)) / 0.3), ang=-4, maxw=W * 0.9)


# ---------------------------------------------------------------- 13. versus: two halves, two values, winner glows
def k_versus(im, sh, lt, t, talk, R):
    fnt = sh.get("font", "Bebas"); L, Rr = sh["left"], sh["right"]; d = ImageDraw.Draw(im)
    if footage(sh):
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        dl.rectangle([0, 0, W, H / 2], fill=col(L.get("c", (40, 110, 220)), 105)); dl.rectangle([0, H / 2, W, H], fill=col(Rr.get("c", (235, 120, 40)), 105)); im.alpha_composite(lay)
    else: d.rectangle([0, 0, W, H / 2], fill=col(L.get("c", (40, 110, 220)))); d.rectangle([0, H / 2, W, H], fill=col(Rr.get("c", (235, 120, 40))))
    for side, y in ((L, H * 0.25), (Rr, H * 0.75)):
        text(im, (W / 2, y - 140), side["label"], fnt, 96, WHITE, sw=8, maxw=W * 0.9)
        p = ease((lt - side.get("at", 0.4)) / 1.2); v = side["value"] * p
        text(im, (W / 2, y + 30), side.get("fmt", "${:,.0f}").format(v), fnt, 190, WHITE, sw=10, maxw=W * 0.9)
    text(im, (W / 2, H / 2), "VS", "BlackOps", 120, GOLD, sw=10, scale=back((lt - 0.2) / 0.3))
    if sh.get("win") is not None and lt > sh.get("win_at", 2.5):
        y = H * 0.25 if sh["win"] == 0 else H * 0.75; text(im, (W * 0.82, y - 250), sh.get("win_label", "WINNER"), "Bangers", 80, GOLD, sw=7, ang=-10, scale=back((lt - sh.get("win_at", 2.5)) / 0.25))
    host(im, sh, t, talk, R)


# ---------------------------------------------------------------- 14. pixel: retro 8-bit game screen (score counts, coins)
def k_pixel(im, sh, lt, t, talk, R):
    d = ImageDraw.Draw(im)
    bands = [(24, 18, 70), (44, 30, 110), (70, 46, 150), (110, 64, 170), (160, 84, 170), (220, 120, 150)]  # 8-bit dusk, banded like real pixel art
    bh = H * 0.82 / len(bands)
    for i, c in enumerate(bands): d.rectangle([0, int(i * bh), W, int((i + 1) * bh) + 1], fill=c + (255,))
    rnd = random.Random(11)
    for cx, cy in ((180, 300), (720, 520), (420, 760)):  # blocky clouds
        for dx, dy, w_ in ((0, 0, 240), (60, -60, 120), (-60, 60, 360)): d.rectangle([cx + dx, cy + dy, cx + dx + w_, cy + dy + 60], fill=(235, 220, 240, 255))
    x = 0
    while x < W:  # blocky skyline with lit windows
        bw = rnd.randrange(120, 220); bh2 = rnd.randrange(260, 620); top = int(H * 0.82) - bh2; shade = rnd.choice([(30, 24, 60), (40, 32, 80), (22, 20, 50)])
        d.rectangle([x, top, x + bw, int(H * 0.82)], fill=shade + (255,))
        for wy in range(top + 30, int(H * 0.82) - 40, 70):
            for wx in range(x + 20, x + bw - 30, 50):
                if rnd.random() < 0.55: d.rectangle([wx, wy, wx + 24, wy + 30], fill=(255, 214, 90, 255))
        x += bw + rnd.randrange(0, 30)
    for x in range(0, W, 60):
        for y in range(int(H * 0.82), H, 60): d.rectangle([x, y, x + 56, y + 56], fill=(70, 160, 60, 255) if (x // 60 + y // 60) % 2 else (60, 140, 50, 255))
    for i in range(14):
        sx = (i * 173 + int(lt * 60 * (1 + i % 3))) % W; sy = (i * 311) % int(H * 0.7); d.rectangle([sx, sy, sx + 6, sy + 6], fill=(232, 232, 236, 200))
    text(im, (60, 170), sh.get("hud_l", "SCORE"), "Pixel", 40, WHITE, sw=0, anchor="lm", maxw=W * 0.55); text(im, (W - 60, 170), sh.get("hud_r", "LV 1"), "Pixel", 40, GOLD, sw=0, anchor="rm")
    p = ease((lt - sh.get("at", 0.3)) / sh.get("dur", 2.0)); v = sh.get("start", 0) + (sh.get("to", 0) - sh.get("start", 0)) * p
    text(im, (W / 2, H * 0.24), sh.get("prefix", "$") + f"{v:,.0f}", "Pixel", sh.get("size", 76), GOLD, sw=0, maxw=W * 0.92)
    if sh.get("msg"): text(im, (W / 2, H * 0.36), sh["msg"], "Pixel", 40, WHITE, sw=0, maxw=W * 0.9)
    for i in range(5):  # coins bouncing
        cx = W * (0.15 + 0.17 * i); cy = H * 0.74 - abs(math.sin(lt * 4 + i)) * 120
        d.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=(255, 205, 60, 255), outline=(180, 120, 20, 255), width=6)
    host(im, sh, t, talk, R)


# ---------------------------------------------------------------- 15. flagvote: RED FLAG or GREEN FLAG panel with a timer
def k_flagvote(im, sh, lt, t, talk, R):
    if sh.get("dim", 70): dim(im, sh.get("dim", 70))
    fnt = sh.get("font", "Archivo"); rv = sh.get("reveal_at", 2.0)
    panel(im, [60, H * 0.075, W - 60, H * 0.22], fill=(20, 20, 30, 235), outline=GOLD, ow=6)
    text(im, (W / 2, H * 0.11), sh.get("round", "RED FLAG OR GREEN FLAG?"), fnt, 50, GOLD, sw=0)
    text(im, (W / 2, H * 0.175), sh["q"], fnt, 56, WHITE, sw=0, maxw=W * 0.84)
    if lt < rv:
        left = max(0.0, rv - lt); cx, cy, r = W / 2, H * 0.3, 70; d = ImageDraw.Draw(im)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(20, 20, 30, 220)); d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * left / rv, fill=GOLD, width=14)
        text(im, (cx, cy), str(int(math.ceil(left))), fnt, 70, WHITE, sw=4)
    else:
        red = sh.get("verdict", "red") == "red"; p = back((lt - rv) / 0.25); d = ImageDraw.Draw(im)
        fx, fy = W * 0.5, H * 0.3; c = RED if red else GREEN
        lay = Image.new("RGBA", (520, 420), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        dl.rectangle([40, 20, 62, 410], fill=(80, 60, 40, 255)); dl.polygon([(62, 30), (480, 90), (62, 200)], fill=c); dl.line([(62, 30), (480, 90), (62, 200)], fill=INK, width=8)
        lay = lay.resize((max(1, int(520 * p)), max(1, int(420 * p)))); im.alpha_composite(lay, (int(fx - lay.width / 2), int(fy - lay.height / 2)))
        text(im, (W / 2, H * 0.43), "RED FLAG" if red else "GREEN FLAG", "BlackOps", 110, c, sw=8, scale=back((lt - rv - 0.1) / 0.25))
    host(im, sh, t, talk, R)


KINDS = {"flagvote": k_flagvote, "counter": k_counter, "scale": k_scale, "bars": k_bars, "line": k_line, "quiz": k_quiz, "receipt": k_receipt,
         "grid": k_grid, "stamp": k_stamp, "spend": k_spend, "chalk": k_chalk, "kinetic": k_kinetic, "host": k_host,
         "versus": k_versus, "pixel": k_pixel}
