# sugar pie

Classic pie pumpkin, Cucurbita pepo. ~15 cm across, 6-8 in, 6-7 lb.
Small round neat fruit, slightly flattened, smooth bright orange skin
with light ridging, thick ridged green-brown stem.

## reference files

- `front.jpg` - front three-quarter view
- `profile.jpg` - side profile, full silhouette

## observed traits (from refs)

- round ball, height ~0.9x width
- 18-20 shallow ribs, smooth skin, light sheen
- skin bright orange (#e86a10), thin rind look
- stem thick, upright, ridged, green-brown

## spec

| trait               | value                                      |
| ------------------- | ------------------------------------------ |
| proportions (w x h) | 1.0 x 0.9                                  |
| ribs                | 18-20, shallow                             |
| base color          | #e86a10                                    |
| stem                | thick ridged cylinder, green-brown #6b6b3a |
| surface             | smooth, light clearcoat sheen              |

## blender plan (separate file: `blender/cultivars/sugar_pie.py`)

Construction: UV sphere scaled to pie proportions, shallow rib displacement,
subdivision surface for the smooth grocery-pumpkin finish. Stem from a
ridged cylinder with vertical groove displacement.

Feature shown: subdivision surface modifier workflow.
Docs: [subdivision surface](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/subdivision_surface.html),
[modifiers](https://docs.blender.org/manual/en/latest/modeling/modifiers/index.html).

## photocraft plan

Feature: curves adjustment for the clean orange ramp.
Docs: [photocraft](https://github.com/storytold/photocraft).

## acceptance

Render matches `profile.jpg`: neat round ball, shallow ribs, thick stem.
