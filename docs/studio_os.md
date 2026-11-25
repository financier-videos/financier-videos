# STUDIYA OS — 8 rol, ikkala kanal (Shohjahon 2026-11-25: "aytgan kasblaring kabi o'zing ishla, hammasini o'zing qil, hech biri qolib ketmasin, o'z vaqtida va a'lo darajada bo'lishini tekshirib tur")

Bu fayl `docs/producer_task.md` dan USTUN (QAT'IY CHEGARALAR o'zgarmaydi). Har ishga tushishda (A 09:17, B 15:17, C 23:17 Toshkent) shu tartibda 8 rolni bajar.
Kanallar: Financier (UC3URYtuy-f6c1fTNhesFkGA, Buck) va Red Flag Rocco (UCUyPbjsSFdWKnC4nVRDhOiA). Post faqat vidIQ orqali.

## 0. HAJM VA ORALIQ (dalil: docs/results_2026-11-25.md — burst yuklash videolarni "o'ldirdi")
- Financier: kuniga 3–4 Short, YouTube'ga YUKLASH oralig'i ≥3 soat. Rocco: kuniga 2 Short, oralig'i ≥4 soat.
  (Sprint'dagi "kuniga 8" BEKOR: 23-noy burstida 17 video 1–7 ko'rish oldi, oraliqli "Hi Mom" 4 soatda 834.)
- Hech qachon bir zumda 2 tadan ko'p publish qilma. Kech qolgan videoni keyingi bo'sh slotga sur (vaqt o'tgan bo'lsa draft_update).
- Haftasiga 1 uzun video (5–8 daqiqa) har kanalga — yakshanba (Financier), chorshanba (Rocco), sprintdan keyin (2026-12-01 dan).

## 1. STRATEG (har ishga tushishda, 5 daqiqa)
- `docs/studio_board.md` ni och: bugungi slotlar, kim/nima, holat. Bo'sh slot bo'lsa — to'ldir.
- Qaror qoidasi (raqam bilan): 72 soatda ≥1,000 ko'rish → format SERIYA (keyingi 3 kunda 2 davomi). <100 ko'rish ikki marta → format to'xtatiladi.
  Har hafta (dushanba A): 1 format to'xtat, 1 format kuchaytir, 1 yangi format sina → `docs/studio_board.md` "Haftalik qaror".
- Faol formatlar ro'yxati: Buck — Time Ladder / "hypothetically" katta raqam (BK-03, BK-11), trend raqam (GTA), Guess the Number (sinov);
  Rocco — Penny Plays Dumb seriyasi (2D, unikal joylar), Scam or Legit #N, qisqa matn-firibgarlik tushuntirishi ("Hi Mom"), Scammer's plan backfires, sinov: D1 tan olish, A1 sirli odat.
  TO'XTATILGAN: Rocco 3D GPU epizodlar; Buck chalk/receipt/stamp/versus (trendsiz).

## 2. TADQIQOTCHI / ANALITIK (A da, 15 daqiqa; ~20–40 vidIQ kredit/kun)
- vidiq_outliers + vidiq_trending_videos: ikkala nishada oxirgi 7 kun outlier'lari; yangi 3 tasini `docs/competitor_watch.md` ga (sana, id, ko'rish, nega).
- Yangiliklar: Black Friday/Cyber Monday/bayram, yangi FTC/BBB/FBI ogohlantirishlari, katta pul raqamlari — rasmiy manba bilan.
- Natija: `docs/studio_board.md` "G'oyalar" ga har kanalga 3 ta g'oya (mavzu + format + manba + hook). `docs/growth_research_2026-11-25.md` shablonlaridan foydalan.
- C da: 24/72 soatlik raqamlar (vidiq_user_videos + vidiq_channel_analytics) → `docs/results.md` + format ustuni.

## 3. SSENARIST
- Har video: 3 hook varianti yoz, eng kuchlisini tanla (viral-hooks skill). Birinchi jumla — voqea o'rtasidan, raqam yoki g'alati harakat; salom/ism yo'q.
- Tuzilma: hook (0–2 s) → 5–8 s da burilish → 2-burilish/payoff → loop (oxiri boshiga ulanadi). Dars/ogohlantirish ohangi yo'q — saboq hikoya ichida, oxirgi 1 jumla.
- Uzunlik: Buck hypothetical 45–60 s; Rocco sketch 40–60 s; o'yin 40–45 s; mikro 15–20 s.
- Savol ohangidagi qatorlar darak gap qilib yoziladi (prosody FLAT_Q xatosi). Qisqa so'zlar, og'zaki til.

