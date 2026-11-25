#!/usr/bin/env python3
"""Background-reuse check (Shohjahon 2026-11-25: "nega hamma videoda bir xil fon?").

usage: python3 engine/bg_reuse_check.py NEW_SPEC.json PREV_SPEC.json [PREV_SPEC.json ...] [--max 0.3]
Collects every background file (bg, bg2) a spec uses and reports what share of the new
video's backgrounds already appeared in the previous videos. FAIL when the share is above
--max (default 30%), so every new episode gets its own sets/footage.
"""
import json, os, sys


def bgs(path):
    d = json.load(open(path))
    out = set()
    for s in d.get("shots", []):
        for k in ("bg", "bg2"):
            if s.get(k):
                out.add(os.path.basename(s[k]))
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    mx = float(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 0.3
    if "--max" in sys.argv:
        args.remove(sys.argv[sys.argv.index("--max") + 1])
    new, prev = bgs(args[0]), set()
    for p in args[1:]:
        prev |= bgs(p)
    if not new:
        print("bg_reuse: no backgrounds in spec"); return 0
    reused = sorted(new & prev)
    share = len(reused) / len(new)
    verdict = "FAIL" if share > mx else "PASS"
    print(json.dumps({"verdict": verdict, "share": round(share, 2), "new": len(new), "reused": reused}))
    return 1 if verdict == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
