# Round 2 builder notes

## Global checks (loop_02_pre, measured — outrank impressions)

- EXPOSURE: render 15 levels darker -> exposure 0.40 -> 0.62, fill 0.08 -> 0.30.
- SHADOW SIDE: darks crushed 13 levels -> same fill/exposure lift; rind groove
  colour kept, flanks now keep orange hue.
- Measured framing boxes already matched (ref aspect 1.12 vs render 1.121),
  so only a small fill tweak (frame_pull 0.80 -> 0.78); no big dolly move.

## Findings chosen (scores <= 5 force big changes; minors ignored)

1. Mouth rebuild (critical): new GRIN with 4 broad upper V-teeth, 3 lower
   points, thin band, sharp upswept corner tips reaching both cheeks.
2. Face openings as true holes: bevel funnels recessed INSIDE the rind
   (outer rim was 8mm proud of the surface = the "double rim" and corner
   "fins"); pale flesh walls (#FFD98A, low emission) + amber caps.
3. Smooth rind: noise streak/bump unlinked from the toon shader; gloss 0.12
   -> 0.06; groove tubes 0.0023 -> 0.0015; LineArt 7 -> 5.
4. White mid-surface streak: rim gate narrowed to silhouette X in [0.85, 1.0],
   strength 1.5 -> 0.9. Streak gone; soft rim only near right edge.
5. Eyes resized/repositioned to observation-sheet stations; right eye
   enlarged into a flank wedge.
6. Body rounder: sz 0.70 -> 0.75, bottom flatten softened; mouth clears base.
7. Stem rebuilt: longer hooked path, slimmer (r 0.020), ridges computed on
   the tube front surface (old fixed offsets were buried inside), knobby
   broken-tip nub, olive colour.
8. Glow declipped: emission 2.3 -> 1.5, gradient range widened for raised face.
9. Note: `--cycles-device CPU` is rejected by this Blender 4.4 build
   ("unknown argument"); rebuilt without it (script forces CPU anyway).

## Second pass in-round

- Bevel walls still read wide/pale at mouth corners -> bevel_inner 0.84.
- Stem rendered near-black -> lightened to #6E6A38, noise amount 0.2.

## Kept or reverted: KEPT

New render vs backup: smooth skin, no white streak, wide correct-tooth grin
clear of the base, larger flank eye, declipped cores, longer ridged stem.
Nothing visibly worse.

## Still open

- Stem front still darker than reference olive; needs its own lift.
- Mouth corner tips still slightly flap-like; glow cores still pale-lemon
  rather than warm amber.
- Twig/sprig still blobby (minor, deferred); rib count 15 vs ~10 (minor).
- Cell-shade band edge and faint lobe-crown streaks (signature details) weak.
