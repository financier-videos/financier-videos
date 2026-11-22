"""10 Buck videos, 10 different formats (2026-11-22). Facts verified by web search (sources in each *_desc.txt)."""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__))
BR = ["FINANCIER", [255, 205, 60]]
SETS = ["teal", "pink", "sky", "peach", "green", "yellow"]


def react(line, frm, mood, prop, i):
    return {"kind": "host", "set": SETS[i % len(SETS)], "line": line, "from": frm, "buck": {"mood": mood, "h": 1300, "y": 1.04}, "prop": prop, "cap": True}


def spec(id_, title, lines, shots, sfx, extra=None, reacts=()):
    sh = list(shots)
    props = {str(line): prop for line, frm, mood, prop in reacts}  # cutaway props; add_cutaways.py places the cutaways
    sh.sort(key=lambda s: (s["line"], 9 if s["kind"] == "end" else s.get("from", 0)))
    sp = {"id": id_, "title": title, "brand": BR, "props": props, "tail": 1.6, "speed": 1.08, "amb": "room", "lines": [["B", t] for t in lines], "shots": sh, "sfx": sfx}
    sp.update(extra or {}); json.dump(sp, open(os.path.join(D, id_.lower().replace("-", "") + ".json"), "w"), indent=1)


B = lambda **k: dict({"buck": {"x": 0.82, "y": 0.99, "h": 560, "mood": k.pop("mood", "point")}}, **k)

# B01 SCALE — US debt as a stack of $100 bills
spec("BK-01", "$40 Trillion in $100 Bills Reaches Past the Satellites", [
    "[excited] This is forty trillion dollars. America's debt. In hundred-dollar bills.",
    "[building suspense] Stack them up. Past the clouds. Past the space station...",
    "[shocked] ...past the satellites! Forty-three thousand kilometers tall!",
    "[deadpan] The space station? Only four hundred kilometers up.",
    "[playful] So this stack is a hundred and seven times taller.",
    "[serious] And it grows every single day. Follow, and I'll show you how fast."],
    [{"kind": "kinetic", "line": 0, "from": 0, "set": "sky", "hook": "", "words": [{"t": "$40,000,000,000,000", "size": 110, "c": [255, 205, 60]}, {"t": "IN $100 BILLS", "size": 120}], **B(mood="shocked")},
     {"kind": "scale", "line": 1, "from": 0, "set": "sky", "ref_m": 408, "stack_m": 43688, "unit": "km", "ref_label": "SPACE STATION", "stack_label": "$40T IN $100s", "at": 0.1, "dur": 4.5, "title": "HOW TALL IS $40 TRILLION?", "cap": True},
     {"kind": "counter", "line": 2, "from": 0, "set": "green", "to": 43688, "prefix": "", "suffix": " KM", "label": "STACK HEIGHT", "dur": 1.6, "sub": "PAST THE SATELLITES", **B(mood="shocked")},
     {"kind": "versus", "line": 3, "from": 0, "left": {"label": "SPACE STATION", "value": 408, "fmt": "{:,.0f} KM", "c": [40, 110, 220]}, "right": {"label": "DEBT STACK", "value": 43688, "fmt": "{:,.0f} KM", "c": [220, 60, 60]}, "win": 1, "win_at": 1.6, "win_label": "107x"},
     {"kind": "kinetic", "line": 4, "from": 0, "bgcol": [[20, 20, 40], [60, 20, 40]], "words": [{"t": "107x", "size": 300, "c": [255, 205, 60], "font": "Anton"}, {"t": "TALLER", "size": 140}]},
     {"kind": "counter", "line": 5, "from": 0, "set": "peach", "to": 40171825101340, "dec": 0, "label": "US DEBT (SEPT 30, 2026)", "size": 92, "dur": 2.5, "ticker": "+$76,738/s", **B(mood="sideeye")}],
    [{"line": 0, "frac": 0.0, "name": "impact", "gain": 0.35}, {"line": 1, "frac": 0.0, "name": "riser", "gain": 0.25}, {"line": 2, "frac": 0.0, "name": "subboom", "gain": 0.4},
     {"line": 3, "frac": 0.2, "name": "boing", "gain": 0.25}, {"line": 4, "frac": 0.0, "name": "impact", "gain": 0.35}, {"line": 5, "frac": 0.3, "name": "tick", "gain": 0.2, "dur": 1.5}],
    {"hot": ["TRILLION", "DEBT", "SATELLITES", "TALLER"]},
    reacts=[(1, 0.6, "shocked", "PAST THE CLOUDS"), (2, 0.6, "dizzy", "43,688 KM"), (4, 0.55, "laugh", "107x"), (5, 0.55, "point", "+$76,738/s")])

