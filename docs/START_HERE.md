# SHU YERDAN BOSHLA — kod chati / vazifa uchun yagona tartib (chat Trade, 2026-11-21 22:10 Toshkent)
> **2026-11-22: LAVHA + MAKET** — lavha faqat `docs/footage_bank.md` dan; bo'sh panel taqiq; Buck ≥ 1/4 kadr. Buyurtma 8 (`docs/night_order.md`).
Shohjahon: "hammasi tayyor bo'lsa kodni ishga tushiraman". Bu fayl boshqa hamma hujjatdan OLDIN o'qiladi; ziddiyat bo'lsa — bu fayl va unda ko'rsatilgan yangi hujjatlar ustun (producer_task va sprint_10d dagi eski andoza bandlaridan).

## 0. Har ishga tushishda
**Avval `docs/run_checklist.md` (2026-11-22) — boshida va oxirida, bandma-band.**
`git pull --rebase origin media` → docs/changes.md oxirgi 20 qator → docs/night_order.md (BUYURTMA 6, 7 va ularning tuzatishlari) → docs/skills/INDEX.md.

## 0.5 ROCCO: eski uslub TO'XTATILDI — docs/rocco_style_v2.md (yorug' fon, Rocco + Penny suhbati, hazil, yangi ovoz tanlovi). Ovoz tanlanguncha yangi Rocco videosi chiqmaydi; birinchi ish — rocco_voice_test.mp4.

## 1. NAVBAT (qat'iy shu tartibda)
1. ROCCO r01: Buffer postini ushla (6b01befd142c957519268046) — eski ko'rinishda chiqmasin; yangi qoidada qayta yasa.
2. TREND: script_bank T-02 → T-01 (Financier, 22-noy 02:00 va 05:00 Toshkent slotlari; u yerdagi eski postlar suriladi), T-04 (Rocco). Muddat 23-noy 15:00 UTC. Dvigatel yangiligi ulgurmasa — mavjud dvigatelda, lekin yangi ssenariy + yorqin to'liq ekranli lavha bilan chiqar.
3. DVIGATEL minimal to'plami: (a) "shots" — har ≤2 s yangi tasvir; (b) 1–3 so'zli sinxron subtitr, doimiy sarlavhasiz rejim; (c) look "fullbleed"; (d) "paper", "split"; (e) ikkinchi ovoz ("voices"). Har biri tayyor bo'lganda ENGINE_VERSION + changes.md + push.
4. YANGI FORMATLAR: V-01…V-05, C-01, C-02; sanaga bog'liq R-05 (Black Friday, 27-noyabrgacha).
5. QAYTA YASASH: R-01…R-08 (Metricool id lari night_order BUYURTMA 7 da). Eski shablondagi post slotiga yangi versiya ulgurmasa — post suriladi, o'chirilmaydi.
Hajm: kuniga 8 Short (Financier) + Rocco kuniga 1–2; aralashma script_rules v2.2.

