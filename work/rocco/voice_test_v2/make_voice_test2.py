#!/usr/bin/env python3
"""rocco_voice_test2.mp4: designed character voices (design_voices.py previews). Rocco 1-8, Penny 9-12, + old F for reference.
  python3 -I work/rocco/voice_test_v2/make_voice_test2.py DESIGN_DIR OLD_F_MP3 OUTDIR"""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
src = open(os.path.join(ROOT, "work/rocco/style_v2_mock.py")).read(); src = src[:src.index("\na=bg(")]
src = src.replace("/tmp/fonts/LilitaOne-Regular.ttf", os.path.join(ROOT, "assets/fonts/LilitaOne-Regular.ttf")).replace("/tmp/fin_rocco_lib800/", "/tmp/fin_rocco_lib/")
G = {}; exec(src, G)
dd, oldf, out = sys.argv[1], sys.argv[2], sys.argv[3]; os.makedirs(out, exist_ok=True)
PICK = [("1", "R1_1", "street-smart wise-cracker"), ("2", "R1_3", "street-smart wise-cracker"),
        ("3", "R2_3", "noir detective, gravelly"), ("4", "R2_1", "noir detective, gravelly"),
        ("5", "R3_2", "scrappy & sarcastic"), ("6", "R3_1", "scrappy & sarcastic"),
        ("7", "R4_2", "warm & sly"), ("8", "R4_1", "warm & sly"),
        ("9", "P1_1", "bubbly & squeaky"), ("10", "P1_3", "bubbly & squeaky"),
        ("11", "P2_1", "playful & giggly"), ("12", "P2_2", "playful & giggly"), ("F", None, "old F (reference)")]
COL = [((255, 214, 64), (255, 170, 40)), ((64, 201, 198), (30, 150, 170)), ((178, 236, 120), (96, 200, 110)), ((255, 170, 205), (200, 120, 230))]
segs = []
t = G["bg"]((255, 214, 64), (255, 170, 40), dots=(255, 255, 255), rays=(255, 236, 140)); G["brand"](t)
G["txt"](t, (540, 480), "VOICE TEST #2", 120, (255, 255, 255), sw=14)
G["txt"](t, (540, 640), "Character voices", 72, (255, 255, 255), sw=10)
G["txt"](t, (540, 760), "Rocco: 1 - 8", 72, (255, 255, 255), sw=10); G["txt"](t, (540, 860), "Penny: 9 - 12  (F = old)", 72, (255, 255, 255), sw=10)
G["rocco"](t, "happy_00.webp", 640, 30, 1060); G["piggy"](t, 800, 1450, 420, "happy"); t.save(f"{out}/title.jpg", quality=93)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-i", f"{out}/title.jpg", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", "3",
                "-vf", "scale=1080:1920,format=yuv420p", "-r", "30", "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k", f"{out}/seg_00.mp4"], check=True)
segs.append(f"{out}/seg_00.mp4")
for k, (num, tag, desc) in enumerate(PICK, 1):
    role = "penny" if (tag is None or tag.startswith("P")) else "rocco"
    mp3 = oldf if tag is None else f"{dd}/{tag}.mp3"
    c1, c2 = COL[k % 4]
    im = G["bg"](c1, c2, dots=(255, 255, 255), rays=tuple(min(255, x + 40) for x in c1)); G["brand"](im)
    G["txt"](im, (540, 300), num, 330, (255, 255, 255), sw=16)
    G["txt"](im, (540, 560), ("ROCCO" if role == "rocco" else "PENNY") + " · " + desc.upper(), 60, (255, 255, 255), sw=9)
    if role == "rocco": G["rocco"](im, "happy_00.webp", 900, 90, 700)
    else: G["piggy"](im, 540, 1180, 760, "happy")
    im.save(f"{out}/{num}.jpg", quality=93)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-i", f"{out}/{num}.jpg", "-i", mp3,
                    "-af", "adelay=400|400,apad=pad_dur=0.7,loudnorm=I=-14:TP=-1.5,aresample=48000,aformat=channel_layouts=stereo",
                    "-vf", "scale=1080:1920,format=yuv420p", "-r", "30", "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k", "-shortest", f"{out}/seg_{k:02d}.mp4"], check=True)
    segs.append(f"{out}/seg_{k:02d}.mp4")
open(f"{out}/list.txt", "w").write("".join(f"file '{s}'\n" for s in segs))
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{out}/list.txt", "-c", "copy", f"{out}/rocco_voice_test2.mp4"], check=True)
d = json.load(open(f"{dd}/design.json"))
key = [{"num": n, "preview": t, "desc": ds, "generated_voice_id": (next(p["generated_voice_id"] for p in d[t[:2]]["previews"] if p["file"].endswith(t + ".mp3")) if t else None),
        "prompt": d[t[:2]]["prompt"] if t else "ElevenLabs premade Jessica cgSgspJ2msm6clMCkdW9"} for n, t, ds in PICK]
json.dump(key, open(f"{out}/voice_test2_key.json", "w"), indent=1); print("ok", f"{out}/rocco_voice_test2.mp4")