# B02 SPEND SIMULATOR — Musk's fortune
spec("BK-02", "I Tried to Spend Elon Musk's $869 Billion", [
    "[mischievous] Forbes says Elon Musk is worth eight hundred sixty-nine billion dollars. Let's spend it.",
    "[excited] First, every copy of GTA 6 sold on day one. Three point seven nine billion.",
    "[gleeful] Then all of America's online shopping on Cyber Week. Forty-four billion.",
    "[warm] Thanksgiving dinner for every single American? Only two billion.",
    "[smug] Still eight hundred and nineteen billion left.",
    "[dramatic] Okay. Let's pay off the US debt with everything that's left...",
    "[deflated] ...that covers two percent. Two."],
    [{"kind": "kinetic", "line": 0, "from": 0, "set": "green", "words": [{"t": "SPEND", "size": 150}, {"t": "$869 BILLION", "size": 140, "c": [255, 205, 60]}, {"t": "CHALLENGE", "size": 120}], **B(mood="smug")},
     {"kind": "spend", "line": 1, "from": 0, "who": "ELON MUSK'S MONEY (FORBES, NOV 1 2026)", "balance": 869e9, "step": 99, "items": [["GTA 6 DAY ONE", 3.79e9], ["CYBER WEEK 2025", 44.2e9], ["THANKSGIVING FOR ALL US", 2.0e9]], "font": "Archivo"},
     {"kind": "spend", "line": 2, "from": 0, "who": "ELON MUSK'S MONEY (FORBES, NOV 1 2026)", "balance": 869e9, "step": 99, "items": [["GTA 6 DAY ONE", 3.79e9], ["CYBER WEEK 2025", 44.2e9], ["THANKSGIVING FOR ALL US", 2.0e9]]},
     {"kind": "spend", "line": 3, "from": 0, "who": "ELON MUSK'S MONEY (FORBES, NOV 1 2026)", "balance": 869e9, "step": 99, "items": [["GTA 6 DAY ONE", 3.79e9], ["CYBER WEEK 2025", 44.2e9], ["THANKSGIVING FOR ALL US", 2.0e9]]},
     {"kind": "counter", "line": 4, "from": 0, "set": "yellow", "start": 869e9, "to": 819e9, "dur": 1.2, "label": "STILL LEFT", **B(mood="smug")},
     {"kind": "versus", "line": 5, "from": 0, "left": {"label": "MUSK'S FORTUNE", "value": 869, "fmt": "${:,.0f}B", "c": [40, 150, 90]}, "right": {"label": "US DEBT", "value": 40000, "fmt": "${:,.0f}B", "c": [210, 50, 50]}, "win": 1, "win_at": 2.0, "win_label": "46x BIGGER"},
     {"kind": "kinetic", "line": 6, "from": 0, "bgcol": [[30, 10, 10], [10, 10, 10]], "words": [{"t": "2%", "size": 380, "c": [235, 64, 52]}, {"t": "OF THE DEBT", "size": 120}], **B(mood="sad")}],
    [{"line": 0, "frac": 0.0, "name": "cash", "gain": 0.3}, {"line": 1, "word": "three", "name": "cash", "gain": 0.3}, {"line": 2, "word": "forty", "name": "cash", "gain": 0.3}, {"line": 3, "word": "two", "name": "cash", "gain": 0.3},
     {"line": 5, "frac": 0.6, "name": "drumroll", "gain": 0.25}, {"line": 6, "frac": 0.2, "name": "wahwah", "gain": 0.35}],
    {"hot": ["SPEND", "BILLION", "DEBT"]},
    reacts=[(0, 0.6, "laugh", "$869B"), (1, 0.62, "happy", "-$3.79B"), (2, 0.62, "laugh", "-$44.2B"), (5, 0.55, "confused", "$40 TRILLION")])
# fix spend item reveal per line: each spend shot shows items up to that line
S = json.load(open(os.path.join(D, "bk02.json")))
n = 0
for s in S["shots"]:
    if s["kind"] == "spend": n += 1; s["items"] = s["items"][:n]; s["step"] = 0.01 if n > 1 else 0.6
json.dump(S, open(os.path.join(D, "bk02.json"), "w"), indent=1)

