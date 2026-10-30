"""Harvest moon: big golden ball, the lighting study.

Construction (differs from every other cultivar): smooth globe with a
documented three-point area-light rig. The body is a plain ribbed sphere;
the feature is the light values (warm key, cool fill, rim) tuned so gold
reads without blowing out. Thick green-brown stem. Whole uncarved fruit.

GUI track: Add > Light > Area x3, world and exposure settings copied
from the script values. Steps in tutorial.md.

Spec: refs/harvest-moon/README.md.
Rebuild: blender -b --factory-startup --python-exit-code 1 -P blender/cultivars/harvest_moon.py [-- --preview]
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
    R=0.26, sx=1.0, sy=0.96, sz=0.90,
    lobes=17, groove_depth=0.06, groove_pow=0.60,
    segs=150, rings=75,
    rind="#F0A832", groove_c="#B06A10",
    stem_c="#6B6B3A",
    # documented light rig: warm key, cool fill, warm rim
    key_az=45, key_el=38, key_e=0.90, key_c="#fff1e0",
    fill_az=-65, fill_el=15, fill_e=0.55, fill_c="#e8f0ff",
    rim_az=155, rim_el=35, rim_e=0.80, rim_c="#ffd9b0",
    bg="#909399", exposure=0.95, lens=70, margin=1.12,
)


def build_body(name, mat, col):
    R, N = P["R"], P["lobes"]
    segs, rings = P["segs"], P["rings"]
    phase = -math.pi / 2 - math.pi / N
    CZ = R * P["sz"]
    bm = bmesh.new()
    glay = bm.verts.layers.float.new("groove")
    bot = bm.verts.new((0.0, 0.0, 0.004))
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


def rind_material():
    mat = H.material("HarvestRind", P["rind"], roughness=0.38)
    nt = mat.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    base = bsdf.inputs.get("Base Color") or bsdf.inputs[0]
    attr = nt.nodes.new("ShaderNodeAttribute")
    attr.attribute_name = "groove"
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs["A"].default_value = H.color(P["rind"])
    mix.inputs["B"].default_value = H.color(P["groove_c"])
    nt.links.new(attr.outputs["Fac"], mix.inputs["Factor"])
    nt.links.new(mix.outputs["Result"], base)
    H.add_noise_variation(mat, scale=9, amount=0.08, roughness_amount=0.05)
    return mat


def light_rig(focus, r):
    # three-point rig with written-down values; the point of this file
    dist = r * 4.0

    def at(az, el):
        a, e = math.radians(az), math.radians(el)
        from mathutils import Vector
        return focus + Vector((math.sin(a) * math.cos(e),
                               -math.cos(a) * math.cos(e),
                               math.sin(e))) * dist

    k = dist * dist * 1.0
    key = H.add_light("AREA", "Key", at(P["key_az"], P["key_el"]), focus,
                      energy=10 * k * P["key_e"], size=dist * 0.55,
                      light_color=P["key_c"])
    fill = H.add_light("AREA", "Fill", at(P["fill_az"], P["fill_el"]), focus,
                       energy=10 * k * P["fill_e"], size=dist * 1.2,
                       light_color=P["fill_c"])
    rim = H.add_light("AREA", "Rim", at(P["rim_az"], P["rim_el"]), focus,
                      energy=6 * k * P["rim_e"], size=dist * 0.5,
                      light_color=P["rim_c"])
    H._no_shadow(fill)
    H._no_shadow(rim)
    H.world_color("#0a0d13", 0.7)
    return [key, fill, rim]


def build_stem(name, mat, col, topz):
    stem = H.add_cylinder(name, 0.030, 0.10, radius_top=0.022,
                          vertices=12, mat=mat, collection=col)
    stem.location = (0.0, 0.0, topz + 0.030)
    stem.rotation_euler = (0.0, 0.0, 0.0)
    return [stem]


def render_view(cam, body, parts, azimuth, path):
    H.frame_objects(cam, [body] + parts, azimuth=azimuth, elevation=5.0,
                    margin=P["margin"])
    H.render_still(path, background=P["bg"])


def main():
    H.reset_scene()
    col = H.collection("HarvestMoon")
    body = build_body("HarvestMoon", rind_material(), col)
    stem_mat = H.material("HarvestStem", P["stem_c"], roughness=0.8)
    topz = 2 * P["R"] * P["sz"]
    parts = build_stem("HarvestStem", stem_mat, col, topz)
    lo, hi = H.bbox([body] + parts)
    from mathutils import Vector
    focus = (lo + hi) / 2
    r = max((hi - lo).length / 2, 0.01)
    light_rig(Vector(focus), r)
    cam = H.add_camera("Camera", location=(0, -3, 0.3), target=tuple(focus),
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
    render_view(cam, body, parts, 0.0, os.path.join(VDIR, "harvest-moon.png"))
    render_view(cam, body, parts, 90.0,
                os.path.join(VDIR, "harvest-moon-profile.png"))
    H.save_blend(os.path.join(VDIR, "harvest-moon.blend"))
    H.report()


main()
