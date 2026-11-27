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
| 2026-11-27 | `bwwmalsQUZM` | Montra Explains — 625 obun. → 68.6K (51 s, 24-noy) | Financier | mexanizm-tushuntirish 'How does X work?' | savol-sarlavha + bitta oddiy mexanizm; KICHIK KANAL breakout (U-5 manbasi bilan bir oila) |
| 2026-11-27 | `xpSVELloBYc` | lifemem — 7.9K obun. → 163K (6 s, 24-noy) | Rocco/Financier | mikro-skit 6 s: ilova narxi vs haqiqiy narx | bitta zarba, darhol loop; 'app price' mavzusi (dinamik narx) |
| 2026-11-27 | `qh-n-KXM6XU` | Yonside — 259K → 5.3K/15 soat, ER 20% (68 s) | Financier | 'Black Friday then vs now' sketch | then/now ikki qism, ER juda yuqori — vaqt mashinasi formati (d) uchun dalil |
| 2026-11-27 | `aFXIynmjweI` | FANG — 30K → 173K (63 s, 26-noy) | Rocco | firibgarlik hikoyasi + adolat burilishi | 'Scammers took her money, so she…' — status inversiyasi sarlavhada |
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

## 2026-11-25 skan (to'liq tahlil: docs/growth_research_2026-11-25.md)
| Sana | Video ID | Kanal / natija | Kanalimiz | Format | Nega ishlaydi / olish kerak bo'lgan lahza |
|---|---|---|---|---|---|
| 2026-11-25 | `Ml36RBLHWZY` | MrWhy (178 obun.) — 22.4K, 6.5x, 1:04 | Buck | "1 cent every second" vaqt zinapoyasi | sek→daq→kun→yil→umr→Rim 753 BC; 0:04 teaser "3,000 years" 0:44 da to'lanadi; gapma-gap seamless loop (B1) |
| 2026-11-25 | `kI-UC7vuMlc` | Old School Animate (32 obun.) — 20.5K, 15x, 0:49 | Buck | "Every word costs $1" qoida-sketch | boshi ustida balans yorlig'i, chek/muhr har sahnada, 16,000 so'z/kun fakti, beixtiyor "ouch" punchline (B2) |
| 2026-11-25 | `I4TJOP7M04U` | Retroyap (76.5K) — 9.3M, 67x, 2:03 | Buck | "$X but catch" rejalar zinapoyasi | 3 reja tobora kattaroq, har birida raqam/vaqt, ekzistensial burilish; piksel shrift (B3) |
| 2026-11-25 | `F01I1GMwFuM` | Quiet Panther (3.4K) — 132.9K, 42x, 1:45 | Buck | jazavali xaridor vs xotirjam mentor | qizil taymer hook, kontrar "no such thing as Black Friday", 3 sepia flashback, atama "artificial urgency" (B4) |
| 2026-11-25 | `ikuRVdAAue8` | Income Infinity (394K) — 2.5M, 35x, 2:59 | Buck | x1000 katta sonlar zinapoyasi | real boylikdan boshlab har pog'ona x1000 + jismoniy anchor + sanash vaqti (B5) |
| 2026-11-25 | `AWlZMV7M5Wk` | TD3 Studios (33.5K) — 623K 1 kunda, 2:07 | Buck | "Guess the Number: 8 Billion" | dramatik ironiya: tomoshabin raqamni ko'radi, o'yinchi yo'q; qizil X / yashil ✓; doimiy banner (B6) |
| 2026-11-25 | `qO2i4AH_84s` | MrGee Math (202K) — 328K 1 kunda, 1:12 | Buck | "scam your friends" tanga tikishi (Penney's game) | "you go first" hook → 7/8 ehtimol → formula → yarim loop (B7, Buck=tanga) |
| 2026-11-25 | `uQ0-eq5GpMk` | Zeyfra (2.1K) — 30.7K, 17x, 0:40 | Buck | "billionaires called X an idiot" 2D komiks | ziddiyatli hook + "yaxshi billioner" burilishi; real yuz — biz silueta bilan |
| 2026-11-25 | `Air9U8z3D_A` | ChatigerWorld (2.7K) — 25.5K, 14x, 0:27 | Rocco | 2FA kod paranoyasi dialogi | 10 kadr shot-reverse-shot, aylana mantiq "That's what made it suspicious", deadpan yakun (RC-A) |
| 2026-11-25 | `VSQm4NhTAyc` | Hannah Kim (405K) — 321K, 45x, 1:02 | Rocco | "POV: tried to scam … but good deed" | doimiy POV banner; tizim qoidasi (refund asl kartaga) firibgarni teskari uradi (RC-B) |
| 2026-11-25 | `eyM-37VuERA` | All In Camera (41.1K) — 6.3M, 185x, 0:20 | Rocco | Marketplace bitta detal gag | 0 kesim, qizil banner, absurd model detali, gap o'rtasida kesish → qayta ko'rish (RC-C) |
| 2026-11-25 | `JUAm6j5YBEE` | Sarthak Paraye (140 obun.) — 22K, 44x, 1:45 | Rocco | "sen mastermind" tarixiy firibgarlik (Salad Oil 1963) | arzon narsa → ulkan summa hook, STEP 1..5, 99% suv/1% moy oddiy fizika (RC-D) |
| 2026-11-25 | `tEkYMu_8hi8` | HELLOG (59.6K) — 1.4M, 28x, 2:41 | Rocco | romance scam dramatik ironiya hikoyasi | 5-s da tomoshabin firibgarni biladi; "boss" qo'llanmasi; 2 tuzoq; burilish (RC-E, zo'ravonliksiz) |
| 2026-11-25 | `zWcZP5YcO8s` | Yah Bak (37.2K) — 1.72M, 3:00 | Rocco | "$2M in 10 minutes?" stavka zinapoyasi | doimiy savol-banner; $1K→$100K; ataylab yutqazish; priming sir ochilishi (RC-F; film klipi — faqat struktura) |
| 2026-11-25 | `u8woqMLoZ80` | Costello Cards (124K) — 565K, 20x, 1:07 | Rocco | sotuvchi POV "This clown is a scammer" | real vendor lavhasi — faqat mavzu signali (kolleksiya/soxta kartochka) |
| 2026-11-25 | `vcPnUMJNdkw` | KarolkaShow (191K) — 6.06M (49K vph), 1:37 | Rocco | ataylab ahmoq bo'lish (qayta o'lchov) | 22-noydagi 2.1M → 6.06M: format hali o'sishda; Penny Plays Dumb (1,298) davom |

