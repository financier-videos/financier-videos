# Kino darajasidagi vizual: grafika, joylar, effektlar — tadqiqot (2026-11-21, Shohjahon so'radi)
Maqsad: har videoda boshqa grafika, boshqa "joy" (shahar, xarita, do'kon, aeroport), kino effektlari. Bizda: PIL+ffmpeg dvigatel v6.4 (kamera, parallaks, grading, blur), 3D Buck kutubxonasi (faqat chat sessiyasida render), Playwright/Chromium (konteynerda bor), GPU yo'q (4 yadro).

## 1. O'RNATILDI — iart-ai motion skills (MIT, 7 to'plam, faqat matn) → `docs/skills/iart-motion/`
- map-animation: Vox uslubidagi xarita (zoom, pin, marshrut, 12 fps "stutter"). QO'LLANDI → pilot quyida.
- data-animation: chart-animation (bar chart race, sanagich — "qiymat = kadrning funksiyasi"), animated-infographic, presentation-video.
- explainer-video: isometric-animation, whiteboard, diagram-animation, "wrapped" uslubi.
- kinetic-typography, motion-design (animatsiya tamoyillari, shot-composition, color-motion, motion-background).
- webgl-animation (three.js, shader, particle), javascript-animation (canvas filmlar). "soundtrack" — MUSIQA, ISHLATILMAYDI.
- Ko'pi Remotion (React) da yozilgan. Remotion litsenziyasi: jismoniy shaxs va ≤3 kishilik kompaniyaga bepul, kattaroqqa pullik (remotion.dev/license) — kanal kimning nomida ekanini Shohjahon tasdiqlamaguncha Remotion O'RNATILMAYDI; tamoyillar PIL dvigateliga ko'chiriladi yoki Playwright bilan HTML/canvas kadrlari olinadi (litsenziya muammosi yo'q).

## 2. PILOT (ishladi): `work/pilot_map/map_insert.py`
4 s, 1080x1920, bepul: AQSh shtatlari (us-atlas 3.0.1, ISC), kamera New York'dan uzoqlashib butun marshrutni ochadi, pinlar tushadi, punktir marshrut chiziladi (12 fps), "$800 ROUND TRIP" yorlig'i. Render ~1 daqiqa (4 yadro). Kadrlar: `work/pilot_map/contact_sheet.png`.
Keyingi qadam: dvigatelga "map" sahna turi (spec: {"map": {"from": "36", "to": "06", "label": "..."}}) — 1 ta Shortda sinov, growth_log ga.

## 3. QO'SHIMCHA KERAK BO'LADIGANLAR (skill emas)
| Nima | Beradi | Narx / ruxsat |
|---|---|---|
| Poly Haven (HDRI, 3D model, tekstura) | kino yorug'ligi, real muhit fonlari | CC0, bepul; API ning alohida shartlari bor — o'qib keyin |
| Kenney City Kit (Suburban, Roads, Industrial, Commercial) | 3D shahar, ko'cha, do'konlar — Buck uchun "joylar" | CC0, bepul |
| Blender (headless, `blender --background --python`) | yuqoridagi aktivlardan 3D sahna render | bepul (GPL — faqat vosita, natija bizniki); GPU kerak (RunPod) |
| Wan 2.2 (Alibaba) image-to-video | rasmdan 5–10 s kino klip (shahar manzarasi, b-roll o'rniga) | Apache-2.0; RunPod Public Endpoint ~$0.30 / 5 s (~$0.06/s). PULLIK → Shohjahon ruxsati. Real odam yuzi, logotip yo'q; Buck'ni AI ga berilmaydi (Tripo modeli maxfiy) |
| LTX-Video | shunga o'xshash | litsenziyasi tijorat uchun daromad chegarasiga bog'liq — OLINMAYDI |
| Pexels/Pixabay API | ko'proq b-roll joylar (hozir vidIQ find_broll: ≤1/video) | bepul, lekin akkaunt + API kalit → Shohjahon ochishi kerak |
| BlenderMCP (ahujasid/blender-mcp) | Claude Blender'ni boshqaradi | desktop Blender kerak — bulut sessiyada foydasiz; headless skript yetarli |
| gl-transitions (ffmpeg-gl-transition) | 60+ GLSL o'tish effekti | ffmpeg'ni qayta yig'ish kerak — hozircha shart emas; o'tishlar dvigatelda bor |

RunPod (2026-11-21 00:30 tekshiruv): rest.runpod.io → 502 (oldin 403). Ishlamaguncha GPU yo'li yopiq.
