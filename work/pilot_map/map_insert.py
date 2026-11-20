#!/usr/bin/env python3
"""map_insert.py — PILOT (2026-11-21): Vox-style US map insert for Shorts, pure PIL + ffmpeg, no keys, no network.

    python3 -I map_insert.py out.mp4 [--from 36 --to 06 --label "$800 ROUND TRIP" --secs 4 --theme noir]

Ideas taken from iart-ai map-animation skill (MIT; docs/skills/iart-motion/map-animation-skills):
  - camera zoom/pan over a vector map; pins drop, a route draws on, a label calls out;
  - overlays (pins/route/label) quantized to a 12 fps "stutter" so motion reads as graphic, camera stays smooth 30 fps.
Map data: us-atlas 3.0.1 states-albers-10m.json (ISC, from US Census cartographic boundaries) — LICENSE_us-atlas_ISC.
State ids are FIPS codes (36 = New York, 06 = California, 17 = Illinois, 48 = Texas, 12 = Florida).
"""
import json, math, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
ANTON = next((p for p in ("/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf",
                          "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf",
                          "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf") if os.path.exists(p)), None)
THEMES = {  # bg, land, border, highlight, route, text
    "noir":  ((10, 12, 18), (34, 40, 54), (70, 80, 100), (245, 197, 66), (255, 90, 80), (245, 245, 240)),
    "ocean": ((6, 22, 38), (22, 58, 84), (60, 110, 140), (120, 230, 255), (255, 200, 70), (240, 250, 255)),
    "mint":  ((8, 26, 20), (24, 66, 50), (60, 120, 95), (140, 255, 190), (255, 210, 80), (240, 255, 245)),
}


def load_states(path):
    d = json.load(open(path))
    sx, sy = d["transform"]["scale"]; tx, ty = d["transform"]["translate"]
    arcs = []
    for arc in d["arcs"]:
        x = y = 0; pts = []
        for dx, dy in arc:
            x += dx; y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)

    def ring(idx):
        out = []
        for i in idx:
            a = arcs[i] if i >= 0 else arcs[~i][::-1]
            out.extend(a if not out else a[1:])
        return out

    states = {}
    for g in d["objects"]["states"]["geometries"]:
        polys = [g["arcs"]] if g["type"] == "Polygon" else g["arcs"]
        states[g["id"]] = [[ring(r) for r in poly] for poly in polys]
    return states


def centroid(polys):
    best = max((p[0] for p in polys), key=len)  # largest outer ring
    a = cx = cy = 0.0
    for (x0, y0), (x1, y1) in zip(best, best[1:] + best[:1]):
        c = x0 * y1 - x1 * y0; a += c; cx += (x0 + x1) * c; cy += (y0 + y1) * c
    return cx / (3 * a), cy / (3 * a)


def ease(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)


