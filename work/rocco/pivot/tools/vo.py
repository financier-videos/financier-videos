#!/usr/bin/env python3
"""ElevenLabs voice + character alignment for the pivot renderers.
usage: python3 vo.py lines.json out_dir VOICE_ID [model] [stability]
lines.json = [[key, text], ...]  ->  out_dir/<key>.mp3 + <key>.json (alignment)"""
import base64, json, os, sys, time, urllib.request
lines = json.load(open(sys.argv[1])); out = sys.argv[2]; voice = sys.argv[3]
model = sys.argv[4] if len(sys.argv) > 4 else "eleven_multilingual_v2"
stab = float(sys.argv[5]) if len(sys.argv) > 5 else 0.4
os.makedirs(out, exist_ok=True)
for i, (key, text) in enumerate(lines):
    if os.path.exists(f"{out}/{key}.json"): continue
    body = {"text": text, "model_id": model, "voice_settings": {"stability": stab, "similarity_boost": 0.8, "style": 0.35}}
    if i: body["previous_text"] = lines[i - 1][1]
    if i + 1 < len(lines): body["next_text"] = lines[i + 1][1]
    for a in range(4):
        try:
            rq = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps",
                data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "xi-api-key": "x"})
            r = json.load(urllib.request.urlopen(rq, timeout=120)); break
        except Exception as e:
            print(key, "retry", e, flush=True); time.sleep(3 + 3 * a)
    else: sys.exit(f"{key} failed")
    open(f"{out}/{key}.mp3", "wb").write(base64.b64decode(r["audio_base64"]))
    json.dump(r["alignment"], open(f"{out}/{key}.json", "w"))
    print(key, "ok", flush=True)
