# O'SISH JURNALI — "har kuni kechagidan yaxshiroq" (Shohjahon, 2026-11-20 07:07)
Har kuni KAMIDA bitta yozuv. Format: sana — O'RGANILDI (manba, sana) → O'ZGARTIRILDI (qaysi fayl/qoida) → O'LCHOV (ertaga nimaga qarab bilamiz). Taxmin va manbasiz "benchmark" yozilmaydi. A rejim har ish boshida oxirgi 5 yozuvni o'qib amal qiladi. 60 qatordan oshsa eng eskilarini 1 qatorlik xulosaga aylantir.

## 2026-11-20 (chat sessiyasi)
1. O'RGANILDI: YouTube 2026-10-01 da Shorts tavsiya tizimi original kontentga ustunlik berishini, boshqalarning videosini deyarli o'zgartirmay qayta yuklaydigan kanallar kam tarqatilishini e'lon qildi (ppc.land; MediaPost). "Shablon asosidagi kichik o'zgarishlar" originallik hisoblanmaydi.
   O'ZGARTIRILDI: bizga to'g'ridan tegmaydi (hammasi o'zimizniki), lekin b-roll ulushi past bo'lsin: Short'da ≤1 b-roll sahna, ≤4 s.
2. O'RGANILDI: YouTube 2026-07 da "inauthentic content" monetizatsiya qoidasini 3 toifaga ajratib tushuntirdi (Tubefilter 2026-07-13; TechCrunch 2026-07-20): (a) umumiy/takroriy/shablon kontent — ketma-ket ko'rganda bir xil tuyuladigan, kam izohli videolar; (b) yoqimsiz/aldamchi kontent; (c) AI personaj inson EKSPERT sifatida sog'liq, huquq, MOLIYA, siyosat bo'yicha MASLAHAT bersa.
   O'ZGARTIRILDI (bizning eng katta xavf — a va c): Buck HECH QACHON ekspert/maslahatchi emas — u hazilkash tanga, faqat manbali fakt aytadi; "you should", "always", "never invest" kabi maslahat jumlalari taqiq (S-10 dan olib tashlangan). Kuniga 4 Short bir xil qolipda bo'lmasin: har kuni kamida 2 xil tuzilma (vs-ochilish / stat-ochilish / savol-ochilish / afsona-haqiqat), har xil sahna soni va hazil usuli.
   O'LCHOV: 5 ta tungi video ketma-ket ko'rilganda bir xil tuyuladimi — keyingi B ishida 5 tasining 1-3-sahnalarini yonma-yon ko'rib baho yoz.
3. O'RGANILDI (tasdiqlanmagan, YouTube rasman aytmagan): tahlilchilar 30 kundan eski Shorts kam ko'rsatilayotganini xabar qilmoqda (Search Engine Journal; Tubefilter 2025-12-05).
   O'ZGARTIRILDI: hech narsa — faqat kuzatamiz; o'z videolarimizda 30 kundan keyin tekshiramiz.
4. XATO VA SABOQ: GPU lab-qimirlash renderida 540 kadrdan 300 tasi teksturasiz (qora tana) chiqdi va tekshiruvsiz repoga tushdi. SABOQ: har kutubxona pushidan oldin avtomatik "qora kadr" tekshiruvi (shaffof bo'lmagan piksellarning >30% i yorqinligi <12 bo'lsa — rad). Keyingi GPU ishida engine/gpu_render.py ga qo'shilsin; yetishmayotgan kayfiyatlar (point, proud, thumbsup, dizzy, sad, angry, sideeye t2/t3) qayta render.
5. XATO VA SABOQ: Gemini ssenariylarining 11 tasidan 9 tasida kamida bitta manbasiz yoki noto'g'ri raqam bor edi ($140,000, $42,000, $1,350, $150...). SABOQ: tashqi ssenariy hech qachon tekshiruvsiz ishlatilmaydi; har raqam birlamchi manbadan.
6. O'ZGARTIRILDI (Shohjahon 07:11 talabi — xilma-xillik): dvigatel v6.1 — 6 ta fon ko'rinishi ("theme": vault/mint/ember/royal/ocean/noir; berilmasa birinchi jumladan avtomatik); producer_task ga XILMA-XILLIK QOIDASI (8 format, 6 emotsiya, theme/ochilish/tuzilma almashinuvi). KAMCHILIK: tungi 5 video eski bir xil ko'rinishda va bir xil skeletda render bo'lgan. O'LCHOV: ertangi 4 video yonma-yon qo'yilganda 1-kadrlari bir-biridan farq qiladimi.
   HALI YO'Q: 3D muhit/proplar (kupyura, do'kon, samolyot), har videoga maxsus 3D kadr — eng katta xilma-xillik shundan keladi; GPU ishi, alohida bosqich.
7. O'ZGARTIRILDI (BUYURTMA 2, 07:25–08:05): tungi 7 Short qayta yasaldi. ESKIDAN FARQI: 7 videoda 5 xil theme (royal, ember, ocean, noir, mint) — avval hammasi bir xil fon; 7 xil format (raqam hikoyasi, taxmin o'yini, vs, detektiv, sanoq, afsona-haqiqat, "sen shu yerdasan"); ochilishlar har xil (b-roll+raqam, Buck center savol, katta raqam, "case file", vs-panel); emotsiyalar 6 xil. Ovoz: buzuq TTS take endi keshdagi belgi/soniya bilan avtomatik topiladi (<9 → qayta); raqamlar "say" da so'z bilan.
   O'LCHOV: 23:17 tahlilda 20-noy Shortlarining 3 s ushlab qolishi (vosita bersa) — kechagi (19-noy, eski uslub) bilan solishtir; ertangi B ishida 7 videoning 1-kadrlarini yonma-yon qo'yib "bir xil tuyuladimi" bahosi.

