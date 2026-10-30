# baby boo

Miniature white pumpkin, Cucurbita pepo. ~8 cm across, palm size.
Flattened disc, deeply ribbed for its size, creamy ghost-white smooth
skin, thin upright green-brown stem.

## reference files

- `front.jpg` - front three-quarter view
- `profile.jpg` - side profile, full silhouette

## observed traits (from refs)

- flat disc, width ~1.6x height
- 10 deep ribs, smooth matte skin
- skin creamy white (#f2ede2), faint warm shading in valleys
- stem thin, upright, green-brown

## spec

| trait               | value                              |
| ------------------- | ---------------------------------- |
| proportions (w x h) | 1.6 x 1.0                          |
| ribs                | 10, deep for size                  |
| base color          | #f2ede2                            |
| stem                | thin cylinder, green-brown #7a6b45 |
| surface             | matte, no sheen                    |

## blender plan (separate file: `blender/cultivars/baby_boo.py`)

Construction: small ribbed body built once, then linked duplicates arranged
as a cluster of three minis at varied rotation. Teaches instancing for
repeated props instead of rebuilding.

Feature shown: linked duplicates / collection instances.
Docs: [linked duplicates](https://docs.blender.org/manual/en/latest/scene_layout/object/editing/linked_duplicates.html),
[collections](https://docs.blender.org/manual/en/latest/scene_layout/collections/collections.html).

## photocraft plan

Feature: threshold adjustment layer for a high-contrast ink-style variant.
Docs: [photocraft](https://github.com/storytold/photocraft).

## acceptance

Render matches `profile.jpg`: flat white disc, deep ribs, thin stem.
