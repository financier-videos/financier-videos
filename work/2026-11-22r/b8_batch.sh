#!/bin/bash
# BUYURTMA 8: render + QC the queued Financier videos one by one (memory: never in parallel)
cd /home/user/financier-videos
M="--model /tmp/kokoro/kokoro-v1.0.int8.onnx --voices /tmp/kokoro/voices-v1.0.bin"
SK="Skillar: footage_bank (Buyurtma 8), Ko'rik 3 layout fixes, empty_check, qc_gate; ishlatilmadi: vidiq_find_broll (bank yetarli)"
run() { # name out title prev...
  n=$1; o=$2; t=$3; shift 3
  python3 -I engine/make_video.py work/2026-11-22r/${n}_b8.json $o $M > work/2026-11-22r/${n}_b8_rendered.json 2>work/2026-11-22r/${n}_b8.err
  python3 engine/qc_gate.py $o --spec work/2026-11-22r/${n}_b8.json --rendered work/2026-11-22r/${n}_b8_rendered.json --title "$t" --prev "$@" --skills "$SK" --out work/2026-11-22r/${n}_b8_qc.json > work/2026-11-22r/${n}_b8_qc.txt 2>&1
  echo "$n $(tail -1 work/2026-11-22r/${n}_b8_qc.txt)"
}
run r04_airport 2026-11-22_airport_r04_b8.mp4 "Airport Prices Have a Legal Limit" 2026-11-22_gta_timeline_b8.mp4 2026-11-22_gta_how_big_v615.mp4 2026-11-22_gta_per_second.mp4 2026-11-21_twenty_secrets_b3.mp4
run r05_bfcm 2026-11-22_bfcm_r05_b8.mp4 "Friday or Monday: Guess Who Wins" 2026-11-22_airport_r04_b8.mp4 2026-11-22_gta_timeline_b8.mp4 2026-11-22_gta_how_big_v615.mp4 2026-11-22_gta_per_second.mp4
run r06_cart 2026-11-23_cart_r06_b8.mp4 "Why Shopping Carts Keep Getting Bigger" 2026-11-22_bfcm_r05_b8.mp4 2026-11-22_airport_r04_b8.mp4 2026-11-22_gta_timeline_b8.mp4 2026-11-22_gta_how_big_v615.mp4
run r07_pink 2026-11-23_pink_r07_b8.mp4 "Pink or Blue? One Costs More 42% of the Time" 2026-11-23_cart_r06_b8.mp4 2026-11-22_bfcm_r05_b8.mp4 2026-11-22_airport_r04_b8.mp4 2026-11-22_gta_timeline_b8.mp4
run r08_fees 2026-11-23_fees_r08_b8.mp4 "5 Fees You Paid Without Noticing" 2026-11-23_pink_r07_b8.mp4 2026-11-23_cart_r06_b8.mp4 2026-11-22_bfcm_r05_b8.mp4 2026-11-22_airport_r04_b8.mp4
run r02_noseat 2026-11-24_noseat_r02_b8.mp4 "They Sold Your Seat Twice" 2026-11-23_fees_r08_b8.mp4 2026-11-23_pink_r07_b8.mp4 2026-11-23_cart_r06_b8.mp4 2026-11-22_bfcm_r05_b8.mp4
run r03_subs 2026-11-24_subs_r03_b8.mp4 "What \$111 a Month Really Is" 2026-11-24_noseat_r02_b8.mp4 2026-11-23_fees_r08_b8.mp4 2026-11-23_pink_r07_b8.mp4 2026-11-23_cart_r06_b8.mp4
# rerun airport with varied footage (first pass: 12 cuts < 13)
run r04_airport 2026-11-22_airport_r04_b8.mp4 "Airport Prices Have a Legal Limit" 2026-11-22_gta_timeline_b8.mp4 2026-11-22_gta_how_big_v615.mp4 2026-11-22_gta_per_second.mp4 2026-11-21_twenty_secrets_b3.mp4
run r05_bfcm 2026-11-22_bfcm_r05_b8.mp4 "Friday or Monday: Guess Who Wins" 2026-11-22_airport_r04_b8.mp4 2026-11-22_gta_timeline_b8.mp4 2026-11-22_gta_how_big_v615.mp4 2026-11-22_gta_per_second.mp4
