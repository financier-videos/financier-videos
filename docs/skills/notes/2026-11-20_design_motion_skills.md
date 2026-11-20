# Dizayn va harakat skillari (Shohjahon 2026-11-20 20:23: "ko'rib chiq, saqlab ishlat")
Uchalasi ham VEB-INTERFEYS dizayni uchun yozilgan (sayt, dashboard, ilova ekrani) — video uchun emas. Bizga ko'chadigani: tipografika, rang, kompozitsiya va harakat (animatsiya) tamoyillari; ular kadrdagi grafika, thumbnail va (kelajakda) kanal sahifasi uchun.
| Manba | Litsenziya | Olingan | Bizda |
|---|---|---|---|
| emilkowalski/skills (64eb3de) | MIT | animatsiya skillari: animation-vocabulary, choreograph, animate, review-animations (+STANDARDS), improve-animations, find-animation-opportunities, learn-taste, animation-performance | `docs/skills/emil-skills/` |
| pbakaus/impeccable (b49177d) | Apache-2.0 (NOTICE saqlangan) | SKILL.md + 15 qo'llanma: typeset, colorize, layout, animate, critique(-rubric), craft, polish, visualize, bolder, distill, delight, clarify, foundations | `docs/skills/impeccable/` (CLI va skriptlari olinmadi) |
| Leonxlnx/taste-skill (tasteskill.dev) | MIT (sayt bo'yicha) | KO'CHIRILMADI — faqat eslatma: veb-sahifa yasaydi, 3 kenglikda brauzerda tekshiradi; kalit talab qilmaydi, rasm qidirish uchun internetga chiqadi | kanal uchun landing/"link in bio" sahifasi kerak bo'lganda ishlatiladi |

## VIDEOGA KO'CHADIGAN TAMOYILLAR (o'z so'zimiz bilan; UI qoidalarini ko'r-ko'rona ko'chirmaymiz — video multfilm harakatiga ega)
1. Har harakatning sababi bo'lsin: yo'nalish ko'rsatadi, holat o'zgarganini bildiradi yoki tushuntiradi. "Chiroyli" uchun harakat — olib tashlanadi.
2. Kirish — tez boshlanib sekinlashadi (ease-out); chiqish — qisqaroq. Kirish va chiqish vaqti bir xil bo'lmasin.
3. Bir nechta element birga kirsa — 30–80 ms oraliq bilan navbatma-navbat (stagger), hammasi birdan emas.
4. Tez-tez takrorlanadigan element (subtitr so'zlari, progress chizig'i) — minimal harakat; kamdan-kam hodisa (raqam ochilishi, Buck tryuki) — to'liq "delight".
5. Tipografika: bitta kadrda ko'pi bilan 2 shrift oilasi va 3 o'lcham darajasi; eng kichik matn ham telefonda o'qilsin.
6. Rang: bitta urg'u rangi kadrga; qizil — faqat yo'qotish/ogohlantirish, yashil — o'sish; matn va fon kontrasti yuqori.
7. Tanqid tartibi: avval ierarxiya (ko'z birinchi qayerga tushadi), keyin o'qilishi, keyin bezak.

## QO'LLANDI (2026-11-20 20:55)
- Tipografika tekshiruvi kadrlarimizda bitta aniq kamchilik topdi: "Source:" qatori 26 px, kulrang — telefonda o'qilmaydi (har fakt manbali degan qoidamizni ko'rinmas qilib qo'yadi). TUZATILDI — dvigatel v6.4: 32 px, ochroq rang + qora kontur, uzun qator kadrga sig'ishi uchun avtomatik kichrayadi. Sinov kadri ko'rildi.
- KEYINGI (B ishi): `review-animations` o'nta mezoni bo'yicha dvigateldagi kirish animatsiyalarini ko'rib chiqish (stat, sticker, vs-panel, Buck pop-in) — topilmalar jadvali growth_log ga; bittasini tuzatish.
