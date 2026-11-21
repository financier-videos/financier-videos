# HAZIL VA AKTYORLIK (Shohjahon 2026-11-21 21:36: "hazillar-chi? hammasi komediyaga mos bo'ladimi? effektlar aktyorlik bilan o'xshatib chiqadimi?")
HOLAT (halol): hozirgacha Buck "aktyorlik" qilmagan — 12 kayfiyat pozasi + 3 harakat (flip, bonk, dodge). Hazil faqat matnda edi ("Heh...", so'z o'yini), tasvirda emas.
G'OLIBLARDA hazil qayerdan chiqadi (docs/lessons_winners_2026-11-21.md): VAZIYATDAN va REAKSIYADAN — kassir terlaydi va "tushlik qilmayman" deydi; cho'ntak multfilmdek shishadi; o'rgimchak to'ri bosgan kassa; xo'jayin velosipedda, kassir kabrioletda. So'z o'yini emas — ko'rsa bo'ladigan gag.

## QOIDA — har videoda (mikrodan tashqari)
1. KAMIDA 1 TA KO'RINADIGAN GAG (matnsiz ham kulgili): bo'rttirish (narsa haddan tashqari katta/ko'p/tez), kontrast (boy ↔ kambag'al yonma-yon), kutilmagan buyum, "jim kadr" (hamma to'xtaydi, chigirtka ovozi).
2. REAKSIYA KADRI: har kuchli raqam yoki burilishdan KEYIN 0.6–1.0 s Buck/Rocco reaksiyasi — yaqin plan, kadr balandligining ≥1/3. Reaksiya = harakat (pastdagi ro'yxat), poza emas.
3. TAYMING: hazildan oldin 0.3–0.5 s sukunat (musiqa/effekt to'xtaydi), keyin zarba. Hazildan keyin 0.5 s — tushunishga vaqt. Hazil ZICHLIGI formatga qarab (pastda 'HAZIL GAPLAR').
4. HARAKAT QOIDASI: tayyorlanish → harakat → davomi (siqilish–cho'zilish). Har harakatga O'Z TOVUSHI (boing, sirpanish, tanga, qo'ng'iroq, "bo'm").
5. PERSONAJ XARAKTERI: Buck — o'ziga ishongan, biroz maqtanchoq tanga; hazil ko'pincha uning o'ziga qaytadi (o'zi aldanadi, monokli tushib ketadi). Rocco — jiddiy detektiv, hazili quruq (deadpan); mijoz hayajonlanadi — Rocco kiprik qoqmaydi.
6. TAQIQ: odamlar ustidan kulish (millat, jins, yosh, tashqi ko'rinish), jabrlanuvchi ustidan kulish (Rocco!), so'kinish, behayo ishora. Fakt hazil uchun buzilmaydi — hazil faktning YONIDA.
7. Ssenariy jadvalida ustun: "gag" (qaysi sahna, qaysi tur) va "reaksiya" (qaysi harakat).

## BUCK HARAKATLARI (spec: sahna "mascot": {"act": "<nom>", "at": soniya})
| act | Nima | Qachon | Uzunlik |
|---|---|---|---|
| flip, bonk, dodge | (eski) salto; boshga zarba → gangish; chetlanish | xursandlik; "narx urdi"; tushayotgan narsa | 0.7 / 1.5 / 0.75 s |
| doubletake | chetga qarab turadi → to'xtaydi → keskin qaytib ko'zi chaqnaydi, shlyapa sakraydi | kutilmagan raqam ("...to'xta, QANCHA?") | 1.07 s |
| jawdrop | qotadi, og'zi ochilib qoladi, shlyapa otiladi, monokl tushadi | eng katta raqam / burilish | 1.07 s |
| shrug | ikki qo'l yonga, yelka qisadi, og'zi qiyshayadi | "kim biladi", bahsli fakt, "tarixchilar bahslashadi" | 0.93 s |
| sigh | yelkasi tushadi, ko'zini yumadi, shlyapa oldinga siljiydi, sekin bosh chayqaydi | ahmoqona to'lov, o'z xatosi | 1.2 s |
| deadpan | tomoshabinga tosh qotgan nigoh, bitta sekin kiprik qoqish | hazildan KEYINGI sukunat; "jiddiymi?" | 1.0 s |
Kutubxona: assets/buck3d_v3_acts.tar (800 px, 15 kadr/s, shaffof fon). Rocco uchun shu 5 harakatning 2D varianti — rocco_sprites.py ga qo'shilsin (kod chati).
Keyingi harakatlar navbati (rig tayyor): yashirincha mo'ralash (kadr chetidan), kulib yiqilish, pul sanash, qo'l bilan "to'xta", skipetr bilan ko'rsatish, yurib kirish/chiqish.

## HAZIL GAPLAR (2026-11-21 21:50; Shohjahon: "ko'proq hazil so'zlar va gaplar ishlatish ma'qul emasmi?" — HA; 2 ta kulgili g'olib transkripti o'qildi)
Dalil: ishga qabul suhbati skiti (3.4K obunachi → 990K, 63 s): tez savol–javob, HAR javob bitta so'zga qaytadi (takroriy hazil), har ~3 s da hazil; "kvartira qidirish" skiti (59.6K → 1.2M, 74 s): hammaga tanish bema'ni vaziyat (bu yerga ko'p topasan, u yerga kam), oxirida quruq bitta jumla. Matn ko'chirilmaydi — mexanika olinadi.
ZICHLIK:
- Fakt videolari (why_story, scale_ladder, ranking...): har 8–10 s da 1 kulgili gap yoki gag; 30 s da ≥3, 60 s da ≥5.
- Kulgili skit (yangi tuzilma `comedy_skit`, 35–60 s, Buck + ikkinchi ovoz): har 3–4 s da hazil; ichida 1–2 ta HAQIQIY raqam (manbali) — hazil faktning yonida.
HAZIL TURLARI (har videoda kamida 2 xil):
1. TAKRORIY HAZIL (running gag): bitta so'z/ibora 3+ marta qaytadi, har safar yangi ma'noda; oxirgisi burilish.
2. TEZ SAVOL–JAVOB: savol uzun, javob 1–3 so'z.
3. TANISH JAHL: tomoshabin "bu men!" deydigan vaziyat (bankomat to'lovi, choychaqa ekrani, obunani bekor qilish labirinti, "bepul" yetkazish).
4. QURUQ YAKUN (deadpan): eng oxirida sokin bitta jumla + Buck "deadpan" harakati.
5. BO'RTTIRISH: raqamni kulgili taqqoslash ("bu pulga 4 ta xot-dog... yoki bitta aeroport suvi").
6. O'ZIGA QAYTGAN HAZIL: Buck maqtanadi → darhol o'zi tushib qoladi.
Buck iboralari (takrorlanib brend bo'ladi, lekin har videoda emas): "Heh." · "I'm a coin. I'd know." · "Asking for a friend. The friend is me."
TAQIQ (o'zgarmaydi): odamlar/guruhlar ustidan kulish, jabrlanuvchi ustidan kulish, so'kinish, behayo ishora, faktni hazil uchun buzish. Hazil faktdek eshitilmasin — bahsli joyda ekranda "joke" / "Buck's theory".
O'LCHOV: har videoda "hazillar soni" playbook yozuviga; 72 soatda kulgili skit va fakt videosi ko'rishlari solishtiriladi.
