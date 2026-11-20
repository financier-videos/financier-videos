# Agent Reach — agent uchun platformalarni o'qish/qidirish vositasi (Shohjahon 2026-11-20 18:59: "shuni ham saqla")
Manba: https://github.com/Panniantong/Agent-Reach — MIT (README bo'yicha; ishlatishdan oldin LICENSE faylini o'qi). Holat: SAQLANDI, O'RNATILMAGAN, SINALMAGAN. README xitoy tilida o'qildi (2026-11-20).

## Nima
Bitta CLI (`agent-reach <kanal> <harakat>`): platformalarni FAQAT O'QIYDI va qidiradi (post yozmaydi, izoh/layk qilmaydi). Kanallar:
- loginsiz (standart): youtube (video ma'lumoti, qidiruv, subtitr; ovozni matnga o'girish uchun Groq/OpenAI kaliti kerak), github (repo, README, issue/PR), web (qidiruv, sahifa o'qish), bilibili, v2ex;
- login talab qiladi: reddit, twitter/X, instagram, facebook, linkedin, xiaohongshu va boshq.
Ichida: yt-dlp, Jina Reader, Exa va boshqa ochiq vositalar.

## Bizga nimasi foydali
1. Raqobatchi Shorts/videolarining SUBTITRLARI va metadata'si — B RAQOBAT tahlilida hook, tuzilma va tempni matn bo'yicha o'rganish (vidIQ transcript kreditini tejaydi).
2. GitHub qidiruvi — "har kuni 3–4 yangi skill" ishi uchun.
3. (faqat login bilan) Reddit — tomoshabin fikri. HOZIR ISHLATILMAYDI: login kerak.

## CHEKLOVLAR (bizning qoidalar bo'yicha — o'zgartirilmaydi)
- Faqat LOGINSIZ kanallar (youtube, github, web) va faqat BULUT sessiyasida. Shohjahon kompyuteriga O'RNATILMAYDI: vosita loginli saytlar uchun Chrome'dagi o'sha sayt loginini o'z brauzeriga nusxalaydi — brauzer sessiyalari/akkauntlariga tegish bizda taqiq. Loginli kanal kerak bo'lsa — Shohjahondan so'raladi (alohida "kichik" akkaunt bilan, o'zi kiradi).
- Hech qanday kalit (Groq/OpenAI) kiritilmaydi; ovozni matnga o'girish — bizdagi faster-whisper bilan.
- O'rnatish: README dagi "install.md ni agentga ber" yo'li ISHLATILMAYDI (begona ko'rsatmani ko'r-ko'rona bajarish). Avval install.md va o'rnatiladigan paketlar ro'yxati O'QILADI, keyin faqat kerakli qism (masalan to'g'ridan yt-dlp) o'rnatiladi. PyPI'dagi `agent-reach` nomli paket bu loyiha EMAS (README ogohlantirishi) — o'rnatma.
- Raqobatchi videosi/audiosi yuklab olinmaydi va qayta ishlatilmaydi — faqat subtitr/metadata tahlil uchun; matni ko'chirilmaydi (faqat format va g'oya).
- YouTube xizmat shartlari: avtomatik yuklab olish cheklangan — kuniga bir necha so'rovdan oshirma; bloklansa aylanib o'tma.

## Birinchi sinov (keyingi B RAQOBAT ishi)
`pip install --break-system-packages yt-dlp` → bitta raqobatchi Short uchun `yt-dlp --skip-download --write-auto-subs --sub-langs en --print title,duration,view_count <url>`; ishlasa — 3 ta eng ko'p ko'rilgan Short hook'ini (birinchi 2 jumla) solishtirib playbook 5-bo'limga yoz. youtube.com hosti muhitda yopiq bo'lsa — growth_log ga yoz va vidIQ transcript bilan davom et.
