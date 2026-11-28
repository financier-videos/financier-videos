"""BK-16 description + qcspec (same conversion as work/buck/b10/meta.py)."""
import json, re
d = "work/buck/b16"; k = "bk16"
title = "$275 Billion in $100 Bills Reaches Space"
body = ("Would you climb it or spend it?\n"
        "Adobe expects Americans to spend a record $275.1 billion online this holiday season (Nov 1 - Dec 31, 2026; forecast). "
        "In $100 bills that's 2.75 billion notes. Stacked up: about 186.7 miles tall - past the clouds, about 34 Mount Everests, "
        "three times past the edge of space (62 miles), and about 3,000 tons of paper.\n"
        "Math: $275.1B / $100 = 2.751B notes x 0.0043 in = 11.83M in = 186.7 mi; Everest 29,032 ft = 5.50 mi (33.9x); "
        "1 note ~1 g -> ~2,751 metric tons (~3,030 US tons).")
src = ("Adobe Digital Insights 2026 holiday forecast (Sept 28, 2026); Bureau of Engraving and Printing currency FAQ "
       "(note thickness 0.0043 in, weight about 1 gram).")
foot = ("\nFootage: Pixabay (34168960, andrey3dp, BeezeeStock, flutie8211, JoshuaWoroniecki, doktorkleinmusic, AdisResic, NASA-Imagery, phlyingdoctor)."
        "\nNot financial advice. For education and entertainment.\nBuck is our original character.")
tags = "#holidayshopping #moneyfacts #shorts"
open(f"{d}/{k}_desc.txt", "w").write(f"{body}\n\nSources: {src}{foot}\n\n{tags}\n")
sp = json.load(open(f"{d}/{k}.json")); sc = []
KM = {"counter": "stat", "scale": "chart", "kinetic": "sticker"}
for i, (_, t) in enumerate(sp["lines"]):
    main = next((x for x in sp["shots"] if x.get("line") == i and not x.get("_auto")), {"kind": "host"})
    vis = str(main.get("bg", "")).endswith(".mp4") and main["kind"] in ("host", "kinetic")
    kk = "broll" if vis else KM.get(main["kind"], "broll"); tx = re.sub(r"\[[^\]]*\]\s*", "", t).strip()
    sc.append({"text": tx, kk: f"{k}-{i}"} if kk != "broll" else {"text": tx, "shots": [{"broll": main.get("bg")}]})
sc.append({"text": ""})
bench = ["EpTFo_wkNwA physical scale 3.3M", "siIMLJRNM0c how long until broke 3.7M", "BK-01 own $40T stack (scale format, 128 in burst)"]
json.dump({"format": "short", "look": "fx", "scenes": sc, "benchmarks": bench, "title": title, "visual_hook": sp.get("visual_hook"),
           "source_titles": []}, open(f"{d}/{k}_qcspec.json", "w"), indent=1)
print("ok")