# B03 PIXEL GAME — pay the debt at $1M a day
spec("BK-03", "Paying Off the US Debt at $1 Million a Day", [
    "[game announcer] New game! Pay off America's forty trillion dollar debt.",
    "[excited] You get one million dollars. Every. Single. Day.",
    "[fast] Day one, one million. Day one hundred, a hundred million.",
    "[confident] Keep going for your whole life. Eighty years.",
    "[nervous] Twenty-nine billion paid. Debt left? Still basically forty trillion.",
    "[shocked] You'd need about a hundred and nine thousand years.",
    "[deadpan] The pyramids aren't even five thousand years old. Game over."],
    [{"kind": "pixel", "line": 0, "from": 0, "hud_l": "DEBT", "hud_r": "LV 1", "start": 40e12, "to": 40e12, "msg": "PAY OFF $40 TRILLION", **B(mood="happy")},
     {"kind": "pixel", "line": 1, "from": 0, "hud_l": "+$1,000,000/DAY", "hud_r": "DAY 1", "start": 0, "to": 1e6, "dur": 0.8, "msg": "PAID SO FAR"},
     {"kind": "pixel", "line": 2, "from": 0, "hud_l": "PAID", "hud_r": "DAY 100", "start": 1e6, "to": 100e6, "dur": 2.0, "msg": "PAID SO FAR", **B(mood="proud")},
     {"kind": "pixel", "line": 3, "from": 0, "hud_l": "PAID", "hud_r": "YEAR 80", "start": 100e6, "to": 29.2e9, "dur": 2.0, "msg": "A WHOLE LIFETIME"},
     {"kind": "pixel", "line": 4, "from": 0, "hud_l": "DEBT LEFT", "hud_r": "YEAR 80", "start": 40e12, "to": 39.97e12, "dur": 1.5, "msg": "STILL ~$40 TRILLION", **B(mood="confused")},
     {"kind": "kinetic", "line": 5, "from": 0, "bgcol": [[18, 16, 48], [60, 16, 60]], "words": [{"t": "109,514", "size": 220, "c": [255, 205, 60], "font": "Pixel"}, {"t": "YEARS", "size": 120, "font": "Pixel"}]},
     {"kind": "kinetic", "line": 6, "from": 0, "bgcol": [[0, 0, 0], [30, 0, 0]], "words": [{"t": "GAME", "size": 170, "font": "Pixel", "c": [235, 64, 52]}, {"t": "OVER", "size": 170, "font": "Pixel", "c": [235, 64, 52]}], **B(mood="dizzy")}],
    [{"line": 0, "frac": 0.0, "name": "coin", "gain": 0.3}, {"line": 1, "word": "every", "name": "coin", "gain": 0.3}, {"line": 2, "frac": 0.3, "name": "coin", "gain": 0.3},
     {"line": 5, "frac": 0.0, "name": "subboom", "gain": 0.35}, {"line": 6, "word": "over", "name": "buzzer", "gain": 0.3}],
    {"hot": ["DEBT", "MILLION", "YEARS", "OVER"], "cap_y": 0.93},
    reacts=[(0, 0.6, "point", "$40,000,000,000,000"), (3, 0.6, "happy", "80 YEARS"), (5, 0.55, "shocked", "109,514 YRS")])

# B04 RECEIPT — America's Cyber Week receipt
spec("BK-04", "America's Cyber Week Receipt: $44.2 Billion", [
    "[cheerful] Here's America's receipt for Cyber Week, last year.",
    "[reading] Black Friday, online: eleven point eight billion.",
    "[reading] Cyber Monday: fourteen point two five billion. The biggest online shopping day ever.",
    "[reading] The other three days: eighteen billion more.",
    "[shocked] Total? Forty-four point two billion dollars. In five days.",
    "[sly] And over one billion of Cyber Monday was buy now, pay later.",
    "[teasing] This year's receipt prints next week. Guess the total in the comments."],
    [{"kind": "receipt", "line": 0, "from": 0, "title": "CYBER WEEK 2025", "sub": "U.S. ONLINE SALES - ADOBE", "rows": [], "total": "...", "step": 0.5},
     {"kind": "receipt", "line": 1, "from": 0, "title": "CYBER WEEK 2025", "sub": "U.S. ONLINE SALES - ADOBE", "rows": [["BLACK FRIDAY", "$11.80B"]], "total": "...", "step": 0.3},
     {"kind": "receipt", "line": 2, "from": 0, "title": "CYBER WEEK 2025", "sub": "U.S. ONLINE SALES - ADOBE", "rows": [["BLACK FRIDAY", "$11.80B"], ["CYBER MONDAY", "$14.25B"]], "total": "...", "step": 0.01},
     {"kind": "receipt", "line": 3, "from": 0, "title": "CYBER WEEK 2025", "sub": "U.S. ONLINE SALES - ADOBE", "rows": [["BLACK FRIDAY", "$11.80B"], ["CYBER MONDAY", "$14.25B"], ["OTHER 3 DAYS", "$18.15B"]], "total": "...", "step": 0.01},
     {"kind": "receipt", "line": 4, "from": 0, "title": "CYBER WEEK 2025", "sub": "U.S. ONLINE SALES - ADOBE", "rows": [["BLACK FRIDAY", "$11.80B"], ["CYBER MONDAY", "$14.25B"], ["OTHER 3 DAYS", "$18.15B"]], "total": "$44.20B", "stamp": "5 DAYS", "step": 0.01},
     {"kind": "stamp", "line": 5, "from": 0, "set": "pink", "kicker": "CYBER MONDAY 2025:", "claim": "$1.03 BILLION\nWAS 'PAY LATER'", "verdict": "BNPL", "at": 1.2, **B(mood="sideeye")},
     {"kind": "kinetic", "line": 6, "from": 0, "bgcol": [[40, 34, 30], [18, 16, 14]], "words": [{"t": "2026 TOTAL?", "size": 150, "c": [255, 205, 60], "font": "Courier"}, {"t": "COMMENT YOUR GUESS", "size": 80, "font": "Courier"}], **B(mood="point")}],
    [{"line": 1, "frac": 0.0, "name": "tick", "gain": 0.2, "dur": 0.4}, {"line": 2, "frac": 0.0, "name": "tick", "gain": 0.2, "dur": 0.4}, {"line": 3, "frac": 0.0, "name": "tick", "gain": 0.2, "dur": 0.4},
     {"line": 4, "word": "total", "name": "cash", "gain": 0.35}, {"line": 4, "frac": 0.7, "name": "impact", "gain": 0.3}, {"line": 5, "frac": 0.3, "name": "impact", "gain": 0.3}],
    {"hot": ["BILLION", "TOTAL", "LATER"]},
    reacts=[(2, 0.6, "shocked", "$14.25B IN 1 DAY"), (4, 0.6, "dizzy", "$44.2B"), (6, 0.55, "point", "???")])

