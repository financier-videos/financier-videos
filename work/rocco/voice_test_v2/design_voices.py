#!/usr/bin/env python3
"""Rocco v2 voice test #2 (Shohjahon 2026-11-22: none of the stock Rocco voices fit; Penny F a bit better; "study how such
characters usually sound first"). Character archetypes (research): cartoon raccoons = fast-talking, street-smart, slightly
raspy/nasal wise-crackers; comic noir detective = deadpan, private-eye cadence; cartoon pig sidekick = high, bubbly,
slightly nasal, naive, big reactions. ElevenLabs Voice Design (text prompt only - no cloning, no real person).
Writes OUTDIR/<tag>_<n>.mp3 previews + OUTDIR/design.json (generated_voice_id per preview; save the chosen one later).
  python3 -I work/rocco/voice_test_v2/design_voices.py OUTDIR
"""
import base64, json, os, subprocess, sys
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
ROCCO_TEXT = "Red flag. A stranger sends you a thousand dollars, and five seconds later he says it was a mistake. Don't send it back. Report it in the app."
PENNY_TEXT = "Rocco! A stranger sent me a thousand dollars! Wait... now he says it was a mistake? How did you KNOW?! Should I send it back? I'm NICE!"
P = [("R1", "rocco", "Wise-cracking cartoon raccoon detective. Fast-talking, street-smart male voice, mid thirties, slightly raspy and a little nasal, wry and playful, quick comic timing, confident deadpan one-liners, animated movie character energy, American accent."),
     ("R2", "rocco", "Comic noir parody detective who is a cartoon raccoon. Low, smoky, gravelly male voice with a dramatic old-time private-eye cadence, but warm and funny, dry deadpan punchlines, clear diction, animated series character."),
     ("R3", "rocco", "Scrappy cartoon raccoon detective. Mid-high, raspy, mischievous male voice, quick and snappy, sarcastic but lovable, a smirk in every line, big cartoon energy, American accent."),
     ("R4", "rocco", "Friendly cartoon raccoon detective for a family animation. Bright, warm, slightly husky young male voice, clever and curious, upbeat with sly dry humor, crisp American accent, big animated personality."),
     ("P1", "penny", "Cartoon piggy bank character. High-pitched, bubbly, excitable young woman's voice, sweet and a bit naive, slightly nasal and squeaky but clear, fast and breathless when excited, endearing comic sidekick, American accent."),
     ("P2", "penny", "Cheerful cartoon pig sidekick. Bright, playful, youthful female voice with a cute rounded slightly squeaky tone, big expressive reactions, gasps and giggles, warm American accent, animated series energy.")]

def call(path, body):
    r = subprocess.run(["curl", "-sS", "-X", "POST", "--max-time", "240", "https://api.elevenlabs.io/v1" + path + "?output_format=mp3_44100_128",
                        "-H", "xi-api-key: proxy-injected", "-H", "Content-Type: application/json", "--data-binary", json.dumps(body), "-w", "\n%{http_code}"],
                       capture_output=True, text=True)
    body_txt, code = r.stdout.rsplit("\n", 1)
    return int(code or 0), body_txt

res = json.load(open(f"{out}/design.json")) if os.path.exists(f"{out}/design.json") else {}
for tag, role, prompt in P:
    if tag in res: continue
    for model in ("eleven_ttv_v3", "eleven_multilingual_ttv_v2"):
        code, raw = call("/text-to-voice/design", {"voice_description": prompt, "model_id": model, "text": ROCCO_TEXT if role == "rocco" else PENNY_TEXT, "seed": 77})
        if code == 200: break
        print(tag, model, code, raw[:200], file=sys.stderr)
    if code != 200: continue
    d = json.loads(raw); prev = []
    for i, p in enumerate(d.get("previews", [])[:3], 1):
        f = f"{out}/{tag}_{i}.mp3"; open(f, "wb").write(base64.b64decode(p["audio_base_64"]))
        prev.append({"file": f, "generated_voice_id": p["generated_voice_id"]})
    res[tag] = {"role": role, "prompt": prompt, "model": model, "previews": prev}
    json.dump(res, open(f"{out}/design.json", "w"), indent=1)
    print(tag, model, len(prev))
