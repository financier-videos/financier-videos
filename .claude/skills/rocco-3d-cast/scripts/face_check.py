"""Face QA sheet: close-up renders of key expressions for one character (Cycles CPU, headless bpy).
  /tmp/bpyenv/bin/python .claude/skills/rocco-3d-cast/scripts/face_check.py <char> <out.png> [--fixed]"""
import bpy, math, sys, os
args = [a for a in sys.argv[1:] if not a.endswith(".py")]; char, out = args[0], args[1]; fixed = "--fixed" in args
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import face_fix
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=f"/home/user/buck-private/rocco_cast_v1/{char}_rigged.glb")
sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 12; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 360, 360; sc.render.film_transparent = True
cam = bpy.data.objects.new("c", bpy.data.cameras.new("c")); sc.collection.objects.link(cam); sc.camera = cam
cz = {"rocco": 0.66, "penny": 0.66, "slick": 0.74}[char]
cam.data.type = "ORTHO"; cam.data.ortho_scale = 0.42; a = math.radians(12); cam.location = (math.sin(a) * 3, -math.cos(a) * 3, cz); cam.rotation_euler = (math.pi / 2, 0, a)
l = bpy.data.objects.new("l", bpy.data.lights.new("l", "SUN")); l.data.energy = 4; sc.collection.objects.link(l); l.rotation_euler = (math.radians(50), 0, 0.5)
mesh = [o for o in sc.objects if o.type == "MESH"][0]; KB = mesh.data.shape_keys.key_blocks
if fixed: print("fix", face_fix.fix(mesh, char))
cap = face_fix.BLINK_CAP[char]
T = {"rest": {}, "talk_half": {"jaw_open": 0.6}, "talk_open": {"jaw_open": 1.2}, "happy": {"smile": 1.6, "brow_up": 0.5},
     "angry": {"brow_angry": 1.6, "frown": 1.0, "narrow": 0.5}, "sad": {"brow_sad": 1.6, "frown": 1.4}, "shock": {"wide": 1.2, "brow_up": 1.5, "jaw_open": 0.9},
     "blink": {"blink": cap}}
from PIL import Image, ImageDraw
sheet = Image.new("RGB", (360 * len(T), 360), (118, 118, 122))
for i, (nm, d) in enumerate(T.items()):
    for kb in KB: kb.value = 0
    for k, v in d.items():
        for s in ([k + ".L", k + ".R"] if k + ".L" in KB else [k]):
            if s in KB: KB[s].value = v
    f = f"/tmp/_fc_{char}_{i}.png"; sc.render.filepath = f; bpy.ops.render.render(write_still=True)
    im = Image.open(f).convert("RGBA"); sheet.paste(im, (i * 360, 0), im); ImageDraw.Draw(sheet).text((i * 360 + 6, 6), nm, fill=(255, 255, 0))
sheet.save(out); print("SHEET", out)
