"""10 Rocco episodes, 10 different formats (2026-11-22, benchmarks: docs/competitor_watch.md rows of 2026-11-22)."""
import json, os
D = os.path.dirname(os.path.abspath(__file__)); A = "/home/user/financier-videos/assets/toon3d/"
CC, PR, OF, NI, YA, PO, ST, GS, IN, VIP = (A + x + ".jpg" for x in ("slick_callcenter3d", "penny_room3d", "rocco_office3d", "penny_night3d", "slick_yacht3d", "porch3d", "street_door3d", "gameshow3d", "interrogation3d", "slick_vip3d"))


def s(kind, line, frm, bg=None, **k):
    d = {"kind": kind, "line": line, "from": frm, "blur": 1}
    if bg: d["bg"] = bg
    d.update(k); return d


def end(line, bg, l1, l2, l3): return {"kind": "end", "bg": bg, "blur": 2, "line": line, "from": 1.0, "l1": l1, "l2": l2, "l3": l3}


def out(id_, title, lines, shots, sfx, **extra):
    sp = {"id": id_, "title": title, "style": "rocco3d", "tail": 1.6, "speed": 1.06, "amb": "room", "lines": lines, "shots": shots, "sfx": sfx}
    sp.update(extra); json.dump(sp, open(os.path.join(D, id_.lower().replace("-", "") + ".json"), "w"), indent=1)


NOTE = lambda lines: [{"t": "SLICK'S NOTES:", "c": "y", "u": True, "at": -1, "size": 90}] + lines

# RC-13 spelled-out trap call (N09VNM2BOD8 5M, Dcy3hSMxYop 2.2M)
out("RC-13", "The Scammer Wrote Down Her Card Number", [
    ["S", "[smooth, fake official] Hello! Bank fraud department. Read me your card number, please."],
    ["P", "[whispering, nervous] Rocco... the bank wants my card number."],
    ["R", "[whispering, sly] Give him this one. Slowly."],
    ["P", "[slow, careful] Okay... R."],
    ["S", "[writing] R. Got it."],
    ["P", "[slowly] E... D."],
    ["S", "[writing, impatient] E, D. Go on, go on."],
    ["P", "[trying not to laugh] F... L... A... G."],
    ["S", "[proud] Perfect! R, E, D... F, L, A, G."],
    ["S", "[realizing, horrified] ...Wait. RED FLAG?!"],
    ["R", "[deadpan] Banks never ask for your card number on a call. Hang up."],
    ["S", "[whiny] Not again!"]],
    [s("call", 0, 0, PR, bg2=CC, s="sly", s_pose="point", p="happy", r="sly", r_whisper=True, caller='CALLER: "YOUR BANK"', hook="SCAM LIKELY \U0001F4DE".replace("\U0001F4DE", "")),
     s("cu_p", 1, 0, PR, p="shock", r="sideeye", cam={"z": 1.2, "push": 0.06, "fy": 0.42}),
     s("cu_r", 2, 0, OF, r="sly", r_pose="point", cam={"z": 1.3, "push": 0.1, "fy": 0.47}),
     s("cu_p", 3, 0, PR, p="sly", r="sly", cam={"z": 1.25, "push": 0.05, "fy": 0.42}),
     s("chalk", 4, 0, None, lines=NOTE([{"t": "R", "c": "w", "at": 0.05, "size": 260}]), cast=[{"who": "slick", "x": 0.8, "y": 0.99, "h": 900, "mood": "sly"}]),
     s("cu_p", 5, 0, PR, p="sly", r="sly", cam={"z": 1.15, "push": 0.05, "fy": 0.42}),
     s("chalk", 6, 0, None, lines=NOTE([{"t": "R E D", "c": "w", "at": -1, "size": 260}]), cast=[{"who": "slick", "x": 0.8, "y": 0.99, "h": 900, "mood": "happy"}]),
     s("cu_p", 7, 0, PR, p="happy", r="sly", p_pose="point", cam={"z": 1.3, "push": 0.05, "fy": 0.42}),
     s("chalk", 8, 0, None, lines=NOTE([{"t": "R E D", "c": "w", "at": -1, "size": 260}, {"t": "F L A G", "c": "r", "at": 0.3, "size": 260}]), cast=[{"who": "slick", "x": 0.8, "y": 0.99, "h": 900, "mood": "happy", "pose": "arms_up"}]),
     s("kinetic", 9, 0, None, bgcol=[[120, 10, 10], [30, 0, 0]], words=[{"t": "RED", "size": 300, "c": [235, 64, 52], "font": "BlackOps"}, {"t": "FLAG", "size": 300, "c": [235, 64, 52], "font": "BlackOps"}], cast=[{"who": "slick", "x": 0.5, "y": 1.02, "h": 1000, "mood": "shock", "pose": "arms_up"}]),
     s("store", 10, 0, OF, blur=3, l1="BANKS NEVER ASK FOR", l2="YOUR CARD ON A CALL", r="happy"),
     s("slick", 11, 0, CC, s="panic", s_pose="shrug", msg="NOT AGAIN!", msg_at=0.2),
     end(11, PR, '"READ ME YOUR CARD NUMBER"', "= SCAM", "Send this to someone who answers unknown numbers.")],
    [{"line": 0, "frac": 0.0, "name": "ding", "gain": 0.3}, {"line": 4, "frac": 0.1, "name": "scratch", "gain": 0.2}, {"line": 6, "frac": 0.1, "name": "scratch", "gain": 0.2},
     {"line": 8, "frac": 0.3, "name": "scratch", "gain": 0.2}, {"line": 9, "frac": 0.2, "name": "subboom", "gain": 0.4}, {"line": 11, "frac": 0.6, "name": "wahwah", "gain": 0.35}],
    hot=["RED", "FLAG", "CARD", "BANK"], pause_before={"9": 0.5}, amb="lair")

