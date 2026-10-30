# pumpkin build guide - manual reproduce and adapt

companion to build_pumpkin.py. the script is the exact recipe; below is the
same build expressed as blender gui steps for the live demo, plus the post
chain in photocraft. tested against blender 4.4, cycles on cpu.

## part 0 - setup (5 min)

1. open blender, new general file, delete the default cube, light, camera.
2. scene units: metric, unit scale 1.0. save as pumpkin.blend.
3. render engine cycles, device cpu, 32 samples, 960x640.
4. color management: view transform standard, exposure 0.92.
5. world background: very dark blue-grey (#0a0d13), strength 0.7.

## part 1 - ribbed body (25 min)

script ref: build_body, P lobes 15, groove_depth 0.115.

1. add uv sphere, 64 segments, 32 rings, radius 0.30.
2. scale x 1.0, y 0.92, z 0.75 (squat carving pumpkin).
3. edit mode: select every other longitudinal edge loop around the sides,
   scale x/y toward center by ~0.89 to cut 15 grooves. smooth-shade.
4. top: select center top verts, pull down 0.045 to seat the stem crater.
5. bottom: flatten slightly so it sits (scale z of lowest ring).
6. solidify modifier, thickness 0.012, offset -1, rim on: gives the rind
   real thickness so cuts show a flesh rim.

adapt: fewer lobes (10) reads cartoonish, more (20) reads gourd-like.
deeper grooves + darker groove color reads spookier under low light.

## part 2 - stem, twig, leaves (15 min)

script ref: build_stem, STEM_PATH, TWIG_MAIN.

1. stem: bezier curve from crown up 0.15, hook to the right at the tip.
   bevel depth 0.03 tapering to 0.01, convert to mesh.
2. bark: 7 ridges - select alternating rings, pull out 12%, vertex-paint
   a crest/crevice mask, mix dark (#2a2410) and olive (#96905a).
3. broken tip: leave the end open, add a small dark disc 8mm inside.
4. twig: thin curve off the left side partway up, one fork, radius 3mm.
5. leaves: 4 small pointed quads (13mm), dark olive, lying along the twig.

## part 3 - carve the face (25 min)

script ref: EYE_L, EYE_R, GRIN, cut_face, build_cut_bevels.

1. front view, add plane cutters: two tall triangles for eyes, one wide
   zigzag band for the grin (4 upper teeth, 3 lower points, upswept tips).
2. solidify each cutter 0.5 deep, boolean difference on the body, apply.
3. bevel walls: for each hole, build a funnel ring from the hole outline
   sloping inward 0.045 deep - pale flesh material (#f0b45c, slight glow).
4. glow caps: cap each funnel with the outline scaled 0.80 (eyes) or 0.84
   (grin), emission gradient peaking amber (#ffbe45) at center, falling to
   deep orange (#ff8f16) at the cut edge.
5. inner light: point light inside the body, warm (#ffb340), low energy.

adapt: swap the grin polyline for fangs, round eyes, or a witch hat
silhouette - any closed outline flows through the same funnel builder.

## part 4 - shading layers (15 min)

script ref: rind_material, glow_material.

1. rind: toon diffuse (size 0.62, smooth 0.06) mixed 10% toon glossy.
2. groove shading: vertex-paint grooves 0..1, power 2.8, mix lit orange
   (#f07818) to dark groove brown (#6e2f0c).
3. painterly streaks: two noise textures (scales 14 and 28) multiply the
   lit color +/-8%, plus 0.06 bump from the fine streaks.
4. rib-crest lift: lighten lobe crowns toward hot orange (#ff9a30).
5. rim: emission (#ffe6b0, strength 1.7) gated to outer-right silhouette
   by normal-x ramp times a grazing-view facing term.

## part 5 - grease pencil ink pass (10 min)

script ref: setup_outlines.

1. object > add > grease pencil > stroke. rename to Outlines.
2. delete default layers, add one layer named Lines.
3. rename its Black material to OutlineStroke, stroke color near-black
   brown (0.012, 0.005, 0.0025), show stroke on.
4. add line art modifier: source = pumpkin collection, contour + crease +
   intersection on, thickness 3 (6 for the print variant), target the
   Lines layer and OutlineStroke material.
5. groove tubes: thin dark tubes hugging each valley, split with a 9mm
   margin around the face holes so no dash crosses the glow.

render now: camera 70mm dead front, slight elevation, subject fills 90%
of frame. key area light front-right-top warm, fill front-left cool at
75%, rim back-right warm. compositor: fog glow, threshold 0.85, size 6,
mix 0.5. render -> render.png.

drawing variant: white background, line thickness 6, skip the glow node.
render -> render_toon.png (printable inked drawing).

## part 6 - post in photocraft (demo part two, 15 min)

scripted: post/post.sh (headless photocraft-cli engine, same commands as
the gui). live gui equivalents in brackets.

1. open render.png. [file > open]
2. vibrance 35, saturation 12. [image > adjustments > vibrance]
3. brightness -6, contrast +22. [image > adjustments > brightness/contrast]
4. warm photo filter #ff9a30 at 18%. [image > adjustments > photo filter]
5. duplicate layer, gaussian blur radius 8, blend screen at 60%.
   [layer > duplicate, filter > blur > gaussian blur, blend mode screen]
6. flatten, export render_post_glow.png. keep the layered version too:
   render_post.psd opens with real layers in photocraft or photoshop.

talking points: pure rust, offline, no subscription; real psd read and
write; every gui command exists in photocraft-cli, so the whole grade is
a script; --control serves the same engine to agents over json lines.

## adapt menu for the jam

- face: new outline polylines, or scale P inner_eye / inner_grin.
- mood: bg color, rim strength, glow strength, fog glow mix.
- style: toon size up for flatter cartoon, line thickness up for ink.
- turntable: animate camera azimuth 0..360 over 48 frames, eevee draft
  then cycles final. keep cpu only while the shared box is busy.
