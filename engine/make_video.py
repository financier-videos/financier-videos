#!/usr/bin/env python3
"""FINANCIER video engine v6 CINEMA (camera + parallax + grading + motion blur + stereo SFX; ElevenLabs Buck; 3D Buck v2) — Kokoro narrator + PIL frames + ffmpeg.

Usage:
  python3 -I make_video.py spec.json out.mp4 --model kokoro.onnx --voices voices.bin
  python3 -I make_video.py design-buck OUTDIR [--seed 4241] [--no-save] [--force]   # one-time: create Buck's ElevenLabs voice
  python3 -I make_video.py buck-say "Line" out.wav [--model .. --voices ..]          # quick test of Buck's voice

v5 BUCK VOICE (ElevenLabs, primary): Buck's lines ("buck" field) are spoken by OUR OWN ElevenLabs voice "Buck (Financier)",
  made with Voice Design from a text prompt (no cloning, no real person, not from the Voice Library). Needs env
  ELEVENLABS_API_KEY and network access to api.elevenlabs.io (a network secret on that host also works). Voice id:
  BUCK_EL["voice_id"] -> env FIN_BUCK_VOICE_ID -> lookup by name. Model: BUCK_EL["models"] in order (first that works).
  Every line is cached in FIN_TTS_CACHE (credits are spent once per line). If anything fails, Buck falls back to
  Kokoro am_puck (pitched) and the result JSON says so in "buck_voice" — check it in QC and note it in the journal.
  Spec "buck_voice": {"engine": "kokoro"} forces the old voice; {"model": "...", "settings": {...}} overrides.
  v6 (2026-11-19 22:56, Shohjahon): THERE IS NO SEPARATE NARRATOR. Buck speaks every line of every video ("text"/"say")
  with the same ElevenLabs voice; "buck" asides are still Buck (bubble + voice). Voice variants: BUCK_VARIANTS A/B/C
  (A = default until Shohjahon picks; spec "buck_voice": {"variant": "B"} or env FIN_BUCK_VARIANT). TTS: model
  eleven_multilingual_v2, stability 0.28, similarity 0.75, style 0.85, speaker boost; previous/next line sent for
  natural flow; /with-timestamps gives word times -> captions follow Buck's real pauses. Write lines like a
  performance: "..." pauses, "Whoa!", "Wait a second...", "Heh.", "Okay, okay..." (in BOTH "text" and "say").
  Kokoro (am_puck pitched) is only an emergency fallback; result JSON "buck_voice" shows it -> do NOT publish then.
  Spec "narrator": "kokoro" brings back the old am_michael narrator (only if Shohjahon asks).

v6 CINEMA QUALITY (default ON; spec "cinema": false = old look, e.g. for quick tests):
  - camera: every scene gets gentle eased camera moves every 1.5-2 s (push-in / pull-out / drift; seeded per scene).
    Scene "cam": false switches it off for one scene; spec "camera": false for the whole video. Crash "zoom" stacks on top.
  - 3D parallax: background layer moves 0.55x, content (stats, Buck, headline) 1x, a near layer of soft bokeh 1.6x.
    Warm light leaks sweep in on flash/slide cuts. Captions, brand and progress bar never move.
  - motion blur: sub-frame blur on punch/slide cuts, camera shake and crash-zoom snaps; Buck's roll_in/drop_in blur.
    Coin rain gets motion streaks.
  - grade: filmic S-curve with teal shadows / warm highlights, soft bloom on highlights, radial lens fringing,
    vignette, fine film grain (captions are composited after the grade, then grain over everything).
  - sound: STEREO mix. Voice centre; effects panned (corner Buck left, VS panels left/right, slide whoosh travels,
    coin rain wide); auto riser + sub-boom under every stat, shimmer on flash cuts, faint room tone, short stereo
    reverb on effects, effects duck ~5 dB under the voice.
  Render time ~2x of v5 (35 s Short ~4-5 min on 2 cores).

spec.json:
{
  "format": "short" | "long",          # short = 1080x1920, long = 1920x1080
  "style": "rocco"   # v6.12: Rocco look (case-file headline, typewriter, red stamp stats, label captions); scene "phone": {"from": "Unknown number", "msgs": [{"t": "...", "at": 0.3, "flag": true}]}
  "brand": "FINANCIER", "brand_color": "#F5C542"   # v6.11: corner brand text (Rocco: "RED FLAG ROCCO"); character library = env FIN_BUCK3D (Rocco: work/rocco/rocco_sprites.py)
  "bg": "clip.mp4" | ["a.mp4", "b.jpg", ...],   # v6.6: real blurred BACKDROP behind non-b-roll scenes (list = rotates per scene; scene "bg" overrides, false = plain); "bg_mix": 0.62, "bg_blur": 6, "bg_bright": 1.0 (v6.9: 1.3–1.5 = brighter theme + less backdrop dimming; A/B, notes/2026-11-21_color.md). Fetch: engine/pixabay_bg.py
  "theme": "vault|mint|ember|royal|ocean|noir",   # v6.1 background look (palette + pattern); omit = picked from the first line. Never the same theme for two videos in a row.
  "voice": "am_michael", "speed": 1.05,
  "scenes": [
    {"text": "spoken line", "head": "ON-SCREEN HEADLINE", "color": "#F5C542",
     "broll": "/path/clip.mp4" (optional), "stat": "83%" (optional big number)}
  ],
  "source": "Source: ... (optional, shown small at the bottom)",   # scene "show_source": true shows it; "show_source": "Source: X" shows that text instead (v6.2)
  "sfx": true,              # auto whoosh on scene change + pop when a stat appears
  "ambient": "birds",       # optional soft bird/breeze bed under the whole video; "ambient_vol": 0.08
}
Scene "sfx": list of extra effects: coin, cash, impact, tick, birds, whoosh, pop (all synthesized).
Animation (v2): stats count up with an overshoot "punch"; karaoke captions (active word gold, numbers green);
animated background (light sweep, self-drawing chart line, floating $); Ken Burns on b-roll; scene transitions.
Scene extras: "chart": {"labels": ["2014","2024"], "values": [1.42, 3.69], "texts": ["1.42¢","3.69¢"], "at": [0.3, 1.2]} (animated bars;
optional "at" = seconds after scene start when each bar grows, to sync bars with the narration — rule of three!; v6.5 "hi": 0 = which bar is highlighted, default the last one),
"fx": ["coin_rain", "arrow_up" | "arrow_down"], "transition": "punch" | "flash" | "slide".
v2.2: "say": what the voice reads (captions keep "text"); money/percent are auto-normalized for TTS
($58.63 -> "58 dollars and 63 cents", $1.2 trillion -> "1.2 trillion dollars", 9% -> "9 percent").
v3 HUMOR PACK (scene fields):
  "beat": 0.5            comedic pause (silence) BEFORE the line; the mascot/sticker reacts during it.
  "land": 0.4            v6.7: extra silence AFTER the line (punchline "landing"; comics pause after the joke so it registers,
                         keep speech rate steady and vary the gaps instead). Use on 1-2 punchlines per Short, 0.3-0.6 s.
  "mascot": {"mood": "shocked|happy|laugh|smug|confused|sideeye|sad|angry|point|dizzy|thumbsup|proud",
             "say": "short bubble text (<= 6 words)", "pos": "center|corner", "at": 0.0,
             "act": "roll_in|drop_in|flip|bonk|dodge", "act_at": 0.0}
            BUCK = the channel's own cartoon coin (green bow tie, green sneakers, white gloves). Physical comedy:
            roll_in/drop_in = entrances; flip = coin-flip jump; bonk = a price tag falls on his head (stars; pair
            with mood "dizzy", then "thumbsup" in the next scene); dodge = leans back as a price tag flies past. "center" = big (scene must have no stat/chart);
            "corner" = small, upper-left between headline and stat (works with stat/b-roll; avoid with chart). Default pos picks itself.
  "sticker": "MYTH?"     meme-style label that slaps onto the screen (Bangers font, tilted). "sticker_color": "#FF4D4D",
                         "sticker_at": 1.6 (seconds after scene start). Big & centred when the scene has no stat/chart/mascot.
  "look": "sepia"        old-film look for "legend says..." / history beats (flicker + grain).
  "shake": 0.35          camera shake (seconds) at scene start, for punchlines/impacts.
  sfx timing: "ding@5.0" plays 5.0 s after the scene starts (sync the hit with the punchline word).
  new "sfx": scratch (record scratch), boing, slide_up, slide_down, bonk, ding, buzzer, crickets, drumroll, wahwah.
  "buck": "I'm okay!"    BUCK SPEAKS this extra line in his own voice (ElevenLabs Buck; fallback Kokoro) — before the scene line,
                         or after it with "buck_after": true. "text" may be "" (Buck-only scene). The bubble shows his line.
BUCK 3D (v4; library v2 = the 2026-11-20 hybrid Buck with top hat + monocle, else v1): if the sprite library exists
  (env FIN_BUCK3D, else auto-download from GitHub media/assets/buck3d_v2.tar, then buck3d_v1.tar),
  Buck is the 3D Blender-rendered character (buck3d.py); otherwise the 2D drawing. "buck3d": false forces 2D.
Global: "loop": true -> last 0.2 s blends into the first frame (pair with a script whose last line flows into the first).
v4.1 SPLIT-SCREEN "VS" (scene field; replaces stat/chart in that scene; don't combine with "mascot"):
  "vs": {"left": "$86", "left_label": "People guessed", "left_sub": "per month",
         "right": "$219", "right_label": "They actually paid", "right_sub": "per month",
         "win": "right" | "left" | null, "at": [0.3, 2.4], "vs_at": 1.4,
         "left_color": "#9AA4B8", "right_color": "#F5C542"}
  Two panels slide in from the sides at "at" (seconds after scene start; sync the 2nd with the word that reveals it),
  a red VS badge slams in between (vs_at, default midway), values count up; ~0.9 s after the 2nd panel the winner
  glows and the other side dims. Auto sfx: pop per panel + light impact on the VS badge. Myth vs fact, guess vs reality,
  then vs now, plan A vs plan B. Shorts: layout shifted left of the like/comment buttons.
  v6.3: a panel whose "at" > 0.25 s shows a pulsing dashed "?" placeholder in its slot until it lands (no empty middle);
  "no_ghost": true switches that off.
v4.2 REACTION CRASH-ZOOM (scene field):
  "zoom": {"at": 0.0, "amt": 1.25, "hold": 0.8, "on": "buck|stat|sticker|center|[x, y]"}
                         camera snaps in (0.14 s, slight overshoot) on the reaction, holds, eases back out (0.2 s).
                         "at" = seconds after scene start (0.0 + "beat" = zoom on Buck's face during the comic pause);
                         "hold": -1 = stay zoomed to the scene end; [x, y] = fractions of the frame. Default "on" = buck if
                         the scene has Buck, else center. Captions, brand and progress bar stay put (not zoomed).
                         Auto "whip" sfx at the zoom (needs global "sfx": true). Use 1-2 per Short, amt 1.15-1.35
                         (on a big stat <= 1.15 or the number touches the edges; a corner Buck is auto-kept in frame).
  new "sfx": whip (short rising swish for crash zooms / fast moves).
  v6.8 "sfx": fxr_pickup, fxr_powerup, fxr_hurt, fxr_select, fxr_jump (8-bit game palette via pyfxr, engine/sfx_fxr.py;
  skipped silently if pyfxr is missing). 1-2 per Short: coin grab / win / money lost / list beat / Buck hop.
  v6.8 lip-sync: Rhubarb phoneme cues drive Buck's mouth when the binary exists (env FIN_RHUBARB, default
  ~/tools/rhubarb/...; never in the repo). Spec "lipsync": "envelope" forces the old loudness method.
"""
import json, os, re, subprocess, sys, argparse, math, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps, ImageChops

ANTON = "/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf"
INTER_XB = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
INTER_SB = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
FPS = 30
GOLD = (245, 197, 66); GREEN = (43, 214, 123); WHITE = (245, 247, 250); GREY = (150, 160, 180)


def hex2rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


_SCALE = r'(thousand|million|billion|trillion)'


def say_text(x):
    """Make money/percent read naturally in Kokoro (it reads "$58.63" as "dollar fifty-eight point six three")."""
    x = re.sub(r'\$(\d[\d,]*(?:\.\d+)?)\s*' + _SCALE, r'\1 \2 dollars', x)
    x = re.sub(r'\$(\d[\d,]*(?:\.\d+)?)([KMBT])\b', lambda m: m.group(1) + " " + {"K": "thousand", "M": "million", "B": "billion", "T": "trillion"}[m.group(2)] + " dollars", x)
    x = re.sub(r'\$(\d[\d,]*)\.(\d\d)\b', lambda m: f"{m.group(1)} dollar{'s' if m.group(1) != '1' else ''} and {int(m.group(2))} cents", x)
    x = re.sub(r'\$(\d[\d,]*)\b', lambda m: f"{m.group(1)} dollar{'s' if m.group(1) != '1' else ''}", x)
    x = re.sub(r'(\d+(?:\.\d+)?)\s*%', r'\1 percent', x)
    x = re.sub(r'(\d+(?:\.\d+)?)\s*¢', r'\1 cents', x)
    return x.replace("…", "...").replace("—", ", ")


_UZ_APOS = "'\u2019\u2018\u02bb\u02bc`"
_UZ_MAP = {"a": "а", "b": "б", "d": "д", "e": "е", "f": "ф", "g": "г", "h": "ҳ", "i": "и", "j": "ж", "k": "к", "l": "л",
           "m": "м", "n": "н", "o": "о", "p": "п", "q": "қ", "r": "р", "s": "с", "t": "т", "u": "у", "v": "в", "x": "х",
           "y": "й", "z": "з", "c": "с", "w": "в"}


def uz_cyr(x):
    """2026-11-20 (Shohjahon): eleven_v3 reads Uzbek Latin g' like English g and x like "eks"; the Cyrillic spelling
    (ғ, х) was judged correct. Uzbek Latin -> Cyrillic for the VOICE only (captions stay Latin). Spec "lang": "uz"."""
    out = []; i = 0; n = len(x)
    while i < n:
        c = x[i]; lo = c.lower(); nx = x[i + 1] if i + 1 < n else ""; prev = x[i - 1] if i > 0 else ""
        if lo in "og" and nx and nx in _UZ_APOS:
            d = "ў" if lo == "o" else "ғ"; out.append(d.upper() if c.isupper() else d); i += 2; continue
        if lo in "sc" and nx.lower() == "h":
            d = "ш" if lo == "s" else "ч"; out.append(d.upper() if c.isupper() else d); i += 2; continue
        if lo == "y" and nx.lower() in ("o", "u", "a", "e") and not (nx.lower() == "o" and i + 2 < n and x[i + 2] in _UZ_APOS):
            d = {"o": "ё", "u": "ю", "a": "я", "e": "е"}[nx.lower()]; out.append(d.upper() if c.isupper() else d); i += 2; continue
        if lo == "e" and not prev.isalpha():
            out.append("Э" if c.isupper() else "э"); i += 1; continue
        if c in _UZ_APOS and prev.isalpha() and nx.isalpha():
            out.append("ъ"); i += 1; continue
        if lo in _UZ_MAP:
            d = _UZ_MAP[lo]; out.append(d.upper() if c.isupper() else d); i += 1; continue
        out.append(c); i += 1
    return "".join(out)


# Uzbek pronunciation lexicon for the VOICE (lower-case Latin word -> what TTS reads, inserted as-is, not transliterated).
# Built from Shohjahon's listening tests (2026-11-20, voice "Finansist 8"): a Latin word inside Cyrillic text fixed
# "shoshmela". Spec "uz_lex": {...} adds/overrides entries. Keep each value ONE word (caption timing maps word by word).
UZ_LEX = {"shoshmela": "Shoshmela", "shoshmang": "Shoshmang"}


def uz_voice_text(x, lex=None):
    """Latin Uzbek line -> voice text: lexicon words as given, everything else uz_cyr()."""
    lx = dict(UZ_LEX, **{k.lower(): v for k, v in (lex or {}).items()})
    def one(m):
        w = m.group(0); key = w.lower()
        return (lx[key][0].upper() + lx[key][1:] if w[0].isupper() else lx[key]) if key in lx else uz_cyr(w)
    # v3 audio tags ("[sarcastic]", "[whispers]", one word each) pass through untouched
    return "".join(part if part.startswith("[") else re.sub(r"[A-Za-z" + _UZ_APOS + r"]+", one, part)
                   for part in re.split(r"(\[[^\]]*\])", x))


# ---------------- BUCK's voice ----------------
# v5 PRIMARY: our own ElevenLabs voice (Voice Design from a text prompt; owned by the channel's ElevenLabs account).
EL_API = "https://api.elevenlabs.io/v1"
BUCK_VARIANTS = {"A": "Buck A (Trickster)", "B": "Buck B (Adventurer)", "C": "Buck C (Con-Artist)", "D": "Buck D (Wisecracker)", "UZ": "Finansist 8 (Tashkent)"}  # UZ: Uzbek profile voice (Shohjahon 2026-11-20)  # voice lab 2026-11-19
BUCK_VARIANT = os.environ.get("FIN_BUCK_VARIANT", "A")  # A until Shohjahon picks (then set here)
BUCK_EL = {"name": BUCK_VARIANTS.get(BUCK_VARIANT, BUCK_VARIANTS["A"]), "voice_id": "",  # or env FIN_BUCK_VOICE_ID
           "fallback_names": ["Buck A (Trickster)", "Buck (Financier)"],
           "models": ["eleven_multilingual_v2"],
           "settings": {"stability": 0.28, "similarity_boost": 0.75, "style": 0.85, "use_speaker_boost": True}}
BUCK_PROMPT = ("A warm, energetic, and charismatic young adult male voice with a crisp American accent. Cheerful, slightly "
               "cheeky, and expressive like a brave cartoon adventurer. Bright, resonant mid-high pitch, clear articulation, "
               "and comedic timing. Sounds optimistic, friendly, and quick-witted, never arrogant or harsh.")
BUCK_SAMPLE = ("Hey there, I'm Buck! Yes, the coin with the bow tie. Relax, I have a plan. Prices going up again? "
               "Not today, price tag! Ow... worth it. Money doesn't grow on trees. I checked! Stick with me, "
               "and every dollar makes a little more sense.")
TTS_CACHE = os.environ.get("FIN_TTS_CACHE", os.path.join(tempfile.gettempdir(), "fin_tts_cache"))
_EL = {"vid": None, "why": "", "used": []}


def el_call(method, path, body=None, out=None, timeout=90, query=""):
    """ElevenLabs request through curl (uses the session proxy). The API key goes in on stdin (-H @-), never on the
    command line. Returns (http_code, bytes); bytes also written to `out` if given."""
    import hashlib
    key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    hdr = (f"xi-api-key: {key}\n" if key else "") + "Accept: */*\n"
    cmd = ["curl", "-sS", "-X", method, "--max-time", str(timeout), "-H", "@-", "-w", "%{http_code}"]
    tmpo = out or os.path.join(tempfile.gettempdir(), "el_" + hashlib.sha1((path + str(os.getpid())).encode()).hexdigest()[:10])
    cmd += ["-o", tmpo]
    if body is not None:
        bf = tmpo + ".json"; json.dump(body, open(bf, "w")); cmd += ["-H", "Content-Type: application/json", "--data-binary", "@" + bf]
    cmd.append(EL_API + path + query)
    try:
        p = subprocess.run(cmd, input=hdr.encode(), capture_output=True, timeout=timeout + 15)
        code = int((p.stdout.decode().strip() or "0")[-3:])
    except Exception:
        code = 0
    data = open(tmpo, "rb").read() if os.path.exists(tmpo) else b""
    if body is not None and os.path.exists(tmpo + ".json"): os.remove(tmpo + ".json")
    if out is None and os.path.exists(tmpo): os.remove(tmpo)
    return code, data


def el_voice_id(name=None):
    """Buck's ElevenLabs voice id: BUCK_EL["voice_id"] -> env FIN_BUCK_VOICE_ID -> look up by name (variant, then fallbacks)."""
    if _EL["vid"] is None or name:
        vid = (None if name else (BUCK_EL.get("voice_id") or os.environ.get("FIN_BUCK_VOICE_ID", ""))) or ""
        if not vid:
            code, data = el_call("GET", "/voices", timeout=40)
            if code == 200:
                have = {v.get("name"): v["voice_id"] for v in json.loads(data).get("voices", [])}
                for nm in [name or BUCK_EL["name"]] + BUCK_EL.get("fallback_names", []):
                    if nm in have: vid = have[nm]; _EL["name"] = nm; break
                if not vid: _EL["why"] = f"voice '{name or BUCK_EL['name']}' not found (run the voice lab)"
            else:
                _EL["why"] = f"ElevenLabs not reachable (http {code}; key set: {bool(os.environ.get('ELEVENLABS_API_KEY'))})"
        _EL["vid"] = vid
    return _EL["vid"]


