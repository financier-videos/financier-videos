"""Rocco 3D sprite library (BUYURTMA 9). Run with Blender's Python:
  /tmp/bpyenv/bin/python work/rocco/rocco3d/build_lib.py <char> [outdir]
Renders <outdir>/<char>/<mood>_<mouth>_<eyes>.png (transparent, 600x800, Cycles CPU, studio light).
Resumable: frames that exist are skipped. Models: private repo buck-private/rocco_cast_v1 (never copied here)."""
import bpy, math, os, sys, time
from mathutils import Matrix, Euler
args = [a for a in sys.argv[1:] if not a.endswith(".py")]
char = args[0] if args else "rocco"
out = args[1] if len(args) > 1 else "/tmp/rocco3d_lib"
os.makedirs(f"{out}/{char}", exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=f"/home/user/buck-private/rocco_cast_v1/{char}_rigged.glb")
sc = bpy.context.scene
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 24; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 600, 800; sc.render.film_transparent = True
cam = bpy.data.objects.new("c", bpy.data.cameras.new("c")); sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = "ORTHO"; cam.data.ortho_scale = 1.25; a = math.radians(12)
cam.location = (math.sin(a) * 3, -math.cos(a) * 3, 0.52); cam.rotation_euler = (math.pi / 2, 0, a)
for loc, en in (((2, -3, 3), 3.5), ((-3, -2, 2), 1.2)):
    l = bpy.data.objects.new("l", bpy.data.lights.new("l", "SUN")); l.data.energy = en; sc.collection.objects.link(l)
    l.rotation_euler = (math.radians(50), 0, math.atan2(loc[0], -loc[1]))
w = bpy.data.worlds.new("w"); sc.world = w
bg = w.node_tree.nodes.get("Background") if w.node_tree else None
if bg: bg.inputs[0].default_value = (1, 1, 1, 1); bg.inputs[1].default_value = 0.6
mesh = [o for o in sc.objects if o.type == "MESH"][0]; KB = mesh.data.shape_keys.key_blocks
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".claude", "skills", "rocco-3d-cast", "scripts"))
import face_fix; print("face_fix", face_fix.fix(mesh, char))  # skill rocco-3d-cast: Penny snout-safe jaw, slider_max 2.0
BLINK = face_fix.BLINK_CAP[char]
JAW = {"penny": 0.4}.get(char, 1.0)   # Penny's mouth sits under the snout: open it less (QA sheet 2026-11-22)
BASE = {"slick": {"blink": 0.42, "brow_angry": 0.8, "brow_down": 0.4, "smile.L": 1.0, "smile.R": 0.3}}.get(char, {})
PUSH = 0.55 if char == "penny" else 1.0   # procedural keys are subtle: push Rocco/Slick past 1.0, keep Penny's mouth keys soft
MOODS = {
    "neutral": {},
    "happy": {"smile": 1.6 * PUSH + (0.3 if char == "penny" else 0), "brow_up": 0.5},
    "shock": {"wide": 1.2, "brow_up": 1.5},
    "sad": {"brow_sad": 1.6, "frown": 1.4 * PUSH},
    "angry": {"brow_angry": 1.6, "frown": 1.0 * PUSH, "narrow": 0.5 * PUSH},
    "sly": {"blink": 0.45, "brow_down": 0.6, "smile.L": 1.2 * PUSH, "smile.R": 0.2},
    "relieved": {"smile": 0.9 * PUSH, "blink": 0.3, "brow_up": 0.5},
}
MOUTHS = {"closed": {}, "half": {"jaw_open": 0.6 * JAW}, "open": {"jaw_open": 1.2 * JAW}, "o": {"jaw_open": 0.8 * JAW, "narrow": 0.8 * PUSH},
          "e": {"jaw_open": 0.45 * JAW, "wideM": 1.0 * PUSH}}


def setk(d):
    for k, v in d.items():
        for nm in ([k + ".L", k + ".R"] if k + ".L" in KB else [k]):
            if nm in KB: KB[nm].value = v


rig = [o for o in sc.objects if o.type == "ARMATURE"][0]; ORDER = [b.name for b in rig.data.bones]
POSES = {"idle": {},  # character's R arm = screen left
         "point": {"upper_arm.R": [0, 55, 25], "forearm.R": [0, 15, 15]},
         "arms_up": {"upper_arm.L": [0, -75, 0], "upper_arm.R": [0, 75, 0], "forearm.L": [0, -25, 0], "forearm.R": [0, 25, 0]},
         "shrug": {"upper_arm.L": [0, -20, -25], "upper_arm.R": [0, 20, 25], "forearm.L": [0, -45, -30], "forearm.R": [0, 45, 30], "head": [0, 10, 0]}}
POSE_MOODS = {"idle": list(MOODS), "point": ["happy", "sly", "angry", "shock", "sad"], "arms_up": ["happy", "shock", "angry", "sad", "sly"],
              "shrug": ["happy", "sly", "sad", "shock", "neutral"]}


def pose(P):  # world-space rotation about each bone head (same convention as buck-private/rocco_cast_v1/scripts/demo.py)
    for pb in rig.pose.bones: pb.matrix_basis = Matrix.Identity(4)
    for b in ORDER:
        if b in P:
            pb = rig.pose.bones[b]; bpy.context.view_layer.update(); M = pb.matrix.copy(); h = M.to_translation()
            Rw = Euler([math.radians(x) for x in P[b]], "XYZ").to_matrix().to_4x4(); pb.matrix = Matrix.Translation(h) @ Rw @ Matrix.Translation(-h) @ M


n = 0; t0 = time.time()
for pz, P in POSES.items():
    pose(P)
    for mood in POSE_MOODS[pz]:
        mk = MOODS[mood]
        for mouth, mm in MOUTHS.items():
            for eyes in (("open", "closed") if pz == "idle" else ("open",)):
                f = f"{out}/{char}/{mood}_{mouth}_{eyes}.png" if pz == "idle" else f"{out}/{char}/{pz}_{mood}_{mouth}_{eyes}.png"
                if os.path.exists(f): continue
                for kb in KB: kb.value = 0
                setk(BASE if mood != "sly" or char != "slick" else {}); setk(mk); setk(mm)
                if eyes == "closed": setk({"blink": BLINK})
                sc.render.filepath = f; bpy.ops.render.render(write_still=True); n += 1
                print(f"{char} {pz} {mood}_{mouth}_{eyes} {n} {round(time.time() - t0)}s", flush=True)
print("LIB_DONE", char, n)
