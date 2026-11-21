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
