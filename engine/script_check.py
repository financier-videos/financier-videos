#!/usr/bin/env python3
"""script_check.py - "is this script built on the same skeleton as the previous ones?" (Shohjahon 2026-11-21 20:46 audit).

Usage: python3 -I engine/script_check.py NEW_spec.json PREV1.json [PREV2.json ...]   -> exit 1 on FAIL
Checks NEW against each PREV (use the last 4 published/queued specs of the same channel):
  line2   - same opening word(s) of the 2nd line (e.g. "Wait...")            -> FAIL if it matches ANY of the last 4
  ending  - same last 1-2 words of the last line (e.g. "... because...")      -> FAIL if it matches 2+ of the last 4
  shape   - same sequence of scene kinds (stat/chart/vs/broll/sticker/plain)  -> FAIL if identical to any PREV
  length  - word count within +-10% of ALL previous                           -> WARN (lengths should vary: micro / 25-35 s / story 45-75 s)
Also prints words, scenes, words-per-scene and the share of scenes with full-screen footage ("broll").
"""
import json, re, sys

def lines(spec): return [(s.get("say") or s.get("text") or "").strip() for s in spec.get("scenes", [])]
def norm(t): return re.sub(r"[^a-z' ]", " ", t.lower()).split()
def footage(s): return bool(s.get("broll") or s.get("shots"))  # v6.14: "shots" scenes are full-screen footage too
def kind(s):
    if s.get("shots") and not any(s.get(k) for k in ("vs", "chart", "stat")): return "broll"
    for k in ("vs", "chart", "stat", "broll", "phone", "sticker"):
        if s.get(k): return k
    return "plain"

def info(path):
    sp = json.load(open(path)); ls = lines(sp); sc = sp.get("scenes", [])
    return {"path": path.split("/")[-1], "l2": " ".join(norm(ls[1])[:1]) if len(ls) > 1 else "", "end": " ".join(norm(ls[-1])[-1:]) if ls else "",
            "shape": [kind(s) for s in sc], "words": sum(len(l.split()) for l in ls), "scenes": len(sc),
            "broll": sum(1 for s in sc if footage(s)), "look": sp.get("look") or sp.get("style") or "-"}

def main():
    a = sys.argv[1:]
    if len(a) < 2: print(__doc__); return 2
    new, prev = info(a[0]), [info(p) for p in a[1:]]
    fails, warns = [], []
    same_l2 = [p["path"] for p in prev if p["l2"] and p["l2"] == new["l2"]]
    if same_l2: fails.append(f'line2 starts with "{new["l2"]}" like {same_l2}')
    same_end = [p["path"] for p in prev if p["end"] and p["end"] == new["end"]]
    if len(same_end) >= 2: fails.append(f'ending "...{new["end"]}" like {same_end}')
    same_shape = [p["path"] for p in prev if p["shape"] == new["shape"]]
    if same_shape: fails.append(f"scene-kind sequence identical to {same_shape}")
    if prev and all(abs(p["words"] - new["words"]) <= 0.10 * new["words"] for p in prev): warns.append("word count within 10% of all previous - vary the length")
    share = new["broll"] / max(1, new["scenes"])
    if share < 0.40: fails.append(f'full-screen footage in {new["broll"]}/{new["scenes"]} scenes (<40%)')
    for x in [new] + prev:
        print(f'{x["path"]:34s} words {x["words"]:3d} scenes {x["scenes"]:2d} broll {x["broll"]} look {x["look"]:9s} line2 "{x["l2"]}" end "{x["end"]}"')
    for w in warns: print("WARN:", w)
    for f in fails: print("FAIL:", f)
    print("SCRIPT_CHECK:", "FAIL" if fails else "PASS")
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())
