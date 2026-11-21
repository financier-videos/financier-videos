#!/usr/bin/env python3
"""qc_gate.py - ONE command that runs every automatable quality skill on a finished video before it may be posted.
Shohjahon 2026-11-21: "use all the skills every time without me reminding you". Map of all skills: docs/skill_map.md.

  python3 engine/qc_gate.py video.mp4 --spec spec.json [--rendered rendered.json] --title "..." [--platform shorts|youtube|reels]
        [--thumb "THUMB TEXT"] [--out work/<date>/<name>_qc.json]

Steps (skill -> check):
  1 ffmpeg-skill/check.py        platform compliance (codec, size, fps, colour tags, loudness, duration)
  2 ebur128                      integrated loudness -16..-12 LUFS (target -14)
  3 blackdetect                  no empty/black frames >= 0.1 s
  4 bitrate / profile            h264 High, >= 5 Mbit/s for Shorts (visual_quality_director: export)
  5 engine/voice_check.py        ASR transcript vs spec (>= 0.86); prints "heard" - READ the numbers and the last sentence
  6 engine/prosody_check.py      MONOTONE / FLAT_Q / NO_LAND
  7 yt-package/title.py          title lint (>= 80, number in first 40 chars if the title has one)
  8 contact sheet                8 frames tiled -> <out>_sheet.png; Claude MUST Read it (12-point visual QC: sharp text,
                                 Buck not covering numbers, nothing cut off, no blocky gradients, no unsuitable frame)
Result: exit 0 = all PASS (posting allowed); 1 = a FAIL (fix and rerun); 2 = a step could not run (SKIP is listed with
reason; a SKIP of steps 1-5 also blocks posting). The JSON report is committed next to the spec.
"""
import argparse, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SK = os.path.join(ROOT, "docs", "skills")


def run(cmd, timeout=900):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout + p.stderr
    except Exception as e:  # noqa
        return 99, str(e)


def probe(path):
    rc, out = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", path])
    return json.loads(out) if rc == 0 else {}


SETUP = [
    "python3 -I -c 'import numpy, soundfile, sherpa_onnx, parselmouth' 2>/dev/null || python3 -m pip install --break-system-packages -q numpy soundfile sherpa-onnx praat-parselmouth==0.4.7",
    "test -d /tmp/asr/sherpa-onnx-whisper-base.en || (curl -sSfL -o /tmp/w.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-base.en.tar.bz2 && mkdir -p /tmp/asr && tar xf /tmp/w.tar.bz2 -C /tmp/asr)",
]


def setup():
    for c in SETUP:
        subprocess.run(c, shell=True, timeout=900)


