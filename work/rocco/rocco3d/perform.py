"""Animated 3D performance for one Rocco cast member (rocco/penny/slick), frame by frame from a plan made by
rc_render (FIN_PERF_PLAN). Blender Python:
  python perform.py <char> <plan.json> <outdir> [--gpu] [--samples 24] [--res 900x1200] [--frames a:b] [--every 1]
Writes <outdir>/<char>/<frame:05d>.png (transparent, same ortho camera as the sprite library -> rc_render places it
exactly like a library sprite). Resumable: existing frames are skipped (state is still simulated from the first frame).

Acting (skills animation-direction + disney-animator-traditional):
- mood shape keys ease in over ~5 frames (slow in / slow out), visemes over ~2 frames (coarticulation)
- body poses ease per bone with different lags: chest leads, upper arm 3 f, forearm 5 f, head 3 f (overlap, no twins)
- anticipation: a small dip opposite to a new pose before it starts; overshoot ~6 % then settle
- breathing on the chest, head sway, talk accents nod the head, head turns toward the scene centre
- blinks every 2.6-4.2 s (seeded per character), extra blink on a mood change; tail swish for rocco/slick
- shock onset: squash and stretch on the whole body (volume kept)
Models: private repo buck-private/rocco_cast_v1 (never copied into the public repo).
"""
import bpy, json, math, os, random, sys, time
from mathutils import Matrix, Euler

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [a for a in sys.argv[1:] if not a.endswith(".py")]
char, plan_p, out = argv[0], argv[1], argv[2]
opt = {"gpu": "--gpu" in argv, "samples": 24, "res": "900x1200", "frames": None, "every": 1,
       "model": f"/home/user/buck-private/rocco_cast_v1/{char}_rigged.glb", "skills": None}
for i, a in enumerate(argv):
    if a in ("--samples", "--res", "--frames", "--every", "--model", "--skills"): opt[a[2:]] = argv[i + 1]
os.makedirs(f"{out}/{char}", exist_ok=True)
plan = json.load(open(plan_p)); FPS = plan["fps"]; P = {int(k): v for k, v in plan["chars"][char].items()}
frames = sorted(P)
if opt["frames"]:
    a, b = (int(x) for x in opt["frames"].split(":")); frames_out = set(f for f in frames if a <= f < b)
else: frames_out = set(frames)
every = int(opt["every"])

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=opt["model"])
sc = bpy.context.scene
sc.render.engine = "CYCLES"; sc.cycles.samples = int(opt["samples"]); sc.cycles.use_denoising = True
dev = "CPU"
if opt["gpu"]:
    cp = bpy.context.preferences.addons["cycles"].preferences
    for kind in ("OPTIX", "CUDA"):
        try:
            cp.compute_device_type = kind; cp.refresh_devices()   # Blender 5.x: get_devices() alone does not list new GPUs
            gd = [d for d in cp.devices if d.type == kind]
            print("RENDER_DEVICE probe", kind, [(d.name, d.type) for d in cp.devices], flush=True)
            if gd:
                for d in cp.devices: d.use = d.type == kind
                sc.cycles.device = "GPU"; dev = kind + ":" + gd[0].name; break
        except Exception as e: print("no", kind, e)
print("RENDER_DEVICE", dev, flush=True)
if opt["gpu"] and dev == "CPU": sys.exit("RENDER_DEVICE error: --gpu asked but no GPU found (not rendering on CPU)")
rw, rh = (int(x) for x in opt["res"].split("x"))
sc.render.resolution_x, sc.render.resolution_y = rw, rh; sc.render.film_transparent = True
sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_mode = "RGBA"
cam = bpy.data.objects.new("c", bpy.data.cameras.new("c")); sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = "ORTHO"; cam.data.ortho_scale = 1.25; A = math.radians(12)   # identical to build_lib (library sprites)
cam.location = (math.sin(A) * 3, -math.cos(A) * 3, 0.52); cam.rotation_euler = (math.pi / 2, 0, A)
for loc, en in (((2, -3, 3), 3.5), ((-3, -2, 2), 1.2), ((0, 3, 2), 2.0)):   # key, fill, rim (viral benchmarks: crisp rim light)
    l = bpy.data.objects.new("l", bpy.data.lights.new("l", "SUN")); l.data.energy = en; sc.collection.objects.link(l)
    l.rotation_euler = (math.radians(50), 0, math.atan2(loc[0], -loc[1]))
