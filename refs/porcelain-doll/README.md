# porcelain doll

Pink-skinned cultivar, Cucurbita maxima. 10-25 lb, large squared blocky
fruit, deep ribs, salmon-pink to peach glossy skin.

## reference files

- `front.jpg` - front three-quarter view
- `profile.jpg` - side profile, flat sides visible

## observed traits (from refs)

- blocky square-shouldered body, flat sides
- 12-14 deep glossy ribs
- skin salmon pink (#e8907c), glossy highlights
- stem sturdy, tan, medium

## spec

| trait               | value                        |
| ------------------- | ---------------------------- |
| proportions (w x h) | 1.2 x 1.0, squared           |
| ribs                | 12-14, deep                  |
| base color          | #e8907c                      |
| stem                | sturdy cylinder, tan #a08b62 |
| surface             | glossy clearcoat             |

## blender plan (separate file: `blender/cultivars/porcelain_doll.py`)

Construction: start from a cube, subdivide and spherify with bevel-weighted
edges to keep the square shoulders. Rib displacement applied after, so the
blocky read survives the ribs.

Feature shown: bevel modifier with weighted normals.
Docs: [bevel modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/bevel.html),
[weighted normal](https://docs.blender.org/manual/en/latest/modeling/modifiers/modify/weighted_normal.html).

## photocraft plan

Feature: gradient map for the pink blush ramp.
Docs: [photocraft](https://github.com/storytold/photocraft).

## acceptance

Render matches `profile.jpg`: square shoulders, glossy pink ribs.
