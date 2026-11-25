# RETENTION JURNALI (sekundma-sekund tomosha grafigi → ssenariy qarori)

Usul (docs/studio_os.md §2): video chiqqanidan ≥48 soat o'tgach `vidiq_channel_analytics report=audience_retention filters=video==ID`
→ rows faylga → `python3 engine/retention_read.py ROWS.json RENDERED.json SPEC.json --video ID` → natija shu yerga + 1 qator "QAROR".
Eslatma: YouTube Analytics 1–2 kun kechikadi; yangi videolarda bo'sh qaytsa — keyingi ishga tushishda qayta urin.
audienceWatchRatio > 1.0 = qayta ko'rish (loop). Mo'ljal: 3 s dan keyin ≥0.80, o'rta ≥0.60, oxir ≥0.45.

## 2026-11-25 — birinchi 3 ta video
### Iagm5fk5JoU — Penny Plays Dumb With a Scammer (Rocco, 53.3 s, 1,298 ko'rish)
- start 1.19 · 3 s 1.13 · o'rta 0.61 · oxir 0.23
- ENG KATTA TUSHISH: L1 4–6 s "Oh no! Which bank?" −22 pt; L2 6–8 s "...Your... bank!" −8 pt (sekin kirish, pauza) — asosiy hazil (Penny "Six!") faqat 14 s da.
- 14 s dan keyin grafik deyarli tekis (−1 pt/qator) → hazil yadrosi ISHLAYDI.
- Oxirgi qator — Rocco "Real banks never ask…" (dars) −12 pt, oxirgi 3% da 0.47 → 0.23.

### omDytQ_TRVI — Free GTA 6 for PC? Free Cheese. (Rocco, 48 s, 1,316 ko'rish)
- start 1.24 · 6–10 s oralig'ida 1.00 → 0.79 (−21 pt) · o'rta 0.57 · oxir 0.14 (oxirgi 2% da 0.25 → 0.14)
- Xuddi shu naqsh: 5–10 s da katta yo'qotish, oxirgi dars/CTA da keskin tushish.

### XbWyfVGCWM8 — 13 Years Later, GTA Made 4.7x More (Financier, 27 s, 1,307 ko'rish)
- start 1.44 (kuchli loop) · 4.6–9 s da 1.21 → 0.79 (−42 pt) · o'rta 0.72 · oxir 0.46 (oxirida tushish yo'q — dars yo'q, raqam bilan tugaydi)

## XULOSA → QOIDALAR (barcha yangi ssenariylarga, 2026-11-25 dan)
1. **5–9 soniya = asosiy xavf zonasi.** Hook va'dasi shu oraliqda birinchi "to'lov"ni berishi shart (birinchi hazil / birinchi raqam zarbasi / burilish). Sekin kirish, "Oh no! Which…?" kabi bo'sh reaksiya, pauzali qatorlar 0–9 s ga QO'YILMAYDI.
2. **Asosiy hazil ≤5 s da boshlanadi** (Penny Plays Dumb: firibgar so'rovi 1-qatorda, Pennyning birinchi absurd javobi 2-qatorda).
3. **Oxirida dars/maslahat qatori YO'Q.** Punchline bilan tugaydi, saboq ekrandagi kichik matn yoki tavsifda. (Rocco dars qatori −12 pt, oxir 0.23/0.14; dars yo'q Buck oxiri 0.46.)
4. **Loop ishlaydi** (start 1.19–1.44): oxirgi kadr/gap boshiga ulansin.

## QAROR (2026-11-25)
- RC-23 (Penny Plays Dumb 2) va RC-24 (Refund Trick) — hali chiqmagan → kirish qisqartirildi (hazil ≤5 s), oxirgi Rocco dars qatori olib tashlandi, qayta render.

## 2026-11-25 — begona videolar (docs/viral_beatmap_2026-11-25.md, 8 trend + 6 namuna) bilan tasdiq
- Kesim tezligimiz (1.45–1.9 s) benchmarklardan TEZROQ (2.4–3.9 s) → muammo kesimda emas, SO'ZDA: birinchi qator uzun, temp sekin (bizda 1.8–2.35 so'z/s, ularda 2.8–3.6).
- Yangi qoidalar: 1-qator ≤10 so'z, ≤3 s, nutq 0 ms dan; 3–6 s da 2-zarba, 5–9 s da hazil/raqam; ekranda doimiy banner/hisoblagich; har raqamga kundalik taqqoslash; dialog sketchda musiqa yo'q.
- QAROR: RC-23, RC-24, BK-11, BK-12 shu qoidalar bilan qayta yozildi (Rocco "Psst" qatorlari olib tashlandi, doimiy topline banner, Buck speed 1.12–1.15, BK-11 "??,??? YEARS" teaser).
