"""Black futsu: squat blocky fruit, wart-crusted ribs, buff cure patches.

Construction (differs from every other cultivar): ribbed polar body PLUS
geometry-nodes wart scatter. A Geometry Nodes tree distributes points on
faces masked to rib crests (groove attribute > 0.55) and instances a wart
prototype on them. Two-tone cure comes from a noise mask in the shader.
Whole uncarved fruit.

GUI track: Properties > Modifiers > Add Modifier > Geometry Nodes;
Distribute Points on Faces + Instance on Points, density driven by a
Named Attribute. Tutorial covers the script path with node screenshots.

Spec: refs/black-futsu/README.md.
Rebuild: blender -b --factory-startup --python-exit-code 1 -P blender/cultivars/black_futsu.py [-- --preview]
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
    R=0.22, sx=1.0, sy=0.95, sz=0.76,
    lobes=11, groove_depth=0.20, groove_pow=0.60,
    segs=132, rings=66,
    base="#1D2419", groove_c="#101A10", cure="#C99A63",
    stem_c="#9A7F57",
    wart_density=1600.0, wart_seed=7,
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
    top = bm.verts.new((0.0, 0.0, 2 * CZ - 0.01))
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
            if z < 0.03:  # sit-flat bottom
                z = 0.03 + (z - 0.03) * 0.35
            topz = 2 * CZ - 0.01
            if z > topz - 0.05:  # flat top around the stem
                z = topz - 0.05 + (z - topz + 0.05) * 0.35
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


def rind_material():
    mat = H.material("FutsuRind", P["base"], roughness=0.75)
    nt = mat.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    base = bsdf.inputs.get("Base Color") or bsdf.inputs[0]
    attr = nt.nodes.new("ShaderNodeAttribute")
    attr.attribute_name = "groove"
    gmix = nt.nodes.new("ShaderNodeMix")
    gmix.data_type = "RGBA"
    gmix.inputs["A"].default_value = H.color(P["base"])
    gmix.inputs["B"].default_value = H.color(P["groove_c"])
    nt.links.new(attr.outputs["Fac"], gmix.inputs["Factor"])
    # buff cure patches on rib tops: noise mask over the groove mix
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 4.0
    nz.inputs["Detail"].default_value = 2.0
    ramp = nt.nodes.new("ShaderNodeMapRange")
    ramp.clamp = True
    ramp.inputs["From Min"].default_value = 0.65
    ramp.inputs["From Max"].default_value = 0.82
    nt.links.new(nz.outputs["Fac"], ramp.inputs["Value"])
    cmix = nt.nodes.new("ShaderNodeMix")
    cmix.data_type = "RGBA"
    cmix.inputs["B"].default_value = H.color(P["cure"])
    nt.links.new(gmix.outputs["Result"], cmix.inputs["A"])
    nt.links.new(ramp.outputs["Result"], cmix.inputs["Factor"])
    nt.links.new(cmix.outputs["Result"], base)
    return mat


def wart_prototype(mat, col):
    bm = bmesh.new()
    create_icosphere(bm, subdivisions=1, radius=1.0)
    obj = bpy.data.objects.new("WartProto", H.mesh_from_bmesh("WartProto", bm))
    H.link(obj, col)
    H.assign(obj, mat)
    obj.hide_viewport = True
    obj.hide_render = True
    H.shade_smooth(obj, angle=60)
    return obj


def scatter_warts(body, proto):
    tree = bpy.data.node_groups.new("FutsuWarts", "GeometryNodeTree")
    tree.interface.new_socket(name="Geometry", in_out="INPUT",
                              socket_type="NodeSocketGeometry")
    tree.interface.new_socket(name="Geometry", in_out="OUTPUT",
                              socket_type="NodeSocketGeometry")
    gin = tree.nodes.new("NodeGroupInput")
    gout = tree.nodes.new("NodeGroupOutput")
    join = tree.nodes.new("GeometryNodeJoinGeometry")
    dist = tree.nodes.new("GeometryNodeDistributePointsOnFaces")
    dist.distribute_method = "RANDOM"
    dist.inputs["Density"].default_value = P["wart_density"]
    dist.inputs["Seed"].default_value = P["wart_seed"]
    named = tree.nodes.new("GeometryNodeInputNamedAttribute")
    named.data_type = "FLOAT"
    named.inputs[0].default_value = "groove"
    cmp = tree.nodes.new("FunctionNodeCompare")
    cmp.data_type = "FLOAT"
    cmp.operation = "GREATER_THAN"
    cmp.inputs["B"].default_value = 0.55
    inst = tree.nodes.new("GeometryNodeInstanceOnPoints")
    info = tree.nodes.new("GeometryNodeObjectInfo")
    info.inputs["Object"].default_value = proto
    rnd = tree.nodes.new("FunctionNodeRandomValue")
    rnd.data_type = "FLOAT_VECTOR"
    rnd.inputs["Min"].default_value = (0.005, 0.005, 0.004)
    rnd.inputs["Max"].default_value = (0.011, 0.011, 0.009)
    tree.links.new(gin.outputs["Geometry"], dist.inputs["Mesh"])
    tree.links.new(gin.outputs["Geometry"], join.inputs["Geometry"])
    tree.links.new(named.outputs["Attribute"], cmp.inputs["A"])
    tree.links.new(cmp.outputs["Result"], dist.inputs["Selection"])
    tree.links.new(dist.outputs["Points"], inst.inputs["Points"])
    tree.links.new(info.outputs["Geometry"], inst.inputs["Instance"])
    tree.links.new(rnd.outputs["Value"], inst.inputs["Scale"])
    tree.links.new(inst.outputs["Instances"], join.inputs["Geometry"])
    tree.links.new(join.outputs["Geometry"], gout.inputs["Geometry"])
    mod = body.modifiers.new("Warts", "NODES")
    mod.node_group = tree
    return mod


def build_stem(name, mat, col):
    # hard angular tan stem: hexagonal prism reads faceted, slight lean
    stem = H.add_cylinder(name, 0.026, 0.125, radius_top=0.016,
                          vertices=6, mat=mat, collection=col)
    stem.location = (0.012, 0.0, 2 * P["R"] * P["sz"] + 0.045)
    stem.rotation_euler = (0.0, math.radians(18), math.radians(15))
    return [stem]


def render_view(cam, body, parts, azimuth, path):
    H.frame_objects(cam, [body] + parts, azimuth=azimuth, elevation=5.0,
                    margin=P["margin"])
    H.render_still(path, background=P["bg"])


def main():
    H.reset_scene()
    col = H.collection("Futsu")
    rind = rind_material()
    wart_mat = H.material("FutsuWart", "#232B1E", roughness=0.85)
    stem_mat = H.material("FutsuStem", P["stem_c"], roughness=0.9)
    body = build_body("BlackFutsu", rind, col)
    proto = wart_prototype(wart_mat, col)
    scatter_warts(body, proto)
    parts = build_stem("FutsuStem", stem_mat, col)
    H.studio_lighting(target=[body] + parts, key_azimuth=-40,
                      key_elevation=45, intensity=0.7, contrast=0.75,
                      softness=0.5)
    cam = H.add_camera("Camera", location=(0, -3, 0.3), target=(0, 0, 0.19),
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
    render_view(cam, body, parts, 0.0, os.path.join(VDIR, "black-futsu.png"))
    render_view(cam, body, parts, 90.0,
                os.path.join(VDIR, "black-futsu-profile.png"))
    H.save_blend(os.path.join(VDIR, "black-futsu.blend"))
    H.report()


main()