# RC-14 silent karma allegory (DdGowjqMDqS 13.4M)
T = lambda a, b, **k: dict({"t0": a, "t1": b, "blur": 1}, **k)
out("RC-14", "He Promised to Double Her Coins", [["R", "[quiet, dry] Karma doesn't take crypto."]],
    [dict(T(0, 2.2, kind="slick", bg=YA, s="sly", s_pose="point", cap=False)),
     dict(T(2.2, 4.2, kind="cu_p", bg=PR, p="happy", r="sideeye", p_pose="arms_up", cap=False)),
     dict(T(4.2, 6.2, kind="slick", bg=YA, s="happy", s_pose="arms_up", msg="x2 GUARANTEED!", msg_at=0.2, cap=False)),
     dict(T(6.2, 8.2, kind="cu_p", bg=PR, p="sly", r="sly", p_pose="point", cap=False)),
     dict(T(8.2, 10.2, kind="stamp", set="pink", kicker="SLICK'S PROOF:", claim="\"TRUST ME\"", verdict="MYTH", at=0.6, cast=[{"who": "slick", "x": 0.5, "y": 1.02, "h": 900, "mood": "shock", "pose": "shrug"}], cap=False)),
     dict(T(10.2, 12.2, kind="kinetic", bgcol=[[30, 20, 60], [10, 5, 20]], words=[{"t": "KARMA", "size": 260, "c": [255, 205, 60], "font": "Abril"}], cast=[{"who": "slick", "x": 0.5, "y": 1.02, "h": 1000, "mood": "shock", "pose": "arms_up"}], cap=False)),
     {"kind": "cu_r", "bg": OF, "line": 0, "from": 0, "r": "sly", "cam": {"z": 1.3, "push": 0.1, "fy": 0.47}},
     end(0, PR, "\"DOUBLE YOUR MONEY, GUARANTEED\"", "= SCAM", "Send this to someone who loves easy money.")],
    [{"line": 0, "frac": 0.0, "dt": -12.0, "name": "coin", "gain": 0.3}, {"line": 0, "frac": 0.0, "dt": -9.8, "name": "shimmer", "gain": 0.25}, {"line": 0, "frac": 0.0, "dt": -7.8, "name": "cash", "gain": 0.3},
     {"line": 0, "frac": 0.0, "dt": -5.8, "name": "crickets", "gain": 0.25}, {"line": 0, "frac": 0.0, "dt": -3.4, "name": "buzzer", "gain": 0.3}, {"line": 0, "frac": 0.0, "dt": -1.8, "name": "subboom", "gain": 0.4},
     {"line": 0, "frac": 0.0, "dt": -1.6, "name": "bonk", "gain": 0.35}],
    pause_before={"0": 12.2}, tail=2.0, amb="room",
    topline=[{"t": "He promised to double her coins.", "at": 0.2}, {"t": "She only asked for proof.", "at": 6.2}, {"t": "Karma checked his math.", "at": 10.2}])

