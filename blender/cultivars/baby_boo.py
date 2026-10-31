"""Baby boo: miniature white pumpkin, shown as a cluster of three.

Construction (differs from every other cultivar): build once, instance.
One small ribbed body is built from a polar grid, then two linked
duplicates are placed beside it at varied rotation and scale via
collection instances. Thin upright green-brown stems. Whole uncarved.

GUI track: Object > Duplicate Linked, or Add > Collection Instance.
Steps in tutorial.md.

Spec: refs/baby-boo/README.md.
Rebuild: blender -b --factory-startup --python-exit-code 1 -P blender/cultivars/baby_boo.py [-- --preview]
"""
import math
import os
import sys

SKILL_SCRIPTS = "/home/bryanchasko/.local/share/muse/skills/bundled/muse-core~v1/skills/blender/scripts"
sys.path.insert(0, SKILL_SCRIPTS)

import bpy  # noqa: E402
import bmesh  # noqa: E402
import bpy_helpers as H  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(ROOT)
VDIR = os.path.join(ROOT, "tutorial", "variants")
PREVIEW = "--preview" in sys.argv

P = dict(
    R=0.075, sx=1.0, sy=0.94, sz=0.66,
    lobes=10, groove_depth=0.13, groove_pow=0.55,
    segs=100, rings=60,
    dip_depth=0.015, dip_w=0.040,
    rind="#F2EDE2", rind_groove="#C9B895", speckle="#B99B6B",
    stem_green="#5F7031", stem_brown="#7A5C33",
    bg="#909399", exposure=1.0, lens=70, margin=1.12,
)


