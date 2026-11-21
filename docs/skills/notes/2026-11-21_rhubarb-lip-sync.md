# Rhubarb Lip Sync — ovozdan og'iz shakllari (viseme) vaqt jadvali
Manba: https://github.com/DanielSWolf/rhubarb-lip-sync — teg v1.14.0 (commit 9b9573c, HEAD bilan bir xil), MIT.
Bog'liqliklar ham MIT/BSD/Boost kabi ruxsatli; muallif yozishicha natija (lip-sync ma'lumoti) to'liq bizniki.
Tekshirildi: 2026-11-21 (faqat README, LICENSE, release sahifasi o'qildi; hech narsa ishga tushirilmadi).

## Nima
CLI dastur: WAV/OGG ovozni oladi, vaqt belgili og'iz shakllari ro'yxatini chiqaradi (TSV / JSON / XML / DAT).
Asosiy 6 shakl: A (yopiq — P/B/M), B (biroz ochiq, tishlar), C (ochiq — EH/AE), D (keng — AA),
E (yarim yumaloq — AO/ER), F (cho'chchaygan — UW/OW/W). Qo'shimcha: G (F/V), H (L), X (dam/pauza).
Tanuvchi: pocketSphinx (inglizcha, oflayn, standart) yoki "phonetic" (tilga bog'liq emas, kamroq aniq).
`-d dialog.txt` — ssenariy matnini berish aniqlikni oshiradi (bizda "say" matni tayyor).
Windows/macOS/Linux uchun tayyor binar release'da bor. Tarmoqqa murojaat haqida hech narsa yo'q — oflayn ishlaydi.

## Nega bizga
Hozirgi `talk_level()` (engine/make_video.py) og'izni ovoz balandligi + so'zdagi "oo/ow" harflaridan taxmin qiladi
(0 yopiq, 1 yarim, 2 keng, 3 "o"). Rhubarb fonemaga asoslangan: P/B/M da og'iz haqiqatan yopiladi, "you/who" da yumaloqlanadi.

## Qo'llash bosqichlari (Buck kadrlari qayta render QILINMASDAN)
1. Release'dan Linux zip ni yuklab (`Rhubarb-Lip-Sync-1.14.0-Linux.zip` — nomini release sahifasida tasdiqlang),
   `~/tools/rhubarb/` ga oching (repo ichiga EMAS). sha256 ni yozib qo'ying.
2. `make_video.py` da voice.wav yozilgandan keyin har sahna uchun: sahna "say" matnini `dialog.txt` ga yozib,
   `rhubarb -f json -d dialog.txt --extendedShapes X voice_scene.wav -o mouth.json` (yoki butun voice.wav bir marta).
3. Xarita mavjud 4 variantga: A, X -> 0; B, G, H -> 1; C, D -> 2; E, F -> 3.
4. `spec["_mouth_cues"]` = [(start, end, level)] ; `talk_level()` avval shu jadvaldan qidiradi,
   topilmasa (rhubarb yo'q/xato) eski envelope usuliga qaytadi — fallback albatta qolsin.
5. Keyinroq (ixtiyoriy): GPU da 6 shakl uchun alohida og'iz kadrlari (6 kayfiyat x 6) — sifat sezilarli bo'lsagina.
6. QC: 1 ta Short ni eski va yangi usulda render qilib, yonma-yon 0.5x tezlikda ko'ring; jurnalga yozing.

## Cheklov / xavf
- pocketSphinx faqat inglizcha — bizga mos; ElevenLabs ovozidagi tez nutqda aniqlik pasayishi mumkin (dialog fayl yordam beradi).
- Tezlik: real vaqtdan sekinroq bo'lishi mumkin (30 s Short uchun bir necha soniya–daqiqa) — kesh qiling (wav hash bo'yicha).
- Binarni repo'ga qo'shmang; faqat yo'lini env (`FIN_RHUBARB`) orqali bering.
- Sprite tezligi (har 2 kadr) saqlansin, aks holda og'iz "titraydi".