# RC-15 two are scams, one is real (jUF_JPKXTWc 7.5M)
M = lambda txt, c=(52, 120, 246): [{"t": txt, "at": 0.05, "col": list(c), "size": 76}]
out("RC-15", "Two of These Texts Are Scams. One Is Real.", [
    ["R", "[confident] Three texts. Two are scams. One is real. Watch."],
    ["P", "[reading] One. USPS: your package is on hold. Pay a one dollar thirty redelivery fee."],
    ["R", "[flat] Scam. USPS won't text you a link to pay a fee."],
    ["P", "[reading] Two. Bank alert: verify your login here, or your account closes today."],
    ["R", "[flat] Scam. A link plus a deadline. Classic."],
    ["P", "[reading, smiling] Three. Mom: are you coming for Thanksgiving? Bring pie."],
    ["R", "[warm] Real. No link. No money. Just pie."],
    ["P", "[relieved] So the only thing I have to worry about is... pie?"],
    ["R", "[deadpan] Bring two."]],
    [s("kinetic", 0, 0, None, bgcol=[[20, 40, 90], [10, 15, 40]], words=[{"t": "2 SCAMS", "size": 200, "c": [235, 64, 52]}, {"t": "1 REAL", "size": 200, "c": [46, 204, 113]}], cast=[{"who": "rocco", "x": 0.5, "y": 1.02, "h": 1000, "mood": "sly", "pose": "point"}], hook="CAN YOU SPOT THEM?"),
     s("phone", 1, 0, NI, p="happy", sender="USPS?", msgs=M("Your package is on hold.\nPay $1.30 redelivery fee:\nusps-redeliver.co")),
     s("stamp", 2, 0, None, set="sky", kicker="TEXT #1:", claim="USPS: PAY $1.30\nREDELIVERY FEE", verdict="SCAM", at=0.5, cast=[{"who": "rocco", "x": 0.82, "y": 1.0, "h": 760, "mood": "sideeye", "pose": "point"}]),
     s("phone", 3, 0, NI, p="shock", sender="B4nk Alert", msgs=M("Verify your login now or\nyour account closes TODAY:\nsecure-bank-login.net", (220, 60, 60))),
     s("stamp", 4, 0, None, set="pink", kicker="TEXT #2:", claim="VERIFY LOGIN\nOR ACCOUNT CLOSES", verdict="SCAM", at=0.4, cast=[{"who": "rocco", "x": 0.82, "y": 1.0, "h": 760, "mood": "sideeye"}]),
     s("phone", 5, 0, NI, p="happy", sender="Mom", msgs=M("Are you coming for\nThanksgiving? Bring pie", (52, 199, 89))),
     s("stamp", 6, 0, None, set="green", kicker="TEXT #3:", claim="MOM: BRING PIE", verdict="REAL", at=0.4, cast=[{"who": "rocco", "x": 0.82, "y": 1.0, "h": 760, "mood": "happy", "pose": "arms_up"}]),
     s("two", 7, 0, NI, p="happy", r="sly"),
     s("cu_r", 8, 0, OF, r="sly", cam={"z": 1.35, "push": 0.1, "fy": 0.47}),
     end(8, NI, "LINK + MONEY OR DEADLINE", "= SCAM", "Send this to someone who gets 'package on hold' texts.")],
    [{"line": 1, "frac": 0.0, "name": "ding", "gain": 0.3}, {"line": 2, "frac": 0.3, "name": "buzzer", "gain": 0.28}, {"line": 3, "frac": 0.0, "name": "ding", "gain": 0.3},
     {"line": 4, "frac": 0.3, "name": "buzzer", "gain": 0.28}, {"line": 5, "frac": 0.0, "name": "ding", "gain": 0.3}, {"line": 6, "frac": 0.2, "name": "shimmer", "gain": 0.3}, {"line": 8, "frac": 0.2, "name": "bonk", "gain": 0.3}],
    hot=["SCAM", "REAL", "LINK", "FEE"], pause_before={"8": 0.45})

