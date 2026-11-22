#!/usr/bin/env python3
"""Voice check: transcribe a finished video (offline Whisper via sherpa-onnx) and compare with the spec's spoken text.
Catches garbled / skipped / repeated TTS takes that loudness and duration checks miss.

  pip install --break-system-packages sherpa-onnx soundfile numpy
  curl -sSfL -o /tmp/w.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-base.en.tar.bz2
  mkdir -p /tmp/asr && tar xf /tmp/w.tar.bz2 -C /tmp/asr
  python3 -I engine/voice_check.py video.mp4 spec.json [--model /tmp/asr/sherpa-onnx-whisper-base.en] [--min 0.86]

Numbers are ignored on both sides (Whisper writes "$4.99", the script says "four ninety-nine"), so a wrong NUMBER is not
caught here - read the transcript line that is printed. Exit 0 = pass, 1 = below --min or words missing, 2 = could not run.
"""
import sys, json, re, subprocess, tempfile, os, difflib, argparse

NUMW = set("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen "
           "eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million billion trillion "
           "percent dollar dollars cents cent point oh half and a".split())


FILLERS = {"ooh", "oh", "shh", "sh", "uh", "um", "aww", "aw", "mm", "hm", "hmm", "psst", "ah", "pfft", "huh"}


def norm(t):
    t = t.lower().replace("-", " ").replace("’", "'")
    w = re.findall(r"[a-z']+|\d[\d,.]*", t)
    w = [x.strip("'") for x in w if not x[0].isdigit() and x.strip("'") not in NUMW and x.strip("'")]
    w = [x for x in w if x not in FILLERS]  # 2026-11-22: ASR drops interjections ("ooh", "shh", "aww", "mm-hm")
    out, run = [], False  # 2026-11-21: "F T C" / "Q R" spelled for TTS == "FTC" / "QR" from ASR -> join runs of single letters
    for x in w:
        single = len(x) == 1 and (x not in ("a", "i") or run)  # inside a spelled run "a" is a letter (F-L-A-G)
        if single and run: out[-1] += x
        else: out.append(x)
        run = single or (run and single)
    return out


def spoken(spec):
    out = []
    for s in spec["scenes"]:
        b = s.get("buck"); line = s.get("say", s.get("text", ""))
        m = (s.get("mascot") or {}).get("say")
        parts = ([line, b] if s.get("buck_after") else [b, line])
        out += [p for p in parts if p]
    return " ".join(out)


def transcribe(video, model):
    import sherpa_onnx, soundfile as sf, numpy as np
    wav = tempfile.mktemp(suffix=".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-ac", "1", "-ar", "16000", wav], check=True)
    a, sr = sf.read(wav, dtype="float32"); os.remove(wav)
    p = lambda n: os.path.join(model, [f for f in os.listdir(model) if f.endswith(n)][0])
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=p("encoder.int8.onnx"), decoder=p("decoder.int8.onnx"),
                                                     tokens=p("tokens.txt"), language="en", task="transcribe", num_threads=2)
    # split into <= 24 s pieces at the quietest 50 ms near each boundary (Whisper window is 30 s)
    cuts, pos, n = [0], 0, len(a)
    while n - pos > 24 * sr:
        lo, hi = pos + 16 * sr, pos + 24 * sr; win = sr // 20
        e = [float(np.abs(a[i:i + win]).mean()) for i in range(lo, hi, win)]
        pos = lo + int(np.argmin(e)) * win + win // 2; cuts.append(pos)
    cuts.append(n); txt = []
    for i in range(len(cuts) - 1):
        st = rec.create_stream(); st.accept_waveform(sr, a[cuts[i]:cuts[i + 1]]); rec.decode_stream(st); txt.append(st.result.text.strip())
    return " ".join(txt)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("spec")
    ap.add_argument("--model", default="/tmp/asr/sherpa-onnx-whisper-base.en"); ap.add_argument("--min", type=float, default=0.86)
    a = ap.parse_args()
    try:
        heard = transcribe(a.video, a.model)
    except Exception as e:
        print(json.dumps({"rc": 2, "error": str(e)[:300]})); sys.exit(2)
    exp = norm(spoken(json.load(open(a.spec)))); got = norm(heard)
    sm = difflib.SequenceMatcher(None, exp, got, autojunk=False)
    missing, extra = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("delete", "replace"): missing.append(" ".join(exp[i1:i2]))
        if tag in ("insert", "replace"): extra.append(" ".join(got[j1:j2]))
    ratio = round(sm.ratio(), 3); bad = ratio < a.min or any(len(m.split()) >= 3 for m in missing)
    print(json.dumps({"rc": int(bad), "match": ratio, "missing": missing, "extra": extra, "heard": heard}, ensure_ascii=False, indent=1))
    sys.exit(int(bad))


if __name__ == "__main__":
    main()