def _words_from_alignment(al):
    """ElevenLabs character alignment -> [(word, start, end)]."""
    if not al: return []
    ch = al.get("characters") or []; st = al.get("character_start_times_seconds") or []; en = al.get("character_end_times_seconds") or []
    words = []; cur = ""; t0 = t1 = None
    for c, a, b in zip(ch, st, en):
        if c.isspace():
            if cur: words.append((cur, t0, t1)); cur = ""
            continue
        if not cur: t0 = a
        cur += c; t1 = b
    if cur: words.append((cur, t0, t1))
    return words


def el_speak(text, workdir, tag, cfg=None, prev=None, nxt=None, sr=24000):
    """Buck speaks `text` (ElevenLabs, with word timestamps) -> (float32 mono at sr, [(word, start, end)]) or None."""
    import hashlib, base64, soundfile as sf
    cfg = cfg or {}
    vid = cfg.get("voice_id") or (el_voice_id(BUCK_VARIANTS[cfg["variant"]]) if cfg.get("variant") in BUCK_VARIANTS else el_voice_id())
    if not vid: return None
    models = [cfg["model"]] if cfg.get("model") else BUCK_EL["models"]
    settings = dict(BUCK_EL["settings"], **cfg.get("settings", {}))
    txt = text.replace("…", "...").strip()
    os.makedirs(TTS_CACHE, exist_ok=True)
    for m in models:
        h = hashlib.sha1(json.dumps([vid, m, txt, settings, prev, nxt], sort_keys=True).encode()).hexdigest()[:16]
        base = os.path.join(TTS_CACHE, f"buck_{h}")
        if not (os.path.exists(base + ".mp3") and os.path.exists(base + ".json")):
            ok = False
            for st in (settings, None):  # retry without voice_settings if the model rejects one of them
                body = {"text": txt, "model_id": m}
                if st: body["voice_settings"] = st
                if prev and m != "eleven_v3": body["previous_text"] = prev  # v3 rejects previous/next_text (400, 2026-11-20)
                if nxt and m != "eleven_v3": body["next_text"] = nxt
                code, data = el_call("POST", f"/text-to-speech/{vid}/with-timestamps", body, timeout=150,
                                     query="?output_format=mp3_44100_128")
                if code == 200:
                    try:
                        js = json.loads(data); open(base + ".mp3", "wb").write(base64.b64decode(js["audio_base64"]))
                        json.dump(js.get("alignment") or js.get("normalized_alignment") or {}, open(base + ".json", "w")); ok = True; break
                    except Exception as e:
                        _EL["why"] = f"tts {m}: bad response {e}"
                else:
                    _EL["why"] = f"tts {m}: http {code} {data[:160]!r}"
                    if code not in (400, 422): break
            if not ok: continue
        outp = os.path.join(workdir, f"buck_{tag}.wav")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", base + ".mp3", "-af", "highpass=f=75,equalizer=f=3000:t=q:w=1.2:g=1.5",
                        "-ar", str(sr), "-ac", "1", outp], check=True)
        y, _ = sf.read(outp, dtype="float32")
        if len(y) < sr * 0.15: _EL["why"] = "tts audio too short"; continue
        words = _words_from_alignment(json.load(open(base + ".json")))
        # trim edge silence, shift word times to match
        pk = float(np.abs(y).max()) or 1.0; thr = pk * 0.02; idx = np.nonzero(np.abs(y) > thr)[0]
        a0 = max(0, int(idx[0]) - int(0.03 * sr)) if len(idx) else 0; a1 = min(len(y), int(idx[-1]) + int(0.08 * sr)) if len(idx) else len(y)
        y = y[a0:a1]; sh = a0 / sr
        words = [(w, max(0.0, t0 - sh), max(0.0, t1 - sh)) for w, t0, t1 in words]
        y, words = _tighten(y, words, sr, float(cfg.get("max_pause", 0)), float(cfg.get("tempo", 1.0)), workdir, tag)
        _EL["used"].append(f"elevenlabs:{cfg.get('label') or _EL.get('name') or BUCK_EL['name']}/{m}")
        return (y / pk * 0.85).astype(np.float32), words
    return None


def _tighten(y, words, sr, max_pause, tempo, workdir, tag):
    """2026-11-20: Buck's designed voices speak slowly (~1.4 words/s) with long gaps. Shorten every inner pause longer
    than max_pause to max_pause, then speed up with ffmpeg atempo (pitch kept; no new TTS credits — the cache is the raw
    take). Word timestamps are remapped so captions stay in sync. Spec "buck_voice": {"tempo": 1.3, "max_pause": 0.38} (both off by default)."""
    import soundfile as sf
    hop = int(0.01 * sr); n = len(y) // hop
    if n > 10 and max_pause > 0:
        e = np.sqrt(np.mean(y[:n * hop].reshape(n, hop) ** 2, axis=1)); quiet = e < e.max() * 0.03
        cuts = []; i = 0  # (start_s, removed_s)
        while i < n:
            if quiet[i]:
                j = i
                while j < n and quiet[j]: j += 1
                ln = (j - i) * hop / sr
                if ln > max_pause and i > 0 and j < n:
                    keep = max_pause / 2; cuts.append((i * hop / sr + keep, ln - max_pause))
                i = j
            else:
                i += 1
        if cuts:
            parts = []; pos = 0
            for c0, cl in cuts:
                parts.append(y[pos:int(c0 * sr)]); pos = int((c0 + cl) * sr)
            parts.append(y[pos:]); y = np.concatenate(parts).astype(np.float32)

            def mp(t):
                d = 0.0
                for c0, cl in cuts:
                    if t > c0: d += min(cl, t - c0)
                return t - d
            words = [(w, mp(a), mp(b)) for w, a, b in words]
    if tempo and abs(tempo - 1.0) > 0.01:
        src = os.path.join(workdir, f"tight_{tag}_in.wav"); dst = os.path.join(workdir, f"tight_{tag}_out.wav")
        sf.write(src, y, sr)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-af", f"atempo={tempo:.4f}", "-ar", str(sr), "-ac", "1", dst], check=True)
        y, _ = sf.read(dst, dtype="float32"); words = [(w, a / tempo, b / tempo) for w, a, b in words]
    return y, words


def buck_line_el(text, workdir, idx, cfg=None, sr=24000):
    """Buck's aside with the ElevenLabs voice -> float32 mono at `sr`, or None (caller falls back to Kokoro)."""
    r = el_speak(text, workdir, f"aside{idx}", cfg, sr=sr)
    return r[0] if r else None


def _buck_line_el_v5(text, workdir, idx, cfg=None, sr=24000):
    """(v5, kept for reference) plain /text-to-speech without timestamps."""
    import hashlib, soundfile as sf
    cfg = cfg or {}
    vid = cfg.get("voice_id") or el_voice_id()
    if not vid: return None
    models = [cfg["model"]] if cfg.get("model") else BUCK_EL["models"]
    settings = dict(BUCK_EL["settings"], **cfg.get("settings", {}))
    txt = text.replace("…", "...").strip()
    os.makedirs(TTS_CACHE, exist_ok=True)
    for m in models:
        h = hashlib.sha1(json.dumps([vid, m, txt, settings], sort_keys=True).encode()).hexdigest()[:16]
        mp3 = os.path.join(TTS_CACHE, f"buck_{h}.mp3")
        if not (os.path.exists(mp3) and os.path.getsize(mp3) > 1000):
            ok = False
            for st in (settings, None):  # retry without voice_settings if the model rejects one of them
                body = {"text": txt, "model_id": m}
                if st: body["voice_settings"] = st
                code, data = el_call("POST", f"/text-to-speech/{vid}", body, out=mp3 + ".part", timeout=120,
                                     query="?output_format=mp3_44100_128")
                if code == 200 and len(data) > 1000:
                    os.replace(mp3 + ".part", mp3); ok = True; break
                if os.path.exists(mp3 + ".part"): os.remove(mp3 + ".part")
                _EL["why"] = f"tts {m}: http {code} {data[:160]!r}"
                if code not in (400, 422): break
            if not ok: continue
        outp = os.path.join(workdir, f"buck_{idx}.wav")
        # clean, bright, broadcast-ready: trim edge silence, small presence lift, mono at the engine rate
        af = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,areverse,"
              "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,"
              "highpass=f=75,equalizer=f=3000:t=q:w=1.2:g=2")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", mp3, "-af", af, "-ar", str(sr), "-ac", "1", outp], check=True)
        y, _ = sf.read(outp, dtype="float32")
        if len(y) < sr * 0.15: _EL["why"] = "tts audio too short"; continue
        pk = np.abs(y).max() or 1.0
        _EL["used"].append(f"elevenlabs:{vid}/{m}")
        return (y / pk * 0.85).astype(np.float32)
    return None


def _f0_stats(path):
    """Rough pitch check of a voice sample (median F0 Hz, spread) via autocorrelation; used to pick Buck's preview."""
    import soundfile as sf
    wav = path + ".16k.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", path, "-ar", "16000", "-ac", "1", wav], check=True)
    y, sr = sf.read(wav, dtype="float32"); os.remove(wav)
    n = int(0.04 * sr); hop = int(0.01 * sr); f0s = []
    thr = 0.1 * np.sqrt(np.mean(y ** 2) + 1e-12) * 3
    for i in range(0, len(y) - n, hop):
        fr = y[i:i + n] - y[i:i + n].mean()
        if np.sqrt(np.mean(fr ** 2)) < thr: continue
        ac = np.correlate(fr, fr, "full")[n - 1:]
        lo, hi = int(sr / 400), int(sr / 70)
        j = lo + int(np.argmax(ac[lo:hi]))
        if ac[j] > 0.45 * ac[0]: f0s.append(sr / j)
    if len(f0s) < 10: return {"f0": 0.0, "spread": 0.0, "voiced": len(f0s)}
    f = np.array(f0s)
    return {"f0": round(float(np.median(f)), 1), "spread": round(float(np.percentile(f, 90) - np.percentile(f, 10)), 1), "voiced": len(f0s)}


def design_buck(outdir, seed=4241, save=True, force=False):
    """ONE-TIME: create Buck's own voice with ElevenLabs Voice Design (prompt BUCK_PROMPT), keep 3 previews as mp3,
    pick the one closest to a bright mid-high young-male register with the most expressive range, save it to the
    account as BUCK_EL["name"]. Idempotent: if a voice with that name exists it is reused (unless force)."""
    import base64, datetime
    os.makedirs(outdir, exist_ok=True)
    res = {"name": BUCK_EL["name"], "prompt": BUCK_PROMPT, "seed": seed}
    if save and not force:
        code, data = el_call("GET", "/voices", timeout=40)
        if code == 200:
            ex = [v for v in json.loads(data).get("voices", []) if v.get("name") == BUCK_EL["name"]]
            if ex:
                res.update(voice_id=ex[0]["voice_id"], existing=True); print(json.dumps(res)); return res
        elif code in (0, 401, 403):
            sys.exit(f"ElevenLabs not reachable/authorised (http {code}). Need ELEVENLABS_API_KEY + access to api.elevenlabs.io")
    data = None
    for model in ("eleven_ttv_v3", "eleven_multilingual_ttv_v2"):
        body = {"voice_description": BUCK_PROMPT, "model_id": model, "text": BUCK_SAMPLE, "seed": int(seed)}
        code, raw = el_call("POST", "/text-to-voice/design", body, timeout=180, query="?output_format=mp3_44100_128")
        if code == 200:
            data = json.loads(raw); res["design_model"] = model; break
        res.setdefault("design_errors", []).append(f"{model}: http {code} {raw[:200]!r}")
    if not data: print(json.dumps(res)); sys.exit("voice design failed")
    prev = []
    for i, p in enumerate(data.get("previews", [])):
        f = os.path.join(outdir, f"buck_preview_{i + 1}.mp3")
        open(f, "wb").write(base64.b64decode(p["audio_base_64"]))
        st = _f0_stats(f)
        # bright mid-high young male ~ 150-175 Hz median; reward expressive range; penalise unusable samples
        score = -abs(st["f0"] - 160) / 25 + min(st["spread"], 120) / 60 - (5 if st["voiced"] < 30 else 0)
        prev.append({"i": i + 1, "file": f, "generated_voice_id": p["generated_voice_id"],
                     "seconds": p.get("duration_secs"), **st, "score": round(score, 2)})
    res["previews"] = prev
    best = max(prev, key=lambda q: q["score"])
    res["chosen"] = best["i"]
    if save:
        body = {"voice_name": BUCK_EL["name"], "voice_description": BUCK_PROMPT, "generated_voice_id": best["generated_voice_id"],
                "labels": {"accent": "american", "gender": "male", "age": "young", "use_case": "characters"},
                "played_not_selected_voice_ids": [q["generated_voice_id"] for q in prev if q is not best]}
        code, raw = el_call("POST", "/text-to-voice", body, timeout=120)
        if code in (400, 422):  # labels format rejected -> save without labels
            body.pop("labels"); code, raw = el_call("POST", "/text-to-voice", body, timeout=120)
        if code != 200: res["save_error"] = f"http {code} {raw[:300]!r}"; print(json.dumps(res)); sys.exit("saving the voice failed")
        res["voice_id"] = json.loads(raw)["voice_id"]
    res["created_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    json.dump(res, open(os.path.join(outdir, "buck_voice.json"), "w"), indent=2)
    print(json.dumps(res)); return res


# FALLBACK: Kokoro am_puck (Apache-2.0 model), pitched up ~2.5 semitones, brighter EQ + tiny slap-back.
BUCK_VOICE = {"voice": "am_puck", "speed": 1.12, "pitch": 1.16}


def buck_line(k, text, workdir, idx, cfg=None):
    import soundfile as sf
    if (cfg or {}).get("engine", "auto") != "kokoro":
        y = buck_line_el(text, workdir, idx, cfg)
        if y is not None: return y, 24000
    _EL["used"].append("kokoro:am_puck" + (f" ({_EL['why']})" if _EL["why"] else ""))
    cfg = dict(BUCK_VOICE, **{k_: v_ for k_, v_ in (cfg or {}).items() if k_ in BUCK_VOICE})
    s, sr = k.create(say_text(text), voice=cfg["voice"], speed=cfg["speed"], lang="en-us")
    raw = os.path.join(workdir, f"buck_{idx}_raw.wav"); outp = os.path.join(workdir, f"buck_{idx}.wav")
    sf.write(raw, s, sr)
    p = cfg["pitch"]
    af = (f"asetrate={sr}*{p},aresample={sr},atempo={1 / p:.4f},equalizer=f=3200:t=q:w=1.4:g=4,"
          f"equalizer=f=180:t=q:w=1:g=-2,aecho=0.8:0.5:28:0.10")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-af", af, "-ar", str(sr), "-ac", "1", outp], check=True)
    y, _ = sf.read(outp, dtype="float32")
    pk = np.abs(y).max() or 1.0
    return (y / pk * 0.85).astype(np.float32), sr


def tts(spec, args, workdir):
    from kokoro_onnx import Kokoro
    import soundfile as sf
    k = Kokoro(args.model, args.voices)
    voice = spec.get("voice", "am_michael"); speed = spec.get("speed", 1.05)
    gap = 0.1; t = 0.0; chunks = []; sr = 24000
    narr = spec.get("narrator", "buck")  # v6: Buck narrates everything
    bcfg = spec.get("buck_voice") or {}
    lines = [say_text(x.get("say", x.get("text", ""))).strip() for x in spec["scenes"]]
    if lines and spec.get("loop") and re.search(r"\.\.\.$", lines[-1]):  # v6.10: a trailing "..." on the loop line makes
        lines[-1] = re.sub(r"\s*\.\.\.$", "", lines[-1])          # multilingual_v2 stretch into "aaamm" (airport b4, pink 1st take)
    pre = {}
    if spec.get("lang") == "uz" and bcfg.get("one_take", True) and bcfg.get("engine", "auto") != "kokoro":
        # 2026-11-20 (Shohjahon): Uzbek lines read one by one (v3 has no previous/next context) sounded worse than
        # the whole text in one take. Read the full script ONCE, then cut it into scenes at word boundaries.
        lw_all = [[w for w in l.split() if "[" not in w and "]" not in w] for l in lines]
        full = " ".join((l if bcfg.get("script") == "lat" else uz_voice_text(l, spec.get("uz_lex"))) for l in lines if l)  # "script": "lat" = read Latin as is
        R = el_speak(full, workdir, "full", bcfg)
        if R is not None:
            y_all, ws = R; ws = [w for w in ws if "[" not in w[0] and "]" not in w[0]]
            if len(ws) == sum(len(x) for x in lw_all):
                k = 0; spans = []
                for x in lw_all: spans.append((k, k + len(x))); k += len(x)
                sr_ = 24000; bounds = []
                for i, (a, b) in enumerate(spans):
                    if a == b: bounds.append(None); continue
                    t0 = 0.0 if a == 0 else (ws[a - 1][2] + ws[a][1]) / 2
                    t1 = len(y_all) / sr_ if b == len(ws) else (ws[b - 1][2] + ws[b][1]) / 2
                    seg = y_all[int(t0 * sr_):int(t1 * sr_)]
                    pre[i] = (seg, [(l, ws[a + j][1] - t0, ws[a + j][2] - t0) for j, l in enumerate(lw_all[i])])
            else:
                print(f"one_take: word count mismatch ({len(ws)} vs {sum(len(x) for x in lw_all)}) -> per-line TTS", file=sys.stderr)
    for i, sc in enumerate(spec["scenes"]):
        txt = lines[i]; words = None
        if txt:
            r = None
            if narr == "buck" and bcfg.get("engine", "auto") != "kokoro":
                if i in pre:
                    r = pre[i]
                elif spec.get("lang") == "uz":  # voice reads Cyrillic (correct g'/x), word times mapped back to Latin
                    r = el_speak(uz_voice_text(txt, spec.get("uz_lex")), workdir, f"n{i}", bcfg)
                    if r is not None:  # drop v3 audio tags from the word list, then map back to the Latin words
                        sw = [w for w in r[1] if "[" not in w[0] and "]" not in w[0]]
                        lw_ = [w for w in txt.split() if "[" not in w and "]" not in w]
                        r = (r[0], [(l, a, b) for l, (_, a, b) in zip(lw_, sw)] if len(sw) == len(lw_) else sw)
                else:
                    r = el_speak(txt, workdir, f"n{i}", bcfg, prev=(lines[i - 1] or None) if i > 0 else None,
                                 nxt=(lines[i + 1] or None) if i + 1 < len(lines) else None)
            if r is not None:
                s, words = r; sr = 24000
            elif narr == "buck":  # emergency fallback: Buck's old Kokoro voice (do not publish such a render)
                s, sr = buck_line(k, txt, workdir, f"n{i}", dict(bcfg, engine="kokoro"))
            else:
                s, sr = k.create(txt, voice=voice, speed=speed, lang="en-us")
        else:
            s = np.zeros(0, dtype=np.float32)
        sc["words"] = words
        dur = len(s) / sr
        beat = float(sc.get("beat", 0))  # comedic pause before the line
        bk = np.zeros(0, dtype=np.float32)
        if sc.get("buck"):  # Buck speaks his own line (before the narrator unless "buck_after")
            bk, _ = buck_line(k, sc["buck"], workdir, i, bcfg)
        bgap = np.zeros(int(0.15 * sr), dtype=np.float32) if (len(bk) and len(s)) else np.zeros(0, dtype=np.float32)
        sc["start"] = t
        seq = [np.zeros(int(beat * sr), dtype=np.float32)]
        if sc.get("buck_after"):
            sc["speech"] = t + beat; sc["buck_t"] = t + beat + dur + len(bgap) / sr
            seq += [s.astype(np.float32), bgap, bk]
        else:
            sc["buck_t"] = t + beat; sc["speech"] = t + beat + (len(bk) + len(bgap)) / sr
            seq += [bk, bgap, s.astype(np.float32)]
        if sc.get("words"): sc["words"] = [(w, sc["speech"] + a, sc["speech"] + b) for w, a, b in sc["words"]]
        seq.append(np.zeros(int((gap + float(sc.get("land", 0))) * sr), dtype=np.float32))  # v6.7 "land": let a punchline land
        seg = np.concatenate(seq); chunks.append(seg)
        sc["sdur"] = dur; sc["dur"] = len(seg) / sr
        t += sc["dur"]
    audio = np.concatenate(chunks).astype(np.float32)
    # speech envelope at video fps (drives Buck's talking bounce)
    hop = int(sr / FPS); nfr = len(audio) // hop + 1
    envf = np.array([np.sqrt(np.mean(audio[j * hop:(j + 1) * hop] ** 2)) if j * hop < len(audio) else 0.0 for j in range(nfr)], np.float32)
    spec["_speech_env"] = (envf / (np.percentile(envf, 95) + 1e-6)).clip(0, 1.2).tolist()
    spec["_speech_words"] = [w for sc in spec["scenes"] for w in (sc.get("words") or [])]
    spec["_mouth_cues"] = rhubarb_cues(audio, sr, spec, workdir)  # v6.8: phoneme lip-sync (None -> envelope fallback)
    audio = mix_sfx(audio, sr, spec)
    wav = os.path.join(workdir, "voice.wav"); sf.write(wav, audio, sr)
    return wav, t


# ---------------- Sound effects (all synthesized here: no licensing issues) ----------------
def _env(n, attack, release, sr):
    e = np.ones(n, dtype=np.float32)
    a = max(1, int(attack * sr)); r = max(1, int(release * sr))
    e[:a] = np.linspace(0, 1, a); e[-r:] *= np.linspace(1, 0, r)
    return e


def _bandnoise(n, sr, lo, hi, rng):
    x = rng.standard_normal(n).astype(np.float32)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1 / sr)
    X[(f < lo) | (f > hi)] = 0
    y = np.fft.irfft(X, n).astype(np.float32)
    return y / (np.abs(y).max() + 1e-9)


