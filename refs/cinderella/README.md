# cinderella (rouge vif d'etampes)

French heirloom, Cucurbita maxima. 12-24 in diameter, 6 in tall, 15-20 lb.
Very flat wide fruit, concave crown, deep wide ribs, red-orange thick skin.

## reference files

- `front.jpg` - front three-quarter view
- `profile.jpg` - side profile, full silhouette

## observed traits (from refs)

- width is 2.5-3x height; crown dips below rim around stem
- 12-16 deep rounded ribs, sharp valleys
- skin red-orange (#c33d0f base, #e8641b highlights), matte
- stem short, thick, corky, tan with green streaks

## spec

| trait               | value                             |
| ------------------- | --------------------------------- |
| proportions (w x h) | 3.0 x 1.0                         |
| ribs                | 14, deep, rounded                 |
| base color          | #a82e0c (renders to ref red)      |
| highlight           | #e8641b                           |
| stem                | short corky cylinder, tan #a08b62 |
| crown               | concave dip, stem sits below rim  |

## blender plan (separate file: `blender/cultivars/cinderella.py`)

Construction: lathe profile curve (flat disc with dipped crown) via spin,
then rib displacement with 14-fold radial sine. Proportional editing shapes
the crown dip around the stem socket.

Feature shown: proportional editing + spin tool.
Docs: [spin](https://docs.blender.org/manual/en/latest/modeling/meshes/editing/duplicate_extrude/spin.html),
[proportional editing](https://docs.blender.org/manual/en/latest/editors/3dview/controls/proportional_editing.html),
[subdivision surface](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/subdivision_surface.html).

## photocraft plan

Feature: vibrance + warm photo filter to push the red-orange rind.
Docs: [photocraft](https://github.com/storytold/photocraft).

## acceptance

Render matches `profile.jpg` silhouette: flat disc, dipped crown, 14 ribs.
