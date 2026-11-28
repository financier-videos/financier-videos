import json
# BK-16: Adobe 2026 holiday forecast ($275.1B online, Nov 1 - Dec 31) stacked in $100 bills -> 186.7 miles tall.
G = "/tmp/fin/bg/b16/"
bk = lambda m: {"x": 0.82, "y": 0.99, "h": 560, "mood": m}
host = lambda line, frm, mood, bg, st=1.0, prop=None: dict({"kind": "host", "line": line, "from": frm, "buck": {"mood": mood, "h": 1300, "y": 1.04}, "bg": G + bg, "bg_start": st, "dim": 20}, **({"prop": prop} if prop else {}))
lines = [
    ["B", "[excited] [fast] Two hundred seventy-five billion dollars in hundred-dollar bills!"],
    ["B", "[fast] That's what Americans are expected to spend online by New Year's."],
    ["B", "[deadpan] One bill is four thousandths of an inch thick. Basically nothing."],
    ["B", "[building suspense] Now stack two point seven five billion of them. Past the clouds."],
    ["B", "[shocked] Past Mount Everest. Almost thirty-four Everests tall!"],
    ["B", "[excited] At sixty-two miles it hits the edge of space. And it keeps going."],
    ["B", "[whisper] It finally stops at about a hundred eighty-seven miles."],
    ["B", "[deadpan] It weighs around three thousand tons. Free shipping, obviously."],
    ["B", "[sly] And all of it starts with one tiny button. Add to cart."]]
Y = [255, 205, 60]; GR = [80, 200, 120]; R = [235, 64, 52]; WH = [240, 240, 240]
MARKS = [[5.5, "EVEREST 5.5 MI"], [62, "EDGE OF SPACE 62 MI"], [250, "SPACE STATION ~250 MI"]]
shots = [
    # 0: hook - bright bills, the full number slams in at the top third, Buck reacts before 1 s
    {"kind": "kinetic", "line": 0, "from": 0, "y": 0.2, "words": [{"t": "$275,100,000,000", "size": 118, "c": Y, "at": 0.0}], "bg": G + "bills.mp4", "bg_start": 0.5, "dim": 40},
    {"kind": "kinetic", "line": 0, "from": 0.17, "y": 0.2, "words": [{"t": "$275 BILLION", "size": 140, "c": Y, "at": 0.0}], "bg": G + "bills.mp4", "bg_start": 6.0, "dim": 20, "buck": bk("shocked")},
    {"kind": "kinetic", "line": 0, "from": 0.62, "y": 0.2, "words": [{"t": "IN $100 BILLS", "size": 130, "c": GR}], "bg": G + "bills.mp4", "bg_start": 4.0, "dim": 40},
    # 1: what it is - Adobe forecast
    {"kind": "kinetic", "line": 1, "from": 0, "y": 0.25, "words": [{"t": "SPENT ONLINE", "size": 120}, {"t": "NOV 1 - DEC 31", "size": 100, "c": Y}], "bg": G + "phone.mp4", "bg_start": 1.0, "dim": 30},
    host(1, 0.5, "point", "conveyor.mp4", 0.5),
    # 2: one bill - joke
    {"kind": "kinetic", "line": 2, "from": 0, "y": 0.22, "words": [{"t": "0.0043 INCHES", "size": 130, "c": Y}, {"t": "PER BILL", "size": 100}], "bg": G + "bills.mp4", "bg_start": 2.0, "dim": 60, "buck": bk("sideeye")},
    host(2, 0.62, "smug", "bills.mp4", 7.0, "BASICALLY NOTHING"),
    # 3: the stack climbs (scale ruler, miles) over clouds
    {"kind": "scale", "line": 3, "from": 0, "stack_m": 186.7, "unit": "mi", "lo": 0.01, "at": 0.0, "dur": 9.5, "stack_label": "2.75 BILLION $100s", "marks": MARKS, "bg": G + "clouds.mp4", "bg_start": 0.5},
    host(3, 0.6, "proud", "clouds.mp4", 3.0, "PAST THE CLOUDS"),
    # 4: Everest
    {"kind": "kinetic", "line": 4, "from": 0, "y": 0.2, "words": [{"t": "34 x", "size": 190, "c": Y}, {"t": "MOUNT EVEREST", "size": 110}], "bg": G + "peaks.mp4", "bg_start": 0.5, "dim": 30},
    host(4, 0.55, "shocked", "peaks.mp4", 4.0),
    # 5: edge of space - ruler continues, then the rocket
    {"kind": "scale", "line": 5, "from": 0, "stack_m": 186.7, "unit": "mi", "lo": 0.01, "at": -5.0, "dur": 9.5, "stack_label": "2.75 BILLION $100s", "marks": MARKS, "bg": G + "earth.mp4", "bg_start": 0.5},
    {"kind": "kinetic", "line": 5, "from": 0.55, "y": 0.2, "words": [{"t": "AND IT", "size": 110}, {"t": "KEEPS GOING", "size": 140, "c": R}], "bg": G + "rocket.mp4", "bg_start": 2.0, "dim": 30, "buck": bk("shocked")},
    # 6: final height
    {"kind": "kinetic", "line": 6, "from": 0, "y": 0.2, "words": [{"t": "186.7", "size": 200, "c": Y}, {"t": "MILES TALL", "size": 120}], "bg": G + "clouds.mp4", "bg_start": 5.5, "dim": 30},
    host(6, 0.55, "laugh", "peaks.mp4", 6.5, "3x PAST SPACE"),
    # 7: weight joke
    {"kind": "kinetic", "line": 7, "from": 0, "y": 0.2, "words": [{"t": "~3,000 TONS", "size": 150, "c": Y}], "bg": G + "trucks.mp4", "bg_start": 1.0, "dim": 30},
    host(7, 0.55, "sideeye", "trucks.mp4", 4.0, "FREE SHIPPING!"),
    # 8: loop back to the hook
    {"kind": "kinetic", "line": 8, "from": 0, "y": 0.22, "words": [{"t": "ADD TO CART", "size": 150, "c": GR}], "bg": G + "phone.mp4", "bg_start": 4.0, "dim": 20, "buck": bk("sly")},
    {"kind": "kinetic", "line": 8, "from": 0.7, "y": 0.2, "words": [{"t": "$275,100,000,000", "size": 118, "c": Y, "at": 0.0}], "bg": G + "bills.mp4", "bg_start": 0.5, "dim": 40}]
