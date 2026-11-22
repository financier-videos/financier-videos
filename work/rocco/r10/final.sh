#!/bin/bash
# final animated render + metrics + qc_gate for each episode
S=/tmp/claude-0/-home-user-financier-videos/9f67e868-b414-55ad-9f08-28f6c05f12f8/scratchpad
cd /home/user/financier-videos; P=work/rocco/r10; R2=work/rocco/rocco2
PREV="rocco_rc12_wrong_piggy_3d.mp4 rocco_rc11_romance_coin_3d.mp4 rocco_rc10_free_tv_3d.mp4 rocco_rc09_fraud_unit_3d.mp4"
PREVS="$R2/rc12_qcspec.json $R2/rc11_qcspec.json $R2/rc10_qcspec.json $R2/rc09_qcspec.json"
for id in "$@"; do
  FIN_ROCCO3D=/tmp/rocco3d_lib FIN_ROCCO3D_ANIM=$S/${ANIMD:-animR}/$id python3 $R2/rc_render.py $P/$id.json $P/$id.mp4 > $P/${id}_rendered.json 2> $S/${id}_final.err || { echo "$id FINAL FAIL"; tail -3 $S/${id}_final.err; continue; }
  T=$(python3 -c "import json;print(json.load(open('$P/$id.json'))['title'])")
  echo "== $id $(python3 .claude/skills/viral-cartoon-playbook/scripts/cartoon_metrics.py $P/$id.mp4 --json | cut -c1-150)"
  python3 engine/qc_gate.py $P/$id.mp4 --spec $P/${id}_qcspec.json --rendered $P/${id}_rendered.json --title "$T" --out $P/${id}_qc.json --prev $PREV --prev-specs $PREVS --skills "Skillar: rocco-3d-cast, viral-cartoon-playbook, animation-direction, disney-animator-traditional, viral-video-decomposer, blender-core, blender-rendering; ishlatilmadi: analyzing-video (YouTube bloklangan)" 2>&1 | grep -E "^\[(FAIL|WARN)|VERDICT"
done
echo FINAL_DONE
