#!/usr/bin/env python3
"""Rocco style v2 voice test (docs/rocco_style_v2.md rule 7): 4 Rocco candidates (A-D) + 2 Penny candidates (E-F),
same line per role, ElevenLabs premade (stock) voices - no cloning, no real person. Output: rocco_voice_test.mp4
  python3 -I work/rocco/voice_test_v2/make_voice_test.py OUTDIR
"""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
src = open(os.path.join(ROOT, "work/rocco/style_v2_mock.py")).read()
src = src[:src.index("\na=bg(")]  # only the drawing helpers (bg, rocco, piggy, txt, bubble, cap, brand, phone)
src = src.replace("/tmp/fonts/LilitaOne-Regular.ttf", os.path.join(ROOT, "assets/fonts/LilitaOne-Regular.ttf")).replace("/tmp/fin_rocco_lib800/", "/tmp/fin_rocco_lib/")
G = {}; exec(src, G)
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
ROCCO_LINE = "Red flag. A stranger sends you a thousand dollars, and five seconds later he says it was a mistake. Don't send it back. Report it in the app."
PENNY_LINE = "Rocco! A stranger sent me a thousand dollars! Wait... now he says it was a mistake? How did you KNOW?!"
C = [("A", "Roger", "CwhRBWXzGAHq8TQ4Fs17", "rocco", (255, 214, 64), (255, 170, 40)),
     ("B", "Chris", "iP95p4xoKVk53GoZ742B", "rocco", (64, 201, 198), (30, 150, 170)),
     ("C", "Callum", "N2lVS1w4EtoT3dr4eOWO", "rocco", (178, 236, 120), (96, 200, 110)),
     ("D", "Will", "bIHbv24MWmeRgasZH58o", "rocco", (255, 170, 205), (200, 120, 230)),
     ("E", "Laura", "FGY2WhTYpPnrIDTdsKH5", "penny", (255, 214, 64), (255, 150, 90)),
     ("F", "Jessica", "cgSgspJ2msm6clMCkdW9", "penny", (64, 201, 198), (120, 170, 255))]
SET = {"stability": 0.38, "similarity_boost": 0.75, "style": 0.55, "use_speaker_boost": True}

def tts(vid, text, path):
    if os.path.exists(path) and os.path.getsize(path) > 2000: return
    body = json.dumps({"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": SET})
    r = subprocess.run(["curl", "-sS", "-o", path, "-w", "%{http_code}", "-X", "POST",
                        f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128",
                        "-H", "xi-api-key: proxy-injected", "-H", "Content-Type: application/json", "--data-binary", body],
                       capture_output=True, text=True)
    if r.stdout.strip() != "200": sys.exit(f"tts {vid}: http {r.stdout} {open(path,'rb').read()[:200]}")

def card(letter, name, role, c1, c2, path):
    im = G["bg"](c1, c2, dots=(255, 255, 255), rays=tuple(min(255, x + 40) for x in c1))
    G["brand"](im)
    G["txt"](im, (540, 300), letter, 330, (255, 255, 255), sw=16)
    G["txt"](im, (540, 560), ("ROCCO" if role == "rocco" else "PENNY") + " · VOICE " + letter, 78, (255, 255, 255), sw=10)
    if role == "rocco": G["rocco"](im, "happy_00.webp", 900, 90, 700)
    else: G["piggy"](im, 540, 1180, 760, "happy")
    G["txt"](im, (540, 1760), name + " (ElevenLabs stock voice)", 52, (255, 255, 255), sw=8)
    im.save(path, quality=93)

segs = []
t = G["bg"]((255, 214, 64), (255, 170, 40), dots=(255, 255, 255), rays=(255, 236, 140)); G["brand"](t)
G["txt"](t, (540, 520), "ROCCO VOICE TEST", 110, (255, 255, 255), sw=14)
G["txt"](t, (540, 700), "Rocco: pick A, B, C or D", 70, (255, 255, 255), sw=10)
G["txt"](t, (540, 820), "Penny: pick E or F", 70, (255, 255, 255), sw=10)
G["rocco"](t, "happy_00.webp", 640, 30, 1060); G["piggy"](t, 800, 1450, 420, "happy")
t.save(f"{out}/title.jpg", quality=93)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-i", f"{out}/title.jpg", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                "-t", "3", "-vf", "scale=1080:1920,format=yuv420p", "-r", "30", "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k", f"{out}/seg_0.mp4"], check=True)
segs.append(f"{out}/seg_0.mp4")
for i, (L, nm, vid, role, c1, c2) in enumerate(C, 1):
    mp3 = f"{out}/{L}_{nm}.mp3"; tts(vid, ROCCO_LINE if role == "rocco" else PENNY_LINE, mp3)
    card(L, nm, role, c1, c2, f"{out}/{L}.jpg")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-i", f"{out}/{L}.jpg", "-i", mp3,
                    "-af", "adelay=500|500,apad=pad_dur=0.8,loudnorm=I=-14:TP=-1.5,aresample=48000,aformat=channel_layouts=stereo",
                    "-vf", "scale=1080:1920,format=yuv420p", "-r", "30", "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k", "-shortest", f"{out}/seg_{i}.mp4"], check=True)
    segs.append(f"{out}/seg_{i}.mp4")
open(f"{out}/list.txt", "w").write("".join(f"file '{s}'\n" for s in segs))
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{out}/list.txt", "-c", "copy", f"{out}/rocco_voice_test.mp4"], check=True)
print(json.dumps({"out": f"{out}/rocco_voice_test.mp4", "candidates": [(c[0], c[1], c[2], c[3]) for c in C]}))
