"""Face fixes for the Rocco cast v1 rigs (procedural shape keys from buck-private/rocco_cast_v1/scripts/face.py).
Call fix(mesh_obj, char) right after importing <char>_rigged.glb. Pure data API (numpy foreach_get/set), no operators.

Fixes (found in the 2026-11-22 face QA sheet):
  1. Penny jaw_open dragged the snout down -> jaw offsets are faded out above the lip line (snout stays put),
     the lower lip/chin part is boosted 1.35x so the mouth reads at phone size.
  2. All rigs: slider_max -> 2.0 so expressions can be pushed past 1.0 (the procedural keys are too subtle at 1.0).
  3. Penny blink tears the lid skin above 0.6 -> callers must cap Penny's blink (BLINK_CAP).
"""
import numpy as np

BLINK_CAP = {"rocco": 1.0, "penny": 0.55, "slick": 1.0}
MOUTH = {"rocco": dict(cx=0.0, cz=0.598, hw=0.075), "penny": dict(cx=0.012, cz=0.585, hw=0.055), "slick": dict(cx=0.0, cz=0.684, hw=0.04)}


def _ss(a, b, v):
    t = np.clip((v - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)


def fix(mesh, char):
    kb = mesh.data.shape_keys.key_blocks; n = len(mesh.data.vertices)
    base = np.empty(n * 3, np.float32); kb["Basis"].data.foreach_get("co", base); base = base.reshape(-1, 3)
    for k in kb: k.slider_max = 2.0
    report = {}
    if "jaw_open" in kb and char in MOUTH:
        M = MOUTH[char]; co = np.empty(n * 3, np.float32); kb["jaw_open"].data.foreach_get("co", co); co = co.reshape(-1, 3)
        d = co - base; x, z = base[:, 0], base[:, 2]
        if char == "penny":  # keep the snout still: fade out everything above the lip line, boost the jaw below it
            above = _ss(M["cz"] - 0.004, M["cz"] + 0.012, z) * (np.abs(x - M["cx"]) < M["hw"] * 2.2)
            d *= (1 - above)[:, None]; d *= 1.35
        report["jaw_moved_verts"] = int((np.linalg.norm(d, axis=1) > 1e-5).sum())
        kb["jaw_open"].data.foreach_set("co", (base + d).astype(np.float32).ravel())
    mesh.data.update()
    return report
