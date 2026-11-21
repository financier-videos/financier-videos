# ruptures — retention egri chizig'ini bo'laklarga ajratish (change-point detection)
Manba: https://github.com/deepcharles/ruptures — HEAD ee1c8ff; PyPI `ruptures` 1.1.10 (2025-09-10), BSD-2-Clause.
Linux wheel cp39…cp313. Tekshirildi: 2026-11-21 (PyPI metama'lumot va README; o'rnatilmadi).

## Nima
Signaldagi keskin o'zgarish nuqtalarini topuvchi kutubxona (PELT, Binseg, Window, Dynp; "l2", "rbf" xarajat
funksiyalari). numpy/scipy ustida, oflayn, kalit yo'q.

## Nega bizga (youtube-agent-skill retention.py ni TO'LDIRADI, takrorlamaydi)
retention.py bitta videoda "hook leak / cliff / slide" ni qat'iy chegaralar bilan topadi. ruptures esa egri chiziqni
o'zi tabiiy "rejim"larga bo'ladi (tez tushish -> plato -> sekin tushish) — chegara tanlamasdan. Asosiy foyda:
bo'linish nuqtalarini BIZNING spec'dagi sahna chegaralari (`sc["start"]`, `sc["dur"]`) bilan solishtirish —
qaysi sahna turi (stat, b-roll, Buck act, chart) ketma-ket videolarda tushish boshlanishiga to'g'ri keladi.

## Qo'llash bosqichlari
1. `pip install ruptures==1.1.10`.
2. Studio'dan Short retention CSV (Analytics -> video -> Engagement -> retention -> yuklab olish) ni
   `data/retention/<video_id>.csv` ga qo'ying (qo'lda; API/kalit ishlatilmaydi).
3. `engine/retention_segments.py` (o'zimiz yozamiz): CSV ni retention.py dagi kabi o'qing, pozitsiyani soniyaga
   o'tkazing (Short uzunligi spec'dan), `rpt.Pelt(model="l2", min_size=3).fit(y).predict(pen=...)`.
   `pen` ni 3–4 videoda qo'lda sozlang; har bo'lak uchun qiyalik (%/s) hisoblang.
4. Har bo'linish nuqtasiga ±0.5 s ichidagi sahnani spec'dan biriktiring -> jadval: video, sahna turi, qiyalik o'zgarishi.
5. Haftalik C ishida (yakshanba) 10+ Short jadvalini birlashtiring: "qaysi sahna turidan keyin tushish tezlashadi" —
   GIPOTEZA sifatida growth_log ga.

## Cheklov / xavf
- Short retention'ida nuqtalar kam (~100) va loop sabab 100% dan oshishi mumkin — 100+ qiymatlarni kesmang, alohida belgilang.
- `pen` tanlovi natijani o'zgartiradi; kichik namunada xulosa qilmang (kamida 10 video).
- Studio CSV formati o'zgarishi mumkin — o'qish funksiyasi bardoshli bo'lsin.
