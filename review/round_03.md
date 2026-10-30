# Round 3 builder notes

## Global checks (loop_03_pre, measured — fixed first)

- EXPOSURE (-10 levels): exposure 0.62 -> 0.84 (+0.22 EV as advised).
- HIGHLIGHTS (+44, washing out): glow_strength 1.5 -> 0.85, glow_top
  deepened to #FFC946, key 11k -> 10k. Over-contrast pair (dark subject +
  blown brights) addressed together with the shadow-lift items below.

## Findings chosen (all majors; minors ignored — every score was <= 6)

Parts: hollow openings, grin size/teeth, beige corner flaps, right-eye
shape/position, stem shape/surface, twig-vs-spikes. Surface: crushed lobe
shadows, pale glow cores, grey-beige cut walls, black stem, missing rim,
plastic rind, glossy stem / cardboard walls, top-lit falloff, missing halo
and spill.

## What changed (build_pumpkin.py, three build iterations)

- Grin rebuilt from measured proportions: tall band (~40% body height),
  4 large downward upper teeth + 3 large upward lower teeth, sharp upswept
  pointed corner tips. Polygon verified x-monotone, min margin 0.023.
- Right eye rebuilt: smaller tilted wedge leaning onto the side curvature,
  ~1/6 the old area; left eye kept.
- Beige corner flaps deleted by construction: bevel outer rim recessed
  3mm inside the rind (was 4mm proud), outer scale 1.06, inner opening
  0.94 so glow reaches the corner tips; funnel depth 0.05 for real hollow
  read around the full perimeter of all three openings.
- Stem rebuilt: thicker (R 0.022), shorter, stronger taper (2.2 -> 0.28),
  6 alternating light/dark bark ridges, smaller tip nub; color lifted
  toward olive (#948E52), roughness 0.8.
- Twig: thicker branches, leaves 1.35x larger, moved forward out of the
  stem's key-light shadow; twig/leaf colors lightened (#655E2E/#7A7A40).
- Rind: groove color #3A1A08 -> #5E2408, toon size 0.70, new crisp
  rib-crest highlight lift (pow(1-groove,2.5) toward #FF9A30), sheen 0.10.
- Cut walls/flesh: #E89F45 at 0.45 (warm orange-tan, was pale beige).
- Light: key elevation 50 -> 38, fill 0.30 -> 0.45, spill energies ~2x,
  bloom threshold 1.0 -> 0.85 and mix 0.5 for halo + softened cores.
- Rim: gate narrowed to [0.90,1.0] x steep ramp, multiplied by a
  grazing-view (1-facing) term, strength 1.5. Iteration 1 widened the old
  gate to 0.80 and painted a bright streak down a mid-surface lobe flank
  (diagnosed via zoomed crop); iteration 2 reverted it; iteration 3 added
  the narrow+facing gate. Streak gone, true right-limb rim kept.
- Framing: frame_pull 0.78 -> 0.76 (subject was slightly small).

Note: the given rebuild command's `--cycles-device CPU` flag is rejected
by this Blender 4.4 build ("unknown argument"); rebuilt without it — the
script already forces device="CPU" in set_render. Output paths,
resolution (960x640), engine, samples and background unchanged.

## Kept or reverted: KEPT

New render vs backup: grin now tall with big teeth, right eye small and
tilted, no solid flaps outside the cuts, lobes readable reddish-brown,
glow amber instead of neon lemon, stem thicker/ridged/olive, twig visibly
leafy, right-limb rim present with no mid-surface streak. Nothing got
visibly worse.

## Iteration 4 (final): post-pack global checks

First loop_04 pack showed EXPOSURE -12 and SHADOW SIDE crushed (the
pre-round HIGHLIGHTS line was fixed, framing slightly over-filled).
Nudged exposure 0.84 -> 0.95, fill 0.45 -> 0.55, groove albedo to
#6E2F0C, frame_pull 0.76 -> 0.77 and re-ran the loop_04 pack. Final
global checks: SHADOW SIDE -12 (stubborn: darks are the unlit
near-black groove tubes/outlines, fill cannot lift them — next round
should lighten the groove-line/outline albedo instead of adding light)
and HIGHLIGHTS +14 (mild re-appearance from the exposure bump, down
from +44). Net over the round: exposure fixed, highlights +44 -> +14.

## Still open (for round 4)

- Shadow-side crush lives in unlit black linework: lift groove-tube and
  outline color (e.g. toward #2A1206) rather than adding light.
- Settle the exposure/highlight seesaw (try exposure ~0.90, key 9k).
- Stem still darker/browner than the reference olive grey-green; needs
  more lift or a dedicated stem light.
- Twig cluster still slightly spiky; leaves could be broader/rounder.
- Glow cores still a touch pale-lemon at center; could go deeper amber.
- Fine lobe striations/secondary seams (minor, deliberately ignored).