def build_body(name, mat, col):
    R, N = P["R"], P["lobes"]
    segs, rings = P["segs"], P["rings"]
    phase = -math.pi / 2 - math.pi / N
    CZ = R * P["sz"]
    bm = bmesh.new()
    glay = bm.verts.layers.float.new("groove")
    bot = bm.verts.new((0.0, 0.0, 0.008))
    bot[glay] = 0.0
    top = bm.verts.new((0.0, 0.0, 2 * CZ - P["dip_depth"]))
    top[glay] = 0.0
    grid = [[None] * segs for _ in range(rings + 1)]
    for j in range(1, rings):
        phi = math.pi * j / rings
        sh, zc = math.sin(phi), -math.cos(phi)
        for i in range(segs):
            a = 2 * math.pi * i / segs
            g = (0.5 - 0.5 * math.cos(N * (a - phase))) ** P["groove_pow"]
            rr = R * (1 - P["groove_depth"] * g) * sh
            x = rr * P["sx"] * math.cos(a)
            y = rr * P["sy"] * math.sin(a)
            z = zc * R * P["sz"] + CZ
            rh = math.hypot(x, y)
            if z > 2 * CZ - 0.035:  # crown dip: stem seats into it
                z -= P["dip_depth"] * math.exp(-((rh / P["dip_w"]) ** 2))
            if z < 0.010:  # sit-flat bottom
                z = 0.010 + (z - 0.010) * 0.4
            v = bm.verts.new((x, y, z))
            v[glay] = g
            grid[j][i] = v
    for i in range(segs):
        k = (i + 1) % segs
        bm.faces.new((bot, grid[1][i], grid[1][k]))
        bm.faces.new((top, grid[rings - 1][k], grid[rings - 1][i]))
    for j in range(1, rings - 1):
        for i in range(segs):
            k = (i + 1) % segs
            bm.faces.new((grid[j][i], grid[j + 1][i], grid[j + 1][k],
                          grid[j][k]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    obj = bpy.data.objects.new(name, H.mesh_from_bmesh(name, bm))
    H.link(obj, col)
    H.assign(obj, mat)
    H.shade_smooth(obj, angle=35)
    return obj


def build_stem(name, mat, col, r0, h, seat_z):
    # tall green ridged stem with a 5-lobe star base flaring into
    # the crown dip; mesh origin at its base so scaled dupes seat
    sides, rings = 40, 8
    r1 = r0 * 0.62
    ridge_amp = 0.15
    bm = bmesh.new()
    grid = []
    for j in range(rings + 1):
        f = j / rings
        r = r0 + (r1 - r0) * f
        ring = []
        for i in range(sides):
            a = 2 * math.pi * i / sides
            star = 1 + 0.38 * math.cos(5 * a) * max(0.0, 1 - f / 0.30)
            rr = r * (1 + ridge_amp * math.sin(8 * a + f * 2.5)) * star
            ring.append(bm.verts.new((rr * math.cos(a), rr * math.sin(a),
                                      f * h)))
        grid.append(ring)
    for j in range(rings):
        for i in range(sides):
            k = (i + 1) % sides
            bm.faces.new((grid[j][i], grid[j][k], grid[j + 1][k],
                          grid[j + 1][i]))
    bm.faces.new(list(grid[0]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    obj = bpy.data.objects.new(name, H.mesh_from_bmesh(name, bm))
    H.link(obj, col)
    H.assign(obj, mat)
    H.shade_smooth(obj, angle=40)
    obj.location = (0.0, 0.0, seat_z)
    obj.rotation_euler = (0.0, math.radians(3), 0.0)
    return obj


def stem_material():
    # green ridged stalk with brown drying patches and fiber bump
    mat = H.material("BabyBooStemGreen", P["stem_green"], roughness=0.8)
    nt = mat.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    base = bsdf.inputs.get("Base Color") or bsdf.inputs[0]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (8.0, 8.0, 3.0)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 2.0
    nz.inputs["Detail"].default_value = 3.0
    nt.links.new(mp.outputs["Vector"], nz.inputs["Vector"])
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.clamp = True
    mr.inputs["From Min"].default_value = 0.45
    mr.inputs["From Max"].default_value = 0.75
    mr.inputs["To Min"].default_value = 0.0
    mr.inputs["To Max"].default_value = 1.0
    nt.links.new(nz.outputs["Fac"], mr.inputs["Value"])
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs["A"].default_value = H.color(P["stem_green"])
    mix.inputs["B"].default_value = H.color(P["stem_brown"])
    nt.links.new(mr.outputs["Result"], mix.inputs["Factor"])
    nt.links.new(mix.outputs["Result"], base)
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.5
    nt.links.new(nz.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return mat


def rind_material():
    mat = H.material("BabyBooRind", P["rind"], roughness=0.55)
    nt = mat.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    base = bsdf.inputs.get("Base Color") or bsdf.inputs[0]
    attr = nt.nodes.new("ShaderNodeAttribute")
    attr.attribute_name = "groove"
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs["A"].default_value = H.color(P["rind"])
    mix.inputs["B"].default_value = H.color(P["rind_groove"])
    nt.links.new(attr.outputs["Fac"], mix.inputs["Factor"])
    # sparse tan freckles (seen in the profile ref): thresholded noise
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (30.0, 30.0, 30.0)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 1.0
    nz.inputs["Detail"].default_value = 2.0
    nt.links.new(mp.outputs["Vector"], nz.inputs["Vector"])
    # threshold remap: From = input range, To = output range
    thr = nt.nodes.new("ShaderNodeMapRange")
    thr.clamp = True
    thr.inputs["From Min"].default_value = 0.70
    thr.inputs["From Max"].default_value = 0.82
    thr.inputs["To Min"].default_value = 0.0
    thr.inputs["To Max"].default_value = 1.0
    nt.links.new(nz.outputs["Fac"], thr.inputs["Value"])
    dens = nt.nodes.new("ShaderNodeMath")
    dens.operation = "MULTIPLY"
    nt.links.new(thr.outputs["Result"], dens.inputs[0])
    dens.inputs[1].default_value = 0.8
    spmix = nt.nodes.new("ShaderNodeMix")
    spmix.data_type = "RGBA"
    spmix.inputs["B"].default_value = H.color(P["speckle"])
    nt.links.new(mix.outputs["Result"], spmix.inputs["A"])
    nt.links.new(dens.outputs["Value"], spmix.inputs["Factor"])
    nt.links.new(spmix.outputs["Result"], base)
    # groove-driven roughness: satin crests, matte valleys
    gr = nt.nodes.new("ShaderNodeMapRange")
    gr.clamp = True
    gr.inputs["From Min"].default_value = 0.0
    gr.inputs["From Max"].default_value = 1.0
    gr.inputs["To Min"].default_value = 0.45
    gr.inputs["To Max"].default_value = 0.65
    nt.links.new(attr.outputs["Fac"], gr.inputs["Value"])
    rough = bsdf.inputs.get("Roughness")
    if rough is not None:
        nt.links.new(gr.outputs["Result"], rough)
    return mat


def render_view(cam, objs, azimuth, path):
    H.frame_objects(cam, objs, azimuth=azimuth, elevation=5.0,
                    margin=P["margin"])
    H.render_still(path, background=P["bg"])


def main():
    H.reset_scene()
    col = H.collection("BabyBoo")
    rind = rind_material()
    topz = 2 * P["R"] * P["sz"]
    seat = topz - P["dip_depth"] - 0.004
    # hero mini at origin; satellites clearly smaller, nestled behind
    hero = build_body("BabyBoo", rind, col)
    hero_stem = build_stem("BabyBooStem", stem_material(), col, 0.013,
                           topz * 0.55, seat)
    # two linked duplicates: same meshes, varied transform, no rebuild
    dupes = []
    for k, (loc, rot, s) in enumerate((
            ((0.115, 0.005, 0.0), (0, 0, 0.7), 0.55),
            ((-0.105, 0.030, 0.0), (0, 0, -0.5), 0.45),
    )):
        d = bpy.data.objects.new("BabyBooMini%d" % k, hero.data)
        H.link(d, col)
        d.location = loc
        d.rotation_euler = (0, 0, rot[2])
        d.scale = (s, s, s)
        dupes.append(d)
        st = bpy.data.objects.new("BabyBooMiniStem%d" % k, hero_stem.data)
        H.link(st, col)
        st.location = (loc[0], loc[1], seat * s)
        st.rotation_euler = (0, 0, rot[2])
        st.scale = (s, s, s)
        dupes.append(st)
    all_objs = [hero, hero_stem] + dupes
    H.studio_lighting(target=all_objs, key_azimuth=-40, key_elevation=45,
                      intensity=0.7, contrast=0.75, softness=0.5)
    cam = H.add_camera("Camera", location=(0, -3, 0.3), target=(0, 0, 0.05),
                       lens=P["lens"])
    if PREVIEW:
        H.set_render(engine="CYCLES", resolution=(480, 320), samples=10,
                     view_transform="Khronos PBR Neutral",
                     exposure=P["exposure"], device="CPU")
    else:
        H.set_render(engine="CYCLES", resolution=(640, 480), samples=24,
                     view_transform="Khronos PBR Neutral",
                     exposure=P["exposure"], device="CPU")
    os.makedirs(VDIR, exist_ok=True)
    render_view(cam, all_objs, 0.0, os.path.join(VDIR, "baby-boo.png"))
    render_view(cam, all_objs, 90.0,
                os.path.join(VDIR, "baby-boo-profile.png"))
    H.save_blend(os.path.join(VDIR, "baby-boo.blend"))
    H.report()


main()
