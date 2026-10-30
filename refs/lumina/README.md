# lumina (lumina white)

White carving pumpkin, Cucurbita pepo. 8-25 lb, rounded medium fruit,
shallow ribs, smooth matte pure-white skin, firm green stem base.

## reference files

- `front.jpg` - front three-quarter view
- `profile.jpg` - side profile, full silhouette

## observed traits (from refs)

- rounded ball, height ~0.95x width
- 14-16 shallow ribs, smooth matte skin
- skin pure white (#f5f5f2), soft grey valleys
- stem firm, green, upright

## spec

| trait               | value                             |
| ------------------- | --------------------------------- |
| proportions (w x h) | 1.0 x 0.95                        |
| ribs                | 14-16, shallow                    |
| base color          | #f5f5f2                           |
| stem                | firm cylinder, green #5a6b3a      |
| surface             | matte with slight subsurface look |

## blender plan (separate file: `blender/cultivars/lumina.py`)

Construction: smooth sphere body with faint ribs; white skin uses
subsurface scattering so candle light glows through the rind instead of
bouncing off. Built to be lit from inside.

Feature shown: subsurface scattering on principled BSDF.
Docs: [principled BSDF](https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html),
[lighting](https://docs.blender.org/manual/en/latest/render/lights/index.html).

## photocraft plan

Feature: levels adjustment to keep whites clean without clipping.
Docs: [photocraft](https://github.com/storytold/photocraft).

## acceptance

Render matches `profile.jpg`: smooth white ball, green stem, soft valleys.
