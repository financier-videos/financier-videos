# Loop choki va 9:16 xavfsiz zona (2026-11-28 B)
Manba: iart-ai/tiktok-video-skills, skills/short-form-video/SKILL.md (MIT, (c) 2026 iart.ai; raw.githubusercontent.com, main). Matn ko'chirilmadi — o'z so'zimiz bilan; Remotion kodi bizga kerak emas (dvigatel Python).

## 1. Loop choki (seam) — `engine/loop_seam_check.py`, qc_gate `17_loop_seam` (faqat WARN, FAIL emas)
- Nima: oxirgi kadr birinchi kadrga ko'rinishi (kompozitsiya, rang, yorug'lik) bo'yicha ulanadimi. Gap-loop (oxirgi jumla → 1-jumla) bizda bor; KADR-loop yo'q edi.
- O'lchov: seam_diff (kulrang farq), hist_dist (rang gistogrammasi), luma_jump. SMOOTH / MIXED / JUMP.
- Bizning videolar (28-noy): BK-13 SMOOTH 0.03, BK-15 MIXED, BK-16 JUMP (hist 0.62), BK-14 JUMP (0.35/0.92, oxiri qorong'i); g'olib "$1 Trillion in 61 Days" SMOOTH 0.07, gift card SMOOTH 0.04.
- Qo'llash: JUMP bo'lsa oxirgi 0.5–1 s ga 1-sahnaning klipi/rangini qo'y (spec oxirgi sahna "shots" = 1-sahna klipi) yoki oxirgi kadr grade'ini 1-kadrga yaqinlashtir.
- Cheklov: 2 kadr bilan o'lchanadi; ko'rish/retention bilan bog'liqligi hali isbotlanmagan (gipoteza). 3 SMOOTH vs 3 JUMP videoni results.md da 72 soatda solishtir.

## 2. 9:16 xavfsiz zona (1080x1920)
- Muhim narsa markaziy ~900x1400 qutida; tepa ~120 px, pastki ~320 px (sarlavha/tugmalar/audio), o'ng ~120 px (like/izoh/share) BO'SH.
- Bizda tekshirish: kontakt-varaqda subtitr va raqam pastki 320 px ga tushmasin, o'ng chetga yopishmasin. Avtomatik tekshiruv yo'q (matn joyini kadrdan aniqlash qiyin) — keyingi qadam: dvigatel rendered.json'ga matn bloklari koordinatasini yozsa, qc da tekshirish (backlog).
