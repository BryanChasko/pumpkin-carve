"""Jarrahdale: slate blue-grey flattened drum with dusty bloom.

Construction (differs from every other cultivar): drum lathe.
A drum side-profile polyline is revolved; deep ribs modulate each ring.
Dusty bloom lives in the shader: principled sheen masked to rib valleys.
Sturdy tan stem. Whole uncarved fruit.

GUI track: Screw modifier on a drum profile, sheen in the material
properties. Steps in tutorial.md.

Spec: refs/jarrahdale/README.md.
Rebuild: blender -b --factory-startup --python-exit-code 1 -P blender/cultivars/jarrahdale.py [-- --preview]
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
    lobes=13, groove_depth=0.18, groove_pow=0.55,
    segs=182,
    rind="#5F7482", groove_c="#3A4750", bloom="#93A3B0",
    stem_c="#9A7F57",
    bg="#909399", exposure=0.9, lens=70, margin=1.12,
)

# drum profile (r, z): flat bottom, bulging sides, flattened top
PROFILE = [
    (0.000, 0.008), (0.100, 0.005), (0.170, 0.006), (0.225, 0.014),
    (0.265, 0.032), (0.288, 0.060), (0.298, 0.095), (0.296, 0.130),
    (0.284, 0.162), (0.262, 0.188), (0.230, 0.206), (0.190, 0.216),
    (0.145, 0.220), (0.100, 0.219), (0.060, 0.214), (0.030, 0.207),
    (0.000, 0.204),
]


def build_body(name, mat, col):
    n_seg = P["segs"]
    bm = bmesh.new()
    glay = bm.verts.layers.float.new("groove")
    rings = []
    for r0, z0 in PROFILE:
        ring = []
        for i in range(n_seg):
            a = 2 * math.pi * i / n_seg
            g = (0.5 - 0.5 * math.cos(P["lobes"] * a)) ** P["groove_pow"]
            rr = r0 * (1 - P["groove_depth"] * g)
            v = bm.verts.new((rr * math.cos(a), rr * 0.94 * math.sin(a), z0))
            v[glay] = g if r0 > 1e-6 else 0.0
            ring.append(v)
        rings.append(ring)
    for j in range(len(PROFILE) - 1):
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
    mat = H.material("JarrahdaleRind", P["rind"], roughness=0.6)
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
    # dusty bloom: pale sheen strongest in the valleys
    bmix = nt.nodes.new("ShaderNodeMix")
    bmix.data_type = "RGBA"
    bmix.inputs["B"].default_value = H.color(P["bloom"])
    nt.links.new(gmix.outputs["Result"], bmix.inputs["A"])
    nt.links.new(attr.outputs["Fac"], bmix.inputs["Factor"])
    bmix.inputs["Factor"].default_value = 0.0
    drv = nt.nodes.new("ShaderNodeMath")
    drv.operation = "MULTIPLY"
    nt.links.new(attr.outputs["Fac"], drv.inputs[0])
    drv.inputs[1].default_value = 0.30
    # patchy bloom: break the valley mask with coarse noise
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp2 = nt.nodes.new("ShaderNodeMapping")
    mp2.inputs["Scale"].default_value = (3.0, 3.0, 3.0)
    nt.links.new(tc.outputs["Object"], mp2.inputs["Vector"])
    nz2 = nt.nodes.new("ShaderNodeTexNoise")
    nz2.inputs["Scale"].default_value = 3.0
    nz2.inputs["Detail"].default_value = 2.0
    nt.links.new(mp2.outputs["Vector"], nz2.inputs["Vector"])
    mr2 = nt.nodes.new("ShaderNodeMapRange")
    mr2.clamp = True
    mr2.inputs["From Min"].default_value = 0.4
    mr2.inputs["From Max"].default_value = 1.0
    nt.links.new(nz2.outputs["Fac"], mr2.inputs["Value"])
    patch = nt.nodes.new("ShaderNodeMath")
    patch.operation = "MULTIPLY"
    nt.links.new(drv.outputs["Value"], patch.inputs[0])
    nt.links.new(mr2.outputs["Result"], patch.inputs[1])
    nt.links.new(patch.outputs["Value"], bmix.inputs["Factor"])
    nt.links.new(bmix.outputs["Result"], base)
    # roughness breakup: dusty skin is not uniformly smooth
    rough = bsdf.inputs.get("Roughness")
    if rough is not None:
        rr = nt.nodes.new("ShaderNodeMapRange")
        rr.clamp = True
        rr.inputs["From Min"].default_value = 0.0
        rr.inputs["From Max"].default_value = 1.0
        rr.inputs["To Min"].default_value = 0.80
        rr.inputs["To Max"].default_value = 1.00
        nt.links.new(nz2.outputs["Fac"], rr.inputs["Value"])
        nt.links.new(rr.outputs["Result"], rough)
    sheen = bsdf.inputs.get("Sheen weight") or bsdf.inputs.get("Sheen")
    if sheen is not None:
        sheen.default_value = 0.0
    tint = bsdf.inputs.get("Sheen tint")
    if tint is not None:
        tint.default_value = (0.66, 0.71, 0.75, 1.0)
    return mat


def build_stem(name, mat, col):
    # sturdy corky stem: 8 bark ridges, taper, lean
    sides, rings, h = 32, 6, 0.115
    r0, r1 = 0.034, 0.024
    bm = bmesh.new()
    grid = []
    for j in range(rings + 1):
        f = j / rings
        r = r0 + (r1 - r0) * f
        ring = []
        for i in range(sides):
            a = 2 * math.pi * i / sides
            rr = r * (1 + 0.10 * math.sin(8 * a + f * 2.5))
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
    obj.location = (0.004, 0.0, 0.204 - 0.020)
    obj.rotation_euler = (0.0, math.radians(8), 0.0)
    return [obj]


def stem_material():
    mat = H.material("JarrahdaleStemBark", "#8A7350", roughness=0.95)
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
    mix.inputs["A"].default_value = H.color("#6E5A3E")
    mix.inputs["B"].default_value = H.color("#A68D63")
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
    col = H.collection("Jarrahdale")
    body = build_body("Jarrahdale", rind_material(), col)
    parts = build_stem("JarrahdaleStem", stem_material(), col)
    # dusty matte fruit wants soft overcast light: key + fill only,
    # no rim (it etches white crest spots into the matte rind)
    H.studio_lighting(target=[body] + parts, key_azimuth=-40,
                      key_elevation=45, intensity=0.38, contrast=0.55,
                      softness=0.8)
    rim = bpy.data.objects.get("Rim")
    if rim is not None:
        bpy.data.objects.remove(rim, do_unlink=True)
    cam = H.add_camera("Camera", location=(0, -3, 0.3), target=(0, 0, 0.11),
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
    render_view(cam, body, parts, 0.0, os.path.join(VDIR, "jarrahdale.png"))
    render_view(cam, body, parts, 90.0,
                os.path.join(VDIR, "jarrahdale-profile.png"))
    H.save_blend(os.path.join(VDIR, "jarrahdale.blend"))
    H.report()


main()
