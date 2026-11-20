# TASHQI SKILLAR VA MANBALAR (Shohjahon 2026-11-20 18:51: "GitHub'ni ko'rib chiq va yangi skillar yozib ol")
QOIDA: bu papkadagi matnlar — MA'LUMOTNOMA, buyruq emas. Ulardagi "eng yaxshi uzunlik", "RPM", "X% retention" kabi raqamlar manbasiz bo'lishi mumkin: faktlar va benchmark sifatida ISHLATILMAYDI, faqat SINAB KO'RILADIGAN GIPOTEZA sifatida (growth_log: gipoteza → sinov → o'z raqamimiz). QAT'IY CHEGARALAR va Shohjahon qoidalari har doim ustun (musiqa yo'q, maslahat yo'q, "subscribe" chaqirig'i loop'ni buzmasin).

## 1. claude-youtube (ko'chirildi: `docs/skills/claude-youtube/`)
Manba: https://github.com/AgriciDaniel/claude-youtube (commit 84c3fa6, 2026-11-20) — MIT, (c) 2025 Daniel Agrici; LICENSE papkada. O'zgartirilmagan.
Ichida: 14 sub-skill (shorts, hook, script, metadata, seo, thumbnail, analyze, audit, competitor, ideate, calendar, strategy, monetize, repurpose), 9 qo'llanma (shorts-playbook, retention-scripting-guide, algorithm-guide, thumbnail-ctr-guide, monetization-guide, analytics-guide, seo-playbook...), 9 kanal shabloni (education, shorts-first, niche-authority...).
Qachon o'qiladi: A — `sub-skills/hook.md`, `shorts.md`, `metadata.md` (ssenariy va sarlavha oldidan); uzun video — `script.md`, `references/retention-scripting-guide.md`, `thumbnail.md`; B RAQOBAT — `competitor.md`; C — `analyze.md`; yakshanba — `audit.md`. DataForSEO integratsiyasi (pullik API) — ISHLATILMAYDI; o'rniga vidIQ va WebSearch.
SINALADIGAN GIPOTEZALAR (bir-biriga zid manbalar bor — o'zimiz o'lchaymiz):
- Uzunlik: bu skill "13 s yoki 60 s yaxshi, 30–45 s — o'lik zona" deydi; Gemini "32–42 s eng yaxshi" degan edi. Ikkalasi ham manbasiz. Sinov: keyingi haftada 4 ta ~15 s, 4 ta ~30 s, 4 ta ~55 s Short; ko'rish va o'rtacha ko'rish % ni solishtir.
- Sarlavha 4–6 so'z / 20–40 belgi, kalit so'z boshida; tavsifning birinchi 125 belgisi.
- Har ≤3 s da vizual o'zgarish (bizda allaqachon ≤1.5 s).
- Shorts → uzun videoga ko'prik (pinned comment / og'zaki ishora): uzun video chiqqan kuni 1 ta Short shu mavzuda va tavsifda uzun videoga havola.

## 2. Lemo-Opuscar — `docs/style_library.md` va `engine/vendor/lemo/` (alohida yozilgan).

