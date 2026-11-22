#!/bin/bash
# resumable: re-run after any restart, finished frames are skipped
for c in rocco penny slick; do /tmp/bpyenv/bin/python work/rocco/rocco3d/build_lib.py $c /tmp/rocco3d_lib 2>&1 | grep -E "LIB_DONE|Error" ; done
echo ALL_DONE