# RC-16 red flag or green flag panel (SS_6KU9qpr0 20.3M)
FV = lambda line, q, v, **k: s("flagvote", line, 0, GS, q=q, verdict=v, reveal_at=k.pop("reveal_at", 0.8), cast=k.pop("cast", [{"who": "penny", "x": 0.2, "y": 0.98, "h": 650, "mood": "sly"}, {"who": "rocco", "x": 0.8, "y": 1.0, "h": 800, "mood": "sideeye"}]), **k)
out("RC-16", "Red Flag or Green Flag: The Dating App Fox", [
    ["R", "[game show host, big] Red flag or green flag! Tonight's date: a fox from a dating app!"],
    ["S", "[charming, smooth] Hi! I'm a crypto millionaire. I live on a yacht."],
    ["P", "[suspicious] Can we video call?"],
    ["S", "[too fast] My camera is broken."],
    ["R", "[host] Judges?"],
    ["S", "[sweet] I'll fly you to my yacht! I just need a small fee for... customs."],
    ["R", "[host] Judges?"],
    ["S", "[desperate] I love you! Also, please buy these gift cards."],
    ["P", "[flat] Red flag. Red flag. Red flag."],
    ["R", "[warm] No video call. A fee. Gift cards. That's a romance scam. Block."],
    ["S", "[whiny] Not again!"]],
    [s("trio", 0, 0, GS, s="sly", p="happy", r="happy", r_pose="arms_up", rx=0.82, hook="RED FLAG OR GREEN FLAG?"),
     s("slick", 1, 0, YA, s="sly", s_pose="shrug", msg='"CRYPTO MILLIONAIRE"', msg_at=0.3),
     s("cu_p", 2, 0, GS, p="sly", r="sideeye", cam={"z": 1.2, "push": 0.06, "fy": 0.42}),
     s("slick", 3, 0, YA, s="shock", s_pose="arms_up", cam={"z": 1.35, "push": 0.05, "fy": 0.36}),
     FV(4, "\"MY CAMERA IS BROKEN\"", "red"),
     s("slick", 5, 0, YA, s="happy", s_pose="point", msg='"SMALL CUSTOMS FEE"', msg_at=0.5),
     FV(6, "\"SEND A FEE FOR CUSTOMS\"", "red"),
     s("slick", 7, 0, YA, s="panic", s_pose="arms_up", msg="GIFT CARDS?!", msg_at=0.5, cam={"z": 1.2, "push": 0.06, "fy": 0.38}),
     FV(8, "\"BUY ME GIFT CARDS\"", "red", reveal_at=0.3, cast=[{"who": "penny", "x": 0.5, "y": 1.0, "h": 900, "mood": "angry", "pose": "arms_up"}]),
     s("flags", 9, 0, OF, blur=1, r="happy", r_pose="point", n=3, n_prev=0, pop_word="block"),
     s("slick", 10, 0, YA, s="panic", s_pose="shrug", msg="NOT AGAIN!", msg_at=0.2),
     end(10, GS, "NO VIDEO CALL + FEE + GIFT CARDS", "= ROMANCE SCAM", "Send this to someone dating online.")],
    [{"line": 0, "frac": 0.0, "name": "drumroll", "gain": 0.25}, {"line": 4, "frac": 0.3, "name": "buzzer", "gain": 0.3}, {"line": 6, "frac": 0.3, "name": "buzzer", "gain": 0.3},
     {"line": 8, "frac": 0.1, "name": "buzzer", "gain": 0.3}, {"line": 9, "word": "block", "name": "impact", "gain": 0.35}, {"line": 10, "frac": 0.6, "name": "wahwah", "gain": 0.35}],
    hot=["RED", "FLAG", "GREEN", "FEE", "BLOCK"], amb="room")

