---
name: rocco-3d-cast
description: Use for anything with the 3D Red Flag Rocco cast (Rocco the raccoon detective, Penny the piggy bank, Slick the scammer fox) - checking whether the rigged characters look right, fixing their faces (mouth/lip-sync, blink, expression strength), building the 3D sprite library, and putting the 3D characters into a Rocco episode (rc_render style rocco3d). Use before rendering any Rocco cartoon episode and whenever Shohjahon says the characters are not ideal.
---

# Rocco 3D cast — quality, fixes, sprite library

Models live ONLY in the private repo `financier-videos/buck-private` → `rocco_cast_v1/` (`rocco_rigged.glb`, `penny_rigged.glb`,
`slick_rigged.glb`, ~100k verts, 4K textures, armature + 29 procedural shape keys). Never copy them into the public repo.
Clone: `git clone --depth 1 --filter=blob:none --sparse https://github.com/financier-videos/buck-private /home/user/buck-private && git -C /home/user/buck-private sparse-checkout set rocco_cast_v1`.

Blender: `python3 -m venv /tmp/bpyenv && /tmp/bpyenv/bin/pip install bpy==5.3.0 pillow numpy` (wheel ~430 MB).
EEVEE/Workbench need a GPU (EGL) → in the cloud container use **Cycles CPU** (600x800, 24 samples + denoise ≈ 8–16 s/frame).
Follow `blender-core` rules (data API, no context-dependent operators except glTF import).

## What "ideal" means (Shohjahon, 2026-11-22: "personajlar ideal bo'lmasa, o'zgartir, men xohlaganimdek")
1. Faces read at phone size: mouth clearly opens when talking, closes when silent; blink is clean; emotions (happy, angry, sad, shock, sly) are obvious without captions.
2. No skin tearing, no shards, no snout/face dragging in any library frame.
3. Bright studio light (luma ≥ 0.5), soft contact shadow, consistent camera (ortho, 12° turn) across all sprites so cuts don't jump.
4. Body acting: at least idle, point, arms_up (surprise), shrug. Poses limited to ≤ 60–75° (armpit/coat-hem shards beyond).
5. Same design as the 2D Rocco v2 style bible (docs/rocco_style_v2.md, docs/rocco_series_bible.md): Rocco calm deadpan, Penny bright and naive, Slick sly → panicking.

## QA first (always, before using or after changing a rig)
`/tmp/bpyenv/bin/python .claude/skills/rocco-3d-cast/scripts/face_check.py <char> /tmp/fc_<char>.png --fixed`
→ 8 close-ups: rest, talk_half, talk_open, happy, angry, sad, shock, blink. Look at the sheet. Write the verdict in docs/changes.md.

## Known defects (QA 2026-11-22) and fixes
| Defect | Fix |
|---|---|
| Expressions too subtle at 1.0 (keys are procedural offsets, not sculpts) | `face_fix.fix()` sets slider_max 2.0; library pushes Rocco/Slick to 1.2–1.6 |
| Penny: jaw_open drags the snout down; frown opens a dark hole (mouth sits right under the snout) | `face_fix.fix()` fades jaw offsets above the lip line; library opens Penny's jaw at 0.4× and frowns at 0.55×. **Real fix needs a re-sculpted mouth (rig chat):** lower the mouth line ~1.5 cm, add separate upper/lower lip keys and mouth corners |
| Penny: blink > 0.6 tears the lid skin | cap 0.55 (`face_fix.BLINK_CAP`) — reads as a soft blink |
| Rocco: blink makes a dark smear over the mask | acceptable (mask is dark); keep 2-frame blinks |
| phone/think poses push the hand into the coat | removed from the library |
| No fingers, no teeth/tongue sculpt | live with it at phone size; point with the whole arm |

## Sprite library (for rc_render `style: rocco3d`)
`work/rocco/rocco3d/run_lib.sh` (resumable; finished frames are skipped) → `/tmp/rocco3d_lib/<char>/`:
- idle: `<mood>_<mouth>_<eyes>.png` — 7 moods (neutral, happy, shock, sad, angry, sly, relieved) × 5 mouths (closed, half, open, o, e) × eyes (open, closed)
- poses: `<pose>_<mood>_<mouth>_open.png` for point, arms_up, shrug × 5 moods × 5 mouths
Sprite feet sit at 91.6 % of the sprite height. rc_render: `FIN_ROCCO3D=/tmp/rocco3d_lib python3 work/rocco/rocco2/rc_render.py spec.json out.mp4`
(`char3d()` picks mood/mouth from the talk envelope and blinks every ~3.3 s).

## Rules for episodes with the 3D cast
- Backgrounds must match the 3D look: soft 3D-render style sets (vidiq_image_generate "3D animated film style", same light direction), never flat 2D cartoons next to 3D characters.
- Story first (docs/rocco_series_bible.md, cartoon-3d-short beat formula), then storyboard with a pose per line (point on the reveal, arms_up on the shock, shrug on the excuse).
- Before posting: qc_gate 0–15 + 10-frame sheet in docs/looks_samples/.