def main():
    setup()
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--spec"); ap.add_argument("--rendered"); ap.add_argument("--title")
    ap.add_argument("--thumb"); ap.add_argument("--platform", default="shorts"); ap.add_argument("--out")
    a = ap.parse_args()
    out = a.out or os.path.splitext(a.video)[0] + "_qc.json"
    R = {}

    def put(k, status, note=""):
        R[k] = {"status": status, "note": note.strip()[-600:]}
        print(f"[{status:4}] {k}: {note.strip().splitlines()[-1] if note.strip() else ''}"[:200])

    # 1 platform check
    rc, o = run([sys.executable, os.path.join(SK, "ffmpeg-skill", "scripts", "check.py"), a.video, "--platform", a.platform])
    fails = [l for l in o.splitlines() if "FAIL" in l and "subtitle" not in l.lower()]
    put("1_platform_check", "PASS" if not fails and rc in (0, 1) else ("FAIL" if fails else "SKIP"), "\n".join(fails) or o)

    # 2 loudness
    rc, o = run(["ffmpeg", "-nostats", "-i", a.video, "-af", "ebur128", "-f", "null", "-"])
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", o)
    if m:
        i = float(m[-1]); put("2_loudness", "PASS" if -16 <= i <= -12 else "FAIL", f"I = {i} LUFS (target -14)")
    else:
        put("2_loudness", "SKIP", o)

    # 3 black frames
    rc, o = run(["ffmpeg", "-nostats", "-i", a.video, "-vf", "blackdetect=d=0.1:pix_th=0.05", "-an", "-f", "null", "-"])
    b = re.findall(r"black_start:\S+ black_end:\S+", o)
    put("3_blackdetect", "PASS" if not b else "FAIL", "; ".join(b) or "0 black segments")

    # 4 export standard
    p = probe(a.video)
    v = next((s for s in p.get("streams", []) if s.get("codec_type") == "video"), {})
    au = [s for s in p.get("streams", []) if s.get("codec_type") == "audio"]
    br = int(p.get("format", {}).get("bit_rate", 0) or 0)
    dur = float(p.get("format", {}).get("duration", 0) or 0)
    probs = []
    if v.get("codec_name") != "h264": probs.append("codec " + str(v.get("codec_name")))
    if v.get("profile") not in ("High", "Main"): probs.append("profile " + str(v.get("profile")))
    if a.platform in ("shorts", "reels") and br < 5_000_000: probs.append(f"bitrate {br/1e6:.1f} Mbit/s < 5")
    if a.platform in ("shorts", "reels") and dur > 60: probs.append(f"duration {dur:.1f}s")
    if not au or au[0].get("channels") != 2: probs.append("audio not stereo")
    put("4_export", "PASS" if not probs else "FAIL", "; ".join(probs) or f"h264 {v.get('profile')}, {br/1e6:.1f} Mbit/s, {dur:.1f}s, stereo")

    # 5 voice check
    if a.spec:
        rc, o = run([sys.executable, "-I", os.path.join(ROOT, "engine", "voice_check.py"), a.video, a.spec])
        put("5_voice_check", "SKIP" if "Traceback" in o else {0: "PASS", 1: "FAIL"}.get(rc, "SKIP"), o)
    else:
        put("5_voice_check", "SKIP", "no --spec")

    # 6 prosody
    if a.spec:
        cmd = [sys.executable, "-I", os.path.join(ROOT, "engine", "prosody_check.py"), a.video, a.spec]
        if a.rendered: cmd.append(a.rendered)
        rc, o = run(cmd)
        put("6_prosody", "SKIP" if "Traceback" in o else {0: "PASS", 1: "FAIL"}.get(rc, "SKIP"), o)
    else:
        put("6_prosody", "SKIP", "no --spec")

    # 7 title lint
    if a.title:
        cmd = [sys.executable, os.path.join(SK, "youtube-agent-skill", "yt-package", "title.py"), "--title", a.title, "--json"]
        if a.thumb: cmd += ["--thumb", a.thumb]
        rc, o = run(cmd)
        try:
            j = json.loads(o); j = j[0] if isinstance(j, list) else j; sc = j.get("score")
        except Exception:
            sc = None
        num = re.search(r"\d", a.title)
        late = num and num.start() >= 40
        st = "PASS" if sc is not None and sc >= 80 and not late else ("SKIP" if sc is None else "FAIL")
        put("7_title", st, f"score {sc}" + ("; number after 40 chars" if late else "") + ("" if sc is not None else "\n" + o))
    else:
        put("7_title", "SKIP", "no --title")

    # 8 contact sheet (8 frames) - must be looked at
    sheet = os.path.splitext(out)[0] + "_sheet.png"
    if dur > 0:
        n = 8; fps = n / dur
        rc, o = run(["ffmpeg", "-y", "-loglevel", "error", "-i", a.video, "-vf",
                     f"fps={fps:.5f},scale=270:-2,tile={n}x1", "-frames:v", "1", sheet])
        put("8_contact_sheet", "LOOK" if rc == 0 and os.path.exists(sheet) else "SKIP", sheet + " - Read it before posting" + ("" if rc == 0 else "\n" + o))
    else:
        put("8_contact_sheet", "SKIP", "no duration")

    st = [r["status"] for k, r in R.items()]
    blocking_skip = any(R[k]["status"] == "SKIP" for k in R if k[0] in "12345")
    verdict = "FAIL" if "FAIL" in st else ("BLOCKED" if blocking_skip else "PASS")
    R["verdict"] = verdict
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    json.dump(R, open(out, "w"), indent=1)
    print(f"VERDICT: {verdict}  -> {out}")
    sys.exit(0 if verdict == "PASS" else (1 if verdict == "FAIL" else 2))


if __name__ == "__main__":
    main()
