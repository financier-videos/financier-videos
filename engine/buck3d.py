#!/usr/bin/env python3
"""BUCK 3D — the channel's own coin character, built from primitives and rendered with Blender Cycles (bpy).
Original design (no outside models/textures). Renders a sprite library (RGBA PNG, transparent background with a
soft contact shadow) that make_video.py composites into videos.

  python3 buck3d.py --out buck3d --res 720 --samples 32            # whole library (all moods + acts)
  python3 buck3d.py --out test --only proud --frames 1             # quick test
  python3 buck3d.py --cinema --out buck3d_v2                        # v2 CINEMA QUALITY: 1080 px, 64 samples, PBR gold
                                                                   # (micro-scratches, lathe rings, roughness map, clear coat),
                                                                   # iris + cornea eyes, fabric shaders, 3-point + double rim
                                                                   # light, reflection cards, soft deep contact shadows

Library layout: <out>/<clip>_<NN>.png, 15 fps. Clips: one 1-second idle loop per mood (15 frames) and the acts
flip (11), bonk (23), dodge (12). Framing matches the 2D patch: square, width = 4.6 body radii,
body centre at 46% from the top.
"""
import argparse, math, os, sys
import bpy, bmesh
from mathutils import Vector, Euler

FPS = 15
MOODS = ["happy", "shocked", "laugh", "smug", "confused", "sideeye", "sad", "angry", "point", "dizzy", "thumbsup", "proud"]
ACTS = {"flip": 11, "bonk": 23, "dodge": 12}
ANTON = "/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf"

# ---------------------------------------------------------------- materials
def mat(name, color, metallic=0.0, rough=0.5, coat=0.0, sheen=0.0, alpha=1.0, bump=0.0, sss=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Metallic"].default_value = metallic
    b.inputs["Roughness"].default_value = rough
    for key, val in (("Coat Weight", coat), ("Sheen Weight", sheen), ("Subsurface Weight", sss)):
        if key in b.inputs and val: b.inputs[key].default_value = val
    if alpha < 1.0:
        b.inputs["Alpha"].default_value = alpha
    if bump:
        tc = nt.nodes.new("ShaderNodeTexCoord"); nz = nt.nodes.new("ShaderNodeTexNoise"); bp = nt.nodes.new("ShaderNodeBump")
        nz.inputs["Scale"].default_value = 90; nz.inputs["Detail"].default_value = 6
        bp.inputs["Strength"].default_value = bump; bp.inputs["Distance"].default_value = 0.02
        nt.links.new(tc.outputs["Object"], nz.inputs["Vector"]); nt.links.new(nz.outputs["Fac"], bp.inputs["Height"])
        nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m


def smooth(obj, angle=0.7):
    me = obj.data
    for p in me.polygons: p.use_smooth = True
    try: me.set_sharp_from_angle(angle=angle)
    except Exception: pass


def link(obj, parent=None, mat_=None):
    bpy.context.scene.collection.objects.link(obj)
    if parent: obj.parent = parent
    if mat_ is not None:
        if obj.data.materials: obj.data.materials[0] = mat_
        else: obj.data.materials.append(mat_)
    return obj


def sphere(name, r, loc, scale=(1, 1, 1), mat_=None, parent=None, seg=48, half=None):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=seg // 2, radius=r)
    if half:  # "upper" / "lower" hemisphere (closed)
        geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
        res = bmesh.ops.bisect_plane(bm, geom=geom, plane_co=(0, 0, 0), plane_no=(0, 0, 1),
                                     clear_inner=(half == "upper"), clear_outer=(half == "lower"))
        edges = [e for e in res["geom_cut"] if isinstance(e, bmesh.types.BMEdge)]
        bmesh.ops.edgeloop_fill(bm, edges=edges)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); o.location = loc; o.scale = scale
    smooth(o, 1.2); return link(o, parent, mat_)


def curve(name, pts, depth, mat_=None, parent=None):
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"
    cu.bevel_depth = depth; cu.bevel_resolution = 6; cu.use_fill_caps = True
    sp = cu.splines.new("BEZIER"); sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p; bp.handle_left_type = bp.handle_right_type = "AUTO"
    o = bpy.data.objects.new(name, cu); return link(o, parent, mat_)


def set_curve(o, pts):
    for bp, p in zip(o.data.splines[0].bezier_points, pts):
        bp.co = p; bp.handle_left_type = bp.handle_right_type = "AUTO"


def text(name, body, size, loc, rot, mat_, parent, extrude=0.04):
    cu = bpy.data.curves.new(name, "FONT"); cu.body = body; cu.size = size
    cu.extrude = extrude; cu.bevel_depth = 0.008; cu.align_x = "CENTER"; cu.align_y = "CENTER"
    try: cu.font = bpy.data.fonts.load(ANTON, check_existing=True)
    except Exception: pass
    o = bpy.data.objects.new(name, cu); o.location = loc; o.rotation_euler = rot
    return link(o, parent, mat_)


