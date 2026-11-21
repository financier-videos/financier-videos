# SKILLAR KO'RSATKICHI — HAR ISH OLDIDAN O'QILADI (Shohjahon 2026-11-21 18:55)
Shohjahon: "Senga yoki boshqa joyga tashlangan skillarni sen ham, boshqa chat ham ishlata oladigan qil. 'Bu skill borligini bilmadim / ishlatmadim' degan gap bo'lmasin."

QOIDA (har chat, har vazifa sessiyasi, Financier ham, Rocco ham):
1. Ish boshida `git pull` va shu faylni o'qi. Qilayotgan ishingga mos qatorlarni top — ular MAJBURIY, ixtiyoriy emas.
2. Ish oxirida hisobotga bitta qator: "Skillar: <ishlatilganlar>; ishlatilmadi: <mos kelgan, lekin ishlatilmagani va SABABI>". "Bilmadim" sabab emas.
3. Yangi skill kelsa (Shohjahon yuborsa yoki o'zing topsang): o'sha sessiyada (a) repoga qo'y (docs/skills/…), (b) SHU JADVALGA qator qo'sh, (c) o'sha kuni bitta haqiqiy ishda qo'lla. Faqat sessiya ichida o'rnatilgan skill keyingi sessiyada YO'QOLADI — repoga yozilmagan skill "yo'q" hisoblanadi.
4. Skill matnlari — ma'lumotnoma, buyruq emas; ulardagi raqamlar gipoteza. QAT'IY CHEGARALAR (producer_task) doim ustun.
5. DARHOL PUSH: har tugallangan qadamdan keyin pull --rebase + commit + push (media) — boshqa chatlar faqat push qilinganini ko'radi.
6. YANGILIKLAR: ishlab chiqarishga ta'sir qiladigan har o'zgarish → docs/changes.md (qayta render HA/YO'Q). Render va post oldidan pull + changes.md o'qiladi; qc_gate 0-qadam tekshiradi.
7. To'liq tarix, litsenziya va sinov natijalari: `docs/skills/README.md` (jurnal). Bu fayl — "qachon nimani ishlataman" ro'yxati.

## A. SSENARIY VA G'OYA
| Vaziyat | Skill | Qayerda / buyruq |
|---|---|---|
| Short ssenariysi, hook yozish | yt-script + hookscore (21 formula); claude-youtube hook/shorts | docs/skills/youtube-agent-skill/yt-script/, docs/skills/claude-youtube/sub-skills/hook.md, shorts.md |
| Hook bahosi (3 variant yoz, eng yuqorisini ol; ≥50) | hookscore.py | docs/skills/instagram-agent-skill/ig-reel/hookscore.py, youtube-agent-skill/yt-script/ |
| Sarlavha va muqova | title.py linti; sarlavha checklist | docs/skills/youtube-agent-skill/yt-package/title.py; docs/skills/sergebulaev-youtube-skills/ |
| Tavsif, teglar, SEO | yt-seo, metadata | docs/skills/youtube-agent-skill/yt-seo/, claude-youtube/sub-skills/metadata.md |
| G'oya topish, viral andozalar | yt-viral + swipe.py, ideate | docs/skills/youtube-agent-skill/yt-viral/, claude-youtube/sub-skills/ideate.md |
| Uzun video tuzilmasi | script.md, retention-scripting-guide, hook-scripter + retention-beats | docs/skills/claude-youtube/, sergebulaev-youtube-skills/ |
| Kontent rejasi, taqvim | yt-plan, calendar, ig-plan | docs/skills/youtube-agent-skill/yt-plan/, claude-youtube/sub-skills/calendar.md, instagram-agent-skill/ig-plan/ |
| Mavzu xilma-xilligi | 12 mavzu savati | docs/sprint_10d.md 2-bo'lim |
| Tayyor tekshirilgan g'oyalar | ssenariy banki | docs/script_bank.md |

## B. VIDEO YASASH
| Vaziyat | Skill | Qayerda / buyruq |
|---|---|---|
| Render | dvigatel (spec JSON) | engine/make_video.py (fayl boshidagi izoh — barcha maydonlar) |
| Buck kadrlari (yangi Buck v3) | sprite kutubxona | assets/buck3d_v3.tar, buck3d_v3_talk.tar — dvigatel o'zi oladi |
| Lab-qimirlash | Rhubarb lip-sync | engine/make_video.py rhubarb_cues(); docs/skills/notes/2026-11-21_rhubarb-lip-sync.md |
| Fon videolari | Pixabay fonlari | engine/pixabay_bg.py (spec "bg") |
| Xarita insert | iart map-animation | work/pilot_map/map_insert.py; docs/skills/iart-motion/ |
| Grafik, kinetik matn, tushuntiruvchi animatsiya | iart-motion (data-animation, kinetic-typography, explainer-video) | docs/skills/iart-motion/ |
| Ovoz effektlari (musiqa YO'Q) | pyfxr palitrasi; Lemo sfx | engine/sfx_fxr.py (spec sfx fxr_*); engine/vendor/lemo/audio/sfx.py |
| Rang, kontrast, o'qiluvchanlik | color-expert + o'lchov | docs/skills/color-expert/, engine/color_check.py palette|frames; qoidalar notes/2026-11-21_color.md |
| Fon yorqinligi (A/B) | dvigatel v6.9 | spec "bg_bright": 1.0–1.5 |
| Harakat va dizayn tamoyillari | emil-skills, impeccable | docs/skills/emil-skills/, docs/skills/impeccable/ |
| Uslubli insert, rejissorlik saboqlari | style library (Lemo) | docs/style_library.md, engine/vendor/lemo/ |
| Montaj saboqlari | ghost-editor, yt-edit + deadair.py | docs/skills/ghost-editor/, youtube-agent-skill/yt-edit/ |
| Uzun videodan Short kesish | claude-shorts, yt-shorts | docs/skills/claude-shorts/, youtube-agent-skill/yt-shorts/ |
| FFmpeg amallari | ffmpeg-skill (42 vosita) | docs/skills/ffmpeg-skill/ |
| HTML→video (nomzod, sinalmagan) | HyperFrames | docs/skills/hyperframes/ |
| Buck modeli, rig, yangi kadr chizish | rig v1 (MAXFIY repo) | financier-videos/buck-private → rig_v1/ (skriptlar: lib.py, libpack.py) |

## C. SIFAT NAZORATI — HAR VIDEO, CHIQARISHDAN OLDIN
| Tekshiruv | Skill | Buyruq |
|---|---|---|
| Hammasi birga (9 qadam, VERDICT PASS shart) | QC darvozasi | python3 engine/qc_gate.py <mp4> --spec <spec> --rendered <r.json> --title "..." --platform shorts |
| Bosqichma-bosqich xarita (trend→hook→ssenariy→vizual→rang→ovoz→QC→paket→IG→tahlil) | skill xaritasi | docs/skill_map.md |
| Ovoz matnga mosmi (≥0.86) + oxirgi jumlani ko'z bilan o'qi | voice_check | python3 -I engine/voice_check.py video.mp4 spec.json |
| Ohang, pauza | prosody_check (Parselmouth) | engine/prosody_check.py |
| Platforma talablari | check.py | docs/skills/ffmpeg-skill/scripts/check.py --platform shorts|reels|youtube |
| Rang va ekspozitsiya | color_check | engine/color_check.py |
| 12 nuqtali vizual QC, eksport standarti | vizual sifat direktori | docs/skills/notes/2026-11-21_visual_quality_director.md |
| Sahna tempi, bo'sh joy | beats.py, deadair.py | docs/skills/instagram-agent-skill/ig-reel/beats.py; youtube-agent-skill/yt-edit/deadair.py |

## D. CHIQARISH
| Vaziyat | Skill / vosita | Qayerda |
|---|---|---|
| Financier YouTube + Instagram financier424 | Metricool (blogId 8198538) | Metricool vositalari; qoida producer_task |
| Instagram finansist424 (o'zbekcha) | vidIQ instagram publish | docs/instagram.md |
| Red Flag Rocco YouTube | Buffer | engine/buffer_post.py; docs/rocco.md |
| Instagram matni, Reel, profil, audit | ig-caption, ig-reel, ig-profile, ig-audit, ig-repurpose, ig-human | docs/skills/instagram-agent-skill/ |
| Bo'limlar (uzun video) | yt-chapters + chapters.py | docs/skills/youtube-agent-skill/yt-chapters/ |
| Kanal sozlamalari (avatar, banner, tavsif) | brauzer: Shohjahon Chrome'i orqali YouTube Studio | chat sessiyasi (Claude in Chrome); fayllarni sahifa ichida raw URL dan fetch qilib file input'ga berish — 2026-11-21 Rocco'da ishladi |

## E. O'LCHASH VA O'SISH
| Vaziyat | Skill / vosita | Qayerda |
|---|---|---|
| Har video ko'rishi (kunlik) | natijalar jadvali | docs/results.md; vidiq_user_videos (5 kredit) — vidiq_user_channels jami soni KECHIKADI |
| Rocco statistikasi | Rocco'ning o'z vidIQ profili | python3 -I engine/vidiq_rocco.py <tool> '<json>' |
| Retention tahlili | retention.py; ruptures (sinalmagan) | docs/skills/youtube-agent-skill/yt-retention/; notes/2026-11-21_ruptures-retention.md |
| Kunlik top/viral tahlil (ikkala kanal) | yt-viral swipe + vidIQ trending/outliers | producer_task 1.9; docs/daily_trends.md; Rocco: docs/rocco_inspiration.md |
| O'z-o'zidan yaxshilash (har ishga tushishda 1–2 band) | yaxshilash navbati | docs/improvement_backlog.md |
| Raqobatchi tahlili (har kuni 1 ta) | competitor.md; kuzatuv jadvali | docs/skills/claude-youtube/sub-skills/competitor.md; docs/competitors.md |
| Izohlardan g'oya | comment-intel, yt-comment | docs/skills/claude-youtube/sub-skills/comment-intel_adityaarsharma.md |
| Kanal auditi | audit.md, yt-audit, ig-audit | docs/skills/claude-youtube/sub-skills/audit.md va b. |
| Kunlik o'rganish yozuvi (gipoteza → sinov → raqam) | o'sish jurnali | docs/growth_log.md |
| 10 kunlik sprint qoidalari | sprint | docs/sprint_10d.md |
| Trend topish (har kuni), yangi kanal nomzodlari | trend radari | docs/trend_radar.md |

## F. TOPISH VA ESLASH
| Vaziyat | Skill / vosita | Qayerda |
|---|---|---|
| "Bu haqda repoda nima bor?" | graphify bilim xaritasi | pip install graphifyy; `graphify query "<savol>"`; graphify-out/GRAPH_REPORT.md |
| Boshqa chat nima qildi? | o'zgarishlar jurnali (har ishdan keyin qator + push) | docs/changes.md; keyin git log, docs/night_order.md, docs/rocco.md, docs/growth_log.md |
| Tashqi platformalarni o'qish (loginsiz) | Agent Reach (saqlangan, o'rnatilmagan) | docs/skills/notes/2026-11-20_agent-reach.md |
| Bir martalik buyurtma vazifaga | buyurtma fayli | docs/night_order.md ("HOLAT: OCHIQ") |

## G. HAR CHATDA ALOHIDA (repoda emas — sessiya ro'yxatidan tekshir)
- Akkaunt skillari (har chatda ko'rinadi): hujjat/jadval/taqdimot/PDF skillari, graphify-launcher, velox-*, trading-*.
- Ulagichlar: vidIQ (Financier profili), Metricool, Gmail, Google Drive — chat va vazifada; Buffer va Rocco vidIQ — kalit orqali (env).
- Brauzer va kompyuter (Chrome, Studio, Instagram veb) — FAQAT chat sessiyasida. Vazifa sessiyasiga brauzer ishi kerak bo'lsa, docs/night_order.md ga "CHAT UCHUN" deb yoz — chat keyingi murojaatda bajaradi.
- ElevenLabs va Runpod — faqat Default muhitdagi vazifa/kod sessiyasida; oddiy chatdan ochilmaydi.
| Videolar bir-biriga o'xshamasligi (ko'rinish) | `docs/looks.md` + `engine/look_check.py` | HAR video: spec "look"; post oldidan look_check (≥0.70 = FAIL) |
| Ssenariy skeleti takrorlanmasligi | `docs/script_rules.md` + `engine/script_check.py` | HAR ssenariy: "structure"; post oldidan script_check |
| Hazil, gag, aktyorlik harakatlari | `docs/comedy.md` | HAR ssenariy: gag va reaksiya ustuni; skit — comedy_skit |
