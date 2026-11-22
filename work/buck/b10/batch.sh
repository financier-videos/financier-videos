#!/bin/bash
# draft -> cutaways -> final render -> metrics + sheet, for every Buck spec given (sequential: memory)
S=/tmp/claude-0/-home-user-financier-videos/9f67e868-b414-55ad-9f08-28f6c05f12f8/scratchpad
cd /home/user/financier-videos
for id in "$@"; do
  sp=work/buck/b10/$id.json
  python3 work/rocco/rocco2/rc_render.py $sp $S/${id}_draft.mp4 > $S/${id}_r.json 2> $S/${id}.err || { echo "$id DRAFT FAIL"; tail -3 $S/${id}.err; continue; }
  python3 work/buck/b10/add_cutaways.py $sp $S/${id}_r.json
  python3 work/rocco/rocco2/rc_render.py $sp work/buck/b10/${id}.mp4 > work/buck/b10/${id}_rendered.json 2> $S/${id}.err || { echo "$id FINAL FAIL"; tail -3 $S/${id}.err; continue; }
  n=$(ffmpeg -nostats -i work/buck/b10/${id}.mp4 -vf "scale=270:-2,select='gt(scene,0.22)',showinfo" -an -f null - 2>&1 | grep -c pts_time:)
  echo "$id cuts=$((n+1)) $(python3 .claude/skills/viral-cartoon-playbook/scripts/cartoon_metrics.py work/buck/b10/${id}.mp4 --json | cut -c1-170)"
  ffmpeg -loglevel error -y -i work/buck/b10/${id}.mp4 -vf "fps=1/1.6,scale=216:384,tile=8x3" -frames:v 1 $S/${id}_sheet.png
done
echo BATCH_DONE
