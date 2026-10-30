# variants: ten cultivars, ten scripts

each cultivar is its own build script in `blender/cultivars/` — no
shared parameter table, no overrides. this file is the index: what
each script builds, which features it demonstrates, and where its
spec and outputs live.

specs (reference photos + measured proportions + acceptance line):
`refs/<name>/README.md`. gallery: `tutorial/tutorial.md` (cultivar
gallery section). post chains: `post/variants.sh`. each cultivar
ships `tutorial/variants/<name>.png` (front), `<name>-profile.png`,
and `<name>.blend`.

| #   | cultivar           | script                            | blender feature          | photocraft feature  |
| --- | ------------------ | --------------------------------- | ------------------------ | ------------------- |
| 1   | cinderella         | `cultivars/cinderella.py`         | profile lathe            | curves (psd)        |
| 2   | black futsu        | `cultivars/black_futsu.py`        | geo-nodes scatter        | brightness/contrast |
| 3   | sugar pie          | `cultivars/sugar_pie.py`          | primitive + subsurf      | hue/saturation      |
| 4   | baby boo           | `cultivars/baby_boo.py`           | linked duplicates        | invert              |
| 5   | porcelain doll     | `cultivars/porcelain_doll.py`     | cube spherify            | outer glow (psd)    |
| 6   | jarrahdale         | `cultivars/jarrahdale.py`         | sheen bloom              | gradient map (psd)  |
| 7   | lumina             | `cultivars/lumina.py`             | subsurface scattering    | photo filter (cool) |
| 8   | long island cheese | `cultivars/long_island_cheese.py` | boolean socket           | color balance       |
| 9   | harvest moon       | `cultivars/harvest_moon.py`       | documented light rig     | levels              |
| 10  | kabocha            | `cultivars/kabocha.py`            | noise texture + displace | channel mixer       |

rebuild one:

`blender -b --factory-startup --python-exit-code 1 -P blender/cultivars/<file>.py`

preview mode (`-- --preview`) renders 480x320 at 10 samples for
round-tripping; the default run renders 640x480 at 24 samples and
saves the `.blend`.

## build notes worth keeping

- `bmesh.ops.subdivide_edges` with an edge list silently no-ops in
  blender 4.4 (found on porcelain doll: 6-poly mesh, torn-looking
  rim). manual per-face grids weld with `remove_doubles` instead.
- the musgrave _shader_ node is gone in 4.4 (`ShaderNodeTexMusgrave`
  undefined). noise with distortion stands in; the legacy musgrave
  _texture_ still feeds displace modifiers (kabocha).
- geometry-nodes scatter needs the mask attribute to exist on the
  mesh before the modifier evaluates (futsu stores `groove` at
  build time).
- boolean cuts destroy custom attributes: rebuild `groove` from
  positions after `apply_modifiers` (long island cheese).
- `photocraft-cli image.adjustments.threshold` ignores its level in
  0.17 (futsu: identical output at 128, 48, and 0.25). brightness
  lift stands in; recorded in the futsu spec.
- Map Range node: From Min/Max is the INPUT range, To Min/Max the
  OUTPUT range. setting From 0.8-1.0 with default To 0-1 clamps
  almost all noise to 0 — jarrahdale rendered chrome-smooth for
  four rounds before the mirror test caught it. always set both.

cultivar facts: botanical interests (cinderella), garden betty +
specialty produce (black futsu), baker creek + rareseeds
(jarrahdale), cooksinfo (sugar pie, jarrahdale), specialty produce

- gourmetpedia (kabocha), seedsnbeyond (jarrahdale),
  goodgourds (jarrahdale).