## 2026-11-20 (vazifa, A 09:19)
8. O'RGANILDI: kanalning birinchi Buck uzun videosi — 16:9 da dvigatel avval sinalmagan edi; sinov render (3 sahna) layout to'g'ri, lekin to'liq renderda sticker sarlavha va Buck shlyapasini yopardi; dvigatel bitta yadroda ishlaydi.
   O'ZGARTIRILDI: engine v6.2 — 16:9 da sticker Buck yonida; sahnaga o'z "show_source" matni; uzun video 3 bo'lakda parallel render (3 xil theme — bitta video ichida ham xilma-xillik); sticker sarlavhani takrorlamaydi (9 ta sarlavha almashtirildi).
   O'LCHOV: 23:17 C da uzun videoning o'rtacha ko'rish % (vosita bersa) va qaysi bobda tushish — keyingi uzun video tuzilmasiga.

## 2026-11-20 (vazifa, B 15:19)
9. O'RGANILDI: QC jurnalida (BUYURTMA 2) "vs-sahna boshida ~0.5 s bo'sh o'rta" — 1M+ qoidasi 2 ("hech bir kadr 1.5 s o'zgarishsiz / bo'sh o'rta yo'q") buzilardi; raqobatchi etaloni (Humphrey Yang, OutlierKit 2026-09) katta raqamni jismoniy masshtab bilan ko'rsatadi.
   O'ZGARTIRILDI: engine v6.3 — VS panel tushguncha joyida pulslanuvchi punktir "?" maket (kutish → ochilish; "no_ghost": true o'chiradi). Sinov render: 0.15/0.6/1.6/2.5 s kadrlarda o'rta bo'sh emas, maket panel tushishi bilan yo'qoladi. Playbook 5-bo'lim: "masshtab namoyishi" g'oyasi.
   O'LCHOV: keyingi vs-li Short (A 21-noy) kadrlarida 0–1 s oraliq bo'sh emasligi; 23:17 C da vs-ochilishli Shortlarning 3 s ushlab qolishi (vosita bersa) boshqa ochilishlar bilan.
7. O'RGANILDI (2026-11-20 18:50, Shohjahon bergan manba): Lemo-Opuscar uslublar kutubxonasi (github.com/lemomo-ai/lemo-opuscar) — LICENSE, rejissorlik va texnika qo'llanmalari o'qildi. O'ZGARTIRILDI: `docs/style_library.md` (litsenziya, "uslubli insert" tartibi, 12 rejissorlik saboqi), producer_task ga bo'lim. YANGI O'LCHOVLAR: ovoz −14 LUFS (hozir faqat mean dB o'lchanardi), blackdetect, 2 sukunat. O'LCHOV: birinchi insertli Short — keyingi A ishi; vaqt va natija shu yerga yoziladi.
8. O'RGANILDI (2026-11-20 19:10): GitHub'dan claude-youtube skill to'plami (MIT) ko'chirildi → docs/skills/; nomzodlar jadvali (Rhubarb lab-sinxron eng foydalisi). GIPOTEZA: Short uzunligi bo'yicha ikki manba bir-biriga zid (13/60 s vs 32–42 s) — o'zimiz 3 xil uzunlikda sinaymiz. O'LCHOV: 12 ta Short (4×15 s, 4×30 s, 4×55 s) ko'rish va o'rtacha ko'rish %.
9. QO'LLANDI (2026-11-20 19:15, Shohjahon: "skillarni yig'ib o'tirma, qo'lla"): ovoz-matn tekshiruvi yozildi va rejadagi 7 Shortda ishlatildi — mos kelish 0.98, 0.92, 0.96, 0.97, 0.94, 0.97, 1.00; buzuq yoki tushib qolgan jumla yo'q. Hugging Face yopiq edi → model GitHub releases'dan olindi. SABOQ: yangi skill o'sha kuni kamida bitta haqiqiy videoda ishlatilmasa — "qo'shildi" hisoblanmaydi.
10. QO'LLANDI (2026-11-20 20:10): Instagram skill to'plami o'rnatildi; hookscore bizning 5 hookni baholadi: fee_guess 75 (kuchli), giftcard 51, twenty_secrets 48, gate_story 47, costco_case 39 (kuchsiz: 'stakes' past). beats: gate_story hook 4.7 s (3 s dan uzun), 7-jumla 4.7 s. SABOQ: hooklarimiz uzun — birinchi jumla ≤8 so'z. O'LCHOV: ertangi 4 Short hook bali ≥50 va hook ≤3 s; keyin real ko'rishlar bilan solishtiriladi (costco_case past ball oldi — real natijasi bu o'lchov ishonchliligini ko'rsatadi).
11. QO'LLANDI (2026-11-20 20:25): ffmpeg-skill check.py — rejadagi 8 Short (shorts + reels spetsifikatsiyasi) va uzun video (youtube) tekshirildi: 0 xato; ovoz −14 LUFS atrofida, true peak ≤ −1 dBTP. 5 manba ko'rildi: 4 tasi ko'chirildi (MIT/Apache), OpenMontage (AGPL) — faqat eslatma.
12. QO'LLANDI (2026-11-20 20:55): dizayn skillari bo'yicha tipografika ko'rigi → "Source:" qatori o'qilmas edi (26 px, kulrang) → dvigatel v6.4 da 32 px, ochroq, konturli, avtomatik sig'adi. Ertangi videolardan boshlab. Eslatma: bu 3 manba veb-dizayn uchun — videoga faqat tamoyillari ko'chadi.

## 2026-11-20 (vazifa, BUYURTMA 3, 20:34)
13. O'RGANILDI: eleven_v3 /with-timestamps so'z vaqtlarini beradi va voice_settings (speed) ni qabul qiladi, lekin previous_text/next_text ni rad etadi (400 unsupported_model).
   O'ZGARTIRILDI: engine el_speak — v3 da prev/next yuborilmaydi. O'zbekcha namuna 1-urinishda chiqdi (38.4 s, −14 LUFS).
   O'LCHOV: Shohjahonning talaffuz bahosi; "ha" bo'lsa finansist424 uchun o'zbekcha Reellar shu yo'l bilan. v3 da kontekst yo'qligi sababli jumlalar orasidagi intonatsiya uzilishi bo'lishi mumkin — baho kelganda tekshiriladi.

## 2026-11-20 (vazifa, C 23:19)
14. O'RGANILDI (o'z kanalimiz, vidIQ ochiq hisob 23:20): yangi uslubdagi birinchi Short (trillion61 v2: Buck D ElevenLabs, 3D v2 + lip-sync, b-roll+raqam ochilishi, royal) ~3 soatda 241 ko'rish, 80 VPH, 3 izoh; eski uslub (Kokoro hikoyachi, 40–48 s) 1–2 kunda 22–78. Bitta video — xulosa emas, lekin farq 3–10x.
   O'ZGARTIRILDI: playbook 6-bo'lim — "IKKI BARAVAR OSHIR" (dastlabki): b-roll+katta raqam ochilishi; ertangi 4 Shortning 2 tasi shu ochilishda (XILMA-XILLIK: theme/format/emotsiya boshqa bo'lsin).
   O'LCHOV: 21-noy C da trillion61 vs fee_guess (hookscore 75, Buck center+savol ochilishi) 24 soatlik ko'rish va YouTube Analytics kelgan bo'lsa averageViewPercentage. HOOKSCORE MOSLIGI: hozircha ma'lumot yetarli emas (fee_guess chiqqaniga 10 daqiqa; trillion61 hookscore hisoblanmagan) — ertaga ikkalasini bir xil yoshda solishtir.

## 2026-11-21 (chat, 00:10 — Shohjahon: "youtube-skill o'rnat, eng yaxshilarini")
15. QO'SHILDI: yt-agent/youtube-skill GitHub'da yo'q → eng yaqin 3 ta (MIT): Jakeschincariol/youtube-agent-skill (to'liq, 11 skill), sergebulaev/youtube-skills (faqat bilim qismi), adityaarsharma comment-intel. Batafsil: docs/skills/README.md.
   QO'LLANDI: yt-package/title.py navbatdagi 7 sarlavhada — 4 tasi 100, eng pasti uzun video "The Subscription Trap: Why Canceling Is So Hard" 76 (47 belgi: mobil lentada kesiladi, raqam yo'q).
   O'LCHOV: A ishida har sarlavha title.py dan o'tadi (≥90 maqsad, lekin Shorts sarlavhasi ≤50 belgi qoidasi va aldamaslik ustun); keyingi uzun video sarlavhasi ≤40 belgi va raqam bilan — CTR ni subscription_trap bilan solishtir. retention.py — Analytics CSV kelgan birinchi C ishida.