w = bpy.data.worlds.new("w"); sc.world = w
bg = w.node_tree.nodes.get("Background") if w.node_tree else None
if bg: bg.inputs[0].default_value = (1, 0.97, 0.92, 1); bg.inputs[1].default_value = 0.6   # warm ambient

mesh = [o for o in sc.objects if o.type == "MESH"][0]; KB = mesh.data.shape_keys.key_blocks
sk = opt["skills"] or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".claude", "skills", "rocco-3d-cast", "scripts")
sys.path.insert(0, sk)
import face_fix; print("face_fix", face_fix.fix(mesh, char))
BLINK = face_fix.BLINK_CAP[char]
JAW = {"penny": 0.4}.get(char, 1.0); PUSH = 0.55 if char == "penny" else 1.0
BASE = {"slick": {"blink": 0.42, "brow_angry": 0.8, "brow_down": 0.4, "smile.L": 1.0, "smile.R": 0.3}}.get(char, {})
MOODS = {"neutral": {}, "happy": {"smile": 1.6 * PUSH + (0.3 if char == "penny" else 0), "brow_up": 0.5},
         "shock": {"wide": 1.2, "brow_up": 1.5}, "sad": {"brow_sad": 1.6, "frown": 1.4 * PUSH},
         "angry": {"brow_angry": 1.6, "frown": 1.0 * PUSH, "narrow": 0.5 * PUSH},
         "sly": {"blink": 0.45, "brow_down": 0.6, "smile.L": 1.2 * PUSH, "smile.R": 0.2},
         "relieved": {"smile": 0.9 * PUSH, "blink": 0.3, "brow_up": 0.5}}
VIS = {"X": {}, "A": {}, "B": {"jaw_open": 0.35 * JAW, "wideM": 0.6 * PUSH}, "C": {"jaw_open": 0.7 * JAW, "wideM": 0.5 * PUSH},
       "D": {"jaw_open": 1.2 * JAW}, "E": {"jaw_open": 0.75 * JAW, "narrow": 0.5 * PUSH}, "F": {"jaw_open": 0.35 * JAW, "narrow": 1.0 * PUSH},
       "G": {"jaw_open": 0.22 * JAW}, "H": {"jaw_open": 0.6 * JAW}}
NAMES = [kb.name for kb in KB]


def expand(d):
    o = {}
    for k, v in d.items():
        for nm in ([k + ".L", k + ".R"] if k + ".L" in KB else [k]):
            if nm in KB: o[nm] = o.get(nm, 0) + v
    return o


rig = [o for o in sc.objects if o.type == "ARMATURE"][0]; ORDER = [b.name for b in rig.data.bones]
POSES = {"idle": {}, "point": {"upper_arm.R": [0, 55, 25], "forearm.R": [0, 15, 15]},
         "arms_up": {"upper_arm.L": [0, -75, 0], "upper_arm.R": [0, 75, 0], "forearm.L": [0, -25, 0], "forearm.R": [0, 25, 0]},
         "shrug": {"upper_arm.L": [0, -20, -25], "upper_arm.R": [0, 20, 25], "forearm.L": [0, -45, -30], "forearm.R": [0, 45, 30], "head": [0, 10, 0]}}
LAG = {"chest": 0.34, "head": 0.24, "upper_arm.L": 0.2, "upper_arm.R": 0.2, "forearm.L": 0.14, "forearm.R": 0.14, "hand.L": 0.12, "hand.R": 0.12}


def apply_pose(D):
    for pb in rig.pose.bones: pb.matrix_basis = Matrix.Identity(4)
    for b in ORDER:
        if b in D and any(abs(x) > 1e-4 for x in D[b]):
            pb = rig.pose.bones[b]; bpy.context.view_layer.update(); M = pb.matrix.copy(); h = M.to_translation()
            Rw = Euler([math.radians(x) for x in D[b]], "XYZ").to_matrix().to_4x4(); pb.matrix = Matrix.Translation(h) @ Rw @ Matrix.Translation(-h) @ M


