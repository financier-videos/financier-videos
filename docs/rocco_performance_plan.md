# ROCCO — personajlarni "jonlantirish" rejasi (master prompt bo'yicha), 2026-11-22

Manba: Shohjahon master prompti (uch personaj — sevimli, kulgili, ifodali multfilm qahramonlari; bosqichma-bosqich; sinovdan o'tmagan narsa "tayyor" deyilmaydi).
Sinov videosi: `rocco_performance_test_v1.mp4` (12 s, ovozsiz previz), kadrlar `docs/looks_samples/rocco_performance_test_v1.jpg`.
Skriptlar: buck-private/rocco_cast_v1/scripts/skit.py (+ skit_lines.json).

## Xarakter "pasporti" (har epizodda saqlanadi)
| | Rocco | Penny | Slick |
|---|---|---|---|
| Harakat tezligi | sekin, kam, aniq | tez, butun tanasi bilan | tez, mayda, bezovta |
| Asosiy ifoda | yarim yumuq ko'z, bitta qosh | katta ko'z, keng tabassum | qiyshiq iljayish, ko'z o'ynatish |
| Hazil turi | deadpan, quruq javob | sodda tushunmovchilik, haddan ortiq quvonch | o'ziga ishonch → o'zi fosh bo'lish |
| Kulgi qoidasi | hech qachon jabrlanuvchi ustidan emas | ahmoq emas — ishonuvchan | qo'rqinchli emas — omadsiz |
| Imzo harakatlari | sekin qosh ko'tarish, ko'z bilan oldin qarash, ishonchli ko'rsatish, mayda kinoyali tabassum | sakrash, qo'l silkitish, mungli qosh, qiqirlash | pusib kirish, qo'l ishqalash, soxta tabassum, asabiy pirpirash, vahima, qochish |

## Holat: nima TAYYOR va SINALGAN (v1 sinov videosida ko'rinadi)
- Skelet + 31 yuz shape key (ko'z, qovoq, qarash, qosh, og'iz, jag', big_eye), og'iz ichi alohida material.
- Harakat tizimi: silliq o'tishlar (ease), anticipation, overshoot, squash/stretch (hajm saqlanadi), nafas/idle, dum-quloq kechikishi,
  ko'z boshdan oldin buriladi, turli pirpirash, kameralar (keng plan / yirik plan, sekin yaqinlashish), personajlar bir-biriga qaraydi.
- Og'iz harakati: matndagi unlilardan (a/o/u/e/i) — jag' + lab shakli. BU HALI OVOZ BILAN SINXRON EMAS.

## Hali YO'Q yoki sinalmagan (aldamaslik uchun)
- Ovoz va haqiqiy lip-sync (ElevenLabs kod chatida) — sinalmagan. Til, tish — yo'q.
- IK/FK, barmoqlar, plashch/soch fizikasi — yo'q. Penny dumi suyagi yo'q.
- "Kino sifati" yorug'lik/material — yo'q: hozir tezkor Workbench previz; yakuniy render GPU'da (Cycles/EEVEE) qilinishi kerak.
- Slick modeli sodda bolaga o'xshaydi (ifoda bilan qisman tuzatilgan) — yangi model kerak bo'lishi mumkin.
- Qo'ltiq/yeng deformatsiyasida mayda nuqsonlar; Rocco "ko'rsatish" pozasi noaniq (panja yuz oldida).

## Bosqichlar
1. (BAJARILDI) Aktivlarni ko'rish, rig, yuz, multfilm ko'rinishi, birinchi previz.
2. Rig sayqali: qo'ltiq vaznlari, Rocco ko'rsatish/qo'l qovushtirish/shlyapa tuzatish, Penny "qo'llar yonoqda", Slick "terlash", til+tish, Penny dumi.
3. Harakat kutubxonasi: har personajga 10–12 qayta ishlatiladigan harakat + 16 hissiyot presetlari (master prompt 3–5-bo'limlar).
4. Ovoz: tanlangan ovozlar (Rocco 7, Penny 11, Slick) bilan Text-to-Dialogue → nutq konvertidan lip-sync → sinov.
5. Yakuniy ko'rinish: GPU render, yorug'lik, soya, fon to'plamlari (xona, ko'cha, do'kon).
6. Birinchi to'liq epizod (RC-04) → etalon kartasi bilan solishtirish → Shohjahon tasdig'i → chiqarish.
Har bosqich oxirida previz/kadr varag'i ko'rsatiladi; tasdiqlanmagan bosqichdan keyingisiga o'tilmaydi.

## 12. TASHQI KO'RINISH QULFI (Shohjahon, 2026-11-22 16:33) — MAJBURIY
Tasdiqlangan 3D modellar va ularning ko'rinishi — yagona manba. Vazifa: animatsiya, joziba va xarakterni yaxshilash; ko'rinishni QAYTA CHIZMASLIK.
1. Tur, yuz tuzilishi, tana nisbati, ranglar, kiyim va belgi-aksessuarlar o'zgartirilmaydi.
2. Bir personaj boshqasiga o'xshab qolmaydi.
3. Tasdiqlangan 3D aktivlar ruxsatsiz almashtirilmaydi va qayta talqin qilinmaydi.
4. Ifodalar faqat rig, shape key va nazoratli deformatsiya orqali — personaj o'zligini o'zgartirmasdan.
5. Harakat shaklni bo'rttirishi mumkin, lekin asl siluet tanilib turadi.
6. Har sahna, burchak va animatsiyada uchalasi tasdiqlangan modelga aynan o'xshaydi.
7. Animatsiya uchun vizual o'zgarish zarur bo'lsa — avval Shohjahondan ruxsat so'raladi.
Ustuvorlik: o'zlikni saqlash > effektlar va qayta dizayn.
Tavsif (matn): Rocco — kulrang yenot, qora niqob, krem tumshuq/qorin, jigarrang ko'z yarim yumuq qovoq, qizil lentali jigarrang shlyapa, bej plashch, qizil galstuk, halqali dum.
Penny — pushti shar kopilka, orqada tanga tirqishi, sariq-tilla bantik, 4 kalta oyoq, burama dum. Slick — ozg'in baland tulki, tor sariq ko'z, qiyshiq iljayish + bitta tish,
binafsha keng kostyum, oq ko'ylak, qiyshiq qizil galstuk, tilla to'g'nag'ich, peshonada taralgan tutam, to'q jigarrang panjalar.
QARORLAR (Shohjahon, 2026-11-22 16:40) — tasdiqlangan ko'rinish shular:
- ROCCO: yuklangan model (raccoon_detective 2-variant) — tasdiqlangan.
- PENNY: yuklangan model (ko'ylakli cho'chqa qiz), kiyimi/bantigi/poyabzali FIRUZA — tasdiqlangan. Matndagi "shar kopilka, tanga tirqishi, sariq bantik" tavsifi Penny uchun KUCHDAN QOLDI.
- SLICK: hozirgi model VAQTINCHA. Shohjahon yangi model yasaydi (1-variantning yuzi va kiyimi: tor sariq ko'z, qiyshiq iljayish, tish, qizil galstuk; qo'llari tanadan ochiq). Kelgach chat qayta rig qiladi. Ungacha Slick bilan yakuniy epizod chiqmaydi.
- NISBATLAR: multfilm standarti TASDIQLANDI — big_eye 1.0 (Penny 0.7), bosh 1.12, qo'l 1.2.
Bundan boshqa har qanday vizual o'zgarish — faqat ruxsat bilan (7-qoida).
