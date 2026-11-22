#!/bin/bash
# v6.17 cold-open re-render (YT analytics: ~70% swipe away in the first second)
cd /home/user/financier-videos
M="--model /tmp/kokoro/kokoro-v1.0.int8.onnx --voices /tmp/kokoro/voices-v1.0.bin"
SK="Skillar: YT analitika (vidiq_channel_analytics: engaged 30%), cold open + katta yuz 1-kadrda, competitor_watch, eleven_v3, empty_check, qc_gate; ishlatilmadi: —"
run() { n=$1; o=$2; t=$3; shift 3
  python3 -I engine/make_video.py work/2026-11-25c/$n.json $o $M > work/2026-11-25c/${n%%_*}_rendered.json 2>work/2026-11-25c/$n.err
  python3 engine/qc_gate.py $o --spec work/2026-11-25c/$n.json --rendered work/2026-11-25c/${n%%_*}_rendered.json --title "$t" --prev "$@" --skills "$SK" --out work/2026-11-25c/${n%%_*}_qc.json > work/2026-11-25c/${n%%_*}_qc.txt 2>&1
  echo "$n $(tail -1 work/2026-11-25c/${n%%_*}_qc.txt)"; }
run c01_bank 2026-11-25_bank_c01.mp4 "The Bank Charged Me \$4.86 to Get My Own Money" 2026-11-24_subs_r03_b8.mp4 2026-11-24_noseat_r02_b8.mp4 2026-11-23_fees_r08_b8.mp4 2026-11-23_bills_v03.mp4
run v04_print 2026-11-25_print_v04.mp4 "It Costs 11.3 Cents to Print a \$100 Bill" 2026-11-25_bank_c01.mp4 2026-11-24_subs_r03_b8.mp4 2026-11-24_noseat_r02_b8.mp4 2026-11-23_fees_r08_b8.mp4
run v01_buck 2026-11-26_buck_v01.mp4 "1748: Why Your Dollar Is Called a Buck" 2026-11-25_print_v04.mp4 2026-11-25_bank_c01.mp4 2026-11-24_subs_r03_b8.mp4 2026-11-24_noseat_r02_b8.mp4
run c02_cancel 2026-11-25_cancel_c02.mp4 "I Tried to Cancel a \$21 Subscription. It Begged." 2026-11-26_buck_v01.mp4 2026-11-25_print_v04.mp4 2026-11-25_bank_c01.mp4 2026-11-24_subs_r03_b8.mp4
run r01_drawer 2026-11-25_drawer_r01.mp4 "\$27 Billion Is Sitting in Junk Drawers" 2026-11-25_cancel_c02.mp4 2026-11-26_buck_v01.mp4 2026-11-25_print_v04.mp4 2026-11-25_bank_c01.mp4