# ---------------------------------------------------------------- scene
def build(res, samples):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    try: sc.cycles.denoiser = "OPENIMAGEDENOISE"
    except Exception: pass
    sc.cycles.max_bounces = 4; sc.cycles.glossy_bounces = 3; sc.cycles.diffuse_bounces = 2; sc.cycles.transmission_bounces = 2; sc.cycles.transparent_max_bounces = 6
    sc.render.film_transparent = True
    sc.render.resolution_x = sc.render.resolution_y = res; sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_mode = "RGBA"
    try:
        sc.view_settings.view_transform = "Standard"; sc.view_settings.exposure = 0.0
    except Exception: pass
    sc.render.use_persistent_data = True  # keep BVH/shaders between frames (much faster sequences)
    sc.cycles.use_adaptive_sampling = True
    # world: soft studio gradient (only seen in reflections; film is transparent)
    w = bpy.data.worlds.new("studio"); sc.world = w; w.use_nodes = True; nt = w.node_tree
    bg = nt.nodes["Background"]; tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    mr = nt.nodes.new("ShaderNodeMapRange"); ramp = nt.nodes.new("ShaderNodeValToRGB")
    mr.inputs["From Min"].default_value = -1; mr.inputs["From Max"].default_value = 1
    ramp.color_ramp.elements[0].color = (0.02, 0.03, 0.06, 1); ramp.color_ramp.elements[1].color = (0.9, 0.92, 1.0, 1)
    nt.links.new(tc.outputs["Generated"], sep.inputs[0]); nt.links.new(sep.outputs["Z"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = 0.35

    def area(name, loc, size, energy, color):
        L = bpy.data.lights.new(name, "AREA"); L.size = size; L.energy = energy; L.color = color
        o = bpy.data.objects.new(name, L); o.location = loc
        o.rotation_euler = (Vector((0, 0, -0.2)) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
        sc.collection.objects.link(o); return o
    area("key", (-4.0, -6.5, 5.0), 5.0, 800, (1.0, 0.93, 0.84))
    area("fill", (5.0, -6.0, 0.8), 6.0, 260, (0.82, 0.88, 1.0))
    area("rim", (2.5, 5.0, 3.5), 3.0, 1400, (1.0, 1.0, 1.0))
    area("rim2", (-3.0, 4.0, -0.5), 3.0, 600, (0.75, 0.85, 1.0))
    area("softbox", (0.6, -13.0, 2.6), 9.0, 430, (1.0, 0.97, 0.9))  # big frontal softbox: the gold face reflects it
    # camera: framing = 4.6 radii wide, body centre 46% from the top
    cam = bpy.data.cameras.new("cam"); cam.lens = 85; cam.sensor_width = 36; cam.sensor_fit = "HORIZONTAL"
    co = bpy.data.objects.new("cam", cam); sc.collection.objects.link(co); sc.camera = co
    d = 4.6 / (2 * math.tan(math.atan(18 / 85)))
    zc = (2.12 - 2.48) / 2
    co.location = (0, -d, zc); co.rotation_euler = (math.radians(90), 0, 0)
    # shadow catcher under the feet
    me = bpy.data.meshes.new("floor"); bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=6); bm.to_mesh(me); bm.free()
    fl = bpy.data.objects.new("floor", me); fl.location = (0, 0.6, -1.54); sc.collection.objects.link(fl)
    fl.is_shadow_catcher = True

    M = {
        "gold": mat("gold", (1.0, 0.70, 0.22), metallic=1.0, rough=0.24, bump=0.04),
        "gold_rim": mat("gold_rim", (0.95, 0.62, 0.16), metallic=1.0, rough=0.18),
        "eye": mat("eye", (0.95, 0.95, 0.95), rough=0.08, coat=1.0, sss=0.1),
        "pupil": mat("pupil", (0.01, 0.01, 0.012), rough=0.05, coat=1.0),
        "ink": mat("ink", (0.035, 0.028, 0.03), rough=0.45),
        "mouth": mat("mouth", (0.22, 0.02, 0.035), rough=0.35, coat=0.6),
        "tongue": mat("tongue", (0.95, 0.35, 0.40), rough=0.35, sss=0.3),
        "teeth": mat("teeth", (0.97, 0.96, 0.92), rough=0.2, coat=0.6),
        "cheek": mat("cheek", (1.0, 0.36, 0.36), rough=0.6, alpha=0.32),
        "glove": mat("glove", (0.93, 0.93, 0.95), rough=0.5, sheen=0.4, sss=0.15),
        "tie": mat("tie", (0.03, 0.62, 0.26), rough=0.32, sheen=0.6, coat=0.3),
        "tie_d": mat("tie_d", (0.02, 0.38, 0.16), rough=0.3, sheen=0.5),
        "shoe": mat("shoe", (0.04, 0.58, 0.28), rough=0.4, coat=0.4),
        "sole": mat("sole", (0.96, 0.96, 0.96), rough=0.55),
        "white": mat("white", (0.97, 0.97, 0.98), rough=0.3),
        "red": mat("red", (0.95, 0.12, 0.12), rough=0.3, coat=0.5),
        "water": mat("water", (0.45, 0.78, 1.0), rough=0.05, coat=1.0),
        "star": mat("star", (1.0, 0.82, 0.18), metallic=0.6, rough=0.25),
        "paper": mat("paper", (0.98, 0.95, 0.86), rough=0.75),
    }
    root = bpy.data.objects.new("BUCK", None); sc.collection.objects.link(root)
    body = bpy.data.objects.new("body_pivot", None); sc.collection.objects.link(body); body.parent = root
    P = {"root": root, "body": body, "M": M}
    # coin body (axis toward camera)
    bpy.ops.mesh.primitive_cylinder_add(vertices=128, radius=1.0, depth=0.3, location=(0, 0, 0), rotation=(math.radians(90), 0, 0))
    coin = bpy.context.active_object; coin.name = "coin"; coin.parent = body
    bev = coin.modifiers.new("bev", "BEVEL"); bev.width = 0.07; bev.segments = 5; bev.limit_method = "ANGLE"
    smooth(coin, 0.6); coin.data.materials.append(M["gold"]); P["coin"] = coin
    # reeded edge: thin ridges around the rim
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.012, depth=0.2, location=(0, 0, 0), rotation=(math.radians(90), 0, 0))
    ridge = bpy.context.active_object; ridge.name = "ridge"
    ridge.location = (1.0, 0, 0); ridge.parent = body; ridge.data.materials.append(M["gold_rim"])
    # (ridges via an array around an empty)
    emp = bpy.data.objects.new("ridge_rot", None); sc.collection.objects.link(emp); emp.parent = body
    emp.rotation_euler = (0, math.radians(360 / 110), 0)
    arr = ridge.modifiers.new("arr", "ARRAY"); arr.count = 110; arr.use_relative_offset = False; arr.use_object_offset = True; arr.offset_object = emp
    ridge.location = (0, 0, 0); ridge.data.transform(__import__("mathutils").Matrix.Translation((0.995, 0, 0)))
    # raised rim ring on the face + inner ring
    for nm, rr, y in (("ring_f", 0.86, -0.155), ("ring_b", 0.86, 0.155)):
        bpy.ops.mesh.primitive_torus_add(major_radius=rr, minor_radius=0.03, major_segments=128, minor_segments=16,
                                         location=(0, y, 0), rotation=(math.radians(90), 0, 0))
        t = bpy.context.active_object; t.name = nm; t.parent = body; smooth(t, 1.2); t.data.materials.append(M["gold_rim"])
    # embossed "$" on the back (seen during a flip)
    text("back_dollar", "$", 1.1, (0, 0.16, 0.02), (math.radians(90), 0, math.radians(180)), M["gold_rim"], body, extrude=0.03)
    # face
    for s in (-1, 1):
        e = sphere(f"eye{s}", 0.2, (0.3 * s, -0.16, 0.17), (1, 0.45, 1.25), M["eye"], body)
        p = sphere(f"pupil{s}", 0.085, (0.3 * s, -0.235, 0.15), (1, 0.4, 1), M["pupil"], body)
        lid = sphere(f"lid{s}", 0.212, (0.3 * s, -0.16, 0.17), (1, 0.5, 1.27), M["gold"], body, half="upper")
        P[f"eyeline{s}"] = curve(f"eyeline{s}", [(0.3 * s - 0.17, -0.2, 0.15), (0.3 * s, -0.2, 0.22), (0.3 * s + 0.17, -0.2, 0.15)], 0.032, M["ink"], body)
        brow = curve(f"brow{s}", [(0.12 * s, -0.19, 0.48), (0.29 * s, -0.19, 0.51), (0.46 * s, -0.19, 0.48)], 0.034, M["ink"], body)
        ck = sphere(f"cheek{s}", 0.12, (0.56 * s, -0.152, -0.14), (1, 0.12, 0.6), M["cheek"], body)
        P[f"eye{s}"], P[f"pupil{s}"], P[f"lid{s}"], P[f"brow{s}"], P[f"cheek{s}"] = e, p, lid, brow, ck
    P["mouth_line"] = curve("mouth_line", [(-0.2, -0.17, -0.24), (-0.1, -0.17, -0.31), (0, -0.17, -0.33), (0.1, -0.17, -0.31), (0.2, -0.17, -0.24)], 0.03, M["ink"], body)
    P["mouth_open"] = sphere("mouth_open", 1.0, (0, -0.15, -0.22), (0.26, 0.07, 0.18), M["mouth"], body, half="lower")
    P["tongue"] = sphere("tongue", 1.0, (0, -0.19, -0.33), (0.12, 0.05, 0.06), M["tongue"], body)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.2, -0.235))
    teeth = bpy.context.active_object; teeth.name = "teeth"; teeth.parent = body; teeth.scale = (0.4, 0.03, 0.05)
    tb = teeth.modifiers.new("bev", "BEVEL"); tb.width = 0.15; tb.segments = 3; teeth.data.materials.append(M["teeth"]); P["teeth"] = teeth
    P["mouth_o"] = sphere("mouth_o", 1.0, (0, -0.15, -0.32), (0.13, 0.07, 0.17), M["mouth"], body)
    # bow tie
    for s in (-1, 1):
        bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=0.16, radius2=0.035, depth=0.3,
                                        location=(0.15 * s, -0.2, -0.80), rotation=(0, math.radians(-90 * s), 0))
        w_ = bpy.context.active_object; w_.name = f"tie{s}"; w_.parent = body; w_.scale = (1.0, 0.55, 1.0)
        bm_ = w_.modifiers.new("bev", "BEVEL"); bm_.width = 0.02; bm_.segments = 3; smooth(w_, 0.9); w_.data.materials.append(M["tie"]); P[f"tie{s}"] = w_
    P["knot"] = sphere("knot", 0.075, (0, -0.24, -0.8), (1, 0.7, 0.9), M["tie_d"], body)
    # arms (curves + gloves), legs + sneakers
    for s in (-1, 1):
        P[f"arm{s}"] = curve(f"arm{s}", [(0.96 * s, 0.0, -0.12), (1.3 * s, -0.1, -0.3), (1.4 * s, -0.2, -0.4)], 0.045, M["ink"], root)
        P[f"hand{s}"] = sphere(f"hand{s}", 0.15, (1.4 * s, -0.2, -0.4), (1, 0.85, 1), M["glove"], root)
        P[f"thumb{s}"] = sphere(f"thumb{s}", 0.065, (1.4 * s, -0.25, -0.25), (0.8, 0.8, 1.5), M["glove"], root)
        P[f"leg{s}"] = curve(f"leg{s}", [(0.3 * s, 0.0, -0.9), (0.33 * s, -0.04, -1.15), (0.37 * s, -0.08, -1.38)], 0.045, M["ink"], root)
        sh = sphere(f"shoe{s}", 1.0, (0.42 * s, -0.2, -1.43), (0.2, 0.32, 0.12), M["shoe"], root)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0.42 * s, -0.2, -1.5))
        so = bpy.context.active_object; so.name = f"sole{s}"; so.parent = root; so.scale = (0.4, 0.62, 0.05)
        sb = so.modifiers.new("bev", "BEVEL"); sb.width = 0.2; sb.segments = 5; sb.affect = "EDGES"; smooth(so, 0.9); so.data.materials.append(M["sole"])
        P[f"shoe{s}"], P[f"sole{s}"] = sh, so
    # extras
    P["qmark"] = text("qmark", "?", 0.6, (0.95, -0.2, 1.05), (math.radians(90), 0, math.radians(-12)), M["white"], root)
    P["bang"] = text("bang", "!", 0.62, (0.0, -0.2, 1.32), (math.radians(90), 0, 0), M["red"], root)
    P["sweat"] = sphere("sweat", 0.07, (0.85, -0.3, 0.55), (0.8, 0.6, 1.2), M["water"], root)
    P["tear"] = sphere("tear", 0.06, (-0.3, -0.27, -0.05), (0.8, 0.6, 1.2), M["water"], body)
    # stars (dizzy)
    stars = []
    for i in range(3):
        me = bpy.data.meshes.new(f"star{i}"); bm = bmesh.new()
        vs = []
        for k in range(10):
            a = math.pi / 2 + k * math.pi / 5; rr = 0.13 if k % 2 == 0 else 0.055
            vs.append(bm.verts.new((rr * math.cos(a), 0, rr * math.sin(a))))
        f = bm.faces.new(vs); ext = bmesh.ops.extrude_face_region(bm, geom=[f])
        bmesh.ops.translate(bm, vec=(0, 0.05, 0), verts=[v for v in ext["geom"] if isinstance(v, bmesh.types.BMVert)])
        bm.to_mesh(me); bm.free()
        so_ = bpy.data.objects.new(f"star{i}", me); link(so_, root, M["star"]); stars.append(so_)
    P["stars"] = stars
    # price tag prop (bonk / dodge)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 3))
    tag = bpy.context.active_object; tag.name = "tag"; tag.scale = (0.5, 0.025, 0.3)
    tbv = tag.modifiers.new("bev", "BEVEL"); tbv.width = 0.02; tbv.segments = 2; tag.data.materials.append(M["paper"])
    tt = text("tag_txt", "$9.99", 0.2, (0.03, -0.03, 0.0), (math.radians(90), 0, 0), M["red"], None, extrude=0.005)
    tt.parent = tag; tt.scale = (2.0, 2.0, 40.0)  # compensate the parent's scale
    tt.location = (0.05, -0.6, -0.1)
    P["tag"] = tag
    return P


