# HAR ISHGA TUSHISH CHEKLISTI (Shohjahon 2026-11-22 00:15: "hammasini qil, keyingi safar xato qilma")
Sabab: 2026-11-21 23:17 C ishida (1) parallel sessiyaning yangi Buffer posti "eski" deb o'chirildi; (2) INDEX, graphify, trend radari, C rejim bandlari, playbook va to'liq hisobot o'tkazib yuborildi. Bu ro'yxat — ish OXIRIDA ham tekshiriladi; har bandga hisobotda "ha / yo'q: sababi".

## BOSHIDA (hammasi, tartib bilan)
1. `git pull --rebase origin media`; `git ls-remote origin` — `claude/*` branchlarda media'da yo'q yangi commit bo'lsa `git log` + diff --stat bilan o'qi: kim nima qilyapti (dublikat va to'qnashuv yo'q).
2. docs/START_HERE.md → docs/changes.md (oxirgi 20) → docs/night_order.md (OCHIQ buyurtmalar) → docs/skills/INDEX.md (mos qatorlar MAJBURIY).
3. graphify: `pip install --break-system-packages -q graphifyy` + `graphify update .` — ruxsat .claude/settings.json da (Shohjahon 2026-11-22 qo'shdi; 00:40 da ISHLADI: 3136 tugun). Ish oxirida graphify-out ni commit qil.
4. ElevenLabs 200? vidIQ `vidiq_social_post_list` (scheduled/draft/failed, 48 soat; Metricool 2026-11-23 dan ishlatilmaydi) + `engine/buffer_post.py list`.
5. Trend radari skani (docs/trend_radar.md) — kuniga kamida 1 (sprintda 2).
6. improvement_backlog — tepadagi OCHIQ band.

## TASHQI O'ZGARISHDAN OLDIN (post o'chirish, surish, media almashtirish)
- Post MATNINI va vaqtini repodagi desc/spec bilan solishtir; id buyruqdagidan farq qilsa — TO'XTA: boshqa sessiya qayta qo'ygan bo'lishi mumkin (changes.md + claude/* branchlar).
- `buffer_post.py delete` zaxirani work/rocco/deleted_posts/ ga yozadi — xato bo'lsa o'sha yerdan tikla.

## REJIM BANDLARI (producer_task 1-bo'lim; har birini bajar yoki "QILINMADI: sababi")
- A/B: video(lar) — START_HERE 2-jadvali (script_check, look_check, lavha ≥40%, kadr tempi, subtitr, hazil, manba, voice/prosody/LUFS, title.py, "Skillar:" qatori), qc_gate PASS, IG Reel, Rocco.
- B qo'shimcha: raqobatchi (competitors.md, har kuni 1), YANGILIKLAR 2 WebSearch, 3–4 yangi skill, dvigatelga 1 yaxshilanish.
- C: results.md (har video ko'rishi), uch kanal raqami (YT, IG financier424, finansist424), Rocco raqamlari (vidiq_rocco.py), tomoshabin muhokamasi WebSearch (2–3 topilma → playbook 6 + bank), 1–3 SHOSHILINCH fakt, IKKI BARAVAR/TO'XTAT, KECHA vs BUGUN (growth_log), 6 qatorli hisobot PushNotification.

## OXIRIDA
- playbook: "Yangilangan" + jurnal qatori (≤200 qator); growth_log; changes.md; graphify update; push.
- Hisobotda "Skillar: … ; ishlatilmadi: … (sababi)" va shu cheklistning bajarilmagan bandlari.