16. O'RGANILDI (2026-11-21 00:30, Shohjahon: "har xil grafika, joylar, effektlar, kino kabi"): iart-ai motion skills (MIT) — 7 to'plam o'rnatildi; joylar uchun CC0 aktivlar (Poly Haven, Kenney City Kit), AI video (Wan 2.2, Apache-2.0, RunPod ~$0.06/s — pullik, ruxsat kerak). Batafsil: docs/skills/notes/2026-11-21_cinematic_visuals.md.
   O'ZGARTIRILDI: pilot — Vox uslubidagi xarita insert (work/pilot_map/map_insert.py): 1-urinishda xarita 9:16 da kesildi → kamera teskari (yaqindan → butun marshrut) qilindi, 2-urinish to'g'ri.
   O'LCHOV: keyingi sayohat/joy mavzusidagi Shortda 1 xarita sahnasi; o'sha sahnada ushlab qolish tushishi bor-yo'qligi (Analytics kelganda retention.py).
17. ULANDI (2026-11-21 01:10): Pixabay API ISHLADI (PIXABAY_API_KEY; "airport" → 187 video, 11–53 s) — b-roll endi vidIQ kreditisiz. RunPod: api.runpod.ai ochiq, RUNPOD_API_KEY bor, lekin barcha public endpointlar 403 "no permission" (kalit huquqi yetarli emas — Shohjahon "All" huquqli kalit yaratadi). O'LCHOV: ertangi A ishida 1 Short b-roll Pixabay'dan; Wan sinovi kalit tuzatilgach (1 klip, ≤$0.30).
13. QO'LLANDI (2026-11-21 02:00): vizual sifat skillining texnik standart bandi → dvigatel v6.5: x264 medium + CRF 16 (oldin veryfast + CRF 20), rang bt709 deb belgilanadi, audio 192k. Sinov: bitreyt ~2.2 baravar, rang siljimadi. Render vaqti biroz oshadi. 4K — yo'q (haqiqiy 4K alohida qaror: render ~4x sekin + Buck kutubxonasi GPU da qayta).

## 2026-11-21 (vazifa, A 01:46)
18. O'RGANILDI: cdn.pixabay.com bu muhitda proksi 403 (Pixabay API ishlaydi, video CDN yo'q) — 17-yozuvdagi "ertangi A da Pixabay b-roll" sinovi BAJARILMADI. O'rniga map_insert (NY→NJ, label'siz) — imzo kadr sifatida ishladi; yorliq subtitr/manba bilan to'qnashardi → map_insert.py: bo'sh --label endi yorliqni chizmaydi.
   O'ZGARTIRILDI: dvigatel v6.5.1 — eksportga bitreyt chegarasi (Short 12M, long 2M): parallel sessiyaning CRF16 i 30 s Shortni 111 MB qilgan, GitHub rad etgan. Chart "hi" (ajratiladigan ustun).
   O'LCHOV: keyingi Short fayllari ≤55 MB va sifat kadrlarda pasaymaganmi; Shohjahon Muhit sozlamasida cdn.pixabay.com ni ochsa — Pixabay b-roll sinovi.
