# black futsu

Japanese heirloom, Cucurbita moschata. 3-5 lb, squat blocky fruit.
Starts near-black green with heavy ribs and warts, cures toward
tawny buff patches. Gray-blue dusty bloom when young.

## reference files

- `front.jpg` - front three-quarter, curing buff patches visible
- `profile.jpg` - side profile, wart rows along ribs

## observed traits (from refs)

- squat blocky sphere, slightly flat top and bottom
- 10-12 heavy ribs crusted with wart rows
- skin near-black green (#1d2419) curing to buff (#c99a63) on rib tops
- stem hard, angular, tan, medium length

## spec

| trait               | value                                                 |
| ------------------- | ----------------------------------------------------- |
| proportions (w x h) | 1.15 x 1.0                                            |
| ribs                | 10-12, heavy, wart-crusted                            |
| base color          | #1d2419                                               |
| cured patches       | #c99a63                                               |
| stem                | angular tapered box, tan #9a7f57                      |
| surface             | wart instances + dusty bloom (low roughness variance) |

## blender plan (separate file: `blender/cultivars/black_futsu.py`)

Construction: ribbed base mesh, warts as icosphere instances scattered by
geometry nodes (distribute points on faces, density masked to rib crests by
position attribute). Two-tone cure via vertex-color mask mixed in shader.

Feature shown: geometry nodes scatter + instance on points.
Docs: [geometry nodes](https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/index.html),
[instance on points](https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/point/instance_on_points.html),
[shader editor](https://docs.blender.org/manual/en/latest/editors/shader_editor.html).

## photocraft plan

Feature: channel mixer to separate the green-black base from buff cure tones.
Docs: [photocraft](https://github.com/storytold/photocraft).

## acceptance

Render matches `profile.jpg`: blocky silhouette, visible wart rows, buff patches.
