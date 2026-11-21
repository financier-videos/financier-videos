# ROCCO USLUBI v2 — "yorug', kulgili, personaj oldinda" (chat Trade, 2026-11-22 01:50 Toshkent)
Shohjahon (T-04 Reel'ni ko'rib): "juda zerikarli, odamni o'zidan uzoqlashtiradi. Hazillar yo'q, yorug' va yoqimli ranglar yo'q, grafika va kadrlar yomon, ovozi ham jalb qilmaydi."
TASDIQLANDI (o'lchov, T-04): yorqinlik 0.21; 7 jumla — bitta ovoz, monolog, 1 hazil; Rocco 14 kadrdan 3 tasida va kichik; lavhalar — qora/kulrang abstrakt stok (qora ekran, kapyushonli "xaker" klishesi). Chat (Trade) buni "ancha yaxshi" deb xato baholagan — faqat xilma-xillikni o'lchagan, yoqimlilikni emas.
MAKET: docs/looks_samples/rocco_style_v2_mock.jpg (generator: work/rocco/style_v2_mock.py — Penny chizmasi va joylashuv shu yerda).

## QOIDA — Rocco videolari bundan keyin (eski "noir / case-file" uslubi TO'XTATILDI)
1. RANG: yorug' to'yingan fon — sahna bo'yicha almashadi: sariq (#FFD640) → firuza (#40C9C6) → yashil (#B2EC78) → pushti/binafsha; nuqtali (halftone) yoki nurli naqsh. Qora/kulrang fon YO'Q; yorqinlik (look_check luma) ≥0.50. Qizil — faqat bayroq va "RED FLAG" urg'usi.
2. PERSONAJ OLDINDA: Rocco kadrlarning ≥70% ida, kadr balandligining ≥1/3 i. Ikkinchi personaj — mijoz PENNY (pushti cho'chqa-kopilka: pulini asrashi kerak bo'lgan sodda do'st). Penny hayajonlanadi, Rocco sovuqqon. Penny sprite'lari: rocco_sprites.py uslubida (kayfiyatlar: happy, shock, sad, relieved, talk t1–t3) — kod chati; boshlang'ich chizma style_v2_mock.py da.
3. TUZILMA — doim SUHBAT (client_dialogue): Penny yangilik bilan kiradi → Rocco "Red flag." → Penny e'tiroz bildiradi (takroriy hazil) → Rocco bitta faktni ko'rsatadi → himoya qadami → quruq yakun. Monolog YO'Q.
4. HAZIL: har 4–6 s da (docs/comedy.md): takroriy hazil, Penny'ning bo'rttirilgan reaksiyasi, Rocco deadpan/shrug/doubletake harakatlari, kulgili tovush (boing, sirpanish, kassa). Jabrlanuvchi ustidan kulinmaydi — kulgi firibgarning bema'ni talabi ustidan.
5. GRAFIKA — o'z multfilm buyumlarimiz (stok emas): katta telefon va xabar pufakchalari, "HA/YO'Q" kartochkalari, muhr, tuzoq (sichqon qopqoni), kattalashtiruvchi oyna, himoya qadami kartasi (yashil belgi). Stok lavha ko'pi bilan 1–2 ta va yorqin bo'lsa. Shrift: Lilita One (OFL, assets/fonts) — yumaloq, do'stona; Courier/stencil yo'q.
6. SUBTITR: 1–3 so'z, oq + sariq urg'u, qalin qora kontur, pastki uchdan birda.
7. OVOZ: hozirgi Rocco ovozi (voice_id eYibgGvZyWzJUi8HBmQM) ALMASHTIRILADI. Kod chati: 4 nomzod ovoz (iliq, quvnoq, biroz "detektiv" ohangli; real shaxs nusxasi emas) + Penny uchun 2 nomzod (yuqoriroq, hayajonli) bilan BIR XIL 10 soniyalik matnni yozib, bitta "rocco_voice_test.mp4" qilsin (A/B/C/D yorliqlari ekranda) — Shohjahon eshitib tanlaydi. Tanlanguncha yangi Rocco videosi CHIQMAYDI.
8. BIRINCHI VIDEO (uslub sinovi): T-04 shu uslubda qayta — ssenariy:
   Penny: "Rocco! Free GTA Six! For PC!" — Rocco: "Red flag." — Penny: "But it's FREE." — Rocco: "Red flag." — Penny: "It says 'tonight only'!" — Rocco: "Two red flags." | Rocco: "It's on PlayStation and Xbox. There is no PC version." — Penny: "...So what am I downloading?" — Rocco: "A very bad week." | Rocco: "Your move: buy it only in the console store." — Penny: "And the free one?" — Rocco (deadpan): "Free cheese. Mousetrap." Manbalar: Rockstar (platformalar); McAfee, NordVPN, Malwarebytes ogohlantirishlari.
9. Tekshiruv: look_check luma ≥0.50; Rocco kadr ulushi ≥70%; hazillar soni; script_check PASS. Instagram'dagi eski T-04 Reel yangi versiya chiqqach arxivlanadi (o'chirish — Shohjahon qarori).

## NEGA BOSHQALARNIKI PORTLAYDI — tahlil (2026-11-22 02:00; vidIQ: 2 outlier qidiruv, Instagram/TikTok outlier, 2 ta kadrma-kadr "watch"; ~45 kredit). Uslub olinadi, matn/kadr ko'chirilmaydi.
| G'olib | Raqam | Nima uchun ishlaydi |
|---|---|---|
| "Scam Call (cat memes)" — animatsion mushuklar | 391K obunachi → 4.9M, 58 s | FIRIBGAR — AHMOQ, nishon — AQLLI: bola qo'ng'iroqni ataylab ko'tarib, firibgarni laqillatadi. ~8 hazil / 58 s: til sirg'alishi ("I can scam you— save you"), yolg'on ism, hisob raqami deb haqoratni yozdirish (reversal), absurd yakun. Yorug' xonalar, plan almashinuvi har 1–2 s, har replikaga subtitr |
| "Don't Fall For This Scam" — ikki rol (sodda do'st / biladigan do'st) | 46K → 2.2M, 66 s | 1-soniyada VOQEA: "Menga kimdir $1 000 yubordi!"; BASHORAT: "hozir 'adashib yubordim' deb yozadi" → *ding* — aynan shunday bo'ladi; ANIQ ZARAR HISOBI (−$1 000 + qaytarilgan $1 000); 3 qadamli maslahat; "buni kerakli odamga yubor". Yorug' oshxona, emoji va 1–3 so'zli subtitr |
| @dadthelawyer — AI ovoz firibgarligi | 96K → 24M (1070x) | Video firibgarlikning O'ZI bilan boshlanadi ("DAUGHTER: Dad!") — tushuntirish keyin; bitta oddiy himoya (oila uchun maxfiy so'z) |
| 3D animatsiya "IF YOU SEE A BABY FLYING" | 8K → 607K, 26 s | "Agar X ni ko'rsang..." hook; g'alati aniq tasvir; loop |
| "Buyer About to Reset Seller's Phone" | 38K → 4.2M, 20 s | firibgarlik amalda, 20 soniya |
BIZNING T-04 da NIMA YO'Q EDI: voqea o'rniga hikoyachi ("Someone's offering..."), personajlar o'rtasida to'qnashuv yo'q, firibgar personaj yo'q, bashorat/burilish yo'q, zarar hisobi yo'q, hazil 1 ta, qorong'i.