19. QO'LLANDI: hookscore — 100 ball olgan BF varianti ("your money's catching up") ma'nosiz edi → olinmadi (fakt > ball). voice_check "can't"→"can" ni ushladi (ma'no teskari) va buzuq oxirgi take'ni (6.7 c/s, qichqiriq) — ikkalasi tuzatildi. SABOQ: inkor so'zlari ("can't") hookda — "can NOT".
   O'LCHOV (23:17 C): airport (hookscore 80.8, katta raqam) vs bfcm (64.8, vs-panel) — 24 soatlik ko'rish; birinchi o'zbekcha Reellar (finansist424) ko'rish/follower.
20. ULANDI (2026-11-21, Shohjahon): cdn.pixabay.com muhit tarmog'ida ochildi (tekshiruv: 200). Pixabay b-roll endi to'liq ishlaydi (API + video CDN). O'LCHOV: keyingi A/B ishida 1 Short b-roll Pixabay'dan (kadrlarni Read bilan ko'r; tavsifda "Pixabay" + muallif).
21. O'ZGARTIRILDI (2026-11-21, Shohjahon: "oddiy fon emas, har xil yaxshi fonlar"): dvigatel v6.6 — spec "bg" (haqiqiy klip/rasm fon: kichik o'lchamda dekod + gblur + theme bilan 62% aralash + qoraytirish + sekin siljish; ro'yxat sahnalar bo'yicha almashadi) va engine/pixabay_bg.py (Pixabay qidiruv, safesearch, odam/brend teglari chiqarib tashlanadi, muallifni chiqaradi). Sinov: aeroport/savdo markazi/tungi shahar fonlari, 3 sahna — matn va Buck aniq o'qiladi. producer_task XILMA-XILLIK 3a: har videoda majburiy.
   O'LCHOV: B ishidagi 2 Short "bg" bilan; render vaqti oshganmi (kutilgan +5–10%), kadrlar o'qiluvchanligi; C da ko'rish/ushlab qolish eski "oddiy fon"li videolar bilan.

## 2026-11-21 (vazifa, B 09:17 — jadvaldan tashqari)
22. O'RGANILDI (MALAKA: komik timing): stend-ap tahlillari — punchline'dan oldin pauza (CogSci 2026, bizda bor) bilan birga, punchline'dan KEYIN ham pauza kerak (kulgi/tushunish uchun); bir xil bitda nutq segmentlari barqaror, o'zgaradigani — oraliqlar (ScienceBlog 2026, 20 kechalik bit; arXiv 2602.12763 intervyulari). Dalil asosan amaliyotchilardan — gipoteza.
   O'ZGARTIRILDI: dvigatel v6.7 — sahna "land" (jumladan keyingi sukunat, sekundda). Sinov: pink Short 8- va 9-sahnalarda land 0.3/0.4 — timings da sahna uzunligi mos o'sdi, kadrlarda bo'sh o'rta yo'q (Buck va stat turibdi).
   O'LCHOV: C (23:xx) da 22-noy videolari Analytics kelganda — pink (land bor) vs cart (land yo'q) o'rtacha ko'rish %; 3 kunlik farq yo'q bo'lsa "land" ni faqat aniq punchline'larda qoldir.
23. O'RGANILDI: multilingual_v2 oxirgi loop jumlasidagi "because..." ni cho'zib buzuq take beradi (pink 1-render: 52 belgi / 5.7 s, ASR "because" dan keyin noaniq so'z eshitdi). voice_check balli 0.907 (o'tgan!) — ya'ni ball bu xatoni ushlamaydi.
   O'ZGARTIRILDI: QC qadami — voice_check "heard" matnining OXIRGI jumlasini doim ko'z bilan o'qi; "..." bilan tugaydigan jumlani "Because..." deb alohida gapga ajrat (sinaldi: 2-renderda toza).
   O'LCHOV: keyingi 4 Shortda oxirgi jumla buzilishlari soni (maqsad 0).
24. BUYURTMA 4: yangi Buck v3 (chat) render o'rtasida tushdi → 8 EN + 2 UZ video v3 bilan 3 parallel renderda ~35 daqiqada; 6 eski post Metricool'da almashtirildi, hech biri slotga 60 daqiqadan yaqin emas edi. vidIQ keyword_research "rising" + niche — 1 ta aloqasiz natija (5 kredit isrof) → keyingi safar "questions"/"research" rejimi aniq mavzu bilan.
   SKILLAR (bugun 4 ta, hammasi SINALMAGAN): Rhubarb lip-sync, pyfxr, Parselmouth, ruptures — docs/skills/README.md. Ertangi sinov: Rhubarb (v3 talk kadrlari bilan) yoki Parselmouth "land" tekshiruvi.
25. O'RGANILDI (2026-11-21 12:20–12:50, Shohjahon: "hamma skillarni ko'rib chiqib yangiliklar qil"): SINALMAGAN skillardan 3 tasi sinaldi. Parselmouth: Buck D juda jonli (F0 diapazoni 5.6–23.4 st) — "monoton" xavfi yo'q; A-yoki-B savollar ohangi tabiiy pasayadi. title.py: 2 sarlavha raqamsiz, 3 tasi mobil kesimda raqamni yo'qotadi.
   O'ZGARTIRILDI: engine/prosody_check.py (yangi QC); dvigatel v6.8 — pyfxr 8-bit sfx palitrasi (engine/sfx_fxr.py); gift card sarlavhasi raqamli qilindi. Rhubarb — binar yuklash bloklandi.
   O'LCHOV: gift card Short (21-noy 13:00 ET) ko'rishi vs shu kungi qolgan 3 Short; fxr sfx ishlatilgan birinchi Shortlarda ushlab qolish (C da). Yangi muhitda: pip pillow --ignore-installed, Anton/ComicRelief google/fonts dan (aks holda render yiqiladi).
26. O'RGANILDI (2026-11-21 12:55, Shohjahon "Ruhsat"): Rhubarb 1.14.0 Linux binari ishlaydi (5.2 s ovoz → 12 s, 41 og'iz shakli).
   O'ZGARTIRILDI: dvigatel v6.8 lip-sync — talk_level endi fonema jadvalidan (rhubarb_cues), sprite tezligida (har 2 kadr); binar yo'q/xato → eski ovoz-balandligi usuli. graphify xaritasi yangilandi.
   O'LCHOV: keyingi 2 Shortda Buck og'zini 0.5x tezlikda ko'rib, eski usul bilan solishtir (lab "yolg'on gapirayotgandek" ko'rinmasligi); render vaqtiga +10–20 s.
