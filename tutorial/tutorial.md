# making a blender pumpkin, step by step

this tutorial walks you through building a stylized jack-o-lantern in
blender 4.4, the same one in the readme. every step comes two ways:

- **by hand** — the interface version, with modifiers and shader nodes.
- **in code** — a small annotated python snippet from
  `blender/build_pumpkin.py`, so you can rebuild, tweak, and re-render.

do it however you like: fully by hand, fully in code, or mixed. open the
matching file in `tutorial/examples/` at each step to poke at a working
scene before moving on. no prior blender experience assumed beyond opening
the app and orbiting with the middle mouse button.

all renders here use cycles on cpu, 32 samples at 960x640, view transform
standard. preview renders at 480x320 and 10 samples keep the loop fast.

---

## step 0 — set the scene

**by hand**

1. start blender, delete the default cube, light, and camera.
2. scene properties: render engine cycles, device cpu.
3. output: 960x640. color management: view transform standard, exposure 0.92.
4. world: very dark blue-grey (we used `#0a0d13`), strength 0.7.
5. save as `scene.blend` somewhere you can find again.

**in code** — `blender/build_pumpkin.py`, in `main()`:

```python
# one scene, rebuilt from scratch every run: nothing depends on
# what happened to be open when you pressed enter
H.reset_scene()
col = H.collection("Pumpkin")          # everything lives in one collection
```

the helper `H` is `blender/../scripts/bpy_helpers.py` from the blender
skill; plain `bpy` works too, the calls are one-to-one.

![step 1 result](../tutorial/examples/01-body.png)

## step 1 — the ribbed body

**goal:** a squat, round pumpkin with 15 soft grooves, real rind thickness.

**by hand**

1. add a uv sphere (64 segments, 32 rings, radius 0.30 m).
2. scale it: x 1.0, y 0.92, z 0.75. it should look slightly squashed.
3. tab into edit mode. select every other longitudinal edge loop around
   the middle, then scale x/y toward the center by about 0.89. repeat
   until you count 15 grooves. shade smooth.
4. press the top center vertices down about 0.045 m (a shallow crater
   where the stem will sit) and flatten the bottom slightly so it sits.
5. give it thickness: solidify modifier, thickness 0.012, offset -1,
   rim enabled. this is what lets a carved hole show a pale flesh edge.

**in code** — `build_body()` in the script:

```python
# the body is a polar grid: for each ring (rings) and segment (segs),
# the radius dips where a groove belongs. `g` is the groove weight:
# 1 at a valley, 0 on a crest. it is stored as a per-vertex attribute
# and reused later for shading (step 4).
g = (0.5 - 0.5 * cos(N * (a - phase))) ** groove_pow
rr = R * (1 - groove_depth * g) * sin(phi)
```

then `add_shell()` adds the same solidify rim, with a flesh material on
the rim (`material_offset_rim = 1`).

open `tutorial/examples/01-body.blend` and orbit. yours should be a plain
ribbed squash, no stem, no face yet.

**make it yours:** 10 lobes reads cartoonish, 20 reads like a gourd.
deeper grooves look spookier in low light.

![step 2 result](../tutorial/examples/02-stem.png)

## step 2 — stem, twig, leaves

**goal:** a bent, bark-ridged stem with a little broken twig.

**by hand**

1. add a bezier curve: start in the crater, rise about 0.15 m, then hook
   to the right and drop the tip slightly, like a handle.
2. bevel depth about 0.03 m at the base tapering to 0.01 at the tip
   (object data: taper object, or geometry nodes curve to mesh).
3. convert to mesh. for bark, select alternating small loops along the
   stem and pull them out about 12% — seven ridges reads right.
4. leave the tip open and tuck a small dark disc 8 mm inside it: a
   broken, hollow end.
5. twig: a second thin curve off the left side, one fork, radius 3 mm.
   leaves: four small pointed planes, dark olive, lying along the twig.

**in code** — `build_stem()` sweeps a circular profile along the path:

```python
# sweep_mesh(): a ring of vertices at each path point, radius from
# the path table. `ridges` modulates the ring radius so the bark
# ribbing is real geometry, and a `ridge` vertex attribute records
# crest (1) vs crevice (0) for the bark material in step 4.
stem, centers, end_tg = sweep_mesh("Stem", pts, radii, n_sides=14,
                                   mat=stem_mat, col=col,
                                   cap_start=True, cap_end=False,
                                   ridges=7, ridge_amp=0.12)
```

open `tutorial/examples/02-stem.blend`.

![step 3 result](../tutorial/examples/03-carved-face.png)

## step 3 — carve the face

**goal:** two triangular eyes and a wide jagged grin, cut for real, with
glowing interiors.

**by hand**

1. front view (numpad 1). sketch your face on paper first, it helps.
2. eyes: two tall triangles on a new mesh. grin: one wide zigzag band —
   we used 4 upper teeth, 3 lower points, and upswept pointed tips.
3. solidify each shape 0.5 m deep (well past the pumpkin surface).
4. boolean modifier on the body, difference, one per shape. apply all.
5. glow: for each hole, make a shallow funnel from the hole outline
   sloping inward about 0.045 m — pale flesh material. cap the funnel
   with the outline scaled to 0.80 (eyes) or 0.84 (grin) and give the
   cap an emission gradient: bright amber in the middle, deep orange at
   the edge.
6. put a small warm point light inside the body. that is the candle.

**in code** — `cut_face()` cuts with extruded outline polygons:

