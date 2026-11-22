# Viral 3D cartoon study (2026-11-22, vidIQ watch — Shohjahon: "grafikadan ovozgacha, intonatsiya, ranglar, ssenariy — hammasini o'rgan")

| Video | Views | Breakout | Format |
|---|---|---|---|
| Pip & Rue "Meet the Dad" (TikTok @pipandrue) | 6.7M | 14x | 15 s, 3 characters, dialogue skit, double twist |
| Zovi "Bottle Buying Scheme" (YT 2IFK69bB4CE) | 491K | 239x | 78 s, scam as fable, montage, 4th-wall moral |
| Fruit story "Made fun of wife's looks" (TikTok @animators56) | 2.3M | 54x | 115 s, 3-act drama, role reversal |
| Little Mole garden (IG @apextoon_usa14) | 50.2M | 178x | 46 s, no words, cute vs huge, slapstick |

## What they all do (and RC-01..RC-07 did not)
**Script**
- First frame = conflict already happening; first word ≤ 0.65 s ("Hey! Don't you dare touch my wife!"). No title card, no logo.
- **Double twist + tag**: twist 1 (it's her dad) → twist 2 (the scary one likes the audacity) → button line that flips it again ("She's not dead."). Our RC = single reveal; add a tag after the moral.
- **Status inversion**: tiny overconfident character vs a 3x bigger one. Scale contrast in the very first frame.
- Scam stories work as **fables**: show the mechanism through a repeating cycle (buy $20 → $50 → promise $300) and break the 4th wall at the end ("Remember the stock market? Same story.").
- Role reversal / karma ("You cook it today") — the person who mocked gets the same treatment.

**Voice & intonation**
- Each character has an opposite register: high fast raspy fool / low slow deadpan straight-man / sub-bass slow menace.
- Punchline lands **100–150 ms** after the setup line (no dead air) — but the shock line gets a **~400 ms pause before it**.
- Every character changes register inside the video: screech → nervous stammer → smug → chipper. One flat tone = death.
- Scammer: micro-pause before every number ("…twenty dollars", "…fifty dollars").
- A big laugh / gasp / crowd reaction is a sound event of its own.

**Picture**
- 4–5 shot sizes per minute: wide tracking → low-angle/OTS looking up at the big one → MCU reaction → **ECU micro-zoom** on the shock line → wide trio ending. ASL 1.2–2.5 s (montage 0.8 s).
- Expressions are extreme at the key frame: pupils shrink + small "O" mouth for mortification; smug half-lid + one brow; deep brow creases for menace.
- Big glossy eyes with specular highlight; soft fuzzy/iridescent materials; heavy rough texture on the antagonist.
- Light: warm golden-hour key from top-right, crisp rim light, **shallow depth of field** (background blurred). Colour follows mood: warm boom → dim trap → amber/empty aftermath → bright resolution.

**Sound**
- Constant ambience bed (street, room, wind) — never digital silence.
- Low drone/sting under the menace line; tactile foley on every action (glass clink, paper money, thud).
- Silence only as an effect (the "he never came back" beat: music drops, only wind).

**Captions**: white bold sans, black stroke, 2–4 words, lower third, synced word by word.
**Ending**: last frame flows back into the first (loop), or a tag line after the moral.

## Applied (engine)
- rc_render: `pause_before` {line: s}, per-shot `cam` {z, push, fx, fy} (ECU micro-zoom), `amb` bed (room/street/lair) — 2026-11-22.
- Skill `.claude/skills/viral-cartoon-playbook/` + `scripts/cartoon_metrics.py` (first speech, ASL, dead air, colour, loudness).
- RC-08: pauses before lines 2/8/13/16, ECU on "EXCUSE me?!", ominous subboom under "piggy banks", ambience per set.