27. O'RGANILDI (2026-11-21, Shohjahon yuborgan video: Kellan Henneberry, "How I Make $24,937/mo Posting YouTube Shorts (Using Claude AI)", 1.85M ko'rish, outlier 20x; vidIQ transkript, 10 kredit → qoldi 32): (1) "ranking" format 5–7 band + ARALASH tartib (#1 oxirida) — retention uchun; (2) ekrandagi sarlavha aniq 2 qator, kalit so'z boshqa rangda; (3) g'oyani "isbotlangan" videolardan ol — ilhom kanalining eng yaxshi videolari (vidIQ competitor breakdown); (4) har kuni uzilishsiz post. Uning da'volari ($0.42 RPM, "raqobat eng past") — tasdiqlanmagan, faqat uning kanali; bizga monetizatsiya hali yo'q.
   OLINMADI: TikTok/Instagram'dan begona kliplarni yig'ish (mualliflik va "inauthentic/reused content" — QAT'IY CHEGARA 1b), Viblo (pullik, affiliate havola), "hamma ruxsatga always allow".
   O'ZGARTIRILDI: playbook 4-bo'lim — REYTING FORMATI (i) va SARLAVHA-PLASHKA qoidasi; bankda S-12 konsept.
   O'LCHOV: birinchi reyting-Short (aralash tartib) ning o'rtacha ko'rish % i vs o'sha haftadagi sanoq (3 fakt) Shortlar.
28. O'RGANILDI (2026-11-21, Shohjahon yuborgan rus tilidagi "Amerika YouTube" darsi, 34 daq, asosan kurs reklamasi; vidIQ transkript 5 kredit → qoldi 27): (1) "hype" vs "doimiy" nisha — hype tez ko'rish beradi, lekin so'nadi; doimiy mavzu (bizda moliya) 5–10 yil passiv ko'rish beradi; (2) raqobatchi tahlili: kam obunachi + katta ko'rish = issiq nisha; eng mashhur mavzuning hali qilinmagan variantini birinchi bo'lib qil; (3) "o'zgartirilgan kontent" belgisi faqat real odamlar/realistik sahnalar uchun — Buck to'qima multfilm personaj, bizning isAiGeneratedContent=false to'g'ri; (4) post vaqtini raqobatchilar post qiladigan vaqtga qarab tanlash.
   OLINMADI: real odamlar (Bruce Lee, McGregor) bilan AI video — QAT'IY CHEGARA 1b; raqobatchi thumbnail'ini AI bilan o'zgartirish va suv belgisini kesib olib tashlash — mualliflik/litsenziya buzilishi; soxta tug'ilgan sana; "AI monetizatsiyasini saqlaydigan sirli personalizatsiya" — tushuntirilmagan, kurs reklamasi. Monetizatsiya raqamlari (1000 obunachi + 4000 soat yoki 10 mln Shorts) — hozirgi shart; playbook 2-bo'limdagi 2027 o'zgarishi o'z kuchida; O'zbekistonda YPP baribir yo'q.
   O'ZGARTIRILDI: playbook 4-bo'lim — "NISHA SIGNALI VA BIRINCHI BO'L" qoidasi (kuniga kamida 2 doimiy mavzu).
   O'LCHOV: 7 kundan keyin hype vs doimiy Shortlarning 7-kunlik ko'rish o'sishi (doimiylar sekin, lekin to'xtamay o'sishi kerak).

29. O'RGANILDI (chat, 2026-11-21 18:25, Shohjahon: "kanalni rivojlantirmayapsan, konkurentlarni kuzatmayapsan"): har video bo'yicha haqiqiy ko'rish olindi (vidiq_user_videos, 5 kredit → qoldi 22). Jami 1,712 (vidiq_user_channels 128 ko'rsatgan — kechikadi). Raqamli sarlavhali yangi uslub Shortlar 185–1,134, raqamsizlar 11–31. Raqobatchi kuzatuvi shu paytgacha 3 kanal bilan to'xtab qolgan edi.
   O'ZGARTIRILDI: producer_task 1.8 — har kuni 1 raqobatchi, har kuni 1 sinov, har kuni raqamli hisobot; docs/results.md va docs/competitors.md ochildi.
   O'LCHOV: 72 soatdan keyin results.md da raqamli vs raqamsiz sarlavha (6 ga 2); 7 kunda competitors.md da ≥7 yangi tahlil va ≥5 sinov natijasi.
30. O'RGANILDI (2026-11-21 kech, Shohjahon: "ranglarni ko'rib chiq"): rang bo'yicha mustaqil CTR tadqiqoti yo'q — izchil omil faqat KONTRAST (yorug'lik farqi) va 3 rangdan oshmaslik. O'lchov: palitra hammasi o'qiladi (qizil mint/ocean'da faqat katta matn); qizil/yashil deuteranopiyada chalkashadi (strelka bor — OK); videolarimiz qorong'i (o'rtacha yorug'lik 33–48/255, 20–40% qora).
   O'ZGARTIRILDI: color-expert skill (meodai, CC BY 4.0) + engine/color_check.py + qc_gate 9-qadam; qoidalar notes/2026-11-21_color.md (1 theme + oltin + 1 urg'u; Rocco fonlari qizil emas).
   O'LCHOV: A/B 1 hafta — 4 "yorug'" Short vs 4 odatiy: o'rtacha ko'rish % va "stayed to watch". Keyingi B: dvigatelga spec "bg_bright" (fon yorug'ligi ko'paytirgichi) qo'shish.
