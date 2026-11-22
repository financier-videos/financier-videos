# ROCCO — HAQIQIY MULTFILM YO'NALISHI (3D model tayyor bo'lganda)

Shohjahon (2026-11-22): "Rocco uchun 3D model boshqa chatda yasalyapti; tayyor bo'lgach faqat animatsiyaga o'tamiz — syujetli, ssenariyli, haqiqiy multfilm kabi videolar. Kerakli skillarni GitHub'dan topib o'rnat va hammasidan foydalan."

## O'rnatilgan skillar (repo: `.claude/skills/`, har sessiyada avtomatik yuklanadi)
| Skill | Manba (litsenziya) | Nimaga |
|---|---|---|
| `cartoon-3d-short` | mromidev/claude-animated-shorts (MIT) | 55–70 s syujetli multfilm short: beat formulasi (hook → setting → 3–4 kuchayish → snap → deadpan juft gap → tushuntirish → oqibat → callback twist), kamera (glide 18–40 f, flip-kick), ink/DOF/grade qiymatlari, ovoz-SFX taymingi, QA |
| `blender-core` | EL4CTEO/blender-skills (MIT) | Blender 5.x API qoidalari, headless kod ishga tushirish |
| `blender-character-rigging` | 〃 | 3D Rocco'ni rig qilish (Rigify, skinning) |
| `blender-facial-shapekeys` | 〃 | og'iz shakllari (lip-sync), ko'z qisish, qosh |
| `blender-animation` | 〃 | yurish, imo-ishora, NLA, action'lar |
| `blender-stylized-npr` | 〃 | multfilm (toon/ink outline) ko'rinish |
| `blender-lighting-lookdev`, `blender-scene-setup`, `blender-rendering`, `blender-video-editing`, `blender-export-pipelines`, `blender-workflow-recipes` | 〃 | yorug'lik, sahna, render, montaj, eksport |
spark-video (litsenziyasiz) — faqat g'oya olindi: dunyo bibliyasi + personaj kartochkalari + sahnama-sahna ssenariy → storyboard.

## Muhit (tekshirildi 2026-11-22)
- Blender 5.3 `bpy` (pip wheel 427 MB) → `python3 -m venv /tmp/bpyenv && /tmp/bpyenv/bin/pip install bpy==5.3.0`.
- EEVEE konteynerda ishlamaydi (GPU/EGL yo'q). **Cycles CPU ishlaydi**: oddiy kadr 540×960, 16 sample ≈ 3 s.
- 60 s × 30 fps = 1 800 kadr → CPU'da 1.5–4 soat/video. Tezlashtirish: RunPod GPU (muhitda kalit ulangan, api.runpod.io) yoki 24 fps + 1080×1920 da 8–16 sample + denoise.

## 3D modeldan nima kerak (boshqa chatga yuborish uchun ro'yxat)
1. Format: `.blend` (afzal) yoki `.glb/.fbx`; to'qimalar ichiga joylangan (packed).
2. Armature (skelet): umurtqa, bosh, qo'llar (yelka-tirsak-bilak-barmoq 3 ta), oyoqlar, dum; T- yoki A-poza.
3. Yuz shape key'lari (lip-sync uchun ≥8): rest, A, E, O, U, M/B/P, F/V, L; + blink_L/R, brow_up, brow_angry, smile, frown.
4. Shlyapa va plash alohida obyekt (olib qo'yish/animatsiya uchun).
5. 15–40k uchburchak; masshtab 1 birlik = 1 m; oldi −Y tomonga qaragan.
6. Penny va Slick ham shu uslubda (keyinroq) — uchala personaj bitta olamda.

## Ishlab chiqarish tartibi (har epizod)
1. **Bibliya** — `docs/rocco_series_bible.md` (dunyo, personajlar, qoidalar). Har epizod undan boshlanadi.
2. **G'oya + fakt** — `docs/competitor_watch.md` (≤7 kunlik) + rasmiy manba (FTC/bank).
3. **Ssenariy** — cartoon-3d-short beat formulasi; 55–70 s; har 6–8 s da kulgi; ziddiyat Rocco ↔ Slick; Penny — tomoshabin o'rni.
4. **Ovoz** — ElevenLabs Text-to-Dialogue (eleven_v3, his teglari) → so'z vaqtlari (alignment).
5. **Storyboard** — har gapga kadr: plan (wide/MS/CU), kamera harakati, personaj harakati, yuz ifodasi, SFX.
6. **Lip-sync** — alignment → fonemalar → shape key kalit kadrlar (blender-facial-shapekeys).
7. **Sahna** — 3D to'plamlar (Kenney CC0) yoki chizilgan fon + 3D personaj; NPR/ink (blender-stylized-npr).
8. **Render** — Cycles CPU yoki RunPod GPU → kadrlar → ffmpeg + mix.
9. **QC** — qc_gate (0–15) + cartoon-3d-short QA (qora/oq/qotgan kadr) + 10 kadrlik varaq.
