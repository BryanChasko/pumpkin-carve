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
    rind_lit="#C33D0F", rind_groove="#7A2408",
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
    return mat


def build_stem(name, mat, col):
    # short corky tan stem: tapered cylinder, slight lean, flared base
    stem = H.add_cylinder(name, 0.028, 0.055, radius_top=0.020,
                          vertices=24, mat=mat, collection=col)
    stem.location = (0.006, 0.0, 0.160 + 0.022)
    stem.rotation_euler = (0.0, math.radians(7), 0.0)
    base = H.add_cylinder(name + "Base", 0.042, 0.020, radius_top=0.030,
                          vertices=24, mat=mat, collection=col)
    base.location = (0.0, 0.0, 0.165)
    return [stem, base]


def render_view(cam, body, parts, azimuth, path):
    H.frame_objects(cam, [body] + parts, azimuth=azimuth, elevation=5.0,
                    margin=P["margin"])
    H.render_still(path, background=P["bg"])


def main():
    H.reset_scene()
    col = H.collection("Cinderella")
    rind = rind_material()
    stem_mat = H.material("CinderellaStem", P["stem_color"], roughness=0.9)
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
