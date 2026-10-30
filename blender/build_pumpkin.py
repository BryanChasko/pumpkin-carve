"""Stylized carved jack-o-lantern: ribbed body, glowing carved face, bent stem.

Look: toon-shaded rind (Toon BSDF + groove shading layers + warm rim), real
boolean-cut glowing eyes/grin with an emissive core, grease-pencil Line Art
outlines, dark background. CPU Cycles. Tutorial: tutorial/tutorial.md.

Rebuild: blender -b --factory-startup --python-exit-code 1 -P blender/build_pumpkin.py [-- --preview]
"""
import math
import os
import sys

SKILL_SCRIPTS = "/home/bryanchasko/.local/share/muse/skills/bundled/muse-core~v1/skills/blender/scripts"
sys.path.insert(0, SKILL_SCRIPTS)

import bpy  # noqa: E402
import bmesh  # noqa: E402
from mathutils import Vector  # noqa: E402
import bpy_helpers as H  # noqa: E402

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
OUT = os.path.join(ROOT, "blender", "exports")
BLEND = os.path.join(SCRIPT_DIR, "scene.blend")
PREVIEW = "--preview" in sys.argv
TOON = "--toon" in sys.argv
TURNTABLE = "--turntable" in sys.argv
TURNTABLE_FRAMES = 24
STAGE = 99
for _a in sys.argv:
    if _a.startswith("--stage="):
        STAGE = int(_a.split("=", 1)[1])
STAGE_NAMES = {1: "01-body", 2: "02-stem", 3: "03-carved-face", 4: "04-inked-final"}
VARIANT = "generic"
for _a in sys.argv:
    if _a.startswith("--variant="):
        VARIANT = _a.split("=", 1)[1]
FACE_SCALE = 1.0  # outline scale factor for narrow/flat variant bodies
FACE_DZ = 0.0     # vertical shift of face outlines, metres
# Variant overrides: keys replace P entries. spec: blender/variants.md.
# carved=False skips cuts, glow and ink (display whole, line art only).
VARIANTS = {
    "cinderella": dict(lobes=12, groove_depth=0.16, groove_pow=0.50,
                       sx=1.0, sy=0.94, sz=0.55, R=0.34,
                       rind_lit="#D8481C", rind_groove="#7A2408",
                       glow_top="#FFB050", glow_bottom="#E07A10",
                       face_scale=0.80, face_dz=-0.02, stem_scale=0.85),
    "black-futsu": dict(lobes=10, groove_depth=0.20, sx=1.0, sy=0.92,
                        sz=0.65, R=0.22, rind_lit="#2A3A26",
                        rind_groove="#101A10", carved=False,
                        stem_scale=0.65, wart_bump=0.50),
    "sugar-pie": dict(lobes=10, groove_depth=0.07, sx=1.0, sy=0.94,
                      sz=0.85, R=0.18, rind_lit="#F58A1E",
                      rind_groove="#A85A10", face_scale=0.80,
                      stem_scale=0.65),
    "baby-boo": dict(lobes=12, groove_depth=0.09, sx=1.0, sy=0.94,
                     sz=0.70, R=0.05, rind_lit="#E8E4DA",
                     rind_groove="#B8B0A0", carved=False,
                     stem_scale=0.22, groove_lines=False),
    "porcelain-doll": dict(lobes=12, groove_depth=0.13, sx=1.02,
                           sy=0.94, sz=0.62, R=0.32,
                           rind_lit="#E8A0A8", rind_groove="#B07078",
                           face_scale=0.90, stem_scale=0.88),
    "jarrahdale": dict(lobes=12, groove_depth=0.15, sx=1.0, sy=0.94,
                       sz=0.58, R=0.33, rind_lit="#7A8A94",
                       rind_groove="#4A5A64", face_scale=0.80,
                       face_dz=-0.02, stem_scale=0.85),
    "lumina": dict(lobes=11, groove_depth=0.08, sx=1.0, sy=0.94,
                   sz=0.78, R=0.30, rind_lit="#DFE6EA",
                   rind_groove="#AEBAC0", face_scale=0.95),
    "long-island-cheese": dict(lobes=14, groove_depth=0.10, sx=1.0,
                               sy=0.94, sz=0.48, R=0.34,
                               rind_lit="#C8A878", rind_groove="#8A6F4A",
                               carved=False, stem_scale=0.72),
    "harvest-moon": dict(lobes=13, groove_depth=0.12, sx=1.0, sy=0.94,
                         sz=0.72, R=0.30, rind_lit="#E06A10",
                         rind_groove="#5E2806", face_scale=0.95,
                         stem_scale=0.95),
    "kabocha": dict(lobes=10, groove_depth=0.14, sx=1.0, sy=0.94,
                    sz=0.68, R=0.20, rind_lit="#2E4A2A",
                    rind_groove="#1A2E1A", carved=False,
                    stem_scale=0.60, kabocha_speckle=True),
}
P = dict(
    # body (metres, true scale for a large carving pumpkin)
    R=0.30, sx=1.0, sy=0.92, sz=0.75,
    lobes=15, groove_depth=0.115, groove_pow=0.6,
    segs=208, rings=104,
    crater_depth=0.045, crater_w=0.085,
    # camera / framing
    lens=70, azimuth=0.0, elevation=3.0, margin=0.92,
    # look
    bg="#0a0d13", exposure=0.92,
    rind_lit="#F07818", rind_groove="#6E2F0C",
    glow_top="#FFBE45", glow_bottom="#FF8F16", glow_strength=0.75,
    flesh_color="#F0B45C", flesh_strength=0.55, shell=0.012,
    rim_color="#FFE6B0", rim_strength=1.7,
    inner_light_energy=0.5,
    line_color=(0.012, 0.005, 0.0025, 1.0), line_thickness=3,
    crease_threshold=0.70, frame_pull=0.77,
    groove_line_r=0.0012, groove_line_lift=0.0004,
    toon_size=0.62, fill_level=0.75,
    # cut bevel funnels: the outer ring sits exactly on the hole outline and
    # is recessed just inside the rind (no wall may poke outside the cuts);
    # inner opening scale per shape; funnel depth; the inner cap carries the
    # yellow glow gradient
    wall_recess=0.004, wall_depth=0.045, inner_eye=0.80, inner_grin=0.84,
    # light rig
    intensity=0.90, key_az=45.0, key_el=38.0,
)
if VARIANT in VARIANTS:
    P.update(VARIANTS[VARIANT])
