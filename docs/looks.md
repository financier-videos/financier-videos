# KO'RINISHLAR (LOOKS) — videolar bir-biriga o'xshamasligi uchun (Shohjahon 2026-11-21 20:26)
Shohjahon: "videolar yana bir xil bo'lib qolyapti: yozuvlar, grafikalar, lavhalar, stillar."
DALIL: `docs/looks_evidence_2026-11-21.jpg` (oxirgi 8 Short, har biridan 6 kadr). O'lchov (`engine/look_check.py --matrix`): 8 ta video o'zaro 0.77–0.91 o'xshash; o'rtacha yorqinlik hammasida 0.14–0.19; asosiy rang hammasida sariq.
SABAB: qoida so'zda bor edi (theme, fon almashadi), lekin DVIGATELDA BITTA SHABLON: tepada sariq Bangers sarlavha → o'rtada katta raqam → pastda oq/sariq subtitr → chap tepada kichik Buck → oxirida markazda Buck; fon 80% qoraytirilgani uchun 6 theme va Pixabay foni ko'zga ko'rinmaydi. Theme almashtirish = o'sha shablonning boshqa tusi.

## QOIDA (MAJBURIY, Financier va Rocco)
1. Har video spec'ida `"look": "<nom>"` — pastdagi ro'yxatdan. Ketma-ket 3 videoda bir xil look YO'Q; bir kunda kamida 4 xil look.
2. Post oldidan: `python3 -I engine/look_check.py YANGI.mp4 <oxirgi 4 chiqqan/navbatdagi video>` — FAIL (≥0.70) bo'lsa video CHIQMAYDI, look almashtirib qayta render. qc_gate ga qadam sifatida ulansin.
3. Look = 6 narsaning hammasi birga o'zgaradi (faqat rang emas): joylashuv, shrift, rang, fon ishlovi, subtitr uslubi, Buck o'rni/o'lchami.
4. Sarlavha har doim tepada turishi SHART EMAS; har kadrda sarlavha bo'lishi SHART EMAS.

## LOOKLAR (dvigatelga `spec["look"]` sifatida qo'shiladi; "vault" = hozirgi ko'rinish, kuniga ko'pi bilan 1 marta)
| look | Fon | Joylashuv | Shrift | Rang | Subtitr | Buck |
|---|---|---|---|---|---|---|
| vault (hozirgi) | qoraytirilgan lavha | sarlavha tepa, raqam o'rta | Bangers | qora + sariq | pastda 2 qator | kichik, chap tepa |
| paper | OCH: krem qog'oz teksturasi, yengil soya | chapga tekislangan gazeta sahifasi; raqam chap, izoh o'ng ustun | qalin serif (sarlavha) + grotesk | krem, qora siyoh, 1 qizil urg'u | marker bilan belgilangan so'zlar (highlighter) | o'ngda pastda, katta (kadr ≥1/3) |
| fullbleed | Pixabay lavha TO'LIQ yorqin (qoraytirish ≤25%), pastda gradient | matn faqat pastki uchdan birda; tepada sarlavha yo'q | Anton/grotesk, oq | lavha ranglari + oq + 1 urg'u | bitta so'zdan katta (word-by-word) | pastki burchakda yarim tana |
| split | ikki rangli ekran (chap/o'ng yoki tepa/past) | taqqoslash: ikki yarmida ikki raqam, o'rtada VS chizig'i | geometrik sans | 2 to'yingan rang (masalan ko'k/to'q sariq), qora yo'q | markazda, yarimlar orasida | o'rtada, ikki yarmga qarab reaksiya |
| chalk | to'q yashil doska teksturasi | qo'lda chizilgan sxema, strelkalar; raqam bo'r bilan yoziladi | qo'lyozma (Patrick Hand/Caveat) | yashil, oq bo'r, sariq bo'r | bo'r bilan tagiga chizish | chapda, ko'rsatkich bilan (skipetr) |
| receipt | oq chek lentasi qorong'i stol ustida, tepadan pastga suriladi | faktlar chek qatorlari bo'lib chiqadi, jami pastda | monospace | oq, qora, 1 qizil shtamp | chek qatorining o'zi subtitr | chek yonida, kichik emas (≥1/4) |
| neon | tungi shahar lavhasi, yorqin | sarlavha yon tomonda vertikal; raqam neon trubka | yumaloq neon kontur | binafsha/pushti/moviy | pastda kapsula ichida | o'ngda, neon yorug'ida |
Rocco: o'z "case-file" uslubi (v6.12) + shu qoidalar; Rocco uchun looklar: case-file, phone (SMS ekran to'liq), board (dalillar doskasi, ip bilan bog'langan kartalar), paper.

## GRAFIKA VA LAVHA XILMA-XILLIGI (lookdan tashqari)
- Grafik turi ketma-ket takrorlanmaydi: ustun → chiziq → doira/halqa → piktogramma qatori (100 ta odamcha) → xarita → hisoblagich → taymer/progress.
- Lavha (b-roll): har videoda kamida 1 sahna lavha TO'LIQ ekranda va yorqin (matnsiz yoki 1 so'z bilan), 1.5–2.5 s. Hozir lavha faqat xira fon — ko'zga ko'rinmayapti.
- O'tishlar: har videoda bitta "imzo" o'tish, ketma-ket videolarda boshqacha (surish, varaq ag'darish, chek yirtilishi, bo'r o'chirilishi, zoom-through).
- Oxirgi kadr har videoda "markazda Buck + savol" bo'lmasin: 4 xil yakun (savol; keyingi qism va'dasi; boshiga aylanuvchi loop; bitta raqam qora ekranda).

## O'LCHOV
look ustuni docs/results.md ga qo'shiladi; 72 soatda look bo'yicha o'rtacha ko'rish solishtiriladi — eng yaxshi 2 look ko'proq, eng yomoni to'xtatiladi.
