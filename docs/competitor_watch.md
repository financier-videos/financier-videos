# RAQOBATCHI KUZATUVI (competitor watch) — har yangi videodan OLDIN

Shohjahon (2026-11-22): "Eng asosiysi har safar yangi va portlatadigan videolar qilish kerak. Konkurentlarni o'rganib turish kerak."

## Qoida (qc_gate 15_competitors bilan majburiy)
1. Har yangi video spec'ida `"benchmarks": ["<videoId> — nimani oldik", ...]` — kamida **2 ta** video ID, ular quyidagi jurnalda **oxirgi 7 kun** ichida tahlil qilingan bo'lishi shart. Yo'q bo'lsa qc_gate FAIL.
2. Jurnal 7 kundan eski bo'lsa: avval yangi skan (pastdagi tartib), keyin video.
3. Har video kamida **1 ta yangi usul** olishi kerak (oldingi 5 videoda ishlatilmagan lahza/format) — spec "benchmarks" ichida "YANGI:" deb belgilanadi.
4. Format olinadi, mazmun/kadr/matn ko'chirilmaydi; real shaxs, brend, film/o'yin kadri yo'q (QAT'IY CHEGARALAR). Fictional personaj — faqat jamoat mulki (Drakula, Midas, Robin Gud), Disney/Marvel kabi emas.

## Skan tartibi (har kuni avtomatik + video oldidan qo'lda)
- `vidiq_outliers` contentType=short, publishedWithin=thisMonth (yangi bo'lsa thisWeek), minEngagementRate=0.02, limit 15:
  - Rocco: "scam warning skit, scammer gets outsmarted", "scam explained animation", "phone scam call prank", "fake payment app scam".
  - Financier: "surprising money facts explained", "how much money is a billion", "money statistics that sound fake", "price comparison facts".
- Eng yangi va eng tez o'sayotgan (views/hour, breakout ≥5x) 2–4 tasini `vidiq_watch_shortform_content` bilan kadrma-kadr tahlil qilish.
- Natija: pastdagi jurnalga qator + "Keyingi video g'oyalari" ga format; eng kuchli lahzalar `docs/rocco_winner_moments.md` ga.

## Jurnal
| Sana | Video ID | Kanal / natija | Kanalimiz | Format | Olish kerak bo'lgan lahza |
|---|---|---|---|---|---|
| 2026-11-22 | `6agufKA2ZQY` | Noah Kettle Shorts — 2.2M, 303x | Rocco | mutaxassis to'xtatadi + bashorat | "Wait! Don't do anything" → bashorat → xabar aynan shu payt keladi; −$1,000 ikki karra zarar hisobi |
| 2026-11-22 | `N09VNM2BOD8` | 4.9M, 21x | Rocco | firibgar bilan qo'ng'iroq skiti | absurd ism ochilishi + deadpan javob; firibgar tili qoqiladi; 2 zarbali yakun + trubka beep |
| 2026-11-22 | `JMI-iIpHdt8` | Richard animations — 588K, 27x | Rocco | animatsion: firibgar noto'g'ri odamga qo'ng'iroq qiladi | ikki joy almashib; firibgar kulgi obyekti |
| 2026-11-22 | `ZmaE7zI3fmY` | 7x | Rocco | real lavha + qizil doira | split hook, mexanizm lavhada doira bilan |
| 2026-11-22 | `vcPnUMJNdkw` | KarolkaShow — 2.1M, 8x, 1 kunda (42K/soat) | Rocco | "Playing DUMB with a scammer" | qurbon ATAYLAB ahmoq bo'ladi: so'zma-so'z javob ("karta raqami?" → "16"), raqamlarni 1,2,3 deb sanaydi, firibgar tahdidini aks-sado qiladi, absurd yakun ("I identify as a fish"); har 10 s da bitta zarba; tepada doimiy yozuv "Playing DUMB with a SCAMMER" |
| 2026-11-22 | `uaV36whB6H8` | Tech wallah Aryan — 1.3M, 18x | Rocco | politsiyachi + oddiy odam skiti, "tekin" tuzoq | eshik taqillashi hook; "tekin narsa" → biometrik/ID → SMS: balans 0 (qizil); "Free?!" reaksiyasi; har 1.5–2.5 s kesim |
| 2026-11-22 | `8Sp2jBDdTDM` | McDonald Ed — 494K, 26x | Financier | "X ishlamaydi, nega boy?" paradoks hikoyasi | paradoks hook 0–3 s; 3 ustun: aktiv daromad → XARAJAT NOL (eng kuchli lahza) → boshqaruvchi; so'z-so'z yashil ajratish |
| 2026-11-22 | `ftA18KGBrwM` | hxsain — 3.2M, 4.5x | Financier | "Sound fake but 100% real" ro'yxat | 7 fakt, har biri 3–6 s, kichikdan → kosmik miqyosga; xarita/miqyos taqqoslash izoh uyg'otadi; "Part 2" CTA |

## Keyingi video g'oyalari (yangi formatlar — hali ishlatilmagan)
- **Rocco "Penny plays dumb"** (vcPnUMJNdkw formati): Slick "bank xodimi" bo'lib qo'ng'iroq qiladi; Penny Rocco maslahati bilan ataylab so'zma-so'z javob beradi (kod? → "1, 2, 3, 4..."), Slick asabiylashadi, oxiri absurd ("I'm a piggy bank, I don't HAVE a card"). Yakunda Rocco: "Real banks never ask for your code."
- **Rocco "Free gift at the door"** (uaV36whB6H8): "tekin sovg'a" kuryeri → QR/"kodni ayting" → balans 0 SMS. Mavzu: tekin sovg'a/sovg'a kartasi firibgarligi (Black Friday mavsumi).
- **Financier "Why is Dracula rich?"** (8Sp2jBDdTDM; Drakula — jamoat mulki): 3 ustun, eng kuchli lahza "xarajat = $0" (qon tekin, xizmatkor maosh olmaydi) → saboq: daromad − xarajat. Buck hisob kartasi bilan.
- **Financier "Money stats that sound fake"** (ftA18KGBrwM): 5–7 fakt kichikdan kattaga (millionda 11 kun vs milliardda 31.7 yil soniya; ...), har biri 4 s, sariq kartochka; "Part 2" bilan seriya.
