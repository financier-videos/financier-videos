# VIZUAL HOOK — qoida, dalil, tekshiruv (chat Trade, 2026-11-27)

Shohjahon: "Vizual hook degan narsani o'rgan va videolarda qo'lla."

## 1. Nima bu
Vizual hook — tomoshabin ovozni eshitmasdan, yozuvni o'qimasdan OLDIN ko'radigan narsa: birinchi kadr va birinchi 1 soniyadagi harakat.
Ko'z rasmni matndan tezroq ushlaydi; Shorts lentasida qaror ~1 soniyada qabul qilinadi, shuning uchun birinchi kadr "sarlavha foni" emas, o'zi dalil bo'lishi kerak.
Hook = 3 qatlam, uchalasi BIR narsani aytadi: (1) rasm, (2) ekrandagi 3–7 so'z, (3) birinchi aytilgan gap. Bizda shu paytgacha faqat (2) va (3) ishlagan.

## 2. Dalil — 3 ta portlagan video, birinchi 3 soniya (vidIQ kadrma-kadr, 2026-11-27)
| Video | Natija | 1-kadrda nima | Qachon voqea | Savol |
|---|---|---|---|---|
| IdSsAquESBE "How Money Gets Cleaned" (8.5K obunachi kanal) | 2.1M, 18x | 3D personaj stoldagi och-ko'k sumkani OCHAYOTGAN payt (harakat boshlangan), g'ayrioddiy buyum | 1-soniyada ichidan pul chiqadi | "sumkada nima?" — 1–3 s da javob, keyin yangi savol |
| hIlWYivYlSM "Everyone Is a Billionaire… Except Me" | 5.4M | Tilla shahar ustidan kamera uchishi → 1-soniyada yig'layotgan qahramon, ko'kragida "$1" | 0–2 s: 3 ta kadr | "nega hamma boy, u esa $1?" — javob oxirida |
| iEqs6sSIJEE (15 s) | 1.7M | 3 mitti personaj ulkan yurakni tepaga ITARAYOTGAN payt | 2.5 s: osmondan pul bog'lami tushadi | "nimani olib boryapti?" |
Umumiy: (a) harakat ALLAQACHON ketyapti, (b) kadrda bitta g'ayrioddiy/kattalashtirilgan buyum, (c) yorqin, (d) rasmning o'zi savol tug'diradi,
(e) 1–2.5 s ichida birinchi "voqea" (ochilish, tushish, kesim), (f) sarlavha yozuvi kichik, rasmni yopmaydi (subtitr pastda).
Manbalar: vidIQ blog (Shorts hooklari: "payoff'ni ko'rsat, setup'ni emas"; matn 3–7 so'z, yuqori uchdan birida; qaror ~1 s; "Viewed vs Swiped Away" eng yaxshilarda 70–90%).

## 3. Bizning holat (o'lchov: engine/hook_check.py; kadrlar docs/looks_samples/visual_hook_audit_2026-11-27.jpg)
| Video | 1-kadr yorug'ligi | 1 s ichida harakat | Hukm |
|---|---|---|---|
| Rocco P1 Scam or Legit #4 | 0.36 | 0.04 | FAIL — 2 soniya xira binafsha fon + yozuv, rasm umuman yo'q |
| Rocco RC-25 Penny Plays Dumb 3 | 0.49 | 0.06 | FAIL — personajlar 1 s qotib turadi |
| Rocco RC-24, RC-12, RC-08 v2 | 0.54–0.62 | 0.06–0.09 | WARN — kadr yaxshi (RC-12: Slick Penny'ni tortyapti — to'qnashuv bor), lekin qotgan |
| Financier aaa_u03 (81.5M) | 0.19 | 0.15 | FAIL — tungi shahar, qorong'i; kadr markazini sarlavha bloki yopgan |
| Financier u05_fake50, buck_v01 | 0.32–0.35 | 0.12–0.19 | WARN — xira; rasm umumiy (olomon, kiyik), da'voni isbotlamaydi |
| Financier drawer_r01 | 0.41 | 0.22 | PASS — tortma OCHILYAPTI (harakat boshlangan, "ichida nima?") — namuna |
Asosiy kamchilik: bizning hook — YOZUV. Rasm "mavzuga yaqin fon", o'zi hech narsa demaydi; Rocco'da birinchi soniya — qotgan kadr.

## 4. QOIDA — har video (ikkala kanal), ssenariy bosqichidan boshlab
Spec'da yangi majburiy maydon: `"visual_hook": {"type": "...", "frame1": "...", "event_at": 0.x, "question": "..."}`.
1. **Avval rasm, keyin gap.** Ssenariy yozishdan oldin 1-kadr tanlanadi: "ovozsiz, yozuvsiz ko'rsa — to'xtaydimi?" Yo'q bo'lsa — boshqa kadr.
2. **Harakat boshlangan bo'lsin** (action in progress): ochilayotgan, tushayotgan, quyilayotgan, yirtilayotgan, yugurib kirayotgan. Qotgan kadr bilan boshlash TAQIQ (0.0 s dan harakat).
3. **Natijani ko'rsat, tayyorgarlikni emas** (payoff first): eng kuchli tasvir videoning oxiridan olinib 1-kadrga qo'yiladi (keyin "qanday qilib?" ga qaytiladi).
4. **Bitta g'ayrioddiy buyum yoki o'lcham farqi**: ulkan narx yorlig'i, pul to'la sumka, tangalar tog'i yonida mitti Buck, Slick'dan 3 baravar katta soya.
5. **Birinchi voqea ≤ 1.0 s** (kesim, zoom, buyum paydo bo'lishi, personaj reaksiyasi), ikkinchisi ≤ 2.5 s.
6. **Yozuv rasmni yopmaydi**: 3–7 so'z, kadrning YUQORI uchdan birida, markaz bo'sh (asosiy buyum markazda). Katta qora sarlavha bloki markazda — TAQIQ.
7. **Yorug'**: 1-kadr yorqinligi ≥ 0.40 (Rocco ≥ 0.50). Tungi/qorong'i lavha 1-kadrga qo'yilmaydi.
8. **Uch qatlam bir narsani aytadi**: rasm = yozuv = birinchi gap. Rasm "pul", yozuv "kiyik" bo'lsa — hook yo'q.
9. **Halollik**: 1-kadrda ko'rsatilgan narsa videoda albatta bor (aldov-clickbait yo'q). Chegaralar o'zgarmaydi: logo/brend, real shaxs, behayo kiyim, firibgarlik usuli tafsiloti — yo'q.
10. **Loop**: oxirgi kadr 1-kadrga ulanadi (o'sha buyum/burchak) — qayta ko'rish uchun.

## 5. Vizual hook turlari (ketma-ket ikki videoda bir xil tur ishlatilmaydi)
| Tur | Nima | Financier misoli | Rocco misoli |
|---|---|---|---|
| A. Harakat ichida | ish allaqachon ketyapti | qo'l $100 ni yirtyapti / kassa lentasi chiqyapti | Slick derazadan tirmashib kiryapti |
| B. Natija avval | oxirgi kadr boshida | tangalar tog'i (keyin: "bu 1 kunlik…") | Slick qafasda/yiqilgan, Penny qo'l silkiyapti → "30 soniya oldin" |
| C. G'ayrioddiy buyum | kutilmagan narsa | bankomatdan konfet chiqyapti; ulkan narx yorlig'i | sovg'a qutisi ichidan faqat QR chiqadi |
| D. O'lcham farqi | mitti vs ulkan | mitti Buck pul devori oldida | mitti Penny ustida ulkan Slick soyasi |
| E. Reaksiya | kuchli his yaqin planda | Buck jag'i tushgan (ECU) | Penny ko'zi kosasidan chiqqan + telefon |
| F. To'qnashuv | ikki personaj ziddiyatda | Buck vs bank oynasi (itarishyapti) | Rocco Slick qo'lini ushlab turibdi |
| G. Buzilgan kutilma | tanish narsa noto'g'ri | chek 3 metr uzun | "bank xodimi" niqobi sirg'alib tushyapti |
| H. Sanoq/poyga | ekranda tez o'zgarayotgan son | hisoblagich $0 → $149,306 1 s da | "−$500" hisoblagichi Penny tepasida |

## 6. Kanal bo'yicha retsept
**Financier (Buck):** 0.0 s — to'liq ekran YORUG' lavha, markazda bitta buyum, harakat ketyapti (bankdan: `coffee_pour`, `coins_fall`, `wallet_empty`, `cash_count`, `calendar_flip`; yo'q bo'lsa `find_broll` → ko'rib → bankka).
Sarlavha — yuqorida 2 qator, fon blokisiz (kontur bilan). 0.3–0.6 s — raqam kartochkasi "urilib" kiradi (scale 1.3→1.0). ≤1.0 s — Buck reaksiya bilan kiradi (kadrning ≥1/4).
**Rocco (3D/2D):** 0.0 s — to'qnashuv yoki natija kadrida boshlanadi (docs/viral_cartoon_study.md: "first frame = conflict already happening"), personaj allaqachon harakatda
(qo'l cho'zilgan, og'iz ochiq, sakrash o'rtasida). Sarlavha tepada kichik. Birinchi so'z ≤0.65 s. Qo'ng'iroq/telefon ekrani bilan boshlash faqat ekran allaqachon jiringlayotgan/titrayotgan bo'lsa.
"Scam or Legit": xira fon o'rniga 0.0 s dan uchta xabar kartochkasi uchib kiradi, Rocco lupa bilan ustida.

## 7. Navbatdagi videolarga vizual hook (ochilmagan — qayta kesish mumkin)
| Video | Hozir | Vizual hook (1-kadr → ≤1 s voqea) | Tur |
|---|---|---|---|
| Rocco P1 Scam or Legit #4 (28-noy) | xira fon + yozuv, FAIL | 3 xabar kartochkasi 0.0 s dan ekranga "tushadi", Rocco lupani birinchisiga tutadi; fon yorug' | A+C |
| Rocco RC-25 (29-noy) | qotgan kadr, FAIL | Slick'ning qizil "ogohlantirish" ekranlari 0.0 s dan miltillaydi, Penny telefonni quloqqa olib boryapti (harakat o'rtasi); 0.8 s — Penny "ahmoq" qiyofasiga o'tadi (ko'z qisish kameraga) | A+E |
| Rocco RC-24 (29-noy) | qotgan, WARN | Natija avval: Slick pul bog'lamini O'ZI Penny tomon itarib yuboryapti (1 s), yozuv "30 seconds earlier" → suhbat | B |
| Rocco RC-23 (28-noy) | — (hook_check qilinsin) | Penny go'shakni teskari ushlab turibdi, Slick ekranda peshonasiga uradi | G+E |
| Rocco RC-01, RC-02 (1–2 dek) | 2D, qotgan boshlanish ehtimoli | RC-01: telefon stol ustida sakrab jiringlayapti, Rocco panjasi sekin tushadi; RC-02: Penny tepasiga "+$1,000" yog'iladi, 1 s da qizil "?" | A / C |
| Financier BK-13 Cyber Monday $15.1B | — | hisoblagich 0 → $15.1B 1 s da + ustma-ust tushayotgan qutilar (yorug' ombor) | H+A |
| Financier BK-14 Rigged Coin Bet | — | tanga havoda aylanyapti (sekinlashtirilgan, yaqin plan), Buck pastdan tikilib turibdi | A+E |
| Financier BK-15 Spend $100K a Day | — | pul bog'lamlari konveyerda oqyapti / qo'l pul sochyapti, hisoblagich kamaymaydi | A+G |
Ochilgan videolar qayta chiqarilmaydi; qoida shu kundan boshlab har yangi videoga.

## 8. Tekshiruv
- `python3 -I engine/hook_check.py VIDEO.mp4 [--sheet x.jpg]` — 1-kadr yorug'ligi, 1 s ichidagi harakat, markazdagi sarlavha bloki. qc_gate 16-qadam `16_visual_hook`: FAIL = chiqmaydi.
  (Chegaralar o'z videolarimizda sozlangan: qotgan Rocco ochilishlari 0.03–0.08, Financier 0.11–0.22. Raqobatchi fayllarida o'lchanmagan.)
- Mashina o'lchamaydigan qism (rasm da'voni isbotlaydimi, savol tug'diradimi) — 5 kadrlik varaq (`--sheet`) bilan ko'z bilan: "ovozsiz, yozuvsiz to'xtarmidim?"
- Natija o'lchovi: YouTube Studio → Shorts → "Viewed vs Swiped Away". Har video uchun docs/results ga yoziladi; maqsad — kanalning oldingi o'rtachasidan yuqori, etalon 70%+.
- Sinov: haftasiga 3 ta juftlik (bir mavzu, ikki xil vizual hook turi) — qaysi tur yutganini growth_log ga.
