# cultivar scorecard

rubric, each 0-10. overall = mean. iterate until overall >= 8.
each cultivar's full tutorial — visual description, build, renders,
per-cultivar scorecard — lives in `tutorial/cultivars/<name>.md`.
this file is the master table plus shared build notes.
measured 2026-10-30 against `refs/<name>/front.jpg` + `profile.jpg`.

- sil: silhouette + proportions (w/h within 5% = 9+)
- ribs: rib count, depth, regularity vs ref
- color: rind tone vs ref under key light
- surf: surface read (matte/dusty/gloss/mottle/warts)
- stem: size, texture, seat vs ref

| cultivar           | sil | ribs | color | surf | stem | overall | round   |
| ------------------ | --- | ---- | ----- | ---- | ---- | ------- | ------- |
| cinderella         | 8   | 8    | 8     | 8    | 8    | 8.0     | r3 PASS |
| black futsu        | 8   | 8    | 8     | 8    | 8    | 8.0     | r2 PASS |
| sugar pie          | 8   | 8    | 8     | 8    | 8    | 8.0     | r2 PASS |
| baby boo           | 8   | 8    | 8     | 8    | 8    | 8.0     | r2 PASS |
| baby boo           | 9   | 9    | 8     | 8    | 9    | 8.6     | r3 PASS |
| porcelain doll     | 8   | 8    | 8     | 8    | 8    | 8.0     | r3 PASS |
| jarrahdale         | 8   | 8    | 8     | 8    | 8    | 8.0     | r2 PASS |
| lumina             | 9   | 8    | 8     | 8    | 8    | 8.2     | r1 PASS |
| long island cheese | 8   | 8    | 8     | 8    | 8    | 8.0     | r2 PASS |
| harvest moon       | 8   | 8    | 8     | 8    | 8    | 8.0     | r2 PASS |
| kabocha            | 8   | 8    | 8     | 8    | 8    | 8.0     | r3 PASS |

systematic gaps (all): smooth toy stems (refs are corky/fibrous),
skins too uniform (refs have mottling, dust, fiber). fixed per
file below — each cultivar keeps its own construction.

## r2 fixes

- porcelain doll: taller body (sz 0.98), square 0.07, ribs 0.20,
  tall corky ridged stem with fiber bump. target stem 8+, sil 8+.
- jarrahdale: roughness 0.8 + roughness breakup, ribs 0.18, bigger
  stem, bloom patchier. target surf 8+.
- cinderella: deeper red base, corky ridged stem. target color 8+.
- black futsu: bigger angular stem, cure threshold down. target 8.
- kabocha: mottle threshold up (fewer patches). target surf 8.
- sugar pie / baby boo / cheese / harvest moon: corky stems,
  minor color nudges. target 8+.

## r3 fixes

- cinderella: groove-driven roughness (waxy crests 0.32, matte
  valleys 0.58). a noise-streak attempt read as wood grain and
  was reverted. surf 8.
- porcelain doll: square 0.10, darker groove `#9a5f68`. sil 8.
- kabocha: mottle mapping 6.0 to 4.5 (larger celadon blotches);
  a stripe widening overshot and was reverted. surf 8.
