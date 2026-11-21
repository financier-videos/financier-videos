# SSENARIY QOIDALARI v2 (2026-11-21 audit; dalil: docs/audit_2026-11-21.md) — MAJBURIY, script_bank va producer_task dagi eski andozadan USTUN
## TAQIQ (skelet takrori)
- 2-jumla "Wait...?" bilan boshlanishi: 5 videoda ko'pi bilan 1 marta. Yakun "..., because..." : 4 videoda ko'pi bilan 1 marta.
- Ketma-ket ikki videoda bir xil TUZILMA yo'q; bir kunda kamida 4 xil tuzilma.
- Post oldidan: `python3 -I engine/script_check.py YANGI.json <oxirgi 4 spec>` — FAIL bo'lsa qayta yoz.
## TUZILMALAR (har videoda bittasi; spec "structure": nom)
| Nom | G'oya | Uzunlik | Tasvir talabi |
|---|---|---|---|
| why_story | bitta "nega?" savoli → sabab hikoyasi (kim, qachon, nima uchun) → bugungi oqibat | 45–75 s | har 6–9 s yangi sahna; personaj sahna ICHIDA |
| scale_ladder | bitta katta raqam → 5–7 ta kuchayib boruvchi taqqoslash (vaqt, masofa, og'irlik, koinot) | 45–85 s | HAR pog'onaga o'z tasviri; oxirgisi eng katta |
| one_number | bitta raqam, bitta jumla, bitta tasvir | 8–12 s (mikro) | 1–2 kadr, loop |
| myth_bust | "hamma shunday deydi" → aslida → dalil | 25–35 s | ikki holat yonma-yon |
| ranking | 5→1 sanash, har biriga 1 fakt | 30–45 s | har o'ringa alohida lavha |
| timeline | "1970 → bugun": narx/qiymat qanday o'zgardi | 30–50 s | yil hisoblagichi + davr lavhalari |
| how_made | narsa qanday yasaladi/ishlaydi (kupyura, karta, chek) | 45–75 s | bosqichma-bosqich, o'z chizmamiz |
Kunlik aralashma (8 Short): 3 mikro (one_number) + 3 hikoya (why_story / scale_ladder / how_made) + 2 o'rta (myth_bust / ranking / timeline). 72 soatda o'lchab, yutgan qutbga 6:2.
## HAR SSENARIYDA
- HOOK: 1-kadrda to'liq jumla YOZUV bo'lib turadi (ovozsiz ko'rgan ham tushunsin) + birinchi 1.5 s ichida eng kuchli tasvir.
- Bitta video = bitta savol. Statistika ro'yxati emas.
- Har 6–9 s da "yangi narsa" (yangi tasvir yoki burilish); sahna rejasida har sahnaga: aytilgan gap → tasvir (yo'l 1/2/3/4, docs/producer_task "LAVHA TANLASHDA KENG O'YLASH").
- Buck sharhlovchi, lekin har sahnada emas: hikoya sahnalarida burchakda yoki umuman yo'q; 1–2 luqma.
- Yakun 4 xildan biri (savol / keyingi qism / loop / bitta raqam qora fonda) — docs/looks.md.
- Raqamlar: manba va sana; o'z hisobimiz bo'lsa ekranda "our math" va tavsifda formula.
## SARLAVHA (aralashtir): "Why ...", "How big is ...", "How ... is made", raqamli da'vo ("$3.79 Billion in ONE Day") — ketma-ket 3 ta bir xil turdagi sarlavha yo'q.

## HIKOYA MEXANIKASI (2026-11-21 21:20; ikki g'olibning transkripti o'qildi — tuzilma olinadi, matn ko'chirilmaydi)
"Why Prices End In 99 Cents" (60 s, ~190 so'z ≈ 3.2 so'z/s; bizda 2.3):
1. VOQEA O'RTASIDAN boshlanadi: birinchi jumlada personaj nimadir QILADI (kirish, "did you know", raqam yo'q).
2. Mavzu savoliga JAVOB FAQAT OXIRGI JUMLADA — sarlavha savol, javob 55-soniyada. Tomoshabin oxirigacha kutadi.
3. Kichik mojaro: ikki personaj (xo'jayin va kassir), shubha, burilish ("bir kuni ertalab hamma narx 1 sentga o'zgargan").
4. Aniq buyumlar va sahnalar (konfet, etik, velosiped, qo'ng'iroq) — har jumla chizsa bo'ladigan rasm. Statistika 0 ta.
5. Bitta dialog almashinuvi (savol–javob), 1 hazil.
"How Big Is a Trillion?" (85 s): ikki ovozli SUHBAT (biri aytadi, ikkinchisi hayratlanadi) + 7 pog'onali narvon; har pog'ona oldingisidan katta; oxirgisi koinot.
BIZGA QOIDA:
- why_story / how_made: 1-jumla — harakat; javob — oxirgi jumlada; 2 personaj (Buck + bitta yangi obraz: do'kondor, bankir, kassir — o'z chizmamiz); 150–190 so'z / 55–65 s (≈3 so'z/s; Buck ovozi tezligi mos bo'lsin).
- scale_ladder: Buck + ikkinchi ovoz (hayratlanuvchi; ElevenLabs'da ikkinchi ovoz yoki Buck'ning o'ziga savol-javob) — sinov sifatida 1 ta.
- FAKT HALOLLIGI: mashhur rivoyat (masalan 99 sent va kassa apparati) hujjatlashmagan bo'lsa — "one popular explanation" deb aytiladi va ekranda "legend / popular theory" belgisi; isbotlangan fakt sifatida berilmaydi.
- Birinchi sinov: S-yangi "Why Is It Called a 'Buck'?" yoki "Why Do Receipts Fade?" — manbasi topilgan mavzudan (render oldidan manba shart).

## v2.2: yangi tuzilma `comedy_skit` (docs/comedy.md: har 3–4 s hazil, takroriy hazil, quruq yakun) — kunlik 8 Shortdan 1–2 tasi; fakt videolarida har 8–10 s da 1 kulgili gap yoki gag.

## v2.1 (2026-11-21 21:40; dalil: docs/lessons_winners_2026-11-21.md)
- Yangi tuzilmalar: `guess_reveal` (savol → ikkinchi ovoz taxmin qiladi → javob; 5–8 marta; 35–50 s) va `client_dialogue` (Rocco: mijoz + Rocco suhbati → himoya qadami; 40–60 s).
- KADR TEMPI: spec sahnasida "shots": [...] — har ≤2 s da yangi tasvir. 30 s ≥15 kadr; 60 s ≥30 kadr.
- SUBTITR 1–3 so'z; doimiy sarlavha yo'q. JAVOB oxirgi 5 s da; oxiri boshiga ulanadi.
- Kunlik aralashma (8 Short): 2 mikro, 2 sabab hikoyasi, 1 masshtab narvoni, 1 taxmin–javob, 1 reyting/taymlayn, 1 trend. Ketma-ket ikki bir xil tuzilma yo'q.