# B05 QUIZ — guess Cyber Monday
spec("BK-05", "Guess How Much America Spent Online in ONE Day", [
    "[challenging] Quick! How much did Americans spend online on Cyber Monday last year?",
    "[playful] A, one point four billion. B, fourteen billion. C, a hundred forty billion.",
    "[drumroll] Three... two... one...",
    "[excited] B! Fourteen point two five billion dollars. In one day.",
    "[shocked] That's a hundred sixty-four thousand dollars every second.",
    "[teasing] Did you get it? Comment A, B or C. No lying."],
    [{"kind": "kinetic", "line": 0, "from": 0, "bgcol": [[90, 30, 160], [30, 20, 90]], "words": [{"t": "GUESS", "size": 200, "c": [255, 205, 60]}, {"t": "CYBER MONDAY", "size": 120}, {"t": "IN ONE DAY", "size": 120}], **B(mood="sideeye")},
     {"kind": "quiz", "line": 1, "from": 0, "bgcol": [[90, 30, 160], [30, 20, 90]], "q": "CYBER MONDAY 2025:\nU.S. ONLINE SPENDING?", "options": ["$1.4 BILLION", "$14 BILLION", "$140 BILLION"], "answer": 1, "reveal_at": 99, "timer": False, "buck": {"x": 0.5, "y": 1.0, "h": 640, "mood": "point"}},
     {"kind": "quiz", "line": 2, "from": 0, "bgcol": [[90, 30, 160], [30, 20, 90]], "q": "CYBER MONDAY 2025:\nU.S. ONLINE SPENDING?", "options": ["$1.4 BILLION", "$14 BILLION", "$140 BILLION"], "answer": 1, "reveal_at": 2.2, "intro": -2, "buck": {"x": 0.5, "y": 1.0, "h": 640, "mood": "confused"}},
     {"kind": "quiz", "line": 3, "from": 0, "bgcol": [[90, 30, 160], [30, 20, 90]], "q": "CYBER MONDAY 2025:\nU.S. ONLINE SPENDING?", "options": ["$1.4 BILLION", "$14 BILLION", "$140 BILLION"], "answer": 1, "reveal_at": 0.0, "intro": -2, "reveal": "$14.25 BILLION (ADOBE)", "buck": {"x": 0.5, "y": 1.0, "h": 600, "mood": "laugh"}},
     {"kind": "counter", "line": 4, "from": 0, "set": "pink", "to": 164931, "label": "EVERY SECOND", "dur": 2.0, "ticker": "+$164,931", **B(mood="shocked")},
     {"kind": "kinetic", "line": 5, "from": 0, "bgcol": [[90, 30, 160], [30, 20, 90]], "words": [{"t": "A? B? C?", "size": 190, "c": [255, 205, 60]}, {"t": "COMMENT", "size": 130}], **B(mood="laugh")}],
    [{"line": 0, "frac": 0.0, "name": "ding", "gain": 0.3}, {"line": 2, "frac": 0.0, "name": "tick", "gain": 0.25, "dur": 2.0}, {"line": 3, "frac": 0.0, "name": "ding", "gain": 0.35},
     {"line": 4, "frac": 0.2, "name": "cash", "gain": 0.3}],
    {"hot": ["GUESS", "BILLION", "SECOND"], "pause_before": {"3": 0.4}},
    reacts=[(1, 0.62, "point", "A, B OR C?"), (3, 0.6, "laugh", "$14.25B"), (4, 0.6, "dizzy", "$164,931/s")])