CARVED = P.get("carved", True)
FACE_SCALE = P.pop("face_scale", 1.0)
FACE_DZ = P.pop("face_dz", 0.0)

# face cut-out outlines in pumpkin-local metres: (x right, z up), front faces -Y.
# Pixel-measured from hero.jpg crops (frame fractions mapped through the
# body box): both eyes are large tall triangles of similar screen size; the
# right eye leans right and wraps the side rib. Grin: shallow 3-V upper
# edge, 3 upward lower teeth, thin upswept pointed corner tips.
# Variants rescale them: _face() applies FACE_SCALE around the outline
# centre, then FACE_DZ, so narrow/flat bodies keep the face on the rind.
def _face(poly):
    cx = sum(p[0] for p in poly) / len(poly)
    cz = sum(p[1] for p in poly) / len(poly)
    return [(cx + (x - cx) * FACE_SCALE, cz + (z - cz) * FACE_SCALE + FACE_DZ)
            for x, z in poly]
_EYE_L = [(-0.055, 0.342), (0.022, 0.258), (-0.104, 0.258)]
_EYE_R = [(0.185, 0.340), (0.205, 0.282), (0.078, 0.270)]
EYE_L = _face(_EYE_L)
EYE_R = _face(_EYE_R)
# Both polylines are strictly x-monotone with upper above lower at every
# station (min margin 0.010 at the interlocking teeth), so the closed
# polygon cannot self-intersect.
GRIN_UPPER = [(-0.165, 0.189), (-0.100, 0.130), (-0.039, 0.158),
              (0.031, 0.132), (0.096, 0.160), (0.169, 0.134),
              (0.258, 0.201)]
GRIN_LOWER = [(0.244, 0.168), (0.229, 0.104), (0.165, 0.125),
              (0.096, 0.090), (0.040, 0.125), (-0.021, 0.090),
              (-0.077, 0.125), (-0.133, 0.090), (-0.156, 0.162)]
GRIN = _face(GRIN_UPPER + GRIN_LOWER)


