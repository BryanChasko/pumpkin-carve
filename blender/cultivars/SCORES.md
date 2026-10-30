# cultivar scorecard

rubric, each 0-10. overall = mean. iterate until overall >= 8.
measured 2026-10-30 against `refs/<name>/front.jpg` + `profile.jpg`.

- sil: silhouette + proportions (w/h within 5% = 9+)
- ribs: rib count, depth, regularity vs ref
- color: rind tone vs ref under key light
- surf: surface read (matte/dusty/gloss/mottle/warts)
- stem: size, texture, seat vs ref

| cultivar           | sil | ribs | color | surf | stem | overall | round   |
| ------------------ | --- | ---- | ----- | ---- | ---- | ------- | ------- |
| cinderella         | 8   | 8    | 8     | 7    | 8    | 7.8     | r2      |
| black futsu        | 8   | 8    | 8     | 8    | 8    | 8.0     | r2 PASS |
| sugar pie          | 8   | 8    | 8     | 8    | 8    | 8.0     | r2 PASS |
| baby boo           | 8   | 8    | 8     | 8    | 8    | 8.0     | r2 PASS |
| porcelain doll     | 8   | 8    | 8     | 7    | 8    | 7.8     | r2      |
| jarrahdale         | 8   | 8    | 8     | 8    | 8    | 8.0     | r2 PASS |
| lumina             | 9   | 8    | 8     | 8    | 8    | 8.2     | r1 PASS |
| long island cheese | 8   | 8    | 8     | 8    | 8    | 8.0     | r2 PASS |
| harvest moon       | 8   | 8    | 8     | 8    | 8    | 8.0     | r2 PASS |
| kabocha            | 8   | 8    | 8     | 7    | 8    | 7.9     | r2      |

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