# B06 CHALK — credit card minimum math
spec("BK-06", "$1,000 on a Credit Card Costs You $833 Extra", [
    "[teacher voice] Class is in session. You put one thousand dollars on a credit card.",
    "[explaining] The average card that charges interest: twenty-two percent a year. That's the Fed's number.",
    "[calm] You pay twenty-five dollars a month. Sounds responsible.",
    "[building] It takes seventy-three months. Six years.",
    "[shocked] You pay back one thousand eight hundred thirty-three dollars.",
    "[serious] Eight hundred thirty-three dollars... just for waiting. Pay more than the minimum."],
    [{"kind": "chalk", "line": 0, "from": 0, "lines": [{"t": "LESSON: $1,000 ON A CARD", "c": "y", "u": True, "at": 0.2}], **B(mood="point")},
     {"kind": "chalk", "line": 1, "from": 0, "lines": [{"t": "LESSON: $1,000 ON A CARD", "c": "y", "u": True, "at": 0.0}, {"t": "APR = 22.15%", "c": "w", "at": 0.4, "size": 120}, {"t": "(Fed G.19, May 2026)", "c": "w", "at": 1.2, "size": 56}]},
     {"kind": "chalk", "line": 2, "from": 0, "lines": [{"t": "LESSON: $1,000 ON A CARD", "c": "y", "u": True, "at": 0.0}, {"t": "APR = 22.15%", "c": "w", "at": 0.0, "size": 120}, {"t": "PAY $25 / MONTH", "c": "w", "at": 0.3, "size": 110}], **B(mood="happy")},
     {"kind": "chalk", "line": 3, "from": 0, "lines": [{"t": "PAY $25 / MONTH", "c": "w", "at": 0.0, "size": 110}, {"t": "= 73 MONTHS", "c": "y", "at": 0.3, "size": 140}, {"t": "(6 YEARS)", "c": "w", "at": 1.0, "size": 90}]},
     {"kind": "chalk", "line": 4, "from": 0, "lines": [{"t": "YOU PAY BACK:", "c": "w", "at": 0.1, "size": 100}, {"t": "$1,833", "c": "r", "at": 0.6, "size": 220, "u": True}], **B(mood="shocked")},
     {"kind": "chalk", "line": 5, "from": 0, "lines": [{"t": "$833 = INTEREST", "c": "r", "at": 0.1, "size": 130, "u": True}, {"t": "PAY MORE THAN", "c": "y", "at": 1.2, "size": 110}, {"t": "THE MINIMUM", "c": "y", "at": 1.6, "size": 110}], **B(mood="sideeye")}],
    [{"line": 0, "frac": 0.0, "name": "scratch", "gain": 0.2}, {"line": 3, "frac": 0.2, "name": "scratch", "gain": 0.2}, {"line": 4, "frac": 0.5, "name": "subboom", "gain": 0.35}, {"line": 5, "frac": 0.0, "name": "impact", "gain": 0.3}],
    {"hot": ["INTEREST", "PERCENT", "MINIMUM"], "pause_before": {"4": 0.4}},
    reacts=[(1, 0.6, "confused", "22.15%"), (3, 0.55, "sad", "6 YEARS"), (5, 0.6, "angry", "+$833")])

# B07 BARS — money per second ranking
spec("BK-07", "Who Makes the Most Money Per Second?", [
    "[energetic] Money per second. Who wins?",
    "[fast] Elon Musk's fortune dropped sixty-eight billion in one month. That's twenty-five thousand dollars a second.",
    "[fast] GTA 6 on day one: forty-three thousand dollars every second.",
    "[fast] The US debt in the last year: seventy-six thousand dollars a second.",
    "[shocked] And the winner... Cyber Monday shoppers. A hundred sixty-four thousand dollars a second!",
    "[grinning] Shoppers beat billionaires. Follow for more money facts."],
    [{"kind": "kinetic", "line": 0, "from": 0, "bgcol": [[10, 30, 60], [10, 10, 30]], "words": [{"t": "$ PER", "size": 200, "c": [255, 205, 60]}, {"t": "SECOND", "size": 200}], **B(mood="point")},
     {"kind": "bars", "line": 1, "from": 0, "bgcol": [[10, 30, 60], [10, 10, 30]], "title": "DOLLARS PER SECOND", "items": [["MUSK'S OCT DROP", 25388, [120, 120, 140]]]},
     {"kind": "bars", "line": 2, "from": 0, "bgcol": [[10, 30, 60], [10, 10, 30]], "title": "DOLLARS PER SECOND", "items": [["GTA 6 DAY ONE", 43866, [80, 160, 240]], ["MUSK'S OCT DROP", 25388, [120, 120, 140]]], "stagger": 0},
     {"kind": "bars", "line": 3, "from": 0, "bgcol": [[10, 30, 60], [10, 10, 30]], "title": "DOLLARS PER SECOND", "items": [["US DEBT GROWTH", 76738, [220, 70, 60]], ["GTA 6 DAY ONE", 43866, [80, 160, 240]], ["MUSK'S OCT DROP", 25388, [120, 120, 140]]], "stagger": 0},
     {"kind": "bars", "line": 4, "from": 0, "bgcol": [[10, 30, 60], [10, 10, 30]], "title": "DOLLARS PER SECOND", "items": [["CYBER MONDAY", 164931, [46, 204, 113]], ["US DEBT GROWTH", 76738, [220, 70, 60]], ["GTA 6 DAY ONE", 43866, [80, 160, 240]], ["MUSK'S OCT DROP", 25388, [120, 120, 140]]], "stagger": 0, **B(mood="shocked")},
     {"kind": "kinetic", "line": 5, "from": 0, "bgcol": [[46, 160, 90], [10, 60, 30]], "words": [{"t": "SHOPPERS", "size": 170, "c": [255, 205, 60]}, {"t": "BEAT", "size": 150}, {"t": "BILLIONAIRES", "size": 140}], **B(mood="laugh")}],
    [{"line": 0, "frac": 0.0, "name": "whoosh", "gain": 0.3}, {"line": 1, "frac": 0.0, "name": "slide_up", "gain": 0.2}, {"line": 2, "frac": 0.0, "name": "slide_up", "gain": 0.2},
     {"line": 3, "frac": 0.0, "name": "slide_up", "gain": 0.2}, {"line": 4, "frac": 0.4, "name": "impact", "gain": 0.35}, {"line": 5, "frac": 0.0, "name": "ding", "gain": 0.3}],
    {"hot": ["SECOND", "WINNER", "BILLIONAIRES"]},
    reacts=[(1, 0.6, "sad", "-$68B IN A MONTH"), (3, 0.6, "angry", "$2.42T IN A YEAR"), (4, 0.62, "dizzy", "$164,931/s")])