def main():
    a = sys.argv[1:]
    out = a[0]
    opt = lambda k, d: a[a.index(k) + 1] if k in a else d
    src, dst = opt("--from", "36"), opt("--to", "06")
    label = opt("--label", "$800 ROUND TRIP")
    title = opt("--title", "NEW YORK \u2192 CALIFORNIA")
    secs = float(opt("--secs", "4")); theme = THEMES[opt("--theme", "noir")]
    bg, land, border, hi, route_c, txt = theme
    states = load_states(os.path.join(HERE, "states-albers-10m.json"))
    p0, p1 = centroid(states[src]), centroid(states[dst])
    mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
    # map space ~975x610; camera: start wide on whole US, end tighter on the route midpoint
    # vertical frame: start TIGHT on the origin, pull out until the whole route fits the width (reveal)
    z0, z1 = W / 1000 * 2.8, W / 1000 * 1.02
    c0, c1 = (p0[0], p0[1] - 40), (487, 290)
    font = ImageFont.truetype(ANTON, 96); small = ImageFont.truetype(ANTON, 54)
    tmp = tempfile.mkdtemp(prefix="mapins_")
    n = int(secs * FPS)
    SS = 2
    for f in range(n):
        t = f / FPS
        ts = math.floor(t * 12) / 12            # 12 fps stutter for overlays
        k = ease(t / secs)
        z = (z0 + (z1 - z0) * k) * SS
        cx = c0[0] + (c1[0] - c0[0]) * k; cy = c0[1] + (c1[1] - c0[1]) * k
        P = lambda p: ((p[0] - cx) * z + W * SS / 2, (p[1] - cy) * z + H * SS / 2 - 80 * SS)
        im = Image.new("RGB", (W * SS, H * SS), bg)
        dr = ImageDraw.Draw(im)
        hl = ease((ts - 0.2) / 0.5)
        for sid, polys in states.items():
            fill = land
            if sid in (src, dst) and hl > 0:
                fill = tuple(int(l + (h - l) * 0.55 * hl) for l, h in zip(land, hi))
            for poly in polys:
                dr.polygon([P(p) for p in poly[0]], fill=fill, outline=border)
                for hole in poly[1:]:
                    dr.polygon([P(p) for p in hole], fill=bg)
        # route arc (quadratic bezier bowed upward), draws on between 0.6 s and 2.0 s
        q0, q2 = P(p0), P(p1)
        q1 = ((q0[0] + q2[0]) / 2, min(q0[1], q2[1]) - 260 * SS)
        prog = ease((ts - 0.6) / 1.4)
        if prog > 0:
            m = 60; pts = []
            for i in range(int(m * prog) + 1):
                u = i / m
                pts.append(((1 - u) ** 2 * q0[0] + 2 * (1 - u) * u * q1[0] + u * u * q2[0],
                            (1 - u) ** 2 * q0[1] + 2 * (1 - u) * u * q1[1] + u * u * q2[1]))
            if len(pts) > 1:
                # dashed glow route
                glow = Image.new("RGBA", im.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
                gd.line(pts, fill=route_c + (150,), width=22 * SS, joint="curve")
                glow = glow.filter(ImageFilter.GaussianBlur(14 * SS))
                im.paste(glow, (0, 0), glow); dr = ImageDraw.Draw(im)
                for i in range(0, len(pts) - 1, 2):
                    dr.line(pts[i:i + 2], fill=route_c, width=9 * SS)
                hx, hy = pts[-1]
                dr.ellipse((hx - 16 * SS, hy - 16 * SS, hx + 16 * SS, hy + 16 * SS), fill=(255, 255, 255))
        # pins drop with overshoot
        for i, (pp, at) in enumerate(((q0, 0.15), (q2, 1.9))):
            u = (ts - at) / 0.35
            if u <= 0: continue
            drop = (1 - min(u, 1)) * 220 * SS - (math.sin(min(u, 1) * math.pi) * 18 * SS if u < 1 else 0)
            x, y = pp[0], pp[1] - drop
            r = 30 * SS
            dr.ellipse((x - r * 0.6, pp[1] - r * 0.25, x + r * 0.6, pp[1] + r * 0.25), fill=(0, 0, 0))
            dr.polygon([(x - r * 0.8, y - r * 1.6), (x + r * 0.8, y - r * 1.6), (x, y)], fill=hi)
            dr.ellipse((x - r, y - r * 2.6, x + r, y - r * 0.6), fill=hi, outline=(20, 20, 20), width=3 * SS)
            dr.ellipse((x - r * 0.38, y - r * 1.98, x + r * 0.38, y - r * 1.22), fill=bg)
        im = im.resize((W, H), Image.LANCZOS)
        dr = ImageDraw.Draw(im)
        # label slams in at 2.3 s
        u = ease((ts - 2.3) / 0.25)
        if u > 0:
            s = 1.25 - 0.25 * u
            f2 = ImageFont.truetype(ANTON, int(96 * s))
            tw = dr.textlength(label, font=f2)
            x, y = (W - tw) / 2, 1320
            dr.rounded_rectangle((x - 36, y - 16, x + tw + 36, y + 96 * s + 34), 26, fill=(0, 0, 0))
            dr.text((x, y), label, font=f2, fill=hi)
        # top title (static after 0.1 s; stays >= 1.8 s on screen)
        if ts >= 0.1:
            f3 = ImageFont.truetype(ANTON, 74)
            tw = dr.textlength(title, font=f3)
            dr.text(((W - tw) / 2, 420), title, font=f3, fill=txt, stroke_width=4, stroke_fill=(0, 0, 0))
        # vignette
        vg = Image.new("L", (W, H), 0); vd = ImageDraw.Draw(vg)
        vd.ellipse((-W * 0.35, -H * 0.2, W * 1.35, H * 1.2), fill=255)
        vg = vg.filter(ImageFilter.GaussianBlur(160))
        im = Image.composite(im, Image.new("RGB", (W, H), (0, 0, 0)), vg)
        im.save(os.path.join(tmp, f"f{f:04d}.png"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "f%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", out], check=True)
    print(json.dumps({"out": out, "frames": n, "from": src, "to": dst}))


if __name__ == "__main__":
    main()