def sfx_whoosh(sr, rng, dur=0.45):
    n = int(dur * sr); parts = []
    seg = n // 6
    for i in range(6):  # rising band sweep
        lo = 300 + i * 500; parts.append(_bandnoise(seg, sr, lo, lo + 1500, rng))
    y = np.concatenate(parts)[:n]
    y = np.pad(y, (0, n - len(y)))
    env = np.sin(np.linspace(0, np.pi, n)) ** 2
    return (y * env).astype(np.float32)


def sfx_pop(sr, rng, dur=0.16):
    t = np.arange(int(dur * sr)) / sr
    f = 520 * np.exp(-t * 14) + 140
    y = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t * 22)
    return y.astype(np.float32)


def sfx_impact(sr, rng, dur=0.7):
    n = int(dur * sr); t = np.arange(n) / sr
    low = np.sin(2 * np.pi * 55 * t) * np.exp(-t * 6)
    hit = _bandnoise(n, sr, 80, 2500, rng) * np.exp(-t * 30)
    return (0.8 * low + 0.5 * hit).astype(np.float32)


def sfx_coin(sr, rng, dur=0.9):
    n = int(dur * sr); t = np.arange(n) / sr; y = np.zeros(n, np.float32)
    for delay in (0.0, 0.11):  # two hits = "ka-ching"
        d = int(delay * sr); tt = t[: n - d]
        tone = sum(a * np.sin(2 * np.pi * fr * tt) * np.exp(-tt * k)
                   for fr, a, k in ((2093, 1.0, 7), (3136, .6, 9), (4186, .45, 11), (5274, .3, 14)))
        y[d:] += tone.astype(np.float32)
    return y / (np.abs(y).max() + 1e-9)


def sfx_cash(sr, rng, dur=1.0):
    n = int(dur * sr); t = np.arange(n) / sr
    mech = _bandnoise(n, sr, 1500, 6000, rng) * np.exp(-t * 25)
    bell = sfx_coin(sr, rng, dur)
    return (0.4 * mech + 0.8 * bell).astype(np.float32)


def sfx_tick(sr, rng, dur):
    n = int(dur * sr); y = np.zeros(n, np.float32)
    click = _bandnoise(int(0.012 * sr), sr, 2000, 7000, rng) * np.linspace(1, 0, int(0.012 * sr))
    k = 0
    for s in np.arange(0, dur, 0.5):
        i = int(s * sr); amp = 1.0 if k % 2 == 0 else 0.7
        y[i:i + len(click)] += (click * amp)[: max(0, min(len(click), n - i))]; k += 1
    return y


def sfx_birds(sr, rng, dur):
    """Soft synthesized bird chirps over a light breeze."""
    n = int(dur * sr); y = np.zeros(n, np.float32)
    wind = _bandnoise(n, sr, 150, 900, rng) * 0.08
    y += wind.astype(np.float32)
    t0 = rng.uniform(0.1, 0.6)
    while t0 < dur - 0.3:
        kind = rng.integers(0, 3); base = rng.uniform(2600, 4200)
        notes = rng.integers(2, 5)
        for j in range(notes):
            cd = rng.uniform(0.05, 0.11); m = int(cd * sr); tt = np.arange(m) / sr
            if kind == 0: f = base + 1400 * tt / cd                  # rising chirp
            elif kind == 1: f = base + 900 * np.sin(np.pi * tt / cd)  # arched chirp
            else: f = base - 1200 * tt / cd                          # falling chirp
            ch = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.sin(np.pi * tt / cd) ** 2
            i = int((t0 + j * (cd + 0.03)) * sr)
            if i + m < n: y[i:i + m] += (0.35 * ch).astype(np.float32)
        t0 += rng.uniform(0.6, 2.2)
    return y


def sfx_scratch(sr, rng, dur=0.55):
    """Record scratch: two fast back-and-forth strokes (buzzy saw + noise, pitch swinging)."""
    n = int(dur * sr); t = np.arange(n) / sr
    f = 260 + 1100 * np.abs(np.sin(2 * np.pi * t / 0.26))
    ph = np.cumsum(f) / sr
    saw = 2 * (ph % 1.0) - 1
    nz = _bandnoise(n, sr, 600, 5000, rng)
    env = np.abs(np.sin(np.pi * t / 0.26)) ** 0.5 * np.exp(-t * 1.5)
    return ((0.55 * saw + 0.6 * nz) * env).astype(np.float32)


def sfx_boing(sr, rng, dur=0.75):
    t = np.arange(int(dur * sr)) / sr
    f = 170 + 140 * t / dur + 90 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 2.5)
    return (np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t * 3.2) * np.clip(t / 0.01, 0, 1)).astype(np.float32)


def _slide(sr, f0, f1, dur):
    t = np.arange(int(dur * sr)) / sr
    f = f0 * (f1 / f0) ** (t / dur) * (1 + 0.012 * np.sin(2 * np.pi * 6 * t))
    y = np.sin(2 * np.pi * np.cumsum(f) / sr) + 0.25 * np.sin(4 * np.pi * np.cumsum(f) / sr)
    return (y * np.sin(np.pi * t / dur) ** 0.6 * 0.8).astype(np.float32)


def sfx_slide_up(sr, rng): return _slide(sr, 380, 1500, 0.45)
def sfx_slide_down(sr, rng): return _slide(sr, 1400, 260, 0.6)


def sfx_bonk(sr, rng, dur=0.35):
    n = int(dur * sr); t = np.arange(n) / sr
    wood = (np.sin(2 * np.pi * 720 * t) + 0.6 * np.sin(2 * np.pi * 1130 * t)) * np.exp(-t * 28)
    thud = np.sin(2 * np.pi * 140 * t) * np.exp(-t * 18)
    click = _bandnoise(n, sr, 1500, 6000, rng) * np.exp(-t * 90)
    return (0.6 * wood + 0.7 * thud + 0.3 * click).astype(np.float32)


def sfx_ding(sr, rng, dur=1.3):
    t = np.arange(int(dur * sr)) / sr
    y = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, a, k in ((1568, 1.0, 3.2), (3136, .35, 5), (4704, .18, 7)))
    return (y / 1.5).astype(np.float32)


def sfx_buzzer(sr, rng, dur=0.6):
    t = np.arange(int(dur * sr)) / sr
    y = np.sign(np.sin(2 * np.pi * 110 * t)) * 0.5 + np.sign(np.sin(2 * np.pi * 165 * t)) * 0.3
    return (y * _env(len(t), 0.01, 0.08, sr) * 0.7).astype(np.float32)


def sfx_crickets(sr, rng, dur=1.6):
    """Awkward-silence crickets (pulsed 4.6 kHz chirps)."""
    n = int(dur * sr); t = np.arange(n) / sr; y = np.zeros(n, np.float32)
    car = np.sin(2 * np.pi * 4600 * t)
    for s in np.arange(0.05, dur - 0.2, 0.55):
        for j in range(3):
            i = int((s + j * 0.045) * sr); m = int(0.03 * sr)
            if i + m < n: y[i:i + m] += (car[i:i + m] * np.sin(np.pi * np.arange(m) / m)).astype(np.float32)
    return y * 0.6


def sfx_drumroll(sr, rng, dur=1.4):
    n = int(dur * sr); y = np.zeros(n, np.float32)
    hit = _bandnoise(int(0.05 * sr), sr, 200, 6000, rng) * np.exp(-np.arange(int(0.05 * sr)) / sr * 60)
    for s in np.arange(0, dur - 0.25, 0.045):
        i = int(s * sr); amp = 0.25 + 0.6 * s / dur
        y[i:i + len(hit)] += (hit * amp)[: max(0, min(len(hit), n - i))]
    end = sfx_impact(sr, rng, 0.25); i = n - len(end); y[i:] += end * 0.8
    return y


def sfx_wahwah(sr, rng):
    """'Sad trombone' style 4-note fail stinger (synthesized brass). Use at most once per video."""
    notes = [(293.7, 0.32), (277.2, 0.32), (261.6, 0.32), (246.9, 0.95)]; out = []
    for i, (f, d) in enumerate(notes):
        t = np.arange(int(d * sr)) / sr
        vib = 1 + (0.025 * np.sin(2 * np.pi * 5.5 * t) * np.clip((t - 0.15) / 0.2, 0, 1) if i == 3 else 0)
        ph = 2 * np.pi * np.cumsum(f * vib) / sr
        wah = 0.5 + 0.5 * np.clip(t / 0.08, 0, 1) * (0.6 + 0.4 * np.sin(np.pi * t / d))
        y = sum((wah ** (h * 0.5)) * np.sin(h * ph) / h for h in range(1, 9))
        out.append((y * _env(len(t), 0.02, 0.06, sr) * 0.55).astype(np.float32))
    return np.concatenate(out)


def sfx_whip(sr, rng, dur=0.22):
    """v4.1 crash-zoom 'whip': very short rising swish (band-noise sweep, peaks at 2/3, cuts fast)."""
    n = int(dur * sr); t = np.arange(n) / sr; seg = n // 5 + 1
    y = np.concatenate([_bandnoise(seg, sr, 900 + 800 * i, 2800 + 1300 * i, rng) for i in range(5)])[:n]
    env = (t / dur) ** 2 * (1 - t / dur) * 6.75
    return (y * env).astype(np.float32)


def sfx_riser(sr, rng, dur=0.45):
    """v6: short tension riser (band-noise sweep + rising tone) that lands on a stat."""
    n = int(dur * sr); t = np.arange(n) / sr; seg = n // 6 + 1
    nz = np.concatenate([_bandnoise(seg, sr, 400 + i * 700, 1500 + i * 1100, rng) for i in range(6)])[:n]
    f = 300 * (5 ** (t / dur)); tone = np.sin(2 * np.pi * np.cumsum(f) / sr) * 0.25
    return ((0.8 * nz + tone) * (t / dur) ** 2.2).astype(np.float32)


def sfx_subboom(sr, rng, dur=0.7):
    """v6: cinematic sub drop (felt more than heard) under a big number."""
    t = np.arange(int(dur * sr)) / sr; f = 32 + 30 * np.exp(-t * 9)
    return (np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t * 4.5) * np.clip(t / 0.004, 0, 1)).astype(np.float32)


def sfx_shimmer(sr, rng, dur=0.6):
    """v6: sparkle for flash cuts / light leaks."""
    n = int(dur * sr); y = np.zeros(n, np.float32)
    for k in range(9):
        f0 = rng.uniform(2500, 6000); d = int(0.12 * sr); i = int(rng.uniform(0, dur - 0.13) * sr); tt = np.arange(d) / sr
        y[i:i + d] += (np.sin(2 * np.pi * f0 * tt) * np.exp(-tt * 28) * 0.5).astype(np.float32)
    return y


def _pink(n, rng):
    w = rng.standard_normal(n).astype(np.float32); X = np.fft.rfft(w); f = np.arange(len(X), dtype=np.float32); f[0] = 1
    y = np.fft.irfft(X / np.sqrt(f), n).astype(np.float32)
    return y / (np.abs(y).max() + 1e-9)


def _reverb(L, R, sr, wet=0.16, dur=0.55):
    """Short stereo room (decorrelated decaying-noise impulse responses, FFT convolution)."""
    rng = np.random.default_rng(5); n = int(dur * sr); t = np.arange(n) / sr; out = []
    for ch in (L, R):
        ir = rng.standard_normal(n).astype(np.float32) * np.exp(-t * 7.5).astype(np.float32); ir[:int(0.012 * sr)] = 0
        ir /= np.sqrt(np.sum(ir ** 2)) + 1e-9
        N = 1 << (len(ch) + n - 1).bit_length()
        y = np.fft.irfft(np.fft.rfft(ch, N) * np.fft.rfft(ir, N), N)[:len(ch)]
        out.append((ch + wet * y).astype(np.float32))
    return out


def _envelope(x, sr):
    win = max(1, int(0.03 * sr)); e = np.sqrt(np.convolve(x.astype(np.float32) ** 2, np.ones(win, np.float32) / win, "same"))
    k = max(1, int(0.25 * sr)); return np.maximum(e, np.convolve(e, np.ones(k, np.float32) / k, "same"))


SFX = {"whoosh": sfx_whoosh, "pop": sfx_pop, "impact": sfx_impact, "coin": sfx_coin, "cash": sfx_cash,
       "scratch": sfx_scratch, "boing": sfx_boing, "slide_up": sfx_slide_up, "slide_down": sfx_slide_down,
       "bonk": sfx_bonk, "ding": sfx_ding, "buzzer": sfx_buzzer, "crickets": sfx_crickets, "drumroll": sfx_drumroll,
       "wahwah": sfx_wahwah, "whip": sfx_whip, "riser": sfx_riser, "subboom": sfx_subboom, "shimmer": sfx_shimmer}
# (offset seconds after scene start, gain) — effects sit under the voice
SFX_MIX = {"coin": (0.2, 0.22), "cash": (0.2, 0.24), "impact": (0.2, 0.35), "scratch": (0.0, 0.30), "boing": (0.1, 0.30),
           "slide_up": (0.05, 0.20), "slide_down": (0.05, 0.22), "bonk": (0.1, 0.40), "ding": (0.15, 0.22),
           "buzzer": (0.1, 0.16), "crickets": (0.05, 0.16), "drumroll": (0.0, 0.26), "wahwah": (0.1, 0.24),
           "whip": (0.0, 0.20), "riser": (0.0, 0.13), "subboom": (0.0, 0.30), "shimmer": (0.0, 0.10)}
try:  # v6.8: optional 8-bit palette (pyfxr) - fxr_pickup / fxr_powerup / fxr_hurt / fxr_select / fxr_jump
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sfx_fxr as _fxr
    if _fxr.available():
        for _n in _fxr.PRESETS:
            SFX[_n] = (lambda n: (lambda sr, rng: _fxr.render(n, sr)))(_n)
            SFX_MIX[_n] = (0.05, 0.16)
except Exception:
    pass
SFX_PAN = {"coin": 0.25, "cash": 0.2, "boing": -0.25, "bonk": -0.2, "crickets": 0.35, "slide_up": -0.15, "slide_down": 0.15}


def _add(track, clip, at, sr, gain):
    i = int(at * sr)
    if i >= len(track): return
    m = min(len(clip), len(track) - i)
    track[i:i + m] += clip[:m] * gain


def mix_sfx(voice, sr, spec):
    """v6 STEREO mix: voice in the centre, effects panned and layered under it. Spec: "sfx": true/false (auto layer),
    scene "sfx": [...names, "name@sec"], "ambient": "birds". Returns float32 array (n, 2)."""
    rng = np.random.default_rng(11)
    n = len(voice); L = np.zeros(n, np.float32); R = np.zeros(n, np.float32)
    cinema = spec.get("cinema", True)

    def add(clip, at, gain, pan=0.0):  # equal-power pan, centre = gain on both sides
        a = (max(-1.0, min(1.0, pan)) + 1) * math.pi / 4
        _add(L, clip, at, sr, gain * math.cos(a) * 1.4142); _add(R, clip, at, sr, gain * math.sin(a) * 1.4142)
    auto = spec.get("sfx", True)
    for i, sc in enumerate(spec["scenes"]):
        st = sc["start"]
        tr = sc.get("transition") or ("punch" if sc.get("stat") else ["punch", "flash", "slide"][i % 3])
        if auto and i > 0:
            w = sfx_whoosh(sr, rng)
            if cinema and tr == "slide":  # the whoosh travels with the slide
                h = len(w) // 2; add(w[:h], max(0, st - 0.2), 0.16, 0.6); add(w[h:], max(0, st - 0.2) + h / sr, 0.16, -0.6)
            else: add(w, max(0, st - 0.2), 0.16)
            if cinema and tr == "flash": add(sfx_shimmer(sr, rng), st, SFX_MIX["shimmer"][1])
        if auto and sc.get("stat"):
            add(sfx_pop(sr, rng), st + 0.2, 0.28)
            if cinema:
                add(sfx_riser(sr, rng), max(0.0, st + 0.2 - 0.45), SFX_MIX["riser"][1])
                add(sfx_subboom(sr, rng), st + 0.2, SFX_MIX["subboom"][1])
        for name in sc.get("sfx", []):
            at_ = None
            if "@" in name: name, at_ = name.split("@", 1); at_ = float(at_)  # "ding@5.0" = 5 s after scene start
            pan = SFX_PAN.get(name, 0.0)
            if at_ is not None and name in SFX:
                add(SFX[name](sr, rng), st + at_, SFX_MIX.get(name, (0.0, 0.2))[1], pan); continue
            if name == "tick": add(sfx_tick(sr, rng, sc["dur"]), st, 0.22)
            elif name == "birds":
                add(sfx_birds(sr, rng, sc["dur"]), st, 0.1, -0.6); add(sfx_birds(sr, rng, sc["dur"]), st, 0.1, 0.6)
            elif name in SFX:
                off, g = SFX_MIX.get(name, (0.0, 0.2))
                add(SFX[name](sr, rng), st + off, g, pan)
        if auto and sc.get("mascot"):
            m_ = sc["mascot"]; pos = m_.get("pos") or ("corner" if (sc.get("stat") or sc.get("chart") or sc.get("vs") or sc.get("broll")) else "center")
            add(sfx_pop(sr, rng), st + float(m_.get("at", 0)) + 0.05, 0.18, -0.55 if pos == "corner" else 0.0)
        if auto and sc.get("vs"):  # v4.1: pop as each panel lands (left / right), light impact when the VS badge slams in
            vat = _vs_at(sc["vs"])
            for a_, p_ in zip(vat, (-0.5, 0.5)): add(sfx_pop(sr, rng), st + a_ + 0.3, 0.26, p_)
            add(sfx_impact(sr, rng, 0.45), st + float(sc["vs"].get("vs_at", (vat[0] + vat[1]) / 2 + 0.1)), 0.2)
        if auto and sc.get("zoom"): add(sfx_whip(sr, rng), st + float(sc["zoom"].get("at", 0)), SFX_MIX["whip"][1])
        if cinema and auto and "coin_rain" in sc.get("fx", []):  # coins landing all around the stereo field
            for _ in range(10):
                add(sfx_coin(sr, rng, 0.5), st + rng.uniform(0.15, max(0.3, min(2.6, sc["dur"] - 0.3))), 0.045, rng.uniform(-0.9, 0.9))
    if spec.get("ambient") == "birds":
        v_ = float(spec.get("ambient_vol", 0.08))
        add(sfx_birds(sr, np.random.default_rng(31), n / sr), 0, v_, -0.7); add(sfx_birds(sr, np.random.default_rng(32), n / sr), 0, v_, 0.7)
    if cinema:
        L += _pink(n, np.random.default_rng(21)) * 0.0035; R += _pink(n, np.random.default_rng(22)) * 0.0035  # room tone
        L, R = _reverb(L, R, sr)
        env = _envelope(voice, sr); g = (1.0 - 0.45 * np.clip(env / (env.max() + 1e-9) * 2.5, 0, 1)).astype(np.float32)
        L *= g; R *= g  # effects duck under the voice
    out = np.stack([voice + L, voice + R], axis=1)
    peak = np.abs(out).max()
    return (out / peak * 0.95).astype(np.float32) if peak > 0.98 else out.astype(np.float32)


