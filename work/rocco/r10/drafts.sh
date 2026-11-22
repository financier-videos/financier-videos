#!/bin/bash
# draft (library sprites) -> reaction cut-ins -> second draft -> pacing count + sheet
S=/tmp/claude-0/-home-user-financier-videos/9f67e868-b414-55ad-9f08-28f6c05f12f8/scratchpad
cd /home/user/financier-videos
for id in "$@"; do
  sp=work/rocco/r10/$id.json
  FIN_ROCCO3D=/tmp/rocco3d_lib python3 work/rocco/rocco2/rc_render.py $sp $S/${id}_lib.mp4 > $S/${id}_r.json 2> $S/${id}.err || { echo "$id DRAFT FAIL"; tail -4 $S/${id}.err; continue; }
  python3 work/rocco/rocco2/add_reactions.py $sp $S/${id}_r.json --redo --max 2.0
  FIN_ROCCO3D=/tmp/rocco3d_lib python3 work/rocco/rocco2/rc_render.py $sp $S/${id}_lib.mp4 > $S/${id}_r.json 2> $S/${id}.err || { echo "$id DRAFT2 FAIL"; tail -4 $S/${id}.err; continue; }
  n=$(ffmpeg -nostats -i $S/${id}_lib.mp4 -vf "scale=270:-2,select='gt(scene,0.22)',showinfo" -an -f null - 2>&1 | grep -c pts_time:)
  echo "$id cuts=$((n+1)) dur=$(python3 -c "import json;print(json.load(open('$S/${id}_r.json'))['seconds'])")"
  ffmpeg -loglevel error -y -i $S/${id}_lib.mp4 -vf "fps=1/1.8,scale=216:384,tile=8x3" -frames:v 1 $S/${id}_sheet.png
done
echo DRAFTS_DONE
