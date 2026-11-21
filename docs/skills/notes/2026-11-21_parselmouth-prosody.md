# Parselmouth (Praat) — ovoz prosodiyasi va komik pauza tekshiruvi
Manba: https://github.com/YannickJadoul/Parselmouth — HEAD 9a3d671; PyPI `praat-parselmouth` 0.4.7 (2025-11-27), GPL-3.0.
Linux wheel'lar cp311 uchun bor. Tekshirildi: 2026-11-21 (PyPI metama'lumot va README; o'rnatilmadi).

## Nima
Praat (fonetika dasturi) ning Python API'si: F0 (ovoz balandligi/pitch) konturi, intensivlik (dB), formantlar,
ovozli/ovozsiz bo'laklar. Oflayn, kalit/tarmoq yo'q.

## Nega bizga
`engine/voice_check.py` faqat SO'ZLARni tekshiradi (ASR). Bu esa QANDAY aytilganini o'lchaydi:
- monotonlik: jumla F0 diapazoni (yarim tonlarda) juda tor bo'lsa — Buck "robotdek" eshitiladi;
- savol jumlasi oxirida ko'tarilish bormi; punchline urg'usi (F0/intensivlik cho'qqisi) kalit so'zga tushadimi;
- komik vaqt: punchline oldidagi pauza uzunligi (bizda spec "land" maydoni bor) haqiqatda necha ms chiqdi.

## Qo'llash bosqichlari
1. `pip install praat-parselmouth==0.4.7`.
2. `engine/prosody_check.py` (o'zimiz yozamiz) — voice.wav + spec sahna vaqtlari (`speech`, `sdur`, `words`):
   har sahna uchun `snd.to_pitch()` -> F0 median, 10–90 persentil diapazoni (semiton), `snd.to_intensity()` -> cho'qqi vaqti.
3. Ogohlantirish qoidalari (GIPOTEZA, o'z raqamimiz bilan sozlanadi): diapazon < ~3 semiton -> "monoton";
   "?" bilan tugagan jumlada oxirgi 300 ms F0 pasaysa -> "savol ohangi yo'q"; punchline oldi pauza < "land" -> ogohlantirish.
4. Natijani result JSON ga `prosody` bo'limi sifatida yozing; QC ro'yxatiga qo'shing. Monoton jumla -> ElevenLabs
   sozlamasini (stability/style) o'zgartirib qayta sintez yoki matnga vergul/pauza qo'shish.
5. Bir haftalik ma'lumotdan keyin prosody ko'rsatkichlarini retention bilan solishtiring (growth_log).

## Cheklov / xavf
- GPL-3.0: biz faqat ISHLATAMIZ (dastur sifatida tarqatmaymiz) — tijorat videolari uchun muammo yo'q; kodini repo'ga ko'chirmang.
  Agar kelajakda dvigatelni boshqalarga tarqatsak, bu bog'liqlik GPL majburiyatini keltiradi — shunda ixtiyoriy modul qiling.
- Chegaralar (3 semiton va h.k.) — manbasiz taxmin, faqat sinov uchun.
- Sintetik ovozda F0 aniqlash odatda yaxshi; shivir/kulgi bo'laklarida xato bo'lishi mumkin.
