#!/usr/bin/env python3
"""pixabay_bg.py — fetch a backdrop/b-roll clip from Pixabay (v6.6 "bg"). Key from env PIXABAY_API_KEY (never printed).

    python3 -I engine/pixabay_bg.py "airport terminal" out.mp4 [--pick 0] [--secs 8] [--list]

safesearch on; skips clips tagged with revealing-clothing contexts or brands; people are allowed (ALWAYS look at the frames before publishing).
Prints JSON with the author ("user") and page URL for the description credit: "Footage: Pixabay (<user>)".
"""
import json, os, subprocess, sys, urllib.parse

# Shohjahon 2026-11-21 20:37: people ARE allowed in footage; the ban is on immodest/revealing clothing (and nudity). Logos/brands stay out.
AVOID = ("bikini", "swimsuit", "swimwear", "lingerie", "underwear", "sexy", "nude", "naked", "topless", "erotic", "sensual", "lady", "glamour", "bodybuilder",
         "beach", "pool", "fitness", "gym", "yoga", "dance", "dancer", "model", "fashion", "kiss", "logo", "brand")


def main():
    a = sys.argv[1:]
    if len(a) < 2: sys.exit(__doc__)
    q, out = a[0], a[1]
    opt = lambda k, d: a[a.index(k) + 1] if k in a else d
    pick, secs = int(opt("--pick", "0")), float(opt("--secs", "8"))
    key = os.environ.get("PIXABAY_API_KEY") or sys.exit("PIXABAY_API_KEY not set")
    url = "https://pixabay.com/api/videos/?" + urllib.parse.urlencode({"key": key, "q": q, "safesearch": "true", "per_page": 30})
    hits = json.loads(subprocess.run(["curl", "-sSf", url], capture_output=True, check=True, timeout=60).stdout)["hits"]  # curl: Pixabay 403s the urllib user agent
    ok = [h for h in hits if not any(w in h["tags"].lower().split(", ") for w in AVOID) and h["duration"] >= 5]
    if "--list" in a:
        for i, h in enumerate(ok): print(i, h["id"], h["duration"], h["user"], h["tags"])
        return
    if not ok: sys.exit("no clean clip for: " + q)
    h = ok[min(pick, len(ok) - 1)]; v = h["videos"]
    src = (v.get("medium") or v.get("large") or v["small"])["url"]
    tmp = out + ".src.mp4"
    subprocess.run(["curl", "-sSfL", "-o", tmp, src], check=True, timeout=180)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-t", str(secs), "-an", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", out], check=True)
    os.remove(tmp)
    print(json.dumps({"out": out, "id": h["id"], "user": h["user"], "page": h["pageURL"], "tags": h["tags"]}))


if __name__ == "__main__":
    main()
