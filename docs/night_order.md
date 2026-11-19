# BUYURTMA 2026-11-20 tun — HOLAT: OCHIQ
Shohjahon (2026-11-20 03:42 Toshkent): "eng zo'r ssenariylardan videolar 2–3 soat ichida tayyor bo'lsin, grafika va sifat eng zo'r bo'lsin". Bu buyurtma soatga qaramay BIRINCHI bajariladi. Vaqt byudjeti: boshlanganidan 2 soat 15 daqiqa; undan keyin yangi render boshlama, tugatib yoz.
Chegaralar: `docs/producer_task.md` dagi QAT'IY CHEGARALAR to'liq amal qiladi.

## 1. Tayyorgarlik
- ElevenLabs tekshiruvi (producer_task 0-bo'lim). 200 bo'lmasa — hech narsa chiqarma, pastga sababini yoz va to'xta.
- Lab qimirlashi: `assets/buck3d_v2_talk.tar` repoda bormi? Yo'q bo'lsa har 5 daqiqada `git pull --rebase origin media` bilan ko'pi bilan 20 daqiqa kut (shu vaqtda 2-banddagi tekshiruvni qil). Baribir yo'q bo'lsa — usiz davom et va pastga yoz. Kutubxonani O'ZING render QILMA.
- Costco: WebSearch bilan rotisserie tovuq narxi hozir ham $4.99 ekanini tekshir. O'zgargan bo'lsa n2 ni tashlab, o'rniga script_bank S-01 ni yasab chiqar.

## 2. Render navbati (spec'lar tayyor va sinovdan o'tgan: `work/night_2026-11-20/`)
1. n1_fee64k.json — "A 1% Fee Can Cost You $64,000" (bank S-10)
2. n2_costco.json — "Costco's $4.99 Chicken Is Bait" (S-09)
3. n3_copier.json — "Why Copiers Refuse to Copy Money" (S-08)
4. n4_giftcards.json — "$27 Billion Is Hiding in Junk Drawers" (S-05)
5. n5_overbooking.json — "Airlines Sell Your Seat Twice. Legally." (S-06)
6. (vaqt qolsa) `work/2026-11-20/short1_trillion61_rendered.json` va `short2_turkey_flights_rendered.json` ni YANGI Buck (v2, bo'lsa lab qimirlashi) bilan qayta render qilib, AYNAN O'SHA fayl nomlari bilan (2026-11-20_trillion61.mp4, 2026-11-20_turkeyflights.mp4) almashtir. Ularni QAYTA POST QILMA — Metricool postlari allaqachon bor.
Spec matnidagi fakt va raqamlarni o'zgartirma (manbalari `docs/script_bank.md` da). Faqat texnik tuzatish mumkin: sahna vaqtlari ("at", "act_at", "sticker_at"), b-roll (har videoga ≤1 find_broll, odobli, ≤4 s sahna; shart emas), sfx.
Har biri: `python3 -I engine/make_video.py <spec> 2026-11-20_<nom>.mp4 --model .. --voices ..` → SIFAT NAZORATI (producer_task A-h): "buck_voice" faqat elevenlabs, "cinema": true, "buck3d": "v2"; 8 kadrni ko'r (matn sig'adi, Buck stat/subtitrni yopmaydi, sticker Buck ustiga tushmagan); ≤40 s (oshsa "speed" 1.15, yana oshsa eng kuchsiz bitta jumlani qisqartir — faktni emas); 2 kanal; mean −20..−12 dB. Muammo bo'lsa 1 marta tuzatib qayta render. Sifatdan o'tmagan videoni CHIQARMA.

## 3. Hosting va post
Push (producer_task A-i), raw URL 200. Avval Metricool getScheduledPosts bilan band slotlarni ko'r (trillion61 → 2026-11-20 10:00 ET, turkeyflights → 16:00 ET). Yangi videolarni BO'SH slotlarga tartib bilan qo'y: 2026-11-20 13:00 ET, 19:00 ET; 2026-11-21 10:00, 13:00, 16:00 ET (bitta slotga bitta video). Post parametrlari — producer_task A-j. Sarlavha ≤50 belgi (yuqoridagi nomlar), tavsif 1-qatori — izoh savoli (script_bank), "Sources:" to'liq nom va sana bilan, n1 uchun "Illustration from the U.S. Department of Labor ($25,000, 35 years, 7% a year)."

## 4. Yakun
- Playbook 9-bo'lim va `docs/script_bank.md` (ishlatilganlar [CHIQDI]) ni yangila.
- Shu fayl boshidagi HOLAT ni "BAJARILDI <vaqt>" qil va pastga natijani yoz: har video — fayl, uzunlik, slot, Metricool id, lab qimirlashi bor/yo'q; chiqmaganlari — sababi.
- Shohjahonga xabar (≤6 qator, o'zbekcha): nechta video tayyor, qaysi vaqtda chiqadi, muammo bo'lsa nima.

## NATIJA
(sessiya to'ldiradi)
