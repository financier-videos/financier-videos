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