```python
# EYE_L, EYE_R, GRIN are just (x, z) outlines in metres, measured off
# the reference drawing. change the numbers, get a new face.
for name, outline in (("CutEyeL", EYE_L), ("CutEyeR", EYE_R),
                      ("CutGrin", GRIN)):
    c = H.add_extrusion(name, outline, depth=0.5,
                        location=(0, -0.18, 0), rotation=(90, 0, 0))
    H.boolean(body, c)
```

`build_cut_bevels()` then builds the funnel plus glow cap per hole, with
the outer ring sitting exactly on the hole outline so nothing pokes out.

open `tutorial/examples/03-carved-face.blend`.

## step 4 — shading layers

**goal:** flat cartoon orange that still shows form: lit crests, dark
grooves, a warm rim on the silhouette.

**by hand** (shader editor, on the body material)

1. add a toon bsdf (diffuse, size 0.62, smooth 0.06). mix 10% toon
   glossy for a slight sheen.
2. paint the grooves: vertex paint, dark in the valleys. in nodes, read
   it with an attribute node, raise to power 2.8, and mix lit orange
   `#f07818` toward groove brown `#6e2f0c`.
3. painterly streaks: two noise textures (scale 14 and 28), each mapped
   to a 0.88–1.08 multiply, added over the lit color. add 0.06 bump
   from the fine noise so the light catches the fibres.
4. crest lift: lighten the rib crowns toward hot orange `#ff9a30`.
5. rim: emission `#ffe6b0` at strength 1.7, multiplied by a ramp on the
   normal x component (outer-right silhouette only) times one-minus-
   facing from a layer weight node. silhouettes glow, faces do not.
6. glow caps: emission with a gradient that peaks at each hole's own
   center height — bright in the middle, amber at the cut edge.

**in code** — `rind_material()` builds exactly this node tree. the groove
mix reads the attribute written in step 1:

```python
attr = nt.nodes.new("ShaderNodeAttribute")
attr.attribute_name = "groove"        # the step-1 vertex weight
pw = nt.nodes.new("ShaderNodeMath")
pw.operation = "POWER"                # sharpen the falloff
pw.inputs[1].default_value = 2.8
```

**make it yours:** toon size up (0.8) goes flatter and more cartoon;
size down (0.4) goes softer and more clay-like.

![step 5 result](../tutorial/examples/04-inked-final.png)

## step 5 — ink it with grease pencil

**goal:** bold drawn outlines over the 3d shading, so the render reads
as an illustration you could also print and color in.

**by hand**

1. object > add > grease pencil > stroke. rename it `Outlines`.
2. delete its default layers, add one layer called `Lines`.
3. add a line art modifier: source = your pumpkin collection, contour,
   crease, and intersection on, thickness 3. target layer `Lines`,
   material near-black brown.
4. thin dark tubes hugging each groove (curve circles, radius 1.2 mm)
   deepen the ribs. keep them 9 mm away from the face holes so no dash
   crosses the glow.
5. compositor: glare node, fog glow, threshold 0.85, size 6, mix 0.5.

**in code** — `setup_outlines()`:

```python
# STROKE preset matters: a fresh grease pencil material has no stroke
# styles until a preset initializes them
bpy.ops.object.grease_pencil_add(type="STROKE", location=(0, 0, 0))
gp = bpy.context.active_object
gp.name = "Outlines"
mod = gp.modifiers.new("LineArt", "LINEART")
mod.source_type = "COLLECTION"
mod.source_collection = source_col   # lines follow the 3d forms
mod.use_contour = True
mod.use_crease = True
mod.use_intersection = True
```

open `tutorial/examples/04-inked-final.blend`, then run the full script:

```
blender -b --factory-startup --python-exit-code 1 -P blender/build_pumpkin.py
```

you get `blender/exports/render.png`. two more modes:

```
blender -b --factory-startup --python-exit-code 1 -P blender/build_pumpkin.py -- --toon
blender -b --factory-startup --python-exit-code 1 -P blender/build_pumpkin.py -- --preview
```

`--toon` is the inked drawing on white (line thickness 6, no bloom):
`blender/exports/render_toon.png`. `--preview` renders small and fast
while you iterate. `--stage=1` … `--stage=4` rebuilds the example files.

**camera and lights, either way:** 70 mm lens, dead front, subject fills
about 90% of frame. key area light front-right-top warm, fill front-left
cool at 75%, rim back-right warm.

## step 6 — grade it in photocraft

you have a render. now give it a finished, candlelit feel. photocraft is
an open-source image editor written in rust (layers, masks, adjustment
layers, real psd files, works offline). open `blender/exports/render.png`
in it, or run the same steps headlessly — every interface command exists
in `photocraft-cli` too, which is how the files in `post/` were made.

1. vibrance 35, saturation 12. (image > adjustments > vibrance)
2. brightness -6, contrast +22.
3. warm photo filter `#ff9a30` at 18%.
4. duplicate the layer, gaussian blur radius 8, set the copy to screen
   blend at 60% opacity. highlights bloom like candlelight.
5. keep two versions: flattened for the web, layered as a real `.psd`
   you can keep editing (`post/render_post.psd`).

reproduce from the terminal with `post/post.sh`. talking points if you
show this to others: the whole grade is five commands, so it is a
script; the same engine answers agents over a local control connection;
and the psd really does open elsewhere with layers intact.

## where to go next

- new faces: edit the `EYE_L`, `EYE_R`, `GRIN` outlines in the script,
  or draw new cutters by hand. fangs, round eyes, a whole scene — any
  closed outline flows through the same builder.
- mood: background color, rim strength, glow strength, bloom mix.
- motion: `--turntable` renders 24 orbit frames into
  `blender/exports/frames/`; stitch with ffmpeg into an animated webp.
- print: the `--toon` drawing at line thickness 6 makes a clean
  coloring page.
