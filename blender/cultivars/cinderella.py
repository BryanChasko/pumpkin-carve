"""Cinderella (rouge vif d'etampes): flat red disc, dipped crown, 14 ribs.

Construction (differs from every other cultivar): profile-driven lathe.
A measured side-profile polyline is revolved around Z, then each ring is
modulated by a 14-fold radial rib function. The concave crown dip is part
of the profile itself, not a crater hack. Whole uncarved fruit: deep
sutures make real cinderellas hard to carve, so this one is display-only.

GUI track: Add > Mesh > ... no lathe tool exists; the equivalent is the
Screw modifier on a profile edge loop, then a Displace-style rib edit.
Tutorial covers the script path; screw-modifier steps in tutorial.md.

Spec: refs/cinderella/README.md.
Rebuild: blender -b --factory-startup --python-exit-code 1 -P blender/cultivars/cinderella.py [-- --preview]
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
    lobes=14, groove_depth=0.16, groove_pow=0.50,
    segs=196,
    rind_lit="#A82E0C", rind_groove="#5E1C06",
    stem_color="#A08B62", stem_dark="#5E4A2E",
    bg="#909399", exposure=1.0,
    lens=70, margin=1.12,
)

# side profile (r, z), metres: half-width 0.30, height 0.20, crown centre
# dips to 0.160 while the rim rides at 0.185. Bottom sits at z=0.
PROFILE = [
    (0.000, 0.010), (0.080, 0.006), (0.150, 0.004), (0.210, 0.008),
    (0.255, 0.020), (0.285, 0.042), (0.298, 0.070), (0.300, 0.098),
    (0.292, 0.125), (0.275, 0.148), (0.248, 0.165), (0.212, 0.176),
    (0.170, 0.183), (0.125, 0.186), (0.085, 0.184), (0.050, 0.178),
    (0.028, 0.170), (0.012, 0.163), (0.000, 0.160),
]


def build_body(name, mat, col):
    n_seg = P["segs"]
    n_pro = len(PROFILE)
    bm = bmesh.new()
    glay = bm.verts.layers.float.new("groove")
    rings = []
    for j, (r0, z0) in enumerate(PROFILE):
        ring = []
        for i in range(n_seg):
            a = 2 * math.pi * i / n_seg
            g = (0.5 - 0.5 * math.cos(P["lobes"] * a)) ** P["groove_pow"]
            rr = r0 * (1 - P["groove_depth"] * g)
            v = bm.verts.new((rr * math.cos(a), rr * math.sin(a), z0))
            v[glay] = g if r0 > 1e-6 else 0.0
            ring.append(v)
        rings.append(ring)
    for j in range(n_pro - 1):
        for i in range(n_seg):
            k = (i + 1) % n_seg
            try:
                bm.faces.new((rings[j][i], rings[j][k],
                              rings[j + 1][k], rings[j + 1][i]))
            except ValueError:
                pass
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    obj = bpy.data.objects.new(name, H.mesh_from_bmesh(name, bm))
    H.link(obj, col)
    H.assign(obj, mat)
    H.shade_smooth(obj, angle=35)
    return obj


def rind_material():
    mat = H.material("CinderellaRind", P["rind_lit"], roughness=0.5)
    nt = mat.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    base = bsdf.inputs.get("Base Color") or bsdf.inputs[0]
    attr = nt.nodes.new("ShaderNodeAttribute")
    attr.attribute_name = "groove"
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs["A"].default_value = H.color(P["rind_lit"])
    mix.inputs["B"].default_value = H.color(P["rind_groove"])
    nt.links.new(attr.outputs["Fac"], mix.inputs["Factor"])
    nt.links.new(mix.outputs["Result"], base)
    H.add_noise_variation(mat, scale=9, amount=0.12, roughness_amount=0.08)
    # waxy crests, matte valleys: groove drives roughness
    # (From = input range, To = output range)
    gr = nt.nodes.new("ShaderNodeMapRange")
    gr.clamp = True
    gr.inputs["From Min"].default_value = 0.0
    gr.inputs["From Max"].default_value = 1.0
    gr.inputs["To Min"].default_value = 0.32
    gr.inputs["To Max"].default_value = 0.58
    nt.links.new(attr.outputs["Fac"], gr.inputs["Value"])
    rough = bsdf.inputs.get("Roughness")
    if rough is not None:
        nt.links.new(gr.outputs["Result"], rough)
    return mat


def build_stem(name, mat, col):
    # short corky tan stem: 8 bark ridges, slight lean, flared base
    sides, rings, h = 32, 5, 0.070
    r0, r1 = 0.030, 0.021
    bm = bmesh.new()
    grid = []
    for j in range(rings + 1):
        f = j / rings
        r = r0 + (r1 - r0) * f
        ring = []
        for i in range(sides):
            a = 2 * math.pi * i / sides
            rr = r * (1 + 0.12 * math.sin(8 * a + f * 2.0))
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
    obj.location = (0.006, 0.0, 0.160)
    obj.rotation_euler = (0.0, math.radians(7), 0.0)
    base = H.add_cylinder(name + "Base", 0.042, 0.020, radius_top=0.030,
                          vertices=24, mat=mat, collection=col)
    base.location = (0.0, 0.0, 0.165)
    return [obj, base]


def stem_material():
    mat = H.material("CinderellaStemBark", "#8A6F45", roughness=0.95)
    nt = mat.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    base = bsdf.inputs.get("Base Color") or bsdf.inputs[0]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (6.0, 6.0, 14.0)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 8.0
    nz.inputs["Detail"].default_value = 3.0
    nt.links.new(mp.outputs["Vector"], nz.inputs["Vector"])
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs["A"].default_value = H.color("#6E5636")
    mix.inputs["B"].default_value = H.color("#A68D5E")
    nt.links.new(nz.outputs["Fac"], mix.inputs["Factor"])
    nt.links.new(mix.outputs["Result"], base)
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.6
    nt.links.new(nz.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return mat


def render_view(cam, body, parts, azimuth, path):
    H.frame_objects(cam, [body] + parts, azimuth=azimuth, elevation=5.0,
                    margin=P["margin"])
    H.render_still(path, background=P["bg"])


def main():
    H.reset_scene()
    col = H.collection("Cinderella")
    rind = rind_material()
    stem_mat = stem_material()
    body = build_body("Cinderella", rind, col)
    parts = build_stem("CinderellaStem", stem_mat, col)
    H.studio_lighting(target=[body] + parts, key_azimuth=-40,
                      key_elevation=45, intensity=0.7, contrast=0.75,
                      softness=0.5)
    cam = H.add_camera("Camera", location=(0, -3, 0.3), target=(0, 0, 0.10),
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
    render_view(cam, body, parts, 0.0, os.path.join(VDIR, "cinderella.png"))
    render_view(cam, body, parts, 90.0,
                os.path.join(VDIR, "cinderella-profile.png"))
    H.save_blend(os.path.join(VDIR, "cinderella.blend"))
    H.report()


main()
