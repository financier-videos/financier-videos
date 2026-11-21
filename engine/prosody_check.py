#!/usr/bin/env python3
"""Prosody check (skill: docs/skills/notes/2026-11-21_parselmouth-prosody.md) - HOW Buck said it, not WHAT.
voice_check.py checks the words; this checks pitch movement per scene with Praat (Parselmouth, GPL-3.0 - used as a
tool only, not vendored).

  pip install --break-system-packages praat-parselmouth==0.4.7
  python3 -I engine/prosody_check.py video.mp4 spec.json [rendered.json] [--json out.json]

rendered.json = the engine's result JSON ("timings": [[start, dur], ...] per scene). Without it scenes are split evenly.
Flags (HYPOTHESES - thresholds are ours, tune them against retention in growth_log):
  MONOTONE   - 10-90 percentile F0 range of the scene < 3 semitones (sounds robotic)
  FLAT_Q     - spoken text ends with a yes/no "?" (not "A or B?", not a wh-question) but the last voiced 0.35 s does not rise (> +0.5 st) vs the 0.35 s before
  NO_LAND    - scene has "land" (punchline pause) but the longest unvoiced gap after the last voiced word < land*0.6
Exit 0 = no MONOTONE/FLAT_Q flags, 1 = flags found, 2 = could not run. Music-free mix is assumed (we have none).
"""
import sys, json, os, subprocess, tempfile, argparse
import numpy as np


WH = {"what", "why", "who", "whom", "whose", "where", "when", "which", "how", "worst", "best"}


def scene_text(s):
    b = s.get("buck"); line = s.get("say", s.get("text", ""))
    parts = [line, b] if s.get("buck_after") else [b, line]
    return " ".join(p for p in parts if p).strip()


def st(f, ref):
    return 12.0 * np.log2(f / ref)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("spec"); ap.add_argument("rendered", nargs="?")
    ap.add_argument("--json"); ap.add_argument("--mono", type=float, default=3.0)
    a = ap.parse_args()
    try:
        import parselmouth
    except Exception as e:
        print("prosody_check: parselmouth missing:", e); return 2
    spec = json.load(open(a.spec))
    scenes = spec["scenes"]
    wav = tempfile.mktemp(suffix=".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-ac", "1", "-ar", "22050", wav], check=True)
    snd = parselmouth.Sound(wav); os.remove(wav)
    total = snd.get_total_duration()
    if a.rendered and os.path.exists(a.rendered):
        tm = json.load(open(a.rendered)).get("timings")
    else:
        tm = None
    if not tm or len(tm) != len(scenes):
        d = total / len(scenes); tm = [[i * d, d] for i in range(len(scenes))]
    pitch = snd.to_pitch(time_step=0.01, pitch_floor=75, pitch_ceiling=500)
    f0 = pitch.selected_array["frequency"]; ts = pitch.xs()
    voiced = f0 > 0
    ref = np.median(f0[voiced]) if voiced.any() else 150.0
    out, bad = [], 0
    for i, (sc, (t0, dur)) in enumerate(zip(scenes, tm)):
        txt = scene_text(sc)
        m = (ts >= t0) & (ts < t0 + dur)
        v = m & voiced
        r = {"scene": i + 1, "t": round(t0, 2), "text": txt[:60], "flags": []}
        if v.sum() < 15 or not txt:
            r["note"] = "no speech"; out.append(r); continue
        s_ = st(f0[v], ref)
        rng = float(np.percentile(s_, 90) - np.percentile(s_, 10))
        r["range_st"] = round(rng, 1)
        if rng < a.mono: r["flags"].append("MONOTONE")
        vt = ts[v]; last = vt.max()
        q = txt.rstrip().rsplit(".", 1)[-1].lower().split("...")[-1].strip()
        yn = q.endswith("?") and " or " not in q and q.split()[0].strip("¿") not in WH if q.split() else False
        if yn:  # yes/no question only: "A or B?" and wh-questions normally FALL in English
            e = s_[vt >= last - 0.35]; b_ = s_[(vt < last - 0.35) & (vt >= last - 0.7)]
            if len(e) > 3 and len(b_) > 3:
                rise = float(np.median(e) - np.median(b_)); r["q_rise_st"] = round(rise, 1)
                if rise < 0.5: r["flags"].append("FLAT_Q")
        gaps = np.diff(vt); r["max_gap_s"] = round(float(gaps.max()) if len(gaps) else 0.0, 2)
        tail = t0 + dur - last; r["tail_s"] = round(tail, 2)
        if sc.get("land"):
            if max(tail, r["max_gap_s"]) < float(sc["land"]) * 0.6: r["flags"].append("NO_LAND")
        bad += any(f in ("MONOTONE", "FLAT_Q") for f in r["flags"])
        out.append(r)
    for r in out:
        print(f"{r['scene']:>2} {r['t']:>6.2f}s range={r.get('range_st','-'):>4} st  gap={r.get('max_gap_s','-')}  "
              f"{' '.join(r['flags']) or 'ok'}  | {r['text']}")
    res = {"median_f0": round(float(ref), 1), "scenes": out, "flagged": bad}
    print(json.dumps({"median_f0": res["median_f0"], "flagged_scenes": bad}))
    if a.json: json.dump(res, open(a.json, "w"), indent=1)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
