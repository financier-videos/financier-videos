#!/bin/bash
S=/tmp/claude-0/-home-user-financier-videos/9f67e868-b414-55ad-9f08-28f6c05f12f8/scratchpad
cd /home/user/financier-videos; P=work/buck/b10
ALL=(bk01 bk02 bk03 bk04 bk05 bk06 bk07 bk08 bk09 bk10)
for id in "$@"; do
  T=$(python3 -c "import json;print(json.load(open('$P/$id.json'))['title'])")
  prev=(); prevs=(); for o in "${ALL[@]}"; do [ "$o" != "$id" ] && [ ${#prev[@]} -lt 4 ] && { prev+=($P/$o.mp4); prevs+=($P/${o}_qcspec.json); }; done
  echo "== $id"
  python3 engine/qc_gate.py $P/$id.mp4 --spec $P/${id}_qcspec.json --rendered $P/${id}_rendered.json --title "$T" --out $P/${id}_qc.json --prev ${prev[@]} --prev-specs ${prevs[@]} --skills "Skillar: viral-cartoon-playbook, viral-video-decomposer, dataviz, color-expert, animation-direction; ishlatilmadi: blender-* (Buck 3D kutubxonasi tayyor)" 2>&1 | grep -E "^\[(FAIL|WARN)|VERDICT"
done
echo QC_DONE
