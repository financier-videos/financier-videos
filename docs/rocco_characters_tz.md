# RED FLAG ROCCO — personajlar TZ (2D surat → 3D model)

Sana: 2026-11-22. Kim uchun: Shohjahon (avval surat, keyin 3D). Hozir serialda 3 ta personaj bor: **Rocco, Penny, Slick**.
Promptlar inglizcha — rasm generatoriga shu holicha qo'yiladi.

---

## 0. Uchala personajga umumiy talablar

**Uslub.** Yorug', do'stona 3D multfilm (oilaviy animatsiya filmi darajasi): yumshoq dumaloq shakllar, katta bosh, katta ko'zlar,
toza silliq material (yumshoq plastik/vinil o'yinchoq + ozgina mayin jun fakturasi), yumshoq studiya yorug'ligi. Qo'rqinchli, real, "noir" emas.

**Nisbat.** Bosh : tana ≈ 1 : 1.2 (bo'yi 2–2.5 "bosh"). Kalta oyoq-qo'l, 4 barmoqli yo'g'on panja (qo'lqopsimon). Siluet qora soyada ham taniladigan bo'lsin.

**Uchovi yonma-yon turganda farqi:**

| | Rocco | Penny | Slick |
|---|---|---|---|
| Asosiy shakl | dumaloq + uchburchak quloq | to'liq shar | uzun uchburchak (tor, cho'ziq) |
| Asosiy rang | kulrang + jigarrang shlyapa + QIZIL | pushti | to'q sariq + binafsha |
| Bo'yi | 1.0 (etalon) | 0.75 | 1.15 (ozg'in, baland) |
| Fe'li | sovuqqon, kinoyali, mehribon | sodda, hayajonli | ayyor, shoshqaloq, omadsiz |

**3D ga o'tkazish uchun suratga talab (eng muhimi):**
- Bitta personaj, to'liq bo'y, boshdan oyoqqa kadrda, markazda; fon bir tekis och kulrang yoki oq; yerda faqat yumshoq soya.
- **A-poza**: qo'llar tanadan ~35° ochiq, oyoqlar bir oz kerilgan, barmoqlar ajratilgan. Qo'l tanaga, dum oyoqqa yopishmasin.
- Neytral yuz: og'iz yopiq, yengil tabassum, ko'zlar to'g'riga qaragan (ifodalar keyin rigda qilinadi).
- Qo'lda hech narsa yo'q. Buyumlar (bayroq, lupa, telefon) — ALOHIDA suratlar va alohida modellar.
- Simmetrik old ko'rinish + alohida: yon (90°), orqa, 3/4 ko'rinishlar (turnaround varaq).
- Ingichka, osilib turgan, shaffof detal yo'q (uzun mo'ylov, ip, tutun, shisha — yo'q). Mo'ylov = 2–3 ta yo'g'on kalta "tayoqcha" yoki umuman yo'q.
- Suratda yozuv, logo, suv belgisi, ramka yo'q. Kiyimda ham yozuv yo'q.
- O'lcham ≥ 2048 px, kvadrat yoki 3:4.

**Taqiq (mualliflik huquqi).** Hech bir mavjud personajga o'xshamasin — mashhur multfilm/o'yin yenoti, tulkisi, cho'chqasi yoki
kopilkasi nusxasi emas. Promptga personaj/film/studiya nomi YOZILMAYDI. Real odam yuzi yo'q. Qurol yo'q.

**Har bir personaj uchun 2 ta surat kerak:** (A) "chiroyli" reklama surati — xarakterli poza, kanal muqovasi uchun;
(B) 3D uchun A-poza turnaround. Avval (A) ni tasdiqlaymiz, keyin o'sha ko'rinishdan (B).

**Umumiy prompt qo'shimchasi (har promptning oxiriga):**
`stylized 3D cartoon character, family animated feature film quality, soft rounded shapes, big expressive eyes, smooth clean materials with subtle soft fur, soft studio lighting, gentle rim light, plain light grey seamless background, soft contact shadow, full body, centered, high detail, 4-finger mitten hands, original character design, no text, no logo, no watermark`

**Umumiy negative prompt:**
`realistic, photoreal, scary, creepy, dark, noir, gritty, human face, weapon, text, letters, logo, watermark, extra limbs, extra fingers, thin whiskers, transparent parts, glass, smoke, busy background, cropped, cut off feet, multiple characters, existing cartoon character`

---

## 1. ROCCO — bosh qahramon, "firibgarlik detektivi"

**Kim.** Yenot-detektiv. Hamma narsani ko'rgan, hech narsaga hayron bo'lmaydi; firibgarni bir qarashda taniydi va bitta
quruq gap bilan fosh qiladi ("Red flag."). Sovuqqon va kinoyali, lekin Penny'ga mehribon akadek. Hech qachon jabrlanuvchi ustidan kulmaydi.
Ovozi: iliq, ayyorona, biroz xirildoq.

**Ko'rinishi (hozirgi avatar bilan uzviy — tanilishi saqlansin):**
- Tur: yenot. Bosh katta, dumaloq, yonoqlari to'la. Quloqlar uchburchak, ichi och pushti.
- Ko'z atrofida **qora "niqob"** (yenot belgisi) — detektiv niqobiga o'xshab ketadi, bu uning asosiy belgisi. Ko'zlar katta, oq, qorachig'i to'q jigarrang, yuqori qovoq yarim tushgan (deadpan qarash uchun).
- Tumshuq oq-krem, burun qora, kichik. Qoshlar — niqob ustida och kulrang yo'g'on chiziq (ifoda uchun muhim).
- Jun: asosiy kulrang, qorin va tumshuq krem. **Dum: yo'g'on, kalta, 4–5 ta qora-kulrang halqali** (yuqoriga qayrilgan, tanadan ajralgan).
- **Shlyapa:** jigarrang detektiv shlyapasi (kalta soyabonli fedora), atrofida **qizil lenta**. Shlyapa quloqlar orasida o'tiradi, quloqlar ko'rinib turadi.
- **Kiyim:** och qum rang (bej) kalta plashch (trench), yoqasi ko'tarilgan, 2 qator to'q tugma, belbog'. Ichida ko'rinsa — qizil galstuk yoki qizil bo'yinbog'. Shim yo'q (multfilm an'anasi), oyoqlar kulrang, panjalar to'qroq.
- Bo'yi: 2.3 "bosh". Gavda nok shaklida, yelka tor, qorin biroz chiqqan.