## ROCCO FORMULASI (bundan keyin faqat shu 4 formatdan; ketma-ket ikkitasi bir xil emas)
Uchinchi personaj: FIRIBGAR "SLICK" — kulgili, omadsiz tulki (yoki kalamush) telefon/ekran ichida; hech qachon qo'rqinchli emas, doim yutqazadi. Sprite — kod chati (rocco_sprites uslubi), ovozi — bo'g'iq, shoshgan.
1. SCAM-BAIT (45–60 s): Slick qo'ng'iroq qiladi → Rocco sovuqqonlik bilan uni chalg'itadi (takroriy hazil) → Slick o'zi o'zini fosh qiladi → Rocco kameraga 1 jumla himoya: "Siz esa — shunchaki go'shakni qo'ying." (Rasmiy maslahat: firibgar bilan gaplashmaslik — shuni AYTAMIZ; Rocco "mutaxassis" sifatida hazil qiladi.)
2. BASHORAT (40–55 s): Penny xushxabar bilan keladi → Rocco: "Hozir u ... deydi" → *ding* → Penny: "QANDAY?!" → zarar hisobi ekranda (−$… ) → 3 qadam → "buni buvingga yubor".
3. "AGAR ... KO'RSANG" (12–20 s, mikro): bitta g'alati aniq belgi + bitta harakat. Loop.
4. FIRIBGARLIKNING O'ZI BILAN BOSHLANADI (25–40 s): 1-kadr — xabar/qo'ng'iroq ekranda (Slick ovozi), Penny javob bermoqchi → Rocco qo'lini ushlaydi → 1 oddiy himoya.
HAR VIDEODA: hazil ≥1 har 6 s da; firibgar — ahmoq, jabrlanuvchi — hech qachon kulgi emas; yorqinlik ≥0.50; plan almashinuvi ≤2 s; oxirgi kadrda himoya qadami KATTA yozuv bilan + "Send this to someone who'd pick up."
ETALON KARTASI (majburiy, playbook yozuvida): qaysi g'olibga qiyoslab yasaldi; hook turi; hazillar soni; yorqinlik; personaj kadr ulushi; kesim tempi — g'olibnikidan past bo'lsa CHIQMAYDI.