def wrap(draw, text, font, maxw):
    words = text.split(); lines = []; cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=font) <= maxw: cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines


def caption_chunks(text, start, dur):
    words = text.split(); chunks = []; cur = []
    for w in words:
        cur.append(w)
        if len(cur) >= 4 or (re.search(r'[.,:?!;]$', w) and len(cur) >= 2):
            chunks.append(cur); cur = []
    if cur:
        if chunks and len(cur) < 2: chunks[-1] += cur
        else: chunks.append(cur)
    total = sum(len(' '.join(c)) for c in chunks) or 1
    out = []; t = start
    for c in chunks:
        s = ' '.join(c); d = dur * len(s) / total
        out.append((t, t + d, s.upper())); t += d
    return out


def caption_chunks_timed(text, words):
    """v6: caption chunks timed by Buck's real word timings (ElevenLabs alignment). The on-screen words ("text") are
    mapped onto the spoken words ("say") by position, so spelled-out numbers still line up."""
    tw = text.split()
    if not tw or not words: return []
    n_s = len(words); st = []; p = 0
    norm = lambda w: re.sub(r"[^a-z0-9']", "", w.lower())
    sw = [norm(w[0]) for w in words]
    for j in range(len(tw)):  # greedy: exact word match in a small window, else the next spoken word
        q = next((q for q in range(p, min(n_s, p + 8)) if sw[q] and sw[q] == norm(tw[j])), None)
        if q is None: q = min(p, n_s - 1)
        st.append(words[q][1]); p = min(q + 1, n_s - 1) if q >= p else p
    end_all = words[-1][2]
    chunks = []; cur = []
    for j, w in enumerate(tw):
        cur.append(j)
        if len(cur) >= 4 or (re.search(r'[.,:?!;]$', w) and len(cur) >= 2): chunks.append(cur); cur = []
    if cur:
        if chunks and len(cur) < 2: chunks[-1] += cur
        else: chunks.append(cur)
    out = []
    for ci, c in enumerate(chunks):
        t0 = st[c[0]]; t1 = st[chunks[ci + 1][0]] if ci + 1 < len(chunks) else end_all + 0.25
        out.append((t0, max(t1, t0 + 0.2), ' '.join(tw[j] for j in c).upper(), [st[j] for j in c]))
    return out


ENGINE_VERSION = "6.12"  # bump on every engine change and add a line to docs/changes.md

THEMES = {  # v6.1: per-video look so videos don't all share one background. Spec "theme": name | "auto" (default: from the first line).
    "vault": ([((9, 14, 28), (19, 30, 54)), ((12, 10, 30), (32, 20, 58)), ((6, 20, 24), (14, 42, 48))], "grid"),
    "mint":  ([((5, 24, 18), (10, 52, 38)), ((8, 30, 30), (16, 58, 44)), ((4, 18, 22), (12, 44, 30))], "stripes"),
    "ember": ([((30, 10, 12), (62, 22, 18)), ((26, 12, 22), (58, 26, 14)), ((20, 8, 16), (50, 18, 26))], "glow"),
    "royal": ([((16, 8, 36), (44, 18, 78)), ((10, 10, 40), (30, 26, 86)), ((22, 8, 30), (56, 16, 66))], "dots"),
    "ocean": ([((4, 18, 34), (8, 46, 72)), ((6, 24, 40), (10, 58, 70)), ((4, 14, 30), (14, 40, 82))], "waves"),
    "noir":  ([((10, 10, 12), (30, 30, 34)), ((14, 12, 10), (38, 34, 28)), ((8, 10, 14), (26, 30, 38))], "rings"),
}


def pick_theme(spec):
    t = spec.get("theme")
    if t in THEMES: return t
    key = (spec.get("scenes") or [{}])[0].get("text", "") + spec.get("source", "")
    return sorted(THEMES)[sum(ord(c) for c in key) % len(THEMES)]


