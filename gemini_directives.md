# Financier Money Facts — production directives (TOP-10 / Cinema standard)
Updated 2026-11-20 (Tashkent). Owner: Shohjahon. Channel: **Financier Money Facts** (@FINANCIER4241), English money facts for a US audience.
Canonical working playbook (Uzbek, updated by the production agents several times a day): Claude project "Trade" → `claude/youtube_playbook.md`. If anything here conflicts with it, the playbook wins.

## 1. Goal
- 2 Shorts per day + 1 long video every 3 days, published without waiting for approval.
- 1 billion total views in 6 months; TOP-10 of the "money facts / how money works" niche within 12 months.
- Every video must look and sound like a big-budget animated film, not a template.

## 2. Buck — the channel's character (new look from 2026-11-20)
- A 24k gold coin with an engraved scroll border and an embossed "$" under the face; a slightly tilted black velvet top hat with a gold band and a small dollar bill tucked in it; a gold monocle on a chain over the right eye; big glossy amber eyes, thick dark-brown brows, a living mouth; thin gold arms and legs; four-finger white cartoon gloves; red-and-gold sneakers. No bow tie, no green sneakers (old look).
- Built as a **hybrid**: Shohjahon's Tripo sculpt (paid plan, commercial rights) supplies the body; the face (eyes, lids, brows, shape-key mouth, monocle + chain, "$") and the limbs are procedural so Buck can act. Code: `engine/buck3d.py` (`--cinema`, default `--style tripo`).
- The Tripo model file is **private** — never commit it to this public repository or share it. The sprite library is rendered only in Shohjahon's Claude chat and published as `assets/buck3d_v2.tar` (226 frames, 1080 px, 15 fps: 12 moods + flip/bonk/dodge).
- Render standard: Blender Cycles, 1080x1080, 64 samples + OIDN, warm key / cool fill / double rim / softbox / top light, reflection cards, soft deep contact shadow.
- Never add a cane, spats or any other recognizable mascot's signature items; never use real people's faces, names or voices.

## 3. Voice — Buck is the ONLY narrator
- No separate narrator. Buck speaks 100% of every Short and long video, in first person: asks, reacts, answers.
- ElevenLabs voice made with Voice Design from archetype prompts only (no cloning, no voice library, no real names). Variants: A "Trickster", B "Adventurer", C "Con-Artist"; A until Shohjahon picks.
- TTS: `eleven_multilingual_v2`, stability 0.28, similarity_boost 0.75, style 0.85, use_speaker_boost true.
- Script performance marks: natural pauses "...", interjections "Whoa!", "Wait a second...", "Heh.", "Okay, okay..." (2–4 per Short).
- A video whose voice falls back to the emergency TTS (`"buck_voice": "kokoro..."`) is **not published**.

## 4. Picture and sound (engine `engine/make_video.py`, v6 CINEMA)
- Camera push/pull/drift every 1.5–2 s, 3D parallax layers, motion blur on cuts and moves, cinematic grade (teal-orange, bloom, grain), timed karaoke captions from Buck's real word timings.
- No music. Synthesized stereo SFX (riser + sub-boom under stats, shimmer on flashes, room tone, reverb, ducking); birds where it fits.
- Hook in the first 2 s (number or paradox on screen), one question per Short, 25–35 s, loop the last line into the first, a visual change every 1.5–3 s.

## 5. Content rules (non-negotiable)
- No nudity, sexual, indecent or illegal content in any frame, text or topic; no gambling promotion, scams, tax evasion, drugs, piracy; no swearing; family-friendly humor only.
- Every fact has a named, dated source; forecasts are called forecasts; myths are labeled. No financial advice ("Not financial advice. For education and entertainment." in every description).
- No copying competitors' scripts; only our own character, synthesized effects, OFL fonts and credited Pexels b-roll.
- Purchases, plan changes and new accounts only after Shohjahon says yes (with price and reason). Never enter payment data, passwords or API keys; keys live in environment settings, never in chat or files.

## 6. Open blockers (2026-11-20)
- ElevenLabs is unreachable from the scheduled-task environment (key missing, `api.elevenlabs.io` blocked) → Buck's voice cannot be rendered there yet; videos wait instead of shipping with a robotic voice.
- GPU rendering (Runpod) is blocked the same way (`api.runpod.io` 403); the 3D library renders on CPU in the chat (~75–80 s/frame).
