# "Elite video production & visual quality director" (Shohjahon yuborgan matn, 2026-11-21 01:49) — bizga qo'llanishi
Asl matn: `2026-11-21_visual_quality_director_ORIGINAL.md`. U jonli suratga olish studiyasi uchun yozilgan (kamera, dron, DaVinci, After Effects). Bizda video KOD bilan chiziladi, shuning uchun har band uch toifaga ajratildi. Matndagi eng muhim qoida bizga to'liq tegishli: "vosita 4K/8K/HDR bermasa — bergan deb aytma".

| Band | Bizda | Holat |
|---|---|---|
| 10. Sifat nazorati (12 nuqta) | har video: o'lcham/keskinlik, kadrlar izchilligi, rang, harakat silliqligi, o'tishlar, grafika, animatsiya, ovoz, siqish artefaktlari, eksport sozlamalari | QO'LLANADI — producer_task QC ro'yxatiga qo'shildi |
| 8. Texnik standart: kodek, bitreyt, rang belgisi, artefaktsiz | dvigatel v6.5: x264 `medium`, CRF 16 (oldin `veryfast`, CRF 20), rang bt709 deb belgilanadi (oldin belgisiz), audio 192k | QO'LLANDI 2026-11-21 (sinov: bitreyt ~2.2x, rang o'zgarmadi, check.py "colour bt709" PASS) |
| 6. Ovoz: toza, kesilmagan, balanslangan | −14 LUFS, true peak ≤ −1 dBTP, voice_check | bor |
| 5. Rang: izchil greyd, qora "ezilmagan", yorug' "kuymagan" | CineGrade (S-egri, teal/iliq, bloom, dona) + 6 theme | bor; QC ga "qora ezilmaganmi / raqam kuymaganmi" qo'shildi |
| 3. Motion grafika: silliq egri, aniq tekislash, yagona til | stat/vs/chart/sticker; emil-skills bo'yicha animatsiya ko'rigi navbatda | qisman |
| 2. Montaj: ritm, match cut, speed ramp, ortiqcha o'tish yo'q | kamera kalitlari 1.2–1.5 s, punch/flash/slide | qisman; "ortiqcha o'tish yo'q" — qoida |
| 7. Kadr xilma-xilligi: umumiy/o'rta/yirik/makro plan | Buck corner (kichik) / center (o'rta) / zoom (yirik); makro va 3D muhit YO'Q | KAMCHILIK — 3D sahnalar bosqichi |
| 1. Kinematografiya: real footage, 4K–8K, linza, dron | bizda footage deyarli yo'q (Pexels b-roll ≤1 sahna) | QO'LLANMAYDI (jonli suratga olish yo'q) |
| 4. VFX: tracking, rotoscoping, green screen | yo'q | QO'LLANMAYDI |
| 8. 4K (3840×2160), 10-bit, HDR | render 1080×1920 / 1920×1080, 8-bit SDR | YO'Q. 1080p ni 4K ga cho'zish — soxta 4K, qilinmaydi. Haqiqiy 4K: dvigatel S=2160 (render ~4x sekin, Buck kutubxonasi 2160 px da GPU da qayta render) — alohida qaror |
| 9. DaVinci, Premiere, After Effects, Cinema 4D | yo'q (pullik, qo'lda ishlatiladi) | QO'LLANMAYDI; Blender — bor (Buck) |
"Mavzu/ssenariy yozma" degan band bizga TEGISHLI EMAS: producer ssenariyni ham yozadi (Shohjahon topshirig'i). Bu skill faqat vizual-texnik bosqichda o'qiladi.
