"""Long island cheese: flat buff wheel with a stem sunk in a well.

Construction (differs from every other cultivar): boolean socket.
A flattened ribbed wheel is built from a polar grid, then a cylinder
cutter booleans a recessed well into the crown and the short stem is
planted inside it. Buff-tan smooth skin. Whole uncarved fruit.

GUI track: Add > Mesh > Cylinder cutter, Boolean modifier (Difference),
stem placed in the socket. Steps in tutorial.md.

Spec: refs/long-island-cheese/README.md.
Rebuild: blender -b --factory-startup --python-exit-code 1 -P blender/cultivars/long_island_cheese.py [-- --preview]
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
    R=0.26, sx=1.0, sy=0.95, sz=0.50,
    lobes=17, groove_depth=0.08, groove_pow=0.60,
    segs=170, rings=80,
    rind="#C08A3E", groove_c="#8A6430",
    stem_c="#7A7A45",
    well_r=0.060, well_depth=0.055,
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


def cut_well(body, col, topz):
    # recessed socket for the sunken stem: boolean cylinder, capped by hand
    cut = H.add_cylinder("WellCutter", P["well_r"], P["well_depth"] + 0.02,
                         vertices=24, collection=col)
    cut.location = (0.0, 0.0, topz - P["well_depth"] / 2 + 0.005)
    H.boolean(body, cut)
    H.apply_modifiers(body)
    # cap the well floor with a slightly domed disc at the socket bottom
    bm = bmesh.new()
    n = 24
    center = bm.verts.new((0.0, 0.0, topz - P["well_depth"]))
    ring = []
    for i in range(n):
        a = 2 * math.pi * i / n
        ring.append(bm.verts.new((P["well_r"] * math.cos(a),
                                  P["well_r"] * 0.95 * math.sin(a),
                                  topz - P["well_depth"] + 0.004)))
    for i in range(n):
        bm.faces.new((center, ring[i], ring[(i + 1) % n]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    cap = bpy.data.objects.new("WellFloor", H.mesh_from_bmesh("WellFloor", bm))
    H.link(cap, col)
    H.assign(cap, body.data.materials[0])
    H.shade_smooth(cap, angle=60)
    return cap


def build_stem(name, mat, col, topz):
    # short woody stem: 7 bark ridges rising out of the well
    sides, rings, h = 28, 4, 0.11
    r0, r1 = 0.022, 0.015
    bm = bmesh.new()
    grid = []
    for j in range(rings + 1):
        f = j / rings
        r = r0 + (r1 - r0) * f
        ring = []
        for i in range(sides):
            a = 2 * math.pi * i / sides
            rr = r * (1 + 0.12 * math.sin(7 * a + f * 2.0))
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
    obj.location = (0.0, 0.0, topz - 0.015)
    return [obj]


def rind_material():
    mat = H.material("CheeseRind", P["rind"], roughness=0.45)
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
    H.add_noise_variation(mat, scale=9, amount=0.07, roughness_amount=0.05)
    return mat


def render_view(cam, objs, azimuth, path):
    H.frame_objects(cam, objs, azimuth=azimuth, elevation=5.0,
                    margin=P["margin"])
    H.render_still(path, background=P["bg"])


def main():
    H.reset_scene()
    col = H.collection("Cheese")
    body = build_body("LongIslandCheese", rind_material(), col)
    topz = 2 * P["R"] * P["sz"]
    cap = cut_well(body, col, topz)
    stem_mat = H.material("CheeseStem", P["stem_c"], roughness=0.8)
    parts = build_stem("CheeseStem", stem_mat, col, topz) + [cap]
    # groove attribute must survive the boolean: rebuild from positions
    me = body.data
    attr = me.attributes.get("groove")
    if attr is None:
        attr = me.attributes.new("groove", "FLOAT", "POINT")
    N = P["lobes"]
    phase = -math.pi / 2 - math.pi / N
    for v in me.vertices:
        a = math.atan2(v.co.y / P["sy"], v.co.x / P["sx"])
        attr.data[v.index].value = (0.5 - 0.5 * math.cos(N * (a - phase))) ** P["groove_pow"]
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
    render_view(cam, [body] + parts, 0.0,
                os.path.join(VDIR, "long-island-cheese.png"))
    render_view(cam, [body] + parts, 90.0,
                os.path.join(VDIR, "long-island-cheese-profile.png"))
    H.save_blend(os.path.join(VDIR, "long-island-cheese.blend"))
    H.report()


main()
