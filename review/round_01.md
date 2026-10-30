# Round 1 (builder)

## Blind review input (independent panel)

Grader: color 7, detail 3, lighting 3, shape 6, texture 3. Critics: parts 5, surface 5.
Global checks (measured): SHADOW SIDE — render darks 21 levels lighter than reference (p10 51 vs 30).

## Findings chosen (all 12 majors; minors ignored per loop rule while scores <= 6)

Parts: right-eye wedge shape/placement; no open hollow depth in any cut; mouth too
small with blunted teeth; stem thin/straight; single-wire tendril with blob leaf.
Surface: pale washed-out cut fills; no orange two-tone bevel bands; no right-edge rim
band; satin-CG-plastic rind; non-emissive matte cuts; no glow spill/halo; weak rib
highlights. Plus the measured shadow-side line.

## What changed (build_pumpkin.py; paths/resolution/engine/samples/background unchanged)

- Face redrawn from hero.jpg measurements: left eye widened to 0.16 (apex
  (0.008,0.315), base z 0.222); right eye a tilted wedge on the curvature
  ((0.190,0.318),(0.224,0.252),(0.118,0.240)); grin widened to x -0.140..0.232
  with 4 tall upper V valleys, 3 lower teeth, corners sweeping to z 0.21/0.235.
  Grin polygon verified x-monotone, no self-intersections (an earlier draft
  self-intersected and destroyed the body in the boolean; caught and fixed).
- Real cut depth: new build_cut_bevels() projects each outline onto the grooved
  surface (surface_y() relaxed fixed-point inversion) and builds orange emissive
  funnel walls (outer rim 1.03x tucked behind the rind, 50 mm deep) plus a yellow
  gradient glow cap (0.65x inner opening). Removed the flat GlowCore shell.
- Glow colors deepened (top #FFE45C, bottom #FF9E1F, strength 2.6); flesh walls
  orange #F59A2E at 1.4.
- Stem rebuilt: radius 0.024 with flared 1.7x base, 9-point hooked path with tip
  curling down at x 0.13, 5 bark-ridge tubes, warmer olive #7a7038 with grain
  noise + bump. Tendril replaced by 3 branching tubes + 5 pointed leaves.
- Rind: vertical brush-streak noise (±8% + bump 0.12), deeper groove #200E04,
  heavier groove tubes (r 0.0028) and LineArt (thickness 7), tighter crisper gloss
  (size 0.15, fac 0.12, #E06A10).
- Rim: old LayerWeight+MapRange gate mask-rendered RED ON THE WRONG (left) SIDE
  (MapRange mis-gates below-range inputs); replaced with commutative math-only
  X-ramp over [0.62,0.95], pale #FFE6B0 at 2.0.
- Light: key 12k with smaller 0.55 size, fill 0.07->0.03, world 1.0->0.45 (shadow
  side), rim light 1.2x, two warm no-shadow spill points in front of mouth/eyes,
  compositor fog-glow bloom (threshold 1.0, size 6) for cut/halo spill.
- Note: `blender --cycles-device CPU` is rejected by this Blender 4.4 build
  ("unknown argument"); rebuilds run without it (script already forces CPU).

## Keep or revert: KEPT

New render vs backup: two-tone beveled glowing cuts on all three openings,
wide sharp-toothed grin, tilted right wedge, thick hooked stem, leafy sprig,
right-edge rim band, darker shadow side, crisper rib streaks. Nothing regressed:
framing still matches (subject box ~equal), rind orange restored after two
exposure detours (spill energy, rim-veil whiteout) that were diagnosed with
scene.blend isolation renders and fixed in-script.

## Exposure rebalance (same round, measured lines)

First loop_02 pack overshot: mean -20, darks -15 crushed, brights +12. Rebalanced
in three steps: exposure 0.15->0.40, fill 0.03->0.08, world 0.45->0.70,
toon_size 0.55->0.62, key 12k->11k, rim 2.0->1.5, glow 2.6->2.3, flesh
1.4->1.2, groove shading narrowed (power 1.5->2.8, color #3A1A08) with tubes
0.0023. Final loop_02: mean 94 vs 108 (-15), p10 17 vs 30 (-13), highlights
line cleared (p90 199 vs 192). Residual is dark-share, not gain: unlit black
groove tubes + LineArt + bg inside the tall stem box. Framing matches (aspect
1.121 vs 1.12, center within 2%).

## Still open (for round 2+)

- Rim streak between right eye and grin corner runs a bit hot/white; warm it.
- Brush-streak texture still subtle vs reference heavy painted strokes.
- Minor findings untouched: side-lobe count/width, secondary rib seams, stem
  highlight ridge (stem warmed already as part of rebuild).
- Verify loop_02 pack numbers (shadow-side p10, framing) against reference.
