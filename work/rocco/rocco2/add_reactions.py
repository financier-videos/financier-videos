#!/usr/bin/env python3
"""Insert reaction cut-ins into an rc_render spec so no shot runs longer than MAX seconds (qc_gate 11_pacing: a new picture every <= 2 s).
usage: add_reactions.py spec.json rendered.json [--max 2.3]
A long scammer shot gets a victim/detective reaction (cu_p shock or cu_r sideeye); a long victim/detective shot gets the other one."""
import json, sys
sp_p, rj_p = sys.argv[1], sys.argv[2]; MAX = float(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 2.3
CONT = {"chalk", "stamp", "kinetic", "grid", "flagvote", "pixel", "phone", "quiz", "counter", "scale", "bars", "receipt", "spend", "versus", "line", "store", "flags", "box"}
sp = json.load(open(sp_p)); rj = json.load(open(rj_p))
if "--redo" in sys.argv: sp["shots"] = [x for x in sp["shots"] if not x.get("_auto")]
if any("line" not in x for x in sp["shots"]):  # absolute-timed shots (t0/t1): order is the author's, do not touch
    print("absolute-timed spec: no reaction cut-ins"); json.dump(sp, open(sp_p, "w"), indent=1); sys.exit(0)
lt = [(a, b) for _, _, a, b in rj["lines"]]
def t_of(s): a, b = lt[s["line"]]; return a + (b - a) * s.get("from", 0)
def line_at(t):
    for i, (a, b) in enumerate(lt):
        if a <= t < b: return i, round((t - a) / max(0.01, b - a), 2)
    return None, None
_any_bg = next((s["bg"] for s in sp["shots"] if s.get("bg")), None)
home_p = next((s["bg"] for s in sp["shots"] if s["kind"] in ("cu_p", "phone", "two") and s.get("bg")), _any_bg)
home_r = next((s["bg"] for s in sp["shots"] if s["kind"] in ("cu_r", "store") and s.get("bg")), home_p)
shots = [s for s in sp["shots"] if "line" in s]; end = rj["seconds"]; add = []
for j, s in enumerate(shots):
    if s["kind"] == "end": continue
    t0 = t_of(s); t1 = t_of(shots[j + 1]) if j + 1 < len(shots) else end
    n = int((t1 - t0) / MAX)
    for k in range(1, n + 1):
        t = t0 + (t1 - t0) * k / (n + 1); li, fr = line_at(t)
        if li is None or fr < 0.12 or fr > 0.9: continue
        spk = sp["lines"][li][0]
        if spk == "S" or s["kind"] in ("slick", "call"):
            r = {"kind": "cu_p", "bg": home_p, "p": "shock", "r": "sideeye", "cam": {"z": 1.25, "push": 0.06, "fy": 0.42}} if k % 2 else \
                {"kind": "cu_r", "bg": home_r, "r": "sideeye", "cam": {"z": 1.3, "push": 0.1, "fy": 0.47}}
        elif spk == "P":  # the speaker stays on screen: wider two-shot with Rocco listening
            r = {"kind": "two", "bg": home_p, "p": s.get("p", "happy"), "r": "sideeye", "cam": {"z": 1.0, "push": 0.06}}
        else:  # Rocco talks: alternate a two-shot (he stays visible) and Penny's reaction
            r = {"kind": "two", "bg": home_r, "p": "happy", "r": s.get("r", "sly"), "cam": {"z": 1.05, "push": 0.06}} if k % 2 else \
                {"kind": "cu_p", "bg": home_p, "p": "shock", "r": "sly", "cam": {"z": 1.2, "push": 0.06, "fy": 0.42}}
        r.update({"line": li, "from": fr, "blur": 1, "amb": s.get("amb", sp.get("amb", "room")), "_auto": True}); add.append(r)
        if s["kind"] in CONT:  # graphic shot: come back to it after the reaction, its animation clock keeps running
            li2, fr2 = line_at(t + 1.0)
            if li2 is not None and t + 1.0 < t1 - 0.5: add.append(dict(s, line=li2, **{"from": fr2}, cont=True, _auto=True, hook=None))
allsh = sp["shots"] + add
key = lambda s: (s.get("line", 99), 9 if s["kind"] == "end" else s.get("from", 0))
sp["shots"] = sorted(allsh, key=key)
json.dump(sp, open(sp_p, "w"), indent=1); print(f"added {len(add)} reaction cut-ins -> {len(sp['shots'])} shots")