def make_bg(W, H, seed, theme="vault"):
    """Static branded background layer (dark gradient + faint pattern, per theme). Motion is added per frame."""
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    palettes, pat = THEMES.get(theme, THEMES["vault"])
    c1, c2 = palettes[seed % len(palettes)]
    for y in range(H):
        f = y / (H - 1); d.line([(0, y), (W, y)], fill=tuple(int(c1[i] + (c2[i] - c1[i]) * f) for i in range(3)))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); o = ImageDraw.Draw(ov)
    step = 90; A = (255, 255, 255, 11)
    if pat == "grid":
        for x in range(0, W, step): o.line([(x, 0), (x, H)], fill=A)
        for y in range(0, H, step): o.line([(0, y), (W, y)], fill=A)
    elif pat == "stripes":
        for x in range(-H, W, 70): o.line([(x, H), (x + H, 0)], fill=(255, 255, 255, 9), width=3)
    elif pat == "dots":
        for yi, y in enumerate(range(30, H, 64)):
            for x in range(30 + (32 if yi % 2 else 0), W, 64): o.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(255, 255, 255, 16))
    elif pat == "waves":
        for y0 in range(60, H, 110):
            o.line([(x, y0 + 22 * math.sin(x / 95.0 + y0 * 0.013)) for x in range(0, W + 20, 20)], fill=(255, 255, 255, 13), width=3)
    elif pat == "rings":
        cx, cy = W * (0.2 + 0.3 * (seed % 3)), H * 0.38
        for r in range(120, int(max(W, H) * 1.2), 120): o.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255, 12), width=2)
    elif pat == "glow":
        g = Image.new("L", (W // 8, H // 8), 0); gd = ImageDraw.Draw(g)
        cx, cy = (W // 8) * (0.3 + 0.2 * (seed % 3)), (H // 8) * 0.35; r = max(W, H) // 8 * 0.36
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=44)
        g = g.filter(ImageFilter.GaussianBlur(r * 0.5)).resize((W, H), Image.BILINEAR)
        ov = Image.merge("RGBA", (Image.new("L", (W, H), 255), Image.new("L", (W, H), 170), Image.new("L", (W, H), 110), g))
    return Image.alpha_composite(im.convert("RGBA"), ov)


def broll_frames(path, W, H, n, start=0.0):
    # decode slightly larger than the frame so a slow Ken Burns zoom never shows edges
    BW, BH = int(W * 1.1) // 2 * 2, int(H * 1.1) // 2 * 2
    cmd = ["ffmpeg", "-loglevel", "error", "-ss", f"{start}", "-i", path, "-vf",
           f"scale={BW}:{BH}:force_original_aspect_ratio=increase,crop={BW}:{BH},fps={FPS}",
           "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.run(cmd, capture_output=True)
    raw = p.stdout; fs = BW * BH * 3
    return [raw[i:i + fs] for i in range(0, len(raw) - fs + 1, fs)], (BW, BH)


def backdrop_frames(path, W, H, n, start=0.0, blur=6):
    """v6.6 cinematic BACKDROP (Shohjahon 2026-11-21: "oddiy fon emas, har xil yaxshi fonlar"): a real clip or photo
    behind the graphics of non-b-roll scenes — decoded small, blurred (shallow depth of field), slow drift.
    Returns small RGB frames; the caller upscales, tints toward the theme and darkens so text/Buck stay readable."""
    bw, bh = int(W * 0.30) // 2 * 2, int(H * 0.30) // 2 * 2
    img = path.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    pre = ["-loop", "1"] if img else ["-stream_loop", "-1", "-ss", f"{start}"]
    vf = (f"scale={int(bw * 1.12) // 2 * 2}:{int(bh * 1.12) // 2 * 2}:force_original_aspect_ratio=increase,"
          f"crop={int(bw * 1.12) // 2 * 2}:{int(bh * 1.12) // 2 * 2},gblur=sigma={blur},fps={FPS}")
    cmd = ["ffmpeg", "-loglevel", "error"] + pre + ["-i", path, "-vf", vf, "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    BW, BH = int(bw * 1.12) // 2 * 2, int(bh * 1.12) // 2 * 2; fs = BW * BH * 3
    return [raw[i:i + fs] for i in range(0, len(raw) - fs + 1, fs)], (BW, BH)


def ease_out(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3


def ease_back(x, s=1.9):
    """Overshoot ease: goes a bit past 1, then settles (the 'punch' feel)."""
    x = max(0.0, min(1.0, x)); x -= 1
    return x * x * ((s + 1) * x + s) + 1


def zoom_amt(zt, amt, hold):
    """v4.1 crash-zoom envelope: snap in 0.14 s (overshoot), hold, ease out 0.2 s. hold < 0 = stay zoomed."""
    if zt < 0: return 1.0
    if zt < 0.14: return 1 + (amt - 1) * ease_back(zt / 0.14, 1.4)
    if hold < 0 or zt < 0.14 + hold: return amt
    r = (zt - 0.14 - hold) / 0.2
    return 1 + (amt - 1) * (1 - ease_out(r)) if r < 1 else 1.0


NUM_RE = re.compile(r'^(\D*?)(\d[\d,]*(?:\.\d+)?)(\D*)$')


def count_text(stat, p):
    """Count-up animation for stats like $85M, 3.69¢, 250B, 232 YRS. Non-numeric stats are returned as is."""
    m = NUM_RE.match(stat)
    if not m: return stat
    pre, num, suf = m.groups()
    dec = len(num.split('.')[1]) if '.' in num else 0
    val = float(num.replace(',', '')) * p
    s = f"{val:,.{dec}f}" if ',' in num else f"{val:.{dec}f}"
    return pre + s + suf


def draw_coin(d, cx, cy, r, squash, alpha):
    """Simple gold coin with a $; squash < 1 fakes a 3D spin."""
    rx = max(2, r * abs(squash))
    d.ellipse([cx - rx, cy - r, cx + rx, cy + r], fill=(214, 160, 30, alpha), outline=(255, 214, 90, alpha), width=max(2, int(r * 0.12)))
    if abs(squash) > 0.45:
        f = ImageFont.truetype(ANTON, max(8, int(r * 1.1)))
        tw = d.textlength("$", font=f)
        d.text((cx - tw / 2, cy - r * 0.72), "$", font=f, fill=(120, 80, 0, alpha))


def karaoke_lines(d, words, font, maxw):
    lines = []; cur = []; w = 0; sp = d.textlength(" ", font=font)
    for i, wd in enumerate(words):
        ww = d.textlength(wd, font=font)
        if cur and w + sp + ww > maxw:
            lines.append(cur); cur = []; w = 0
        cur.append(i); w += (sp if len(cur) > 1 else 0) + ww
    if cur: lines.append(cur)
    return lines


# ---------------- v3 HUMOR PACK: Buck the coin, speech bubbles, stickers ----------------
FONT_DIR = os.environ.get("FIN_FONTS", os.path.join(tempfile.gettempdir(), "fin_fonts"))
COMIC_FALLBACK = "/usr/share/fonts/truetype/google-fonts/ofl/comicrelief/ComicRelief-Bold.ttf"


def fun_font(name="Bangers-Regular.ttf"):
    """Open-licence (OFL) display fonts from github.com/google/fonts; falls back to Comic Relief."""
    p = os.path.join(FONT_DIR, name)
    if not os.path.exists(p):
        sub = {"Bangers-Regular.ttf": "bangers", "LilitaOne-Regular.ttf": "lilitaone", "CourierPrime-Bold.ttf": "courierprime",
               "BlackOpsOne-Regular.ttf": "blackopsone"}.get(name)
        try:
            os.makedirs(FONT_DIR, exist_ok=True)
            subprocess.run(["curl", "-sSfL", "-o", p + ".part", f"https://raw.githubusercontent.com/google/fonts/main/ofl/{sub}/{name}"], timeout=60, check=True)
            os.replace(p + ".part", p)
        except Exception:
            return COMIC_FALLBACK
    return p


INK = (24, 20, 30, 255)
COIN_RIM = (178, 118, 14, 255); COIN_FACE = (240, 182, 40, 255); COIN_RING = (214, 154, 24, 255); COIN_HI = (255, 222, 110, 255)
MOODS = ("happy", "shocked", "laugh", "smug", "confused", "sideeye", "sad", "angry", "point", "dizzy", "thumbsup", "proud")
ACTS = ("roll_in", "drop_in", "flip", "bonk", "dodge")
_BROWS = {"shocked": (-0.13, -0.13), "angry": (0.11, -0.07), "sad": (-0.09, 0.06), "sideeye": (0.04, 0.04),
          "laugh": (-0.07, -0.04), "happy": (-0.05, -0.02), "point": (-0.04, -0.02), "dizzy": (-0.1, 0.02),
          "thumbsup": (-0.06, -0.03), "proud": (-0.08, -0.06)}
_ARMS = {"shocked": [(-1.55, -0.8), (1.55, -0.8)], "happy": [(-1.45, 0.3), (1.5, -0.55)], "laugh": [(-0.7, 0.72), (0.7, 0.72)],
         "smug": [(-0.98, 0.55), (1.0, 0.55)], "confused": [(-1.4, 0.45), (0.62, -1.08)], "sideeye": [(-1.2, 0.8), (1.2, 0.8)],
         "sad": [(-1.1, 1.0), (1.1, 1.0)], "angry": [(-1.3, -0.3), (1.3, -0.3)], "point": [(-1.25, 0.65), (1.8, -0.2)],
         "dizzy": [(-1.5, 0.1), (1.5, 0.5)], "thumbsup": [(-1.2, 0.7), (1.45, -0.75)], "proud": [(-0.98, 0.5), (0.98, 0.5)]}
TIE = (43, 214, 123, 255); TIE_D = (20, 140, 80, 255); SHOE = (43, 190, 110, 255)


def _price_tag(d, x, y, s, ang=0.0, label="$9.99"):
    """Small paper price tag (white card + hole + string) centred at x, y; s = height in px."""
    w, h = s * 1.5, s
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    def rot(px, py): return (x + px * ca - py * sa, y + px * sa + py * ca)
    pts = [rot(-w / 2 + h * 0.3, -h / 2), rot(w / 2, -h / 2), rot(w / 2, h / 2), rot(-w / 2 + h * 0.3, h / 2), rot(-w / 2, 0)]
    d.polygon(pts, fill=(255, 250, 235, 255), outline=INK, width=max(2, int(s * 0.07)))
    hx, hy = rot(-w / 2 + h * 0.28, 0); hr = s * 0.08
    d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=INK)
    if abs(ang) < 25:
        f = ImageFont.truetype(ANTON, max(8, int(s * 0.5)))
        tw = d.textlength(label, font=f); cx_, cy_ = rot(h * 0.12, 0)
        d.text((cx_ - tw / 2, cy_ - s * 0.36), label, font=f, fill=(220, 40, 50, 255))


def _star(d, x, y, r, fill=(255, 214, 60, 255)):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * 0.45
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    d.polygon(pts, fill=fill, outline=INK)


def mascot_patch(R, mood, t, lt, SS=2, act=None, act_lt=-1.0):
    """BUCK — the channel's own cartoon coin (original design, drawn here in code; no outside assets).
    Look: gold coin, green bow tie, green sneakers, white gloves, big kind eyes; the eyebrows do the acting.
    Character: kind, brave, a little clumsy; does his own stunts and always bounces back.
    Returns an antialiased RGBA patch + its anchor (body centre). act: roll_in | drop_in | flip | bonk | dodge."""
    r = R * SS; P = int(r * 4.6)
    im = Image.new("RGBA", (P, P), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ax, ay = P / 2, P * 0.46
    a = ease_back(lt / 0.32) if lt < 0.32 else 1.0
    if act in ("roll_in", "drop_in"): a = 1.0  # these acts are their own entrance
    if a < 0.04: return None, (0, 0)
    wob = math.exp(-lt * 5) * math.sin(lt * 26)
    sx, sy = 1 + 0.12 * wob, 1 - 0.12 * wob
    dx, dy, tilt = 0.0, math.sin(t * 4.2) * 0.035 * r, 0.0
    if mood == "shocked":
        if lt < 0.45: dy -= math.sin(lt / 0.45 * math.pi) * 0.45 * r
        else: dx = math.sin(t * 60) * 0.022 * r
    elif mood == "laugh": dy -= abs(math.sin(t * 13)) * 0.09 * r; tilt = math.sin(t * 9) * 6
    elif mood == "confused": tilt = 10 * math.sin(min(1.0, lt / 0.5) * math.pi / 2)
    elif mood == "sad": sy *= 0.96; dy += 0.05 * r
    elif mood == "angry": dx = math.sin(t * 45) * 0.02 * r
    elif mood == "happy": dy -= abs(math.sin(t * 5)) * 0.05 * r
    elif mood == "dizzy": tilt = math.sin(t * 3.5) * 8; dx = math.sin(t * 3.5) * 0.05 * r
    elif mood == "proud": sy *= 1.03; dy -= 0.03 * r
    # ---- stunts ----
    tag_fall = None; tag_fly = None; stars = 0.0
    if act == "flip" and 0 <= act_lt < 0.7:
        p = act_lt / 0.7
        dy -= math.sin(p * math.pi) * 0.9 * r
        sx *= max(0.08, abs(math.cos(p * 2 * math.pi)))  # two edge-on spins = coin flip
    elif act == "bonk":
        if act_lt < 0.22: tag_fall = act_lt / 0.22                      # tag falling onto his head
        elif act_lt < 0.4: q = (act_lt - 0.22) / 0.18; sy *= 1 - 0.18 * math.sin(q * math.pi); sx *= 1 + 0.12 * math.sin(q * math.pi)
        if 0.22 <= act_lt < 1.5: stars = act_lt - 0.22
    elif act == "dodge" and 0 <= act_lt < 0.75:
        p = act_lt / 0.75
        tilt = -24 * math.sin(p * math.pi); dx += 0.12 * r * math.sin(p * math.pi)
        tag_fly = p
    cx, cy = ax + dx, ay + dy
    k = a; rx, ry = r * sx * a, r * sy * a
    lw = max(2, int(0.065 * r))
    # legs + green sneakers (white soles)
    for side in (-1, 1):
        lx = cx + side * 0.3 * min(rx, r); fy = cy + ry + 0.42 * r * k
        d.line([(lx, cy + ry * 0.85), (lx + side * 0.05 * r, fy)], fill=INK, width=lw)
        sxc = lx + side * 0.12 * r
        d.rounded_rectangle([sxc - 0.22 * r * k, fy - 0.09 * r * k, sxc + 0.22 * r * k, fy + 0.09 * r * k], radius=int(0.08 * r), fill=SHOE, outline=INK, width=max(2, int(0.03 * r)))
        d.rectangle([sxc - 0.2 * r * k, fy + 0.03 * r * k, sxc + 0.2 * r * k, fy + 0.07 * r * k], fill=(255, 255, 255, 255))
    # arms (curved) + white gloves (hidden while edge-on mid-flip)
    arms = _ARMS.get(mood, [(-1.4, 0.4), (1.4, 0.4)]) if sx >= 0.35 else []
    for i, (hx, hy) in enumerate(arms):
        side = -1 if i == 0 else 1
        x0, y0 = cx + side * min(rx, r) * 0.95, cy + 0.12 * r
        ex, ey = cx + hx * r * k, cy + hy * r * k
        if mood == "happy" and i == 1: ey += math.sin(t * 11) * 0.14 * r  # waving
        mx_, my_ = (x0 + ex) / 2 + side * 0.12 * r, (y0 + ey) / 2 + 0.12 * r
        d.line([(x0, y0), (mx_, my_), (ex, ey)], fill=INK, width=lw, joint="curve")
        hr = 0.16 * r * k
        d.ellipse([ex - hr, ey - hr, ex + hr, ey + hr], fill=(252, 252, 252, 255), outline=INK, width=max(2, int(0.035 * r)))
        if mood == "thumbsup" and i == 1:  # thumb up
            d.rounded_rectangle([ex - hr * 0.35, ey - hr * 2.0, ex + hr * 0.35, ey - hr * 0.6], radius=int(hr * 0.3), fill=(252, 252, 252, 255), outline=INK, width=max(2, int(0.03 * r)))
    # body: rim, face, inner ring, shine, outline
    face = (238, 130, 70, 255) if mood == "angry" else COIN_FACE
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=COIN_RIM)
    d.ellipse([cx - rx * .92, cy - ry * .92, cx + rx * .92, cy + ry * .92], fill=face)
    d.ellipse([cx - rx * .8, cy - ry * .8, cx + rx * .8, cy + ry * .8], outline=COIN_RING, width=max(2, int(0.04 * r)))
    d.ellipse([cx - rx * .64, cy - ry * .8, cx - rx * .2, cy - ry * .5], fill=COIN_HI)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=INK, width=lw)
    edge_on = sx < 0.35  # mid-flip: no face
    # eyes
    blink = (t % 2.7) < 0.12 and mood not in ("shocked", "dizzy")
    ew, eh = (0.27 * r * k, 0.36 * r * k) if mood == "shocked" else (0.21 * r * k, 0.27 * r * k)
    ew *= min(1.0, sx); ey0 = cy - 0.17 * r * k
    pdx = {"sideeye": 0.1, "smug": 0.05, "point": 0.08}.get(mood, 0) * r
    pdy = {"sad": 0.06, "confused": -0.08}.get(mood, 0) * r
    for side in (() if edge_on else (-1, 1)):
        ex0 = cx + side * 0.3 * r * k * min(1.0, sx)
        if mood == "dizzy":  # spiral eyes
            d.ellipse([ex0 - ew, ey0 - eh, ex0 + ew, ey0 + eh], fill=(255, 255, 255, 255), outline=INK, width=max(2, int(0.035 * r)))
            for j in range(3):
                rr_ = (0.75 - 0.22 * j) * ew; st_ = (t * 400 + j * 90) % 360
                d.arc([ex0 - rr_, ey0 - rr_, ex0 + rr_, ey0 + rr_], st_, st_ + 250, fill=INK, width=max(2, int(0.03 * r)))
            continue
        if blink or mood in ("laugh", "proud"):
            if mood in ("laugh", "proud"):  # happy closed eyes ^ ^
                d.arc([ex0 - ew, ey0 - eh * 0.6, ex0 + ew, ey0 + eh * 0.9], 200, 340, fill=INK, width=lw)
            else:
                d.line([(ex0 - ew, ey0), (ex0 + ew, ey0)], fill=INK, width=lw)
            continue
        d.ellipse([ex0 - ew, ey0 - eh, ex0 + ew, ey0 + eh], fill=(255, 255, 255, 255), outline=INK, width=max(2, int(0.035 * r)))
        pr = (0.07 if mood == "shocked" else 0.09) * r * k
        px, py = ex0 + pdx, ey0 + pdy + 0.04 * r
        d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=INK)
        d.ellipse([px - pr * .6, py - pr * .7, px - pr * .15, py - pr * .25], fill=(255, 255, 255, 255))
        if mood in ("smug", "sideeye"):  # heavy lids
            d.chord([ex0 - ew - 1, ey0 - eh - 1, ex0 + ew + 1, ey0 + eh + 1], 180, 360, fill=face)
            d.line([(ex0 - ew, ey0), (ex0 + ew, ey0)], fill=INK, width=lw)
    # eyebrows
    for side in (() if edge_on else (-1, 1)):
        inn, out = _BROWS.get(mood, (0.0, 0.0))
        if mood == "smug" and side == 1: inn, out = -0.1, -0.15
        if mood == "confused": inn, out = ((-0.13, -0.1) if side == 1 else (0.02, 0.02))
        by = ey0 - eh - 0.09 * r * k
        d.line([(cx + side * 0.12 * r * k * min(1, sx), by + inn * r), (cx + side * 0.46 * r * k * min(1, sx), by + out * r)], fill=INK, width=max(3, int(0.075 * r)))
    # mouth
    my = cy + 0.34 * r * k
    if edge_on: pass
    elif mood in ("happy", "laugh", "thumbsup", "proud"):
        w = 0.36 if mood == "laugh" else 0.28
        d.chord([cx - w * r, my - 0.2 * r, cx + w * r, my + (0.32 if mood == "laugh" else 0.2) * r], 0, 180, fill=(120, 24, 34, 255), outline=INK, width=lw)
        d.ellipse([cx - 0.13 * r, my + 0.05 * r, cx + 0.13 * r, my + (0.26 if mood == "laugh" else 0.17) * r], fill=(240, 110, 120, 255))
    elif mood == "shocked":
        d.ellipse([cx - 0.14 * r, my - 0.1 * r, cx + 0.14 * r, my + 0.24 * r], fill=(100, 18, 28, 255), outline=INK, width=lw)
    elif mood == "smug":
        d.line([(cx - 0.2 * r, my + 0.04 * r), (cx + 0.05 * r, my + 0.06 * r), (cx + 0.26 * r, my - 0.1 * r)], fill=INK, width=lw, joint="curve")
    elif mood == "sideeye":
        d.line([(cx - 0.16 * r, my + 0.03 * r), (cx + 0.2 * r, my)], fill=INK, width=lw)
    elif mood == "sad":
        d.arc([cx - 0.22 * r, my, cx + 0.22 * r, my + 0.3 * r], 200, 340, fill=INK, width=lw)
    elif mood == "angry":
        d.rounded_rectangle([cx - 0.24 * r, my - 0.05 * r, cx + 0.24 * r, my + 0.13 * r], radius=int(0.05 * r), fill=(255, 255, 255, 255), outline=INK, width=lw)
        for q in (-0.12, 0, 0.12): d.line([(cx + q * r, my - 0.05 * r), (cx + q * r, my + 0.13 * r)], fill=INK, width=max(2, lw // 2))
    elif mood in ("confused", "dizzy"):
        pts = [(cx - 0.2 * r + i * 0.04 * r, my + 0.05 * r + math.sin(i * 1.3 + (t * 6 if mood == "dizzy" else 0)) * 0.04 * r) for i in range(11)]
        d.line(pts, fill=INK, width=lw, joint="curve")
    else:  # point / neutral smile
        d.arc([cx - 0.2 * r, my - 0.14 * r, cx + 0.2 * r, my + 0.12 * r], 20, 160, fill=INK, width=lw)
    # signature green bow tie (wiggles when he's happy)
    if not edge_on:
        tw_ = 0.3 * r * k; th_ = 0.15 * r * k; bx, by_ = cx, cy + ry * 0.8
        wig = math.sin(t * 9) * 0.04 * r if mood in ("happy", "laugh", "proud", "thumbsup") else 0
        d.polygon([(bx, by_), (bx - tw_, by_ - th_ + wig), (bx - tw_, by_ + th_ - wig)], fill=TIE, outline=INK)
        d.polygon([(bx, by_), (bx + tw_, by_ - th_ - wig), (bx + tw_, by_ + th_ + wig)], fill=TIE, outline=INK)
        kr = 0.07 * r * k
        d.rounded_rectangle([bx - kr, by_ - kr, bx + kr, by_ + kr], radius=int(kr * 0.4), fill=TIE_D, outline=INK, width=max(2, int(0.025 * r)))
    # extras
    if mood == "confused" and lt > 0.2:
        fq = ImageFont.truetype(ANTON, int(0.55 * r))
        d.text((cx + 0.92 * r, cy - 1.3 * r + math.sin(t * 5) * 0.05 * r), "?", font=fq, fill=(255, 255, 255, 255), stroke_width=max(3, int(0.05 * r)), stroke_fill=INK)
    if mood == "shocked" and lt > 0.15:
        fq = ImageFont.truetype(ANTON, int(0.5 * r))
        d.text((cx - 0.12 * r, cy - 1.75 * r), "!", font=fq, fill=(255, 77, 77, 255), stroke_width=max(3, int(0.05 * r)), stroke_fill=INK)
        sw = 0.5 + 0.5 * math.sin(t * 3)
        d.ellipse([cx + 0.72 * r, cy - 0.65 * r + sw * 0.1 * r, cx + 0.86 * r, cy - 0.42 * r + sw * 0.1 * r], fill=(120, 200, 255, 255), outline=INK, width=2)
    if mood in ("sad", "laugh"):
        fall = (lt * 0.6) % 1.0 if mood == "sad" else 0.0
        for side in ((-1,) if mood == "sad" else (-1, 1)):
            tx = cx + side * (0.3 * r + (0.2 * r if mood == "laugh" else 0)); ty = ey0 + 0.25 * r + fall * 0.6 * r
            d.ellipse([tx - 0.06 * r, ty - 0.06 * r, tx + 0.06 * r, ty + 0.1 * r], fill=(120, 200, 255, 255), outline=INK, width=2)
    if mood == "angry":
        for j, sx0 in enumerate((-0.45, 0.45)):
            pz = (t * 1.5 + j * 0.5) % 1.0
            rr = (0.08 + 0.1 * pz) * r
            d.ellipse([cx + sx0 * r - rr, cy - 1.15 * r - pz * 0.4 * r - rr, cx + sx0 * r + rr, cy - 1.15 * r - pz * 0.4 * r + rr], fill=(235, 235, 240, int(230 * (1 - pz))))
    if mood == "laugh":  # hands in front, holding the belly
        for hx in (-0.55, 0.55):
            ex, ey = cx + hx * r * k, cy + 0.72 * r * k; hr = 0.16 * r * k
            d.ellipse([ex - hr, ey - hr, ex + hr, ey + hr], fill=(252, 252, 252, 255), outline=INK, width=max(2, int(0.035 * r)))
    # stunt props
    if tag_fall is not None:
        _price_tag(d, cx + 0.1 * r, (ay - 2.0 * r) + tag_fall * (1.0 * r), 0.42 * r, ang=15 * tag_fall)
    if stars > 0 or mood == "dizzy":
        st = stars if stars > 0 else t
        for j in range(3):
            ang_ = st * 6 + j * 2.09
            _star(d, cx + math.cos(ang_) * 0.6 * r, cy - 1.12 * r + math.sin(ang_) * 0.16 * r, 0.12 * r)
    if tag_fly is not None:
        _price_tag(d, ax + (1.0 - 2.0 * tag_fly) * 2.1 * r, ay - 0.45 * r, 0.38 * r, ang=-10)
        for j in range(3):  # speed lines
            lx = ax + (1.0 - 2.0 * tag_fly) * 2.1 * r + 0.75 * r + j * 0.18 * r
            d.line([(lx, ay - 0.55 * r + j * 0.1 * r), (lx + 0.3 * r, ay - 0.55 * r + j * 0.1 * r)], fill=(255, 255, 255, 200), width=max(2, int(0.03 * r)))
    if tilt: im = im.rotate(tilt, resample=Image.BICUBIC, center=(ax, ay))
    out = im.resize((P // SS, P // SS), Image.LANCZOS)
    # white sticker outline so Buck (and his dark limbs) pop on any background
    m = out.split()[3].filter(ImageFilter.GaussianBlur(max(2, R * 0.045))).point(lambda v: 255 if v > 10 else 0)
    border = Image.new("RGBA", out.size, (250, 250, 252, 255)); border.putalpha(m)
    return Image.alpha_composite(border, out), (ax / SS, ay / SS)


# ---- BUCK 3D: pre-rendered Blender (Cycles) sprite library, see buck3d.py ----
BUCK3D_DIR = os.environ.get("FIN_BUCK3D", "")  # optional local library (any version)
_GH = "https://raw.githubusercontent.com/financier-videos/financier-videos/media/assets/"
BUCK3D_LIBS = [("v3", _GH + "buck3d_v3.tar"), ("v2", _GH + "buck3d_v2.tar"), ("v1", _GH + "buck3d_v1.tar")]  # v3 = rigged Buck (2026-11-21, 800 px); v2 = cinema 1080 px; v1 = 600 px fallback
BUCK3D_FPS = 15
ACT_CLIP = {"flip": ("flip_happy", 0.7), "bonk": ("bonk_dizzy", 1.5), "dodge": ("dodge_shocked", 0.75)}
BUCK3D_CLIPS = list(MOODS) + ["flip_happy", "bonk_dizzy", "dodge_shocked"]
_B3 = {"ok": None, "cache": {}, "dir": None, "ver": None, "n": {}, "ext": {}}


def b3_feet():
    """Feet line of the sprite (fraction of its height): v1 framing 0.79; the v2 slot holds the hybrid Buck (taller hat, longer
    legs, framing scaled 1.234x) whose shoes sit at 0.86."""
    return 0.86 if _B3.get("ver") in ("v2", "v3") else 0.79


def buck3d_extent(clip, size):
    """Union alpha bbox (x0, y0, x1, y1) of every frame of a clip at this sprite size (cached) -> keeps a corner Buck,
    including raised gloves and the hat, fully inside the frame."""
    key = (clip, size)
    if key not in _B3["ext"]:
        box = None; n = 0
        while n < 40:
            im = buck3d_frame(clip, n, size) if n < max(1, _B3["n"].get(clip, (1, ""))[0]) else None
            if im is None: break
            b = im.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox()
            if b: box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
            n += 1
        _B3["ext"][key] = box
    return _B3["ext"][key]


def _lib_complete(d):
    return bool(d) and os.path.isdir(d) and all(
        any(os.path.exists(os.path.join(d, f"{c}_00.{e}")) for e in ("webp", "png")) for c in BUCK3D_CLIPS)


def _fetch_tar(url, d, timeout=600):
    """Unpack a sprite tar into d. Prefers the repo's own assets/<name> (no download); otherwise downloads to a
    per-process temp name so parallel renders never delete each other's half-downloaded tar (2026-11-20 race)."""
    name = url.rsplit("/", 1)[-1]
    local = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", name)
    try:
        os.makedirs(d, exist_ok=True)
        if os.path.isfile(local) and os.path.getsize(local) > 1_000_000:
            subprocess.run(["tar", "-xf", local, "-C", d], check=True); return
        tar = os.path.join(d, f".{name}.{os.getpid()}.part")
        try:
            subprocess.run(["curl", "-sSfL", "-o", tar, url], timeout=timeout, check=True)
            subprocess.run(["tar", "-xf", tar, "-C", d], check=True)
        finally:
            if os.path.exists(tar): os.remove(tar)
    except Exception:
        pass


def buck3d_ready():
    """Pick the best COMPLETE sprite library: env FIN_BUCK3D -> v2 (cinema) -> v1 (downloaded from GitHub once)."""
    if _B3["ok"] is None:
        cands = ([("local", BUCK3D_DIR, None)] if BUCK3D_DIR else []) + \
                [(v, os.path.join(tempfile.gettempdir(), f"fin_buck3d_{v}"), u) for v, u in BUCK3D_LIBS]
        for ver, d, url in cands:
            if not _lib_complete(d) and url:
                _fetch_tar(url, d)
            if _lib_complete(d):
                _B3.update(dir=d, ver=ver)
                if ver in ("v2", "v3") and not os.path.exists(os.path.join(d, "happy_t1_00.webp")):  # optional lip-sync mouth variants
                    _fetch_tar(_GH + f"buck3d_{ver}_talk.tar", d, timeout=900)
                _B3["talk"] = any(os.path.exists(os.path.join(d, f"happy_t1_00.{e}")) for e in ("webp", "png"))
                break
        _B3["ok"] = _B3["dir"] is not None
    return _B3["ok"]


def buck3d_frame(clip, i, size):
    d = _B3["dir"]
    if clip not in _B3["n"]:
        ext = "webp" if os.path.exists(os.path.join(d, f"{clip}_00.webp")) else "png"; n = 0
        while os.path.exists(os.path.join(d, f"{clip}_{n:02d}.{ext}")): n += 1
        _B3["n"][clip] = (n, ext)
    n, ext = _B3["n"][clip]
    if n == 0: return None
    key = (clip, min(i, n - 1) if not (clip in MOODS or "_t" in clip[-3:]) else i % n, size)
    if key not in _B3["cache"]:
        if len(_B3["cache"]) > 400: _B3["cache"].clear()
        im = Image.open(os.path.join(d, f"{key[0]}_{key[1]:02d}.{ext}")).convert("RGBA")
        _B3["cache"][key] = im.resize((size, size), Image.LANCZOS)
    return _B3["cache"][key]


OPEN_MOODS = ("happy", "laugh", "thumbsup")  # idle mouth already open -> use the small-open variant between syllables


RHUBARB = os.environ.get("FIN_RHUBARB", os.path.expanduser("~/tools/rhubarb/Rhubarb-Lip-Sync-1.14.0-Linux/rhubarb"))
_SHAPE_LV = {"A": 0, "X": 0, "B": 1, "G": 1, "H": 1, "C": 2, "D": 2, "E": 3, "F": 3}


def rhubarb_cues(audio, sr, spec, workdir):
    """v6.8 lip-sync (skill: docs/skills/notes/2026-11-21_rhubarb-lip-sync.md; Rhubarb 1.14.0, MIT, offline binary kept
    OUTSIDE the repo - env FIN_RHUBARB). Dry voice (before sfx) + spoken script as dialog hint -> [(start, end, level)]
    with level 0 closed/rest, 1 half, 2 wide, 3 rounded. Cached by audio hash. Any failure -> None (envelope fallback)."""
    if spec.get("lipsync") == "envelope" or not os.path.isfile(RHUBARB): return None
    try:
        import hashlib, soundfile as sf
        h = hashlib.sha1(np.asarray(audio, np.float32).tobytes()).hexdigest()[:16]
        cdir = os.environ.get("FIN_TTS_CACHE", os.path.join(tempfile.gettempdir(), "fin_tts_cache"))
        os.makedirs(cdir, exist_ok=True); cj = os.path.join(cdir, f"rhubarb_{h}.json")
        if not os.path.exists(cj):
            w16 = os.path.join(workdir, "lips16k.wav"); tmp = os.path.join(workdir, "lips_tmp.wav"); sf.write(tmp, audio, sr)
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-ar", "16000", "-ac", "1", w16], check=True)
            dlg = os.path.join(workdir, "dialog.txt")
            txt = " ".join(" ".join(p for p in (sc.get("buck"), sc.get("say", sc.get("text", ""))) if p) for sc in spec["scenes"])
            open(dlg, "w").write(re.sub(r"\s+", " ", txt))
            subprocess.run([RHUBARB, "-q", "-f", "json", "-d", dlg, "--extendedShapes", "GHX", w16, "-o", cj + ".part"],
                           check=True, timeout=600, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os.replace(cj + ".part", cj)
        cues = [(c["start"], c["end"], _SHAPE_LV.get(c["value"], 1)) for c in json.load(open(cj))["mouthCues"]]
        print(f"[lipsync] rhubarb: {len(cues)} cues", file=sys.stderr)
        return cues
    except Exception as e:
        print(f"[lipsync] rhubarb failed ({e}); envelope fallback", file=sys.stderr)
        return None


def talk_level(env, words, fi, t, cues=None):
    """Lip-sync: mouth variant for this video frame (0 = idle pose, 1 half open, 2 wide, 3 rounded 'o') from the speech
    envelope (sampled at the sprite rate so it never flickers) and the vowel of the word being spoken."""
    if cues:  # v6.8 phoneme cues, sampled at the sprite rate (every 2nd frame) so the mouth never flickers
        tj = ((fi // 2) * 2) / FPS
        return next((lv for st_, en_, lv in cues if st_ <= tj < en_), 0)
    if not env: return None
    j = (fi // 2) * 2; a = max(env[min(j, len(env) - 1)], env[min(j + 1, len(env) - 1)])
    if a < 0.12: return 0
    w = next((x[0].lower() for x in (words or []) if x[1] - 0.03 <= t <= x[2] + 0.03), "")
    if a < 0.5 and any(k in w for k in ("oo", "ou", "ow", "oh", "wh", "you", "who", "two")): return 3
    return 2 if a >= 0.5 else 1


def mascot3d_patch(R, mood, t, lt, act=None, act_lt=-1.0, talk=None):
    """3D Buck: picks the loop/act frame and adds the 2D extras (pop-in, squash, shocked jump)."""
    size = int(R * 4.6)
    a = ease_back(lt / 0.32) if lt < 0.32 else 1.0
    if act in ("roll_in", "drop_in"): a = 1.0
    if a < 0.04: return None, (0, 0)
    clip = mood if mood in MOODS else "happy"
    if act in ACT_CLIP and 0 <= act_lt < ACT_CLIP[act][1]:
        clip = ACT_CLIP[act][0]; fi = int(act_lt * BUCK3D_FPS)
    else:
        fi = int(lt * BUCK3D_FPS)
        if talk is not None and _B3.get("talk") and clip in MOODS:
            lv = talk if talk else (1 if clip in OPEN_MOODS else 0)
            if lv:
                n0 = _B3["n"].get(clip) or (buck3d_frame(clip, 0, size) is not None and _B3["n"].get(clip))
                tclip = f"{clip}_t{lv}"
                tim = buck3d_frame(tclip, fi % max(1, (n0 or (15, ""))[0]), size)
                if tim is not None: clip = tclip
    im = buck3d_frame(clip, fi, size)
    if im is None: return "missing", (0, 0)
    wob = math.exp(-lt * 5) * math.sin(lt * 26)
    sx, sy = a * (1 + 0.10 * wob), a * (1 - 0.10 * wob)
    if act == "drop_in" and 0.4 < act_lt < 0.7:  # landing squash
        q = (act_lt - 0.4) / 0.3; sy *= 1 - 0.15 * math.sin(q * math.pi); sx *= 1 + 0.1 * math.sin(q * math.pi)
    dy = 0.0
    if mood == "shocked" and lt < 0.45 and act not in ACT_CLIP: dy = -math.sin(lt / 0.45 * math.pi) * 0.45 * R
    if abs(sx - 1) > 1e-3 or abs(sy - 1) > 1e-3:  # squash & stretch, feet stay planted
        w2, h2 = max(1, int(size * sx)), max(1, int(size * sy))
        im2 = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        paste_rgba(im2, im.resize((w2, h2), Image.BILINEAR), (size - w2) / 2, size * b3_feet() - h2 * b3_feet())
        im = im2
    if dy:
        im2 = Image.new("RGBA", (size, size), (0, 0, 0, 0)); paste_rgba(im2, im, 0, dy); im = im2
    return im, (size / 2, size * 0.46)


def bubble_patch(text, size, maxw, tail="down", SS=2):
    """White comic speech bubble with tail; Bangers font."""
    f = ImageFont.truetype(fun_font("Bangers-Regular.ttf"), int(size * SS))
    tmp = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    lines = wrap(tmp, text.upper(), f, maxw * SS * 0.86)
    lh = f.size * 1.05
    tw = max(tmp.textlength(l, font=f) for l in lines)
    pad = f.size * 0.45; bw = tw + pad * 2; bh = lh * len(lines) + pad * 1.4; tl = f.size * 0.7
    im = Image.new("RGBA", (int(bw + 12), int(bh + tl + 12)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    o = 6; lwid = max(3, int(size * SS * 0.07))
    if tail == "down":
        tri = [(o + bw * 0.42, o + bh - lwid), (o + bw * 0.58, o + bh - lwid), (o + bw * 0.47, o + bh + tl)]
    else:  # tail to the left (mascot sits left of the bubble)
        tri = [(o + lwid, o + bh * 0.45), (o + lwid, o + bh * 0.72), (o - tl * 0.2, o + bh * 0.9)]
    d.polygon(tri, fill=INK)
    d.rounded_rectangle([o, o, o + bw, o + bh], radius=int(f.size * 0.45), fill=(255, 255, 255, 255), outline=INK, width=lwid)
    shrink = [(x + (0 if tail == "down" else lwid * 1.2), y - (lwid * 1.3 if tail == "down" else 0)) for x, y in tri]
    d.polygon(shrink, fill=(255, 255, 255, 255))
    for i, l in enumerate(lines):
        w = d.textlength(l, font=f)
        d.text((o + (bw - w) / 2, o + pad * 0.75 + i * lh), l, font=f, fill=INK)
    return im.resize((max(1, im.width // SS), max(1, im.height // SS)), Image.LANCZOS)


def sticker_patch(text, size, color=(255, 77, 77), SS=2):
    f = ImageFont.truetype(fun_font("Bangers-Regular.ttf"), int(size * SS))
    tmp = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    tw = tmp.textlength(text.upper(), font=f); pad = f.size * 0.3
    im = Image.new("RGBA", (int(tw + pad * 2 + 20), int(f.size * 1.35 + 20)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([10, 10, 10 + tw + pad * 2, 10 + f.size * 1.3], radius=int(f.size * 0.18), fill=tuple(color) + (255,), outline=INK, width=max(4, int(size * SS * 0.06)))
    d.text((10 + pad, 10 + f.size * 0.12), text.upper(), font=f, fill=(255, 255, 255, 255), stroke_width=max(3, int(size * SS * 0.05)), stroke_fill=INK)
    im = im.rotate(-7, resample=Image.BICUBIC, expand=True)
    return im.resize((max(1, im.width // SS), max(1, im.height // SS)), Image.LANCZOS)


def paste_rgba(dst, patch, x, y):
    """Alpha-composite patch onto dst at (x, y), clipping at the edges."""
    x, y = int(round(x)), int(round(y))
    sx0, sy0 = max(0, -x), max(0, -y)
    ex, ey = min(patch.width, dst.width - x), min(patch.height, dst.height - y)
    if ex <= sx0 or ey <= sy0: return
    dst.alpha_composite(patch.crop((sx0, sy0, ex, ey)) if (sx0 or sy0 or ex < patch.width or ey < patch.height) else patch, (x + sx0, y + sy0))


# ---------------- v4.1: split-screen "VS" comparison ----------------
def _vs_at(vs):
    at = [float(a) for a in vs.get("at", [0.2, 1.2])][:2]
    while len(at) < 2: at.append((at[-1] if at else 0.2) + 1.0)
    return at


def prep_vs(vs, W, H, S, long):
    """Precompute the VS layout: two panels (label / big value / sub-line) and the badge."""
    at = _vs_at(vs)
    cx = W * (0.5 if long else 0.47)  # Shorts: keep clear of the right-side buttons
    pw = W * (0.40 if long else 0.39); gap = W * (0.07 if long else 0.04)
    y0, y1 = (H * 0.24, H * 0.74) if long else (H * 0.285, H * 0.60)
    tmp = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    f_lab = ImageFont.truetype(INTER_XB, int(S * (0.04 if long else 0.042)))
    f_sub = ImageFont.truetype(INTER_SB, int(S * (0.032 if long else 0.036)))
    sides = []
    for i, side in enumerate(("left", "right")):
        val = str(vs.get(side, ""))
        vsz = int(S * (0.16 if long else 0.17))
        while vsz > 30 and tmp.textlength(val, font=ImageFont.truetype(ANTON, vsz)) > pw * 0.70: vsz = int(vsz * 0.92)
        sides.append({"val": val, "vsz": vsz,
                      "lab": wrap(tmp, str(vs.get(side + "_label", "")).upper(), f_lab, pw * 0.86),
                      "sub": wrap(tmp, str(vs.get(side + "_sub", "")), f_sub, pw * 0.86),
                      "col": hex2rgb(vs.get(side + "_color", "#9AA4B8" if side == "left" else "#F5C542")),
                      "x": cx - gap / 2 - pw if i == 0 else cx + gap / 2, "sgn": -1 if i == 0 else 1, "at": at[i],
                      "win": vs.get("win", "right") == side})
    return {"at": at, "cx": cx, "pw": pw, "y0": y0, "y1": y1, "sides": sides, "f_lab": f_lab, "f_sub": f_sub,
            "has_win": vs.get("win", "right") in ("left", "right"), "W": W, "S": S, "fonts": {},
            "vs_at": float(vs.get("vs_at", (at[0] + at[1]) / 2 + 0.1)), "no_ghost": bool(vs.get("no_ghost")), "badge_r": S * (0.055 if long else 0.06)}  # values stay inside 70% of the panel, so the badge never covers them


def _vs_font(v, path, size):
    key = (path, int(size))
    if key not in v["fonts"]: v["fonts"][key] = ImageFont.truetype(path, max(8, int(size)))
    return v["fonts"][key]


def draw_vs(fd, v, lt):
    """Panels slide in (overshoot), values count up with a punch, winner glows, loser dims, VS badge slams."""
    W, S, pw, y0, y1 = v["W"], v["S"], v["pw"], v["y0"], v["y1"]
    settle = max(v["at"]) + 0.9; rad = int(S * 0.03)
    for sd in v["sides"]:
        p = (lt - sd["at"]) / 0.35
        if p <= 0:
            # v6.3: no empty middle before a panel lands — a dashed "?" placeholder pulses in its slot (teases the reveal)
            if sd["at"] > 0.25 and not v.get("no_ghost"):
                fin = min(1.0, lt / 0.2) * (1 - max(0.0, min(1.0, (lt - sd["at"] + 0.08) / 0.08)))
                pul = 0.75 + 0.25 * math.cos(lt * 7 + sd["sgn"]); a = int(150 * fin * pul)
                x = sd["x"]; dash = S * 0.035; wd = max(3, int(S * 0.005)); col = sd["col"] + (a,)
                for (xa, ya, xb, yb) in ((x, y0, x + pw, y0), (x, y1, x + pw, y1), (x, y0, x, y1), (x + pw, y0, x + pw, y1)):
                    L = math.hypot(xb - xa, yb - ya); n = max(1, int(L / (dash * 2)))
                    for k in range(n):
                        t0 = k * 2 * dash / L; t1 = min(1.0, (k * 2 + 1) * dash / L)
                        fd.line([(xa + (xb - xa) * t0, ya + (yb - ya) * t0), (xa + (xb - xa) * t1, ya + (yb - ya) * t1)], fill=col, width=wd)
                fq = _vs_font(v, ANTON, sd["vsz"] * (0.9 + 0.06 * pul))
                fd.text((x + pw / 2, (y0 + y1) / 2), "?", font=fq, fill=col, stroke_width=max(2, int(S * 0.004)), stroke_fill=(0, 0, 0, a), anchor="mm")
            continue
        e = ease_back(p) if p < 1 else 1.0
        x = sd["x"] + (1 - e) * W * 0.6 * sd["sgn"]
        dim = 1.0
        if v["has_win"] and not sd["win"] and lt > settle: dim = max(0.45, 1 - (lt - settle) / 0.4 * 0.55)
        A = lambda a: int(a * dim); col = sd["col"]
        if sd["win"] and lt > settle:  # pulsing glow around the winner
            q = lt - settle; pulse = 0.65 + 0.35 * math.cos(q * 6)
            g = max(2, int(S * 0.007))
            for j in (3, 2, 1):
                fd.rounded_rectangle([x - j * g, y0 - j * g, x + pw + j * g, y1 + j * g], radius=rad + j * g, outline=col + (int(pulse * 90 / j),), width=g)
        fd.rounded_rectangle([x, y0, x + pw, y1], radius=rad, fill=(10, 14, 28, A(225)), outline=col + (A(255),), width=max(3, int(S * 0.007)))
        mx = x + pw / 2; ly = y0 + S * 0.035
        for ln in sd["lab"]:
            fd.text((mx, ly), ln, font=v["f_lab"], fill=(232, 236, 245, A(255)), anchor="ma")
            ly += v["f_lab"].size * 1.15
        q = (lt - sd["at"] - 0.15) / 0.6
        if q > 0:
            cnt = ease_out(q); k_ = 0.6 + 0.4 * ease_back(min(1.0, q / 0.6))
            txt = count_text(sd["val"], cnt) if cnt < 0.999 else sd["val"]
            fv = _vs_font(v, ANTON, sd["vsz"] * k_)
            vy = (max(ly, y0 + (y1 - y0) * 0.30) + y1 - S * 0.03 - (len(sd["sub"]) * v["f_sub"].size * 1.2)) / 2
            fd.text((mx, vy), txt, font=fv, fill=col + (A(70),), stroke_width=int(S * 0.016), stroke_fill=col + (A(40),), anchor="mm")
            fd.text((mx, vy), txt, font=fv, fill=col + (A(255),), stroke_width=max(3, int(S * 0.006)), stroke_fill=(0, 0, 0, A(255)), anchor="mm")
            sy_ = y1 - S * 0.03 - len(sd["sub"]) * v["f_sub"].size * 1.2
            for ln in sd["sub"]:
                fd.text((mx, sy_), ln, font=v["f_sub"], fill=(190, 198, 212, A(255)), anchor="ma")
                sy_ += v["f_sub"].size * 1.2
    q = lt - v["vs_at"]
    if q > 0:  # VS badge slams in (big -> normal) between the panels
        s_ = 1.8 - 0.8 * ease_out(q / 0.18); r = v["badge_r"] * s_
        bx, by = v["cx"], (y0 + y1) / 2
        fd.ellipse([bx - r, by - r, bx + r, by + r], fill=(255, 77, 77, 255), outline=INK, width=max(3, int(S * 0.008)))
        fb = _vs_font(v, fun_font("Bangers-Regular.ttf"), r * 0.95)
        fd.text((bx, by), "VS", font=fb, fill=(255, 255, 255, 255), stroke_width=max(2, int(r * 0.07)), stroke_fill=INK, anchor="mm")


# ---------------- v6 CINEMA: camera, parallax, bokeh, light leaks, grading, motion blur ----------------
def camera_keys(si, dur, corner=False):
    """Camera keyframes every 1.2-1.5 s (no static framing longer than 1.5 s): alternating push-in / pull-out with drift,
    and roughly every third move is a stronger punch-in (seeded, eased)."""
    rng = np.random.default_rng(900 + si)
    zmax = 1.05 if corner else 1.10
    keys = []; t = 0.0; z = 1.0 + rng.uniform(0.02, 0.05); push = rng.random() < 0.5
    while t < dur + 2.0:
        px, py = (rng.uniform(-0.012, 0.0), rng.uniform(-0.008, 0.008)) if corner else (rng.uniform(-0.016, 0.016), rng.uniform(-0.012, 0.012))
        keys.append((t, z, px, py))
        t += rng.uniform(1.2, 1.5)
        step = rng.uniform(0.045, 0.065) if (push and rng.random() < 0.35) else rng.uniform(0.018, 0.038)
        z = min(zmax, max(1.012, z + (step if push else -step)))
        if rng.random() < 0.7: push = not push
    return keys


def cam_at(keys, lt):
    for (t0, z0, x0, y0), (t1, z1, x1, y1) in zip(keys, keys[1:]):
        if lt < t1:
            u = max(0.0, (lt - t0) / (t1 - t0)); u = u * u * (3 - 2 * u)
            return z0 + (z1 - z0) * u, x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
    return keys[-1][1:]


def cam_xform(img, z, px, py):
    """Virtual camera: zoom z (>= ~1) and pan (fractions of the frame), clamped so no empty edges appear."""
    W, H = img.size
    if abs(z - 1) < 1e-3 and abs(px) < 1e-4 and abs(py) < 1e-4: return img
    w, h = W / z, H / z
    x0 = W / 2 + px * W - w / 2; y0 = H / 2 + py * H - h / 2
    if z >= 1: x0 = min(max(x0, 0.0), W - w); y0 = min(max(y0, 0.0), H - h)
    return img.transform((W, H), Image.EXTENT, (x0, y0, x0 + w, y0 + h), Image.BILINEAR)


def bokeh_sprites(S):
    """Soft out-of-focus discs (brighter rim) for the near parallax layer."""
    out = []
    for r, col in ((S * 0.025, (255, 224, 150)), (S * 0.04, (255, 236, 190)), (S * 0.06, (255, 210, 120)), (S * 0.085, (210, 225, 255))):
        R_ = int(r); size = int(R_ * 2.8); im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = size / 2
        d.ellipse([c - R_, c - R_, c + R_, c + R_], fill=col + (95,))
        d.ellipse([c - R_ * 0.86, c - R_ * 0.86, c + R_ * 0.86, c + R_ * 0.86], fill=col + (55,))
        out.append(im.filter(ImageFilter.GaussianBlur(max(1, R_ * 0.12))))
    return out


def light_leak(W, H):
    """Warm anamorphic light leak (left version; flipped for the right)."""
    h = int(H * 0.7); yy, xx = np.mgrid[0:h, 0:W].astype(np.float32)
    d = np.sqrt(((xx - 0) / (W * 0.75)) ** 2 + ((yy - h * 0.45) / (h * 0.55)) ** 2)
    a = np.clip(1 - d, 0, 1) ** 2 * 95
    arr = np.zeros((h, W, 4), np.uint8); arr[..., 0] = 255; arr[..., 1] = 150; arr[..., 2] = 70; arr[..., 3] = a.astype(np.uint8)
    im = Image.fromarray(arr, "RGBA"); return im, im.transpose(Image.FLIP_LEFT_RIGHT)


_ALPHA_CACHE = {}


def _alpha_scaled(img, k, key):
    q = round(max(0.0, min(1.0, k)) * 12) / 12
    ck = (key, q)
    if ck not in _ALPHA_CACHE:
        if len(_ALPHA_CACHE) > 300: _ALPHA_CACHE.clear()
        im2 = img.copy(); im2.putalpha(img.split()[3].point(lambda v: int(v * q))); _ALPHA_CACHE[ck] = im2
    return _ALPHA_CACHE[ck]


def near_layer(W, H, bok, pts, t, lt, leak, si):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); used = False
    for (x, y, k, a, ph) in pts:
        sp = bok[k]
        yy = (y - t * H * 0.012 * (1 + k * 0.35)) % (H + 300) - 150
        xx = x + math.sin(t * 0.5 + ph) * W * 0.02
        al = a * (0.55 + 0.45 * math.sin(t * 1.3 + ph))
        if al > 0.08:
            paste_rgba(lay, _alpha_scaled(sp, al, ("bok", k)), xx - sp.width / 2, yy - sp.height / 2); used = True
    if leak is not None and lt < 0.45:
        lk = leak[si % 2]; k_ = (1 - lt / 0.45) ** 1.8
        paste_rgba(lay, _alpha_scaled(lk, k_, ("leak", si % 2)), 0, H * (0.05 if si % 2 else 0.3)); used = True
    return lay if used else None


class CineGrade:
    """Film look: radial lens fringing, soft bloom, S-curve with teal shadows / warm highlights, film grain."""
    def __init__(self, W, H):
        x = np.arange(256) / 255.0; k = 0.9
        y = 0.5 + 0.5 * np.tanh(k * (2 * x - 1)) / np.tanh(k); y = 0.012 + y * 0.988
        sh = 4 * y * (1 - y) ** 2; hl = 4 * y ** 2 * (1 - y)
        to = lambda a: [int(v) for v in np.clip(np.round(a * 255), 0, 255)]
        self.lut = to(y + 0.03 * hl - 0.018 * sh) + to(y + 0.004 * hl + 0.006 * sh) + to(y - 0.03 * hl + 0.04 * sh)
        self.bloom = [int(max(0, v - 200) * 1.5) for v in range(256)] * 3
        self.W, self.H = W, H
        rng = np.random.default_rng(77)
        self.grains = [np.clip(rng.normal(0, 3.0, (H, W, 1)), -10, 10).astype(np.int16) for _ in range(4)]

    def scene(self, im):
        W, H = self.W, self.H; rgb = im.convert("RGB"); e = 0.0022
        r_, g_, b_ = rgb.split()
        r_ = r_.transform((W, H), Image.EXTENT, (W * e, H * e, W * (1 - e), H * (1 - e)), Image.BILINEAR)
        b_ = b_.transform((W, H), Image.EXTENT, (-W * e, -H * e, W * (1 + e), H * (1 + e)), Image.BILINEAR)
        rgb = Image.merge("RGB", (r_, g_, b_))
        glow = rgb.resize((W // 6, H // 6), Image.BILINEAR).point(self.bloom).filter(ImageFilter.GaussianBlur(4))
        rgb = ImageChops.add(rgb, glow.resize((W, H), Image.BILINEAR)).point(self.lut)
        return rgb.convert("RGBA")

    def grain(self, rgb, fi):
        a = np.asarray(rgb, dtype=np.int16) + self.grains[fi % 4]
        return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


_SHUTTER = (-0.25, -0.125, 0.0, 0.125, 0.25)  # sub-frame offsets (frames) = 180° shutter, 5 samples


def _avg(imgs):
    out = imgs[0]
    for k, im in enumerate(imgs[1:], 2): out = Image.blend(out, im, 1.0 / k)
    return out


def mblur_patch(p, vx, vy, n=5):
    """Directional motion blur of an RGBA sprite (premultiplied average of shifted copies). Returns (img, (padx, pady))."""
    pad_x, pad_y = int(abs(vx) / 2) + 1, int(abs(vy) / 2) + 1
    a = np.asarray(p, dtype=np.float32) / 255.0; a[..., :3] *= a[..., 3:4]
    h_, w_ = a.shape[:2]; acc = np.zeros((h_ + 2 * pad_y, w_ + 2 * pad_x, 4), np.float32)
    for k in range(n):
        f = k / (n - 1) - 0.5; ox, oy = int(round(pad_x + f * vx)), int(round(pad_y + f * vy))
        acc[oy:oy + h_, ox:ox + w_] += a
    acc /= n; al = acc[..., 3:4]
    rgb = np.where(al > 1e-4, acc[..., :3] / np.maximum(al, 1e-4), 0)
    return Image.fromarray(np.clip(np.concatenate([rgb, al], axis=2) * 255, 0, 255).astype(np.uint8), "RGBA"), (pad_x, pad_y)


def _act_off(act, a_lt, mx, my, mR):
    if act == "roll_in" and a_lt < 0.7: return -(1 - ease_out(max(0.0, a_lt) / 0.7)) * (mx + mR * 2.5), 0.0
    if act == "drop_in" and a_lt < 0.45: return 0.0, -(1 - ease_out(max(0.0, a_lt) / 0.45) ** 2) * (my + mR * 3)
    return 0.0, 0.0


def render(spec, wav, total, out, workdir):
    long = spec.get("format") == "long"
    W, H = (1920, 1080) if long else (1080, 1920)
    S = min(W, H)
    ROC = spec.get("style") == "rocco"  # v6.12: Red Flag Rocco look - case-file tabs, typewriter, red stamps, label captions, phone SMS
    f_head = ImageFont.truetype(fun_font("CourierPrime-Bold.ttf") if ROC else ANTON, int(S * (0.075 if long else (0.088 if ROC else 0.105))))
    f_stamp = ImageFont.truetype(fun_font("BlackOpsOne-Regular.ttf"), int(S * 0.17)) if ROC else None
    f_phone = ImageFont.truetype(INTER_SB, int(S * 0.044)); f_phone_b = ImageFont.truetype(INTER_XB, int(S * 0.036))
    ACC = (255, 59, 59) if ROC else GOLD
    cap_sz = int(S * (0.05 if long else 0.07))
    f_cap = ImageFont.truetype(INTER_XB, cap_sz)
    f_cap_big = ImageFont.truetype(INTER_XB, int(cap_sz * 1.12))
    f_stat = ImageFont.truetype(ANTON, int(S * (0.22 if long else 0.30)))
    f_src = ImageFont.truetype(INTER_SB, int(S * 0.030))   # v6.4: was 0.024 — unreadable on a phone
    f_brand = ImageFont.truetype(ANTON, int(S * 0.04))
    f_lbl = ImageFont.truetype(INTER_XB, int(S * 0.04))
    f_val = ImageFont.truetype(ANTON, int(S * 0.06))
    nframes = int(math.ceil(total * FPS))
    caps = []
    for sc in spec["scenes"]:
        sp0 = sc.get("speech", sc["start"])
        if sc.get("text", "").strip():
            caps += (caption_chunks_timed(sc["text"], sc["words"]) if sc.get("words") else
                     caption_chunks(sc["text"], sp0, sc.get("sdur", sc["dur"] - (sp0 - sc["start"])) + 0.1))
    bgs = {}
    rng = np.random.default_rng(5)
    # floating "$" particles for the animated background (shared, drift upward forever)
    parts = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(25, 70), rng.uniform(0.03, 0.08) * S, rng.uniform(0, 6.28)) for _ in range(14)]
    f_part = {}
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", wav,
                            "-vf", "scale=in_range=full:in_color_matrix=bt709:out_range=tv:out_color_matrix=bt709",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-maxrate", ("12M" if not long else "2M"), "-bufsize", ("24M" if not long else "4M"), "-pix_fmt", "yuv420p",   # v6.5: was veryfast/crf 20, untagged colour; v6.5.1 (2026-11-21): bitrate cap — crf16 alone gave 111 MB Shorts (> GitHub 100 MB), cap keeps a 35 s Short <= ~55 MB and long video <= 100 MB
                            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                            "-af", "highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2,loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                            "-shortest", "-movflags", "+faststart", out + ".tmp.mp4"], stdin=subprocess.PIPE)
    # cinematic vignette (pro look), precomputed once
    yy, xx = np.mgrid[0:H, 0:W]
    rr = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    vig = Image.fromarray(np.clip((rr - 0.75) * 200, 0, 140).astype(np.uint8), "L")
    vignette = Image.new("RGBA", (W, H), (0, 0, 0, 255)); vignette.putalpha(vig)
    del yy, xx, rr
    trans_cycle = ["punch", "flash", "slide"]
    first_frame = None
    use3d = spec.get("buck3d", True) and any(s.get("mascot") for s in spec["scenes"]) and buck3d_ready()
    cinema = spec.get("cinema", True)
    cg = CineGrade(W, H) if cinema else None
    bok = bokeh_sprites(S) if cinema else None
    leak = light_leak(W, H) if cinema else None
    bg_bright = max(0.6, min(2.0, float(spec.get("bg_bright", 1.0))))  # v6.9
    for si, sc in enumerate(spec["scenes"]):
        f0 = int(round(sc["start"] * FPS)); f1 = min(nframes, int(round((sc["start"] + sc["dur"]) * FPS)))
        n = max(1, f1 - f0)
        clip, csz = (broll_frames(sc["broll"], W, H, n, sc.get("broll_start", 0)) if sc.get("broll") and os.path.exists(sc["broll"]) else (None, None))
        bdclip = None
        if not clip:
            if si % 3 not in bgs:
                bgs[si % 3] = make_bg(W, H, si % 3, pick_theme(spec))
                if bg_bright != 1.0:  # v6.9: A/B "bright" look (notes/2026-11-21_color.md) - lifts the theme gradient
                    _rgb = ImageEnhance.Brightness(bgs[si % 3].convert("RGB")).enhance(bg_bright)
                    bgs[si % 3] = _rgb.convert("RGBA")
            base_static = bgs[si % 3]
            _bd = sc.get("bg", spec.get("bg"))  # v6.6: str or list of clips/photos; scene "bg": false = plain theme
            if isinstance(_bd, list) and _bd: _bd = _bd[si % len(_bd)]
            if isinstance(_bd, str) and os.path.exists(_bd):
                bdclip, bdsz = backdrop_frames(_bd, W, H, n, sc.get("bg_start", (si * 3.7) % 9), spec.get("bg_blur", 6))
                bd_mix = float(spec.get("bg_mix", 0.62))  # share of the real picture vs theme colour
        col = hex2rgb(sc.get("color", "#FF3B3B" if spec.get("style") == "rocco" else "#F5C542"))
        trans = sc.get("transition") or ("punch" if sc.get("stat") else trans_cycle[si % 3])
        stat_sz = f_stat.size
        if sc.get("stat"):
            _m = ImageDraw.Draw(Image.new("RGB", (8, 8)))
            while stat_sz > 40 and _m.textlength(sc["stat"], font=ImageFont.truetype(ANTON, stat_sz)) > W * 0.84:
                stat_sz = int(stat_sz * 0.92)
        chart = sc.get("chart")  # {"labels": [...], "values": [...], "texts": [...]}
        vsd = prep_vs(sc["vs"], W, H, S, long) if sc.get("vs") else None  # v4.1 split-screen comparison
        coins = []
        if "coin_rain" in sc.get("fx", []):
            crng = np.random.default_rng(100 + si)
            coins = [(crng.uniform(0.05, 0.95) * W, crng.uniform(-0.6, 0) * H, crng.uniform(0.5, 1.0) * H, crng.uniform(0.025, 0.05) * S, crng.uniform(3, 8)) for _ in range(18)]
        arrow = next((a for a in sc.get("fx", []) if a in ("arrow_up", "arrow_down")), None)
        # ---- v3 humor pack: mascot, bubble, sticker ----
        masc = sc.get("mascot"); bub = None
        if masc:
            mood = masc.get("mood", "happy") if masc.get("mood", "happy") in MOODS else "happy"
            mpos = masc.get("pos") or ("corner" if (sc.get("stat") or sc.get("chart") or sc.get("vs") or clip or sc.get("phone")) else "center")
            m_at = float(masc.get("at", 0))
            if mpos == "center":
                mR = H * 0.13 if long else W * 0.17; mx, my = W * 0.5, H * 0.47
            else:
                # corner = upper-left, between the headline and the big stat (keeps the stat and captions clear)
                mR = H * 0.08 if long else W * 0.085; mx, my = (W * 0.11, H * 0.60) if long else (W * 0.15, H * 0.285)
                if use3d:  # keep the whole sprite (raised gloves, hat) inside the frame
                    sz_ = int(mR * 4.6); ex_ = buck3d_extent(mood, sz_)
                    if ex_: mx = max(mx, W * 0.015 + sz_ / 2 - ex_[0])
            if sc.get("buck") and not masc.get("say"): masc["say"] = sc["buck"]
            bub_at = (sc.get("buck_t", sc["start"]) - sc["start"]) if sc.get("buck") else (m_at + 0.25)
            if masc.get("say"):
                if mpos == "center":
                    bub = bubble_patch(masc["say"], S * 0.05, W * (0.6 if long else 0.8), "down")
                    bub_xy = (W / 2 - bub.width / 2, my - mR * 1.38 - bub.height)
                else:
                    bx0 = mx + mR * 1.3
                    bub = bubble_patch(masc["say"], S * 0.04, (W * 0.84 - bx0), "left")
                    bub_xy = (bx0, my - mR * 0.35 - bub.height / 2)
        stk = None
        if sc.get("sticker"):
            big = not (sc.get("stat") or chart or masc or vsd)
            stk = sticker_patch(sc["sticker"], S * (0.13 if big else 0.085), hex2rgb(sc.get("sticker_color", "#FF4D4D")))
            stk_c = (W / 2, H * (0.42 if big else (0.27 if not long else 0.24))); stk_at = float(sc.get("sticker_at", 0))
            if long and not big and not vsd:  # v6.2: 16:9 has room at the side — keep stickers off the headline and Buck's hat
                stk_c = (W * 0.75, H * 0.42)
        look = sc.get("look"); shake = float(sc.get("shake", 0))
        # ---- v4.1 reaction crash-zoom: focus point + timing ----
        zm = sc.get("zoom")
        if zm:
            z_amt = float(zm.get("amt", 1.25)); z_at = float(zm.get("at", 0)); z_hold = float(zm.get("hold", 0.8))
            z_on = zm.get("on", "buck" if masc else "center")
            if isinstance(z_on, (list, tuple)): z_fc = (float(z_on[0]) * W, float(z_on[1]) * H)
            elif z_on == "buck" and masc: z_fc = (mx, my - mR * 0.25)
            elif z_on == "stat" and sc.get("stat"): z_fc = (W / 2, H * (0.36 if not long else 0.30) + stat_sz * 0.6)
            elif z_on == "sticker" and stk is not None: z_fc = stk_c
            else: z_fc = (W / 2, H / 2)
        # ---- v6 cinema: camera path + near-layer particles for this scene ----
        cam_keys = camera_keys(si, sc["dur"], corner=bool(masc) and mpos == "corner") if (cinema and spec.get("camera", True) and sc.get("cam", True)) else None
        nprng = np.random.default_rng(300 + si)
        near_pts = [(nprng.uniform(0, W), nprng.uniform(0, H), int(nprng.integers(0, 4)), nprng.uniform(0.3, 1.0), nprng.uniform(0, 6.28)) for _ in range(8)] if cinema else []
        # chart line of the background draws itself across each scene
        lrng = np.random.default_rng(7 + si); v = 0; line_pts = []
        for i in range(31):
            v += lrng.uniform(-0.5, 1.0) if arrow != "arrow_down" else lrng.uniform(-1.0, 0.5)
            line_pts.append((i * W / 30, H * 0.74 - v * H * 0.012))
        for k in range(n):
            fi = f0 + k; t = fi / FPS; lt = k / FPS; prog = k / max(1, n - 1)
            # ---------- background ----------
            if clip:
                BW, BH = csz
                fr = Image.frombytes("RGB", (BW, BH), clip[min(k, len(clip) - 1)])
                z = 1.0 + 0.06 * prog  # Ken Burns push-in
                cw, ch = int(BW / z / 1.1 * 1.0), int(BH / z / 1.1)
                cx0 = (BW - cw) // 2 + int((BW - cw) * 0.15 * (prog - 0.5)); cy0 = (BH - ch) // 2
                base = fr.crop((cx0, cy0, cx0 + cw, cy0 + ch)).resize((W, H), Image.BILINEAR).convert("RGBA")
                base = ImageEnhance.Color(ImageEnhance.Contrast(base.convert("RGB")).enhance(1.12)).enhance(1.15).convert("RGBA")
                base = Image.alpha_composite(base, Image.new("RGBA", (W, H), (0, 0, 0, 105)))
            elif bdclip:
                BW2, BH2 = bdsz
                fr = Image.frombytes("RGB", (BW2, BH2), bdclip[min(k, len(bdclip) - 1)])
                cw, ch = int(BW2 / 1.12), int(BH2 / 1.12)
                dx = int((BW2 - cw) * (0.5 + 0.45 * math.sin(si * 1.7 + prog * 1.2) * 0.9)); dy = int((BH2 - ch) * (0.5 + 0.4 * (prog - 0.5)))
                bd = fr.crop((dx, dy, dx + cw, dy + ch)).resize((W, H), Image.BILINEAR)
                bd = ImageEnhance.Color(bd).enhance(0.85)
                base = Image.blend(base_static.convert("RGB"), bd, bd_mix).convert("RGBA")
                _lum = float(np.asarray(fr.convert("L"), dtype=np.float32).mean())  # bright backdrops (sky, white walls) get darker
                _dk = int(max(70, min(185, 70 + (_lum - 70) * 1.3 + (35 if (chart or vsd) else 0))))
                if bg_bright != 1.0: _dk = int(max(30, _dk / bg_bright))  # v6.9: less dimming of the real backdrop
                base = Image.alpha_composite(base, Image.new("RGBA", (W, H), (0, 0, 0, _dk)))
            else:
                base = base_static.copy()
                ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); o = ImageDraw.Draw(ov)
                # moving light sweep
                sx = (-0.4 + 1.8 * ((t * 0.18) % 1.0)) * W
                o.polygon([(sx, 0), (sx + W * 0.18, 0), (sx - W * 0.22, H), (sx - W * 0.4, H)], fill=(255, 255, 255, 9))
                # self-drawing chart line with glow
                upto = max(2, int(len(line_pts) * ease_out(prog * 1.4)))
                lc = (43, 214, 123) if arrow != "arrow_down" else (255, 77, 77)
                o.line(line_pts[:upto], fill=lc + (40,), width=max(10, W // 90), joint="curve")
                o.line(line_pts[:upto], fill=lc + (110,), width=max(4, W // 270), joint="curve")
                # floating $ particles
                for (px, py, spd, sz, ph) in parts:
                    yy = (py - spd * t * 2.2) % (H + 200) - 100
                    xx = px + math.sin(t * 0.8 + ph) * 25
                    key = int(sz)
                    if key not in f_part: f_part[key] = ImageFont.truetype(ANTON, key)
                    o.text((xx, yy), "$", font=f_part[key], fill=(245, 197, 66, 26))
                base = Image.alpha_composite(base, ov)
            if look == "sepia":  # old-film look for "legend says..." beats
                g = ImageOps.grayscale(base.convert("RGB"))
                base = ImageOps.colorize(g, black=(26, 17, 8), white=(240, 220, 180)).convert("RGBA")
                base = ImageEnhance.Brightness(base).enhance(1 + 0.05 * math.sin(fi * 2.3))
                if (fi * 7) % 23 < 3:  # occasional film scratch
                    sd = ImageDraw.Draw(base); xs = (fi * 137) % W
                    sd.line([(xs, 0), (xs + 6, H)], fill=(250, 240, 210, 255), width=2)
            im = base; d = ImageDraw.Draw(im)
            fx = Image.new("RGBA", (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fx)
            # v4.1: in zoom scenes captions/brand/progress go on their own layer so the camera move doesn't crop them
            ui = Image.new("RGBA", (W, H), (0, 0, 0, 0)) if (zm or cinema) else None
            ud = ImageDraw.Draw(ui) if ui is not None else fd
            # ---------- coin rain ----------
            for (cx, cy0, spd, r, spin) in coins:
                yy = cy0 + spd * lt * 1.2
                if -r < yy < H + r:
                    if cinema:  # motion streak behind each falling coin
                        xs_ = cx + math.sin(lt * 2 + cx) * 12
                        fd.ellipse([xs_ - r * 0.42, yy - r * 2.8, xs_ + r * 0.42, yy], fill=(255, 214, 90, 34))
                    draw_coin(fd, cx + math.sin(lt * 2 + cx) * 12, yy, r, math.cos(lt * spin + cx), 230)
            # ---------- animated bar chart ----------
            if chart:
                vals = chart["values"]; labels = chart.get("labels", [""] * len(vals)); texts = chart.get("texts")
                nb = len(vals); vmax = max(vals) or 1
                area_w = W * (0.72 if long else 0.66); bw = area_w / nb * 0.55; gap = area_w / nb
                x0 = (W - area_w) / 2 - (0 if long else W * 0.03); ybase = H * (0.60 if not long else 0.68); hmax = H * (0.24 if not long else 0.36)
                for i, v in enumerate(vals):
                    b_at = chart.get("at") or [0.25 + 0.25 * j for j in range(nb)]; b_len = 0.5 if chart.get("at") else 0.8
                    _lim = max(0.6, sc["dur"] - 0.7)  # v6.10: the last bar must finish >= 0.7 s before the cut (airport_cap b3 never showed +15%)
                    if max(b_at) + b_len > _lim:
                        _k = max(0.2, (_lim - b_len) / max(max(b_at), 1e-3)); b_at = [x * _k for x in b_at]
                    p = ease_out((lt - b_at[i]) / b_len)
                    h = hmax * (v / vmax) * p
                    bx = x0 + i * gap + (gap - bw) / 2
                    cc = col if i == chart.get("hi", nb - 1) else (120, 130, 150)  # v6.5: "hi" = highlighted bar index (default last)
                    fd.rounded_rectangle([bx, ybase - h, bx + bw, ybase], radius=int(bw * 0.12), fill=cc + (255,))
                    if p > 0.05:
                        txt = (texts[i] if texts and p >= 0.999 else count_text(texts[i], p)) if texts else f"{v * p:.2f}"
                        tw = fd.textlength(txt, font=f_val)
                        fd.text((bx + bw / 2 - tw / 2, ybase - h - f_val.size * 1.25), txt, font=f_val, fill=(255, 255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0, 255))
                    lw = fd.textlength(labels[i], font=f_lbl)
                    fd.text((bx + bw / 2 - lw / 2, ybase + S * 0.015), labels[i], font=f_lbl, fill=(220, 225, 235, 255), stroke_width=3, stroke_fill=(0, 0, 0, 255))
            # ---------- v4.1 split-screen VS ----------
            if vsd: draw_vs(fd, vsd, lt)
            # ---------- stat: count-up + overshoot punch ----------
            if sc.get("stat") and not chart and not vsd and ROC:  # red rubber stamp slams down
                p_in = (lt - 0.12) / 0.22
                if p_in > 0:
                    k_ = 1.0 + 0.7 * (1 - ease_out(min(1.0, p_in)))
                    txt = sc["stat"]; tw_ = int(fd.textlength(txt, font=f_stamp)); th_ = int(f_stamp.size * 1.25)
                    pad = int(S * 0.035); st_im = Image.new("RGBA", (tw_ + pad * 2, th_ + pad * 2), (0, 0, 0, 0)); sd_ = ImageDraw.Draw(st_im)
                    sd_.rounded_rectangle([4, 4, st_im.width - 5, st_im.height - 5], radius=int(S * 0.02), outline=col + (235,), width=int(S * 0.012))
                    sd_.text((pad, pad - f_stamp.size * 0.08), txt, font=f_stamp, fill=col + (240,))
                    rng_ = np.random.default_rng(si)  # ink texture: a few worn specks
                    for _ in range(40):
                        x_, y_ = rng_.uniform(0, st_im.width), rng_.uniform(0, st_im.height); r_ = rng_.uniform(1, S * 0.006)
                        sd_.ellipse([x_ - r_, y_ - r_, x_ + r_, y_ + r_], fill=(0, 0, 0, 0))
                    st_im = st_im.rotate(-7, expand=True, resample=Image.BICUBIC)
                    if abs(k_ - 1) > 1e-3: st_im = st_im.resize((int(st_im.width * k_), int(st_im.height * k_)), Image.BILINEAR)
                    if st_im.width > W * 0.88: st_im = st_im.resize((int(W * 0.88), int(st_im.height * W * 0.88 / st_im.width)), Image.LANCZOS)
                    paste_rgba(fx, st_im, (W - st_im.width) / 2, H * (0.46 if masc else 0.40) - st_im.height / 2)  # below a corner mascot
            elif sc.get("stat") and not chart and not vsd:
                p_in = (lt - 0.15) / 0.45
                if p_in > 0:
                    sc_k = 0.6 + 0.4 * ease_back(p_in)
                    cnt = ease_out((lt - 0.15) / 0.7)
                    txt = count_text(sc["stat"], cnt) if cnt < 0.999 else sc["stat"]
                    fs = ImageFont.truetype(ANTON, max(10, int(stat_sz * sc_k)))
                    tw = fd.textlength(txt, font=fs)
                    sy = H * (0.36 if not long else 0.30) + (stat_sz - fs.size) * 0.5
                    # soft glow
                    fd.text(((W - tw) / 2, sy), txt, font=fs, fill=col + (60,), stroke_width=22, stroke_fill=col + (40,))
                    fd.text(((W - tw) / 2, sy), txt, font=fs, fill=col + (255,), stroke_width=7, stroke_fill=(0, 0, 0, 255))
                    if arrow:
                        a = ease_out((lt - 0.5) / 0.4)
                        if a > 0:
                            ac = (43, 214, 123) if arrow == "arrow_up" else (255, 77, 77)
                            ax = W * 0.5; ay = sy - S * 0.08 - (S * 0.05 * (1 - a)) * (1 if arrow == "arrow_up" else -1)
                            s2 = S * 0.06
                            pts = [(ax, ay - s2), (ax - s2, ay + s2 * 0.2), (ax + s2, ay + s2 * 0.2)] if arrow == "arrow_up" else [(ax, ay + s2), (ax - s2, ay - s2 * 0.2), (ax + s2, ay - s2 * 0.2)]
                            fd.polygon(pts, fill=ac + (int(255 * a),))
            # ---------- headline: drop-in with overshoot + underline sweep ----------
            if sc.get("head") and not (ROC and clip and si > 0):  # Rocco: full-screen footage scenes carry no headline
                lh_t = lt + (0.4 if si == 0 else 0.0)  # hook: headline fully visible on frame 1 (works with sound off)
                a = ease_back(lh_t / 0.4) if lh_t < 0.4 else 1.0
                al = int(255 * min(1.0, lh_t / 0.2))
                lines = wrap(fd, sc["head"], f_head, W * 0.86)
                lh = f_head.size * 1.08
                y0 = (H * 0.815 + (1 - a) * 70) if ROC else (H * (0.095 if not long else 0.075) - (1 - a) * 70)  # Rocco: case-file tab at the bottom
                boxh = lh * len(lines) + S * 0.04
                if ROC:  # manila case-file tab, typewriter text, left aligned
                    fd.rectangle([W * 0.05, y0 - S * 0.045, W * 0.32, y0 - S * 0.015], fill=(205, 170, 96, al))
                    fd.rectangle([W * 0.05, y0 - S * 0.02, W * 0.95, y0 + boxh - S * 0.02], fill=(222, 190, 120, al))
                    fd.text((W * 0.065, y0 - S * 0.045), "CASE FILE", font=f_src, fill=(70, 50, 25, al))
                    for li, ln in enumerate(lines):
                        fd.text((W * 0.08, y0 + li * lh), ln, font=f_head, fill=(28, 24, 20, al))
                else:
                    fd.rounded_rectangle([W * 0.05, y0 - S * 0.02, W * 0.95, y0 + boxh - S * 0.02], radius=int(S * 0.025), fill=(0, 0, 0, int(175 * al / 255)))
                    for li, ln in enumerate(lines):
                        tw = fd.textlength(ln, font=f_head)
                        fd.text(((W - tw) / 2, y0 + li * lh), ln, font=f_head, fill=col + (al,))
                u = ease_out((lh_t - 0.2) / 0.5)
                if u > 0:
                    uw = W * 0.5 * u
                    by = y0 + boxh - S * 0.02  # underline sits just below the headline box
                    fd.rectangle([W / 2 - uw / 2, by + S * 0.008, W / 2 + uw / 2, by + S * 0.016], fill=(ACC if ROC else col) + (255,))
            # ---------- v3: Buck the coin + speech bubble + sticker ----------
            if masc and lt >= m_at:
                m_lt = lt - m_at; act = masc.get("act"); act_lt = m_lt - float(masc.get("act_at", 0))
                ox_, oy_ = 0.0, 0.0
                if act == "roll_in" and act_lt < 0.7:  # rolls in on his edge from the left, then wobbles
                    pr_ = ease_out(max(0.0, act_lt) / 0.7); ox_ = -(1 - pr_) * (mx + mR * 2.5)
                elif act == "drop_in" and act_lt < 0.45:  # falls in from above and squashes
                    oy_ = -(1 - ease_out(max(0.0, act_lt) / 0.45) ** 2) * (my + mR * 3)
                mp = "missing"
                if use3d:
                    tk_ = talk_level(spec.get("_speech_env"), spec.get("_speech_words"), fi, t, spec.get("_mouth_cues"))
                    mp, (pax, pay) = mascot3d_patch(mR, mood, t, m_lt, act=act, act_lt=act_lt, talk=tk_)
                if isinstance(mp, str): mp, (pax, pay) = mascot_patch(mR, mood, t, m_lt, act=act, act_lt=act_lt)  # 2D fallback
                env_ = spec.get("_speech_env")
                if mp is not None and env_ and not (act in ACT_CLIP and 0 <= act_lt < ACT_CLIP[act][1]):
                    a_ = env_[min(fi, len(env_) - 1)]  # v6: Buck is talking -> squash & stretch on the syllables
                    if a_ > 0.15:
                        sy_ = 1 + 0.045 * a_; sx_ = 1 - 0.022 * a_
                        w2, h2 = max(1, int(mp.width * sx_)), max(1, int(mp.height * sy_))
                        im2 = Image.new("RGBA", mp.size, (0, 0, 0, 0))
                        paste_rgba(im2, mp.resize((w2, h2), Image.BILINEAR), (mp.width - w2) / 2, mp.height * b3_feet() - h2 * b3_feet())
                        mp = im2
                if mp is not None:
                    if act == "roll_in" and act_lt < 0.7: mp = mp.rotate(math.degrees(-ox_ / mR), resample=Image.BILINEAR, center=(pax, pay))
                    if cinema and act in ("roll_in", "drop_in") and 0 <= act_lt < 0.7:  # v6 motion blur on fast entrances
                        px0, py0 = _act_off(act, act_lt - 1 / FPS, mx, my, mR)
                        vx_, vy_ = (ox_ - px0) * 0.6, (oy_ - py0) * 0.6
                        if abs(vx_) + abs(vy_) > 3:
                            mp, (bpx, bpy) = mblur_patch(mp, vx_, vy_); pax += bpx; pay += bpy
                    paste_rgba(fx, mp, mx - pax + ox_, my - pay + oy_)
                if bub is not None:
                    bt = lt - bub_at
                    if bt > 0:
                        s_ = ease_back(bt / 0.25) if bt < 0.25 else 1.0
                        if s_ > 0.05:
                            bp = bub if abs(s_ - 1) < 1e-3 else bub.resize((max(1, int(bub.width * s_)), max(1, int(bub.height * s_))), Image.BILINEAR)
                            if mpos == "center": paste_rgba(fx, bp, W / 2 - bp.width / 2, bub_xy[1] + bub.height - bp.height)
                            else: paste_rgba(fx, bp, bub_xy[0], bub_xy[1] + (bub.height - bp.height) / 2)
            if stk is not None and lt >= stk_at:
                lts = lt - stk_at
                s_ = 1.8 - 0.8 * ease_out(lts / 0.18)
                sp_ = stk if abs(s_ - 1) < 1e-3 else stk.resize((max(1, int(stk.width * s_)), max(1, int(stk.height * s_))), Image.BILINEAR)
                jit = (math.sin(fi * 2.1) * S * 0.006 * max(0.0, 1 - lts / 0.4))
                paste_rgba(fx, sp_, stk_c[0] - sp_.width / 2 + jit, stk_c[1] - sp_.height / 2)
            # ---------- v6.12 phone: generic SMS screen, messages pop in (no real brand, no real number) ----------
            ph = sc.get("phone")
            if ph:
                pa = ease_back(min(1.0, lt / 0.3)) if lt < 0.3 else 1.0
                pw_, phh = W * 0.62 * pa, H * 0.44 * pa; px_, py_ = (W - pw_) / 2 + (W * 0.08 if masc else 0), H * 0.20
                fd.rounded_rectangle([px_ - S * 0.012, py_ - S * 0.012, px_ + pw_ + S * 0.012, py_ + phh + S * 0.012], radius=int(S * 0.06), fill=(18, 18, 22, 255))
                fd.rounded_rectangle([px_, py_, px_ + pw_, py_ + phh], radius=int(S * 0.05), fill=(150, 156, 170, 255))
                if pa > 0.95:
                    fd.rectangle([px_, py_ + S * 0.05, px_ + pw_, py_ + S * 0.11], fill=(186, 190, 202, 255))
                    hdr = ph.get("from", "Unknown number"); tw = fd.textlength(hdr, font=f_phone_b)
                    fd.text((px_ + (pw_ - tw) / 2, py_ + S * 0.062), hdr, font=f_phone_b, fill=(30, 30, 36, 255))
                    yy_ = py_ + S * 0.14
                    for mi, m_ in enumerate(ph.get("msgs", [])):
                        m_at = float(m_.get("at", 0.3 + 0.8 * mi)) if isinstance(m_, dict) else 0.3 + 0.8 * mi
                        mt = m_["t"] if isinstance(m_, dict) else m_
                        if lt < m_at: break
                        ma = ease_back(min(1.0, (lt - m_at) / 0.25))
                        ln_ = wrap(fd, mt, f_phone, pw_ * 0.72); bh_ = len(ln_) * f_phone.size * 1.25 + S * 0.03
                        bw_ = max(fd.textlength(l, font=f_phone) for l in ln_) + S * 0.04
                        flag = isinstance(m_, dict) and m_.get("flag") and lt > m_at + 0.6
                        fd.rounded_rectangle([px_ + S * 0.03, yy_, px_ + S * 0.03 + bw_ * ma, yy_ + bh_ * ma], radius=int(S * 0.03),
                                             fill=(226, 168, 168, 255) if flag else (196, 200, 210, 255), outline=(ACC + (255,)) if flag else None, width=int(S * 0.006))
                        if ma > 0.9:
                            for k_, l in enumerate(ln_): fd.text((px_ + S * 0.05, yy_ + S * 0.015 + k_ * f_phone.size * 1.25), l, font=f_phone, fill=(20, 20, 24, 255))
                        if flag:
                            fd.text((px_ + S * 0.03 + bw_ - S * 0.04, yy_ - S * 0.035), "!", font=f_head, fill=ACC + (255,), stroke_width=4, stroke_fill=(0, 0, 0, 255))
                        yy_ += bh_ + S * 0.025
            # ---------- karaoke captions ----------
            for cap in caps:
                c0, c1, txt = cap[:3]
                if c0 <= t < c1:
                    words = txt.split()
                    if len(cap) > 3:  # v6: exact word timing from Buck's audio
                        act = max([i for i, ws in enumerate(cap[3]) if ws <= t] or [0])
                    else:
                        wts = [len(w) + 1 for w in words]; tot = sum(wts); acc = 0; act = len(words) - 1
                        for i, w in enumerate(wts):
                            acc += w
                            if (t - c0) < (c1 - c0) * acc / tot: act = i; break
                    pop = ease_out((t - c0) / 0.1)
                    lines = karaoke_lines(ud, words, f_cap, W * (0.86 if long else 0.78))
                    yb = H * (0.645 if not long else 0.80) + (1 - pop) * 20
                    sp = ud.textlength(" ", font=f_cap)
                    for li, idxs in enumerate(lines):
                        widths = [ud.textlength(words[i], font=(f_cap_big if i == act else f_cap)) for i in idxs]
                        lw = sum(widths) + sp * (len(idxs) - 1); x = (W * (1.0 if long else 0.94) - lw) / 2
                        if ROC:  # black label strip behind each caption line
                            ud.rectangle([x - S * 0.02, yb + li * cap_sz * 1.2 - cap_sz * 0.08, x + lw + S * 0.02, yb + li * cap_sz * 1.2 + cap_sz * 1.12], fill=(12, 12, 14, int(225 * pop)))
                        for j, i in enumerate(idxs):
                            wd = words[i]; fnt = f_cap_big if i == act else f_cap
                            isnum = bool(re.search(r'[\d$¢%]', wd))
                            fill = GOLD if i == act else (GREEN if isnum else WHITE)
                            if ROC:
                                fill = WHITE if i == act else ((255, 214, 90) if isnum else (225, 228, 235))
                                if i == act: ud.rectangle([x - S * 0.006, yb + li * cap_sz * 1.2 - cap_sz * 0.1, x + widths[j] + S * 0.006, yb + li * cap_sz * 1.2 + cap_sz * 1.1], fill=ACC + (int(255 * pop),))
                            yy = yb + li * cap_sz * 1.2 - (cap_sz * 0.06 if i == act else 0)
                            ud.text((x, yy), wd, font=fnt, fill=fill + (int(255 * pop),), stroke_width=max(5, cap_sz // 9), stroke_fill=(0, 0, 0, int(255 * pop)))
                            x += widths[j] + sp
                    break
            # ---------- source, progress, brand ----------
            src_txt = sc["show_source"] if isinstance(sc.get("show_source"), str) else spec.get("source")  # 2026-11-20: per-scene source line (long videos cite many sources)
            if src_txt and sc.get("show_source"):
                fs_ = f_src; tw = ud.textlength(src_txt, font=fs_)
                if tw > W * 0.92:   # v6.4: shrink a long source line to fit instead of running off the frame
                    fs_ = ImageFont.truetype(INTER_SB, max(int(S * 0.020), int(S * 0.030 * W * 0.92 / tw))); tw = ud.textlength(src_txt, font=fs_)
                ud.text(((W - tw) / 2, H * (0.93 if long else (0.915 if ROC else 0.775))), src_txt, font=fs_, fill=(196, 204, 220, 255),
                        stroke_width=max(1, int(S * 0.002)), stroke_fill=(0, 0, 0, 200))
            ud.rectangle([0, 0, int(W * t / total), int(S * 0.009)], fill=ACC + (255,))
            ud.text(((W * 0.96 - ud.textlength(spec.get("brand", ""), font=f_brand)) if ROC else W * 0.04, (H - S * 0.07) if long else S * 0.03), spec.get("brand", "FINANCIER"), font=f_brand, fill=(hex2rgb(spec["brand_color"]) if spec.get("brand_color") else GOLD) + (150,))
            if cinema:  # v6: parallax — background 0.55x, content 1x, near bokeh 1.6x of the camera move
                cz, cpx, cpy = cam_at(cam_keys, lt) if cam_keys else (1.0, 0.0, 0.0)
                im = cam_xform(im, 1 + (cz - 1) * 0.55, cpx * 0.55, cpy * 0.55)
                im = Image.alpha_composite(im, cam_xform(fx, cz, cpx, cpy))
                nl = near_layer(W, H, bok, near_pts, t, lt, leak if (si > 0 and trans != "punch") else None, si)
                if nl is not None: im = Image.alpha_composite(im, cam_xform(nl, 1 + (cz - 1) * 1.6, cpx * 1.6, cpy * 1.6))
            else:
                im = Image.alpha_composite(im, vignette)
                im = Image.alpha_composite(im, fx)
            # ---------- v4.1 reaction crash-zoom (scene layer only; captions stay put) ----------
            if zm:
                def _zoomed(img, zz):
                    if zz <= 1.001: return img
                    zw, zh = W / zz, H / zz
                    zx0 = min(max(z_fc[0] - zw / 2, 0.0), W - zw); zy0 = min(max(z_fc[1] - zh / 2, 0.0), H - zh)
                    if masc and mpos == "corner" and z_on != "buck":  # two-shot framing: never crop a corner Buck
                        zx0 = min(zx0, max(0.0, mx - mR * 1.45)); zy0 = min(zy0, max(0.0, my - mR * 1.9))
                    return img.transform((W, H), Image.EXTENT, (zx0, zy0, zx0 + zw, zy0 + zh), Image.BILINEAR)
                zt_ = lt - z_at
                if cinema and (0 <= zt_ < 0.16 or (z_hold >= 0 and 0.14 + z_hold <= zt_ < 0.36 + z_hold)):  # v6 motion blur on the snap
                    im = _avg([_zoomed(im, zoom_amt(zt_ + o / FPS, z_amt, z_hold)) for o in _SHUTTER])
                else:
                    im = _zoomed(im, zoom_amt(zt_, z_amt, z_hold))
            if cinema:
                im = Image.alpha_composite(im, vignette)
                im = cg.scene(im)
            # ---------- scene transition ----------
            def _trans(img, lt_):
                q = max(0.0, lt_) / 0.22
                if trans == "punch":
                    zz = 1.0 + 0.09 * (1 - ease_out(q))
                    bw2, bh2 = int(W * zz), int(H * zz)
                    return img.resize((bw2, bh2), Image.BILINEAR).crop(((bw2 - W) // 2, (bh2 - H) // 2, (bw2 - W) // 2 + W, (bh2 - H) // 2 + H))
                if trans == "flash":
                    return Image.alpha_composite(img, Image.new("RGBA", (W, H), (255, 255, 255, int(150 * (1 - min(1.0, q))))))
                if trans == "slide":
                    off = int(W * 0.25 * (1 - ease_out(q)))
                    shifted = Image.new("RGBA", (W, H), (0, 0, 0, 255)); shifted.paste(img, (off, 0)); return shifted
                return img
            if si > 0 and lt < 0.22:
                if cinema and trans in ("punch", "slide"):  # v6: 5-sample motion blur through the cut (180° shutter)
                    im = _avg([_trans(im, lt + o / FPS) for o in _SHUTTER])
                else:
                    im = _trans(im, lt)
            if shake and lt < shake:
                def _shk(img, f_):
                    amp = S * 0.016 * max(0.0, 1 - (f_ - f0) / FPS / shake); z = 1.035
                    big_ = img.resize((int(W * z), int(H * z)), Image.BILINEAR)
                    ox = (big_.width - W) / 2 + amp * math.sin(f_ * 2.7); oy = (big_.height - H) / 2 + amp * math.cos(f_ * 3.9)
                    return big_.crop((int(ox), int(oy), int(ox) + W, int(oy) + H))
                if cinema: im = _avg([_shk(im, fi + o) for o in _SHUTTER])
                else: im = _shk(im, fi)
            if ui is not None: im = Image.alpha_composite(im, ui)  # captions / brand / progress: never moved or blurred
            frame = im.convert("RGB")
            if cinema: frame = cg.grain(frame, fi)
            if spec.get("loop"):
                if fi == 0: first_frame = frame.copy()
                elif fi >= nframes - 6 and first_frame is not None:
                    frame = Image.blend(frame, first_frame, (fi - (nframes - 6) + 1) / 7)
            enc.stdin.write(frame.tobytes())
    enc.stdin.close(); enc.wait()
    if enc.returncode == 0: os.replace(out + ".tmp.mp4", out)
    return enc.returncode


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "design-buck":
        ap = argparse.ArgumentParser(prog="make_video.py design-buck")
        ap.add_argument("cmd"); ap.add_argument("outdir"); ap.add_argument("--seed", type=int, default=4241)
        ap.add_argument("--no-save", action="store_true"); ap.add_argument("--force", action="store_true")
        a = ap.parse_args()
        design_buck(a.outdir, a.seed, save=not a.no_save, force=a.force); return
    if len(sys.argv) > 1 and sys.argv[1] == "buck-say":
        ap = argparse.ArgumentParser(prog="make_video.py buck-say")
        ap.add_argument("cmd"); ap.add_argument("text"); ap.add_argument("out")
        ap.add_argument("--model"); ap.add_argument("--voices")
        a = ap.parse_args()
        import soundfile as sf
        y = buck_line_el(a.text, tempfile.mkdtemp(prefix="fin_"), 0)
        if y is None:
            if not (a.model and a.voices): sys.exit(f"ElevenLabs failed ({_EL['why']}); pass --model/--voices for the Kokoro fallback")
            from kokoro_onnx import Kokoro
            y, _ = buck_line(Kokoro(a.model, a.voices), a.text, tempfile.mkdtemp(prefix="fin_"), 0)
        sf.write(a.out, y, 24000); print(json.dumps({"out": a.out, "buck_voice": _EL["used"]})); return
    ap = argparse.ArgumentParser()
    ap.add_argument("spec"); ap.add_argument("out")
    ap.add_argument("--model", required=True); ap.add_argument("--voices", required=True)
    args = ap.parse_args()
    spec = json.load(open(args.spec))
    workdir = tempfile.mkdtemp(prefix="fin_")
    wav, total = tts(spec, args, workdir)
    rc = render(spec, wav, total, args.out, workdir)
    import hashlib, datetime as _dt
    _sha = hashlib.sha1(open(os.path.abspath(__file__), "rb").read()).hexdigest()[:12]  # v6.9: freshness stamp (qc_gate step 0)
    print(json.dumps({"rc": rc, "seconds": round(total, 2), "out": args.out, "engine": ENGINE_VERSION, "engine_sha": _sha,
                      "rendered_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                      "buck_voice": sorted(set(_EL["used"])), "buck3d": _B3.get("ver"), "cinema": spec.get("cinema", True),
                      "timings": [[round(s["start"], 2), round(s["dur"], 2)] for s in spec["scenes"]]}))


if __name__ == "__main__":
    main()