# RC-17 unsolved whodunit (PibMox6nk4c)
SUS = [["PENNY", "\"BAKING ALL DAY\"", (60, 60, 70)], ["SLICK", "\"AT THE LIBRARY\"", (60, 60, 70)], ["MAILMAN", "\"JUST LETTERS\"", (60, 60, 70)], ["COUSIN KEV", "\"IN HAWAII\"", (60, 60, 70)]]
G = lambda line, n, **k: s("grid", line, 0, IN, title="4 SUSPECTS", cells=SUS[:n], cols=2, cell_h=300, stagger=0.0 if n > 1 else 0.3, **k)
out("RC-17", "Only a Real Detective Can Solve This", [
    ["R", "[mysterious, low] Only a real detective can solve this. Listen till the end."],
    ["R", "[storytelling] Grandma got a call. 'Grandma, it's me! I'm in jail! Send three thousand dollars, fast!'"],
    ["R", "[serious] Four people were near Grandma's phone that day."],
    ["R", "Penny says she was baking all day."],
    ["R", "Slick says he was at the library. Reading."],
    ["R", "The mailman says he only delivers letters."],
    ["R", "Cousin Kevin says he's been in Hawaii all week."],
    ["R", "[whispering] Clue: the caller said 'Grandma'... but never said his own name."],
    ["R", "[sly, to camera] So who's lying? Comment your answer. Real detectives only."]],
    [s("loom_r", 0, 0, IN, r="sly", s="shock", hook="CAN YOU SOLVE IT?"),
     s("phone", 1, 0, IN, p="shock", sender="Unknown", msgs=M('"GRANDMA, IT\'S ME!\nI\'M IN JAIL.\nSEND $3,000 FAST!"', (220, 60, 60))),
     s("cu_r", 2, 0, IN, r="sideeye", r_pose="point", cam={"z": 1.2, "push": 0.08, "fy": 0.47}),
     G(3, 1, cast=[{"who": "penny", "x": 0.25, "y": 1.0, "h": 650, "mood": "happy"}]),
     G(4, 2, cast=[{"who": "slick", "x": 0.75, "y": 1.0, "h": 750, "mood": "sly"}]),
     G(5, 3),
     G(6, 4, cast=[{"who": "rocco", "x": 0.8, "y": 1.0, "h": 700, "mood": "sideeye"}]),
     s("chalk", 7, 0, None, lines=[{"t": "CLUE:", "c": "y", "u": True, "at": 0.2}, {"t": "\"GRANDMA, IT'S ME\"", "c": "w", "at": 0.8, "size": 90}, {"t": "...BUT NO NAME", "c": "r", "at": 2.0, "size": 110}], cast=[{"who": "rocco", "x": 0.82, "y": 1.0, "h": 800, "mood": "sly", "pose": "point"}]),
     s("loom_r", 8, 0, IN, r="sly", s="sly"),
     end(8, IN, "WHO'S LYING?", "COMMENT BELOW", "Real detectives only.")],
    [{"line": 0, "frac": 0.0, "name": "subboom", "gain": 0.35}, {"line": 1, "frac": 0.0, "name": "ding", "gain": 0.3}, {"line": 3, "frac": 0.0, "name": "pop", "gain": 0.3}, {"line": 4, "frac": 0.0, "name": "pop", "gain": 0.3},
     {"line": 5, "frac": 0.0, "name": "pop", "gain": 0.3}, {"line": 6, "frac": 0.0, "name": "pop", "gain": 0.3}, {"line": 7, "frac": 0.6, "name": "riser", "gain": 0.25}],
    hot=["LYING", "CLUE", "JAIL", "DETECTIVE"], amb="lair")

# RC-18 POV phishing click-through (Df331TOAaAO 2.1M)
out("RC-18", "POV: You Just Won a PS6", [
    ["P", "[squealing] POV: I just won a PS6!"],
    ["P", "[excited] Step one: answer three easy questions. Done!"],
    ["P", "[happy] Step two: my name and address. Sure!"],
    ["P", "[slower] Step three: shipping fee, two ninety-nine... card number..."],
    ["R", "[sharp] STOP."],
    ["P", "[whining] But it's FREE!"],
    ["R", "[deadpan] Free prizes don't need your card number. Look who made this page."],
    ["S", "[annoyed, caught] So close! Not again!"]],
    [s("phone", 0, 0, NI, p="happy", p_pose="arms_up", sender="PRIZE CENTER", msgs=M("CONGRATULATIONS!\nYou won a PS6!\nClaim in 10:00", (214, 80, 160)), hook="POV: YOU WON A PS6"),
     s("phone", 1, 0, NI, p="happy", sender="PRIZE CENTER", msgs=M("Step 1 of 3:\nAnswer 3 questions ✓", (52, 120, 246))),
     s("phone", 2, 0, NI, p="happy", p_pose="point", sender="PRIZE CENTER", msgs=M("Step 2 of 3:\nName + address ✓", (52, 120, 246))),
     s("phone", 3, 0, NI, p="sad", sender="PRIZE CENTER", msgs=M("Step 3 of 3:\nShipping $2.99\nCARD NUMBER: ____", (220, 60, 60))),
     s("loom_r", 4, 0, NI, r="angry", s="shock"),
     s("cu_p", 5, 0, NI, p="sad", r="sideeye", p_pose="shrug", cam={"z": 1.25, "push": 0.05, "fy": 0.42}),
     s("cu_r", 6, 0, OF, r="sly", r_pose="point", cam={"z": 1.2, "push": 0.08, "fy": 0.47}),
     s("slick", 7, 0, CC, s="panic", s_pose="arms_up", msg="PAGE OWNER: SLICK", msg_at=0.0),
     end(7, NI, "\"FREE\" PRIZE + CARD NUMBER", "= SCAM", "Send this to someone who clicks every prize.")],
    [{"line": 0, "frac": 0.0, "name": "shimmer", "gain": 0.3}, {"line": 1, "frac": 0.6, "name": "pop", "gain": 0.3}, {"line": 2, "frac": 0.6, "name": "pop", "gain": 0.3},
     {"line": 4, "frac": 0.0, "name": "scratch", "gain": 0.35}, {"line": 4, "frac": 0.0, "name": "impact", "gain": 0.35}, {"line": 7, "frac": 0.6, "name": "wahwah", "gain": 0.35}],
    hot=["PS6", "FREE", "CARD", "STOP"], pause_before={"4": 0.4})

