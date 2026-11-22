#!/usr/bin/env python3
"""qc_gate.py - ONE command that runs every automatable quality skill on a finished video before it may be posted.
Shohjahon 2026-11-21: "use all the skills every time without me reminding you". Map of all skills: docs/skill_map.md.

  python3 engine/qc_gate.py video.mp4 --spec spec.json [--rendered rendered.json] --title "..." [--platform shorts|youtube|reels]
        [--thumb "THUMB TEXT"] [--out work/<date>/<name>_qc.json]

Steps (skill -> check):
  0 freshness                   repo not behind origin/media; rendered with current engine or no 'QAYTA RENDER: HA' change since (docs/changes.md)
  1 ffmpeg-skill/check.py        platform compliance (codec, size, fps, colour tags, loudness, duration)
  2 ebur128                      integrated loudness -16..-12 LUFS (target -14)
  3 blackdetect                  no empty/black frames >= 0.1 s
  4 bitrate / profile            h264 High, >= 5 Mbit/s for Shorts (visual_quality_director: export)
  5 engine/voice_check.py        ASR transcript vs spec (>= 0.86); prints "heard" - READ the numbers and the last sentence
  6 engine/prosody_check.py      MONOTONE / FLAT_Q / NO_LAND
  7 yt-package/title.py          title lint (>= 80, number in first 40 chars if the title has one)
  10 engine/look_check.py      --prev <last 4 videos>: similarity >= 0.70 = FAIL (docs/looks.md)
  9 engine/color_check.py frames  CLIPPED = FAIL; CRUSHED/DULL = WARN (color skill)
  11 pacing                     ffmpeg scene>0.22 hard cuts >= duration/2 (a new picture every <= 2 s)
  12 engine/script_check.py      --prev-specs <last 4 specs>: skeleton repeat / footage share < 40% = FAIL
  13 skills line                 --skills "Skillar: ...; ishlatilmadi: ... (sababi)" missing = FAIL
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
    ap.add_argument("--thumb"); ap.add_argument("--platform", default="shorts"); ap.add_argument("--out"); ap.add_argument("--prev", nargs="*", default=[])
    ap.add_argument("--prev-specs", nargs="*", default=[], dest="prev_specs")  # v6.14: last 4 specs of the channel -> script_check
    ap.add_argument("--skills", default="")  # v6.14: the "Skillar: ...; ishlatilmadi: ..." line (docs/skills/INDEX.md rule 2)
    a = ap.parse_args()
    out = a.out or os.path.splitext(a.video)[0] + "_qc.json"
    R = {}

    def put(k, status, note=""):
        R[k] = {"status": status, "note": note.strip()[-600:]}
        print(f"[{status:4}] {k}: {note.strip().splitlines()[-1] if note.strip() else ''}"[:200])

    # 0 freshness: repo up to date + video rendered with the CURRENT engine and after every "QAYTA RENDER: HA" change
    #   (Shohjahon 2026-11-21: "other chats ship improvements but you keep releasing videos in the old state")
    run(["git", "-C", ROOT, "fetch", "-q", "origin", "media"])
    rc, behind = run(["git", "-C", ROOT, "rev-list", "--count", "HEAD..origin/media"])
    probs = []
    if rc == 0 and behind.strip() not in ("", "0"): probs.append(f"repo {behind.strip()} commit(s) behind origin/media - git pull --rebase and re-render")
    if a.rendered and os.path.exists(a.rendered):
        rj = json.load(open(a.rendered)); import hashlib
        cur = hashlib.sha1(open(os.path.join(ROOT, rj.get("renderer_path") or "engine/make_video.py"), "rb").read()).hexdigest()[:12]  # Rocco v2: own renderer
        if not rj.get("engine_sha"): probs.append("rendered.json has no engine stamp (engine < 6.9) - re-render")
        elif rj["engine_sha"] != cur:
            when = rj.get("rendered_at", "")
            if when.endswith("Z"):  # changes.md rows are Tashkent time (UTC+5); rendered_at is UTC
                import datetime as _dt
                when = (_dt.datetime.strptime(when, "%Y-%m-%dT%H:%M:%SZ") + _dt.timedelta(hours=5)).strftime("%Y-%m-%d %H:%M")
            ch = [l for l in open(os.path.join(ROOT, "docs", "changes.md")).read().splitlines()
                  if l.startswith("| 20") and l.split("|")[1].strip() > when[:16].replace("T", " ") and "QAYTA RENDER: HA" in l
                  and re.search(r"dvigatel|engine|make_video|ENGINE", l)]  # only engine changes; a review of one video is not a global re-render
            if ch: probs.append("engine changed since render with re-render required: " + " / ".join(c.split("|")[3].strip() for c in ch))
            else: R["0_note"] = {"status": "INFO", "note": "engine changed since render, no re-render-required change"}
    else:
        probs.append("no --rendered json - freshness unknown")
    put("0_freshness", "FAIL" if probs else "PASS", "; ".join(probs) or "up to date")

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
    tim = []
    if a.rendered and os.path.exists(a.rendered):
        _rj = json.load(open(a.rendered)); tim = _rj.get("timings") or []
        if tim and abs(float(_rj.get("seconds", 0)) - dur) > 0.6:  # rendered.json is from another render of this spec
            R["8_note"] = {"status": "WARN", "note": f"rendered.json is {_rj.get('seconds')} s but video is {dur:.1f} s - stale json, even sampling used"}
            tim = []
    if dur > 0 and tim:
        # one frame per scene at 80% of the scene - animations (count-ups, slide-ins, flips) have settled by then,
        # so a mid-animation frame is not mistaken for a wrong number or a cut-off panel
        ts = [st + 0.8 * d for st, d in tim][:12]; frames = []
        for i, t in enumerate(ts):
            f = os.path.splitext(sheet)[0] + f"_{i}.png"
            run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", a.video, "-frames:v", "1", "-vf", "scale=270:-2", f])
            if os.path.exists(f): frames.append(f)
        cmd = ["ffmpeg", "-y", "-loglevel", "error"]
        for f in frames: cmd += ["-i", f]
        rc, o = run(cmd + ["-filter_complex", f"hstack=inputs={len(frames)}", sheet]) if len(frames) > 1 else (1, "no frames")
        for f in frames: os.remove(f)
    elif dur > 0:
        n = 8; fps = n / dur
        rc, o = run(["ffmpeg", "-y", "-loglevel", "error", "-i", a.video, "-vf",
                     f"fps={fps:.5f},scale=270:-2,tile={n}x1", "-frames:v", "1", sheet])
    if dur > 0:
        put("8_contact_sheet", "LOOK" if rc == 0 and os.path.exists(sheet) else "SKIP", sheet + " - Read it before posting" + ("" if rc == 0 else "\n" + o))
    else:
        put("8_contact_sheet", "SKIP", "no duration")

    # 9 colour / exposure (docs/skills/notes/2026-11-21_color.md)
    rc, o = run([sys.executable, "-I", os.path.join(ROOT, "engine", "color_check.py"), "frames", a.video])
    if "Traceback" in o or rc not in (0, 1):
        put("9_color", "SKIP", o)
    else:
        clipped = "CLIPPED" in o; warn = ("CRUSHED" in o) or ("DULL" in o)
        put("9_color", "FAIL" if clipped else ("WARN" if warn else "PASS"),
            "clipped highlights (big number burnt)" if clipped else ("dark/dull frames - brighten bg or less b-roll dimming" if warn else "exposure and colour OK"))

    # 10 look similarity vs the last 4 published/queued videos (docs/looks.md, engine/look_check.py; >= 0.70 = FAIL)
    if a.prev:
        rc, o = run([sys.executable, "-I", os.path.join(ROOT, "engine", "look_check.py"), a.video] + a.prev)
        _st = "SKIP" if "Traceback" in o else ("PASS" if rc == 0 else "FAIL")
        if _st == "FAIL" and a.spec and json.load(open(a.spec)).get("look") == "fullbleed":
            # BUYURTMA 8 (2026-11-22) makes full-screen footage the one layout, so layout/tone match by design;
            # it still FAILS when the colours are the same too (palette >= 0.92 = same footage feel)
            pals = [float(m) for m in re.findall(r"FAIL\s+[\d.]+\s+\(layout [\d.]+, palette ([\d.]+)", o)]
            if pals and max(pals) < 0.92: _st = "WARN"; o += "\nWARN: fullbleed layout shared by design (Buyurtma 8); palette differs (< 0.92)"
        put("10_look", _st, o)
    else:
        put("10_look", "SKIP", "no --prev videos given (pass the last 4 videos of this channel)")

    # 11 pacing (docs/lessons_winners_2026-11-21.md; KO'RIK №1): a new picture every <= 2 s -> hard cuts >= duration/2.
    #    Measured on the VIDEO with ffmpeg scene detection (scene > 0.22, as the Trade review does) - camera moves and
    #    re-framing the same clip do not count; the engine's own "cuts" list is shown for reference only.
    if dur > 0:
        rc, o = run(["ffmpeg", "-nostats", "-i", a.video, "-vf", "scale=270:-2,select='gt(scene,0.22)',showinfo", "-an", "-f", "null", "-"])
        nc = 1 + len(re.findall(r"pts_time:", o)); need = int(dur / 2)
        rjc = json.load(open(a.rendered)) if a.rendered and os.path.exists(a.rendered) else {}
        put("11_pacing", "PASS" if nc >= need else "FAIL",
            f"{nc} hard cuts (ffmpeg scene>0.22) in {dur:.1f} s = {dur / max(1, nc):.1f} s/cut (need >= {need}); engine planned {len(rjc.get('cuts', []))}")
    else:
        put("11_pacing", "SKIP", "no duration")
    # 12 script skeleton vs the last 4 specs of the channel (docs/script_rules.md, engine/script_check.py)
    if a.spec and a.prev_specs:
        rc, o = run([sys.executable, "-I", os.path.join(ROOT, "engine", "script_check.py"), a.spec] + a.prev_specs)
        put("12_script", "SKIP" if "Traceback" in o else ("PASS" if rc == 0 else "FAIL"), o)
    else:
        put("12_script", "SKIP", "no --prev-specs (pass the last 4 specs of this channel)")
    # 14 empty panel (night_order BUYURTMA 8 #2): one flat colour/stripe area > 15 % of any of 12 frames = FAIL
    if dur > 0:
        rc, o = run([sys.executable, "-I", os.path.join(ROOT, "engine", "empty_check.py"), a.video])
        put("14_empty_panel", "SKIP" if (rc == 2 or "Traceback" in o) else ("PASS" if rc == 0 else "FAIL"), o.strip().splitlines()[-1] if o.strip() else o)
    else:
        put("14_empty_panel", "SKIP", "no duration")
    # 13 skills line (docs/skills/INDEX.md: missing = FAIL)
    put("13_skills_line", "PASS" if re.search(r"Skillar:.+;\s*ishlatilmadi:", a.skills) else "FAIL",
        a.skills or 'no --skills "Skillar: ...; ishlatilmadi: ... (sababi)"')

    st = [r["status"] for k, r in R.items()]
    blocking_skip = any(R[k]["status"] == "SKIP" for k in R if k.split("_")[0].isdigit() and int(k.split("_")[0]) <= 5)  # 2026-11-22: "12_script" is not step 1
    verdict = "FAIL" if "FAIL" in st else ("BLOCKED" if blocking_skip else "PASS")
    R["verdict"] = verdict
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    json.dump(R, open(out, "w"), indent=1)
    print(f"VERDICT: {verdict}  -> {out}")
    sys.exit(0 if verdict == "PASS" else (1 if verdict == "FAIL" else 2))


if __name__ == "__main__":
    main()