# ---------------------------------------------------------------- v2 CINEMA QUALITY
def _bsdf(m):
    nt = m.node_tree
    return nt, nt.nodes["Principled BSDF"]


def _set(b, **kw):
    names = {"coat": "Coat Weight", "coat_rough": "Coat Roughness", "sheen": "Sheen Weight", "sheen_rough": "Sheen Roughness",
             "sss": "Subsurface Weight", "aniso": "Anisotropic", "rough": "Roughness", "metal": "Metallic", "ior": "IOR"}
    for k, v in kw.items():
        n = names.get(k, k)
        if n in b.inputs: b.inputs[n].default_value = v


def _bump_tree(m, layers, strength, distance=0.004, rough_mod=None):
    """Procedural micro-surface: sum of height layers -> Bump -> Normal; optional roughness modulation.
    layers: list of (kind, scale, weight, extra) with kind in noise|rings|scratch|waves."""
    nt, b = _bsdf(m); N = nt.nodes; L = nt.links
    for l in list(L):
        if l.to_node == b and l.to_socket.name in ("Normal", "Roughness"): L.remove(l)
    tc = N.new("ShaderNodeTexCoord"); acc = None
    for kind, scale, weight, extra in layers:
        if kind == "noise":
            t = N.new("ShaderNodeTexNoise"); t.inputs["Scale"].default_value = scale; t.inputs["Detail"].default_value = extra or 8
            L.new(tc.outputs["Object"], t.inputs["Vector"]); out = t.outputs["Fac"]
        elif kind == "rings":  # lathe / machining rings around the coin axis
            t = N.new("ShaderNodeTexWave"); t.wave_type = "RINGS"; t.inputs["Scale"].default_value = scale
            t.inputs["Distortion"].default_value = extra or 0.6; t.inputs["Detail"].default_value = 2
            L.new(tc.outputs["Object"], t.inputs["Vector"]); out = t.outputs["Fac"]
        elif kind == "waves":  # soft satin folds
            t = N.new("ShaderNodeTexWave"); t.inputs["Scale"].default_value = scale; t.inputs["Distortion"].default_value = extra or 3
            L.new(tc.outputs["Object"], t.inputs["Vector"]); out = t.outputs["Fac"]
        else:  # scratch: very stretched noise through a narrow ramp -> thin random hairline scratches
            mp = N.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (45.0, 1.0, 45.0)  # stretched along the face plane
            mp.inputs["Rotation"].default_value = (0.0, 0.0, extra or 0.0)
            t = N.new("ShaderNodeTexNoise"); t.inputs["Scale"].default_value = scale; t.inputs["Detail"].default_value = 1.5
            L.new(tc.outputs["Object"], mp.inputs["Vector"]); L.new(mp.outputs["Vector"], t.inputs["Vector"])
            cr = N.new("ShaderNodeValToRGB"); e = cr.color_ramp.elements
            e[0].position = 0.495; e[0].color = (0, 0, 0, 1); e[1].position = 0.505; e[1].color = (1, 1, 1, 1)
            cr.color_ramp.interpolation = "EASE"
            nw = cr.color_ramp.elements.new(0.515); nw.color = (0, 0, 0, 1)
            L.new(t.outputs["Fac"], cr.inputs["Fac"]); out = cr.outputs["Color"]
        mul = N.new("ShaderNodeMath"); mul.operation = "MULTIPLY"; mul.inputs[1].default_value = weight
        L.new(out, mul.inputs[0])
        if acc is None: acc = mul.outputs[0]
        else:
            add = N.new("ShaderNodeMath"); add.operation = "ADD"; L.new(acc, add.inputs[0]); L.new(mul.outputs[0], add.inputs[1]); acc = add.outputs[0]
    bp = N.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = strength; bp.inputs["Distance"].default_value = distance
    L.new(acc, bp.inputs["Height"]); L.new(bp.outputs["Normal"], b.inputs["Normal"])
    if "Coat Normal" in b.inputs and m.name.startswith("gold"):
        pass  # the clear coat stays perfectly smooth (polished look over the micro-detail)
    if rough_mod:  # roughness = lo..hi driven by the same micro-surface (scratches are rougher)
        lo, hi = rough_mod
        mr = N.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = 0.0; mr.inputs["From Max"].default_value = 1.0
        mr.inputs["To Min"].default_value = lo; mr.inputs["To Max"].default_value = hi
        L.new(acc, mr.inputs["Value"]); L.new(mr.outputs["Result"], b.inputs["Roughness"])


