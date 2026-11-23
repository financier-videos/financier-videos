# BUYURTMA 4 (2026-11-21 03:30) — HOLAT: BAJARILDI 2026-11-21 10:05 Toshkent
Shohjahon (03:28): "hali joylanmagan hamma videolarni boshqattan YANGI BUCK bilan qilib chiqasan; boshqa chatda yangi Buck yasalyapti."
SHART (boshlash): yangi Buck kutubxonasi repoda paydo bo'lsa — `media` da assets/buck3d_*.tar ga yangi commit (yangi fayl, masalan buck3d_v3.tar, yoki buck3d_v2.tar almashtirilgan; `git log -1 --format=%ci -- assets/` 2026-11-21 03:30 dan keyin) YOKI shu faylda Shohjahon/chat "BUCK TAYYOR" deb yozgan bo'lsa. Shart bajarilmagan bo'lsa — bu buyruqni o'tkazib yubor (odatdagi rejim), keyingi ishga tushishda yana tekshir.
1. Dvigatel yangi kutubxonani olishini ta'minla: yangi nom bo'lsa engine/make_video.py BUCK3D_LIBS ro'yxatining boshiga qo'sh (talk kutubxonasi bo'lsa — u ham). Qisqa sinov render: natija JSON "buck3d" yangi versiyani ko'rsatsin; 4–6 kadrni Read bilan ko'r (Buck kadrdan chiqmaydi, raqam/subtitrni yopmaydi, lab-qimirlash).
2. HALI CHIQMAGAN postlarni (getScheduledPosts bilan tekshir — chiqib bo'lganlariga TEGMA) chiqish vaqti bo'yicha tartibda qayta render qil. Holat 03:30 dagi ro'yxat (Metricool id: YT / IG):
   - 21-noy 10:00 ET twenty_secrets — 435060150 / 435716081 — spec work/remake_2026-11-20/r3_twenty_secrets.json
   - 21-noy 13:00 ET giftcard_myth — 435060242 / 435716104 — r4_giftcard_myth.json
   - 21-noy 16:00 ET gate_story — 435060376 / 435716122 — r5_gate_story.json
   - 21-noy 19:00 ET subscriptions — 435035715 / 435716142 — work/2026-11-20b/s01_subscriptions.json
   - 22-noy 10:00 ET airport_cap — 436158013 / 436158099 — work/2026-11-22/s1_airport.json (xarita: work/pilot_map/map_insert.py --from 36 --to 34 --label "" --title "JFK · LGA · NEWARK" --secs 5 --theme ocean → /tmp/fin/broll/nyc_map.mp4)
   - 22-noy 13:00 ET bf_vs_cm — 436158072 / 436158149 — work/2026-11-22/s2_bfcm.json
   - (20-noy 19:00 ET costco_case 435052219 / 435716038 — bu buyruq vaqtida allaqachon chiqqan bo'lishi mumkin; chiqmagan bo'lsa — r2.)
   Har spec'ga yangi qoida bo'yicha "bg" (producer_task 3a, engine/pixabay_bg.py) qo'sh; spec'dagi /tmp b-roll yo'llari yo'q bo'lsa — qayta yasab/yuklab ol yoki o'sha sahnadan "broll" ni olib tashla. Matn, raqam va ovoz O'ZGARMAYDI (TTS kesh bo'lmasa — qayta generatsiya, voice_check ≥0.86).
3. QC: −14 LUFS, check.py --platform shorts 0 FAIL, blackdetect 0, fayl ≤90 MB, 6–8 kadr.
4. Yangi nom bilan push (masalan <eski_nom>_b2.mp4; eskisini o'chir), raw URL 200 bo'lgach Metricool updateScheduledPost — YT va IG postlari, VAQT, sarlavha va matn o'zgarmaydi (faqat media; matnga "Footage: Pixabay (...)" qo'shish mumkin). Javobdagi yangi id larni shu yerga yoz.
5. Slotgacha 60 daqiqadan kam qolgan post — tegma (eski versiya chiqadi), NATIJA ga yoz.
6. O'zbekcha Reellar (finansist424) allaqachon chiqqan — qayta qo'yilmaydi. Bundan keyingi barcha videolar faqat yangi Buck bilan.
7. HOLAT ni "BAJARILDI <vaqt>" qil, NATIJA yoz, Shohjahonga xabar (PushNotification): nechta video yangilandi, qaysilari ulgurmadi.

## BUCK TAYYOR (chat, 2026-11-21 10:55 Toshkent)
Yangi Buck kutubxonasi `media` da: `assets/buck3d_v3.tar` (226 kadr: 12 kayfiyat x 15 + flip 11 / bonk 23 / dodge 12) va `assets/buck3d_v3_talk.tar` (540 kadr: har kayfiyat uchun _t1/_t2/_t3). 800 px WebP, oyoq chizig'i 0.86 (v2 bilan bir xil).
- Dvigatel allaqachon yangilangan (engine/make_video.py: BUCK3D_LIBS boshida "v3", talk `buck3d_v3_talk.tar`, b3_feet v3 = 0.86). Chatda tekshirildi: buck3d_ready() -> ver "v3", talk True; mascot3d_patch happy/smug/shocked/point/dizzy + talk 1-3 to'g'ri chiqdi. To'liq video render (ovoz bilan) chatda sinalmagan — 1-banddagi qisqa sinovni baribir qil.
- Yangi Buck KENGROQ: o'ng qo'lida (kadrda chapda) skipetr, "happy" da chap qo'li tepada. "corner" holatda skipetr yoki qo'l sarlavha/raqamni yopmasligini kadrlarda tekshir; yopsa mascot "pos" ni almashtir yoki o'sha sahnada boshqa kayfiyat ol.
- "shocked", "dodge", "bonk" da monokl zanjirida osilib turadi (ataylab). "flip" o'rta kadrlarida Buck kadr tepasidan qisman chiqadi (v2 dagidek).
- Ma'lum zaifliklar: kadrlar CPU da 24 namuna bilan chizilgan (GPU qayta render keyin); gapirish variantlari faqat og'iz sohasini almashtirib yig'ilgan.
- Model va rig fayllari faqat maxfiy repoda (buck-private/rig_v1). Bu repoga QO'YILMAYDI.

## NATIJA (4) — vazifa sessiyasi, 2026-11-21 09:35–10:05 Toshkent
- Dvigatel o'zgartirilmadi (chat allaqachon v3 ni BUCK3D_LIBS boshiga qo'ygan). Natija JSON "buck3d": "v3", talk bor. 1-render (twenty_secrets) kadrlari Read bilan ko'rildi: corner Buck skipetri sarlavha/raqamni yopmaydi, Buck kadrdan chiqmaydi.
- 6/6 chiqmagan post qayta render qilindi (Buck v3 + Pixabay "bg"; matn/raqam/sarlavha/vaqt o'zgarmadi; tavsifga "Footage: Pixabay (...)" qo'shildi). TTS kesh yo'q edi → qayta generatsiya, voice_check hammasi ≥0.86. QC: −14.0..−14.2 LUFS, shorts 0 FAIL, blackdetect 0, fayl 43–52 MB.
  | video | slot ET | yangi fayl | voice | YT id | IG id |
  |---|---|---|---|---|---|
  | twenty_secrets | 21-noy 10:00 | 2026-11-21_twenty_secrets_b3.mp4 | 0.908 | 436377479 | 436377496 |
  | giftcard_myth | 21-noy 13:00 | 2026-11-21_giftcard_myth_b3.mp4 | 0.973 | 436378496 | 436378508 |
  | gate_story | 21-noy 16:00 | 2026-11-21_gate_story_b3.mp4 | 0.993 | 436378556 | 436378566 |
  | subscriptions | 21-noy 19:00 | 2026-11-20_subscriptions_b3.mp4 | 0.886 | 436383121 | 436383138 |
  | airport_cap | 22-noy 10:00 | 2026-11-22_airport_cap_b3.mp4 | 0.945 | 436383180 | 436383197 |
  | bf_vs_cm | 22-noy 13:00 | 2026-11-22_bf_vs_cm_b3.mp4 | 0.983 | 436383257 | 436383285 |
