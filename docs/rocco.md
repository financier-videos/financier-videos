# RED FLAG ROCCO — qarorlar va holat (yig'ma, 2026-11-21 18:30 Toshkent)
Manba: docs/new_channel_plan.md (to'liq reja, nomzodlar jadvali, manbalar), engine/buffer_post.py, work/rocco/, git tarixi (dc0261d, c07d755, 9e9e454, aa82e79). Bu fayl — qisqa "hozir qayerdamiz"; batafsil tahlil new_channel_plan.md da.

XABARDORLIK: har tugagan ishdan keyin `docs/changes.md` ga bitta qator + push.
SKILLAR: har ish oldidan `docs/skills/INDEX.md` — Rocco uchun ham majburiy (ssenariy, QC, chiqarish, o'lchash bo'limlari).

TREND (2026-11-21, docs/trend_radar.md): GTA 6 shu hafta eng tez o'sayotgan mavzu — Rocco uchun "GTA 6 firibgarliklari: qizil bayroqlar" Shorti 48 soat ichida (rasmiy ogohlantirish manbasi bilan; hujum usuli ko'rsatilmaydi).

## 1. HOLAT
| Narsa | Holat |
|---|---|
| Instagram | @redfrocco — Shohjahon 2026-11-22 qo'shdi (vidIQ'da manual, joylash uchun OAuth kerak). To'plam: docs/instagram_redfrocco.md, assets/instagram/redfrocco/ |
| Kanal | OCHILDI 2026-11-21 13:13 — "Red Flag Rocco", @RedFrocco, https://www.youtube.com/@RedFrocco |
| Avatar / banner / tavsif | QO'YILDI 2026-11-21 18:45 (chat sessiyasi, Shohjahon Chrome'i orqali YouTube Studio): avatar_800.png, banner_2560x1440.png, channel_description.txt. Ommaviy sahifada tavsif ko'rinadi |
| Izohlar | YOQILGAN (Studio → Настройки → Модерация сообщества: "Комментарии: Включены", moderatsiya "Базовая") — tekshirildi 2026-11-21 18:46 |
| Kanal kalit so'zlari / auditoriya | 2026-11-21 18:47: "velox" olib tashlandi; qo'yildi: scam alerts, how to spot a scam, scam red flags, phishing text, fraud prevention, online safety, protect parents from scams, scam awareness, text message scams, phone scams. Auditoriya: "kanal bolalar uchun emas" |
| Akkaunt | Kanal velox.int.logistics@gmail.com Google akkauntida (Chrome'da kirilgan). Studio'da "Страна проживания" = AQSh deb turibdi — chat o'zgartirmadi; haqiqiy yashash davlati bo'lishi kerak (Shohjahon qarori) |
| Post qilish vositasi | Buffer (bepul) ulandi 2026-11-21; env BUFFER_API_KEY; api.buffer.com ochiq; engine/buffer_post.py — draft sinovi o'tdi va o'chirildi |
| Rocco ovozi (ElevenLabs) | YARATILDI 2026-11-21: "Rocco (Scam Detective)", voice_id `eYibgGvZyWzJUi8HBmQM` (Voice Design eleven_ttv_v3, 3 previewdan F0 diapazoni eng kengi; iliq, xotirjam, quruq hazil; median F0 ~182 Hz — Buck D ~259 Hz dan aniq farqli). Namuna: work/rocco/voice_lab/out/Rocco_R_sample.mp3; ASR tekshiruvi — matn to'g'ri eshitildi. Skript: work/rocco/voice_lab/rocco_voice_lab.py (qayta ishga tushsa yangi ovoz yaratmaydi). TTS sozlamasi Buck bilan bir xil (multilingual_v2, stability 0.28, style 0.85) |
| vidIQ | ULANDI 2026-11-21 (alohida vidIQ profili, Free, 150 kredit, yangilanish 2026-12-21; kanal UCUyPbjsSFdWKnC4nVRDhOiA). Kalit env VIDIQ_API_KEY; `python3 -I engine/vidiq_rocco.py <tool> '<json args>'` (sessiyadagi tayyor vidIQ vositalari — Financier profili, Rocco uchun ISHLATILMAYDI) |
| Chiqqan / rejalashtirilgan video | 1 — r01 brushing (Buffer 6b01befd142c957519268046, 2026-11-21 22:00 UTC / 17:00 ET) |

## 1.5 MAQSAD VA QARORLAR (Shohjahon, 2026-11-21 19:xx)
- MAQSAD: 1 hafta ichida 15 mln ko'rish. Claude'ning baholashi (Shohjahonga aytildi): yangi kanal uchun real emas, kafolatlanmaydi; sun'iy oshirish (bot, sotib olish) TAQIQ. Shunga qaramay eng yuqori ehtimolli yo'l bilan ishlanadi: shu hafta Black Friday / Cyber Monday xarid firibgarliklari, kuniga 3–4 Short, "ota-onangga yubor" ulashish uslubi, har kuni Rocco vidIQ tahlili va moslashuv. Har kuni haqiqiy raqam yoziladi.
- ElevenLabs: Financier uzun videosi haftasiga 2 taga tushirildi (producer_task) — bo'shagan belgi Rocco ovoziga. Rocco ovozi va videolari BOSHLANADI.
- KANAL SOZLAMALARI: Shohjahon — "o'zing sozla". → BAJARILDI 2026-11-21 18:45 chat sessiyasida (Chrome orqali, 1-jadval). Saboq: brauzer ishi vazifa sessiyasida yo'q — docs/night_order.md ga "CHAT UCHUN" buyurtma yoziladi (INDEX G). Shohjahon 2026-11-21: "menga ish qildirma" → bu haqda QAYTA SO'RALMAYDI; kanal tavsifi o'rniga har video tavsifida 1 qator kanal haqida ("Rocco spots scams so you don't fall for them").
- vidIQ eslatma: get_channels_by_ids 5 kredit oladi (bepul emas).

## 2. QABUL QILINGAN QARORLAR
- NISHA (2026-11-21, Shohjahon: "boshla — nishani o'zing top"): A — firibgarlikdan himoya / raqamli xavfsizlik, AQSh kattalari. Rad etildi: B "qanday ishlaydi" (AI-klonlar ko'p, tibbiy kadr xavfi), C psixologiya faktlari (b-roll asosan odamlar — shartga zid).
- NOM: "Red Flag Rocco" (@RedFrocco).
- PERSONAJ: Rocco — yenot-detektiv (sobiq "niqobli o'g'ri" endi firibgarlarni ushlaydi). Buck'dan butunlay farqli; Financier'da bir martalik mehmon kesishuvi mumkin.
- POST: Buffer (bepul). Metricool ikkinchi brendi pullik — yo'q.
- vidIQ: Rocco — o'z profili va o'z kreditlari (Financier krediti Rocco'ga sarflanmaydi). Kredit tartibi Financier'dagidek (producer_task 3-band), lekin Rocco hisobidan.
- isAiGenerated false (Rocco — to'qima multfilm, "realistik o'zgartirilgan kontent" emas); kategoriya 27 Education; madeForKids false.
- JADVAL: boshida kuniga 1 Short (2 hafta), natijaga qarab 2. Financier ustuvor.

## 3. MAJBURIY QOIDALAR (Shohjahon, 2026-11-21 13:2x)
- Behayo kontent yo'q; musiqa yo'q (ovoz + sintez sfx); ochiq kiyimdagi ayollar yo'q. ODATIY kiyimdagi odamlar lavhada RUXSAT (Shohjahon 2026-11-21 20:37 aniqlik kiritdi; avvalgi "odamli b-roll umuman yo'q" talqini bekor) — qoida: producer_task "LAVHADA ODAMLAR"; har klip kadr-kadr ko'riladi; tanib bo'ladigan yaqin yuz "firibgar/jabrlanuvchi" rolida ko'rsatilmaydi.
- Financier'ning QAT'IY CHEGARALARI (producer_task) to'liq: manbali fakt, real odam yuzi/ovozi yo'q, begona kontent yo'q, maslahat emas.
- "FOYDALI BO'LSIN": har Short — bitta aniq himoya qadami rasmiy manbadan (FTC, FBI IC3, CFPB, AARP), tavsifda manba. Render oldidan: "tomoshabin ertaga o'zini/ota-onasini qanday himoya qiladi?" — bir jumlada javob bo'lmasa, chiqmaydi.
- Ohang xotirjam va hazilli, panika thumbnail yo'q, aldangan odam masxara qilinmaydi; tabiiy ulashish chaqiruvi ("Send this to someone who still answers unknown numbers").
- Hujum usuli, skript, "qanday aldash" tafsiloti HECH QACHON — faqat belgilar va himoya. Ekrandagi soxta xabarlarda real brend logotipi yo'q.

## 4. FORMAT VA KONTENT REJASI
- Short 25–35 s: soxta (umumiy) xabar/qo'ng'iroq ekranda → "RED FLAG #1/#2/#3" → to'g'ri harakat (FTC/FBI) → izoh savoli "Have you gotten this one?" → loop. Reyting formati (5–7 bayroq, aralash tartib) ham sinaladi.
- Vizual: engine/make_video.py + yangi theme; telefon ekrani mock-up'lari o'zimiz chizamiz. Ovoz: ElevenLabs'da YANGI ovoz (Buck emas); sfx — qizil bayroq signali, qulf, xabar ovozi.
- Birinchi 10 mavzu (raqamlar render oldidan joriy rasmiy manbadan): 1 paket yetkazilmadi SMS; 2 "Grandma, it's me" ovoz klonlash; 3 toll-to'lov SMS (FBI IC3); 4 gift card bilan to'lov = firibgarlik; 5 "account locked" bank xabari; 6 "task scam" ish taklifi; 7 romance/pig butchering (faqat belgilar); 8 parkovkadagi QR stikerlar; 9 texnik yordam pop-up; 10 soxta qaytarim xabari.

## 5. BUFFER BILAN ISHLASH
- `python3 -I engine/buffer_post.py channels | list | delete <id>`
- `python3 -I engine/buffer_post.py schedule --video <raw url> --title "..." --text desc.txt --at <UTC ISO> [--draft]`
- Cheklovlar (bepul): 3 kanal, bir vaqtda 10 tagacha rejalashtirilgan post, tavsifga #PoweredByBuffer qo'shiladi, Shorts thumbnail yo'q. Kalit hech qayerga yozilmaydi/chiqarilmaydi.

## 6. OCHIQ — SHOHJAHON QARORI KERAK
1. ~~Avatar, banner, tavsif, izohlar~~ — BAJARILDI 2026-11-21 (chat). Qolgani: "Страна проживания" AQSh deb ko'rsatilgan — to'g'rilash yoki qoldirish Shohjahon qarori.
2. ElevenLabs limiti: "creator" 131,000 belgi/oy; Financier rejasi o'zi ≈138,000/oy (limitdan oshadi), Rocco +≈12,000/oy. Variantlar: (a) tarifni oshirish (to'lov — faqat Shohjahon); (b) uzun videoni haftasiga 2 taga tushirish; (c) TTS keshini sessiyalar orasida saqlash. QAROR 2026-11-21: (b) — Financier uzun videosi haftasiga 2 ta.

## 7. KEYINGI QADAMLAR (qarordan keyin)
Rocco ovozini yaratish (ElevenLabs voice design, bir marta) → yangi theme + telefon mock-up shabloni → 1-mavzu Short, QC (producer_task dagi barcha tekshiruvlar) → raw URL → buffer_post.py schedule → shu faylga "CHIQGAN VIDEOLAR" bo'limi.

## RENDER (Rocco) — 2026-11-21
- Personaj: `python3 -I work/rocco/rocco_sprites.py /tmp/fin_rocco_lib` (766 kadr, ~1 daq; chibi Rocco, 12 kayfiyat, og'iz t1–t3, flip/bonk/dodge) → `FIN_BUCK3D=/tmp/fin_rocco_lib python3 -I engine/make_video.py spec.json out.mp4 --model /tmp/kokoro/kokoro-v1.0.int8.onnx --voices /tmp/kokoro/voices-v1.0.bin`.
- Spec: "style": "rocco" (v6.12: case-file yorliq PASTDA, Courier Prime, qizil muhr stat, qora yorliqli subtitr, qizil progress, "phone" SMS ekran), "brand": "RED FLAG ROCCO", "brand_color": "#FF3B3B", "buck_voice": {"voice_id": "eYibgGvZyWzJUi8HBmQM", "label": "Rocco (Scam Detective)"}, theme noir (qizil fon YO'Q), bg_bright 1.25, bg_mix 0.8, bg_blur 2; sahnalarning ≥40% "broll" to'liq ekran (lavha sahnasida sarlavha chiqmaydi).
- QC: `engine/qc_gate.py ... --prev <oxirgi 4 video>` (look_check: Financier'dan ham farq qilsin).

## CHIQGAN VIDEOLAR
| # | Fayl | Sarlavha | Vaqt | Buffer id | Format / QC |
|---|---|---|---|---|---|
| r01 | rocco_2026-11-21_r01_brushing.mp4 (34.5 s) | 1 Free Box, 1 QR Code, 1 Big Red Flag | 2026-11-21 17:00 ET | 6b01befd142c957519268046 | hiyla ochildi + telefon (soxta QR sahifa); hook "Got a box you never ordered?" (hookscore 81.4); FTC 2026-08; qc_gate PASS (voice ok, prosody 0 bayroq, title 100, look 0.51–0.64 vs Financier); Skillar: hookscore, beats, title.py, qc_gate, color_check, look_check, Pixabay (Openly, flutie8211, magicmore, matlevesque) |

## KUNLIK RAQAMLAR
| sana (Toshkent) | obunachi | video | ko'rish | izoh |
|---|---|---|---|---|
| 2026-11-21 23:50 | 0 | 0 | 0 | hali video chiqmagan; r01 v2 Buffer 22:00 UTC (6b01e0a5…). Rocco vidIQ balansi 95/150 |
