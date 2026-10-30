"""Sugar pie: small neat round pie pumpkin, smooth bright rind.

Construction (differs from every other cultivar): primitive-deform.
A bmesh UV sphere is scaled to pie proportions, ribbed by a shallow
radial displacement in Python, then smoothed with a Subdivision Surface
modifier for the grocery-pumpkin finish. Thick ridged upright stem is a
hand-built bmesh cylinder with 7 bark ridges. Whole uncarved fruit.

GUI track: Add > Mesh > UV Sphere, scale, Subdivision Surface modifier;
stem Add > Mesh > Cylinder with loop-cut ridges. Steps in tutorial.md.

Spec: refs/sugar-pie/README.md.
Rebuild: blender -b --factory-startup --python-exit-code 1 -P blender/cultivars/sugar_pie.py [-- --preview]
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
    R=0.19, sx=1.0, sy=0.94, sz=0.90,
    lobes=18, groove_depth=0.07, groove_pow=0.60,
    rind="#E86A10", rind_groove="#A85A10",
    stem_c="#6B6B3A",
    bg="#909399", exposure=1.0, lens=70, margin=1.12,
)


def build_body(name, mat, col):
    R, N = P["R"], P["lobes"]
    phase = -math.pi / 2 - math.pi / N
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=72, v_segments=36, radius=R)
    glay = bm.verts.layers.float.new("groove")
    for v in bm.verts:
        x, y, z = v.co.x, v.co.y, v.co.z
        a = math.atan2(y / P["sy"], x / P["sx"])
        g = (0.5 - 0.5 * math.cos(N * (a - phase))) ** P["groove_pow"]
        rr = 1 - P["groove_depth"] * g
        x, y = x * rr * P["sx"], y * rr * P["sy"]
        z = z * P["sz"] + R * P["sz"]
        if z < 0.02:
            z = 0.02 + (z - 0.02) * 0.4
        v.co.x, v.co.y, v.co.z = x, y, z
        v[glay] = g
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    obj = bpy.data.objects.new(name, H.mesh_from_bmesh(name, bm))
    H.link(obj, col)
    H.assign(obj, mat)
    sub = obj.modifiers.new("Smooth", "SUBSURF")
    sub.levels = 2
    sub.render_levels = 2
    H.shade_smooth(obj, angle=35)
    return obj


def build_stem(name, mat, col):
    # thick upright ridged stem: 7 bark ridges around, slight taper
    sides, rings, h = 28, 5, 0.12
    r0, r1 = 0.034, 0.026
    bm = bmesh.new()
    grid = []
    for j in range(rings + 1):
        f = j / rings
        r = r0 + (r1 - r0) * f
        ring = []
        for i in range(sides):
            a = 2 * math.pi * i / sides
            rr = r * (1 + 0.09 * math.sin(7 * a))
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
    topz = 2 * P["R"] * P["sz"]
    obj.location = (0.0, 0.0, topz - 0.015)
    return [obj]


def stem_material():
    mat = H.material("SugarPieStemBark", "#5E5E33", roughness=0.9)
    nt = mat.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    base = bsdf.inputs.get("Base Color") or bsdf.inputs[0]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 10.0
    nz.inputs["Detail"].default_value = 3.0
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs["A"].default_value = H.color("#4A4A26")
    mix.inputs["B"].default_value = H.color("#7A7A48")
    nt.links.new(nz.outputs["Fac"], mix.inputs["Factor"])
    nt.links.new(mix.outputs["Result"], base)
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.5
    nt.links.new(nz.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return mat


def rind_material():
    mat = H.material("SugarPieRind", P["rind"], roughness=0.35, coat=0.5)
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
    H.add_noise_variation(mat, scale=9, amount=0.08, roughness_amount=0.05)
    return mat


def render_view(cam, body, parts, azimuth, path):
    H.frame_objects(cam, [body] + parts, azimuth=azimuth, elevation=5.0,
                    margin=P["margin"])
    H.render_still(path, background=P["bg"])


def main():
    H.reset_scene()
    col = H.collection("SugarPie")
    body = build_body("SugarPie", rind_material(), col)
    parts = build_stem("SugarPieStem", stem_material(), col)
    H.studio_lighting(target=[body] + parts, key_azimuth=-40,
                      key_elevation=45, intensity=0.7, contrast=0.75,
                      softness=0.5)
    topz = 2 * P["R"] * P["sz"]
    cam = H.add_camera("Camera", location=(0, -3, 0.3),
                       target=(0, 0, topz / 2), lens=P["lens"])
    if PREVIEW:
        H.set_render(engine="CYCLES", resolution=(480, 320), samples=10,
                     view_transform="Khronos PBR Neutral",
                     exposure=P["exposure"], device="CPU")
    else:
        H.set_render(engine="CYCLES", resolution=(640, 480), samples=24,
                     view_transform="Khronos PBR Neutral",
                     exposure=P["exposure"], device="CPU")
    os.makedirs(VDIR, exist_ok=True)
    render_view(cam, body, parts, 0.0, os.path.join(VDIR, "sugar-pie.png"))
    render_view(cam, body, parts, 90.0,
                os.path.join(VDIR, "sugar-pie-profile.png"))
    H.save_blend(os.path.join(VDIR, "sugar-pie.blend"))
    H.report()


main()
