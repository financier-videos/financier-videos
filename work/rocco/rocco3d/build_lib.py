"""Rocco 3D sprite library (BUYURTMA 9). Run with Blender's Python:
  /tmp/bpyenv/bin/python work/rocco/rocco3d/build_lib.py <char> [outdir]
Renders <outdir>/<char>/<mood>_<mouth>_<eyes>.png (transparent, 600x800, Cycles CPU, studio light).
Resumable: frames that exist are skipped. Models: private repo buck-private/rocco_cast_v1 (never copied here)."""
import bpy, math, os, sys, time
char = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].endswith(".py") else sys.argv[-2]
args = [a for a in sys.argv if not a.endswith(".py")]
char = args[1] if len(args) > 1 else "rocco"
out = args[2] if len(args) > 2 else "/tmp/rocco3d_lib"
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
BLINK = 0.6 if char == "penny" else 1.0
BASE = {"slick": {"blink": 0.42, "brow_angry": 0.8, "brow_down": 0.4, "smile.L": 1.0, "smile.R": 0.3}}.get(char, {})
MOODS = {
    "neutral": {},
    "happy": {"smile": 0.9, "brow_up": 0.3},
    "shock": {"wide": 1.0, "brow_up": 1.0},
    "sad": {"brow_sad": 1.0, "frown": 0.8},
    "angry": {"brow_angry": 1.0, "frown": 0.5, "narrow": 0.4},
    "sly": {"blink": 0.45, "brow_down": 0.5, "smile.L": 0.7, "smile.R": 0.2},
    "relieved": {"smile": 0.6, "blink": 0.3, "brow_up": 0.4},
}
MOUTHS = {"closed": {}, "half": {"jaw_open": 0.35}, "open": {"jaw_open": 0.75}, "o": {"jaw_open": 0.5, "narrow": 0.6}, "e": {"jaw_open": 0.3, "wideM": 0.8}}


def setk(d):
    for k, v in d.items():
        for nm in ([k + ".L", k + ".R"] if k + ".L" in KB else [k]):
            if nm in KB: KB[nm].value = v


n = 0; t0 = time.time()
for mood, mk in MOODS.items():
    for mouth, mm in MOUTHS.items():
        for eyes in ("open", "closed"):
            f = f"{out}/{char}/{mood}_{mouth}_{eyes}.png"
            if os.path.exists(f): continue
            for kb in KB: kb.value = 0
            setk(BASE if mood != "sly" or char != "slick" else {}); setk(mk); setk(mm)
            if eyes == "closed": setk({"blink": BLINK})
            sc.render.filepath = f; bpy.ops.render.render(write_still=True); n += 1
            print(f"{char} {mood}_{mouth}_{eyes} {n} {round(time.time() - t0)}s", flush=True)
print("LIB_DONE", char, n)
