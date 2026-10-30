# Round 4 builder notes

## Global checks (loop_04_pre, measured — fixed first)

- SHADOW SIDE (-12, crushed darks): fill 0.55 -> 0.65, groove-tube albedo
  #0D0603 -> #2A1206 (dark brown instead of crushed black), groove tubes
  thinned to r=0.0012.
- HIGHLIGHTS (+14, p90 206 vs 192): exposure 0.95 -> 0.88, key intensity
  0.95 -> 0.90, glow_strength 0.85 -> 0.75 with deeper amber gradient
  (#FFBE45/#FF8F16). Loop_05 pack re-measures both.

## Findings chosen (all 6 majors; the rib-count minor ignored — scores <= 6)

Right-eye size/position, flat eye decals (no cut wall), grin upper-edge
shape, protruding grin corner slabs, spike-row sprig, thin black smooth
stem. Grader texture=3/detail=4/lighting=3 also forced big material and
light changes, not tweaks.

## What changed (build_pumpkin.py, four build iterations)

Face geometry re-measured from hero.jpg crops (pixel boxes mapped through
the body box), replacing all three outlines:

- EYE_R rebuilt ~2.5x bigger: tall triangle leaning right onto the side
  rib, apex up. Iteration 1 overshot (base wrapped past frame 0.80);
  iteration 2 pulled apex/base in to [(0.185,0.340),(0.205,0.282),
  (0.078,0.270)] — now similar screen width to the left eye, ~2/3 height.
- EYE_L shifted to measured box, base flattened.
- Grin rebuilt: shallow 3-V upper edge (tooth depth 0.070 -> ~0.028),
  3 upward lower teeth interlocking with thin necks, thin upswept pointed
  corner tips reaching x +/-0.26/0.17 (verified x-monotone, min margin
  0.010, strictly simple polygon).
- Bevel funnels rebuilt: outer ring sits EXACTLY on the hole outline and
  is recessed 4mm inside the rind (kills the tan corner slabs by
  construction — nothing exists outside the cuts); inner openings widened
  (eyes 0.80, grin 0.84) so a broad pale flesh ring (#F0B45C @ 0.55)
  shows around every opening; per-opening glow gradients peaking at each
  cut's own centre (bright core, amber toward cut edges).
- Stem/twig rebuilt as swept MESH (new sweep_mesh: Catmull-Rom path,
  7 bark ribs in geometry + 'ridge' attribute driving a crest/crevice
  bark material, verified-outward normals). This also fixed the root
  cause of the black stem: curve-tube objects rendered unlit (stem pixel
  p90 was 18/255; the mesh stem renders p90 101, matching the reference's
  100). Broad 6cm flared base, arching hook, open tip with dark recessed
  plug (broken hollow end), dedicated stem fill light.
- Twig: single thin sideways shoot + one fork off the stem's left side
  partway up (as in the reference, not at the crown), 4 small dark-olive
  leaflets lying along it. The pale upright diamond row is gone.
- Rind material: linked the (previously dead) painterly mottle + new fine
  vertical rib-streak noise into the lit colour, whisper of streak bump
  on the toon normals, harder cell-shade step (toon 0.62, smooth 0.06).
- Groove tubes: POLY (no bezier overshoot past run ends) + 9mm exclusion
  margin around every hole. Diagnosed and fixed a dark dash inside the
  left-eye glow: the centre groove hugged the hole rim and crossed the
  recessed bevel in screen space. Glow caps moved out of the LineArt
  source collection (their rims coincide with wall inner rings, which
  already draw the inner bevel line) to kill doubled outlines.

Note: the given rebuild command's `--cycles-device CPU` flag is rejected
by this Blender 4.4 build ("unknown argument"); rebuilt without it — the
script already forces device="CPU" in set_render. Output paths,
resolution (960x640), engine, samples and background unchanged.

## Kept or reverted: KEPT

New render vs backup: right eye large and wrapped on the rib (was tiny),
both eyes + grin show wide pale 3D bevel rings (were flat decals), grin
has shallow measured Vs with flush pointed tips (was deep W with tan
slabs past the silhouette), stem is a thick ridged olive arch (was a
thin black hook), sprig is a thin sideways twig with leaflets (was an
upright pale spike row), rind has painterly streaks. The one new artifact
found mid-round (groove dash in the eye glow) was root-caused and fixed
in-round; zoomed crops verify all three openings clean. Nothing got
visibly worse.

## Iteration 5 (final): settling the exposure seesaw

First loop_05 pack: HIGHLIGHTS fixed (p90 177 vs 192, no flag) but
EXPOSURE -11 (mean 98 vs 108) and SHADOW SIDE -12 persisted. Diagnosed
p10 == the LineArt outline colour exactly (thick 5px outlines cover

> 10% of the subject, so no light can lift them): outlines 5px -> 3px
> (the reference's relative line weight) and lightened toward dark brown;
> fill 0.65 -> 0.75 and exposure 0.88 -> 0.92 for the mids. (One failed
> build in between: LineArt thickness requires int, 3.5 raised TypeError —
> fixed to 3. The failed run was masked by `| tail`; exit codes checked
> directly afterwards.) Final loop_05 pack: GLOBAL CHECKS all within
> tolerance, zero lines. Highlights, exposure, shadow side, framing: fixed.

## Still open (for round 5)

- Right eye ~2/3 left-eye height; reference is closer to ~4/5 with the
  apex a touch higher — small nudge, risk of re-overshooting the wrap.
- Left shadow flank still darker/redder than the reference's kept-hue
  falloff (see loop_05 pack; may need groove-albedo lift, not more light).
- Fine secondary rib striations are subtle; reference shows more marked
  fibre strokes on the right lobe crowns.
- Bevel interiors lack the reference's carved texture strokes (fine detail).
- Leaflets read small at output size; could grow ~1.3x.