# B08 VERSUS — Thanksgiving 2022 record vs 2026
spec("BK-08", "Thanksgiving Dinner Got CHEAPER Than 2022", [
    "[curious] Thanksgiving dinner for ten. 2022 versus this year. Which costs more?",
    "[announcer] In 2022, the record: sixty-four dollars and five cents.",
    "[announcer] This year: fifty-eight sixty-three.",
    "[surprised] It's five dollars cheaper than the record!",
    "[sly] But the turkey alone went up. Twenty-one fifty last year, twenty-three sixty-eight now.",
    "[cheerful] Five eighty-six a person. Tell me what your dinner costs."],
    [{"kind": "kinetic", "line": 0, "from": 0, "set": "peach", "words": [{"t": "2022", "size": 200, "c": [40, 110, 220]}, {"t": "VS", "size": 130, "font": "BlackOps"}, {"t": "2026", "size": 200, "c": [235, 120, 40]}], **B(mood="confused")},
     {"kind": "versus", "line": 1, "from": 0, "left": {"label": "2022 (RECORD)", "value": 64.05, "fmt": "${:,.2f}", "c": [40, 110, 220]}, "right": {"label": "2026", "value": 0.0, "fmt": "$?", "c": [235, 120, 40], "at": 99}},
     {"kind": "versus", "line": 2, "from": 0, "left": {"label": "2022 (RECORD)", "value": 64.05, "fmt": "${:,.2f}", "c": [40, 110, 220], "at": -2}, "right": {"label": "2026", "value": 58.63, "fmt": "${:,.2f}", "c": [235, 120, 40]}, **B(mood="happy")},
     {"kind": "versus", "line": 3, "from": 0, "left": {"label": "2022 (RECORD)", "value": 64.05, "fmt": "${:,.2f}", "c": [40, 110, 220], "at": -2}, "right": {"label": "2026", "value": 58.63, "fmt": "${:,.2f}", "c": [235, 120, 40], "at": -2}, "win": 1, "win_at": 0.3, "win_label": "-$5.42"},
     {"kind": "versus", "line": 4, "from": 0, "left": {"label": "TURKEY 2025", "value": 21.50, "fmt": "${:,.2f}", "c": [120, 80, 40]}, "right": {"label": "TURKEY 2026", "value": 23.68, "fmt": "${:,.2f}", "c": [200, 60, 40]}, "win": 1, "win_at": 2.0, "win_label": "+10%", **B(mood="sideeye")},
     {"kind": "counter", "line": 5, "from": 0, "set": "peach", "to": 5.86, "dec": 2, "label": "PER PERSON (AFBF 2026)", "dur": 1.2, **B(mood="thumbsup")}],
    [{"line": 0, "frac": 0.0, "name": "whoosh", "gain": 0.3}, {"line": 1, "frac": 0.5, "name": "ding", "gain": 0.25}, {"line": 2, "frac": 0.5, "name": "ding", "gain": 0.25}, {"line": 3, "frac": 0.1, "name": "impact", "gain": 0.3}, {"line": 4, "word": "twenty-three", "name": "boing", "gain": 0.25}],
    {"hot": ["CHEAPER", "RECORD", "TURKEY"]},
    reacts=[(0, 0.6, "point", "WHICH COSTS MORE?"), (3, 0.6, "laugh", "-$5.42"), (4, 0.62, "shocked", "$23.68")])

