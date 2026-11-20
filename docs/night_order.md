# BUYURTMA 2 (2026-11-20 07:25) — HOLAT: OCHIQ
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
(sessiya to'ldiradi)

## 1-BUYURTMA NATIJASI (arxiv, 2026-11-20 tun)
Sessiya 2026-11-20 06:40–07:45 Toshkent. ElevenLabs 200 (Buck D). Lip-sync kutubxonasi repoda bor edi (assets/buck3d_v2_talk.tar) — barcha videolarda ishlatildi; "buck3d": "v2", "cinema": true; qora siluet yo'q; mean −18.1..−18.7 dB, stereo. Costco narxi WebSearch: 2026 manbalarida $4.99 — n2 qoldi.
- n1 2026-11-20_fee64k.mp4 — 29.0 s — 2026-11-20 13:00 ET — Metricool 435015671 — lip-sync bor.
- n2 2026-11-20_costco.mp4 — 34.6 s — 2026-11-20 19:00 ET — Metricool 435015740 — lip-sync bor.
- n3 2026-11-20_copier.mp4 — 37.1 s (1-render 40.2 s: buzuq TTS take keshdan o'chirildi, qayta render) — 2026-11-21 10:00 ET — Metricool 435023630 — lip-sync bor.
- n4 2026-11-20_giftcards.mp4 — 27.3 s (1-render 31.8 s: oxirgi jumla buzuq take, qayta render) — 2026-11-21 13:00 ET — Metricool 435023666 — lip-sync bor.
- n5 2026-11-20_overbooking.mp4 — 26.1 s — 2026-11-21 16:00 ET — Metricool 435023719 — lip-sync bor. Kichik kamchilik: 3-sahnada 3 qatorli subtitr manba qatoriga tegadi (o'qiladi).
- 6-band: trillion61 (39.7 s) va turkeyflights (35.0 s) v2 + lip-sync bilan qayta render qilinib, xuddi shu fayl nomlari bilan repoda almashtirildi. QAYTA POST QILINMADI. DIQQAT: Metricool videoni o'z serveriga ko'chirgan, shuning uchun 434764903 / 434764979 postlari eski versiyani chiqaradi (yangilash uchun Metricool'da media almashtirish kerak).