def _card(sc, name, loc, size, strength, color=(1, 1, 1)):
    """Emission card seen only in reflections (classic product-shot trick for metal)."""
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); o.location = loc; o.scale = (size[0], size[1], 1)
    o.rotation_euler = (Vector((0, 0, 0)) - Vector(loc)).to_track_quat("Z", "Y").to_euler()
    m = bpy.data.materials.new(name + "_m"); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = strength; em.inputs["Color"].default_value = (*color, 1)
    out = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], out.inputs[0])
    me.materials.append(m)
    for attr in ("visible_camera", "visible_diffuse", "visible_shadow", "visible_transmission", "visible_volume_scatter"):
        if hasattr(o, attr): setattr(o, attr, False)
    sc.collection.objects.link(o); return o


def cinema_upgrade(P, sc, look="Medium High Contrast"):
    """v2: film-grade materials, lights and render settings on top of the v1 build (same shapes, same poses)."""
    M = P["M"]
    sc.cycles.adaptive_threshold = 0.02; sc.cycles.adaptive_min_samples = 12  # OIDN (albedo+normal) cleans the rest
    sc.cycles.max_bounces = 6; sc.cycles.glossy_bounces = 3; sc.cycles.diffuse_bounces = 2; sc.cycles.transmission_bounces = 2
    sc.cycles.caustics_reflective = False; sc.cycles.caustics_refractive = False; sc.cycles.blur_glossy = 1.0
    for k, v in (("denoising_input_passes", "RGB_ALBEDO_NORMAL"), ("denoising_prefilter", "ACCURATE"), ("denoising_quality", "HIGH")):
        try: setattr(sc.cycles, k, v)
        except Exception: pass
    try: sc.cycles.filter_width = 1.2
    except Exception: pass
    try: sc.view_settings.look = look
    except Exception: pass
    # --- PBR gold: lathe rings + micro-scratches + smudge roughness map + thin polished clear coat
    g = M["gold"]; _, b = _bsdf(g)
    b.inputs["Base Color"].default_value = (1.0, 0.72, 0.30, 1); _set(b, metal=1.0, coat=0.22, coat_rough=0.04)
    # polished proof-coin field: smudge roughness map (fingerprints/polish) + very fine micro-grain; no stripes
    _bump_tree(g, [("noise", 3, 0.7, 6), ("noise", 420, 0.3, 8)], strength=0.025, distance=0.0015, rough_mod=(0.12, 0.27))
    gr = M["gold_rim"]; _, b = _bsdf(gr)
    b.inputs["Base Color"].default_value = (0.98, 0.66, 0.24, 1); _set(gr.node_tree.nodes["Principled BSDF"], metal=1.0, aniso=0.55, coat=0.15, coat_rough=0.05)
    _bump_tree(gr, [("noise", 160, 0.4, 6), ("scratch", 14, 0.5, 0.5)], strength=0.06, distance=0.002, rough_mod=(0.12, 0.26))
    # --- eyes: wet sclera (coat = cornea), iris discs with fibre detail
    _set(_bsdf(M["eye"])[1], rough=0.18, coat=1.0, coat_rough=0.02, sss=0.18)
    _set(_bsdf(M["pupil"])[1], coat=1.0, coat_rough=0.02)
    iris = bpy.data.materials.new("iris"); iris.use_nodes = True; nt = iris.node_tree; bi = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord"); wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "RINGS"; wv.rings_direction = "SPHERICAL"
    wv.inputs["Scale"].default_value = 26; wv.inputs["Distortion"].default_value = 6; wv.inputs["Detail"].default_value = 4
    cr = nt.nodes.new("ShaderNodeValToRGB"); cr.color_ramp.elements[0].color = (0.12, 0.05, 0.015, 1); cr.color_ramp.elements[1].color = (0.55, 0.30, 0.08, 1)
    nt.links.new(tc.outputs["Object"], wv.inputs["Vector"]); nt.links.new(wv.outputs["Fac"], cr.inputs["Fac"]); nt.links.new(cr.outputs["Color"], bi.inputs["Base Color"])
    _set(bi, rough=0.3, coat=1.0, coat_rough=0.02)
    for s in (-1, 1):
        P[f"iris{s}"] = sphere(f"iris{s}", 0.115, (0.3 * s, -0.225, 0.15), (1, 0.3, 1), iris, P["body"])
    # --- fabrics and rubber
    _set(_bsdf(M["glove"])[1], rough=0.55, sheen=0.7, sheen_rough=0.35, sss=0.12)
    _bump_tree(M["glove"], [("noise", 420, 0.6, 4), ("noise", 25, 0.4, 3)], strength=0.05, distance=0.002)
    for k in ("tie", "tie_d"):
        _set(_bsdf(M[k])[1], rough=0.26, sheen=0.55, aniso=0.45, coat=0.15)
        _bump_tree(M[k], [("waves", 7, 0.6, 3.5), ("noise", 300, 0.2, 3)], strength=0.12, distance=0.004)
    _bsdf(M["shoe"])[1].inputs["Base Color"].default_value = (0.0, 0.42, 0.16, 1)
    _set(_bsdf(M["shoe"])[1], rough=0.36, coat=0.25, coat_rough=0.12)
    _bump_tree(M["shoe"], [("noise", 260, 0.5, 6)], strength=0.04, distance=0.002)
    _bump_tree(M["sole"], [("noise", 200, 0.6, 4)], strength=0.08, distance=0.002, rough_mod=(0.5, 0.7))
    _bsdf(M["ink"])[1].inputs["Base Color"].default_value = (0.018, 0.016, 0.02, 1)
    _set(_bsdf(M["ink"])[1], rough=0.42, coat=0.12, coat_rough=0.2, sheen=0.2)
    _bump_tree(M["paper"], [("noise", 180, 0.7, 5)], strength=0.1, distance=0.002)
    # --- cinematic lighting: dominant warm key (soft, deep shadow), low cool fill, double rim, top kicker
    L = {o.name: o for o in sc.objects if o.type == "LIGHT"}
    def put(name, loc, size, energy, color):
        o = L.get(name)
        if o is None:
            Ld = bpy.data.lights.new(name, "AREA"); o = bpy.data.objects.new(name, Ld); sc.collection.objects.link(o)
        o.location = loc; o.data.size = size; o.data.energy = energy; o.data.color = color
        o.rotation_euler = (Vector((0, 0, -0.1)) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    put("key", (-4.2, -6.0, 5.6), 3.2, 980, (1.0, 0.90, 0.78))
    put("fill", (6.0, -5.0, 0.6), 8.0, 150, (0.70, 0.80, 1.0))
    put("rim", (3.2, 4.6, 3.2), 2.2, 1900, (0.85, 0.92, 1.0))
    put("rim2", (-3.4, 4.4, 2.2), 2.2, 1700, (1.0, 0.86, 0.62))
    put("softbox", (-2.5, -12.0, 7.5), 7.0, 230, (1.0, 0.97, 0.9))  # high & left: top-left -> bottom-right gradient on the gold
    put("top", (0.2, -0.8, 7.0), 1.6, 260, (1.0, 0.97, 0.92))
    # reflection cards: long highlights along the gold edges (seen only in reflections)
    _card(sc, "card_l", (-3.2, -3.4, 0.9), (0.7, 4.5), 6.0, (1.0, 0.95, 0.88))
    _card(sc, "card_r", (3.4, -2.8, 0.4), (0.6, 4.0), 4.5, (0.88, 0.94, 1.0))
    _card(sc, "card_top", (0.0, -2.6, 3.6), (4.0, 0.8), 3.0, (1.0, 1.0, 1.0))
    sc.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.28
    # --- v2 geometry detail: domed face field, beaded border, thicker rim, set-in eyes with lids, tapered limbs,
    #     gloves with fingers + cuffs, sneaker toe caps. Face features move forward to sit on the dome.
    body, root = P["body"], P["root"]
    dome = sphere("face_dome", 0.84, (0, -0.15, 0), (1, 0.06, 1), M["gold"], body, seg=96)
    for nm in ("ring_f", "ring_b"):
        o = sc.objects.get(nm)
        if o: o.scale = (1.0, 1.0, 1.9)  # taller raised rim (local Z of the rotated torus = depth toward the camera)
    bead_me = bpy.data.meshes.new("bead"); bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=10, v_segments=6, radius=0.022)
    bmesh.ops.translate(bm, vec=(0.92, -0.166, 0.0), verts=bm.verts[:]); bm.to_mesh(bead_me); bm.free()
    bead = bpy.data.objects.new("beads", bead_me); link(bead, body, M["gold_rim"]); smooth(bead, 1.2)
    emp = bpy.data.objects.new("bead_rot", None); sc.collection.objects.link(emp); emp.parent = body
    emp.rotation_euler = (0, math.radians(360 / 84), 0)
    arr = bead.modifiers.new("arr", "ARRAY"); arr.count = 84; arr.use_relative_offset = False; arr.use_object_offset = True; arr.offset_object = emp
    P["face_dy"] = {"brow": -0.02, "eyeline": -0.02, "mouth_line": -0.035, "tongue": -0.035}
    for k, dy in (("mouth_open", -0.035), ("teeth", -0.035), ("mouth_o", -0.035), ("cheek-1", -0.04), ("cheek1", -0.04)):
        P[k].location.y += dy
    for s in (-1, 1):  # tapered, thicker limbs (radius per bezier point)
        for k, rad in ((f"arm{s}", (1.35, 1.12, 0.92)), (f"leg{s}", (1.3, 1.15, 1.05))):
            P[k].data.bevel_depth = 0.052
            for bp_, r_ in zip(P[k].data.splines[0].bezier_points, rad): bp_.radius = r_
        fingers = [sphere(f"finger{s}_{j}", 0.052, (0, 0, 0), (0.78, 0.78, 1.55), M["glove"], root, seg=24) for j in range(3)]
        cuff = None
        bpy.ops.mesh.primitive_torus_add(major_radius=0.105, minor_radius=0.038, major_segments=40, minor_segments=12)
        cuff = bpy.context.active_object; cuff.name = f"cuff{s}"; cuff.parent = root; smooth(cuff, 1.2); cuff.data.materials.append(M["glove"])
        P[f"fingers{s}"] = fingers; P[f"cuff{s}"] = cuff
        P[f"hand{s}"].scale = (1.05, 0.8, 0.95)
        toe = sphere(f"toe{s}", 1.0, (0.42 * s, -0.46, -1.47), (0.11, 0.06, 0.05), M["sole"], root)
        P[f"toe{s}"] = toe


