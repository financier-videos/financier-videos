# 2026-11-20 A rejim — faqat spec'lar (render YO'Q)
Sabab: ElevenLabs kaliti muhitda bor, lekin cheklangan — `/v1/voices` 401 "missing the permission voices_read"; `/v1/user`, `/v1/models` ham 401 (user_read, models_read yo'q). Ovoz laboratoriyasi (voices_read + voice generation/voices_write) va dvigatel (voice lookup + TTS) ishlamaydi. Kokoro bilan chiqarish taqiqlangan.
- short1_trillion61.json — "$1 Trillion in 61 Days. How Fast Is That?" (= work/t1_61/t1_61_v6.json; b-roll: work/t1_61/*_seg.mp4 → /tmp/fin/broll/). 10:00 ET.
- short2_turkey_flights.json — "Thanksgiving Flights Just Got 17% Pricier" (SHOSHILINCH, 26-noyabrgacha; vs format). 16:00 ET. Render oldidan AAA raqamlarini qayta tekshir, 1 find_broll.
Kalit tuzatilgach: avval voice lab, keyin shu ikki Short.

## 2026-11-20 ~02:05 Toshkent — CHIQARILDI (sessiya financier-videos-78)
DIQQAT, PARALLEL SESSIYA: ikkala Short render qilindi (Buck D, ElevenLabs, cinema, QC o'tdi) va Metricool'ga joylandi. QAYTA POST QILMA.
- 2026-11-20_trillion61.mp4 (40.0 s) → 2026-11-20 10:00 ET. Spec: short1_trillion61_rendered.json
- 2026-11-20_turkeyflights.mp4 (34.9 s) → 2026-11-20 16:00 ET. Spec: short2_turkey_flights_rendered.json