- Ulgurmaganlar: yo'q (eng yaqin slot 21-noy 10:00 ET edi — ~10 soat qolgan). costco_case 20-noy 19:00 ET da chiqib bo'lgan (getScheduledPosts da yo'q) — tegilmadi.
- Fonlar: twenty — padrinan, asabovebelowloa, Dimitri_K; giftcard — tommyvideo, xBriantcx, JawadAliKhan; gate — Coverr-Free-Footage, wserrano, Martin_Grabo; subscriptions — Coverr-Free-Footage, QuinceCreative; airport va bfcm — avvalgi kliplar (o'sha mualliflar).
- Shu ishda yangi 2 Short (22-noy 16:00/19:00 ET) ham faqat v3 bilan yasaldi; o'zbekcha 2 Reel (finansist424) — v3.

# BUYURTMA 3 (2026-11-20 21:15) — HOLAT: BAJARILDI 2026-11-20 20:50 Toshkent
Shohjahon (20:30): "hozir tashla namunani" — O'ZBEKCHA NAMUNA. Soatga qaramay BIRINCHI bajariladi; qisqa ish (bitta render), keyin odatdagi rejim davom etadi.
1. ElevenLabs 200 ekanini tekshir.
2. `work/uz_test/giftcard_uz.json` ni render qil → `work/uz_test/giftcard_uz.mp4` (spec tayyor: o'zbekcha matn, "buck_voice": {"variant":"D","model":"eleven_v3"}; vizual chat sessiyasida sinalgan). Matn va raqamlarni o'zgartirma.
3. Xato bo'lsa tartib bilan sinab ko'r va har birini NATIJA ga yoz: (a) eleven_v3 /with-timestamps bermasa — dvigatelda vaqt belgisiz yo'l bormi (bo'lmasa subtitrni jumla uzunligiga teng taqsimlash bilan chiqadigan kichik tuzatish kirit); (b) v3 da "speed"/"style" sozlamasi rad etilsa — settings ni olib tashla; (c) v3 umuman ishlamasa — TO'XTA: Kokoro yoki boshqa ovoz bilan chiqarma, sababini yoz.
4. Tekshir: kadrlar (har 3 s), uzunlik ≤45 s, −14 LUFS atrofida, check.py --platform reels. voice_check o'zbekcha uchun ISHLAMAYDI — o'tkazib yubor.
5. mp4 ni push qil (work/uz_test/ ichida qoladi — repo ildiziga emas, YouTube'ga QO'YILMAYDI, Instagram'ga ham QO'YILMAYDI). Shohjahonga xabar (SendUserMessage bo'lsa, fayl bilan — SendUserFile): "O'zbekcha namuna tayyor — talaffuzni eshitib baholang" + raw URL: https://raw.githubusercontent.com/financier-videos/financier-videos/media/work/uz_test/giftcard_uz.mp4
6. Shu fayl HOLAT ni "BAJARILDI <vaqt>" qil va NATIJA ni yoz (model, uzunlik, so'z vaqt belgilari ishladimi, lab-qimirlash bor-yo'qligi, eshitishda sezilgan narsa bo'lsa — yo'q, sen eshita olmaysan: faqat texnik natija).

## NATIJA (3)
Sessiya 2026-11-20 20:34–20:50 Toshkent (rejalashtirilgan vazifa). ElevenLabs 200.
- Model: eleven_v3, Buck D (Wisecracker), "settings": {"speed": 1.0} QABUL QILINDI (rad etilmadi). Natija JSON: buck_voice "elevenlabs:Buck D (Wisecracker)/eleven_v3", buck3d v2, cinema true.
- /with-timestamps v3 da ISHLAYDI (alignment qaytadi) — subtitrlar so'zma-so'z (kadrlarda tasdiqlandi).
- XATO TOPILDI VA TUZATILDI: v3 "previous_text"/"next_text" ni rad etadi (400 unsupported_model) — dvigatelning qayta urinishi faqat settings'ni olib tashlardi, shuning uchun har jumla yiqilardi. engine/make_video.py el_speak: model eleven_v3 bo'lsa prev/next yuborilmaydi (inglizcha multilingual_v2 ga ta'sir yo'q).
- Uzunlik 38.4 s (≤45). Sahnalar: 6.5/3.7/9.0/3.5/6.8/5.2/3.8 s; buzuq take belgisi yo'q (11–15 belgi/s).
- Ovoz: −14.0 LUFS, true peak −2.2 dBTP, stereo. blackdetect: 0. check.py --platform reels: 13 tekshiruv, 0 FAIL (faqat "subtitles none" WARN).
- Kadrlar (har 3 s): vs → "?" maket → $0 ochiladi; Buck drop_in, 43% / $244 / $27 MLRD stat, bonk; o'zbekcha matn sig'adi, Buck raqam/subtitrni yopmaydi.
- Lab-qimirlash: talk kutubxonasi yuklandi (90 ta *_t1_* kadr) → og'iz nutq energiyasiga moslashadi (texnik jihatdan yoqiq; eshitib/ko'rib baholash Shohjahonda).
- voice_check o'tkazilmadi (o'zbekcha uchun ishlamaydi). Talaffuzni men eshita olmayman.
- Fayl: work/uz_test/giftcard_uz.mp4 (31 MB). YouTube/Instagram'ga QO'YILMADI.

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

## BUYURTMA 5 — TREND: GTA 6 (chat Trade, 2026-11-21 14:56 UTC) — HOLAT: OCHIQ, muddat 2026-11-23 15:00 UTC (48 soat; kech qolsa bekor)
Nega: hozir YouTube'dagi eng katta mavzu (docs/trend_radar.md, SKAN 20:00). O'yin kadri, logotip, personaj rasmi, musiqa ISHLATILMAYDI — faqat o'z animatsiya, raqam grafikasi.
YANGILANDI: tayyor ssenariylar docs/script_bank.md T-01…T-05 (yangi tuzilmalar, sahnama-sahna tasvir rejasi) — pastdagi 1–5 o'rniga O'SHALARNI ishlat.
FINANCIER (keyingi bo'sh slotlar, sprint chelagi "trend", kuniga ≤2, ketma-ket emas):
 1. MIKRO 8–12 s: "$3.79 Billion in ONE Day" — birinchi kun savdosi, bitta taqqos (GTA V 2013: $800M).
 2. 25–30 s: "GTA 6 Made More in a Day Than…" — $3.79B vs GTA V $800M; 32.5M nusxa oldindan; "bu savdo bahosi, foyda emas" jumlasi shart.
 3. 25–30 s: "32.5 Million Copies Before Launch" — oldindan sotuv rekordi + 13 yillik kutish (GTA V 2013 → 2026).
 Manba satri: "Source: Take-Two Interactive press release, Nov 20, 2026". Byudjet/foyda mish-mishlari YO'Q. Sarlavhada raqam.
ROCCO (Buffer, vidIQ Rocco profili):
 4. "GTA 6 on PC? It's a Trap" — qizil bayroq: PC/mobil versiya yo'q; himoya qadami: faqat rasmiy konsol do'koni.
 5. "Free GTA 6 Key = Stolen Account" — bepul kalit/keygen; himoya: hech narsa yuklamaslik, 2 bosqichli himoya. Manba: McAfee, NordVPN ogohlantirishlari (2026-11). Hujum usuli ko'rsatilmaydi.
O'lchov: results.md da "trend" belgisi, 72 soatda odatdagi Shortlar bilan solishtiruv.

## BUYURTMA 6 — KO'RINISH XILMA-XILLIGI (chat Trade, 2026-11-21 15:29 UTC) — HOLAT: OCHIQ, ENG YUQORI USTUVORLIK (yangi video yasashdan OLDIN)
Shohjahon 20:26: "videolar yana bir xil: yozuvlar, grafikalar, lavhalar, stillar". To'liq qoida va dalil: docs/looks.md, docs/looks_evidence_2026-11-21.jpg.
1. Dvigatelga `spec["look"]` qo'sh (Rocco "style" kabi tarmoq): birinchi navbatda 3 ta — **paper, fullbleed, split**; keyin chalk, receipt, neon. Har biri docs/looks.md jadvalidagi 6 o'qning hammasini o'zgartiradi. Shriftlar faqat ochiq litsenziyali (OFL) — assets/fonts ga.
2. engine/look_check.py ni qc_gate ga qadam qilib ula (yangi video vs oxirgi 4): ≥0.70 = FAIL.
3. Hali CHIQMAGAN navbatdagi videolar (2026-11-22 va keyingilari): slotgacha ≥60 daqiqa bo'lsa yangi look bilan QAYTA RENDER (ovoz qayta yozilmaydi — faqat tasvir), Metricool'da almashtir. Ketma-ket 3 ta bir xil look bo'lmasin.
4. Har look uchun 1 kadrlik kontakt-varaqni docs/looks_samples/ ga qo'y va changes.md ga yoz — chat (Trade) ko'rib tekshiradi.
5a. MAVZUGA MOS LAVHA: producer_task "g" (yangi) — har Shortda ≥40% sahna aytilayotgan gapga mos Pixabay lavhasi, to'liq ekran, yorqin; qc_gate ga "broll ulushi" tekshiruvi. Qayta renderda ham qo'lla.
5b. SSENARIY v2: docs/script_rules.md; engine/script_check.py ni qc_gate ga ula; dvigatelga uzun Short (45–85 s) va 'har sahnaga o'z tasviri' uchun kerakli sahna turlari (hisoblagich, tasma/taxlam, yil taymlayni). 5c. Har video yozuvida 'Skillar:' qatori bo'lmasa qc_gate FAIL.
5d. KADR TEMPI VA IKKI OVOZ (docs/lessons_winners_2026-11-21.md): dvigatelga sahna ichida "shots" (har ≤2 s yangi tasvir), 1–3 so'zli sinxron subtitr rejimi, doimiy sarlavhasiz rejim, ikkinchi ovoz (spec "voices"); qc_gate: kadr soni (30 s ≥15, 60 s ≥30). Tayyor ssenariylar: script_bank V-01…V-05 va T-01…T-05 — ERTANGI 8 slotga shulardan (aralashma script_rules v2.1).
5. Qila olmagan qismingni "QILINMADI: sababi" deb shu yerga yoz — jim qoldirma.
JARAYON (vazifa sessiyasi, 2026-11-21 16:25 UTC): 2-band BAJARILDI — qc_gate 10-qadam `--prev <oxirgi 4>` (look_check, ≥0.70 FAIL). Rocco uchun alohida look (case-file, v6.12) — r01 Financier'ga nisbatan 0.51–0.64. QILINMADI hali: 1-band (paper/fullbleed/split) va 3-band (navbatdagilarni qayta render) — sabab: shu sessiyada navbatdagi 8 video ko'rigi, airport_cap qayta render va Rocco birinchi videosi bajarildi; keyingi ishga tushishda improvement_backlog 1-band sifatida birinchi navbatda.

## BUYURTMA 7 — HAMMASINI YANGI USULGA O'TKAZISH (chat Trade, 2026-11-21 16:29 UTC) — HOLAT: OCHIQ, BUYURTMA 6 bilan birga ENG YUQORI
Shohjahon 21:27: "hamma narsani yangi ishlaydiganiga almashtir, videolarni boshqatdan yasab chiqsin, portlatadigan videolar bo'lishi kerak".
1. Bugundan ESKI SHABLONDA yangi video YASALMAYDI. Har yangi video: script_rules v2.1 + looks.md + lavha ≥40% + kadr har ≤2 s + subtitr 1–3 so'z; post oldidan qc_gate (look_check, script_check) PASS.
2. Dvigatel (BUYURTMA 6: 1, 5a, 5b, 5d) — BIRINCHI ISH. Minimal to'plam, shu tartibda: (a) "shots" — sahna ichida har ≤2 s yangi tasvir; (b) 1–3 so'zli sinxron subtitr + doimiy sarlavhasiz rejim; (c) look "fullbleed" (lavha yorqin, qoraytirish ≤25%); (d) look "paper" va "split"; (e) ikkinchi ovoz. (a)+(b)+(c) tayyor bo'lishi bilan videolar chiqa boshlaydi — qolganini kutma.
3. NAVBATDAGI 8 MAVZU (Metricool 8198538; eski shablon): 436448923/436378508 gift cards (21-noy 23:00 — ulgurilmaydi, eski ko'rinishda chiqadi: taqqoslash uchun asos), 436378556/436378566 no seat (22-noy 02:00), 436383121/436383138 subscriptions (05:00), 436729765/436729817 airport (20:00), 436383257/436383285 BF vs CM (23:00), 436389660/436389672 cart (23-noy 02:00), 436389711/436389720 pink/blue (05:00), 436535579 fees (20:00).
   Har biri script_bank R-01…R-08 bo'yicha QAYTADAN yasaladi (yangi matn → ovoz qayta yoziladi) va Metricool'da media almashtiriladi. Yangi versiya slotdan ≥30 daqiqa oldin tayyor bo'lmasa — post O'CHIRILMAYDI, keyingi bo'sh slotga SURILADI (eski ko'rinish chiqmasin). Chiqib bo'lgan eski videolar o'chirilmaydi.
4. Yangi videolar: script_bank T-01…T-05 (GTA 6, muddat 23-noy 15:00 UTC) va V-01…V-05 — kuniga 8 slot (sprint_10d.md), aralashma script_rules v2.1.
5. Birinchi 3 ta yangi video chiqishi bilan: har biridan 10 kadrlik kontakt-varaq docs/looks_samples/ ga + changes.md ga qator — chat (Trade) eski 8 tasi bilan yonma-yon tekshiradi va Shohjahonga ko'rsatadi.
6. Ulgurmagan har band: "QILINMADI: sababi, qachon" — shu yerga.

### BUYURTMA 7 ga TUZATISH — NAVBAT TARTIBI (chat Trade, 2026-11-21 16:31 UTC; Shohjahon 21:30: "hozir trenddagi mavzularni birinchi qilish foydaliroq emasmi?") — USTUN
TREND BIRINCHI. Tartib: (1) trend videolari — umri 48 soat; (2) sanaga bog'liq (Black Friday R-05 — 27-noyabrgacha); (3) yangi doimiy formatlar V-01…V-05; (4) eski mavzularni qayta yasash R-01…R-08 (ular eskirmaydi — kutishi mumkin).
- Eng yaqin slotlar (22-noy 02:00 va 05:00 Toshkent): T-02 (mikro "$43,866 Every Second" — eng tez yasaladi) va T-01 ("How Big Is $3.79 Billion in ONE Day?"). Shu slotlardagi eski postlar (no seat, subscriptions) keyinga SURILADI.
- 22-noy kun davomida: T-03 (Financier), T-04 va T-05 (Rocco, Buffer). Hammasi 23-noy 15:00 UTC gacha; kech qolgani bekor.
- Dvigatelning yangi imkoniyati (shots/subtitr/fullbleed) trend slotiga ulgurmasa: trend videosi baribir chiqadi — mavjud dvigatelda, lekin yangi ssenariy, ≥40% yorqin to'liq ekranli lavha (bg_bright bilan) va script_check PASS bilan. Trendni kutib o'tkazib yuborma.
- DOIMIY QOIDA: har ishga tushishda avval trend_radar ning oxirgi skani; trend videosi bor bo'lsa — o'sha kunning BIRINCHI slotlari unga.

### BUYURTMA 7 ga QO'SHIMCHA — ROCCO BUGUN (chat Trade, 2026-11-21 16:33 UTC; Shohjahon 21:32: "Rocco'ning ham videosini bugunning o'zida tayyorla")
- r01 (brushing) tayyor va Buffer'da 21-noy 17:00 ET — chat ko'rib chiqdi: look_check PASS (Financier'ga 0.55–0.64), lavha 5/10, −14 LUFS tekshiruvi qc da. O'zgartirish shart emas.
- BUGUNGI ishga tushishda (23:17 Toshkent) Financier T-02/T-01 bilan BIR QATORDA: Rocco T-04 "GTA 6 on PC? It's a Trap" (script_bank) — render, QC, Buffer'ga 22-noy eng yaqin bo'sh slotga (r01 dan kamida 3 soat keyin). T-05 (mikro) — 22-noy kun davomida.
- Rocco uchun ham: har ≤2 s yangi kadr (10 sahna/34 s kam — keyingisida ≥17 kadr), subtitr 1–3 so'z, 1-kadrda to'liq hook yozuvi.

### !!! ROCCO r01 — ESKI HOLATDA CHIQMAYDI (chat Trade, 2026-11-21 16:34 UTC; Shohjahon 21:33: "yana eski holatdami? sen bilan ko'rib chiqdik-ku") — yuqoridagi "r01 o'zgartirish shart emas" BEKOR
BUGUNGI 23:17 ishga tushishda ENG BIRINCHI ISH (Financier trendidan ham oldin, chunki post 03:00 Toshkentda chiqadi):
1. Buffer postini ushla: `python3 -I engine/buffer_post.py delete 6b01befd142c957519268046` (yoki keyinga sur) — r01 eski ko'rinishda CHIQMASIN.
2. r01 ni YANGI qoidada qayta yasa (mavzu va faktlar o'sha: brushing, FTC 2026-08): tuzilma client_dialogue yoki why_story (voqea o'rtasidan: "A box lands on your porch. Your name. You ordered nothing."), javob/himoya qadami oxirida; ≥17 kadr / 34 s (har ≤2 s yangi tasvir); subtitr 1–3 so'z sinxron; 1-kadrda to'liq hook yozuvi; pastdagi doimiy "CASE FILE" yorlig'i HAR kadrda turmasin (faqat bo'lim almashganda 1.5 s); lavha ≥50% to'liq ekran, 4 yo'ldan kamida 3 tasi (to'g'ridan-to'g'ri: quti/eshik; masshtab: saralash markazi dron; metafora: qarmoq/tuzoq; his: tungi ko'cha).
3. qc_gate + look_check + script_check PASS → Buffer'ga 22-noy eng yaqin slot. Ulgurmasa — post yo'q, sababi shu yerga.
4. Keyin T-04 (GTA 6 PC tuzog'i) — o'sha qoidada.

### JARAYON (vazifa sessiyasi, 2026-11-21 23:20 Toshkent) — ROCCO r01
- 1-band BAJARILDI: Buffer'dagi r01 posti (id 6b01d6af8bd84d5966080972 — eski 6b01befd… o'rnida qayta qo'yilgan, 21-noy 22:00 UTC) O'CHIRILDI. Buffer'da rejalashtirilgan post yo'q. Video fayl repoda qoladi.
- TUZATISH (23:35 Toshkent): o'chirilgan 6b01d6af… posti aslida parallel kod sessiyasining (branch claude/lucid-volta-x5cic0) YANGI r01 v2 posti edi (qc PASS). XATO tuzatildi: r01 v2 mp4 `media` ga qo'yildi va Buffer'ga qayta rejalashtirildi — id 6b01e0a50247969092f278c1, 2026-11-21 22:00 UTC, sarlavha "A Box You Never Ordered? It's a Scam Sign", matn work/rocco/r01_v2/desc.txt. Eski r01 (6b01befd…) o'sha sessiya tomonidan o'chirilgan.
- DIQQAT boshqa sessiyalarga: claude/lucid-volta-x5cic0 dagi ish (dvigatel v6.14, T-02, T-01 spec, T-04 spec) hali `media` ga birlashtirilmagan.
- QILINMADI (vazifa sessiyasi, 23:50 Toshkent): T-01 (19:00 ET slot) va Rocco T-04 — sabab: kod sessiyasi (claude/lucid-volta-x5cic0) ularni dvigatel v6.14 da yasamoqda (t01_how_big.json, t04.json bor); takror yasash slot to'qnashuviga olib keladi. Keyingi ishga tushishda: 19:00 ET slot hali bo'sh bo'lsa va o'sha branchda T-01 mp4 bo'lmasa — shu sessiya yasaydi.

### JARAYON (kod sessiyasi 01MWGZtb7, 2026-11-21 22:15–00:00 Toshkent) — START_HERE navbati
- 1. ROCCO r01: eski post 6b01befd… o'chirildi; r01 v2 (why_story, fullbleed, 44 s, 25 kesim) qc_gate PASS → Buffer (hozir 6b01e0a5…, 21-noy 22:00 UTC; vazifa sessiyasi tasodifan o'chirib qayta qo'ygan).
- 2. TREND: T-02 → Metricool 22-noy 02:00 Toshkent (YT 436903322, IG 436903474). Eski no seat / subscriptions 24-noy 02:00/05:00 ga SURILDI. T-01 → 22-noy 05:00 (YT 436928897, IG 436929041). T-04 (Rocco) → Buffer 6b01e461…, 22-noy 15:00 UTC.
- 3. DVIGATEL v6.14: (a) shots + auto_shots, (b) 1–3 so'zli subtitr + headline hook, (c) look fullbleed — TAYYOR. QILINMADI: (d) paper, split; (e) ikkinchi ovoz ("voices") — sabab: shu sessiya trend videolariga ketdi; keyingi kod sessiyasida birinchi navbatda. Neon look ham yo'q (T-02 fullbleed bilan chiqdi).
- QILINMADI: T-03, T-05 (trend, muddat 23-noy 15:00 UTC), V-01…V-05, C-01/C-02, R-05 (BF, 27-noyabrgacha), R-01…R-08 — sabab: vaqt; 22-noy 20:00 (airport) va 23:00 (BF vs CM) eski shablondagi postlar hali surilmagan — keyingi sessiya slotdan ≥30 daq oldin yangi versiya qo'ysin yoki sursin.
- DIQQAT: kod sessiyasi videolari `claude/lucid-volta-x5cic0` branchida (raw URL shu branchdan); media ga merge Shohjahon ruxsati bilan.

## KO'RIK №1 — yangi videolar (chat Trade, 2026-11-21 19:49 UTC) — kod va vazifa sessiyalari uchun TUZATISHLAR
Rasm: docs/looks_samples/review_2026-11-22_new_vs_old.jpg. O'lchov (look_check --matrix; kesim = ffmpeg scene>0.22):
| Video | look | yorqinlik | eski 3 taga o'xshashlik | qattiq kesim |
|---|---|---|---|---|
| gta_per_second (13.7 s) | fullbleed | 0.31 | 0.47–0.58 | 7 (1.7 s/kesim) ✔ |
| gta_how_big (51.9 s) | vault+words | 0.18 | 0.61–0.69 (chegarada) | 11 (4.3 s) |
| gta_timeline (26.3 s) | paper | 0.69 | 0.30–0.43 | 5 (4.4 s) |
| airport_r04 (26.5 s) | split | 0.40 | 0.17–0.26 ✔ | 5 (4.4 s) |
| cart_r06 (27.8 s) | paper | 0.69 | 0.32–0.43 | 3 (6.9 s) |
YAXSHI: uch xil yangi ko'rinish haqiqatan farq qiladi (eski 8 tasi o'zaro 0.77–0.91 edi); subtitr 1–3 so'z; lavhalar ko'rinadi; Rocco r01v2/T-04 — har sahnada boshqa lavha.
TUZATILSIN (ustuvorlik tartibida):
1. PAPER TAKRORI: gta_timeline ↔ cart_r06 = 0.93 (deyarli bir xil), oralarida atigi 2 post. look_check --prev ga navbatdagi (hali chiqmagan) videolar ham kirsin; paper uchun kamida 3 variant (qog'oz rangi: krem / gazeta kulrang / ko'k chizmali daftar; foto joyi: tepa / chap ustun / to'liq kenglik) — yoki cart_r06 boshqa lookka o'tkazilsin (slot 23-noy 02:00 Toshkent).
2. PAPER BO'SH: kadrning ~55% i bo'sh krem; foto kichik (kenglikning 80%, balandlikning 18%). Foto balandligi ≥35%, raqam va subtitr orasida bo'shliq qolmasin, Buck ≥1/4 kadr. Bitta sahnada foto TO'LIQ sahifa bo'lsin.
3. KADR TEMPI HALI SEKIN (per_second dan tashqari): 4.3–6.9 s/kesim; me'yor ≤2 s. Kamera siljishi kesim hisoblanmaydi — boshqa lavha/boshqa plan kerak. 27 s video = ≥14 xil tasvir.
4. gta_how_big hali qorong'i (0.18) va eski shablonga 0.69 gacha o'xshash — scale_ladder pog'onalari (Oy, XKS, taxlam) to'liq ekranli yorqin lavha/grafika bo'lsin, vault emas. Keyingi narvon videosida.
5. gta_per_second: "$3.79B" 8 kadrdan 4 tasida — raqam bir marta, qolganida yangi tasvir.
6. NAVBATDA HALI ESKI SHABLON (Metricool): BF vs CM 436383257/436383285 (22-noy 23:00 — ENG YAQIN, R-05), pink/blue 436389711/436389720 (23-noy 05:00, R-07), fees 436535579 (23-noy 20:00, R-08), no seat 436864779/436864859 (24-noy 02:00, R-02), subscriptions 436864890/436865045 (24-noy 05:00, R-03). Slotdan ≥30 daq oldin almashtir yoki sur.
7. Hali yo'q: ikkinchi ovoz bilan birorta video (C-01, C-02, V-02, R-02, R-05, R-07), komediya harakatlari (doubletake/jawdrop/…) ishlatilgan video, V-01 (buck tarixi).
INSTAGRAM @redfrocco: T-04 Reel CHIQDI (ikkinchi urinish; birinchisida konteyner 20 s da so'ralgan — kamida 45 s kut): https://www.instagram.com/reel/DgBBJi1HK90/ . Rocco Reel'lari endi vidiq_instagram_publish_reel bilan, platformAccountId 29264618826539059, isAiGenerated true. r01v2 — yuzli klip almashtirilgach.

### JARAYON №2 (kod sessiyasi 01MWGZtb7, 2026-11-22 00:15–02:00 Toshkent) — KO'RIK №1 javobi
- 1 PAPER TAKRORI: R-06 fullbleed ga o'tdi; paper 3 variant (cream/news/grid): T-03 news, R-08 grid. 2 PAPER BO'SH: foto kattaroq, har kesimda katta foto ↔ karta, Buck kattaroq. 3 KADR TEMPI: dvigatel v6.15 — avtomatik kesim boshqa klipga o'tadi; qc_gate 11 endi ffmpeg scene>0.22 bilan o'lchaydi; navbatdagi hamma video 1.5–1.9 s/kesim. 4 gta_how_big: vault → split (yorqinroq). 5 per_second: QILINMADI (chiqib bo'lgan slotga yaqin; 8 kesim / 13.7 s me'yorda). 6 ESKI SHABLON: hammasi almashtirildi (Metricool id: changes.md 02:00 qatori). 7 Ikkinchi ovoz: R-02, R-03, R-05, R-07 da (ElevenLabs premade Jessica); komediya harakatlari (doubletake/jawdrop/sigh/deadpan/shrug) hamma yangi videolarda.
- r01v2: yuzli klip (qutini ochayotgan odam) olib tashlandi → rocco_2026-11-22_r01v2b_brushing.mp4, Buffer 6b01ff74… (Instagram Reel uchun ham shu faylni ishlating).
- QILINMADI: V-01…V-05, C-01, C-02 (slot ham yo'q, 24-noy 05:00 dan keyingi bo'sh slotlar uchun) — sabab: vaqt navbatni v6.15 da qayta yasashga ketdi; keyingi sessiya v6.15 bilan (look navbatini look_check --prev bilan tekshirib).

### ROCCO v2 — JARAYON (kod sessiyasi, 2026-11-22 02:10 Toshkent)
- rocco_voice_test.mp4 (repo ildizi) — Shohjahon tanlaydi: Rocco A/B/C/D, Penny E/F. Tanlanguncha yangi Rocco videosi CHIQMAYDI.
- Buffer: eski uslubdagi 3 Rocco posti ushlandi (r01v2b, T-04b, T-05). Instagram @redfrocco dagi eski T-04 Reel — arxivlash Shohjahon qarori (tegilmadi).
- Keyingi: Penny va Slick sprite'lari (rocco_sprites.py uslubida), dvigatelga "style": "rocco2" (yorug' fon, Lilita One, Rocco ≥1/3 kadr, suhbat), keyin RC-04 / RC-02.


## BUYURTMA 8 — LAVHA VA MAKET (2026-11-22, chat → kod; ustuvor)

Shohjahon: ovoz yaxshilandi, lekin grafika buzildi (subs_r03: yarim ekran bo'sh panel, aloqasiz xira lavha, mitti Buck).

1. `docs/footage_bank.md` + `engine/footage_bank.json` — ko'rib tanlangan 30 lavha. Bundan buyon lavha faqat bankdan yoki
   bankka qo'shilgandan keyin (prevyu ko'rilgan) olinadi. `/tmp/fin/bg/r2/river.mp4` va boshqa xira/aloqasiz kliplar ishlatilmaydi.
2. Maket qoidasi (o'sha fayl, "bo'sh panel TAQIQ"): lavha butun ekran, raqam sariq kartochkada, Buck ≥ 1/4 kadr.
   `split` ko'rinishidagi bo'sh chiziqli panel olib tashlansin; qc_gate'ga "bir rangli bo'sh maydon > 15%" = FAIL qo'shilsin.
3. Qayta render: `2026-11-24_subs_r03` (jadval faylda tayyor). Navbatdagi boshqa videolar (R-04…R-08, T-03) shu qoida bilan
   tekshirilsin; bo'sh panel yoki aloqasiz lavha bo'lsa — chiqishidan oldin qayta render, bo'lmasa o'sha video ushlab turiladi.
4. Tavsif oxiriga `Footage: Pexels — <mualliflar>`.
5. Hisobotda har video uchun 10 kadrlik varaq (`docs/looks_samples/`) — chat ko'rib tasdiqlaydi.


## KO'RIK №2 — rocco_rc04b_free_gta_pc.mp4 (2026-11-22, chat; 24 kadr bo'yicha, ovoz eshitilmagan)

Yaxshi: yorug', 3 personaj, suhbat, hazil har 3–4 s, 26 kesim, split hook, Slick yutqazadi, himoya qadami bor. Eski uslubdan ancha yuqori.
CHIQISHDAN OLDIN TUZATILSIN (4 ta qo'shimcha lavha zaif, qolgani tegilmaydi):
1. "SHADY LINK" (qorong'i ko'k xira barmoq) → `phone_scroll` (bank), qizil doira ekrandagi havola ustida.
2. "PS5 + XBOX ONLY" (ko'k shisha bino — mavzuga aloqasiz) → `gamepad_hands` (bank; logo ko'rinsa kesib olinadi).
3. "INSTALLING…?" (yashil chiziq) → `laptop_phone`; "steals your passwords" so'zida `typing_keys`.
4. "OFFICIAL STORE ONLY" (savdo markazi olomoni, xira, do'kon yozuvlari ko'rinadi) → o'z multfilm "do'kon kartasi" buyumi yoki `online_card`; yakuniy kartada ham mall o'rniga yorug' xona.
5. Rocco bir necha kadrda burchakda mitti (~1/5) — gapirayotganda ≥ 1/3 kadr.
6. Ekrandagi 'PLAYSTATION 5 / XBOX SERIES' — faqat matn (logo emas) qolsin; manba satri qo'shilsin (Take-Two press-relizi, 2026-11-20).
Tuzatilgach 10 kadrlik varaq → chat tasdiqlaydi → Buffer.


## KO'RIK №3 — b8 qayta renderlar (2026-11-22, chat; 16 kadrdan)

`2026-11-24_subs_r03_b8.mp4` — QABUL (bo'sh panel yo'q, lavhalar gapga mos, sariq kartochka, har kadrda Buck). Mayda tuzatishlar, keyingi videolarga ham:
1. Buck ~1/5 kadr va butun video bir joyda, bir o'lchamda — qoida ≥1/4; har 2–3 sahnada joy/o'lcham/harakat almashsin (reaksiyada 1/3).
2. "$13,320 / 10 YEARS" kartochkasi pult lavhasi ustida qolib ketgan — kartochka faqat o'z gapida tursin, mehmon replikasida olinadi.
3. Manba satri Buck boshi ustiga tushyapti — pastga, plashkaga.
4. Chetlardagi qorong'i vinyetka kuchli — 50% ga kamaytirilsin (kadr yorug' ko'rinsin).
5. Raqam sanab chiqish (count-up) — gap tugaguncha yakuniy songa yetib, kamida 0.8 s tursin (kadrda "$686", "$211" oraliq son ko'rinib qoldi).

`2026-11-22_gta_how_big_b8.mp4` — HALI ZAIF, shu holida boshqalarga namuna emas:
1. Buck 16 kadrdan 5 tasida — har sahnada bo'lsin (≥1/4).
2. Kartochkalar kadr chetiga tiralgan ("≈413 KM", "1.5× MOON", "3,800 T") — kenglik ≤ 80% kadr, chetdan ≥ 60 px.
3. Yo'l+osmon lavhasi 3 marta takror — "bills end to end" uchun `cash_count`/`cash_stacks`, balandlik uchun osmon 1 marta.
4. Koinot sahnalari qora — `earth_night` (quyoshli), `moon_big`; ustma-ust qorong'ilatish olinadi.
5. Ustunli diagramma xira osmon ustida — yorug' tekis lavha (`cash_desk`) ustida, ustunlar kattaroq.
Rocco: `rc04c.json` bor, video hali yo'q — render qilingach varaq bilan.

### JARAYON (vazifa sessiyasi, 2026-11-22 09:21–10:35 Toshkent, A ishi)
- START_HERE navbati 4 (yangi formatlar): V-02 (tangalar) → 23-noy 07:00 ET (YT 437269586 / IG 437269599), V-03 (kupyuralar) → 23-noy 13:00 ET (YT 437285216 / IG 437285230). Ikkalasi qc_gate PASS, v6.16, footage_bank.
- QILINMADI: V-01, V-04, V-05 (Rocco), C-01, C-02 — sabab: vaqt; V-04 manbasi (federalreserve.gov) muhitda ochilmaydi; C-01/C-02 raqamlari 23-noy fees/24-noy subs postlari bilan takrorlanadi → 25-noydan keyin. Rocco: KO'RIK №2/№3 va rc04c — kod sessiyasiniki, tegilmadi. finansist424 (UZ) — qilinmadi (vaqt).
- 10 kadrlik varaqlar: work/2026-11-23v/v02_qc_sheet.png, v03_qc_sheet.png.

### JARAYON №3 (kod sessiyasi 01MWGZtb7, 2026-11-22 03:00–11:30 Toshkent) — KO'RIK №2, BUYURTMA 8, KO'RIK №3 javobi
- KO'RIK №2 (RC-04): 1–6 bandlar bajarildi → `rocco_rc04c_free_gta_pc.mp4`, qc PASS, varaq `docs/looks_samples/rc04c_10frames.jpg`. Shohjahon oldindan ruxsat bergani uchun chat tasdig'ini kutmasdan Buffer'da RC-04b o'rniga qo'yildi (6b0252e3…, 22-noy 14:30 UTC). Chat varaqni ko'rib e'tiroz bildirsa — slotgacha almashtiriladi.
- BUYURTMA 8: 1) bank ishlatildi (muhitga videos.pexels.com qo'shildi; 32 klip /tmp/fin/bg/bank). 2) split'dagi bo'sh panel olib tashlandi; qc_gate 14_empty_panel (engine/empty_check.py). 3) navbat qayta render — natijalar changes.md 11:30 qatorida; fees_r08, subs_r03 jarayonda. 4) tavsiflarda `Footage: Pexels — …`. 5) har video uchun qc varag'i `work/2026-11-22*/…_b8_qc_sheet.png`.
- KO'RIK №3: Buck har sahnada/o'lcham-joy almashadi, kartochka ≤80%, vinyetka 50%, manba plashkada, count-up ushlab turiladi — dvigatelda.
- XATO: how_big 22-noy 05:00 da eski split holatda chiqib ketdi (worker qayta ishga tushdi). Yangi versiya `2026-11-22_gta_how_big_b8.mp4` repoda, lekin T-02 ga juda o'xshash (0.89) — qayta chiqarilmaydi.
- Bank eslatmalari (engine/footage_bank.json "note"): cash_desk tepasi bo'sh devor; cash_stacks 3–6 s qorong'i; coins_fall toza oq fon.

### JARAYON (vazifa sessiyasi, 2026-11-22 15:19–16:05 Toshkent, B ishi)
- S-13 → 23-noy 21:00 ET (YT 437456019 / IG 437456058), qc PASS, varaq work/2026-11-22t/s13_qc_sheet.png.
- R-01: KOORDINATSIYA №3 bo'yicha vazifa sessiyasiniki edi, lekin kod sessiyasi 18:40 da 2026-11-25_drawer_r01.mp4 ni yasagan — vazifa nusxasi chiqarilmadi (dublikat yo'q). Kod sessiyasi: R-01 ni Metricool'ga o'zingiz qo'ying (hali rejalashtirilmagan).
- QILINMADI (vaqt/limit): trend radari skani, raqobatchi kunlik tahlili, 3–4 yangi skill, finansist424 UZ Reel, graphify update — keyingi ishga tushishda.


## BUYURTMA 9 — ROCCO 3D MULTFILM (2026-11-22, chat → kod)
To'liq matn: `docs/rocco_3d_cast.md`. Qisqasi: buck-private/rocco_cast_v1 dagi rig qilingan Rocco/Penny/Slick'dan GPU'da sprite kutubxonasi → rc_render `style: rocco3d` → RC-04 birinchi 3D epizod → varaq chatga.

### JARAYON (vazifa sessiyasi, 2026-11-23 09:20–09:40 Toshkent, A ishi)
- ElevenLabs 200 (38,040 / 131,000 belgi ishlatilgan). Metricool getScheduledPosts: 22-noy 13:00 ET BF vs CM (437309502/437309531) ERROR "account limit"; PENDING 12 post (23-noy 07:00 nickel, 13:00 $10 bill; 24-noy 07:00 bank fees, 10:00 $100 print, 13:00 buck 1748; 25-noy 07:00 subscription, 10:00 junk drawer — YT+IG). S-13 (23-noy 21:00 ET, 437456019) ro'yxatda yo'q.
- Limit: Metricool Free — 20 chiqqan post/kalendar oy, 1-dekabrda yangilanadi → yuqoridagi 12 post ham ERROR bo'lishi kutiladi.
- QILINMADI: yangi Financier Short (A ishi) — sabab: chiqarish yo'li yo'q; Shohjahon qarori (Metricool tarifi yoki vidIQ orqali YouTube) kelgach keyingi ishga tushishda. Trend: yangi kuchli mavzu yo'q (Black Friday 27-noy, Cyber Monday 30-noy — Adobe prognozi allaqachon bankda).

## BUYURTMA 10 — YOUTUBE vidIQ ORQALI (Shohjahon 2026-11-23 ~09:45 Toshkent: "vidIQ orqali chiqarishga ruxsat beraman") — HOLAT: OCHIQ
Sabab: Metricool Free limiti (20 chiqqan post/oy) tugagan, 1-dekabrgacha Metricool orqali hech narsa chiqmaydi. Financier YouTube endi vidIQ (vidiq_social_post_*; kanal UC3URYtuy-f6c1fTNhesFkGA, canPublish true) orqali.
Metricool'dagi 7 ta PENDING YT posti vidIQ qoralamasiga ko'chirildi (o'sha video — Metricool static URL'dan vidiq_video_upload; o'sha sarlavha, matn, teglar, vaqt; public):
| slot ET | video | vidIQ postId | publicationId |
|---|---|---|---|
| 23-noy 07:00 | A Nickel Costs 13.78 Cents | af1640a1-721c-43da-bd58-41d0e822885c | 5dff7d62-8172-4f28-a77b-6aaaffb019cc (1-urinish FAILED: uploadLimitExceeded) |
| 23-noy 13:00 | The $10 Bill Dies First | d6ad3635-85c5-421b-8873-266b5bc4c432 (rev 2ed44b4a) | d358b6aa-2f38-4cb4-94ec-c29f3aa8ea74 |
| 24-noy 07:00 | Bank Charged Me $4.86 | 945db7c1-aa71-4b9c-ae7c-f6dece740f5b (rev a4d7050a) | f429ef7b-77fb-415e-b028-cfb7c1f6bf2e |
| 24-noy 10:00 | 11.3 Cents to Print a $100 | f075a22f-0d5d-43a1-8865-ea4ae41eac0e (rev 1c453622) | aa719985-fdd6-455e-bb9b-b762e00a97e0 |
| 24-noy 13:00 | 1748: Why Dollar Is a Buck | 5d2ea26c-315b-4f37-bb38-5f796363fc17 (rev 7cbc1955) | b1c7e693-9c7b-4cf7-bb91-708226ed577b |
| 25-noy 07:00 | Cancel a $21 Subscription | 1869da50-fb52-4b27-a1ae-cb5df2197fe8 (rev 17eb49f5) | 7d743d2a-8c46-4b7a-8291-68bfc2cda246 |
| 25-noy 10:00 | $27 Billion in Junk Drawers | b32ab8ad-3c8c-4a16-8542-085e3b46e644 (rev 374c1770) | 342a17a7-2e52-4944-bb9d-d19ddf2cff27 |
MUAMMO: 1-publish "YouTube's daily upload limit for this channel was reached (uploadLimitExceeded)" — YouTube API kunlik yuklash limiti (taxminan Tinch okeani vaqti yarim tunida, ~08:00 UTC yangilanadi). Rejalashtirilgan video ham YUKLANGAN paytda limitni sarflaydi.
KEYINGI ISHGA TUSHISHDA (≥08:00 UTC): vidiq_social_post_publish — avval nickel (postId af1640a1…, publicationIds [5dff7d62…], 07:00 ET slot o'tib ketgan bo'lsa draft_update bilan eng yaqin bo'sh vaqtga), keyin 23-noy 13:00, so'ng qolganlari vaqt tartibida; har biridan keyin vidiq_social_post_status. Limitga yana ursa — to'xta, qolganini keyingi kunga. Kuniga ko'pi bilan ~3–4 yuklash deb reja qil.
INSTAGRAM financier424: vidiq_social_post IG uchun AI belgisi yo'q → IG Reel'lar vidiq_instagram_publish_reel (isAiGenerated true) bilan slot vaqtida qo'lda chiqariladi (Metricool IG postlari ham ERROR bo'ladi).
Metricool'dagi eski 12 PENDING post o'chirilmadi (oy limiti tufayli baribir ERROR bo'ladi, 1-dekabrdan oldingi sanalar).
- 2026-11-23 ~09:55 Toshkent, Shohjahon: "Metricool'dagi hammasini vidIQ ga o'tkazib, vidIQ da ishla bundan keyin". 7 ta YT qoralamasi + 7 ta IG captioni (Metricool'dagi IG matnlari) `work/vidiq_migration/queue_2026-11-23.json` da — har ishga tushishda shu navbatni bajar va yt_status/ig_status ni yangilab push qil. producer_task, run_checklist, START_HERE, instagram.md ga "POST FAQAT vidIQ ORQALI" qo'shildi. Metricool'dagi eski PENDING postlar o'chirilmadi (oy limiti tufayli ERROR bo'ladi; Metricool MCP'da o'chirish vositasi yo'q).

- 2026-11-23 10:20 UTC (vazifa): nickel YT 3-urinish yana uploadLimitExceeded. SABAB ANIQLANDI: vidiq_social_post_list — 23-noy 01:17–01:18 UTC da Financier kanaliga vidIQ orqali 10 ta video ketma-ket yuklangan (9 completed, 1 failed "final penny"); YouTube limiti shu yuklashlar bilan to'lgan va oyna 24 soatlik bo'lsa ~24-noy 01:20 UTC (06:20 Toshkent) da ochiladi. KEYINGI URINISH: ≥24-noy 01:30 UTC, avval nickel, keyin ten_bill; kuniga ko'pi bilan 3–4; bir vaqtda ketma-ket 10 ta YUKLAMA. IG nickel chiqdi: https://www.instagram.com/reel/DgFJuwHAOMh/