**Ranglar:** jun `#8E97A3`, to'q jun/halqa `#2B2F36`, krem `#F3EFE7`, niqob `#23262D`, shlyapa `#8A6A45`, lenta va urg'u `#FF3B3B`, plashch `#D9BE8F`, tugma `#5A4632`, quloq ichi `#F1D3CC`, ko'z `#3A2414`.

**Buyumlari (alohida modellar):** 1) **qizil bayroqcha** kalta yog'och dastada (asosiy belgi; `#FF3B3B`, dastasi `#D9B77A`); 2) lupa (shishasiz — faqat halqa va dasta, 3D uchun); 3) kichik bloknot.

**Kerakli ifodalar (rig/blendshape):** neytral, deadpan (yarim yumuq ko'z), bitta qosh ko'tarilgan (shubha), yengil kulgi, hayrat (ko'z katta), ko'z qisish, xo'rsinish; gapirish uchun og'iz: yopiq, yarim ochiq, ochiq, "O", "E".
**Harakatlar:** bayroq ko'tarish, panja bilan to'xtatish ("stop"), yelka qisish, barmoq bilan ko'rsatish, shlyapani tuzatish, qo'l qovushtirish.

**Prompt A (reklama surati):**
`A charming raccoon detective mascot standing confidently with one eyebrow raised and a knowing half-smile, holding up a small bright red flag on a short wooden stick in one paw, the other paw on his hip. Big round head, chubby cheeks, classic black raccoon eye-mask marking, large white eyes with dark brown pupils and half-lowered upper lids, cream muzzle, small black nose, triangular ears with pale pink insides. Grey fur, cream belly, thick short tail with black rings curled up behind him. Wearing a brown short-brim detective fedora with a red band, and a short sand-beige trench coat with a popped collar, double row of dark buttons and a belt, small red necktie. Short legs, chunky paws.` + umumiy qo'shimcha

**Prompt B (3D uchun):**
`Character turnaround sheet of the same raccoon detective: front view, side view, back view and three-quarter view, A-pose with arms held 35 degrees away from the body and legs slightly apart, fingers separated, empty hands, neutral face with closed mouth and a slight smile, eyes looking straight ahead, tail clearly separated from the legs, hat on, trench coat closed, perfectly symmetrical front view, orthographic look, even flat lighting.` + umumiy qo'shimcha

---

## 2. PENNY — mijoz va do'st, "pulini asrashi kerak bo'lgan sodda"

**Kim.** Tirik cho'chqa-kopilka. Har xabarga ishonadi, darrov hayajonlanadi ("Rocco! Rocco! FREE!"), keyin qo'rqib ketadi.
Tomoshabin o'zini unda ko'radi — shuning uchun yoqimli, ahmoq emas: shunchaki ishonuvchan va mehribon. Ovozi: baland, shodon, tez.

**Ko'rinishi:**
- Tur: cho'chqacha-kopilka (jonli, lekin kopilka belgilari bor). **Tana — deyarli to'liq shar**, bosh va tana bitta hajm (bosh alohida emas).
- Orqa ustida **tanga tirqishi** (qora kalta yo'lak) — asosiy belgi. Qorin ostida kopilka "tiqini" (kichik dumaloq, to'qroq pushti) — ixtiyoriy.
- Quloqlar: kichik uchburchak, oldinga egilgan, ichi to'q pushti. Tumshuq: katta dumaloq "pyatachok", ikki burun teshigi.
- Ko'zlar juda katta, dumaloq, bir-biriga yaqin, qorachig'i katta va yaltiroq nuqtali; kipriklar 2–3 ta kalta yo'g'on. Yonoqlarda och pushti qizarish doiralari.
- Oyoqlar: 4 ta kalta yo'g'on "ustuncha", tuyoqlari to'qroq. Ikki oyoqda tik turadi: oldingi ikkitasi qo'l vazifasida (kalta, tuyoqli).
- Dum: bitta burama spiral, YO'G'ON (ingichka emas).
- **Aksessuar:** bo'ynida kichik sariq-tilla bantik yoki boshida kichik sariq gul/to'g'nag'ich (bitta tanlanadi; Rocco qizilidan farq qilsin).
- Material: silliq, biroz yaltiroq (sopol kopilka kabi), lekin yumshoq — ezilib-cho'zilishi mumkin.
- Bo'yi: Rocco bo'yining 0.75 qismi.

**Ranglar:** tana `#FF9EC0`, to'q pushti (quloq ichi, tuyoq, tumshuq cheti) `#E86A9A`, qizarish `#FFC2D6`, tirqish `#3A2430`, ko'z `#2A1B22`, bantik `#FFD640`.

**Buyumlari (alohida):** 1) telefon (umumiy, logosiz, och ko'k g'ilofda); 2) tilla tanga; 3) kichik sumkacha.

