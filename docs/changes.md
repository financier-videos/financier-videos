# O'ZGARISHLAR JURNALI — ishlab chiqarishga ta'sir qiladigan har yangilik (har chat yozadi)
Shohjahon 2026-11-21: "boshqa chatda yangiliklar qilsak ham sen eski holatda video chiqarasan — bu yaxshi emas".
QOIDA: dvigatel, spec qoidasi, QC, ovoz, uslub o'zgarsa — shu jadvalga 1 qator (eng yangisi pastda), keyin push. "QAYTA RENDER: HA" — hali chiqmagan videolar ham shu o'zgarish bilan qayta yasalishi SHART (slotgacha ≥60 daqiqa bo'lsa); "YO'Q" — faqat keyingi videolardan. Dvigatel o'zgarsa ENGINE_VERSION ni oshir.
Ishlab chiqaruvchi (vazifa/chat): HAR render va HAR post oldidan `git pull --rebase origin media`, so'ng shu faylni oxirgi ishidan beri o'qi; qc_gate 0-qadami eski render yoki orqada qolgan repoda FAIL beradi.

| Vaqt (UTC) | Kim | Nima o'zgardi | Qayta render |
|---|---|---|---|
| 2026-11-21 14:15 | vazifa sessiyasi | dvigatel v6.9: spec "bg_bright" (fon yorqinligi A/B); natija JSON'da "engine", "engine_sha", "rendered_at" | QAYTA RENDER: YO'Q |
| 2026-11-21 14:15 | vazifa sessiyasi | QC darvozasi (engine/qc_gate.py) majburiy: 0 yangilik, platforma, LUFS, qora kadr, eksport, voice/prosody, sarlavha, kontakt-varaq, rang | QAYTA RENDER: YO'Q |
| 2026-11-21 14:15 | vazifa sessiyasi | rang qoidalari (notes/2026-11-21_color.md): qizil kichik matn yo'q, 1 theme + oltin + 1 urg'u | QAYTA RENDER: YO'Q |