# RC-19 hidden identity status flip (DfSbqCJPpE8 1.1M)
out("RC-19", "Fake IRS Agent Picked the Wrong Grandpa", [
    ["S", "[fake official, bossy] IRS agent! You owe back taxes! Pay now in gift cards or you go to jail!"],
    ["R", "[sleepy, old and slow] Oh dear... gift cards? Which ones, sonny?"],
    ["S", "[greedy] Big ones! Five hundred dollars! Today!"],
    ["R", "[slowly] Let me find my glasses... and my badge."],
    ["S", "[confused] Your... badge?"],
    ["R", "[sharp, normal voice] Detective Rocco. Fraud Unit."],
    ["S", "[panicking] I... I was just leaving!"],
    ["R", "[dry, to camera] The IRS doesn't take gift cards. And it doesn't call to threaten jail."],
    ["S", "[whiny] Not again!"]],
    [s("slick", 0, 0, ST, s="sly", s_pose="point", msg='"IRS AGENT"', msg_at=0.1, hook="FAKE IRS AGENT", cam={"z": 1.1, "push": 0.06, "fy": 0.4}),
     s("cu_r", 1, 0, ST, r="sad", cam={"z": 1.2, "push": 0.05, "fy": 0.47}),
     s("slick", 2, 0, ST, s="happy", s_pose="arms_up", msg="$500 TODAY!", msg_at=0.3),
     s("cu_r", 3, 0, ST, r="sideeye", cam={"z": 1.35, "push": 0.06, "fy": 0.47}),
     s("slick", 4, 0, ST, s="shock", s_pose="shrug", cam={"z": 1.4, "push": 0.05, "fy": 0.36}),
     s("loom_r", 5, 0, ST, r="angry", s="shock"),
     s("slick", 6, 0, ST, s="panic", s_pose="arms_up", cam={"z": 1.25, "push": 0.06, "fy": 0.38}),
     s("store", 7, 0, OF, blur=3, l1="THE IRS NEVER ASKS", l2="FOR GIFT CARDS", r="happy"),
     s("trio", 8, 0, ST, s="panic", p="happy", r="sly", rx=0.82),
     end(8, ST, "\"PAY THE IRS IN GIFT CARDS\"", "= SCAM", "Send this to someone's grandpa.")],
    [{"line": 0, "frac": 0.0, "name": "impact", "gain": 0.3}, {"line": 3, "word": "badge", "name": "subboom", "gain": 0.35}, {"line": 5, "frac": 0.0, "name": "impact", "gain": 0.4},
     {"line": 6, "frac": 0.3, "name": "slide_down", "gain": 0.25}, {"line": 8, "frac": 0.6, "name": "wahwah", "gain": 0.35}],
    hot=["IRS", "GIFT", "BADGE", "DETECTIVE"], pause_before={"5": 0.5}, amb="street")

