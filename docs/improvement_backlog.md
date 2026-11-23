# YAXSHILASH NAVBATI (producer_task "O'Z-O'ZIDAN RIVOJLANISH") — eng yuqori ta'sir tepada
Har ishga tushishda: tepadagi OCHIQ bandni ol → bajar → sina → natija bilan "BAJARILDI <sana>: ..." yoki "QAYTARILDI: sabab". Yangi muammo topilsa (qc_gate WARN/FAIL, past ko'rsatkich, skill sinalmagan, Shohjahon shikoyati) — shu yerga qo'sh. Kamida 5 ta OCHIQ band doim bo'lsin.

## OCHIQ
- (2026-11-23 09:30 vazifa, ENG YUQORI) METRICOOL LIMITI ANIQLANDI: Free tarif — kalendar oyida 20 ta CHIQQAN post (YT va IG har biri alohida hisoblanadi), 1-dekabrda yangilanadi (help.metricool.com 'Main differences between Free and paid plans'; metricool.com/pricing). Noyabr limiti 22-noy 13:00 ET da tugagan → navbatdagi 12 post (23-noy 07:00 ET dan 25-noy 10:00 ET gacha, YT+IG) ERROR bo'ladi. Muqobil: vidIQ social account list — Financier YouTube (UC3URYtuy…) va IG financier424 canPublish true (0 kredit tekshiruv). Shohjahon qarori kerak: (a) Metricool pullik tarif yoki (b) YouTube'ni vidIQ orqali chiqarishga ruxsat. Qaror kelguncha yangi Financier Short Metricool'ga qo'yilmaydi.
- (2026-11-22 C, ENG YUQORI) METRICOOL LIMITI: 22-noy 13:00 ET post "You have reached your Metricool account limit" ERROR. Zaxira yo'li: vidIQ social_post_draft_create/publish (Financier YT kanali canPublish true) yoki Buffer 3-kanali (bepul: 3 kanal, har biriga 10 navbat) — Shohjahon "ha"/tarif qarori kerak; shu orada qaysi limit (oylik post soni?) ekanini Metricool getBrandSettings bilan aniqlash.
- (2026-11-22, vazifa) SPLIT LOOK: to'yingan split_colors (#7B3FE4) lavhani deyarli yopdi, empty_check 20% FAIL — dvigatelda split rang qatlami alfa ≤0.35 yoki faqat chiziq/kartochkaga rang; v03_bills_split bilan sinash.
- BAJARILDI 2026-11-22 (vazifa): `bash engine/setup_env.sh` — sinaldi (OK). Eski matn: MUHIT TAYYORLASH SKRIPTI: yangi konteynerda dvigatel ishga tushmaydi (numpy/pillow python3.11 da yo'q, tizim PIL buzuq, Anton yo'q) — engine/setup_env.sh yozilsin (pip --ignore-installed pillow, shriftlar, kokoro modeli), har sessiya boshida 1 buyruq.
0. SESSIYALAR KOORDINATSIYASI (2026-11-21): ish boshida `git ls-remote origin` — `claude/*` branchlarda media'dan yangi commit bo'lsa, o'qi va takrorlama; post o'chirish/surishdan oldin matnini repodagi desc bilan solishtir. Kod sessiyasining claude/lucid-volta-x5cic0 dagi dvigatel v6.14 ni media'ga birlashtirish kerak (boshqa sessiyalar eski dvigatelda qolmasin).
1. Looklar (BUYURTMA 6): dvigatelga "paper", "fullbleed", "split" — Financier uchun; navbatdagi videolarni look bilan qayta render.
1b. Rocco: BUYURTMA 5 (GTA 6) — 2 Short; keyin "package held" qo'ng'iroq sahnasi (ikki ovozli dialog — dvigatelga sahna "voice" maydoni kerak).
2. Yorug'lik A/B: keyingi 4 Short spec'ida "bg_bright": 1.4, 4 tasida 1.0 → 72 soatdan keyin o'rtacha ko'rish % (growth_log 30).
3. SPRINT (docs/sprint_10d.md) ustun: kuniga 8 Short, 12 mavzu savati; navbatdagi postlarni savat qoidasiga tekshirish. Financier kunlik trend tahlili (producer_task 1.9) — birinchi marta; Financier nishasida yt-viral swipe.
4. fees_rank voice_check 0.909: "heh"/"checked" takrorlanadigan TTS xatolari ro'yxati → ssenariyda bu so'zlardan qochish yoki ElevenLabs "pronunciation" (alias) — engine'da `say` almashtirish jadvali.
5. ruptures retention (SINALMAGAN 2026-11-21) — Studio retention CSV yo'q; vidIQ channel_analytics_extended dan audience retention olish mumkinmi tekshir.
6. Rocco: telefon ekrani mock-up shabloni (SMS/qo'ng'iroq UI, real brend yo'q) — engine'da yangi sahna turi "phone".
7. Uzun video thumbnail: thumbnail.md + color qoidalari (3 rang, kulrang sinov) + vidiq_score_thumbnail — 22-noy uzun videoga.
8. hyperframes (NOMZOD) — 7 kun sinalmasa o'chirish (2026-11-27).

## BAJARILDI
- BAJARILDI 2026-11-21 23:45: buffer_post.py delete endi postni o'chirishdan oldin work/rocco/deleted_posts/<id>.json ga zaxiralaydi va matn boshini chiqaradi (xato o'chirishni tiklash oson).
- 2026-11-21: Rocco 1-Short (brushing) + Rocco uslubi (dvigatel v6.12) + Rocco sprite generatori; airport_cap qayta render (grafik +15% ko'rinmasdi).
- 2026-11-21: Rocco ovozi yaratildi (voice_id eYibgGvZyWzJUi8HBmQM) — rocco.md.
- 2026-11-21 18:45: Rocco avatar/banner/tavsif/izohlar — chat sessiyasi (Chrome). Brauzer ishi → night_order "CHAT UCHUN".
- 2026-11-21: engine v6.9 "bg_bright" (fon yorqinligi, A/B uchun) — theme fonlari 1.4x da o'rtacha yorug'lik 20–39 → 28–54; py_compile OK.
- 2026-11-21: qc_gate (8 qadam + rang), color_check, skill_map, kunlik top tahlil, Rocco vidIQ.
