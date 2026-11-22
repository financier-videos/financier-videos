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

| 2026-11-22 | `oiMsxtYm5SI` | explicable TV — 634K, 543x | Rocco (3D) | animatsion "wrong number trap" | dramatik ironiya: tomoshabin 1-kadrdan firibgar politsiyaga qo'ng'iroq qilayotganini biladi; firibgar skriptini to'liq o'qiydi (OTP, 30 s, "jim gapiring"); burilish 1:00 da; firibgar "tarmoq yomon" → absurd chekinish ("Jesus loves you") — eng ko'p ulashilgan lahza |
| 2026-11-22 | `s-nyFs1118A` | NAVYA — 2M, 1509x | Rocco (3D) | animatsion "ego trap" | firibgar qurbonni kamsitadi ("bu sen uchun emas") → qurbon g'ururi uchun 20x qimmatga sotib oladi; har savdolashuvga yangi kamsitish; 0 kesim, faqat aktyorlik; yakun — firibgarlar kuladi |
| 2026-11-22 | `2IFK69bB4CE` | Zovi — 491K, 239x (3D, AI-labeled) | Rocco | firibgarlik = ertak (pump&dump shishalar) | narx sikli $20→$50→$300 montaj 0.8 s; raqamdan oldin mikro-pauza; oxirida 4-devorni buzish "Remember the stock market? Same story."; tun/bo'sh ko'cha + faqat shamol sukunati |
| 2026-11-22 | `DfC5DUuTroA` | IG @apextoon_usa14 — 50.2M, 178x (3D) | Rocco | kichkina-yoqimli vs ulkan-xavfli slapstick | 0-soniyada harakat boshlangan; masshtab kontrasti; ~28 kesim/46 s; makro DoF; ovozsiz ham tushunarli |
| 2026-11-22 | `pipandrue` (TikTok 7699859376038743304) | 6.7M, 14x (3D skit) | Rocco | 3 qahramon dialog, ikki burilish + tag | birinchi so'z 0.65 s; zarba setupdan 100–150 ms keyin; dahshatli satrdan oldin 0.4 s pauza; past rakurs + ECU mikro-zum; 'She's not dead.' tag |
| 2026-11-22 | `N09VNM2BOD8` | 5.0M, 21x | Rocco | harflab aytilgan tuzoq qo'ng'iroq | qurbon ma'lumotni harfma-harf aytadi → yozilgani haqorat; trubka tovushi + loop |
| 2026-11-22 | `Dcy3hSMxYop` | IG 2.2M, 174x | Rocco | SCAM LIKELY qo'ng'iroq, tekis personaj realistik xonada | '***PHONE'S RINGING***' caption 0-s |
| 2026-11-22 | `DdGowjqMDqS` | IG 13.4M, 412x | Rocco | 14 s ovozsiz karma allegoriyasi | tepada 3 qatorli she'r; 14 s; sukut + SFX |
| 2026-11-22 | `jUF_JPKXTWc` | 7.5M | Rocco | 2 tasi scam, 1 tasi real | har 12–15 s yangi holat; qizil strelka; yashil flesh |
| 2026-11-22 | `DeZc6g0uaBv` | IG 2.1M, 7.5x | Rocco | ovozsiz soxta o'yin, 2 marta fosh | foley; ALL OR NOTHING |
| 2026-11-22 | `SS_6KU9qpr0` | 20.3M, 9.9x | Rocco | RED FLAG or GREEN FLAG panel | 02:00 taymer; har 8 s savol |
| 2026-11-22 | `PibMox6nk4c` | 66.8K, 17x | Rocco | yechilmagan sir — izohlar yechadi | 'only a real detective can solve this' |
| 2026-11-22 | `Df331TOAaAO` | IG 2.1M, 9x | Rocco | POV fishing click-through | so'nggi sahifa masxara |
| 2026-11-22 | `DfSbqCJPpE8` | IG 1.1M, 54.8x | Rocco | yashirin shaxs status flip | sahna o'rtasidan boshlanadi |
| 2026-11-22 | `DflN4MGBPX5` | IG 168.9K, 93x | Rocco | 'did you order this?' ikki kishilik | QR karta; 'Well… free shirt' |
| 2026-11-22 | `4ILxskhpnpo` | 602K, 481x | Rocco | 'This just happened to…' ogohlantirish | qizil ramka sarlavha + skrinshot + 3 qoida |
| 2026-11-22 | `EpTFo_wkNwA` | 3.3M, 39x | Buck | jismoniy ko'lam (kichik taxlam → devor) | 'This little stack is…' keng ochilish |
| 2026-11-22 | `siIMLJRNM0c` | 3.7M, 56x | Buck | 'qancha vaqtda bankrot bo'ladi?' | imkonsiz javob (ming yillar) |
| 2026-11-22 | `e6XktxbqN00` | 1.7M, 15x | Buck | eski chek vs bugungi narx | item-by-item stikerlar + total |
| 2026-11-22 | `8yUm4dyVXuE` | 1.5M, 41x | Buck | 10 mamlakatda bir xil narsa | raqamli kartalar, izohga savol |
| 2026-11-22 | `R2qQD6IcN2w` | 155.8K, 216x | Buck | narxni top | 11–17 s, slayder |
| 2026-11-22 | `YmPcakD7FcI` | 7.7M, 36x | Buck | yasash narxi | taxmin → tannarx kartasi |
| 2026-11-22 | `mofrqidM4Mo` | 408K, 192x | Buck | jonli to'ladigan reyting jadvali | har 2–3 s qator; oxiri ??? |

## Keyingi video g'oyalari (yangi formatlar — hali ishlatilmagan)
- **Rocco "Penny plays dumb"** (vcPnUMJNdkw formati): Slick "bank xodimi" bo'lib qo'ng'iroq qiladi; Penny Rocco maslahati bilan ataylab so'zma-so'z javob beradi (kod? → "1, 2, 3, 4..."), Slick asabiylashadi, oxiri absurd ("I'm a piggy bank, I don't HAVE a card"). Yakunda Rocco: "Real banks never ask for your code."
- **Rocco "Free gift at the door"** (uaV36whB6H8): "tekin sovg'a" kuryeri → QR/"kodni ayting" → balans 0 SMS. Mavzu: tekin sovg'a/sovg'a kartasi firibgarligi (Black Friday mavsumi).
- **Financier "Why is Dracula rich?"** (8Sp2jBDdTDM; Drakula — jamoat mulki): 3 ustun, eng kuchli lahza "xarajat = $0" (qon tekin, xizmatkor maosh olmaydi) → saboq: daromad − xarajat. Buck hisob kartasi bilan.
- **Financier "Money stats that sound fake"** (ftA18KGBrwM): 5–7 fakt kichikdan kattaga (millionda 11 kun vs milliardda 31.7 yil soniya; ...), har biri 4 s, sariq kartochka; "Part 2" bilan seriya.
