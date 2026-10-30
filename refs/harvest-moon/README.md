# harvest moon

Large golden pumpkin, Cucurbita pepo. 20-30 lb, big round fruit, golden
yellow smooth skin with light ribbing, thick green-brown stem.

## reference files

- `front.jpg` - front three-quarter view
- `profile.jpg` - side profile, full silhouette

## observed traits (from refs)

- big round ball, height ~0.95x width
- 16-18 light ribs, smooth skin, warm sheen
- skin golden yellow (#f0a832)
- stem thick, upright, green-brown

## spec

| trait               | value                      |
| ------------------- | -------------------------- |
| proportions (w x h) | 1.0 x 0.95, large          |
| ribs                | 16-18, light               |
| base color          | #f0a832                    |
| stem                | thick, green-brown #6b6b3a |
| surface             | smooth, warm sheen         |

## blender plan (separate file: `blender/cultivars/harvest_moon.py`)

Construction: large round body with light ribs; this build is the lighting
study — three-point area-light rig with warm key so the gold reads without
blowing out. Documents light placement values, not just the mesh.

Feature shown: studio lighting (area lights, world, exposure).
Docs: [lights](https://docs.blender.org/manual/en/latest/render/lights/index.html),
[color management](https://docs.blender.org/manual/en/latest/render/color_management.html).

## photocraft plan

Feature: hue/saturation for the golden grade.
Docs: [photocraft](https://github.com/storytold/photocraft).

## acceptance

Render matches `profile.jpg`: big gold ball, warm even light, thick stem.