**Ifodalar:** shodon, hayajon (ko'z yulduzdek katta, og'iz ochiq), hayrat/"gasp", qo'rquv (ko'z katta, ter tomchisi), xafa, yengil tortish, uyalib kulish; og'iz shakllari — Rocco bilan bir xil to'plam.
**Harakatlar:** joyida sakrash, telefonni ko'tarib ko'rsatish, tuyoqlarini yonoqqa qo'yish, orqaga chayqalish, bosh irg'ash.

**Prompt A:**
`An adorable living piggy-bank character jumping with excitement, mouth open in a delighted gasp, holding up a generic smartphone in a pale blue case with one front hoof. Almost perfectly spherical glossy pink body where head and body are one round shape, a coin slot on the top of her back, small forward-folded triangular ears with darker pink insides, a big round snout with two nostrils, very large round sparkling eyes set close together with short thick lashes, soft blush circles on the cheeks, four short stubby legs with darker pink hooves, a thick curly spiral tail, a small golden-yellow bow at the neck. Smooth, slightly glossy ceramic-like but soft and squishy surface.` + umumiy qo'shimcha

**Prompt B:**
`Character turnaround sheet of the same piggy-bank character: front view, side view, back view, three-quarter view and a top view showing the coin slot, standing upright on two hind legs in an A-pose with the two short front legs held away from the body, empty hooves, neutral face with closed mouth and a small smile, eyes looking straight ahead, thick curly tail clearly visible and separated from the body, perfectly symmetrical front view, orthographic look, even flat lighting.` + umumiy qo'shimcha

---

## 3. SLICK — firibgar, "har doim yutqazadigan ayyor"

**Kim.** Tulki-firibgar. O'zini juda aqlli deb o'ylaydi, lekin har safar o'zi o'zini fosh qiladi ("Trust me! I'm a professional!").
Kulgili va omadsiz — hech qachon qo'rqinchli yoki xavfli ko'rinmaydi. Kulgi uning bema'ni talabi ustidan. Ovozi: shoshgan, shivirlovchi, tez.

**Ko'rinishi:**
- Tur: tulki. **Siluet tor va cho'ziq**: uzun uchburchak tumshuq, uzun o'tkir quloqlar (uchi qora), ingichka bo'yin, ozg'in gavda, uzun oyoqlar — Rocco va Penny dumaloqligiga qarama-qarshi.
- Ko'zlar: tor, yarim yumuq, **sariq**, qorachig'i kichik; qovoqlari og'ir ("ayyor" qarash). Qoshlar ingichka emas — yo'g'on, burchakli, harakatchan.
- Tabassum: bir tomonga qiyshaygan keng iljayish, bitta tish yaltirab turadi (ixtiyoriy, kulgili detal).
- Jun: to'q sariq, tumshuq pasti, yonoq va ko'krak oq-krem; panjalar to'q jigarrang ("qo'lqop"). Dum: katta, momiq, uchi oq (tanadan ajralgan).
- **Kiyim:** yaltiroq **binafsha kostyum** — yelkasi juda keng, yengi biroz uzun (o'ziga katta — arzon ko'rinsin), ichida oq ko'ylak, **qizil galstuk** qiyshiq bog'langan. Yoqasida sariq soxta "tilla" to'g'nag'ich (yozuvsiz dumaloq).
- Sochi: peshonasida orqaga silliq taralgan bir tutam (gel bilan).
- Bo'yi: Rocco'dan 1.15 baravar baland, lekin bukchayib turadi.