## 2. HAR VIDEO UCHUN MAJBURIY (bittasi yo'q bo'lsa — chiqmaydi)
| Nima | Qayerda | Tekshiruv |
|---|---|---|
| Tuzilma (9 tadan biri), javob oxirida, skelet takrori yo'q | docs/script_rules.md | engine/script_check.py PASS |
| Ko'rinish (look), oxirgi 4 videoga <0.70 o'xshash | docs/looks.md | engine/look_check.py / qc_gate 10-qadam |
| Lavha ≥40% sahna, gapga mos, yorqin, 4 yo'ldan ≥3 tasi; odatiy kiyimdagi odamlar mumkin, behayo kiyim yo'q | producer_task "g", "LAVHA TANLASHDA KENG O'YLASH", "LAVHADA ODAMLAR" | script_check + kadrlarni ko'z bilan ko'rish |
| Kadr tempi: 30 s ≥15 kadr, 60 s ≥30 | docs/lessons_winners_2026-11-21.md | kontakt-varaq sanog'i |
| Subtitr 1–3 so'z; 1-kadrda to'liq hook yozuvi | o'sha | kontakt-varaq |
| Hazil: ko'rinadigan gag ≥1, reaksiya harakati (doubletake / jawdrop / shrug / sigh / deadpan), fakt videosida har 8–10 s da kulgili gap | docs/comedy.md | playbook yozuvida "hazillar soni" |
| Fakt: manba + sana; o'z hisob — "our math"; bahsli — "probably / popular theory"; prognoz — "forecast" | producer_task QAT'IY CHEGARALAR | render oldidan manbani qayta ochish |
| Ovoz: ASR tekshiruv, prosody, −14 LUFS | INDEX | qc_gate |
| Sarlavha, tavsif, teglar | INDEX (title.py, yt-seo) | title.py balli |
| "Skillar: … ; ishlatilmadi: … (sababi)" qatori | INDEX | yo'q bo'lsa qc FAIL |
QAT'IY CHEGARALAR o'zgarmagan: behayo/noqonuniy narsa yo'q, musiqa yo'q, logotip/brend/film/o'yin kadri yo'q, real shaxs yo'q, moliyaviy maslahat yo'q, sotib olingan ko'rish/obunachi yo'q.

- INSTAGRAM TRIAL REELS: docs/instagram.md "TRIAL REELS" — obunachi soni yetgan kundan boshlab ruxsat etilgan maksimumgacha (5 → 10 → 15 → 20/kun), har biri boshqa video; har kuni imkoniyat ochilganini tekshir.

- ETALON KARTASI (2026-11-22, Shohjahon: "nega yana yomon kontent?"): HAR yangi video uchun playbook yozuvida — qaysi PORTLAGAN videoga qiyoslab yasaldi (havola), va 5 o'lchov bo'yicha solishtiruv: hook turi, hazillar soni, yorqinlik, personaj kadr ulushi, kesim tempi. Etalondan aniq past bo'lsa — video CHIQMAYDI, qayta yasaladi. Rocco: docs/rocco_style_v2.md (formula + RC-01…RC-04).

## 3. HISOBOT
Har tugagan ishdan keyin: changes.md ga qator + push. Birinchi 3 ta yangi videodan 10 kadrlik kontakt-varaq → docs/looks_samples/. Qilinmagan har narsa: "QILINMADI: sababi, qachon" — night_order ga. "Bilmadim / esimdan chiqdi" yozilmaydi — shu fayl va INDEX buning uchun.

## 4. NIMA TAYYOR, NIMA YO'Q (2026-11-21 22:10)
TAYYOR: qoidalar (script_rules v2.2, looks, comedy, lessons), 20 ssenariy (T-01…05, V-01…05, C-01…02, R-01…08), tekshiruvchilar (look_check, script_check; look_check qc_gate ga ulangan), dvigatel v6.13 (5 komediya harakati), Rocco sprite'lari (845 kadr), Buck harakatlari (assets/buck3d_v3_acts.tar — push qilinadi), vidIQ Pro (2 500 kredit).
YO'Q (kod qiladi): dvigatelda shots / 1–3 so'zli subtitr / fullbleed-paper-split looklar / ikkinchi ovoz; script_check ni qc_gate ga ulash; videolarning o'zi.

## 5. YANGI (vazifa sessiyasi, 2026-11-22 01:00 Toshkent) — boshqa chatlar o'qisin
- `docs/run_checklist.md` — har ishga tushishda boshida/oxirida (post o'chirishdan oldin matnni solishtirish, claude/* branchlarni tekshirish).
- `docs/instagram_redfrocco.md` + `assets/instagram/redfrocco/` — Rocco Instagram'i: avatar, ism, bio, 3 post, 4 highlight, Reel captionlar. Joylash uchun redfrocco OAuth ulanishi kerak (hozir manual).
- graphify ishlaydi (ruxsat `.claude/settings.json` da).
- Kunlik natijalar: `docs/results.md` (21-noy 18:40 UTC), trend: `docs/trend_radar.md`, `docs/daily_trends.md`; bank S-13, S-14.