# RC-20 "did you order this?" two-hander (DflN4MGBPX5)
out("RC-20", "Free Socks and a Very Bad QR Code", [
    ["P", "[curious] Rocco, did you order socks?"],
    ["R", "[flat] No. Why?"],
    ["P", "[puzzled] A package came for me. Socks. And a card with a QR code."],
    ["R", "[knowing] That's a brushing scam."],
    ["R", "[explaining] Sellers mail stuff to real addresses so they can post fake reviews in your name."],
    ["R", "[serious] And that QR code can send you to a site that steals your info. Don't scan it."],
    ["P", "[pause, hopeful] ...So I keep the socks?"],
    ["R", "[dry] Keep the socks. Toss the QR code."]],
    [s("two", 0, 0, PO, p="happy", r="sideeye", hook="A PACKAGE YOU NEVER ORDERED"),
     s("cu_r", 1, 0, PO, r="sideeye", cam={"z": 1.25, "push": 0.06, "fy": 0.47}),
     s("box", 2, 0, PO, open_at=0.4, r="sideeye"),
     s("loom_r", 3, 0, PO, r="sly", s="sly"),
     s("chalk", 4, 0, None, lines=[{"t": "BRUSHING SCAM:", "c": "y", "u": True, "at": 0.1}, {"t": "1. mail you stuff", "c": "w", "at": 0.8, "size": 80}, {"t": "2. post fake reviews", "c": "w", "at": 2.2, "size": 80}], cast=[{"who": "rocco", "x": 0.82, "y": 1.0, "h": 800, "mood": "sideeye", "pose": "point"}]),
     s("stamp", 5, 0, None, set="pink", kicker="THE QR CARD:", claim="\"SCAN FOR YOUR GIFT\"", verdict="DON'T", at=1.0, cast=[{"who": "rocco", "x": 0.82, "y": 1.0, "h": 760, "mood": "angry"}]),
     s("cu_p", 6, 0, PO, p="sly", r="sideeye", cam={"z": 1.3, "push": 0.05, "fy": 0.42}),
     s("two", 7, 0, PO, p="happy", r="sly"),
     end(7, PO, "UNORDERED PACKAGE + QR CODE", "DON'T SCAN", "Send this to someone who loves free stuff.")],
    [{"line": 2, "frac": 0.2, "name": "pop", "gain": 0.3}, {"line": 3, "frac": 0.0, "name": "subboom", "gain": 0.3}, {"line": 5, "frac": 0.5, "name": "impact", "gain": 0.35}, {"line": 7, "frac": 0.3, "name": "ding", "gain": 0.3}],
    hot=["SCAM", "QR", "SOCKS", "FAKE"], pause_before={"6": 0.45}, amb="street")

# RC-21 "this just happened to Penny" (4ILxskhpnpo 602K, 481x)
out("RC-21", "This Just Happened to Penny", [
    ["R", "[urgent, to camera] This just happened to Penny. Watch closely."],
    ["R", "[serious] A text from 'her bank'. Suspicious charge. Call this number."],
    ["R", "She called. The 'bank' knew her name and the last four digits of her card."],
    ["R", "[slow] Then they told her to move her money to a 'safe account'."],
    ["P", "[shaken] It sounded SO real!"],
    ["R", "[firm] Real banks never ask you to move money to keep it safe."],
    ["R", "[counting] Three rules. Hang up. Call the number on your card. Never move money for anyone."]],
    [s("loom_r", 0, 0, OF, r="angry", s="shock", hook="THIS JUST HAPPENED"),
     s("phone", 1, 0, PR, p="shock", sender="BANK ALERT?", msgs=M("Suspicious charge $849.00\nCall us now: (888) 555-0142", (220, 60, 60))),
     s("cu_r", 2, 0, OF, r="sideeye", r_pose="point", cam={"z": 1.2, "push": 0.08, "fy": 0.47}),
     s("kinetic", 3, 0, None, bgcol=[[90, 10, 10], [20, 0, 0]], words=[{"t": "\"SAFE", "size": 220, "c": [255, 205, 60]}, {"t": "ACCOUNT\"", "size": 220, "c": [255, 205, 60]}, {"t": "= THEIR ACCOUNT", "size": 110}], cast=[{"who": "slick", "x": 0.8, "y": 1.0, "h": 800, "mood": "sly"}]),
     s("cu_p", 4, 0, PR, p="sad", r="sideeye", p_pose="arms_up", cam={"z": 1.25, "push": 0.05, "fy": 0.42}),
     s("store", 5, 0, OF, blur=3, l1="BANKS NEVER ASK YOU", l2="TO MOVE YOUR MONEY", r="happy"),
     s("chalk", 6, 0, None, lines=[{"t": "3 RULES", "c": "y", "u": True, "at": 0.1}, {"t": "1. Hang up", "c": "w", "at": 0.9}, {"t": "2. Call the # on your card", "c": "w", "at": 1.7, "size": 76}, {"t": "3. Never move money", "c": "r", "at": 3.0}], cast=[{"who": "rocco", "x": 0.82, "y": 1.0, "h": 760, "mood": "happy", "pose": "point"}]),
     end(6, OF, "\"MOVE IT TO A SAFE ACCOUNT\"", "= SCAM", "Send this to someone you'd hate to see lose their savings.")],
    [{"line": 0, "frac": 0.0, "name": "impact", "gain": 0.3}, {"line": 1, "frac": 0.0, "name": "ding", "gain": 0.3}, {"line": 3, "frac": 0.3, "name": "subboom", "gain": 0.35}, {"line": 6, "frac": 0.2, "name": "tick", "gain": 0.2, "dur": 1.0}],
    hot=["SAFE", "ACCOUNT", "NEVER", "HANG"], amb="room")

