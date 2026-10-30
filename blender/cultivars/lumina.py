"""Lumina: smooth white ball with a green stem, built to glow from inside.

Construction (differs from every other cultivar): icosphere shell.
A subdivided icosphere gives perfectly even triangles, scaled to a tall
round fruit with faint ribs. White rind uses subsurface scattering so
interior light bleeds through. Firm green upright stem.

GUI track: Add > Mesh > Ico Sphere, scale, Subsurface in material.
Steps in tutorial.md.

Spec: refs/lumina/README.md.
Rebuild: blender -b --factory-startup --python-exit-code 1 -P blender/cultivars/lumina.py [-- --preview]
"""
import math
import os
import sys

SKILL_SCRIPTS = "/home/bryanchasko/.local/share/muse/skills/bundled/muse-core~v1/skills/blender/scripts"
sys.path.insert(0, SKILL_SCRIPTS)

import bpy  # noqa: E402
import bmesh  # noqa: E402
from bmesh.ops import create_icosphere  # noqa: E402
import bpy_helpers as H  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(ROOT)
VDIR = os.path.join(ROOT, "tutorial", "variants")
PREVIEW = "--preview" in sys.argv

P = dict(
    R=0.22, sx=1.0, sy=0.96, sz=0.95,
    subdiv=4,
    lobes=15, groove_depth=0.06, groove_pow=0.60,
    rind="#F5F5F2", groove_c="#C9CDC9",
    stem_c="#5A6B3A",
    sss_radius=0.35, sss_scale=0.6,
    bg="#909399", exposure=1.0, lens=70, margin=1.12,
)


def build_body(name, mat, col):
    R, N = P["R"], P["lobes"]
    phase = -math.pi / 2 - math.pi / N
    bm = bmesh.new()
    create_icosphere(bm, subdivisions=P["subdiv"], radius=R)
    glay = bm.verts.layers.float.new("groove")
    for v in bm.verts:
        x, y, z = v.co.x, v.co.y, v.co.z
        L = math.sqrt(x * x + y * y) or 1e-9
        a = math.atan2(y / P["sy"], x / P["sx"])
        g = (0.5 - 0.5 * math.cos(N * (a - phase))) ** P["groove_pow"]
        rr = 1 - P["groove_depth"] * g
        x, y = x * rr, y * rr
        z = z * P["sz"] + R * P["sz"]
        if z < 0.02:
            z = 0.02 + (z - 0.02) * 0.4
        v.co.x, v.co.y, v.co.z = x, y, z
        v[glay] = g
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-6)
    obj = bpy.data.objects.new(name, H.mesh_from_bmesh(name, bm))
    H.link(obj, col)
    H.assign(obj, mat)
    H.shade_smooth(obj, angle=35)
    return obj


def rind_material():
    mat = H.material("LuminaRind", P["rind"], roughness=0.5)
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
    sss = bsdf.inputs.get("Subsurface weight")
    if sss is not None:
        sss.default_value = P["sss_scale"]
    rad = bsdf.inputs.get("Subsurface radius")
    if rad is not None:
        rad.default_value = (P["sss_radius"],) * 3
    scol = bsdf.inputs.get("Subsurface color")
    if scol is not None:
        scol.default_value = H.color("#FFF4E0")
    return mat


def build_stem(name, mat, col, topz):
    # firm green upright stem
    stem = H.add_cylinder(name, 0.026, 0.10, radius_top=0.020,
                          vertices=12, mat=mat, collection=col)
    stem.location = (0.0, 0.0, topz + 0.030)
    stem.rotation_euler = (math.radians(3), 0.0, 0.0)
    return [stem]


def render_view(cam, body, parts, azimuth, path):
    H.frame_objects(cam, [body] + parts, azimuth=azimuth, elevation=5.0,
                    margin=P["margin"])
    H.render_still(path, background=P["bg"])


def main():
    H.reset_scene()
    col = H.collection("Lumina")
    body = build_body("Lumina", rind_material(), col)
    stem_mat = H.material("LuminaStem", P["stem_c"], roughness=0.7)
    topz = 2 * P["R"] * P["sz"]
    parts = build_stem("LuminaStem", stem_mat, col, topz)
    H.studio_lighting(target=[body] + parts, key_azimuth=-40,
                      key_elevation=45, intensity=0.7, contrast=0.7,
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
    render_view(cam, body, parts, 0.0, os.path.join(VDIR, "lumina.png"))
    render_view(cam, body, parts, 90.0,
                os.path.join(VDIR, "lumina-profile.png"))
    H.save_blend(os.path.join(VDIR, "lumina.blend"))
    H.report()


main()