def build_body(name, mat, col, r_scale=1.0):
    """Ribbed oblate pumpkin via polar grid; per-vertex 'groove' 0..1 weight."""
    R, N = P["R"] * r_scale, P["lobes"]
    segs, rings = P["segs"], P["rings"]
    phase = -math.pi / 2 - math.pi / N  # a groove centred on the front (-Y)
    CZ = R * P["sz"]
    # crater and sit-flat scale with the body so minis keep their proportions
    CR = R / 0.30
    crater_depth, crater_w = P["crater_depth"] * CR, P["crater_w"] * CR
    sit = 0.02 * CR
    bm = bmesh.new()
    glay = bm.verts.layers.float.new("groove")
    bot = bm.verts.new((0.0, 0.0, 0.0))
    bot[glay] = 0.0
    top = bm.verts.new((0.0, 0.0, 2 * CZ - crater_depth))
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
            if zc > 0:  # shoulder dip around the stem
                rh = math.hypot(x, y)
                z -= crater_depth * math.exp(-((rh / crater_w) ** 2))
            if z < sit:  # slight bottom flatten so it sits
                z = sit + (z - sit) * 0.45
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
            bm.faces.new((grid[j][i], grid[j + 1][i], grid[j + 1][k], grid[j][k]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    obj = bpy.data.objects.new(name, H.mesh_from_bmesh(name, bm))
    H.link(obj, col)
    H.assign(obj, mat)
    H.shade_smooth(obj, angle=35)
    return obj


def surface_point(a, phi, phase):
    """Pumpkin surface position for azimuth a / polar phi (same math as build_body)."""
    R = P["R"]
    CZ = R * P["sz"]
    CR = R / 0.30
    crater_depth, crater_w = P["crater_depth"] * CR, P["crater_w"] * CR
    sit = 0.02 * CR
    sh, zc = math.sin(phi), -math.cos(phi)
    g = (0.5 - 0.5 * math.cos(P["lobes"] * (a - phase))) ** P["groove_pow"]
    rr = R * (1 - P["groove_depth"] * g) * sh
    x = rr * P["sx"] * math.cos(a)
    y = rr * P["sy"] * math.sin(a)
    z = zc * R * P["sz"] + CZ
    if zc > 0:
        rh = math.hypot(x, y)
        z -= crater_depth * math.exp(-((rh / crater_w) ** 2))
    if z < sit:
        z = sit + (z - sit) * 0.45
    return (x, y, z)


def point_in_poly(x, z, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        x1, z1 = poly[i]
        x2, z2 = poly[(i + 1) % n]
        if (z1 > z) != (z2 > z) and x < (x2 - x1) * (z - z1) / (z2 - z1 + 1e-12) + x1:
            inside = not inside
    return inside


def surface_y(x, z):
    """Front-surface Y for pumpkin-local (x, z), including groove modulation.

    Inverts the build_body parametric form with relaxed fixed-point iteration
    (the groove term makes x(a) non-monotonic, so plain iteration ping-pongs).
    """
    R, N = P["R"], P["lobes"]
    phase = -math.pi / 2 - math.pi / N
    CZ = R * P["sz"]
    zc = max(-0.95, min(0.95, (z - CZ) / (R * P["sz"])))
    sh = math.sqrt(max(0.05, 1 - zc * zc))
    a, reff = -math.pi / 2, R
    for _ in range(10):
        denom = sh * reff * P["sx"]
        c = max(-1.0, min(1.0, x / denom))
        a_new = -math.acos(c)  # front half
        a = 0.5 * (a + a_new)
        g = (0.5 - 0.5 * math.cos(N * (a - phase))) ** P["groove_pow"]
        reff = R * (1 - P["groove_depth"] * g)
    return sh * reff * P["sy"] * math.sin(a)


def _flip_toward(bm, want):
    """Flip all faces when their average normal points away from `want`."""
    n = Vector((0, 0, 0))
    for f in bm.faces:
        n += f.normal * f.calc_area()
    if n.dot(Vector(want)) < 0:
        for f in bm.faces:
            f.normal_flip()


def build_cut_bevels(col, glow_col, wall_mat, cap_mats):
    """Pale flesh bevel-wall funnels + amber glow caps inside every carved hole.

    The outer ring sits exactly on the boolean hole outline and is recessed
    just inside the rind surface, so no wall pokes out past the cuts.
    The walls slope inward to a smaller opening
    capped by the per-opening emissive gradient; the wide pale ring plus
    the deep funnel reads as a true carved opening with real depth.
    """
    out = []
    for name, outline in (("EyeL", EYE_L), ("EyeR", EYE_R), ("Grin", GRIN)):
        cx = sum(p[0] for p in outline) / len(outline)
        cz = sum(p[1] for p in outline) / len(outline)
        si = P["inner_grin"] if name == "Grin" else P["inner_eye"]
        inner = [(cx + (x - cx) * si, cz + (z - cz) * si) for x, z in outline]
        # walls
        bm = bmesh.new()
        ov = [bm.verts.new((x, surface_y(x, z) + P["wall_recess"], z))
              for x, z in outline]
        iv = [bm.verts.new((x, surface_y(x, z) + P["wall_depth"], z))
              for x, z in inner]
        n = len(outline)
        for i in range(n):
            j = (i + 1) % n
            bm.faces.new((ov[i], ov[j], iv[j], iv[i]))
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        _flip_toward(bm, (0, -1, 0.35))
        walls = bpy.data.objects.new(name + "Walls",
                                     H.mesh_from_bmesh(name + "Walls", bm))
        H.link(walls, col)
        H.assign(walls, wall_mat)
        out.append(walls)
        # glow cap across the inner opening
        bc = bmesh.new()
        cv = [bc.verts.new((x, surface_y(x, z) + P["wall_depth"], z))
              for x, z in inner]
        bc.faces.new(list(cv))
        bmesh.ops.recalc_face_normals(bc, faces=bc.faces)
        _flip_toward(bc, (0, -1, 0))
        cap = bpy.data.objects.new(name + "Glow",
                                   H.mesh_from_bmesh(name + "Glow", bc))
        # caps live outside the LineArt source: their rims coincide exactly
        # with the wall inner rings, which already draw the inner bevel line
        H.link(cap, glow_col)
        H.assign(cap, cap_mats[name])
        out.append(cap)
    return out


def _dist_to_poly(x, z, poly):
    """Shortest distance from (x, z) to a polygon outline."""
    d2 = float("inf")
    n = len(poly)
    for i in range(n):
        x1, z1 = poly[i]
        x2, z2 = poly[(i + 1) % n]
        dx, dz = x2 - x1, z2 - z1
        t = max(0.0, min(1.0, ((x - x1) * dx + (z - z1) * dz)
                         / (dx * dx + dz * dz or 1e-12)))
        px, pz = x1 + dx * t, z1 + dz * t
        dd = (x - px) ** 2 + (z - pz) ** 2
        if dd < d2:
            d2 = dd
    return math.sqrt(d2)


def build_groove_lines(line_mat):
    """Dark tubes hugging every valley, pole to pole, split around the face holes.
    The split zone has a margin past the hole rims: the bevel funnels are
    recessed behind the surface, so a tube hugging a rim would still cross
    the pale bevel in screen space (it rendered as stray dark dashes inside
    the glow). Kept out of the LineArt source collection so they draw no
    outlines of their own."""
    N = P["lobes"]
    phase = -math.pi / 2 - math.pi / N
    holes = (EYE_L, EYE_R, GRIN)
    MARGIN = 0.009
    serene = []
    for k in range(N):
        a = phase + (2 * k + 1) * math.pi / N
        run = []

        def flush(run):
            if len(run) >= 3:
                # POLY (no smoothing): bezier overshoot past run ends would
                # poke dark tube tips into the carved holes
                H.add_tube(f"GrooveLine{k}_{len(serene)}", list(run),
                           radius=P["groove_line_r"], mat=line_mat,
                           collection=None, smooth_path=False)
                serene.append(True)
            run.clear()

        steps = 44
        for s in range(steps + 1):
            phi = math.pi * (0.5 + s) / (steps + 1)
            x, y, z = surface_point(a, phi, phase)
            if y < -0.05 and any(point_in_poly(x, z, h)
                                   or _dist_to_poly(x, z, h) < MARGIN
                                   for h in holes):
                flush(run)  # gap across carved holes (front only)
                continue
            rh = math.hypot(x, y) or 1e-9
            lift = P["groove_line_lift"]
            run.append((x + x / rh * lift, y + y / rh * lift, z))
        flush(run)
    return len(serene)


def rind_material():
    name = "RindToon"
    old = bpy.data.materials.get(name)
    if old is not None:
        bpy.data.materials.remove(old)
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    attr = nt.nodes.new("ShaderNodeAttribute")
    attr.attribute_name = "groove"
    pw = nt.nodes.new("ShaderNodeMath")
    pw.operation = "POWER"
    pw.inputs[1].default_value = 2.8
    nt.links.new(attr.outputs["Fac"], pw.inputs[0])
    # painterly vertical brush streaks modulate the lit colour before grooving
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (5.0, 5.0, 1.0)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 14.0
    nz.inputs["Detail"].default_value = 3.0
    nt.links.new(mp.outputs["Vector"], nz.inputs["Vector"])
    nr = nt.nodes.new("ShaderNodeMapRange")
    nr.clamp = True
    nr.inputs["From Min"].default_value = 0.35
    nr.inputs["From Max"].default_value = 0.65
    nt.links.new(nz.outputs["Fac"], nr.inputs["Value"])
    # fine vertical rib streaks: rapid around the circumference, slow along
    # Z, so the rind reads painterly with fibre strokes instead of flat toy
    # plastic; also drives a whisper of bump relief on the toon shading
    mp2 = nt.nodes.new("ShaderNodeMapping")
    mp2.inputs["Scale"].default_value = (5.0, 5.0, 0.5)
    nt.links.new(tc.outputs["Object"], mp2.inputs["Vector"])
    nz2 = nt.nodes.new("ShaderNodeTexNoise")
    nz2.inputs["Scale"].default_value = 28.0
    nz2.inputs["Detail"].default_value = 2.0
    nt.links.new(mp2.outputs["Vector"], nz2.inputs["Vector"])
    nr2 = nt.nodes.new("ShaderNodeMapRange")
    nr2.clamp = True
    nr2.inputs["From Min"].default_value = 0.35
    nr2.inputs["From Max"].default_value = 0.65
    nt.links.new(nz2.outputs["Fac"], nr2.inputs["Value"])
    lit = H.color(P["rind_lit"])
    dk = nt.nodes.new("ShaderNodeMix")
    dk.data_type = "RGBA"
    dk.blend_type = "MULTIPLY"
    dk.inputs["Factor"].default_value = 1.0
    dk.inputs["A"].default_value = lit
    dk.inputs["B"].default_value = (0.88, 0.88, 0.88, 1.0)
    lt = nt.nodes.new("ShaderNodeMix")
    lt.data_type = "RGBA"
    lt.blend_type = "MULTIPLY"
    lt.inputs["Factor"].default_value = 1.0
    lt.inputs["A"].default_value = lit
    lt.inputs["B"].default_value = (1.08, 1.08, 1.08, 1.0)
    streak = nt.nodes.new("ShaderNodeMix")
    streak.data_type = "RGBA"
    nt.links.new(dk.outputs["Result"], streak.inputs["A"])
    nt.links.new(lt.outputs["Result"], streak.inputs["B"])
    # broad mottling and fine streaks share the lit-colour variation band
    s_add = nt.nodes.new("ShaderNodeMath")
    s_add.operation = "ADD"
    nt.links.new(nr.outputs["Result"], s_add.inputs[0])
    nt.links.new(nr2.outputs["Result"], s_add.inputs[1])
    s_half = nt.nodes.new("ShaderNodeMath")
    s_half.operation = "MULTIPLY"
    nt.links.new(s_add.outputs["Value"], s_half.inputs[0])
    s_half.inputs[1].default_value = 0.5
    nt.links.new(s_half.outputs["Value"], streak.inputs["Factor"])
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.06
    nt.links.new(nz2.outputs["Fac"], bump.inputs["Height"])
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    # painterly lit colour: mottled + streaked variation feeds the groove mix
    nt.links.new(streak.outputs["Result"], mix.inputs["A"])
    mix.inputs["B"].default_value = H.color(P["rind_groove"])
    mix.inputs["Factor"].default_value = 0.85
    nt.links.new(pw.outputs["Value"], mix.inputs["Factor"])
    # crisp painted rib-crest lift: lighten lobe crowns toward hot orange so
    # each rib reads as a separate painted band, not an airbrushed gradient
    cone = nt.nodes.new("ShaderNodeMath")
    cone.operation = "SUBTRACT"
    cone.inputs[0].default_value = 1.0
    nt.links.new(attr.outputs["Fac"], cone.inputs[1])
    cpow = nt.nodes.new("ShaderNodeMath")
    cpow.operation = "POWER"
    cpow.inputs[1].default_value = 2.5
    nt.links.new(cone.outputs["Value"], cpow.inputs[0])
    cscale = nt.nodes.new("ShaderNodeMath")
    cscale.operation = "MULTIPLY"
    cscale.inputs[1].default_value = 0.45
    nt.links.new(cpow.outputs["Value"], cscale.inputs[0])
    crown = nt.nodes.new("ShaderNodeMix")
    crown.data_type = "RGBA"
    crown.inputs["B"].default_value = H.color("#FF9A30")
    nt.links.new(mix.outputs["Result"], crown.inputs["A"])
    nt.links.new(cscale.outputs["Value"], crown.inputs["Factor"])
    diff = nt.nodes.new("ShaderNodeBsdfToon")
    diff.component = "DIFFUSE"
    diff.inputs["Size"].default_value = P["toon_size"]
    diff.inputs["Smooth"].default_value = 0.06
    nt.links.new(crown.outputs["Result"], diff.inputs["Color"])
    if P.get("kabocha_speckle", False):  # kabocha: sparse light speckles
        sp = nt.nodes.new("ShaderNodeTexNoise")
        sp.inputs["Scale"].default_value = 60.0
        sp.inputs["Detail"].default_value = 1.0
        nt.links.new(mp.outputs["Vector"], sp.inputs["Vector"])
        thr = nt.nodes.new("ShaderNodeMapRange")
        thr.clamp = True
        thr.inputs["From Min"].default_value = 0.72
        thr.inputs["From Max"].default_value = 0.78
        nt.links.new(sp.outputs["Fac"], thr.inputs["Value"])
        spmix = nt.nodes.new("ShaderNodeMix")
        spmix.data_type = "RGBA"
        spmix.inputs["B"].default_value = H.color("#C8B060")
        nt.links.new(crown.outputs["Result"], spmix.inputs["A"])
        nt.links.new(thr.outputs["Result"], spmix.inputs["Factor"])
        nt.links.new(spmix.outputs["Result"], diff.inputs["Color"])
    gloss = nt.nodes.new("ShaderNodeBsdfToon")
    gloss.component = "GLOSSY"
    gloss.inputs["Color"].default_value = H.color("#E06A10")
    gloss.inputs["Size"].default_value = 0.15
    gloss.inputs["Smooth"].default_value = 0.2
    nt.links.new(bump.outputs["Normal"], diff.inputs["Normal"])
    nt.links.new(bump.outputs["Normal"], gloss.inputs["Normal"])
    if P.get("wart_bump", 0):  # black futsu: voronoi warts over the rind
        vno = nt.nodes.new("ShaderNodeTexVoronoi")
        vno.feature = "F1"
        vno.inputs["Scale"].default_value = 18.0
        nt.links.new(mp.outputs["Vector"], vno.inputs["Vector"])
        wb = nt.nodes.new("ShaderNodeBump")
        wb.inputs["Strength"].default_value = P["wart_bump"]
        nt.links.new(vno.outputs["Distance"], wb.inputs["Height"])
        nt.links.new(bump.outputs["Normal"], wb.inputs["Normal"])
        nt.links.new(wb.outputs["Normal"], diff.inputs["Normal"])
        nt.links.new(wb.outputs["Normal"], gloss.inputs["Normal"])
    sheen = nt.nodes.new("ShaderNodeMixShader")
    sheen.inputs["Fac"].default_value = 0.10
    nt.links.new(diff.outputs["BSDF"], sheen.inputs[1])
    nt.links.new(gloss.outputs["BSDF"], sheen.inputs[2])
    # warm rim on the outer right silhouette only: steep ramp over X in
    # [0.90, 1.0] times a grazing-view term, built from commutative math ops
    # only (plain math nodes clamp predictably at the edges).
    # A wider gate paints a hard white streak down a
    # mid-surface lobe flank; the facing term keeps only the true limb.
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(geo.outputs["Normal"], sep.inputs["Vector"])
    shift = nt.nodes.new("ShaderNodeMath")
    shift.operation = "ADD"
    nt.links.new(sep.outputs["X"], shift.inputs[0])
    shift.inputs[1].default_value = -0.90
    scale = nt.nodes.new("ShaderNodeMath")
    scale.operation = "MULTIPLY"
    nt.links.new(shift.outputs["Value"], scale.inputs[0])
    scale.inputs[1].default_value = 9.0
    hi = nt.nodes.new("ShaderNodeMath")
    hi.operation = "MINIMUM"
    nt.links.new(scale.outputs["Value"], hi.inputs[0])
    hi.inputs[1].default_value = 1.0
    gate = nt.nodes.new("ShaderNodeMath")
    gate.operation = "MAXIMUM"
    nt.links.new(hi.outputs["Value"], gate.inputs[0])
    gate.inputs[1].default_value = 0.0
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    inv_face = nt.nodes.new("ShaderNodeMath")
    inv_face.operation = "SUBTRACT"
    inv_face.inputs[0].default_value = 1.0
    nt.links.new(lw.outputs["Facing"], inv_face.inputs[1])
    gate2 = nt.nodes.new("ShaderNodeMath")
    gate2.operation = "MULTIPLY"
    nt.links.new(gate.outputs["Value"], gate2.inputs[0])
    nt.links.new(inv_face.outputs["Value"], gate2.inputs[1])
    rim = nt.nodes.new("ShaderNodeEmission")
    rim.inputs["Color"].default_value = H.color(P["rim_color"])
    rim.inputs["Strength"].default_value = P["rim_strength"]
    add = nt.nodes.new("ShaderNodeAddShader")
    nt.links.new(sheen.outputs["Shader"], add.inputs[0])
    nt.links.new(rim.outputs["Emission"], add.inputs[1])
    nt.links.new(add.outputs["Shader"], out.inputs["Surface"])
    rimmix = nt.nodes.new("ShaderNodeMix")
    rimmix.data_type = "RGBA"
    rimmix.inputs["A"].default_value = (0, 0, 0, 1)
    rimmix.inputs["B"].default_value = H.color(P["rim_color"])
    nt.links.new(gate2.outputs["Value"], rimmix.inputs["Factor"])
    nt.links.new(rimmix.outputs["Result"], rim.inputs["Color"])
    return mat


def glow_material(name, center_z):
    """Emissive gradient peaking at the opening's own centre height, so each
    cut glows bright in the middle and falls to amber toward its cut edges."""
    old = bpy.data.materials.get(name)
    if old is not None:
        bpy.data.materials.remove(old)
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(geo.outputs["Position"], sep.inputs["Vector"])
    rng = nt.nodes.new("ShaderNodeMapRange")
    rng.clamp = True
    rng.inputs["From Min"].default_value = center_z - 0.20
    rng.inputs["From Max"].default_value = center_z + 0.20
    rng.inputs["To Min"].default_value = 0.0
    rng.inputs["To Max"].default_value = 1.0
    nt.links.new(sep.outputs["Z"], rng.inputs["Value"])
    sub = nt.nodes.new("ShaderNodeMath")
    sub.operation = "SUBTRACT"
    sub.inputs[0].default_value = 0.5
    nt.links.new(rng.outputs["Result"], sub.inputs[1])
    ab = nt.nodes.new("ShaderNodeMath")
    ab.operation = "ABSOLUTE"
    nt.links.new(sub.outputs["Value"], ab.inputs[0])
    two = nt.nodes.new("ShaderNodeMath")
    two.operation = "MULTIPLY"
    two.inputs[1].default_value = 2.0
    nt.links.new(ab.outputs["Value"], two.inputs[0])
    one = nt.nodes.new("ShaderNodeMath")
    one.operation = "SUBTRACT"
    one.inputs[0].default_value = 1.0
    nt.links.new(two.outputs["Value"], one.inputs[1])
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs["A"].default_value = H.color(P["glow_bottom"])
    mix.inputs["B"].default_value = H.color(P["glow_top"])
    nt.links.new(one.outputs["Value"], mix.inputs["Factor"])
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Strength"].default_value = P["glow_strength"]
    nt.links.new(mix.outputs["Result"], em.inputs["Color"])
    nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
    return mat


def add_shell(body, flesh):
    """Give the rind real thickness so the carved holes show a flesh rim."""
    body.data.materials.append(flesh)  # slot 1
    mod = body.modifiers.new("Shell", "SOLIDIFY")
    mod.thickness = P["shell"]
    mod.offset = -1.0
    mod.use_rim = True
    if hasattr(mod, "material_offset_rim"):
        mod.material_offset_rim = 1
    if hasattr(mod, "material_offset"):
        mod.material_offset = 1


def cut_face(body):
    cutters = []
    for name, outline in (("CutEyeL", EYE_L), ("CutEyeR", EYE_R), ("CutGrin", GRIN)):
        c = H.add_extrusion(name, outline, depth=0.5, location=(0, -0.18, 0),
                            rotation=(90, 0, 0))
        H.boolean(body, c)
        cutters.append(c)
    H.apply_modifiers(body)
    # boolean rebuilds the mesh: recompute the groove weight from final positions
    N = P["lobes"]
    phase = -math.pi / 2 - math.pi / N
    me = body.data
    attr = me.attributes.get("groove")
    if attr is None:
        attr = me.attributes.new("groove", "FLOAT", "POINT")
    for v in me.vertices:
        a = math.atan2(v.co.y / P["sy"], v.co.x / P["sx"])
        g = (0.5 - 0.5 * math.cos(N * (a - phase))) ** P["groove_pow"]
        attr.data[v.index].value = g
    H.shade_smooth(body, angle=35)
    return cutters


# gnarled stalk measured from hero.jpg: broad flared base (~6cm) seated in
# the crown, rising shaft, arch over to the right, tip descending with a
# broken hollow end; (x, y, z, radius) in metres
STEM_PATH = [(-0.010, 0.005, 0.335, 0.034),
             (-0.009, 0.005, 0.385, 0.030),
             (-0.004, 0.005, 0.425, 0.024),
             (0.004, 0.005, 0.458, 0.020),
             (0.018, 0.005, 0.482, 0.017),
             (0.038, 0.005, 0.497, 0.0145),
             (0.060, 0.005, 0.503, 0.0125),
             (0.080, 0.005, 0.499, 0.011),
             (0.094, 0.005, 0.488, 0.010),
             (0.100, 0.005, 0.476, 0.0095)]
# single sideways twiggy shoot off the stem's left side, partway up, with
# one fork; small leaflets ride along it (built in build_stem)
TWIG_MAIN = [(-0.008, 0.002, 0.448), (-0.045, -0.002, 0.458),
             (-0.080, -0.006, 0.466), (-0.112, -0.008, 0.468)]
TWIG_MAIN_R = [0.0038, 0.0030, 0.0022, 0.0015]
TWIG_FORK = [(-0.055, -0.003, 0.461), (-0.075, -0.005, 0.472),
             (-0.088, -0.006, 0.484)]
TWIG_FORK_R = [0.0024, 0.0018, 0.0012]


def sweep_mesh(name, pts, radii, n_sides=12, mat=None, col=None,
               cap_start=True, cap_end=True, ridges=0, ridge_amp=0.10):
    """Circular profile swept along a polyline, built as a real mesh.

    Catmull-Rom resampling smooths the path; bark ribs modulate the ring
    radius around the circumference and are stored in a 'ridge' vertex
    attribute (1 crest .. 0 crevice) for the bark material. Normals are
    verified outward on a mid ring, so the tube can never render inside-out.
    Returns (object, centers, end_tangent).
    """
    vp = [Vector(p) for p in pts]
    ext = [vp[0]] + vp + [vp[-1]]
    er = [radii[0]] + list(radii) + [radii[-1]]
    SUB = 7
    center, rad = [], []
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        r0, r1, r2, r3 = er[i - 1], er[i], er[i + 1], er[i + 2]
        for s in range(SUB):
            t = s / SUB
            t2, t3 = t * t, t * t * t
            c = (p1 * 2.0 + (p2 - p0) * t
                 + (p0 * 2.0 - p1 * 5.0 + p2 * 4.0 - p3) * t2
                 + (p3 - p0 + p1 * 3.0 - p2 * 3.0) * t3) * 0.5
            r = (r1 * 2.0 + (r2 - r0) * t
                 + (r0 * 2.0 - r1 * 5.0 + r2 * 4.0 - r3) * t2
                 + (r3 - r0 + r1 * 3.0 - r2 * 3.0) * t3) * 0.5
            center.append(c)
            rad.append(max(r, 0.0008))
    center.append(vp[-1])
    rad.append(max(radii[-1], 0.0008))
    n = len(center)
    up = Vector((0, 1, 0))
    bm = bmesh.new()
    rlay = bm.verts.layers.float.new("ridge") if ridges else None
    rings = []
    for k, (c, r) in enumerate(zip(center, rad)):
        tg = center[min(k + 1, n - 1)] - center[max(k - 1, 0)]
        if tg.length < 1e-9:
            tg = Vector((0, 0, 1))
        else:
            tg.normalize()
        nn = tg.cross(up)
        if nn.length < 1e-6:
            nn = Vector((1, 0, 0))
        else:
            nn.normalize()
        bb = tg.cross(nn).normalized()
        f = k / max(n - 1, 1)
        ring = []
        for j in range(n_sides):
            th = 2 * math.pi * j / n_sides
            rv, wob = 1.0, 0.5
            if ridges:
                ph = math.sin(th * ridges + f * 2.5)
                rv = 1.0 + ridge_amp * ph
                wob = 0.5 + 0.5 * ph
            v = bm.verts.new(c + (nn * math.cos(th) + bb * math.sin(th))
                             * (r * rv))
            if rlay is not None:
                v[rlay] = wob
            ring.append(v)
        rings.append(ring)
    for k in range(n - 1):
        for j in range(n_sides):
            j2 = (j + 1) % n_sides
            try:
                bm.faces.new((rings[k][j], rings[k][j2],
                              rings[k + 1][j2], rings[k + 1][j]))
            except ValueError:
                pass
    if cap_start:
        try:
            bm.faces.new(list(rings[0]))
        except ValueError:
            pass
    if cap_end:
        try:
            bm.faces.new(list(reversed(rings[-1])))
        except ValueError:
            pass
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mid = rings[n // 2][0].co - center[n // 2]
    if rings[n // 2][0].link_faces[0].normal.dot(mid) < 0:
        for f in bm.faces:
            f.normal_flip()
    obj = bpy.data.objects.new(name, H.mesh_from_bmesh(name, bm))
    H.link(obj, col)
    H.assign(obj, mat)
    H.shade_smooth(obj, angle=40)
    end_tangent = (center[-1] - center[-2]).normalized()
    return obj, center, end_tangent


def stem_material():
    """Olive bark: crest/crevice colours mixed by the sweep's ridge weight."""
    mat = H.material("StemBark", "#7A7444", roughness=0.85)
    nt = mat.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    base = bsdf.inputs.get("Base Color") or bsdf.inputs[0]
    attr = nt.nodes.new("ShaderNodeAttribute")
    attr.attribute_name = "ridge"
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs["A"].default_value = H.color("#2A2410")
    mix.inputs["B"].default_value = H.color("#96905A")
    nt.links.new(attr.outputs["Fac"], mix.inputs["Factor"])
    nt.links.new(mix.outputs["Result"], base)
    return mat


def build_stem(col, stem_mat, twig_mat, leaf_mat):
    # variants shrink the whole stem to their body (see blender/variants.md)
    ss = P.get("stem_scale", 1.0)
    pts = [(x * ss, y * ss, z * ss) for x, y, z, _ in STEM_PATH]
    radii = [r * ss for _, _, _, r in STEM_PATH]
    stem, centers, end_tg = sweep_mesh("Stem", pts, radii, n_sides=14,
                                       mat=stem_mat, col=col,
                                       cap_start=True, cap_end=False,
                                       ridges=7, ridge_amp=0.12)
    parts = [stem]
    # dark recessed plug inside the open tip: reads as a broken hollow end
    tip_c, tip_r = centers[-1], radii[-1]
    nn = end_tg.cross(Vector((0, 1, 0)))
    nn = nn.normalized() if nn.length > 1e-6 else Vector((1, 0, 0))
    bb = end_tg.cross(nn).normalized()
    bc = bmesh.new()
    tv = []
    for j in range(10):
        th = 2 * math.pi * j / 10
        tv.append(bc.verts.new(tip_c - end_tg * 0.008
                               + (nn * math.cos(th) + bb * math.sin(th))
                               * tip_r * 0.75))
    bc.faces.new(list(tv))
    bmesh.ops.recalc_face_normals(bc, faces=bc.faces)
    _flip_toward(bc, end_tg)
    plug = bpy.data.objects.new("StemTipDark",
                                H.mesh_from_bmesh("StemTipDark", bc))
    H.link(plug, col)
    H.assign(plug, twig_mat)
    parts.append(plug)
    # single sideways twiggy shoot + one fork, swept thin meshes
    # (scaled with the stem so minis keep their proportions)
    def _sp(pts, rr):
        return ([(x * ss, y * ss, z * ss) for x, y, z in pts],
                [r * ss for r in rr])
    twig, _, _ = sweep_mesh("Twig", *_sp(TWIG_MAIN, TWIG_MAIN_R),
                            n_sides=7, mat=twig_mat, col=col)
    fork, _, _ = sweep_mesh("TwigFork", *_sp(TWIG_FORK, TWIG_FORK_R),
                            n_sides=7, mat=twig_mat, col=col)
    parts += [twig, fork]
    # small pointed leaflets lying along the shoot, dark olive (never pale,
    # never upright: upright or pale reads as spikes, not leaves)
    leaf_shape = [(0, 0.013 * ss), (0.0056 * ss, 0.0016 * ss),
                  (0.0019 * ss, -0.013 * ss), (-0.0056 * ss, 0.0016 * ss)]
    for k, (loc, rot) in enumerate((
            ((-0.062, -0.010, 0.470), (90, 0, -25)),
            ((-0.098, -0.012, 0.473), (90, 0, 35)),
            ((-0.080, -0.010, 0.489), (90, 0, -10)),
            ((-0.114, -0.011, 0.470), (90, 0, 55)),
    )):
        leaf = H.add_extrusion(f"Leaf{k}", leaf_shape, depth=0.0015 * ss,
                               mat=leaf_mat, collection=col)
        loc = (loc[0] * ss, loc[1] * ss, loc[2] * ss)
        leaf.location = loc
        leaf.rotation_euler = [math.radians(a) for a in rot]
        parts.append(leaf)
    return parts


def setup_outlines(source_col):
    # STROKE preset brings grease-pencil materials with styles initialized
    # (fresh materials have grease_pencil=None and cannot take a stroke color).
    bpy.ops.object.grease_pencil_add(type="STROKE", location=(0, 0, 0))
    gp = bpy.context.active_object
    gp.name = "Outlines"
    for layer in list(gp.data.layers):
        gp.data.layers.remove(layer)
    gp.data.layers.new("Lines")
    mat = bpy.data.materials.get("Black")
    mat.name = "OutlineStroke"
    mat.grease_pencil.color = P["line_color"]
    mat.grease_pencil.show_stroke = True
    mod = gp.modifiers.new("LineArt", "LINEART")
    mod.source_type = "COLLECTION"
    mod.source_collection = source_col
    mod.use_contour = True
    mod.use_crease = True
    mod.use_crease_on_smooth = False  # groove lines are geometry tubes, not creases
    mod.use_edge_mark = False
    mod.use_loose = False
    mod.use_intersection = True
    mod.use_material = True
    mod.thickness = P["line_thickness"]
    mod.crease_threshold = P["crease_threshold"]
    mod.target_layer = "Lines"
    mod.target_material = mat
    return gp


def lighting(focus, r):
    dist = r * 4.0
    k = dist * dist * P["intensity"]

    def at(az, el):
        a, e = math.radians(az), math.radians(el)
        return focus + Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e),
                               math.sin(e))) * dist

    key = H.add_light("AREA", "Key", at(P["key_az"], P["key_el"]), focus,
                      energy=10 * k, size=dist * 0.55, light_color="#fff1e0")
    fill = H.add_light("AREA", "Fill", at(-65, 15), focus,
                       energy=10 * k * P["fill_level"], size=dist * 1.2,
                       light_color="#e8f0ff")
    rim = H.add_light("AREA", "Rim", at(155, 35), focus,
                      energy=6 * k * 1.2, size=dist * 0.5, light_color="#ffd9b0")
    H._no_shadow(fill)
    H._no_shadow(rim)
    # warm spill faking light thrown out of the cuts onto surrounding rind
    spill_m = H.add_light("POINT", "SpillMouth", (0.04, -0.50, 0.14),
                          (0.04, 0.0, 0.14), energy=0.22, light_color="#ff9a30")
    spill_e = H.add_light("POINT", "SpillEye", (-0.02, -0.48, 0.28),
                          (-0.02, 0.0, 0.28), energy=0.12, light_color="#ffa53c")
    H._no_shadow(spill_m)
    H._no_shadow(spill_e)
    stem_l = H.add_light("POINT", "StemLight", (0.0, -0.38, 0.58),
                         (0.0, 0.0, 0.45), energy=0.10, light_color="#fff5e0")
    H._no_shadow(stem_l)
    H.world_color("#0a0d13", 0.7)
    return [key, fill, rim, spill_m, spill_e, stem_l]


def add_bloom():
    """Fog-glow halo on the brightest pixels (cut glow, rim band, highlights)."""
    scene = bpy.context.scene
    scene.use_nodes = True
    nt = scene.node_tree
    comp = next((n for n in nt.nodes
                 if n.bl_idname == "CompositorNodeComposite"), None)
    if comp is None:
        rl = nt.nodes.new("CompositorNodeRLayers")
        comp = nt.nodes.new("CompositorNodeComposite")
        nt.links.new(rl.outputs[0], comp.inputs[0])
    src = comp.inputs[0].links[0].from_socket
    glare = nt.nodes.new("CompositorNodeGlare")
    glare.glare_type = "FOG_GLOW"
    glare.quality = "HIGH"
    glare.threshold = 0.85
    glare.size = 6
    glare.mix = 0.5
    nt.links.new(src, glare.inputs[0])
    nt.links.new(glare.outputs[0], comp.inputs[0])


def main():
    H.reset_scene()
    col = H.collection("Pumpkin")

    rind = rind_material()
    eye_glow = glow_material("GlowEye", 0.307)
    grin_glow = glow_material("GlowGrin", 0.150)
    stem_mat = stem_material()
    twig_mat = H.material("TwigMat", "#4A4226", roughness=0.85)
    leaf_mat = H.material("LeafMat", "#6A6232", roughness=0.8)

    body = build_body("Pumpkin", rind, col)
    flesh = H.emission_material("Flesh", P["flesh_color"], P["flesh_strength"])
    add_shell(body, flesh)
    groove = H.emission_material("GrooveLine", "#2A1206", 1.0)
    if P.get("groove_lines", True):
        build_groove_lines(groove)
    if STAGE >= 3 and CARVED:
        cut_face(body)
        if P.get("groove_lines", True):
            build_groove_lines(groove)
        glow_col = H.collection("GlowParts")
        build_cut_bevels(col, glow_col, flesh,
                           {"EyeL": eye_glow, "EyeR": eye_glow, "Grin": grin_glow})
        H.add_light("POINT", "InnerGlow", (0.03, -0.10, 0.20), (0.03, -0.5, 0.20),
                    energy=P["inner_light_energy"], light_color="#ffb340")

    greens = build_stem(col, stem_mat, twig_mat, leaf_mat) if STAGE >= 2 else []

    lo, hi = H.bbox([body] + greens)
    focus = (lo + hi) / 2
    r = max((hi - lo).length / 2, 0.01)
    lighting(focus, r)

    cam = H.add_camera("Camera", location=(0, -3, 0.3), target=tuple(focus), lens=P["lens"])
    H.frame_objects(cam, [body] + greens, azimuth=P["azimuth"], elevation=P["elevation"],
                    margin=P["margin"])
    # frame_objects pads for bbox depth; pull in so the subject fills the frame
    c2 = (lo + hi) / 2
    cam.location = c2 + (cam.location - c2) * P["frame_pull"]

    if STAGE >= 4:
        if TOON:
            P["line_thickness"] = 6
        setup_outlines(col)
    if STAGE in STAGE_NAMES:
        ex = os.path.join(ROOT, "tutorial", "examples", STAGE_NAMES[STAGE])
        os.makedirs(os.path.dirname(ex), exist_ok=True)
        H.set_render(engine="CYCLES", resolution=(480, 320), samples=10,
                     view_transform="Standard", exposure=P["exposure"], device="CPU")
        if STAGE >= 3:
            add_bloom()
        H.render_still(ex + ".png", background=P["bg"])
        H.save_blend(ex + ".blend")
        H.report()
        return

    if VARIANT != "generic" and STAGE == 99 and not (PREVIEW or TOON or TURNTABLE):
        vdir = os.path.join(ROOT, "tutorial", "variants")
        os.makedirs(vdir, exist_ok=True)
        ex = os.path.join(vdir, VARIANT)
        H.set_render(engine="CYCLES", resolution=(480, 320), samples=10,
                     view_transform="Standard", exposure=P["exposure"], device="CPU")
        if CARVED:
            add_bloom()
        H.render_still(ex + ".png", background=P["bg"])
        H.save_blend(ex + ".blend")
        H.report()
        return
    if PREVIEW:
        H.set_render(engine="CYCLES", resolution=(480, 320), samples=10,
                     view_transform="Standard", exposure=P["exposure"], device="CPU")
        add_bloom()
        H.render_still(OUT + "/preview.png", background=P["bg"])
    elif TOON:
        H.set_render(engine="CYCLES", resolution=(960, 640), samples=32,
                     view_transform="Standard", exposure=1.0, device="CPU")
        H.render_still(OUT + "/render_toon.png", background="#FFFFFF")
    elif TURNTABLE:
        os.makedirs(OUT + "/frames", exist_ok=True)
        H.set_render(engine="CYCLES", resolution=(480, 320), samples=10,
                     view_transform="Standard", exposure=P["exposure"], device="CPU")
        add_bloom()
        base = cam.location - c2
        for i in range(TURNTABLE_FRAMES):
            ang = 2 * math.pi * i / TURNTABLE_FRAMES
            ca, sa = math.cos(ang), math.sin(ang)
            off = Vector((base.x * ca - base.y * sa,
                          base.x * sa + base.y * ca, base.z))
            cam.location = c2 + off
            H.look_at(cam, tuple(focus))
            H.render_still("%s/frames/f%02d.png" % (OUT, i),
                           background=P["bg"])
    else:
        H.set_render(engine="CYCLES", resolution=(960, 640), samples=32,
                     view_transform="Standard", exposure=P["exposure"], device="CPU")
        add_bloom()
        H.render_still(OUT + "/render.png", background=P["bg"])
    H.save_blend(BLEND)
    H.report()


main()
