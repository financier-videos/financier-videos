# G'OLIBLARDAN SABOQ — 2026-11-21 kechqurun (vidIQ Pro: 2 ta "watch" kadrma-kadr tahlil, 4 transkript, 3 outlier qidiruv; ~50 kredit)
Uslub va tuzilma olinadi; matn, kadr, personaj, brend lavhasi KO'CHIRILMAYDI.

## O'LCHANGAN FARQ (eng muhimi)
| Ko'rsatkich | G'oliblar | Biz (navbatdagi videolar) |
|---|---|---|
| Kadr almashinuvi | 60 s da 41 kadr; 47 s da 31 kadr → har ~1.5 s da yangi tasvir | 30 s da 9–10 sahna → har ~3.2 s |
| Subtitr | 1–3 so'z, nutq bilan sinxron, pastki-markaz yoki markaz, oq + qora kontur | 2 qator jumla + tepada doimiy sarlavha |
| Yorqinlik | yorqin, to'yingan sahnalar (kechki sahna — ataylab, 1–2 marta) | hammasi qorong'i (0.14–0.19) |
| Temp (so'z/s) | 2.7–3.2 | 2.3 |
| Boshlanish | harakat yoki savol 1-soniyada; kirish yo'q | da'vo + "Wait...?" |
| Javob | oxirgi 3–5 soniyada; oxiri boshiga ulanadi (loop yoki "callback") | 1-jumlada aytib qo'yiladi |
| Statistika | hikoyalarda 0 ta; "taxmin–javob"da har 5 s da bitta | har sahnada raqam |
| Tovush | har harakatga o'z effekti (qo'ng'iroq, tanga, kalit) | effektlar bor, lekin kam |

## 5 TA ISHLAYOTGAN TUZILMA (dalil bilan)
1. SABAB HIKOYASI — "Why Prices End In 99 Cents" (2.9K → 1.1M), "Why Physics Books Use This Kid's Name" (1K → 2.8M, 47 s), "The Actor Who Invented the Backpack Parachute" (18.6K → 3.9M, 65 s). Personaj + adolatsizlik/mojaro + burilish + oxirida 1-sahnaga qaytish ("callback": boshidagi haqorat oxirida g'alabaga aylanadi).
2. MASSHTAB NARVONI — "How Big Is a Trillion?" (19.7K → 2.6M, 85 s): ikki ovoz, 7 pog'ona.
3. TAXMIN–JAVOB — "How Fast Companies Make $1 Million" (15.6K → 550K, 47 s): savol → mehmon taxmin qiladi → haqiqiy javob; 8 marta takror; oxiri "men shu jumlani tugatguncha..." (real vaqt taqqosi).
4. MIJOZ SUHBATI (Rocco uchun) — "Don't Fall For This Scam" (46K → 2.2M, 66 s): biri "menga pul keldi!" deydi, ikkinchisi "to'xta, tegma" deb tushuntiradi → aniq himoya qadami.
5. "BUNI QILMA" — "Don't type 'No' on WhatsApp" (1.2M), bank PSA lari (2.5M, 1.4M): bitta aniq harakat taqiqi sarlavhada.

## BIZGA QOIDA (script_rules.md va looks.md ga qo'shildi)
- TASVIR TEMPI: har ≤2 s da yangi kadr (sahna ichida "shots" ro'yxati: plan o'zgarishi, yaqinlashish, boshqa lavha, yangi buyum). 30 s video ≥15 kadr, 60 s ≥30 kadr. look_check ga "kadr soni" o'lchovi qo'shiladi.
- SUBTITR: 1–3 so'z, nutq bilan sinxron; doimiy sarlavha yo'q (faqat 1-kadrda hook yozuvi 1.5–2 s).
- JAVOBNI KECHIKTIR: sarlavha savol bo'lsa, javob oxirgi 5 s da; oxirgi kadr 1-kadrga ulanadi.
- IKKINCHI OVOZ: taxmin–javob va suhbat formatlari uchun (Buck + "mehmon"; Rocco + "mijoz"). ElevenLabs'da ikkinchi ovoz tanlanadi (bepul kutubxonadagi, real shaxs nusxasi emas).
- CHEKLOVLARIMIZ o'zgarmaydi: brend do'koni/logotipi lavhasi yo'q (g'olib №3 buni qilgan — biz qilmaymiz: o'rniga o'z grafikamiz va umumiy lavha); musiqa yo'q — o'rniga ritmik sintez effektlar va har harakatga tovush.