**Ranglar:** jun `#F28C28`, to'q jun/quloq uchi `#3A2A22`, krem `#FFF3E0`, ko'z `#FFD23F`, kostyum `#6C3FC4`, kostyum soyasi `#4B2A8F`, galstuk `#E23B3B`, ko'ylak `#F7F7F7`, to'g'nag'ich `#FFD640`.

**Buyumlari (alohida):** 1) **yashil telefon** (`#59D185`, logosiz — uning doimiy buyumi); 2) naushnik-garnitura (kol-markaz); 3) "sovg'a qutisi" (qizil lentali, ichi bo'sh); 4) soxta nishon (yozuvsiz).

**Ifodalar:** ayyor iljayish, shirin-soxta tabassum, shoshib ishontirish, sarosima (ko'z katta, quloq tushgan), "jawdrop" (jag'i osilgan), yig'lamsirash, terlash; og'iz shakllari — umumiy to'plam.
**Harakatlar:** telefonni quloqqa tutish, qo'l ishqalash, barmoq bilan chaqirish, galstuk tuzatish, orqaga tisarilish, boshini changallash.

**Prompt A:**
`A comically sly fox con-artist character leaning forward with a crooked overconfident grin, one paw rubbing his chin, the other holding a plain bright green smartphone. Tall, skinny and angular silhouette: long pointed triangular snout, long sharp ears with dark tips, thin neck, lanky legs. Narrow half-closed yellow eyes with heavy lids, thick angular eyebrows, one shiny tooth showing. Orange fur, cream lower muzzle, cheeks and chest, dark brown paws like gloves, a big fluffy tail with a white tip. Wearing a shiny purple suit that is a size too big with oversized shoulders and slightly long sleeves, a white shirt, a crooked red necktie and a plain round gold lapel pin, a slicked-back tuft of fur on his forehead. Funny and harmless, clearly a loser villain, not scary.` + umumiy qo'shimcha

**Prompt B:**
`Character turnaround sheet of the same fox con-artist: front view, side view, back view and three-quarter view, standing straight in an A-pose with arms held 35 degrees away from the body and legs slightly apart, fingers separated, empty hands, neutral face with closed mouth and a slight smirk, eyes looking straight ahead, fluffy tail clearly separated from the legs, suit jacket closed, perfectly symmetrical front view, orthographic look, even flat lighting.` + umumiy qo'shimcha

---

## 4. Qabul qilish ro'yxati (har surat uchun)

1. Kichraytirilgan holda (100 px) va qora siluetda ham kimligi tanilyaptimi?
2. Uchovi yonma-yon qo'yilganda rang va shakl bo'yicha aralashmayaptimi?
3. Mavjud mashhur personajni eslatmayaptimi? (eslatsa — qayta)
4. Rocco: niqob, qizil lentali shlyapa, halqali dum, plashch — to'rttasi ham bormi?
5. Penny: shar tana, orqada tirqish, sariq bantik bormi?
6. Slick: binafsha kostyum, qiyshiq qizil galstuk, sariq ko'z, tor siluet bormi? Qo'rqinchli emasmi?
7. B suratda: A-poza, qo'l-dum ajralgan, og'iz yopiq, qo'l bo'sh, fon toza, yozuv yo'q?
8. Barmoqlar soni to'g'ri (4), ortiqcha a'zo yo'q?

## 5. 3D bosqichi uchun (Tripo yoki shunga o'xshash)

- Kirish: B suratining faqat OLD ko'rinishi (toza kesilgan) + imkon bo'lsa yon va orqa (multi-view).
- Chiqish: GLB/FBX, to'rtburchak (quad) topologiya, ≤ 60 000 uchburchak, tekstura 2K (base color + normal + roughness).
- Ko'z, qovoq, qosh, og'iz ichi (til, tish) alohida mesh bo'lsa — ifodalar oson; bo'lmasa blendshape bilan.
- Skelet: gumanoid rig + dum (4–5 suyak) + quloqlar (har biriga 2 suyak); Penny uchun — squash/stretch suyagi va quloq/dum suyaklari.
- Buyumlar alohida fayl; qo'lga "socket" orqali biriktiriladi.
- Model va rig fayllari faqat yopiq repoda (`financier-videos/buck-private`), ochiq repoga qo'yilmaydi.