31. O'RGANILDI (2026-11-21 kech, Shohjahon: "rivojlan, to'xtab qolma; aytishimdan oldin qil"): yaxshilash faqat Shohjahon aytganda bo'layotgan edi; "slotlar to'la" ishlar bo'sh o'tayotgan edi (12:14, 15:18, 18:15).
   O'ZGARTIRILDI: docs/improvement_backlog.md + producer_task "O'Z-O'ZIDAN RIVOJLANISH" (har ishda 1–2 band); shu zahoti 2 band bajarildi: dvigatel v6.9 "bg_bright", Rocco ovozi (ElevenLabs Voice Design).
   O'LCHOV: har kuni backlog'dan yopilgan bandlar soni (maqsad ≥3/kun); Shohjahon "nega qilmading" degan holatlar soni (maqsad 0).

30. O'RGANILDI (chat, 2026-11-21 19:05, Shohjahon: "rivojlan"): vidIQ outliers — kichik inglizcha fakt-kanallarda portlagan 8 Shortdan 5 tasi 5–13 soniya, mavzusi keng "pul viktorinasi" (jadval: docs/competitors.md). Bizning Shortlar 30–48 s va yarmi do'kon narxlari haqida.
   O'ZGARTIRILDI: sprint 1.5 — har kuni 4 mikro (8–12 s) + 4 odatdagi; mikro mavzular ro'yxati.
   O'LCHOV: 72 soatda mikro vs odatdagi ko'rish (results.md "format" ustuni); qaror qoidasi sprint 1.5 da.
32. O'RGANILDI (2026-11-21, navbatdagi 8 video ko'rigi): grafik ustuni animatsiyasi (at + 0.5 s) qisqa sahnada tugamaydi — tomoshabin asosiy raqamni KO'RMAYDI (airport_cap: +15% o'rniga +11%). Teng oraliqli kontakt-varaq animatsiya o'rtasini olib yolg'on xato ko'rsatadi; eski rendered.json boshqa render vaqtlarini beradi.
   O'ZGARTIRILDI: dvigatel v6.10 (ustunlar sahna oxiridan 0.7 s oldin to'liq; loop jumlasida "..." TTS ga ketmaydi); qc_gate — kontakt-varaq har sahnaning 80% nuqtasidan, rendered.json davomiyligi mos kelmasa ogohlantiradi; map_insert yaqin marshrutni zoom qiladi. airport_cap b4 bilan almashtirildi.
   O'LCHOV: keyingi 10 videoda "asosiy raqam ekranda to'liq ko'rinmadi" holatlari soni (maqsad 0); airport_cap ko'rishi va o'rtacha ko'rish % (22-noy 10:00 ET).

### 2026-11-21 23:40 Toshkent — C ishi (vazifa sessiyasi)
O'RGANILDI: ikki sessiya bir vaqtda ishladi (kod sessiyasi claude/lucid-volta branchida, vazifa sessiyasi media'da); vazifa sessiyasi Buffer'dagi post ID ni "eski r01" deb o'chirdi, aslida u yangi r01 v2 edi. O'ZGARTIRILDI: Buffer/Metricool postini o'chirishdan OLDIN matnini repodagi spec/desc bilan solishtirish va boshqa branchlarni (`git ls-remote origin`) tekshirish — improvement_backlog ga band. O'LCHOV: r01 v2 22:00 UTC da chiqdimi — keyingi ishda Buffer list.
Raqamlar: jami 1,878 (+166), obunachi 3 (+1); "3 Secrets on a $20 Bill" 3.5 soatda 146.
KECHA vs BUGUN (2026-11-21 C): bugun chiqqan 2 Short (twenty_secrets b3, giftcard b3) — Buck v3, Pixabay fon, −14 LUFS (kecha −18 dB), voice_check ≥0.9; "$20 Bill" 3.5 soatda 146 (kechagi eng yaxshi start $1T 3 soatda 241 — sekinroq, lekin eski uslubdagi 22–78 dan ancha yuqori). Yomonlashgan: kanal jami o'sishi sekinlashdi (+166/kun; $1T to'xtagan). Ertaga: GTA 6 trend + raqamli sarlavhalar; yangi dvigatel v6.14 (shots, 1–3 so'z subtitr) birinchi haqiqiy natija.

### 2026-11-22 10:05 Toshkent — A ishi (vazifa sessiyasi)
O'RGANILDI: mehmon ovozining "taxmin?" savollari ElevenLabs'da tekis intonatsiya bilan chiqadi (prosody FLAT_Q 2 sahna). O'ZGARTIRILDI: taxminlar ishonchli noto'g'ri gap qilib yozildi ("Hmm... two cents. Tops." / "Easy. Twenty cents.") — prosody 0 flag, hazil kuchaydi (ishonch + xato). O'LCHOV: coins_v02 (23-noy 07:00 ET) 24/72 soatlik ko'rishni pink_r07 (savolli taxmin) bilan results.md da solishtirish.

### 2026-11-22 23:30 Toshkent — C ishi (vazifa sessiyasi)
O'RGANILDI: 24 soatda kanal 1,878 → 6,369 (+4,491). Yangi v6.14+ uslub (fullbleed/shots, 1–3 so'zli subtitr) + "$X Billion" sarlavha: 3 ta video 960–1,274; eski uslub 24–81 da qoldi. IG retention: mikro 14 s — 71%, 52 s masshtab — 22%, 26–31 s — 33–51%. Metricool bepul limiti 22-noy 13:00 ET da tugadi (post ERROR) — bu sprintning eng katta to'sig'i.
O'ZGARTIRILDI: script_bank — 4 ta IKKI BARAVAR davomi (G-1, H-1, H-2; G-2 Rocco'ga) va 2 SHOSHILINCH (Farm Bureau $58.63; Rocco bot-izohlar); backlog — Metricool limiti zaxira yo'li (vidIQ social_post yoki Buffer 3-kanal) bandi.
O'LCHOV: 23-noy C — G-1/H-1 davomlari 24 soatda ≥1,000 mi; Metricool post ERROR soni (maqsad 0).
KECHA vs BUGUN: kecha eng yaxshi kunlik start 146 (3.5 soat), bugun 964 (6 soat, GTA 4.7x) — ~6x. Kadr tempi kecha 3–7 s/kesim, bugungi videolarda 1.5–1.9 s. Yomonlashgan: 1 video chiqmadi (Metricool limit).

