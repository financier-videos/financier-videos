"""BUYURTMA 8: convert queued Financier specs to the full-screen layout with footage-bank clips only."""
import json, sys
B = "/tmp/fin/bg/bank/"
MAP = {
 "r06_cart": {"milk": "cart_pov", "cart": "cart_pov", "mall": "cart_empty", "crowd": "cart_empty"},
 "r04_airport": {"terminal": "airport_hall", "store": "airport_hall", "luggage": "airport_walk"},
 "r05_bfcm": {"mall": "pay_terminal", "laptop": "online_card", "crowd": "cash_desk", "online": "laptop_phone"},
 "r07_pink": {"mall": "cart_pov", "crowd": "cart_empty", "shave": "coins_hand"},
 "r08_fees": {"crowd": "wallet_empty", "laptop": "online_card", "luggage": "airport_walk", "terminal": "cabin_yellow",
              "atm": "atm_use", "online": "phone_scroll", "lobby": "pay_terminal", "elevator": "wallet_empty"},
 "r02_noseat": {"gate": "cabin_empty", "luggage": "airport_walk", "terminal": "airport_hall", "window": "plane_wing", "plane": "cabin_yellow"},
}
MOODS = ["smug", "sideeye", "happy", "point", "shocked", "thumbsup"]
for name, mp in MAP.items():
    d = json.load(open(f"work/2026-11-22r/{name}.json")); d["look"] = "fullbleed"; d.pop("split_colors", None)
    for i, sc in enumerate(d["scenes"]):
        if sc.get("bg"):
            k = sc.pop("bg").rsplit("/", 1)[-1][:-4]; sc["shots"] = [{"broll": B + mp.get(k, k) + ".mp4", "at": 0}]
        for s_ in sc.get("shots", []):
            k = s_["broll"].rsplit("/", 1)[-1][:-4]; s_["broll"] = B + mp.get(k, k) + ".mp4"
        if not sc.get("mascot") and not sc.get("vs"): sc["mascot"] = {"mood": MOODS[i % len(MOODS)], "pos": "corner"}
        for s_ in sc.get("shots", []):
            if not s_["broll"].startswith(B): print("NOT IN BANK", name, s_["broll"])
    json.dump(d, open(f"work/2026-11-22r/{name}_b8.json", "w"), indent=1)
    print(name, [[s["broll"].rsplit("/", 1)[-1] for s in sc.get("shots", [])] for sc in d["scenes"]])