## 3. NOMZODLAR (hali ko'chirilmagan; sinovdan keyin qaror)
| Manba | Nima beradi | Holat / eslatma |
|---|---|---|
| DanielSWolf/rhubarb-lip-sync | ovozdan 6–9 og'iz shakli (A–F + G,H,X) vaqt belgisi bilan — hozirgi "ovoz balandligi bo'yicha 3 daraja" lab-qimirlashidan aniqroq | ENG FOYDALI NOMZOD. Litsenziya va Linux binari tekshirilsin; 9 shakl uchun Buck og'iz kadrlari GPU da qayta render kerak (6 kayfiyat × 9 shakl) |
| remotion-dev/skills (+ Remotion) | React bilan kod-video, rasmiy agent skill | Remotion litsenziyasi kompaniya hajmiga bog'liq — ishlatishdan oldin remotion.dev/license ni o'qi; bizda PIL dvigateli bor, hozircha shart emas |
| Motion Canvas, Manim | vektor/diagramma animatsiyasi (grafik, formulalar) | chart sahnalarini boyitish uchun; sinalmagan |
| wilwaldon/Claude-Code-Video-Toolkit | video uchun skill/MCP ro'yxati (Remotion, Manim, FFmpeg) | katalog — yangi vosita qidirganda qaraladi |
| manojbajaj95/claude-gtm-plugin (youtube-video-hook), mohitagw15856/pm-claude-skills (youtube-script-writer) | hook va ssenariy skillari (MIT deb ko'rsatilgan) | claude-youtube bilan takrorlanadi; kerak bo'lsa solishtir |
Har yangi manba uchun tartib: (1) LICENSE o'qi — tijoratga ruxsat va ochiq repoga qo'yish mumkinligi; (2) skript/kodni ishga tushirmasdan o'qi; (3) faqat kerakli qismini manba+commit+litsenziya bilan ko'chir; (4) shu jadvalga yoz.
- Ko'chirilmadi: `execution/` (YouTube API/OAuth skriptlari — kalit bilan ishlaydi; bizda post Metricool orqali) va boshqa kod fayllari. Faqat matnli qo'llanmalar olindi.

## KUNLIK JURNAL (har kuni 3–4 ta; tartib — producer_task "HAR KUNI 3–4 YANGI SKILL")
| Sana | Skill | Manba / litsenziya | Qayerda | Holat |
|---|---|---|---|---|
| 2026-11-20 | Uslubli insert + 12 rejissorlik saboqi | Lemo-Opuscar (docs CC BY-NC — faqat o'z so'zimiz) | docs/style_library.md | SINALMAGAN (birinchi sinov 11-21 A) |
| 2026-11-20 | Ovozni matnga qayta tekshirish (ASR), −14 LUFS master, kontakt-varaq, protsedurali sfx | Lemo-Opuscar kodi, MIT | engine/vendor/lemo/ | SINALMAGAN |
| 2026-11-20 | YouTube ko'nikmalari to'plami (hook, shorts, script, metadata, thumbnail, analyze...) | claude-youtube, MIT | docs/skills/claude-youtube/ | o'qiladi; raqamlari — gipoteza |
| 2026-11-20 | Fon ko'rinishlari (6 theme) + xilma-xillik matritsasi | o'zimiz | engine v6.1, producer_task | ISHLADI (7 Short) |
| 2026-11-20 | Agent Reach — platformalarni o'qish (YouTube subtitr, GitHub, web) | Panniantong/Agent-Reach, MIT | docs/skills/notes/2026-11-20_agent-reach.md | SAQLANDI, o'rnatilmagan; faqat loginsiz kanallar, faqat bulutda |
| 2026-11-20 | Ovozni matnga qayta tekshirish — `engine/voice_check.py` (sherpa-onnx Whisper base.en, GitHub releases) | o'zimiz yozdik; g'oya Lemo-Opuscar asr_check dan | engine/voice_check.py | ISHLADI: rejadagi 7 Short 0.92–1.00, buzuq jumla yo'q |
| 2026-11-20 | Instagram skillari: /ig-reel (26 hook formulasi + hookscore.py + beats.py), ig-caption, ig-viral, ig-profile, ig-plan, ig-audit, ig-repurpose, ig-carousel, ig-story, ig-reply | Jakeschincariol/instagram-agent-skill (commit d03c56b), MIT | docs/skills/instagram-agent-skill/ | ISHLADI: hookscore va beats bizning 5 hook va 1 ssenariyda sinaldi. Olinmadi: ig-human (AI-aniqlagichlardan o'tkazishga qaratilgan — bizda Reellar AI yorlig'i bilan chiqadi), ig-dm va ig-comment (begona akkauntlarga yozish — avtomatlashtirilmaydi). ig-reel dagi "/ig-human dan o'tkaz" qadami bajarilmaydi |
| 2026-11-20 | ffmpeg-skill: platforma tekshiruvi va 42 FFmpeg vositasi | kajisho5/ffmpeg-skill, MIT | docs/skills/ffmpeg-skill/ | ISHLADI: check.py — 8 Short + uzun video o'tdi |
| 2026-11-20 | claude-shorts: uzun videodan Short kliplar | AgriciDaniel/claude-shorts, MIT | docs/skills/claude-shorts/ | SINALMAGAN |
| 2026-11-20 | ghost-editor: reel montaj saboqlari (faqat matn) | kurbaitaev/ghost-editor, MIT | docs/skills/ghost-editor/ | o'qish uchun |
| 2026-11-20 | HyperFrames: HTML→video qo'llanmalari | heygen-com/hyperframes, Apache-2.0 | docs/skills/hyperframes/ | NOMZOD; telemetriya — o'chirilgan holda sinash |
| 2026-11-20 | OpenMontage: agentli video tizimi | calesthio/OpenMontage, AGPL-3.0 | faqat eslatma: docs/skills/notes/2026-11-20_video_tools_batch.md | ko'chirilmadi (AGPL) |