rng = random.Random({"rocco": 1, "penny": 2, "slick": 3}[char])
keys = {}; bones = {}; vel = {}; prev_f = None; prev_mood = None; prev_pose = None; next_blink = rng.uniform(0.5, 2.0); blink_t0 = -9
pose_t0 = -9; shock_t0 = -9; n = 0; t_start = time.time()
base_scale = rig.scale.copy()
for f in frames:
    st = P[f]; t = f / FPS
    if prev_f is None or f - prev_f > 2:   # new appearance: snap to the target (a cut), no easing from an old state
        keys = {}; bones = {}; vel = {}; prev_mood = None; prev_pose = None
    snap = not keys
    # ---- face ----
    tgt = {nm: 0.0 for nm in NAMES}
    for k, v in expand(BASE if not (char == "slick" and st["mood"] == "sly") else {}).items(): tgt[k] += v
    for k, v in expand(MOODS.get(st["mood"], {})).items(): tgt[k] += v
    if st["mood"] != prev_mood:
        if prev_mood is not None: blink_t0 = t   # blink on an emotion change
        if st["mood"] == "shock" and prev_mood is not None: shock_t0 = t
        prev_mood = st["mood"]
    amt = min(1.0, 0.35 + 1.3 * st["talk"])
    vis = {k: v * amt for k, v in expand(VIS.get(st["vis"], {})).items()}
    mouth_keys = set(expand({"jaw_open": 1, "wideM": 1, "narrow": 1}))
    if t >= next_blink: blink_t0 = t; next_blink = t + rng.uniform(2.6, 4.2)
    bt = (t - blink_t0) * FPS; bl = {0: 0.6, 1: 1.0, 2: 0.6, 3: 0.2}.get(int(bt), 0.0) if 0 <= bt < 4 else 0.0
    for nm in NAMES:
        target = tgt[nm] + vis.get(nm, 0.0)
        rate = 0.55 if nm in mouth_keys else 0.3   # visemes ~2 f, moods ~5 f
        cur = target if snap else keys.get(nm, 0.0)
        cur += (target - cur) * rate
        keys[nm] = cur
        val = cur
        if nm.startswith("blink"): val = max(val, bl * BLINK)
        KB[nm].value = max(0.0, min(2.0, val))
    # ---- body ----
    if st["pose"] != prev_pose:
        if prev_pose is not None: pose_t0 = t
        prev_pose = st["pose"]
    tp = POSES.get(st["pose"], {})
    D = {}
    for b in set(list(tp) + list(bones) + ["chest", "head", "hips", "tail", "ear.L", "ear.R"]):
        if b not in rig.pose.bones: continue
        target = tp.get(b, [0, 0, 0]); cur = list(target) if snap else bones.get(b, [0, 0, 0]); v0 = vel.get(b, [0, 0, 0])
        k = LAG.get(b, 0.25)
        nv = [v0[i] * 0.55 + (target[i] - cur[i]) * k for i in range(3)]   # damped spring: ease out + ~6 % overshoot, then settle
        cur = [cur[i] + nv[i] for i in range(3)]; bones[b] = cur; vel[b] = nv; D[b] = list(cur)
    ta = t - pose_t0
    if 0 <= ta < 0.2 and "chest" in D: D["chest"][0] += -3.0 * math.sin(math.pi * ta / 0.2)   # anticipation dip
    breath = math.sin(2 * math.pi * t / 3.4 + rng.random() * 0)
    look = st.get("look", 1)
    if "chest" in D: D["chest"][0] += 1.4 * breath; D["chest"][2] += 1.5 * math.sin(t / 1.7)
    if "head" in D:
        nod = 5.0 * min(1.0, st["talk"]) * (0.5 + 0.5 * math.sin(t * 9.0))   # accents while talking
        D["head"][0] += -nod + 0.8 * breath; D["head"][2] += 9.0 * look + 2.5 * math.sin(t / 2.3); D["head"][1] += 2.0 * math.sin(t / 3.1)
    if "hips" in D: D["hips"][1] += 1.0 * math.sin(t / 1.9)
    if "tail" in D and char in ("rocco", "slick"): D["tail"][2] += 12.0 * math.sin(t * 2.4)
    for e, ph in (("ear.L", 0.0), ("ear.R", 1.3)):
        if e in D: D[e][1] += 4.0 * max(0.0, math.sin(t * 0.9 + ph)) ** 8
    apply_pose(D)
    ts = t - shock_t0   # squash then stretch, volume kept
    s = 1.0 + (0.07 * math.sin(math.pi * ts / 0.25) * math.exp(-ts * 4) if 0 <= ts < 0.6 else 0.0)
    rig.scale = (base_scale[0] / math.sqrt(s), base_scale[1] / math.sqrt(s), base_scale[2] * s)
    prev_f = f
    if f in frames_out and (f % every == 0):
        fp = f"{out}/{char}/{f:05d}.png"
        if not os.path.exists(fp):
            sc.render.filepath = fp; bpy.ops.render.render(write_still=True); n += 1
            if n % 20 == 0: print(f"{char} frame {f} rendered {n} {round(time.time() - t_start)}s", flush=True)
print("PERF_DONE", char, n, round(time.time() - t_start), "s", flush=True)
