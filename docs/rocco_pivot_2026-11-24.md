# ROCCO PIVOT — har xil yo'nalishlarni sinash (Shohjahon 2026-11-23 ~21:00 UTC: "Rocco natija 0; faqat multik yo'nalishida bir xil qilgansan, har xil yo'nalishni sina; hamma narsaga ruxsat")

## Diagnoz (vidiq_user_videos, 23-noy 21:10 UTC)
| video | uslub | ko'rish |
|---|---|---|
| Penny Plays Dumb With a Scammer (22-noy) | 2D Rocco v2 | 1,103 |
| Free GTA 6 for PC? Free Cheese. (22-noy) | 2D Rocco v2 + trend | 1,168 |
| 3 Red Flags in One Dating App Match (23-noy) | 3D GPU | 4 |
| He Tried to Scam the Wrong Piggy Bank (23-noy) | 3D GPU | 2 |
| The Scammer Wrote Down Her Card Number (23-noy) | 3D GPU | 1 |
Xulosa: (1) 3D epizodlar ko'p vaqt va GPU yedi, natija ~0 (qisman 23-noy 01:17 UTC dagi burst yuklash ham sabab bo'lishi mumkin — isbot emas). (2) Bir formatga (multfilm) hamma kuch tikildi — xato. Endi PORTFEL: har yo'nalishdan 1–2 video, 72 soatda solishtir, yutganini ko'paytir.

## Bozor signali (vidiq_outliers, 10 kredit)
- "POV: When a stranger Venmos you $1,000" — 2D animatsiya, 875.8K (60K kanal); boshqa kanalda shu mavzu 182K (2.1K kanal) → hayotiy POV pul-vaziyat ishlaydi.
- "Joe Huang vs Two-Factor Authentication" 19.8K (2.6K kanal), "A Prince Slid Into Your Inbox" 16.9K (53 obunachi, 16 s), "Bad At Detecting Scams!" 365K (17 s), "This is Definitely a Scam..." 362K (21 s) → juda QISQA (15–30 s), bitta aniq g'oya.
- "Fake Cops Demand Bitcoin" 719K — haqiqiy voqea / yangilik uslubi.

## 6 YO'NALISH (har biri alohida test)
| # | Yo'nalish | Nima | Holat |
|---|---|---|---|
| P1 | SCAM OR LEGIT? chat-o'yin | telefon ekrani, 3 SMS, 3-2-1, muhr, "tell" belgilanadi, izohda ball. Personaj yo'q | 01 TAYYOR (work/rocco/pivot/chat_game.py, sol01; IG 23-noy) |
| P2 | POV pul-vaziyat (2D, qisqa) | "POV: notanish odam sizga $1,000 Venmo qildi" turidagi — 2D Rocco v2 (1,100 olgan uslub), 20–30 s | navbatda |
| B1 | Tarixiy firibgar, kino uslubi (AI kartina kadrlari + Ken Burns + hikoyachi George) | Poyais (1822) — 52.8 s, 27 kadr, o'rtacha 1.95 s/kadr; work/rocco/pivot/story_film.py, hist01; 8 kadr vidIQ image_generate (96 kredit) | TAYYOR, YT draft 24-noy 23:00 UTC |
| P3 | Haqiqiy voqea / yangilik | FTC/DOJ ishi: "Bu odam $X yo'qotdi — mana qanday" lavha + katta raqam + tez matn, 30–45 s | navbatda |
| P4 | 10 soniyalik mikro | bitta qizil bayroq, bitta jumla, loop (8–12 s) | navbatda |
| P5 | Ekran-tahlil (screen breakdown) | haqiqiy firibgar xat/sayt maketi, qizil doiralar bilan 5 ta xato | navbatda |
| P6 | "Scammer vs ..." komediya skiti (ovozli dialog, chat ekranida) | firibgar yutqazadi — matnli chat-hikoya formati | navbatda |
QOIDA: ketma-ket ikki Rocco videosi bir yo'nalishdan bo'lmaydi; 3D GPU epizodlari TO'XTATILDI (natija kelguncha); yuklash — kuniga ≤2 Rocco, oraliq ≥4 soat (burst yo'q).
O'LCHOV: 24/72 soatlik ko'rish + IG plays → docs/results.md "Rocco yo'nalish" ustuni. 72 soatdan keyin eng yaxshi 2 yo'nalish kuniga 2 tadan, qolganlari haftasiga 1 (tekshiruv uchun).

Navbat va id'lar: work/rocco/pivot/queue.json. Tahlil: docs/rocco_research_2026-11-23.md.
