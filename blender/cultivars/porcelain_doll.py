"""Porcelain doll: pink blocky fruit with square shoulders.

Construction (differs from every other cultivar): cube to pumpkin.
A subdivided cube is spherified toward a sphere but stopped early, so
flat sides and square shoulders survive; then ribs are displaced and a
bevel modifier softens edges, with weighted normals. Glossy pink shader.

GUI track: Add > Mesh > Cube, Subdivision Surface, To Sphere (partial),
Bevel modifier. Steps in tutorial.md.

Spec: refs/porcelain-doll/README.md.
Rebuild: blender -b --factory-startup --python-exit-code 1 -P blender/cultivars/porcelain_doll.py [-- --preview]
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
    R=0.24, sx=1.0, sy=0.94, sz=0.85,
    spherify=1.0, subdiv=3, square=0.05,
    lobes=13, groove_depth=0.18, groove_pow=0.60,
    rind="#E8907C", rind_groove="#B07078",
    stem_c="#A08B62",
    bg="#909399", exposure=1.0, lens=70, margin=1.12,
)


def build_body(name, mat, col):
    R, N = P["R"], P["lobes"]
    phase = -math.pi / 2 - math.pi / N
    h = R
    n = 20
    bm = bmesh.new()
    faces = [
        ((-h, -h, h), (2 * h, 0, 0), (0, 2 * h, 0)),      # top
        ((-h, h, -h), (2 * h, 0, 0), (0, -2 * h, 0)),     # bottom
        ((-h, h, -h), (0, 0, 2 * h), (2 * h, 0, 0)),      # +y
        ((h, -h, -h), (0, 0, 2 * h), (-2 * h, 0, 0)),     # -y
        ((h, -h, -h), (0, 2 * h, 0), (0, 0, 2 * h)),      # +x
        ((-h, -h, -h), (0, 0, 2 * h), (0, 2 * h, 0)),     # -x
    ]
    for o, u, w in faces:
        grid = [[None] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            for j in range(n + 1):
                grid[i][j] = bm.verts.new((
                    o[0] + u[0] * i / n + w[0] * j / n,
                    o[1] + u[1] * i / n + w[1] * j / n,
                    o[2] + u[2] * i / n + w[2] * j / n))
        for i in range(n):
            for j in range(n):
                try:
                    bm.faces.new((grid[i][j], grid[i + 1][j],
                                  grid[i + 1][j + 1], grid[i][j + 1]))
                except ValueError:
                    pass
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-6)
    # spherify fully, then re-add a hint of square shoulders in the rib loop
    for v in bm.verts:
        x, y, z = v.co.x, v.co.y, v.co.z
        L = math.sqrt(x * x + y * y + z * z) or 1e-9
        t = R / L
        s = P["spherify"]
        x, y, z = x + (x * t - x) * s, y + (y * t - y) * s, z + (z * t - z) * s
        v.co.x, v.co.y, v.co.z = x, y, z
    # ribs + faint square shoulders + squash to pumpkin proportions
    glay = bm.verts.layers.float.new("groove")
    for v in bm.verts:
        x, y, z = v.co.x, v.co.y, v.co.z
        a = math.atan2(y, x)
        g = (0.5 - 0.5 * math.cos(N * (a - phase))) ** P["groove_pow"]
        rr = (1 - P["groove_depth"] * g) * (1 + P["square"] * math.cos(4 * a))
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
    wn = obj.modifiers.new("WeightedNormal", "WEIGHTED_NORMAL")
    H.shade_smooth(obj, angle=50)
    return obj


def rind_material():
    mat = H.material("PorcelainRind", P["rind"], roughness=0.25, coat=0.8,
                     coat_roughness=0.2)
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


def build_stem(name, mat, col, topz):
    stem = H.add_cylinder(name, 0.030, 0.085, radius_top=0.022,
                          vertices=14, mat=mat, collection=col)
    stem.location = (0.005, 0.0, topz - 0.030)
    stem.rotation_euler = (0.0, math.radians(6), 0.0)
    return [stem]


def render_view(cam, body, parts, azimuth, path):
    H.frame_objects(cam, [body] + parts, azimuth=azimuth, elevation=5.0,
                    margin=P["margin"])
    H.render_still(path, background=P["bg"])


def main():
    H.reset_scene()
    col = H.collection("PorcelainDoll")
    body = build_body("PorcelainDoll", rind_material(), col)
    stem_mat = H.material("PorcelainStem", P["stem_c"], roughness=0.85)
    topz = 2 * P["R"] * P["sz"]
    parts = build_stem("PorcelainStem", stem_mat, col, topz)
    H.studio_lighting(target=[body] + parts, key_azimuth=-40,
                      key_elevation=45, intensity=0.7, contrast=0.75,
                      softness=0.5)
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
    render_view(cam, body, parts, 0.0, os.path.join(VDIR, "porcelain-doll.png"))
    render_view(cam, body, parts, 90.0,
                os.path.join(VDIR, "porcelain-doll-profile.png"))
    H.save_blend(os.path.join(VDIR, "porcelain-doll.blend"))
    H.report()


main()
