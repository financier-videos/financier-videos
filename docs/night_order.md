# BUYURTMA 3 (2026-11-20 21:15) — HOLAT: OCHIQ
Shohjahon (20:30): "hozir tashla namunani" — O'ZBEKCHA NAMUNA. Soatga qaramay BIRINCHI bajariladi; qisqa ish (bitta render), keyin odatdagi rejim davom etadi.
1. ElevenLabs 200 ekanini tekshir.
2. `work/uz_test/giftcard_uz.json` ni render qil → `work/uz_test/giftcard_uz.mp4` (spec tayyor: o'zbekcha matn, "buck_voice": {"variant":"D","model":"eleven_v3"}; vizual chat sessiyasida sinalgan). Matn va raqamlarni o'zgartirma.
3. Xato bo'lsa tartib bilan sinab ko'r va har birini NATIJA ga yoz: (a) eleven_v3 /with-timestamps bermasa — dvigatelda vaqt belgisiz yo'l bormi (bo'lmasa subtitrni jumla uzunligiga teng taqsimlash bilan chiqadigan kichik tuzatish kirit); (b) v3 da "speed"/"style" sozlamasi rad etilsa — settings ni olib tashla; (c) v3 umuman ishlamasa — TO'XTA: Kokoro yoki boshqa ovoz bilan chiqarma, sababini yoz.
4. Tekshir: kadrlar (har 3 s), uzunlik ≤45 s, −14 LUFS atrofida, check.py --platform reels. voice_check o'zbekcha uchun ISHLAMAYDI — o'tkazib yubor.
5. mp4 ni push qil (work/uz_test/ ichida qoladi — repo ildiziga emas, YouTube'ga QO'YILMAYDI, Instagram'ga ham QO'YILMAYDI). Shohjahonga xabar (SendUserMessage bo'lsa, fayl bilan — SendUserFile): "O'zbekcha namuna tayyor — talaffuzni eshitib baholang" + raw URL: https://raw.githubusercontent.com/financier-videos/financier-videos/media/work/uz_test/giftcard_uz.mp4
6. Shu fayl HOLAT ni "BAJARILDI <vaqt>" qil va NATIJA ni yoz (model, uzunlik, so'z vaqt belgilari ishladimi, lab-qimirlash bor-yo'qligi, eshitishda sezilgan narsa bo'lsa — yo'q, sen eshita olmaysan: faqat texnik natija).

## NATIJA (3)
(sessiya to'ldiradi)

# [arxiv] BUYURTMA 2 (2026-11-20 07:25) — BAJARILDI 2026-11-20 08:05
Shohjahon (07:15 va 07:22 Toshkent): "videolarni boshqattan yasa"; "bugun qo'yiladigan videolarni ham ko'rib chiq, eng zo'ri qilib tayyorlab joylashtir; grafika, video va ovoz eng yaxshi holatda bo'lsin". Sabab: tungi 5 video bir xil fonda va bir xil skeletda chiqqan. Bu buyurtma soatga qaramay BIRINCHI bajariladi. `docs/producer_task.md` QAT'IY CHEGARALARI va XILMA-XILLIK QOIDASI amal qiladi.

## 1. Render (spec'lar tayyor, chat sessiyasida zaxira ovoz bilan sinovdan o'tgan: `work/remake_2026-11-20/`)
Tartib — chiqish vaqti bo'yicha (eng yaqin slot birinchi):
| # | Spec | Yangi fayl | Sarlavha (≤50) | Format / theme | Almashtiriladigan Metricool posti (slot ET) |
|---|---|---|---|---|---|
| 1 | r6_trillion61.json | 2026-11-20_trillion61_v2.mp4 | (o'zgarmaydi) | raqam hikoyasi / royal | 434764903 (11-20 10:00) |
| 2 | r1_fee_guess.json | 2026-11-20_fee_guess.mp4 | Guess What a 1% Fee Costs You | taxmin o'yini / ember | 435015671 (11-20 13:00) |
| 3 | r7_turkeyflights.json | 2026-11-20_turkeyflights_v2.mp4 | (o'zgarmaydi) | vs / ocean | 434764979 (11-20 16:00) |
| 4 | r2_costco_case.json | 2026-11-20_costco_case.mp4 | The $4.99 Chicken Mystery | detektiv / noir | 435015740 (11-20 19:00) |
| 5 | r3_twenty_secrets.json | 2026-11-21_twenty_secrets.mp4 | 3 Secrets Hiding on a $20 Bill | sanoq / royal | 435023630 (11-21 10:00) |
| 6 | r4_giftcard_myth.json | 2026-11-21_giftcard_myth.mp4 | Gift Cards Feel Like Free Money | afsona vs haqiqat / mint | 435023666 (11-21 13:00) |
| 7 | r5_gate_story.json | 2026-11-21_gate_story.mp4 | Sorry, No Seat. Is That Legal? | "sen shu yerdasan" hikoyasi / ocean | 435023719 (11-21 16:00) |
- r6 b-roll: `mkdir -p /tmp/fin/broll && cp work/t1_61/*_seg.mp4 /tmp/fin/broll/`.
- 5-qator (royal) 1-qator bilan bir xil theme — ular ketma-ket emas, lekin xohlasang r3 ni "noir"/"vault" ga almashtirma: r2 noir. Qoldir.
- Fakt va raqamlarni o'zgartirma (manbalar `docs/script_bank.md`). Texnik tuzatish mumkin (vaqtlar, sfx, speed).
- SIFAT NAZORATI har videoga (producer_task A-h) + QO'SHIMCHA: (a) har 2 s dan kadr ol — qora siluet Buck yo'q, sticker/Buck/stat bir-birini yopmaydi, subtitr manba qatoriga tegmaydi (tegsa o'sha sahnada "show_source" ni qo'shni sahnaga ko'chir); (b) OVOZ: har jumlani tekshir — "timings" dagi sahna uzunligi so'z soniga mos kelmasa (≈0.33 s/so'z dan 40% ko'p) bu buzuq TTS take: keshdan o'chirib qayta render; mean −20..−12 dB, max ≤ −1 dB, 2 kanal; (c) ≤40 s (oshsa speed 1.15); (d) "buck_voice" faqat elevenlabs, "cinema": true, "buck3d": "v2". O'tmagan video CHIQARILMAYDI — eski post o'z holicha qoladi.

## 2. Joylash — YANGI POST EMAS, mavjud postni yangilash
Har video uchun: push (raw URL 200) → Metricool updateScheduledPost bilan o'sha post id sida media ni yangi raw URL ga, sarlavha/tavsifni yangisiga almashtir (vaqt o'zgarmaydi) → getScheduledPosts bilan media haqiqatan yangilanganini tekshir. updateScheduledPost ishlamasa yoki media yangilanmasa: YANGI post yaratma (bitta slotda ikki video bo'lib qoladi) — eski post qoladi, NATIJA ga "almashtirilmadi" deb yoz va Shohjahonga xabarda ayt (u Metricool'da o'zi almashtiradi yoki eski postni o'chiradi).
Tavsif: 1-qator izoh savoli (r1 "Did you guess it?", r2 "What did YOU leave with last time?", r3 "Which one did you already know?", r4 "How much is hiding in yours?", r5 "Cash or seat?"), keyin "Sources:" to'liq nom+sana, "Not financial advice. For education and entertainment.", "Buck is our original character.", 3 hashtag.

## 3. Yakun
Eski 2026-11-20_{fee64k,costco,copier,giftcards,overbooking,trillion61,turkeyflights}.mp4 fayllarini Metricool yangilangani tasdiqlangandan KEYIN o'chir. Playbook 9-bo'lim (format/emotsiya/theme/ochilish bilan), script_bank, growth_log (1 yozuv: yangi videolar eskisidan nimasi bilan farq qiladi) ni yangila. Shu fayl HOLAT ni "BAJARILDI <vaqt>" qil, NATIJA ni to'ldir. Shohjahonga ≤6 qator xabar.

## NATIJA
Sessiya 2026-11-20 07:25–08:05 Toshkent. ElevenLabs 200 (Buck D). 7/7 render QC dan o'tdi (elevenlabs, buck3d v2, cinema, stereo, mean −18.3..−18.6 dB, max ≤ −1.4 dB, ≤40 s) va 7/7 Metricool posti updateScheduledPost bilan almashtirildi (yangi media fayli, vaqt o'zgarmadi; getScheduledPosts bilan tasdiqlandi; yangi post yaratilmadi). Eski 7 mp4 o'chirildi.
| # | Fayl | Davomiylik | Yangi Metricool id | Izoh |
|---|---|---|---|---|
| 1 | 2026-11-20_trillion61_v2.mp4 | 36.9 s | 435051986 | 1-render 40.9 s + buzuq take ("$16.6 billion", 7.6 belgi/s) → say so'z bilan, tempo 1.08, max_pause 0.45 |
| 2 | 2026-11-20_fee_guess.mp4 | 34.1 s | 435052161 | chart yorlig'i subtitrga yaqin (o'qiladi) |
| 3 | 2026-11-20_turkeyflights_v2.mp4 | 35.7 s | 435052137 | "Ow. Worth it." 1.9 s — pauzali luqma, tabiiy |
| 4 | 2026-11-20_costco_case.mp4 | 33.9 s | 435052219 | stat "$40M" — ovozda "$30 to $40 million" |
| 5 | 2026-11-21_twenty_secrets.mp4 | 33.4 s | 435060150 | — |
| 6 | 2026-11-21_giftcard_myth.mp4 | 28.8 s | 435060242 | — |
| 7 | 2026-11-21_gate_story.mp4 | 29.2 s | 435060376 | 180/185 o'rindiq — illyustratsiya (tavsifda aytildi) |


## 1-BUYURTMA NATIJASI (arxiv, 2026-11-20 tun)
Sessiya 2026-11-20 06:40–07:45 Toshkent. ElevenLabs 200 (Buck D). Lip-sync kutubxonasi repoda bor edi (assets/buck3d_v2_talk.tar) — barcha videolarda ishlatildi; "buck3d": "v2", "cinema": true; qora siluet yo'q; mean −18.1..−18.7 dB, stereo. Costco narxi WebSearch: 2026 manbalarida $4.99 — n2 qoldi.
- n1 2026-11-20_fee64k.mp4 — 29.0 s — 2026-11-20 13:00 ET — Metricool 435015671 — lip-sync bor.
- n2 2026-11-20_costco.mp4 — 34.6 s — 2026-11-20 19:00 ET — Metricool 435015740 — lip-sync bor.
- n3 2026-11-20_copier.mp4 — 37.1 s (1-render 40.2 s: buzuq TTS take keshdan o'chirildi, qayta render) — 2026-11-21 10:00 ET — Metricool 435023630 — lip-sync bor.
- n4 2026-11-20_giftcards.mp4 — 27.3 s (1-render 31.8 s: oxirgi jumla buzuq take, qayta render) — 2026-11-21 13:00 ET — Metricool 435023666 — lip-sync bor.
- n5 2026-11-20_overbooking.mp4 — 26.1 s — 2026-11-21 16:00 ET — Metricool 435023719 — lip-sync bor. Kichik kamchilik: 3-sahnada 3 qatorli subtitr manba qatoriga tegadi (o'qiladi).
- 6-band: trillion61 (39.7 s) va turkeyflights (35.0 s) v2 + lip-sync bilan qayta render qilinib, xuddi shu fayl nomlari bilan repoda almashtirildi. QAYTA POST QILINMADI. DIQQAT: Metricool videoni o'z serveriga ko'chirgan, shuning uchun 434764903 / 434764979 postlari eski versiyani chiqaradi (yangilash uchun Metricool'da media almashtirish kerak).