## 2026-11-25 sekundma-sekund beat map (to'liq: docs/viral_beatmap_2026-11-25.md)
| Sana | Video ID | Kanal / natija | Kanalimiz | Format | Olish kerak bo'lgan lahza (struktura/vaqt) |
|---|---|---|---|---|---|
| 2026-11-25 | `NeI6GU94Hc4` | Competent Cat (232) — 33.2K, 19x, 0:56 | Buck | "penny every time X" gipoteza, 2D mushuk | 1 tanga (3 s) → banka → shkaf → uy (5–9 s) → shahar (14 s) uzluksiz vizual eskalatsiya; "lekin muammo" 2-akt (37 s); fakt-punchline yakun; 3.6 so'z/s, kesim 2.6 s |
| 2026-11-25 | `MI-qVW1IKdU` | GD University (3.3K) — 48K, 1.5K vph, 1:28 | Buck | "$1B + catch" vaqt-lapse | shart (SIGNED kontrakt) 5–6 s da to'liq; kun → oy → yil kalendar; 1-kadrga vizual qaytish |
| 2026-11-25 | `PqYXJ2pUr3w` | Money Math Club (8.1K) — 410K, 140x, 1:01 (Hindi) | Buck | bir xil maosh, ikki odam: qizil/yashil split | doimiy split banner + har 5–7 s ikonka-juftlik (A qiladi → B javob); 0 kesim |
| 2026-11-25 | `nF0HwqRtdXM` | Nigel Green (218K) — 26K, 14x, 0:26 | Buck | daromad qatori, ko'rinish vs raqam | yorliqlar $0K→$2M 0–6 s; eng katta raqam oddiy odamda (6 s) |
| 2026-11-25 | `pnQ5QDxYng0` | TrayFromOhio (5.6K) — 16.4K, 6.1x, 0:44 | Rocco | soxta "mashhur boy" firibgar qo'ng'irog'i do'konda | talab 3 s da; har ~10 s talab ortadi (karta → katta karta → SSN); zum + bass har zarbada; guvoh tasdig'i yakun |
| 2026-11-25 | `3LsXHwMM9bM` | Big Duke13 (373K) — 88.6K, 8.5x, 2:34 | Rocco | haqiqiy firibgarlik hikoyasi, gapiruvchi bosh | sarlavhada raqam ("8 marta") + mexanizm burilishi (qayta o'g'irlash) 27–51 s; moral oxiri — biz uchun emas |
| 2026-11-25 | `u7q17wGWxvM` | Mr Giggles (10K) — 9.4K/1 kun, 13% eng., 2:15 | Rocco | firibgarga 14 xil absurd ovoz | premisa 4 s; har 5–15 s yangi "personaj javobi" katalogi; musiqasiz |
| 2026-11-25 | `iJQLhLuWvlk` | Cyber Detectives (15.5K) — 10.7K, 4x, 0:56 (Hindi) | Rocco | telefon so'rash skiti + sozlama | firibgar o'z tuzog'iga tushib qochadi (38 s) — kech; moral+CTA = eng past breakout |
| 2026-11-25 | `Ml36RBLHWZY` | qayta o'lchov (beat map) | Buck | vaqt zinapoyasi | teaser 3 s → raqam 6 s → konfet anchor 9 s; 2.8 so'z/s, kesim 3.9 s; loop |
| 2026-11-25 | `kI-UC7vuMlc` | qayta o'lchov | Buck | qoida-sketch | balans yorlig'i 3–4 s; SKIPPED muhri ~6 s; har 4–6 s mikro-sahna + muhr |
| 2026-11-25 | `Air9U8z3D_A` | qayta o'lchov | Rocco | absurd xavfsizlik dialogi | rad 3 s, kulgi 8 s; ≤6 so'z replika; 3.2 so'z/s; musiqasiz |
| 2026-11-25 | `VSQm4NhTAyc` | qayta o'lchov — 335K, 45x | Rocco | POV, tizim qoidasi teskari uradi | doimiy banner NATIJANI aytadi (dramatik ironiya); to'lov 48 s; 0 kesim |
| 2026-11-25 | `vcPnUMJNdkw` | qayta o'lchov — 6.1M, 48x, 70K vph | Rocco | ataylab ahmoq bo'lish | firibgar talabi+stavka 9 s gacha; firibgar o'zi absurd 3–5 s; doimiy banner; har 6–10 s zarba |
| 2026-11-25 | `AWlZMV7M5Wk` | qayta o'lchov — 709K, 22K vph | Buck | guess the number | javob butun video ekranda; birinchi javob 3 s; qizil X / yashil 👍; 3–3.8 so'z/s |