def _glove(P, s, hand, elbow, show_all=True):
    """Place the glove fingers + cuff along the forearm direction (2D in the X/Z plane)."""
    if f"fingers{s}" not in P: return
    dx, dz = hand[0] - elbow[0], hand[2] - elbow[2]; n = math.hypot(dx, dz) or 1.0; dx, dz = dx / n, dz / n
    beta = math.atan2(dx, dz); px, pz = -dz, dx  # perpendicular in the X/Z plane
    for j, (off, fwd) in enumerate(((-0.075, 0.12), (0.0, 0.145), (0.075, 0.12))):
        f = P[f"fingers{s}"][j]
        f.location = (hand[0] + dx * fwd + px * off, hand[1] - 0.02, hand[2] + dz * fwd + pz * off)
        f.rotation_euler = (0, beta + off * 2.2, 0); show(f, show_all)
    c = P[f"cuff{s}"]; c.location = (hand[0] - dx * 0.13, hand[1], hand[2] - dz * 0.13); c.rotation_euler = (0, beta, 0); show(c, show_all)


# ---------------------------------------------------------------- posing
ARMS = {"shocked": [(-1.55, 0.8), (1.55, 0.8)], "happy": [(-1.45, -0.3), (1.5, 0.55)], "laugh": [(-0.55, -0.72), (0.55, -0.72)],
        "smug": [(-0.98, -0.55), (1.0, -0.55)], "confused": [(-1.4, -0.45), (0.62, 1.08)], "sideeye": [(-1.2, -0.8), (1.2, -0.8)],
        "sad": [(-1.1, -1.0), (1.1, -1.0)], "angry": [(-1.3, 0.3), (1.3, 0.3)], "point": [(-1.25, -0.65), (1.8, 0.2)],
        "dizzy": [(-1.5, -0.1), (1.5, -0.5)], "thumbsup": [(-1.2, -0.7), (1.45, 0.75)], "proud": [(-0.98, -0.5), (0.98, -0.5)]}