# RC-22 retro pixel game: beat the scam boss (own format)
PX = lambda line, msg, hud_r, cast_, **k: s("pixel", line, 0, None, hud_l="PENNY HP ♥♥♥", hud_r=hud_r, start=0, to=0, prefix="", msg=msg, size=60, cast=cast_, **k)
SL = lambda mood, pose=None: {"who": "slick", "x": 0.72, "y": 0.82, "h": 900, "mood": mood, "pose": pose}
PN = lambda mood, pose=None: {"who": "penny", "x": 0.25, "y": 0.83, "h": 620, "mood": mood, "pose": pose}
out("RC-22", "Level 1: Beat the Scam Boss", [
    ["R", "[retro game announcer] Level one! Boss fight: Slick!"],
    ["S", "[villain] Attack one! A FREE gift card! Just click the link!"],
    ["R", "[announcer] Penny blocks! No link clicked!"],
    ["S", "[villain] Attack two! URGENT! Your account is locked!"],
    ["R", "[announcer] Penny blocks! She calls her bank herself!"],
    ["S", "[desperate] Final attack! Grandma, it's me, your grandson!"],
    ["P", "[sly] Oh really? What's your name, grandson?"],
    ["S", "[long pause] ...Grandson."],
    ["R", "[triumphant] Boss defeated! Level complete!"],
    ["S", "[whiny] Not again!"]],
    [PX(0, "BOSS FIGHT: SLICK", "LV 1", [PN("happy"), SL("sly", "arms_up")], hook="LEVEL 1: SCAM BOSS"),
     PX(1, "ATTACK: FREE GIFT CARD", "LV 1", [PN("shock"), SL("happy", "point")]),
     s("cu_p", 2, 0, PR, p="happy", r="sly", p_pose="arms_up", cam={"z": 1.2, "push": 0.06, "fy": 0.42}),
     PX(3, "ATTACK: ACCOUNT LOCKED!", "LV 1", [PN("shock"), SL("sly", "point")]),
     s("two", 4, 0, PR, p="happy", r="happy", p_pose="arms_up"),
     PX(5, "FINAL ATTACK: GRANDSON", "LV 1", [PN("sly"), SL("happy", "arms_up")]),
     s("cu_p", 6, 0, PR, p="sly", r="sly", p_pose="point", cam={"z": 1.2, "push": 0.05, "fy": 0.42}),
     s("slick", 7, 0, CC, s="shock", s_pose="shrug", cam={"z": 1.45, "push": 0.05, "fy": 0.36}),
     s("kinetic", 8, 0, None, bgcol=[[18, 16, 48], [60, 16, 60]], words=[{"t": "BOSS", "size": 150, "font": "Pixel", "c": [255, 205, 60]}, {"t": "DEFEATED", "size": 110, "font": "Pixel", "c": [255, 205, 60]}], cast=[{"who": "penny", "x": 0.5, "y": 1.0, "h": 800, "mood": "happy", "pose": "arms_up"}]),
     PX(9, "GAME OVER (FOR SLICK)", "WIN", [PN("happy"), SL("shock", "shrug")]),
     end(9, PR, "CLICK LINKS? NO. CALL BACK? YES.", "LEVEL COMPLETE", "Send this to your player 2.")],
    [{"line": 0, "frac": 0.0, "name": "coin", "gain": 0.3}, {"line": 2, "frac": 0.0, "name": "bonk", "gain": 0.3}, {"line": 4, "frac": 0.0, "name": "bonk", "gain": 0.3},
     {"line": 7, "frac": 0.0, "name": "crickets", "gain": 0.25}, {"line": 8, "frac": 0.0, "name": "ding", "gain": 0.35}, {"line": 9, "frac": 0.6, "name": "wahwah", "gain": 0.35}],
    hot=["ATTACK", "BLOCKS", "BOSS", "DEFEATED"], pause_before={"7": 0.6}, amb="room")
print("ok")

# ---- post-process: every graphic shot sits on a real 3D-film set (empty_check / look), no flat gradients ----
for f in sorted(os.listdir(D)):
    if not (f.startswith("rc") and f.endswith(".json") and "_" not in f): continue
    d = json.load(open(os.path.join(D, f))); home = next((x["bg"] for x in d["shots"] if x.get("bg")), PR)
    for x in d["shots"]:
        if x["kind"] in ("kinetic", "stamp") and not x.get("bg"):
            x["bg"] = home; x.pop("bgcol", None); x.pop("set", None); x["dim"] = 150 if x["kind"] == "kinetic" else 90
    json.dump(d, open(os.path.join(D, f), "w"), indent=1)
print("post-process ok")
