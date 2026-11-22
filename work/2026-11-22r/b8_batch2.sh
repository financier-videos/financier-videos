#!/bin/bash
cd /home/user/financier-videos
source <(sed -n '/^M=/,/^}/p' work/2026-11-22r/b8_batch.sh)
run r08_fees 2026-11-23_fees_r08_b8.mp4 "5 Fees You Paid Without Noticing" 2026-11-23_pink_r07_b8.mp4 2026-11-23_cart_r06_b8.mp4 2026-11-22_bfcm_r05_b8.mp4 2026-11-22_airport_r04_b8.mp4
run r03_subs 2026-11-24_subs_r03_b8.mp4 "What \$111 a Month Really Is" 2026-11-24_noseat_r02_b8.mp4 2026-11-23_fees_r08_b8.mp4 2026-11-23_pink_r07_b8.mp4 2026-11-23_cart_r06_b8.mp4