BROWS = {"shocked": (0.13, 0.13), "angry": (-0.11, 0.07), "sad": (0.09, -0.06), "sideeye": (-0.04, -0.04), "laugh": (0.07, 0.04),
         "happy": (0.05, 0.02), "point": (0.04, 0.02), "dizzy": (0.1, -0.02), "thumbsup": (0.06, 0.03), "proud": (0.08, 0.06),
         "smug": (0.0, 0.0), "confused": (0.0, 0.0)}
LINE = {"point": [(-0.2, -0.24), (-0.1, -0.31), (0, -0.33), (0.1, -0.31), (0.2, -0.24)],
        "sad": [(-0.2, -0.37), (-0.1, -0.3), (0, -0.28), (0.1, -0.3), (0.2, -0.37)],
        "smug": [(-0.2, -0.31), (-0.08, -0.32), (0.04, -0.31), (0.16, -0.27), (0.26, -0.2)],
        "sideeye": [(-0.17, -0.29), (-0.08, -0.29), (0, -0.295), (0.1, -0.3), (0.2, -0.31)],
        "confused": [(-0.2, -0.28), (-0.1, -0.33), (0, -0.27), (0.1, -0.33), (0.2, -0.28)],
        "angry": [(-0.2, -0.35), (-0.1, -0.3), (0, -0.29), (0.1, -0.3), (0.2, -0.35)],
        "dizzy": [(-0.2, -0.28), (-0.1, -0.33), (0, -0.27), (0.1, -0.33), (0.2, -0.28)]}