# B09 KINETIC 7 s — the last penny (loop)
spec("BK-09", "The Last Penny Cost 3.69 Cents to Make", [
    "[fast, punchy] This penny cost three point six nine cents to make. So America stopped making them. November twelfth, 2025.",
    "[deadpan] Worth one cent. Cost almost four."],
    [{"kind": "kinetic", "line": 0, "from": 0, "bgcol": [[150, 70, 30], [60, 25, 10]], "words": [{"t": "1¢ COIN", "size": 170}, {"t": "COST 3.69¢", "size": 170, "c": [255, 205, 60]}], **B(mood="shocked")},
     {"kind": "kinetic", "line": 0, "from": 0.45, "bgcol": [[20, 20, 20], [0, 0, 0]], "words": [{"t": "LAST ONE:", "size": 140, "font": "Abril"}, {"t": "NOV 12, 2025", "size": 150, "c": [255, 205, 60], "font": "Abril"}], "cap": True},
     {"kind": "stamp", "line": 1, "from": 0, "set": "peach", "kicker": "THE PENNY:", "claim": "WORTH 1¢\nCOST 3.69¢", "verdict": "LOSS", "at": 0.5, **B(mood="sideeye")}],
    [{"line": 0, "frac": 0.0, "name": "coin", "gain": 0.35}, {"line": 0, "frac": 0.45, "name": "impact", "gain": 0.3}, {"line": 1, "frac": 0.3, "name": "impact", "gain": 0.3}],
    {"hot": ["PENNY", "CENTS"], "tail": 0.6},
    reacts=[(0, 0.75, "dizzy", "3.69¢"), (1, 0.6, "laugh", "1¢")])

# B10 HOST — Buck talking head: GTA 6 pre-sales
spec("BK-10", "32.5 Million People Paid Before GTA 6 Even Existed", [
    "[amazed] Thirty-two point five million copies of GTA 6 were sold... before it even came out.",
    "[playful] That's about everyone in Texas. Paying for a game they hadn't played.",
    "[impressed] Then day one: three point seven nine billion dollars in sales.",
    "[sly] Biggest entertainment launch ever. Bigger than any movie opening.",
    "[teasing] Did you pre-order? Be honest."],
    [{"kind": "host", "line": 0, "from": 0, "set": "pink", "buck": {"mood": "shocked", "h": 1350}, "prop": "32,500,000", "prop_at": 0.2},
     {"kind": "counter", "line": 0, "from": 0.5, "set": "sky", "to": 32.5e6, "prefix": "", "label": "COPIES SOLD BEFORE LAUNCH", "dur": 1.5, "size": 150},
     {"kind": "host", "line": 1, "from": 0, "set": "peach", "buck": {"mood": "laugh", "h": 1350}, "bubble": "\"ABOUT EVERYONE IN TEXAS\""},
     {"kind": "counter", "line": 2, "from": 0, "set": "green", "to": 3.79e9, "label": "DAY ONE SALES (TAKE-TWO)", "dur": 1.6, "size": 130, **B(mood="proud")},
     {"kind": "kinetic", "line": 3, "from": 0, "bgcol": [[20, 10, 30], [60, 10, 40]], "words": [{"t": "BIGGEST", "size": 180, "c": [255, 205, 60]}, {"t": "ENTERTAINMENT", "size": 120}, {"t": "LAUNCH EVER", "size": 140}]},
     {"kind": "host", "line": 4, "from": 0, "set": "yellow", "buck": {"mood": "sideeye", "h": 1350}, "bubble": "DID YOU PRE-ORDER?"}],
    [{"line": 0, "frac": 0.0, "name": "impact", "gain": 0.3}, {"line": 2, "frac": 0.2, "name": "cash", "gain": 0.3}, {"line": 3, "frac": 0.0, "name": "subboom", "gain": 0.3}, {"line": 4, "frac": 0.2, "name": "boing", "gain": 0.25}],
    {"hot": ["MILLION", "BILLION", "EVER"]},
    reacts=[(2, 0.6, "dizzy", "$3.79B"), (3, 0.6, "smug", "#1 EVER")])
print("ok")

# ---- post-process (kept here so a rebuild never loses it) ----
M = [[10, "CLOUDS 10 KM"], [100, "SPACE 100 KM"], [408, "SPACE STATION 408 KM"], [35786, "SATELLITES 35,786 KM"]]
P = lambda k: json.load(open(os.path.join(D, k + ".json")))
def W_(k, d): json.dump(d, open(os.path.join(D, k + ".json"), "w"), indent=1)
d = P("bk01")
d["shots"] = [s for s in d["shots"] if not (s["kind"] == "kinetic" and s["line"] == 0)]
d["shots"].insert(0, {"kind": "kinetic", "line": 0, "from": 0, "set": "sky", "words": [{"t": "$40,000,000,000,000", "size": 110, "c": [255, 205, 60]}, {"t": "IN $100 BILLS", "size": 120}], "buck": {"x": 0.82, "y": 0.99, "h": 560, "mood": "shocked"}})
d["shots"].insert(1, {"kind": "scale", "line": 0, "from": 0.45, "stack_m": 43688, "unit": "km", "stack_label": "$40T IN $100s", "marks": M, "lo": 0.1, "dur": 9.0, "at": 0.0, "title": "HOW TALL IS $40 TRILLION?"})
for s in d["shots"]:
    if s["kind"] == "scale" and s["line"] == 1: s.update({"cont": True, "marks": M, "lo": 0.1, "dur": 9.0, "at": 0.0})
