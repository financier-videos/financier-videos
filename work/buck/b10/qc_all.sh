#!/bin/bash
# QC in real posting order: each video is compared with the 4 videos published right before it
S=/tmp/claude-0/-home-user-financier-videos/9f67e868-b414-55ad-9f08-28f6c05f12f8/scratchpad
cd /home/user/financier-videos; P=work/buck/b10
ORDER=(bk02 bk01 bk07 bk05 bk04 bk10 bk08 bk03 bk06 bk09)
HIST=(2026-11-22_gta_per_second.mp4 2026-11-22_gta_timeline_b8.mp4 2026-11-22_airport_r04_b8.mp4)
for id in "$@"; do
  T=$(python3 -c "import json;print(json.load(open('$P/$id.json'))['title'])")
  prev=("${HIST[@]}"); prevs=()
  for o in "${ORDER[@]}"; do [ "$o" == "$id" ] && break; prev+=($P/$o.mp4); prevs+=($P/${o}_qcspec.json); done
  prev=("${prev[@]: -4}"); prevs=("${prevs[@]: -4}"); [ ${#prevs[@]} -eq 0 ] && prevs=(work/2026-11-22r/r04_airport_b8.json)
  echo "== $id (prev: ${prev[*]##*/})"
  python3 engine/qc_gate.py $P/$id.mp4 --spec $P/${id}_qcspec.json --rendered $P/${id}_rendered.json --title "$T" --out $P/${id}_qc.json --prev ${prev[@]} --prev-specs ${prevs[@]} --skills "Skillar: viral-cartoon-playbook, viral-video-decomposer, dataviz, color-expert, animation-direction; ishlatilmadi: blender-* (Buck 3D kutubxonasi tayyor)" 2>&1 | grep -E "^\[(FAIL|WARN)|VERDICT"
done
echo QC_DONE