OPEN = {"happy": (0.26, 0.17), "laugh": (0.34, 0.25), "thumbsup": (0.25, 0.16), "proud": (0.23, 0.13)}
LIDS = {"happy": -30, "thumbsup": -32, "point": -34, "smug": -12, "sideeye": -4, "sad": -22, "angry": -24}


def show(o, v):
    o.hide_render = not v


def pose(P, mood, t, act=None, act_t=0.0):
    """t = seconds inside the 1-s idle loop; act_t = seconds inside an act."""
    root, body, M = P["root"], P["body"], P["M"]
    w = 2 * math.pi * t  # one cycle per loop
    root.location = (0, 0, 0.03 * math.sin(w)); root.rotation_euler = (0, 0, math.radians(-8)); root.scale = (1, 1, 1)
    body.rotation_euler = (0, 0, 0); body.scale = (1, 1, 1 + 0.012 * math.sin(w))
    tilt = 0.0; jx = 0.0; jz = 0.0; spin = 0.0; sx = 1.0; sz = 1.0
    if mood == "shocked": jx = 0.015 * math.sin(w * 9)
    elif mood == "laugh": jz = 0.06 * abs(math.sin(w * 2)); tilt = 5 * math.sin(w * 2)
    elif mood == "confused": tilt = 9
    elif mood == "dizzy": tilt = 7 * math.sin(w); jx = 0.04 * math.sin(w)
    elif mood == "angry": jx = 0.012 * math.sin(w * 11)
    elif mood == "sad": jz = -0.03; sz = 0.98
    elif mood == "proud": sz = 1.025; jz = 0.02
    elif mood == "happy": jz = 0.04 * abs(math.sin(w * 2))
    tag_pos = None; stars_on = mood == "dizzy"; star_t = t
    if act == "flip":
        p = min(1.0, act_t / 0.7); jz += 0.9 * math.sin(p * math.pi); spin = 720 * p
    elif act == "bonk":
        if act_t < 0.22: tag_pos = (0.1, -0.25, 3.0 - (3.0 - 1.15) * (act_t / 0.22) ** 2)
        elif act_t < 0.4:
            q = (act_t - 0.22) / 0.18; sz *= 1 - 0.16 * math.sin(q * math.pi); sx *= 1 + 0.1 * math.sin(q * math.pi)
            tag_pos = (0.35 + q * 0.6, -0.3, 1.15 - q * 1.6)
        if act_t >= 0.3: stars_on = True; star_t = act_t
    elif act == "dodge":
        p = min(1.0, act_t / 0.75); tilt += -24 * math.sin(p * math.pi); jx += 0.12 * math.sin(p * math.pi)
        tag_pos = (2.4 - 4.8 * p, -0.4, 0.5)
    root.location = (jx, 0, root.location.z + jz)
    root.rotation_euler = (0, math.radians(tilt), math.radians(-8))
    body.rotation_euler = (0, 0, math.radians(spin)); body.scale = (sx, 1, sz * body.scale.z)
    # eyes / lids / pupils
    blink = (0.62 < t < 0.70) and mood not in ("shocked", "dizzy", "laugh", "proud")
    closed_happy = mood in ("laugh", "proud")
    for s in (-1, 1):
        e, p_, lid = P[f"eye{s}"], P[f"pupil{s}"], P[f"lid{s}"]
        big = 1.25 if mood == "shocked" else 1.0
        e.scale = (big, 0.45, 1.25 * big)
        show(e, not (blink or closed_happy)); show(p_, not (blink or closed_happy))
        show(P[f"eyeline{s}"], blink or closed_happy)
        up = 0.08 if closed_happy else 0.0
        set_curve(P[f"eyeline{s}"], [(0.3 * s - 0.17, -0.2, 0.15 - up * 0.3), (0.3 * s, -0.2, 0.15 + up), (0.3 * s + 0.17, -0.2, 0.15 - up * 0.3)])
        px = {"sideeye": 0.1, "smug": 0.05, "point": 0.08}.get(mood, 0.0); pz = {"sad": -0.06, "confused": 0.08}.get(mood, 0.0)
        if mood == "dizzy": px = 0.05 * math.cos(w * 3 + s); pz = 0.05 * math.sin(w * 3 + s)
        p_.location = (0.3 * s + px, -0.235 - (0.03 if mood == "shocked" else 0), 0.14 + pz)
        p_.scale = (0.8 if mood == "shocked" else 1.0, 0.4, 0.8 if mood == "shocked" else 1.0)
        if f"iris{s}" in P:  # v2 cinema: iris disc follows the pupil (gaze, blink, shock)
            ir = P[f"iris{s}"]; show(ir, not (blink or closed_happy))
            ir.location = (p_.location.x, -0.225, p_.location.z)
            k_ = 0.85 if mood == "shocked" else 1.0; ir.scale = (k_, 0.3, k_)
        if "face_dy" in P:  # v2 cinema: real upper lids on every expression (rest -38°; heavier = closer to 0)
            show(lid, not (blink or closed_happy or mood in ("shocked", "dizzy")))
            ang = LIDS.get(mood, -38)
            if mood == "confused" and s == 1: ang = -18
            lid.rotation_euler = (math.radians(ang), math.radians({"angry": 14, "sad": -10}.get(mood, 0) * s), 0)
        else:
            show(lid, mood in ("smug", "sideeye") and not blink)
            lid.rotation_euler = (math.radians(-12 if mood == "smug" else -4), 0, 0)
        inn, out = BROWS.get(mood, (0, 0))
        if mood == "smug" and s == 1: inn, out = 0.1, 0.15
        if mood == "confused": inn, out = ((0.13, 0.1) if s == 1 else (-0.02, -0.02))
        bz = 0.5 + (0.1 if mood == "shocked" else 0)
        set_curve(P[f"brow{s}"], [(0.12 * s, -0.19, bz + inn - 0.02), (0.29 * s, -0.19, bz + (inn + out) / 2 + 0.02), (0.46 * s, -0.19, bz + out - 0.02)])
        show(P[f"cheek{s}"], mood in ("happy", "laugh", "thumbsup", "proud", "point"))
    # mouth
    show(P["mouth_open"], mood in OPEN); show(P["tongue"], mood in OPEN or mood == "shocked")
    show(P["teeth"], mood == "laugh"); show(P["mouth_o"], mood == "shocked"); show(P["mouth_line"], mood in LINE)
    if mood in OPEN:
        w_, h_ = OPEN[mood]
        if mood == "laugh": h_ *= 1 + 0.15 * abs(math.sin(w * 2))
        P["mouth_open"].scale = (w_, 0.07, h_); P["tongue"].location = (0, -0.19, -0.22 - h_ * 0.62); P["tongue"].scale = (w_ * 0.45, 0.05, h_ * 0.33)
        P["teeth"].scale = (w_ * 1.5, 0.03, 0.05)
    if mood == "shocked":
        P["tongue"].location = (0, -0.2, -0.43); P["tongue"].scale = (0.07, 0.04, 0.04)
    if mood in LINE:
        set_curve(P["mouth_line"], [(x, -0.17, z) for x, z in LINE[mood]])
    M["gold"].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = ((1.0, 0.48, 0.22, 1) if mood == "angry" else (1.0, 0.70, 0.22, 1))
    # tie wiggle
    wig = 6 * math.sin(w * 3) if mood in ("happy", "laugh", "proud", "thumbsup") else 0
    for s in (-1, 1): P[f"tie{s}"].rotation_euler = (math.radians(wig * s), math.radians(-90 * s), 0)
    edge_on = act == "flip" and abs(math.cos(math.radians(spin))) < 0.3
    for k in ("tie-1", "tie1", "knot"): show(P[k], not edge_on)
    # arms
    for i, s in enumerate((-1, 1)):
        hx, hz = ARMS.get(mood, [(-1.4, -0.4), (1.4, -0.4)])[i]
        hy = -0.25
        if mood == "laugh": hy = -0.38
        if mood == "happy" and s == 1: hz += 0.14 * math.sin(w * 4)
        hz += 0.02 * math.sin(w + s)
        sh = (0.96 * s * sx, 0.0, -0.1 + jz * 0)
        hand = (hx, hy, hz)
        elbow = ((sh[0] + hx) / 2 + 0.12 * s, (sh[1] + hy) / 2, (sh[2] + hz) / 2 - 0.12)
        if edge_on: hand = (0.2 * s, 0, -0.1); elbow = (0.15 * s, 0, -0.1); sh = (0.1 * s, 0, -0.1)
        set_curve(P[f"arm{s}"], [sh, elbow, hand])
        P[f"hand{s}"].location = hand
        _glove(P, s, hand, elbow, show_all=not edge_on)
        show(P[f"thumb{s}"], mood == "thumbsup" and s == 1)
        P[f"thumb{s}"].location = (hand[0], hand[1] - 0.02, hand[2] + 0.17)
    # extras
    show(P["qmark"], mood == "confused"); P["qmark"].location = (0.95, -0.2, 1.05 + 0.04 * math.sin(w))
    show(P["bang"], mood == "shocked"); show(P["sweat"], mood == "shocked")
    show(P["tear"], mood == "sad"); P["tear"].location = (-0.3, -0.27, -0.02 - 0.35 * t)
    for i, so in enumerate(P["stars"]):
        show(so, stars_on)
        a = star_t * 2 * math.pi * 1.5 + i * 2.094
        so.location = (0.62 * math.cos(a), -0.3 * math.sin(a) - 0.1, 1.2 + 0.12 * math.sin(a)); so.rotation_euler = (0, a, 0)
    show(P["tag"], tag_pos is not None)
    for c in P["tag"].children: show(c, tag_pos is not None)
    if tag_pos: P["tag"].location = tag_pos; P["tag"].rotation_euler = (0, math.radians(12), 0)
    fd = P.get("face_dy")
    if fd:  # v2 cinema: face features sit on the domed face (curves were just reset above, so this never accumulates)
        for s in (-1, 1):
            for key, d in ((f"brow{s}", fd["brow"]), (f"eyeline{s}", fd["eyeline"])):
                for bp_ in P[key].data.splines[0].bezier_points: bp_.co.y += d
        if mood in LINE:
            for bp_ in P["mouth_line"].data.splines[0].bezier_points: bp_.co.y += fd["mouth_line"]
        if mood in OPEN or mood == "shocked": P["tongue"].location.y += fd["tongue"]


