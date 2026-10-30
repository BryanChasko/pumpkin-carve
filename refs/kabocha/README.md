# kabocha

Japanese winter squash, Cucurbita maxima. 2-5 lb, squat drum with flat
ends, dark forest-green skin with pale celadon mottling and faint stripes,
short stubby tan stem.

## reference files

- `front.jpg` - front three-quarter view
- `profile.jpg` - side profile, drum silhouette

## observed traits (from refs)

- squat drum, width ~1.4x height, flat top and bottom
- 12-14 ribs with pale celadon striping along crests
- skin dark green (#24351f) mottled with pale patches (#9fb08a)
- stem short, stubby, tan

## spec

| trait               | value                              |
| ------------------- | ---------------------------------- |
| proportions (w x h) | 1.4 x 1.0                          |
| ribs                | 12-14 with pale crest stripes      |
| base color          | #24351f                            |
| mottling            | #9fb08a patches and crest stripes  |
| stem                | short stubby cylinder, tan #9a7f57 |

## blender plan (separate file: `blender/cultivars/kabocha.py`)

Construction: drum body with moderate ribs; mottling from a musgrave
texture driving both color mix and a small displace, with a second stretched
mapping for the pale crest stripes. No painted patches — all procedural.

Feature shown: texture coordinates + mapping + musgrave for mottling.
Docs: [texture coordinate](https://docs.blender.org/manual/en/latest/render/shader_nodes/input/texture_coordinate.html),
[mapping](https://docs.blender.org/manual/en/latest/render/shader_nodes/vector/mapping.html),
[displace modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/displace.html).

## photocraft plan

Feature: hue/saturation shift demo on the green rind.
Docs: [photocraft](https://github.com/storytold/photocraft).

## acceptance

Render matches `profile.jpg`: dark drum, visible mottling and crest stripes.
