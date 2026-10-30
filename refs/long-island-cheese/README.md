# long island cheese

Old domestic cheese-type pumpkin, Cucurbita moschata. 6-10 lb, very
flattened wheel / truckle shape, buff-tan smooth skin, stem well sunk
into a recessed top.

## reference files

- `front.jpg` - front three-quarter view
- `profile.jpg` - side profile, wheel silhouette

## observed traits (from refs)

- low wheel, width ~2x height, flat top and bottom
- 16-18 fine shallow ribs, smooth skin
- skin buff tan (#d9a960), slightly deeper in valleys
- stem short, recessed into a deep well at top center

## spec

| trait               | value                            |
| ------------------- | -------------------------------- |
| proportions (w x h) | 2.0 x 1.0                        |
| ribs                | 16-18, fine and shallow          |
| base color          | #d9a960                          |
| stem                | short, sunk in recessed well     |
| top                 | deep stem well, not a crown bump |

## blender plan (separate file: `blender/cultivars/long_island_cheese.py`)

Construction: flattened body with fine ribs; the signature is the recessed
stem well, cut with a boolean cylinder sunk into the top, stem planted
inside it. Shows boolean cuts for sockets, not just face holes.

Feature shown: boolean modifier for sockets and wells.
Docs: [boolean modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/booleans.html),
[modifiers](https://docs.blender.org/manual/en/latest/modeling/modifiers/index.html).

## photocraft plan

Feature: warming photo filter for the buff-tan rind.
Docs: [photocraft](https://github.com/storytold/photocraft).

## acceptance

Render matches `profile.jpg`: low wheel, stem visibly sunk in a well.
