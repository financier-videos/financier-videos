# ROCCO PERSONAJLARI — 3D rig v1 (2026-11-22, chat Trade)

Shohjahon qarori: bundan keyin Rocco videolari MULTFILM yo'nalishida — epizodlar, suhbatlar, haqiqiy multfilm kabi; 3D personajlar bilan.
Eski yassi 2D chizmalar (rc_render.py dagi rocco/penny/slick) — vaqtinchalik, 3D kutubxona tayyor bo'lgach almashtiriladi.

Modellar (Shohjahon Tripo'da yasagan, chat rig qildi) — YOPIQ repoda: `financier-videos/buck-private` → `rocco_cast_v1/`
(`rocco_rigged.glb`, `penny_rigged.glb`, `slick_rigged.glb`, skriptlar, README). Ochiq repoga model qo'yilmaydi.

Ko'rinishi: `docs/looks_samples/rocco_cast3d_2026-11-22.jpg`, pozalar: `docs/looks_samples/rocco_cast3d_poses_2026-11-22.jpg`,
harakat sinovi: `rocco_cast_rig_test.mp4` (4 s: gapirish, ko'z qisish, qo'l harakati).

## Nima qimirlaydi
- Suyaklar: root, hips, chest, head, ear.L/R, upper_arm, forearm, hand, thigh, (shin — Slick), foot, tail (Rocco 3, Slick 2).
- Yuz (29 shape key): blink, wide, look_l/r/up/down, brow_up/down/angry/sad, smile, frown, narrow, wideM (har biri .L/.R) + jaw_open.
  Og'iz ichi — alohida to'q material: jaw_open ochilganda haqiqiy og'iz ko'rinadi.
- Penny: ko'ylak/bantik/poyabzal qizildan FIRUZAga o'zgartirilgan (Rocco qizilidan va mavjud personajlardan farq qilishi uchun).
- Slick: A-pozali variant olingan; "ayyor" ko'rinish — standart ifoda (blink 0.42, brow_angry 0.8, brow_down 0.4, smile.L 1.0, smile.R 0.3).

## KOD CHATI UCHUN — keyingi qadam (BUYURTMA 9)
1. `buck-private/rocco_cast_v1` ni oling. GPU'da (Runpod, Buck kutubxonasi kabi) har personaj uchun sprite kutubxonasi:
   kayfiyatlar (neutral, happy, shock, sad, angry, sly/deadpan, relieved) × og'iz (yopiq, yarim, ochiq, O, E) × ko'z qisish,
   + harakat kliplari (point, wave, shrug, stop-panja, sakrash, bosh irg'ash, orqaga tisarilish, telefon tutish), shaffof fon, 800 px, 24 fps.
   Yorug'lik: yorug' studiya (uslub v2 — luma ≥ 0.50), yumshoq soya.
2. `rc_render.py`: 2D chizmalar o'rniga shu kutubxona (`style: rocco3d`). Lab harakati — Buck'dagi kabi nutq konvertidan.
3. Birinchi 3D epizod: RC-04 (Free GTA 6 for PC) — qayta render, 10 kadrlik varaq → chat ko'radi → keyin chiqadi.
4. Ma'lum kamchiliklar (v1): qo'ltiq/plashch etagida mayda uchburchaklar (haddan tashqari qo'l pozasida) — pozalarni 60° gacha cheklang
   yoki chatga yozing; barmoqlar alohida qimirlamaydi; til/tish yo'q; Penny to'liq ko'z yumishi qo'pol (≤0.6 yoki 2 kadr).