### 2026-11-23 23:40 Toshkent — C ishi (vazifa sessiyasi)
O'RGANILDI: kunlik o'sish +894 (kecha +4,491). Bugun chiqqan 6 video (Financier BK 3: 160/79/41; Rocco 3: 4/1/1) — hammasi 23-noy 01:17 UTC dagi 19 ta ketma-ket vidIQ yuklashdan. Kechagi trend+raqam videolari o'sishda davom etdi (GTA 4.7x +333 → 1,297). Gipoteza: burst yuklash + uploadLimitExceeded tavsiyani susaytirdi (isbot emas; Metricool 2026: haftasiga >7 post oylik ko'rishni pasaytiradi).
O'ZGARTIRILDI: backlog tepasi — burst taqiq qoidasi (kanalga kuniga ≤3–4, oraliq ≥2 soat, ikki kanal bir paytda emas) va 24-noy o'lchovi. IG ten_bill Reel slotida chiqarildi.
O'LCHOV: 24-noy C — 6 "burst" videoning 24 soatlik ko'rishi vs 22-noy videolari; vidIQ YT navbatidan ≥2 soat oraliq bilan chiqqanlar (nickel, ten_bill) 24 soatda ≥300 mi.
KECHA vs BUGUN: kecha 3 video 6 soatda 960–1,274 edi, bugun eng yaxshisi 7.5 soatda 160 — YOMONLASHDI. Sabab taxmini yuqorida; ertangi tuzatish: navbat oraliq bilan, Financier trend mavzusi (raqamli sarlavha) birinchi.

