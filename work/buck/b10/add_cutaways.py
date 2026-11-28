#!/usr/bin/env python3
"""Split long graphic shots with Buck reaction cutaways so a new picture comes every <= MAX s (qc_gate 11_pacing).
usage: add_cutaways.py spec.json rendered.json [--max 2.1]
main [0..a] -> Buck cutaway (~1.1 s, other colour, mood from the line's tag, optional prop text) -> main continues ("cont": its clock keeps running)."""
import json, re, sys
sp_p, rj_p = sys.argv[1], sys.argv[2]; MAX = float(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 2.1
sp = json.load(open(sp_p)); rj = json.load(open(rj_p))
if not sp.get("pool"): print("WARNING: spec has no \"pool\" - cutaways fall back to flat colour cards, qc 14_empty_panel will likely FAIL "
                             "(add \"pool\": [names of /tmp/fin/bg/bank/<name>.mp4 footage], 2026-11-28 BK-16)", file=sys.stderr)
sp["shots"] = [s for s in sp["shots"] if not s.get("_auto")]
lt = [(a, b) for _, _, a, b in rj["lines"]]; end = rj["seconds"]
MOOD = [("shock", "shocked"), ("amaz", "shocked"), ("laugh", "laugh"), ("grin", "laugh"), ("play", "laugh"), ("tease", "smug"), ("sly", "smug"),
        ("smug", "smug"), ("deadpan", "sideeye"), ("serious", "point"), ("excit", "happy"), ("cheer", "happy"), ("sad", "sad"), ("deflat", "sad"),
        ("nerv", "confused"), ("curious", "confused"), ("suspense", "point"), ("drumroll", "point"), ("announc", "proud"), ("teach", "point")]
SETS = ["teal", "pink", "sky", "peach", "green", "yellow"]
def mood_of(i):
    tag = " ".join(re.findall(r"\[([^\]]*)\]", sp["lines"][i][1])).lower()
    return next((m for k, m in MOOD if k in tag), "happy")
def t_of(s): a, b = lt[s["line"]]; return a + (b - a) * s.get("from", 0)
def at(t):
    for i, (a, b) in enumerate(lt):
        if a <= t < b: return i, round((t - a) / max(0.01, b - a), 3)
    return None, None
shots = sorted([s for s in sp["shots"] if "line" in s], key=lambda s: (s["line"], 9 if s["kind"] == "end" else s.get("from", 0)))
props = sp.get("props", {}); add = []; k = 0
for j, s in enumerate(shots):
    if s["kind"] == "end" or (s["kind"] == "host" and (t_of(shots[j + 1]) if j + 1 < len(shots) else end) - t_of(s) <= 3.0): continue
    t0 = t_of(s); t1 = t_of(shots[j + 1]) if j + 1 < len(shots) else end; L = t1 - t0
    pos = t0 + min(1.3, L * 0.45)
    while t1 - pos > 0.9 and pos - t0 >= 0.8 and L > MAX:
        li, fr = at(pos)
        if li is None: break
        cut = {"kind": "host", "set": SETS[k % len(SETS)], "line": li, "from": fr, "buck": {"mood": mood_of(li), "h": 1300, "y": 1.04}, "_auto": True}
        if sp.get("pool"): cut.pop("set"); cut.update(bg=f"/tmp/fin/bg/bank/{sp['pool'][(k + 2) % len(sp['pool'])]}.mp4", bg_start=(7.0 if "cash_stacks" in sp["pool"][(k + 2) % len(sp["pool"])] else 0.5) + (k * 2.3) % 5, dim=20)
        if props.get(str(li)): cut["prop"] = props[str(li)]
        if s["kind"] == "host": cut = dict(s, set=SETS[(k + 3) % len(SETS)], line=li, **{"from": fr}, _auto=True); cut["buck"] = dict(s.get("buck", {}), mood=mood_of(li), h=1100, x=0.35)
        add.append(cut); k += 1
        back = pos + 1.1
        if t1 - back > 0.8 and s["kind"] != "host":
            li2, fr2 = at(back)
            if li2 is not None: add.append(dict(s, line=li2, **{"from": fr2}, cont=True, _auto=True, hook=None)); pos = back + min(1.6, (t1 - back) * 0.5)
            else: break
        else: break
sp["shots"] = sorted(sp["shots"] + add, key=lambda s: (s.get("line", 99), 9 if s["kind"] == "end" else s.get("from", 0)))
json.dump(sp, open(sp_p, "w"), indent=1); print(f"{sp_p}: +{len(add)} cutaway shots -> {len(sp['shots'])}")
