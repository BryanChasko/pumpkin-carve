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
    R=0.075, sx=1.0, sy=0.94, sz=0.62,
    lobes=10, groove_depth=0.12, groove_pow=0.55,
    segs=100, rings=50,
    rind="#F2EDE2", rind_groove="#CFC5B2",
    stem_c="#7A6B45",
    bg="#909399", exposure=1.0, lens=70, margin=1.12,
)


def build_body(name, mat, col):
    R, N = P["R"], P["lobes"]
    segs, rings = P["segs"], P["rings"]
    phase = -math.pi / 2 - math.pi / N
    CZ = R * P["sz"]
    bm = bmesh.new()
    glay = bm.verts.layers.float.new("groove")
    bot = bm.verts.new((0.0, 0.0, 0.002))
    bot[glay] = 0.0
    top = bm.verts.new((0.0, 0.0, 2 * CZ))
    top[glay] = 0.0
    grid = [[None] * segs for _ in range(rings + 1)]
    for j in range(1, rings):
        phi = math.pi * j / rings
        sh, zc = math.sin(phi), -math.cos(phi)
        for i in range(segs):
            a = 2 * math.pi * i / segs
            g = (0.5 - 0.5 * math.cos(N * (a - phase))) ** P["groove_pow"]
            rr = R * (1 - P["groove_depth"] * g) * sh
            v = bm.verts.new((rr * P["sx"] * math.cos(a),
                              rr * P["sy"] * math.sin(a),
                              zc * R * P["sz"] + CZ))
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


def build_stem(name, mat, col, r, topz):
    stem = H.add_cylinder(name, r, topz * 0.55, radius_top=r * 0.7,
                          vertices=12, mat=mat, collection=col)
    stem.location = (0.0, 0.0, topz + topz * 0.20)
    stem.rotation_euler = (0.0, math.radians(4), 0.0)
    return stem


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
    nt.links.new(mix.outputs["Result"], base)
    return mat


def render_view(cam, objs, azimuth, path):
    H.frame_objects(cam, objs, azimuth=azimuth, elevation=5.0,
                    margin=P["margin"])
    H.render_still(path, background=P["bg"])


def main():
    H.reset_scene()
    col = H.collection("BabyBoo")
    rind = rind_material()
    stem_mat = H.material("BabyBooStem", P["stem_c"], roughness=0.85)
    topz = 2 * P["R"] * P["sz"]
    # hero mini at origin
    hero = build_body("BabyBoo", rind, col)
    hero_stem = build_stem("BabyBooStem", stem_mat, col, 0.006, topz)
    # two linked duplicates: same mesh, varied transform, no rebuild
    dupes = []
    for k, (loc, rot, s) in enumerate((
            ((0.100, 0.030, 0.0), (0, 0, 0.7), 0.72),
            ((-0.095, 0.045, 0.0), (0, 0, -0.5), 0.60),
    )):
        d = bpy.data.objects.new("BabyBooMini%d" % k, hero.data)
        H.link(d, col)
        d.location = loc
        d.rotation_euler = (0, 0, rot[2])
        d.scale = (s, s, s)
        dupes.append(d)
        st = bpy.data.objects.new("BabyBooMiniStem%d" % k, hero_stem.data)
        H.link(st, col)
        st.location = (loc[0], loc[1], 1.20 * topz * s)
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
