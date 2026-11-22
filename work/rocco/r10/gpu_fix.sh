#!/bin/bash
# plans for every episode -> one GPU job (<= 6 workers) -> frames in $S/animR
S=/tmp/claude-0/-home-user-financier-videos/9f67e868-b414-55ad-9f08-28f6c05f12f8/scratchpad
cd /home/user/financier-videos
B=/tmp/claude-0/-home-user-financier-videos/9f67e868-b414-55ad-9f08-28f6c05f12f8/scratchpad/bundleR2; mkdir -p $B/plans $B/models
cp work/rocco/rocco3d/perform.py .claude/skills/rocco-3d-cast/scripts/face_fix.py $B/
cp /home/user/buck-private/rocco_cast_v1/{rocco,penny,slick}_rigged.glb $B/models/
TOT=0; JOBS=""
for id in "$@"; do
  FIN_ROCCO3D=/tmp/rocco3d_lib FIN_PERF_PLAN=$B/plans/${id}_plan.json python3 work/rocco/rocco2/rc_render.py work/rocco/r10/$id.json /dev/null > /dev/null 2>$S/${id}_plan.err || { echo "$id PLAN FAIL"; tail -3 $S/${id}_plan.err; continue; }
  for c in rocco penny slick; do
    n=$(python3 -c "import json;print(len(json.load(open('$B/plans/${id}_plan.json'))['chars']['$c']))")
    [ "$n" -gt 0 ] && { JOBS="$JOBS $id:$c"; TOT=$((TOT+n)); }
  done
done
echo "jobs:$JOBS total_frames=$TOT"
cat > $B/run.sh <<R
nvidia-smi --query-gpu=name,memory.total --format=csv || true
echo "$JOBS" | tr ' ' '\n' | grep . | xargs -P 6 -I{} bash -c 'ep=\${1%%:*}; c=\${1##*:}; python3 perform.py \$c plans/\${ep}_plan.json \$OUT/\$ep --gpu --samples 32 --res 900x1200 --model models/\${c}_rigged.glb --skills . 2>&1 | grep --line-buffered -E "RENDER_DEVICE error|PERF_DONE|Error|Traceback" | sed -u "s/^/\$ep \$c: /"' _ {}
echo ALL_DONE
R
(cd $B && tar cf $S/jobR2.tar .)
python3 engine/gpu_job.py --bundle $S/jobR2.tar --out /tmp/claude-0/-home-user-financier-videos/9f67e868-b414-55ad-9f08-28f6c05f12f8/scratchpad/animR2 --expect $TOT --max-min 120