def render_clip(P, out, name, mood, n, act=None):
    sc = bpy.context.scene
    for i in range(n):
        f = os.path.join(out, f"{name}_{i:02d}.png")
        if os.path.exists(f): continue
        tt = i / FPS
        pose(P, mood, (tt % 1.0), act=act, act_t=tt)
        sc.render.filepath = f
        bpy.ops.render.render(write_still=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="buck3d"); ap.add_argument("--res", type=int, default=720)
    ap.add_argument("--samples", type=int, default=32); ap.add_argument("--only", default="")
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--cinema", action="store_true", help="v2 cinema quality (defaults 1080 px, 64 samples)")
    ap.add_argument("--look", default="Medium High Contrast"); ap.add_argument("--threads", type=int, default=0)
    a = ap.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:])
    if a.cinema and "--res" not in sys.argv: a.res = 1080
    if a.cinema and "--samples" not in sys.argv: a.samples = 64
    os.makedirs(a.out, exist_ok=True)
    P = build(a.res, a.samples)
    if a.cinema: cinema_upgrade(P, bpy.context.scene, a.look)
    if a.threads:
        bpy.context.scene.render.threads_mode = "FIXED"; bpy.context.scene.render.threads = a.threads
    clips = [(m, m, FPS, None) for m in MOODS] + [("flip_happy", "happy", ACTS["flip"], "flip"),
             ("bonk_dizzy", "dizzy", ACTS["bonk"], "bonk"), ("dodge_shocked", "shocked", ACTS["dodge"], "dodge")]
    if a.only:
        order = a.only.split(","); clips = sorted([c for c in clips if c[0] in order], key=lambda c: order.index(c[0]))
    for name, mood, n, act in clips:
        render_clip(P, a.out, name, mood, a.frames or n, act)
        print("done", name, flush=True)


if __name__ == "__main__":
    main()