## 4. FAKT TEKSHIRUVCHI (har ssenariy, render OLDIDAN)
- Har raqam va da'vo yoniga rasmiy manba (FTC, FBI, Fed, BLS, DOL, Take-Two/kompaniya hisobotlari, Forbes sanali). Taxmin (Sensor Tower va h.k.) rasmiy raqam o'rniga ishlatilmaydi.
- Vaqt so'zlari tekshiriladi ("last year" = qaysi yil?). Hisob-kitob tavsifda ko'rsatiladi (Math: ...).
- Real odam yuzi/ovozi, brend logotipi, begona klip, musiqa — YO'Q. Dramatizatsiya tavsifda ochiq aytiladi.

## 5. OVOZ (ElevenLabs)
- Personaj ovozlari: Rocco v2 hYvMKGEmKYHZz9qvD8oj, Penny XeHmOH0wYkEbMfZqbCws, Slick sKpya0iNfGuRwEz634c4, Buck eH342qEgJkje3sPOEo6z;
  hikoyachi George JBFqnCBsd6RMkjVDRZzb, firibgar tan olishi Callum N2lVS1w4EtoT3dr4eOWO, o'yin boshlovchisi Liam TX3LPaxmHKxFdv7VOQHJ.
- voice_check (Whisper) ≥0.95 moslik; noto'g'ri eshitilgan so'z ("It's socks" → "It sucks") qayta yoziladi. -14 LUFS.

## 6. ANIMATOR / RASSOM (unikal ko'rinish — Shohjahon 2026-11-25: "nega hamma videoda bir xil fon?")
- Har Rocco epizodiga mavzuga mos 2–3 YANGI 2D joy (vidiq_image_generate 9:16, "bright flat 2D cartoon background, no characters, no text") → `assets/toon2d/<nom>.jpg`.
- Buck: har videoga o'z footage to'plami (spec "pool" + shot bg'lari), oldingi 5 video bilan takror ≤30%.
- Render oldidan MAJBURIY: `python3 engine/bg_reuse_check.py NEW.json <oxirgi 5–10 spec>` → FAIL bo'lsa yangi fon.
- Har videoning grade/rangi oldingisidan farq qiladi (look_check).

## 7. MONTAJCHI (render + QC)
- Rocco 2D: `rc_render.py` → `add_reactions.py --redo --max 2.0` → qayta render. Buck: rc_render → `work/buck/b10/add_cutaways.py` → qayta render.
- O'yin: `work/rocco/pivot/chat_game.py`; hikoya/kino: `work/rocco/pivot/story_film.py`; ovoz: `work/rocco/pivot/tools/vo.py`.
- QC: cartoon_metrics PASS (ASL ≤2.3 s, max kadr ≤6 s, birinchi so'z 0 s), -14±1 LUFS, qora kadr 0, kontakt varag'ini O'ZING KO'R (grafik xatolar: "$0", kesilgan matn, eski matn qolgani).
- Fayl: repo ildizida `<kanal>_<id>_<slug>.mp4`, commit + push media.

## 8. COMMUNITY MENEJER (B va C da, 15 daqiqa)
- vidiq_video_comments: oxirgi 48 soatdagi videolar izohlari. Har yangi izohga kanal ovozida qisqa javob (vidiq_reply_to_comment; ruxsat so'ralsa — Shohjahonga 1 qator). Trol bilan bahslashma.
- Har yangi videoga pinned-comment matni: keyingi qism savoli yoki "comment your score".
- Izohlardagi savollar → `docs/studio_board.md` "G'oyalar" (manba: izoh).
- Instagram: har Short → @financier424 / @redfrocco Reel (vidiq_instagram_publish_reel, AI belgisi), YouTube'dan ≥2 soat keyin.

## 9. NAZORATCHI (har ishga tushish OXIRIDA — "hech biri qolib ketmasin")
`docs/studio_board.md` bo'yicha tekshir va har bandni ✅/❌ belgila:
1. Bugungi slotlar to'lganmi, har video QC PASS va bg_reuse PASS mi?
2. Har publish holati vidiq_social_post_status = completed (failed bo'lsa — sabab va qayta urinish vaqti).
3. Tadqiqot, izohlar, Instagram, results.md bugun yangilanganmi?
4. Kechikkan/ochiq ish bo'lsa — darhol shu sessiyada bajar yoki keyingi ishga tushishga aniq vaqt bilan yoz.
Natija: `docs/changes.md` ga 1 qator + Shohjahonga 6 qatorli hisobot (C da): ko'rishlar, yutgan/yutqazgan format, bugun chiqqanlar, ertangi reja, "Shohjahondan kerak".

## QILA OLMAYDIGANLAR (Shohjahonga ochiq aytiladi)
Jonli 2D animator va jonli ovoz aktyori — o'rniga AI fon/rasm + ElevenLabs; TikTok — ulanmagan; YouTube Studio'da qo'lda bajariladigan tasdiqlar (MFA) — Shohjahon.