### 2026-11-24 23:35 Toshkent — C ishi (vazifa sessiyasi)
O'RGANILDI: kunlik o'sish +465 (kecha +894). 23-noy burst videolari 24+ soatda: Financier 295/124/157, Rocco 5/1/1 (o'smadi). Bugun oraliq bilan yuklangan Rocco "Hi Mom" 4 soatda 834 — burst gipotezasi Rocco'da kuchli tasdiqlandi. Financier bugungi 4 video (nickel 31/6 soat, $10 bill 88/3 soat, penny 24, bank_fees 7) — trendsiz, kichik raqamli mavzular: 22-noy trend+milliard videolaridan ~10x sekin.
O'ZGARTIRILDI: script_bank SHOSHILINCH U-3 (AAA 81.5M Thanksgiving, aviachipta $800) va U-4 (benzin rekordi — faqat tasdiqlansa); backlog — "kunda kamida 1 trend/katta raqam Short navbat boshida" bandi. IG Reel'ni YouTube havolasidan chiqarish (vidiq_video_upload'siz) ishladi.
O'LCHOV: 25-noy C — print_100/buck_1748/cancel_sub (trendsiz) vs U-3 (trend) 24 soatlik ko'rish; Rocco "Hi Mom" 24 soatda ≥1,000 mi.
KECHA vs BUGUN: kecha eng yaxshi yangi video 7.5 soatda 160, bugun Financier eng yaxshisi 3 soatda 88 (taxminan teng temp), Rocco 4 soatda 834 (kechagi 1–4 dan ~200x) — Rocco YAXSHILANDI, Financier o'zgarmadi. Sabab: Financier navbatida trend mavzu yo'q; tuzatish — U-3 navbat boshiga.

## 2026-11-25 (A, erta 07:20–08:15 Toshkent)
O'RGANILDI: auto_shots bitta klipli sahnaga boshqa mavzudagi klip qo'shadi (kurka → Yer); tungi osmon / oq fon kliplari empty_panel ni buzadi (38% → 21% → PASS).
O'ZGARTIRILDI: U-3 trend Short (AAA 81.5M) navbat boshiga; har sahnada ≤2 s oraliqli o'z kliplari bilan aniq "shots". Faktlar render oldidan qayta tekshirildi (AAA, 16-noy benzin).
O'LCHOV: 26-noy C — U-3 24 soatlik ko'rish vs print_100/buck_1748 (trendsiz). Gipoteza: trend + katta raqam ≥3x.

## 2026-11-25 10:15 Toshkent (vazifa, A)
O'RGANILDI: vidIQ trending — 201 obunachili kanalning "Fake 50% Off Black Friday tag" mexanizm Shorti 2 kunda 1.05M (22.7K vph). Kichik kanal + mexanizm ("qanday yasaladi") + bayram = eng kuchli signal.
O'ZGARTIRILDI: (1) U-5 [TREND] bankka (FTC 16 CFR 233.1, WalletHub 2025 36%/24%, Oxylabs 2024 75%) — 26-noy 07:00 ET 1-yuklash; (2) dvigatel v6.18 sahna "pool" + auto_pool "scene" (U-3 dagi begona klip xatosi).
O'LCHOV: v6.18 — keyingi Short qc_gate 14_empty_panel PASS va kontakt-varaqda begona klip yo'qligi; U-5 — 24 soatlik ko'rish vs print_100/buck_1748.

## 2026-11-25 B (15:20 Toshkent)
O'RGANILDI: (1) YouTube Shorts okt-2026 "originality" yangilanishi — qayta yuklangan/minimal tahrirli Shortlar tarqatilishi kesildi (Android Headlines, MediaPost; YouTube rasmiy bloglarida tasdiqni tekshirish kerak). (2) YPP "inauthentic content" (2026-07-16): moliya kabi sezgir mavzuda AI persona — demonetizatsiya xavfi (TechRepublic, Android Headlines 2026-07). Buck ekspert emas, maslahat bermaydi — qoida saqlanadi; har videoda o'z tadqiqot + manba.
O'ZGARTIRILDI: U-5 da birinchi marta `auto_pool: "scene"` (dvigatel v6.18) — avto-kesimlar faqat o'z sahna klipidan; how_made "Step 1/2/3" mexanizm + kostyum gag'i; FTC qoidasi + shtat soni (28/90) — huquqiy fakt videoda birinchi marta.
O'LCHOV: 26-noy C — U-5 24 soatlik ko'rish vs U-3 (trend) va print_100 (trendsiz); auto_pool kontakt-varaqda "sahnaga mos bo'lmagan kadr" soni (U-3 da 1 ta edi).

## 2026-11-25 C (23:30 Toshkent)
KECHA vs BUGUN: bugungi 2 Financier Short (U-3 trend 5 ko'rish, print_100 0 — 6 soatda) kechagidan YOMON (kecha nickel 6 soatda 31, ten_bill 3 soatda 88). Sabab (dalil bilan): ikkalasi YouTube'da bir paytda ochilgan (12:00:05 va 12:00:29 UTC) — print_100 publishAt navbat surilganda yangilanmagan. Trend gipotezasi (U-3 ≥3x) hali YUTQAZDI, lekin sinov toza emas (burst-2).
O'RGANILDI: BK-03 "Paying Off the US Debt at $1M a Day" 887 — gipotetik katta raqam 3-kun ham №1; bank_fees skit 24 soatda 6 → kichik raqamli skit TO'XTAT.
O'ZGARTIRILDI: backlog tepasiga publishAt tekshiruvi (har YT yuklashdan oldin draft_update + keyin publishedAt tekshiruvi, ≥3 soat oraliq). script_bank SHOSHILINCH: ICSC $124B (kamaydi), Adobe BF $12.9B.
O'LCHOV: 26-noy C — U-5 (yolg'iz, oraliqli) 24 soatlik ko'rish vs U-3/print_100; publishedAt slotga mosmi.

## 2026-11-26 B (15:20 Toshkent)
YANGILIKLAR (2 WebSearch): (1) YouTube Shorts — noyabr 2026 da RASMIY yangi algoritm xabari topilmadi; oktyabr 2026: Shorts tavsiyasi original kontentni afzal ko'radi, past-mehnatli qayta yuklash kamaytiriladi (androidauthority, "rasman tasdiqlanmagan" ikkinchi manba). Biz uchun: o'z footage + o'z ssenariy qoidasi to'g'ri. (2) Adobe prognozi (news.adobe.com 2026-09): Thanksgiving (BUGUN, 26-noy) $6.9B onlayn (+8.5%, 63% mobil), Black Friday $12.9B, Cyber Monday ~$15.1B, Cyber Week $47.5B, BF da BNPL $807M — PROGNOZ, haqiqiy natija 27–28-noy Adobe'dan.
O'RGANILDI: BK-11 doskada "yuklanmagan" turgan, aslida 05:23Z yuklangan — doska bilan post_list har ishda solishtiriladi (shu ishda tuzatildi).
O'ZGARTIRILDI: qc_gate 7b_title_copy (trend manbasi sarlavhasi bilan ≥0.6 ustma-ustlik = FAIL). IG Rocco caption: o'yin javobi caption'da ochilmaydi.
O'LCHOV: keyingi trend Short spec'ida "source_titles" bor va 7b PASS; Rocco P1#2 Reel (DgM4Z0TN__9) 24 soatlik ko'rishi C ishida.

## 2026-11-27 B (15:20 Toshkent)
YANGILIKLAR (2 WebSearch): (1) Shorts — noyabr 2026 da rasmiy yangi algoritm xabari yo'q; 2026-10 originallik o'zgarishi (qayta yuklash reach kamaydi) hali eng so'nggi; "freshness" — YouTube tasdiqlamagan. (2) Adobe: Thanksgiving kuni prognoz $6.9B (+8.5%), 63% mobil; Cyber Week $47.5B; haqiqiy natija hali yo'q.
O'RGANILDI: Montra Explains (625 obun. → 74.3K) — 2-shaxs "If you… But… So…" zanjiri, har 3–5 s halqa, "Congratulations… But" loop. Teg muammosi: teglar draftda berilsa yuklangan videoda saqlanadi.
O'ZGARTIRILDI: skill notes/2026-11-27_build_it_chain.md va _shorts_originality_oct2026.md; hyperframes o'chirildi (sinalmagan, hajm limiti); junk_drawer teglar bilan yuklandi.
O'LCHOV: keyingi Financier Short BUT/SO zanjirida — 72 soatda U-5 (4 ko'rish/24 soat) bilan solishtirish; junk_drawer 24 soatlik ko'rishi 29-noy C da.

## 2026-11-27 C (23:20 Toshkent)
KECHA vs BUGUN: Financier — kecha 5 yangi video ≤13, bugun 7 yangi video ≤17 (BK-12 trend kunida 8/5.5 soat) → yomonlashuv davom; eski g'oliblar ham +0 (BK-03 1,025 → 1,025). Rocco — A1 80 → 138, kanal +243/kun. IG financier424 7 kunlik views 2,927 → 3,133.
O'RGANILDI: channel_analytics (22–27-noy, video): 25-noydan keyingi videolar hali analytics'da yo'q (≥2 kun kechikish); retention eng yuqori — "13 Years Later, GTA Made 4.7x More" 77%, "$10 Bill Dies First" 75%, Thanksgiving 68%; eng past — bank_fees 25.5%, "1 of 3" tipidagi eski. Engaged/views nisbati g'oliblarda 0.23–0.38.
O'ZGARTIRILDI: IG Reel'lar YouTube havolasidan (yuklash shart emas) — 2 ta, ~3 daqiqada; vidIQ krediti 311 — kunlik byudjet 13 kr (trend skan WebSearch'ga, user_videos faqat C da).
O'LCHOV: 28-noy C — BK-11 va junk_drawer 6 soatlik ko'rishi; ≤20 bo'lsa kanal darajasidagi sabab (burst/dublikat) gipotezasi kuchayadi.
