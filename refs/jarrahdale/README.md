# jarrahdale

Australian heirloom, Cucurbita maxima. 6-10 lb (up to 20+), flattened
drum shape, deep ribs, slate blue-grey dusty skin, golden flesh inside.

## reference files

- `front.jpg` - front three-quarter view
- `profile.jpg` - side profile, drum silhouette

## observed traits (from refs)

- flattened drum, width ~1.5x height, flat top and bottom
- 12-14 deep ribs with dusty bloom in valleys
- skin slate blue-grey (#7a8b99), pale bloom (#a8b6c0)
- stem sturdy, tan, medium

## spec

| trait               | value                        |
| ------------------- | ---------------------------- |
| proportions (w x h) | 1.5 x 1.0                    |
| ribs                | 12-14, deep                  |
| base color          | #7a8b99                      |
| bloom               | #a8b6c0 dusting in valleys   |
| stem                | sturdy cylinder, tan #9a7f57 |

## blender plan (separate file: `blender/cultivars/jarrahdale.py`)

Construction: squashed sphere drum with deep ribs; dusty bloom done in the
shader with a principled BSDF sheen layer masked to rib valleys, not as
geometry.

Feature shown: principled BSDF sheen / clearcoat for bloom.
Docs: [principled BSDF](https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html),
[shader editor](https://docs.blender.org/manual/en/latest/editors/shader_editor.html).

## photocraft plan

Feature: color balance to hold the blue-grey against warm light.
Docs: [photocraft](https://github.com/storytold/photocraft).

## acceptance

Render matches `profile.jpg`: blue-grey drum, visible dusty bloom.
