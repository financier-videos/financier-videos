---
name: viral-cartoon-playbook
description: Rules and a measuring tool for making story cartoon shorts (Red Flag Rocco 3D, any animated skit) as strong as the current viral 3D cartoons - script (double twist + tag, status inversion, fable), voice and intonation (opposite registers, pause before the shock line, fast punchline), camera (shot sizes, ECU micro-zoom), colour/light, ambience and SFX, captions, loop. Use when writing or storyboarding a cartoon episode, before rendering it, and to measure a finished render (cartoon_metrics.py). Use together with rocco-3d-cast and viral-video-decomposer.
---

# Viral cartoon playbook
Evidence: `docs/viral_cartoon_study.md` (4 viral 3D shorts, 0.5M–50M views, watched 2026-11-22). Refresh it monthly:
vidiq_outliers (contentType short, "3D animated cartoon story") + vidiq_instagram_tiktok_outlier_search → vidiq_watch_shortform_content
with the director prompt in the study doc → add rows. Log benchmarks in docs/competitor_watch.md (qc_gate step 15).
YouTube/TikTok downloads are blocked in the cloud container; use vidIQ watch for analysis, `analyzing-video` skill for our own files.

## Script checklist (write it before any render)
1. Frame 1 = conflict in progress, first word ≤ 0.8 s. No title card.
2. Status inversion or scale contrast visible in frame 1 (small vs big, naive vs menace).
3. Double twist + tag: setup → twist 1 → twist 2 → button line after the moral.
4. Scam topic = fable: show the mechanism as a repeating cycle, end with a 4th-wall line tying it to real life.
5. Every character changes register at least twice (smug → panicked, offended → realising).
6. Numbers get a micro-pause before them.

## Voice (ElevenLabs eleven_v3 text-to-dialogue)
- Opposite registers: Penny high/fast, Rocco low/slow deadpan, Slick smooth → whiny. Use audio tags for each shift.
- rc_render `"pause_before": {"<line>": 0.35-0.55}` before the shock/punch line; leave every other gap natural (≤ 0.15 s).

## Picture
- Per shot `"cam": {"z": 1.0-1.5, "push": 0.05-0.25, "fx": 0.5, "fy": 0.4}`: ≥ 4 different framings per episode, ECU (z ≥ 1.3) on the shock line, wide on the ending.
- Extreme expression on the key frame (rocco-3d-cast library moods: shock / angry / sly), arms_up pose on surprise.
- Background: 3D-film sets, warm key light, blurred (`blur` 1–3) so characters read.

## Sound
- `"amb": "room" | "street" | "lair"` (global or per shot) — never digital silence.
- `subboom` under the menace line, `riser` before the punch, foley on every action (cash, ding, bonk, impact).

## Measure (required before posting)
`python3 .claude/skills/viral-cartoon-playbook/scripts/cartoon_metrics.py video.mp4`
HARD: first_speech ≤ 0.8 s, ASL ≤ 2.6 s, dead air ≤ 1.2 s. Soft: max shot ≤ 6 s, saturation ≥ 0.30, luma ≥ 0.40, ≥ −16 LUFS.
Write the result next to the qc_gate result in docs/changes.md.
