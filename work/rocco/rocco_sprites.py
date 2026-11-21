#!/usr/bin/env python3
"""rocco_sprites.py - Rocco (raccoon detective, our original character from work/rocco/rocco.svg) as a sprite library in
the same format as Buck's 3D library, so engine/make_video.py renders Rocco with all its staging (corner/center, drop_in,
flip/bonk/dodge, zoom on face, lip-sync mouth levels t1..t3).

  python3 -I work/rocco/rocco_sprites.py OUTDIR [--size 800]
  FIN_BUCK3D=OUTDIR python3 -I engine/make_video.py spec.json out.mp4 ...   (spec "brand": "RED FLAG ROCCO")

Library: <mood>_NN.webp (15 frames, 15 fps loop) for every engine mood, <mood>_t1..t3_NN (open mouth levels),
flip_happy (11), bonk_dizzy (23), dodge_shocked (12). Feet line at 0.79 of the frame (engine's "local" library value).
Pure PIL, deterministic, no network.
"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter

MOODS = ("happy", "shocked", "laugh", "smug", "confused", "sideeye", "sad", "angry", "point", "dizzy", "thumbsup", "proud")
INK = (35, 39, 45, 255); FUR = (140, 150, 160, 255); FUR_D = (108, 117, 128, 255); FACE = (244, 241, 234, 255)
MASK = (35, 39, 45, 255); PINK = (242, 215, 208, 255); HAT = (140, 106, 69, 255); HAT_D = (122, 90, 58, 255)
RED = (255, 59, 59, 255); RED_D = (161, 18, 18, 255); COAT = (196, 160, 104, 255); COAT_D = (160, 126, 78, 255)
POLE = (217, 192, 138, 255); IRIS = (58, 36, 20, 255); WHITE = (255, 255, 255, 255); SHOE = (60, 52, 46, 255)
SS = 2


def mood_params(m):
    p = dict(brow_l=0.0, brow_r=-0.25, brow_y=0.0, eye_open=1.0, look=(0.25, 0.1), mouth="smirk", extra=None,
             arm="flag_down", tilt=0.0)
    if m == "happy": p.update(brow_r=0.0, mouth="smile", arm="flag_down")
    elif m == "shocked": p.update(brow_l=0.35, brow_r=0.35, brow_y=-14, eye_open=1.25, look=(0, 0), mouth="O", extra="!", arm="up")
    elif m == "laugh": p.update(brow_l=0.2, brow_r=0.2, eye_open=0.25, mouth="grin", extra="ha")
    elif m == "smug": p.update(brow_l=-0.1, brow_r=-0.35, eye_open=0.6, look=(0.35, 0), mouth="smirk")
    elif m == "confused": p.update(brow_l=0.35, brow_r=-0.35, look=(-0.3, -0.3), mouth="wavy", extra="?", tilt=-6)
    elif m == "sideeye": p.update(brow_l=-0.25, brow_r=-0.25, eye_open=0.7, look=(0.85, 0), mouth="flat")
    elif m == "sad": p.update(brow_l=-0.45, brow_r=-0.45, look=(0, 0.4), mouth="frown", extra="drop", tilt=4)
    elif m == "angry": p.update(brow_l=0.5, brow_r=0.5, brow_y=8, eye_open=0.8, look=(0, 0.1), mouth="grr", extra="steam")
    elif m == "point": p.update(brow_r=0.0, mouth="smile", arm="point")
    elif m == "dizzy": p.update(eye_open=-1, mouth="wavy", extra="stars", tilt=6)
    elif m == "thumbsup": p.update(brow_r=0.0, mouth="grin", arm="thumb")
    elif m == "deadpan": p.update(brow_l=-0.05, brow_r=-0.05, brow_y=4, eye_open=0.55, look=(0, 0), mouth="flat")  # flat stare at the viewer (comedy act)
    elif m == "proud": p.update(brow_l=-0.1, brow_r=-0.1, eye_open=0.7, look=(0, -0.1), mouth="smile", arm="flag_up")
    return p


def draw_rocco(size, m, t, talk=0, blink=False):
    """One frame. t = time in the loop (s). Returns RGBA size x size."""
    S = size * SS; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    p = mood_params(m); u = S / 800.0; L = lambda v: int(v * u)
    bob = math.sin(t * 2 * math.pi / 1.0) * 6 * u  # breathing bob (1 s loop)
    feet = 0.79 * S; cx = S * 0.5
    lw = max(2, L(7))
    # legs + shoes
    for sx in (-1, 1):
        x = cx + sx * L(48)
        d.rounded_rectangle([x - L(18), feet - L(62), x + L(18), feet - L(18)], L(10), fill=INK)
        d.ellipse([x - L(44) + sx * L(14), feet - L(34), x + L(38) + sx * L(14), feet + L(6)], fill=SHOE, outline=INK, width=lw)
    # trench coat body
    by = feet - L(58) + bob * 0.4; CH = 160  # coat height (chibi proportions, 2026-11-21)
    d.polygon([(cx - L(118), by), (cx - L(96), by - L(CH)), (cx + L(96), by - L(CH)), (cx + L(118), by)], fill=COAT, outline=INK)
    d.line([(cx, by - L(CH - 10)), (cx, by - L(6))], fill=COAT_D, width=lw)
    for k in range(3): d.ellipse([cx - L(26) - L(7), by - L(CH - 30) + k * L(40) - L(7), cx - L(26) + L(7), by - L(CH - 30) + k * L(40) + L(7)], fill=INK)
    d.polygon([(cx - L(96), by - L(CH)), (cx - L(30), by - L(CH)), (cx - L(60), by - L(CH - 70))], fill=COAT_D, outline=INK)
    d.polygon([(cx + L(96), by - L(CH)), (cx + L(30), by - L(CH)), (cx + L(60), by - L(CH - 70))], fill=COAT_D, outline=INK)
    d.rectangle([cx - L(112), by - L(70), cx + L(112), by - L(52)], fill=COAT_D, outline=INK, width=max(1, lw // 2))
    # arms
    sh_l, sh_r = (cx - L(100), by - L(CH - 20)), (cx + L(100), by - L(CH - 20))
    wave = math.sin(t * 2 * math.pi) * 8
    def arm(sh, ang, ln=135):
        a = math.radians(ang); hx, hy = sh[0] + math.cos(a) * L(ln), sh[1] + math.sin(a) * L(ln)
        d.line([sh, (hx, hy)], fill=COAT, width=L(34)); d.line([sh, (hx, hy)], fill=INK, width=max(2, L(3)))
        d.ellipse([hx - L(22), hy - L(22), hx + L(22), hy + L(22)], fill=FUR_D, outline=INK, width=lw)
        return hx, hy
    arm(sh_l, 115 + wave * 0.3)
    if p["arm"] in ("flag_down", "flag_up", "up"):
        ang = {"flag_down": 60, "flag_up": -60, "up": -75}[p["arm"]] + wave * 0.6
        hx, hy = arm(sh_r, ang)
        # red flag on a pole (the channel's signature)
        top = (hx + L(10), hy - L(190)); d.line([(hx, hy + L(30)), top], fill=POLE, width=L(12))
        fw = math.sin(t * 2 * math.pi * 1.5)
        fl = [top, (top[0] + L(110), top[1] + L(8) + fw * L(10)), (top[0] + L(100), top[1] + L(50)), (top[0] + L(112), top[1] + L(92) + fw * L(8)), (top[0], top[1] + L(80))]
        d.polygon(fl, fill=RED, outline=RED_D)
    elif p["arm"] == "point":
        hx, hy = arm(sh_r, -15, 150); d.polygon([(hx + L(18), hy - L(8)), (hx + L(62), hy - L(4)), (hx + L(18), hy + L(8))], fill=FUR_D, outline=INK)
    elif p["arm"] == "thumb":
        hx, hy = arm(sh_r, -50, 130); d.rounded_rectangle([hx - L(8), hy - L(58), hx + L(10), hy - L(14)], L(8), fill=FUR_D, outline=INK, width=lw)
    # head (own layer, scaled HEAD_K around the neck so the face reads even when Rocco is small in a corner)
    body = im; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    neck = (cx, by - L(CH) + L(10)); HEAD_K = 1.24
    hcx, hcy = cx, neck[1] - L(130) + bob; R = L(150)
    for sx in (-1, 1):  # ears
        e = [(hcx + sx * L(118), hcy - L(55)), (hcx + sx * L(132), hcy - L(165)), (hcx + sx * L(55), hcy - L(110))]
        d.polygon(e, fill=FUR_D, outline=INK); d.polygon([(hcx + sx * L(112), hcy - L(72)), (hcx + sx * L(122), hcy - L(132)), (hcx + sx * L(74), hcy - L(104))], fill=PINK)
    d.ellipse([hcx - R, hcy - R * 0.9, hcx + R, hcy + R * 0.88], fill=FUR, outline=INK, width=lw)
    d.chord([hcx - R * 0.88, hcy - R * 0.45, hcx + R * 0.88, hcy + R * 0.86], 0, 180, fill=FACE)
    d.ellipse([hcx - R * 0.88, hcy - R * 0.45, hcx + R * 0.88, hcy + R * 0.32], fill=FACE)
    # mask band
    d.polygon([(hcx - R * 0.96, hcy - R * 0.08), (hcx - R * 0.5, hcy - R * 0.36), (hcx, hcy - R * 0.12), (hcx + R * 0.5, hcy - R * 0.36),
               (hcx + R * 0.96, hcy - R * 0.08), (hcx + R * 0.55, hcy + R * 0.2), (hcx, hcy + R * 0.06), (hcx - R * 0.55, hcy + R * 0.2)], fill=MASK)
    # eyes
    er = R * 0.2; lx, ly = p["look"]
    for sx in (-1, 1):
        ex, ey = hcx + sx * R * 0.4, hcy - R * 0.1
        if p["eye_open"] < 0:  # dizzy spirals
            for k in range(3): d.arc([ex - er + k * er * 0.3, ey - er + k * er * 0.3, ex + er - k * er * 0.3, ey + er - k * er * 0.3], k * 90, k * 90 + 270, fill=WHITE, width=lw)
            continue
        op = 0.08 if blink else p["eye_open"]
        d.ellipse([ex - er, ey - er * op, ex + er, ey + er * op], fill=WHITE)
        if op > 0.2:
            pr = er * 0.52; px, py = ex + lx * er * 0.45, ey + ly * er * 0.45 * op
            d.ellipse([px - pr, py - pr * min(1, op), px + pr, py + pr * min(1, op)], fill=IRIS)
            d.ellipse([px + pr * 0.2, py - pr * 0.6, px + pr * 0.6, py - pr * 0.2], fill=WHITE)
        # brows (white on the mask, like the svg)
        bang = p["brow_l"] if sx < 0 else p["brow_r"]
        by0 = ey - er * 1.45 + p["brow_y"] * u
        x0, x1 = ex - er * 1.1, ex + er * 1.1
        y_in, y_out = by0 + bang * er * sx * -1 * 0.0, by0
        tilt = bang * er * 1.2
        pts = [(x0, by0 + (tilt if sx > 0 else -tilt)), (ex, by0 - er * 0.25), (x1, by0 + (-tilt if sx > 0 else tilt))]
        d.line(pts, fill=FACE, width=L(9), joint="curve")
    # nose + mouth (talk overrides with open levels)
    ny = hcy + R * 0.33
    d.ellipse([hcx - R * 0.13, ny - R * 0.09, hcx + R * 0.13, ny + R * 0.09], fill=INK)
    my = ny + R * 0.22; mw = R * 0.24
    mouth = p["mouth"] if not talk else "talk"
    if mouth == "talk":
        h = [0, 0.1, 0.17, 0.25][talk] * R
        d.ellipse([hcx - mw * (0.75 + 0.1 * talk), my - h * 0.3, hcx + mw * (0.75 + 0.1 * talk), my + h], fill=(90, 30, 34, 255), outline=INK, width=lw)
        d.ellipse([hcx - mw * 0.35, my + h * 0.35, hcx + mw * 0.35, my + h * 0.9], fill=(222, 100, 110, 255))
    elif mouth == "smirk":
        d.line([(hcx, ny + R * 0.08), (hcx, my - R * 0.02)], fill=INK, width=lw)
        d.arc([hcx - mw, my - R * 0.12, hcx + mw * 1.15, my + R * 0.06], 20, 160, fill=INK, width=lw)
    elif mouth in ("smile", "grin"):
        d.line([(hcx, ny + R * 0.08), (hcx, my - R * 0.02)], fill=INK, width=lw)
        if mouth == "grin":
            d.chord([hcx - mw, my - R * 0.1, hcx + mw, my + R * 0.16], 0, 180, fill=(90, 30, 34, 255), outline=INK, width=lw)
        else:
            d.arc([hcx - mw, my - R * 0.12, hcx + mw, my + R * 0.08], 15, 165, fill=INK, width=lw)
    elif mouth == "O":
        d.ellipse([hcx - mw * 0.45, my - R * 0.04, hcx + mw * 0.45, my + R * 0.2], fill=(90, 30, 34, 255), outline=INK, width=lw)
    elif mouth == "frown":
        d.arc([hcx - mw, my, hcx + mw, my + R * 0.18], 200, 340, fill=INK, width=lw)
    elif mouth == "flat":
        d.line([(hcx - mw * 0.7, my + R * 0.03), (hcx + mw * 0.7, my + R * 0.01)], fill=INK, width=lw)
    elif mouth == "wavy":
        d.line([(hcx - mw, my), (hcx - mw * 0.33, my + R * 0.05), (hcx + mw * 0.33, my - R * 0.02), (hcx + mw, my + R * 0.04)], fill=INK, width=lw, joint="curve")
    elif mouth == "grr":
        d.rectangle([hcx - mw * 0.8, my - R * 0.02, hcx + mw * 0.8, my + R * 0.1], fill=WHITE, outline=INK, width=lw)
        for k in range(1, 4): d.line([(hcx - mw * 0.8 + k * mw * 0.4, my - R * 0.02), (hcx - mw * 0.8 + k * mw * 0.4, my + R * 0.1)], fill=INK, width=max(1, lw // 2))
    # detective hat with the red band
    hy = hcy - R * 0.72
    d.ellipse([hcx - R * 1.02, hy - R * 0.1, hcx + R * 1.02, hy + R * 0.16], fill=HAT_D, outline=INK, width=lw)
    d.chord([hcx - R * 0.62, hy - R * 0.62, hcx + R * 0.62, hy + R * 0.5], 180, 360, fill=HAT, outline=INK, width=lw)
    d.rectangle([hcx - R * 0.6, hy - R * 0.12, hcx + R * 0.6, hy + R * 0.0], fill=RED)
    # extras
    ph = (t * 2) % 1
    if p["extra"] == "!":
        d.text((hcx + R * 0.95, hcy - R * 1.2), "!", fill=RED, font=None)
        d.polygon([(hcx + R * 1.05, hcy - R * 1.25), (hcx + R * 1.2, hcy - R * 1.25), (hcx + R * 1.14, hcy - R * 0.75), (hcx + R * 1.1, hcy - R * 0.75)], fill=RED, outline=INK)
        d.ellipse([hcx + R * 1.08, hcy - R * 0.68, hcx + R * 1.18, hcy - R * 0.58], fill=RED, outline=INK)
    elif p["extra"] == "?":
        d.arc([hcx + R * 0.9, hcy - R * 1.3, hcx + R * 1.25, hcy - R * 0.95], 180, 450, fill=(255, 210, 80, 255), width=L(14))
        d.ellipse([hcx + R * 1.03, hcy - R * 0.82, hcx + R * 1.12, hcy - R * 0.73], fill=(255, 210, 80, 255))
    elif p["extra"] == "drop":
        yy = hcy - R * 0.3 + ph * R * 0.4
        d.polygon([(hcx + R * 0.95, yy - R * 0.14), (hcx + R * 1.03, yy + R * 0.02), (hcx + R * 0.87, yy + R * 0.02)], fill=(120, 190, 255, 255))
        d.ellipse([hcx + R * 0.87, yy - R * 0.04, hcx + R * 1.03, yy + R * 0.1], fill=(120, 190, 255, 255))
    elif p["extra"] == "steam":
        for sx in (-1, 1):
            yy = hcy - R * 0.9 - ph * R * 0.3
            d.ellipse([hcx + sx * R * 1.0 - R * 0.1, yy - R * 0.1, hcx + sx * R * 1.0 + R * 0.1, yy + R * 0.1], fill=(230, 230, 235, int(200 * (1 - ph))))
    elif p["extra"] == "stars":
        for k in range(4):
            a = t * 4 + k * math.pi / 2; sx_, sy_ = hcx + math.cos(a) * R * 0.9, hy - R * 0.25 + math.sin(a) * R * 0.18
            d.regular_polygon((sx_, sy_, R * 0.09), 5, rotation=k * 20, fill=(255, 215, 60, 255), outline=INK)
    elif p["extra"] == "ha":
        d.text((hcx + R * 0.9, hcy - R * 1.1), "HA", fill=(255, 215, 60, 255))
    hs = int(S * HEAD_K); hd = im.resize((hs, hs), Image.LANCZOS)
    im = body; im.paste(hd, (int(neck[0] - neck[0] * HEAD_K), int(neck[1] - neck[1] * HEAD_K)), hd)
    im = im.rotate(p["tilt"], resample=Image.BICUBIC, center=(cx, feet))
    return im.resize((size, size), Image.LANCZOS)


def transform(im, ang=0.0, sx=1.0, sy=1.0, dx=0.0, dy=0.0):
    S = im.size[0]; feet = 0.79 * S
    if sx != 1 or sy != 1:
        w, h = int(S * sx), int(S * sy); im2 = im.resize((max(1, w), max(1, h)), Image.LANCZOS)
        out = Image.new("RGBA", (S, S)); out.paste(im2, (int(S / 2 - w / 2), int(feet - feet * sy)), im2); im = out
    if ang: im = im.rotate(ang, resample=Image.BICUBIC, center=(S / 2, S * 0.5))
    if dx or dy:
        out = Image.new("RGBA", (S, S)); out.paste(im, (int(dx), int(dy)), im); im = out
    return im


def main():
    out = sys.argv[1]; size = int(sys.argv[sys.argv.index("--size") + 1]) if "--size" in sys.argv else 800
    os.makedirs(out, exist_ok=True); n = 0
    for m in MOODS:
        for f in range(15):
            t = f / 15.0; blink = f in (9, 10) and m not in ("laugh", "dizzy")
            draw_rocco(size, m, t, 0, blink).save(os.path.join(out, f"{m}_{f:02d}.webp"), quality=92); n += 1
            for lv in (1, 2, 3):
                draw_rocco(size, m, t, lv, False).save(os.path.join(out, f"{m}_t{lv}_{f:02d}.webp"), quality=92); n += 1
    for f in range(11):  # flip_happy: full spin while hopping
        k = f / 10; im = draw_rocco(size, "happy", k)
        transform(im, ang=-360 * k, dy=-math.sin(k * math.pi) * size * 0.18).save(os.path.join(out, f"flip_happy_{f:02d}.webp"), quality=92); n += 1
    for f in range(23):  # bonk_dizzy: squash on the hit, then dizzy wobble
        k = f / 22
        if k < 0.25: im = transform(draw_rocco(size, "shocked", k), sx=1 + 0.25 * math.sin(k / 0.25 * math.pi), sy=1 - 0.3 * math.sin(k / 0.25 * math.pi))
        else: im = transform(draw_rocco(size, "dizzy", k), ang=math.sin(k * 18) * 6)
        im.save(os.path.join(out, f"bonk_dizzy_{f:02d}.webp"), quality=92); n += 1
    for f in range(12):  # dodge_shocked: lean away and come back
        k = f / 11; s = math.sin(k * math.pi)
        transform(draw_rocco(size, "shocked", k), ang=18 * s, dx=-size * 0.16 * s).save(os.path.join(out, f"dodge_shocked_{f:02d}.webp"), quality=92); n += 1
    # ---- comedy acts (2026-11-21, docs/comedy.md): same clip names as Buck's buck3d_v3_acts.tar ----
    for f in range(16):  # doubletake_shocked: glance away -> squash beat -> snap back, eyes pop
        k = f / 15
        if f < 6: im = draw_rocco(size, "sideeye", k)
        elif f < 8: im = transform(draw_rocco(size, "sideeye", k, 0, True), sx=1.08, sy=0.88)
        else:
            o = math.sin(min(1, (f - 8) / 5) * math.pi); im = transform(draw_rocco(size, "shocked", k), sx=1 - 0.05 * o, sy=1 + 0.08 * o)
        im.save(os.path.join(out, f"doubletake_shocked_{f:02d}.webp"), quality=92); n += 1
    for f in range(16):  # jawdrop_shocked: freeze, stretch pop, tiny shake
        k = f / 15
        if f < 3: im = draw_rocco(size, "happy", k)
        else:
            o = math.sin(min(1, (f - 3) / 6) * math.pi); sh = math.sin(f * 2.4) * (2.5 if f > 9 else 0)
            im = transform(draw_rocco(size, "shocked", 0.0), sx=1 - 0.04 * o, sy=1 + 0.07 * o, ang=sh)
        im.save(os.path.join(out, f"jawdrop_shocked_{f:02d}.webp"), quality=92); n += 1
    for f in range(14):  # shrug_confused: shoulders up, head tilts, comes back
        k = f / 13; o = math.sin(k * math.pi)
        transform(draw_rocco(size, "confused", k), sx=1 + 0.03 * o, sy=1 + 0.05 * o, ang=-5 * o, dy=-size * 0.025 * o).save(os.path.join(out, f"shrug_confused_{f:02d}.webp"), quality=92); n += 1
    for f in range(18):  # sigh_sad: small inhale, shoulders drop, slow head shake
        k = f / 17
        if f < 4: im = transform(draw_rocco(size, "deadpan", k), sy=1 + 0.04 * math.sin(k / 0.22 * math.pi))
        else:
            sh = math.sin((k - 0.5) / 0.36 * 2 * math.pi) * (3.5 if 0.5 < k < 0.86 else 0)
            im = transform(draw_rocco(size, "sad", k, 0, f in (5, 6, 7)), sx=1.03, sy=0.94, ang=sh)
        im.save(os.path.join(out, f"sigh_sad_{f:02d}.webp"), quality=92); n += 1
    for f in range(15):  # deadpan_sideeye: flat stare at the viewer, one slow blink
        draw_rocco(size, "deadpan", 0.0, 0, f in (6, 7, 8, 9)).save(os.path.join(out, f"deadpan_sideeye_{f:02d}.webp"), quality=92); n += 1
    print({"out": out, "frames": n})


if __name__ == "__main__":
    main()