## SSENARIYLAR (yozdi: chat Trade; faktlarni render oldidan rasmiy manbadan qayta tekshir)
### [TAYYOR] RC-01 SCAM-BAIT · ~55 s · "Scammer Calls a Detective. Big Mistake."
Manba (himoya qadami): FTC — bank hech qachon "pulni himoya qilish uchun boshqa hisobga o'tkazing" demaydi; go'shakni qo'yib, kartangiz orqasidagi raqamga o'zingiz qo'ng'iroq qiling (consumer.ftc.gov, impostor scams).
Slick: "Hello! This is Brenda. From your bank." — Rocco: "Which bank?" — "...Yours." — "Name it." — "The... big one. With the money." — Penny (shivirlab): "Ooh, I have that one!" — Rocco: "Shh." | Slick: "Sir, there's fraud on your account. I can steal— SECURE it. Just move your money to a safe account." — Rocco: "Sure. Write down my account number." — "Ready!" — "R. E. D." — "Mm-hm." — "F. L. A. G." — "...Red flag?" — Rocco: "Read it again. Slowly." — *go'shak qo'yiladi* | Penny: "Aww. I liked Brenda." — Rocco (kameraga, deadpan): "Real banks never ask you to move money. You? Just hang up. Call the number on your card."
Takroriy hazil: Slick bank nomini ayta olmaydi. Harakatlar: Rocco deadpan ×2, shrug; Penny doubletake; Slick jawdrop. Yakun yozuvi: "HANG UP. CALL THE NUMBER ON YOUR CARD."
### [TAYYOR] RC-02 BASHORAT · ~45 s · "Someone Sent You $1,000 'By Mistake'" (V-05 o'rniga)
Manba: FTC (payment apps: report to the app); National Cybersecurity Alliance — "accidental deposit" firibgarligi.
Penny: "ROCCO! A stranger sent me a thousand dollars!" — Rocco: "Don't touch it. In five seconds he'll say it was a mistake." — *ding* — Penny (o'qiydi): "'Oops, wrong person, please send it back'... HOW?!" — Rocco: "Detective." — Penny: "So I send it back. I'm NICE." — Rocco: "That money can be stolen. It gets pulled back later. And the thousand YOU sent?" — ekranda: −$1,000 — Penny: "...is gone?" — Rocco: "Gone." | "Your move: don't send anything. Report it in the app. Let the app reverse it." — Penny: "And if he begs?" — Rocco: "A real mistake can wait. A scammer can't." Yakun: "Send this to the nicest person you know."
### [TAYYOR] RC-03 "AGAR KO'RSANG" (mikro) · ~15 s · "If There's a QR Code in a Box You Never Ordered"
Manba: FTC "brushing" ogohlantirishi (2026-08). 1-kadr: quti ochiladi, ichida faqat QR kod. Rocco: "A box you never ordered. Inside: just a QR code." — Penny telefon ko'taradi — Rocco panjasi bilan to'sadi: "Don't scan it. Keep the box. Change your shopping passwords." Loop: quti yana ochiladi.
### [TAYYOR] RC-04 BASHORAT · ~40 s · "Free GTA 6 for PC" (T-04 o'rniga) — yuqoridagi 8-banddagi suhbat + boshida Slick'ning xabari ekranda ("FREE GTA 6 PC — tonight only!!!") va oxirida "Free cheese. Mousetrap." + sichqon qopqoni gagi.
