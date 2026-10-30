"""Kabocha: dark drum with celadon mottling and pale crest stripes.

Construction (differs from every other cultivar): texture-driven skin.
A squat drum body carries a musgrave-noise mottle that drives BOTH the
color mix and a displace modifier, with a second stretched mapping for
the pale stripes along rib crests. No painted patches: all procedural.
Short stubby tan stem. Whole uncarved fruit.

GUI track: Texture Coordinate + Mapping + Musgrave nodes, Displace
modifier with a texture. Steps in tutorial.md.

Spec: refs/kabocha/README.md.
Rebuild: blender -b --factory-startup --python-exit-code 1 -P blender/cultivars/kabocha.py [-- --preview]
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
    R=0.20, sx=1.0, sy=0.96, sz=0.72,
    lobes=13, groove_depth=0.10, groove_pow=0.55,
    segs=156, rings=78,
    rind="#24351F", groove_c="#16220F", mottle="#9FB08A",
    stem_c="#9A7F57",
    mottle_scale=6.0, displace_strength=0.008,
    bg="#909399", exposure=1.0, lens=70, margin=1.12,
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
    top = bm.verts.new((0.0, 0.0, 2 * CZ - 0.008))
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
    H.shade_smooth(obj, angle=40)
    return obj


def add_mottle_displace(obj):
    tex = bpy.data.textures.new("KabochaMottle", "MUSGRAVE")
    tex.noise_scale = 0.25
    tex.musgrave_type = "MULTIFRACTAL"
    mod = obj.modifiers.new("Mottle", "DISPLACE")
    mod.texture = tex
    mod.texture_coords = "OBJECT"
    mod.strength = P["displace_strength"]
    mod.mid_level = 0.5


def rind_material():
    mat = H.material("KabochaRind", P["rind"], roughness=0.55)
    nt = mat.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    base = bsdf.inputs.get("Base Color") or bsdf.inputs[0]
    attr = nt.nodes.new("ShaderNodeAttribute")
    attr.attribute_name = "groove"
    gmix = nt.nodes.new("ShaderNodeMix")
    gmix.data_type = "RGBA"
    gmix.inputs["A"].default_value = H.color(P["rind"])
    gmix.inputs["B"].default_value = H.color(P["groove_c"])
    nt.links.new(attr.outputs["Fac"], gmix.inputs["Factor"])
    # celadon mottle from musgrave noise
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (P["mottle_scale"],) * 3
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    mg = nt.nodes.new("ShaderNodeTexNoise")
    mg.inputs["Scale"].default_value = 4.0
    mg.inputs["Detail"].default_value = 4.0
    mg.inputs["Roughness"].default_value = 0.6
    mg.inputs["Distortion"].default_value = 0.4
    nt.links.new(mp.outputs["Vector"], mg.inputs["Vector"])
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.clamp = True
    mr.inputs["From Min"].default_value = 0.70
    mr.inputs["From Max"].default_value = 0.90
    nt.links.new(mg.outputs["Fac"], mr.inputs["Value"])
    mmix = nt.nodes.new("ShaderNodeMix")
    mmix.data_type = "RGBA"
    mmix.inputs["B"].default_value = H.color(P["mottle"])
    nt.links.new(gmix.outputs["Result"], mmix.inputs["A"])
    nt.links.new(mr.outputs["Result"], mmix.inputs["Factor"])
    # pale stripes along rib crests: stretched mapping, crest-masked noise
    mp2 = nt.nodes.new("ShaderNodeMapping")
    mp2.inputs["Scale"].default_value = (24.0, 24.0, 2.0)
    nt.links.new(tc.outputs["Object"], mp2.inputs["Vector"])
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 6.0
    nt.links.new(mp2.outputs["Vector"], nz.inputs["Vector"])
    sr = nt.nodes.new("ShaderNodeMapRange")
    sr.clamp = True
    sr.inputs["From Min"].default_value = 0.55
    sr.inputs["From Max"].default_value = 0.75
    nt.links.new(nz.outputs["Fac"], sr.inputs["Value"])
    inv = nt.nodes.new("ShaderNodeMath")
    inv.operation = "SUBTRACT"
    inv.inputs[0].default_value = 1.0
    nt.links.new(attr.outputs["Fac"], inv.inputs[1])
    gate = nt.nodes.new("ShaderNodeMath")
    gate.operation = "MULTIPLY"
    nt.links.new(sr.outputs["Result"], gate.inputs[0])
    nt.links.new(inv.outputs["Value"], gate.inputs[1])
    smix = nt.nodes.new("ShaderNodeMix")
    smix.data_type = "RGBA"
    smix.inputs["B"].default_value = H.color("#B8C4A3")
    nt.links.new(mmix.outputs["Result"], smix.inputs["A"])
    nt.links.new(gate.outputs["Value"], smix.inputs["Factor"])
    nt.links.new(smix.outputs["Result"], base)
    return mat


def build_stem(name, mat, col, topz):
    # short stubby tan stem
    stem = H.add_cylinder(name, 0.024, 0.055, radius_top=0.018,
                          vertices=12, mat=mat, collection=col)
    stem.location = (0.0, 0.0, topz + 0.010)
    stem.rotation_euler = (0.0, math.radians(5), 0.0)
    return [stem]


def render_view(cam, body, parts, azimuth, path):
    H.frame_objects(cam, [body] + parts, azimuth=azimuth, elevation=5.0,
                    margin=P["margin"])
    H.render_still(path, background=P["bg"])


def main():
    H.reset_scene()
    col = H.collection("Kabocha")
    body = build_body("Kabocha", rind_material(), col)
    add_mottle_displace(body)
    stem_mat = H.material("KabochaStem", P["stem_c"], roughness=0.85)
    topz = 2 * P["R"] * P["sz"]
    parts = build_stem("KabochaStem", stem_mat, col, topz)
    H.studio_lighting(target=[body] + parts, key_azimuth=-40,
                      key_elevation=45, intensity=0.7, contrast=0.75,
                      softness=0.5)
    cam = H.add_camera("Camera", location=(0, -3, 0.3), target=(0, 0, topz / 2),
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
    render_view(cam, body, parts, 0.0, os.path.join(VDIR, "kabocha.png"))
    render_view(cam, body, parts, 90.0,
                os.path.join(VDIR, "kabocha-profile.png"))
    H.save_blend(os.path.join(VDIR, "kabocha.blend"))
    H.report()


main()
