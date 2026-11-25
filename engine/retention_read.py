#!/usr/bin/env python3
"""Map a YouTube audience-retention curve onto the script lines of one of our videos.

usage: python3 engine/retention_read.py ROWS.json RENDERED.json SPEC.json [--video ID]
  ROWS.json     the "rows" array from vidiq_channel_analytics report=audience_retention
                ([[elapsedVideoTimeRatio, audienceWatchRatio, relativeRetentionPerformance], ...])
  RENDERED.json our renderer output with "timings": [[start_s, dur_s], ...] per script line and "seconds"
  SPEC.json     the episode spec with "lines": [[who, text], ...]
Prints per line: retention at start/end, the drop inside the line, and flags the
biggest drops; plus the first-3-seconds hold and the end (loop) value. Append the
printed block to docs/retention_log.md (docs/studio_os.md §2).
"""
import json, re, sys


def at(rows, r):
    best = min(rows, key=lambda x: abs(x[0] - r))
    return best[1]


def main():
    rows = json.load(open(sys.argv[1]))
    rows = rows.get("rows", rows) if isinstance(rows, dict) else rows
    rend = json.load(open(sys.argv[2]))
    spec = json.load(open(sys.argv[3]))
    vid = sys.argv[sys.argv.index("--video") + 1] if "--video" in sys.argv else spec.get("id", "?")
    total = rend.get("seconds") or sum(d for _, d in rend["timings"])
    tm = rend["timings"]
    lines = spec["lines"]
    out = []
    three = at(rows, min(3.0 / total, 1.0))
    out.append(f"### {vid} — {spec.get('title', '')} ({total:.1f} s)")
    out.append(f"- start {at(rows, 0.01):.2f} · after 3 s {three:.2f} · middle {at(rows, 0.5):.2f} · end {at(rows, 1.0):.2f} "
               f"(>1.0 = replays/loops)")
    drops = []
    for i, (st, du) in enumerate(tm[:len(lines)]):
        a, b = at(rows, st / total), at(rows, min((st + du) / total, 1.0))
        txt = re.sub(r"\[[^\]]*\]\s*", "", lines[i][1])[:70]
        drops.append((a - b, i, a, b, txt))
        out.append(f"- L{i} {st:5.1f}s {a:.2f}→{b:.2f} (−{(a - b) * 100:4.1f} pts) {lines[i][0]}: {txt}")
    worst = sorted(drops, reverse=True)[:3]
    out.append("- BIGGEST DROPS: " + "; ".join(f"L{i} −{d * 100:.0f} pts \"{t[:40]}\"" for d, i, a, b, t in worst))
    print("\n".join(out))


if __name__ == "__main__":
    main()
