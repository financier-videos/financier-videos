#!/usr/bin/env python3
"""Rocco VOICE LAB (copy of work/voice_lab/buck_voice_lab.py with the Rocco archetype). Buck VOICE LAB (one-off): design 3 comedic Buck voices (A/B/C) with ElevenLabs Voice Design (archetype prompts only —
no real person, no cloning, no Voice Library), save each to the account, then render a TTS sample of each with the
engine's performance settings (eleven_multilingual_v2, stability 0.28, similarity 0.75, style 0.85, speaker boost).

  python3 -I buck_voice_lab.py OUTDIR

Needs env ELEVENLABS_API_KEY (passed to curl on stdin, never printed) and network access to api.elevenlabs.io.
Writes OUTDIR/Buck_A_sample.mp3, _B_, _C_ (+ design previews) and OUTDIR/summary.json. Idempotent: a voice that
already exists under the same name is reused (no new design call).
"""
import base64, json, os, subprocess, sys, tempfile
import numpy as np

API = "https://api.elevenlabs.io/v1"
VARIANTS = [
    ("R", "Rocco (Scam Detective)", 505,
     "A warm, relaxed, wry adult male cartoon detective voice with a slightly husky low-mid tone. Calm and reassuring, "
     "with dry deadpan humor and a knowing half-smile in every line; slows down for the important warning, then lands a "
     "quick sarcastic aside. Clear American diction, friendly and trustworthy, never scary, never robotic or flat."),
]
PREVIEW_TEXT = ("Your package is being held? Huh. Funny... I didn't order anything. Red flag number one: they want a fee. "
                "Red flag number two: the link looks weird. Here's my move: I open the app myself. Case closed.")
SAMPLE_TEXT = ("A free package at your door... that you never ordered? Heh. That's not luck. That's a brushing scam. "
               "Keep it, it's yours, but change your password tonight. Send this to someone who still opens every box.")
MODEL = "eleven_multilingual_v2"
SETTINGS = {"stability": 0.28, "similarity_boost": 0.75, "style": 0.85, "use_speaker_boost": True}


def call(method, path, body=None, out=None, timeout=180, query=""):
    key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    hdr = (f"xi-api-key: {key}\n" if key else "") + "Accept: */*\n"
    tmpo = out or tempfile.mktemp(prefix="el_")
    cmd = ["curl", "-sS", "-X", method, "--max-time", str(timeout), "-H", "@-", "-w", "%{http_code}", "-o", tmpo]
    if body is not None:
        bf = tmpo + ".json"; json.dump(body, open(bf, "w")); cmd += ["-H", "Content-Type: application/json", "--data-binary", "@" + bf]
    cmd.append(API + path + query)
    try:
        p = subprocess.run(cmd, input=hdr.encode(), capture_output=True, timeout=timeout + 15)
        code = int((p.stdout.decode().strip() or "0")[-3:])
    except Exception:
        code = 0
    data = open(tmpo, "rb").read() if os.path.exists(tmpo) else b""
    if body is not None and os.path.exists(tmpo + ".json"): os.remove(tmpo + ".json")
    if out is None and os.path.exists(tmpo): os.remove(tmpo)
    return code, data


def f0_stats(path):
    wav = path + ".16k.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", path, "-ar", "16000", "-ac", "1", "-f", "f32le", wav], check=True)
    y = np.fromfile(wav, dtype=np.float32); os.remove(wav); sr = 16000
    n = int(0.04 * sr); hop = int(0.01 * sr); f0s = []; thr = 0.3 * np.sqrt(np.mean(y ** 2) + 1e-12)
    for i in range(0, len(y) - n, hop):
        fr = y[i:i + n] - y[i:i + n].mean()
        if np.sqrt(np.mean(fr ** 2)) < thr: continue
        ac = np.correlate(fr, fr, "full")[n - 1:]; lo, hi = int(sr / 400), int(sr / 70)
        j = lo + int(np.argmax(ac[lo:hi]))
        if ac[j] > 0.45 * ac[0]: f0s.append(sr / j)
    if len(f0s) < 10: return {"f0": 0.0, "spread": 0.0}
    f = np.array(f0s)
    return {"f0": round(float(np.median(f)), 1), "spread": round(float(np.percentile(f, 90) - np.percentile(f, 10)), 1)}


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "voice_lab"; os.makedirs(out, exist_ok=True)
    code, data = call("GET", "/voices", timeout=40)
    if code != 200:
        sys.exit(f"ElevenLabs not reachable/authorised (http {code}; key set: {bool(os.environ.get('ELEVENLABS_API_KEY'))})")
    existing = {v.get("name"): v["voice_id"] for v in json.loads(data).get("voices", [])}
    summary = {"model": MODEL, "settings": SETTINGS, "sample_text": SAMPLE_TEXT, "variants": []}
    for tag, name, seed, prompt in VARIANTS:
        rec = {"variant": tag, "name": name, "prompt": prompt, "seed": seed}
        vid = existing.get(name)
        if not vid:
            design = None
            for model in ("eleven_ttv_v3", "eleven_multilingual_ttv_v2"):
                code, raw = call("POST", "/text-to-voice/design",
                                 {"voice_description": prompt, "model_id": model, "text": PREVIEW_TEXT, "seed": seed},
                                 query="?output_format=mp3_44100_128")
                if code == 200: design = json.loads(raw); rec["design_model"] = model; break
                rec.setdefault("design_errors", []).append(f"{model}: http {code} {raw[:200]!r}")
            if not design: summary["variants"].append(rec); continue
            prev = []
            for i, p in enumerate(design.get("previews", [])):
                f = os.path.join(out, f"Rocco_{tag}_design_preview_{i + 1}.mp3")
                open(f, "wb").write(base64.b64decode(p["audio_base_64"]))
                st = f0_stats(f)
                prev.append({"i": i + 1, "gid": p["generated_voice_id"], **st,
                             "score": st["spread"] - 0.4 * abs(st["f0"] - 150) if st["f0"] else -999})
            best = max(prev, key=lambda q: q["score"]); rec["previews"] = [{k: v for k, v in q.items() if k != "gid"} for q in prev]
            rec["chosen_preview"] = best["i"]
            body = {"voice_name": name, "voice_description": prompt, "generated_voice_id": best["gid"],
                    "played_not_selected_voice_ids": [q["gid"] for q in prev if q is not best]}
            code, raw = call("POST", "/text-to-voice", body)
            if code != 200: rec["save_error"] = f"http {code} {raw[:300]!r}"; summary["variants"].append(rec); continue
            vid = json.loads(raw)["voice_id"]
        else:
            rec["existing"] = True
        rec["voice_id"] = vid
        mp3 = os.path.join(out, f"Rocco_{tag}_sample.mp3")
        code, raw = call("POST", f"/text-to-speech/{vid}", {"text": SAMPLE_TEXT, "model_id": MODEL, "voice_settings": SETTINGS},
                         out=mp3, query="?output_format=mp3_44100_128")
        if code == 200 and os.path.getsize(mp3) > 1000: rec["sample"] = mp3; rec["sample_stats"] = f0_stats(mp3)
        else:
            rec["tts_error"] = f"http {code} {raw[:200]!r}"
            if os.path.exists(mp3): os.remove(mp3)
        summary["variants"].append(rec)
    json.dump(summary, open(os.path.join(out, "summary.json"), "w"), indent=2)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