W_("bk01", d)
d = P("bk02")
for s in d["shots"]:
    if s["kind"] == "spend": s["who"] = "MUSK'S FORTUNE (FORBES, NOV 1)"; s["buck"] = {"x": 0.5, "y": 1.0, "h": 560, "mood": "laugh"}
W_("bk02", d)
d = P("bk07")
for s in d["shots"]:
    if s["kind"] == "bars": s["new"] = 0; s.pop("stagger", None)
W_("bk07", d)
d = P("bk04")
for s in d["shots"]:
    if s["kind"] == "receipt" and s["line"] > 0: s["step"] = 0.01
W_("bk04", d)
# stylised formats alternate with footage lines (>= 40 %)
def swap(k, line, shot):
    d = P(k); d["shots"] = [x for x in d["shots"] if not (x.get("line") == line and x.get("from", 0) == 0 and x["kind"] != "end")] + [dict(shot, line=line, **{"from": 0})]
    d["shots"].sort(key=lambda x: (x["line"], 9 if x["kind"] == "end" else x.get("from", 0))); W_(k, d)
swap("bk03", 1, {"kind": "counter", "to": 1e6, "label": "+$1,000,000 EVERY DAY", "dur": 1.0, "ticker": "+$1M", "rate": 1.5, "buck": {"x": 0.82, "y": 0.99, "h": 560, "mood": "happy"}})
swap("bk04", 0, {"kind": "kinetic", "words": [{"t": "AMERICA'S", "size": 150}, {"t": "CYBER WEEK", "size": 150, "c": [255, 205, 60]}, {"t": "RECEIPT", "size": 170}], "buck": {"x": 0.82, "y": 0.99, "h": 560, "mood": "happy"}})
swap("bk06", 0, {"kind": "kinetic", "words": [{"t": "LESSON:", "size": 130, "font": "Hand"}, {"t": "$1,000", "size": 230, "c": [255, 205, 60]}, {"t": "ON A CARD", "size": 150}], "buck": {"x": 0.82, "y": 0.99, "h": 600, "mood": "point"}})
swap("bk06", 2, {"kind": "counter", "to": 25, "label": "YOU PAY EACH MONTH", "dur": 0.8, "sub": "SOUNDS RESPONSIBLE...", "buck": {"x": 0.82, "y": 0.99, "h": 560, "mood": "happy"}})
swap("bk06", 4, {"kind": "counter", "to": 1833, "label": "YOU PAY BACK", "dur": 1.4, "color": [235, 64, 52], "buck": {"x": 0.82, "y": 0.99, "h": 600, "mood": "shocked"}})
swap("bk07", 1, {"kind": "counter", "to": 25388, "label": "MUSK'S OCTOBER DROP", "sub": "PER SECOND (-$68B IN A MONTH)", "dur": 1.5, "color": [235, 64, 52], "buck": {"x": 0.82, "y": 0.99, "h": 560, "mood": "sad"}})
# real footage behind the graphics (script_check: >= 40 % full-screen footage; empty_check: no flat panels)
POOL = {"bk01": ["cash_count", "cash_stacks", "atm_use", "coins_hand", "wallet_empty"], "bk02": ["cash_count", "gamepad_hands", "online_card", "cart_pov", "atm_use"],
        "bk03": ["cash_count", "calendar_flip", "wallet_empty", "atm_use"], "bk04": ["online_card", "laptop_phone", "cart_pov", "pay_terminal", "phone_scroll"],
        "bk05": ["laptop_phone", "online_card", "typing_keys", "cart_pov", "phone_scroll"], "bk06": ["online_card", "pay_terminal", "wallet_empty", "atm_use"],
        "bk07": ["cash_count", "gamepad_hands", "online_card", "cart_pov", "pay_terminal"], "bk08": ["cart_pov", "cart_empty", "cash_count", "wallet_empty", "coffee_pour"],
        "bk09": ["coins_hand", "cash_count", "wallet_empty"], "bk10": ["gamepad_hands", "tv_remote", "typing_keys", "laptop_phone", "phone_scroll"]}
for k, pool in POOL.items():
    d = P(k); d["pool"] = pool; i = 0
    for s in d["shots"]:
        if s["kind"] in ("chalk", "pixel", "receipt", "end", "scale") or s.get("bg"): continue
        s["bg"] = f"/tmp/fin/bg/bank/{pool[i % len(pool)]}.mp4"; s["bg_start"] = (7.0 if "cash_stacks" in pool[i % len(pool)] else 1.0) + (i * 1.7) % 4; s.pop("set", None); s.pop("bgcol", None)
        if s["kind"] == "host": s["dim"] = 30
        i += 1
    W_(k, d)
print("post-process ok")
