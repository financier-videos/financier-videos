# BUCK — kanal personaji (Financier Money Facts)
Yangilangan: 2026-11-20 01:15 (GitHub'ga ko'chirildi — asosiy nusxa shu fayl). Har bir YouTube agent videoni rejalashtirishdan oldin o'qiydi.

## 1. Kim u
- Buck — oltin tanga, kanalning O'Z personaji. Tagline: "Buck — the bravest coin in your wallet."
- KO'RINISH (2026-11-20 dan; o'zgarmas brend belgilari): 24k oltin tanga — qalin qirra, tishli chekka, gulli o'ymakor hoshiya; yuz ostida bo'rtma "$"; o'ng tepada biroz qiyshaygan qora baxmal silindr shlyapa — tilla tasma, tasmaga qistirilgan yashil dollar; o'ng ko'zida oltin zanjirli monokl; katta yaltiroq ko'zlar, qalin to'q jigarrang qoshlar, jonli og'iz; oltin qo'l-oyoqlar; oq multfilm qo'lqoplari; qizil-oltin krossovkalar. Kapalak galstuk va yashil krossovka ENDI YO'Q.
- 3D: v4 GIBRID — Shohjahonning Tripo modeli (pullik tarif, tijorat huquqi) tanasi + kod bilan qurilgan jonli yuz (shape key og'iz, qovoqlar, monokl + zanjir) + naycha qo'l-oyoqlar. Kod: engine/buck3d.py. Model fayli MAXFIY — repoga qo'yilmaydi; kutubxona faqat Shohjahonning chatida render qilinadi → assets/buck3d_v2.tar (226 kadr, 15 fps: 12 kayfiyat + flip/bonk/dodge).
- BUCK — YAGONA HIKOYACHI VA AKTYOR: alohida hikoyachi YO'Q. U birinchi shaxsda gapiradi, o'zi savol beradi, o'zi hayron bo'ladi, o'zi javob topadi. U "moliyaviy ekspert" emas: maslahat bermaydi, faktni manbasi bilan aytadi.

## 2. Ovozi
- Faqat ElevenLabs'da O'ZIMIZ yaratgan ovoz: Voice Design, ARXETIP tavsifidan (klon emas, real odam ovozi/nomi yo'q, Voice Library emas).
- 3 variant (work/voice_lab/buck_voice_lab.py): A "Buck A (Trickster)" — ekssentrik teatral ayyor; B "Buck B (Adventurer)" — tez gapiradigan energik sarguzashtchi; C "Buck C (Con-Artist)" — silliq, kinoyali animatsion qahramon. Shohjahon tanlaydi; tanlaguncha A. Spec: "buck_voice": {"variant": "A|B|C"}.
- voice_id lar (ovoz laboratoriyasi, 2026-11-20 01:40, eleven_ttv_v3 Voice Design; namunalar work/voice_lab/out/): A "Buck A (Trickster)" = eH342qEgJkje3sPOEo6z; B "Buck B (Adventurer)" = oNvWqVbCi5f9laSmwaf5; C "Buck C (Con-Artist)" = lLwZ4pIcnVhPAHqXFq5O.
- TTS: eleven_multilingual_v2; stability 0.28, similarity_boost 0.75, style 0.85, use_speaker_boost true.
- IJRO YOZUVI (Short'ga 2–4 ta): "...", "Whoa!", "Wait a second...", "Heh.", "Okay, okay...", "Hmm."; KATTA HARF bilan urg'u; savol–javob ritmi.
- ZAXIRA: Kokoro — faqat sinov. "buck_voice" "kokoro" bo'lsa video CHIQARILMAYDI.

## 3. Xarakteri (umumiy xislatlar, hech kimdan nusxa emas)
- "Boy janob" ko'rinishida, lekin mehribon va sodiq: tomoshabinning hamyonini "pul tuzoqlari"dan himoya qiladi; tomoshabin ustidan kulmaydi.
- Jasur, biroz omadsiz kaskadyor: tuzoqqa birinchi o'zi tushadi (narx yorlig'i shlyapasiga tushadi), har doim turib "I'm okay!" deydi.
- Maftunkor, o'ziga haddan ortiq ishongan ayyor: "Relax. I have a plan." — reja buziladi — "Planned that."
- Hazil faqat faktni tushuntiradigan ("related humor").

## 4. Iboralari
- O'ziga-o'zi dialog: "Is that a lot? ... Yeah. That's a lot." Uchlik: "Every day? ... Every minute? ... Every SECOND?!"
- Doimiy (videoda 1–3 ta, aylantirib): "I'm okay!"; "Relax. I have a plan." → "Planned that."; "Ow. Worth it."; "Not today, price tag!"; "Easy, wallet. I got you."; "That's not a discount. That's a costume."; "Money doesn't grow on trees. I checked."; "I'll start Monday."; "Did my own stunts." (bloopers).

## 5. Harakatlari (dvigatel "mascot": {"act": ...})
- roll_in, drop_in, flip, bonk (narx yorlig'i shlyapaga tushadi, yulduzchalar), dodge.
- Kayfiyatlar: happy, shocked (monokl otilib chiqib zanjirda osiladi), laugh, smug, confused, sideeye, sad, angry (yuz qizaradi), point, dizzy, thumbsup, proud.

## 6. Qoidalar va taqiqlar
- Buck ekranda sahnalarning ≥50% ida; har Short'da 1 tryuk, 1–3 ibora, 1 "beat". "center" — stat/chart yo'q sahnada; "corner" — stat/b-roll bilan. Buck raqam va subtitrni yopmasin.
- Running gag: narx yorlig'i — Buck'ning abadiy "dushmani". Buck faktni BUZMAYDI.
- Oila uchun: faqat multfilm slapstick; qurol, alkogol, qimor, behayo narsa yo'q.
- Real odamlarning yuzi/ismi/ovozi yo'q. Boshqa mashhur maskotlarning belgilari (hassa, getr va h.k.) QO'SHILMAYDI. Ko'rinishni o'zgartirma.