spec = {"topline": [{"t": "HOLIDAY SHOPPING 2026 · ONLINE · USA", "at": 0}], "id": "BK-16", "title": "$275 Billion in $100 Bills Reaches Space",
        "brand": ["FINANCIER", Y], "tail": 0.6, "speed": 1.22, "amb": "room", "grade": "lime",
        "lines": lines, "pool": ["b16_clouds", "b16_peaks", "b16_trucks", "b16_bills", "b16_conveyor"], "hot": ["BILLION", "EVEREST", "SPACE", "TONS", "CART"], "cap_y": 0.93,
        "sfx": [{"line": 0, "frac": 0.0, "name": "impact", "gain": 0.32}, {"line": 2, "frac": 0.7, "name": "boing", "gain": 0.25},
                {"line": 3, "frac": 0.0, "name": "riser", "gain": 0.25}, {"line": 4, "frac": 0.0, "name": "subboom", "gain": 0.35},
                {"line": 5, "frac": 0.55, "name": "whip", "gain": 0.3}, {"line": 7, "frac": 0.6, "name": "coin", "gain": 0.3}],
        "visual_hook": {"type": "B", "frame1": "bright pile of real $100 bills, the full number $275,100,000,000 already slamming in at the top third", "event_at": 0.9,
                        "question": "how big is $275 billion?"},
        "source_titles": [],
        "sources": "Adobe Digital Insights 2026 holiday forecast (Sept 28, 2026): $275.1B U.S. online spend Nov 1-Dec 31 (forecast). BEP: note thickness 0.0043 in, weight ~1 g. Our math: $275.1B / $100 = 2.751B notes x 0.0043 in = 11.83M in = 186.7 mi; Everest 29,032 ft = 5.50 mi -> 33.9x; Karman line 100 km = 62 mi; 2.751B g = 2,751 metric t = ~3,030 US tons.",
        "shots": shots}
json.dump(spec, open("bk16.json", "w"), indent=1)
