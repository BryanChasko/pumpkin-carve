# variants: ten cultivars, one builder

each cultivar overrides the generic build through the `VARIANTS` table
in `blender/build_pumpkin.py` (`--variant=<name>`). this file is the
brief: what the cultivar looks like in the field, the exact overrides,
which blender and photocraft features it demonstrates, and the build
record filled in at render time.

generic baseline for every ratio below: 15 lobes, groove depth 0.115,
groove power 0.6, scale (1.0, 0.92, 0.75), radius 0.30 m, rind lit
`#f07818`, groove `#6e2f0c`, carved grin + triangle eyes, warm glow.

refs: `refs/hero.jpg`, `refs/side.png` (look targets, not sources).
cultivar facts: hudson valley seed (black futsu), baker creek /
rareseeds (jarrahdale), victory seeds + nichols nursery (cinderella /
rouge vif), specialty produce (sugar pie, kabocha), seed needs +
tomorrow seeds (baby boo), reimer seeds (porcelain doll), johnny's
(jarrahdale note + long island cheese), tomorrow seeds (lumina),
pumpkinpatches master list (harvest moon), the kitchn winter squash
(kabocha roundup).

## 1. cinderella (rouge vif d'etampes)

french heirloom, _c. maxima_. very flattened, slightly concave crown,
deep wide ribs, brilliant red-orange thick shiny skin, 10-20 lb.
the carriage pumpkin.

- overrides: lobes 12, groove 0.16, power 0.50, scale
  (1.0, 0.94, 0.55), radius 0.34. rind `#d8481c`, groove `#7a2408`,
  crest `#ff7a30`. carved: yes, wide grin.
- blender feature: displace modifier (clouds texture) over a
  subdivided body — sculpted ribs, not math ribs. docs: displace
  modifier, blender manual.
- photocraft feature: curves adjustment layer
  (`layer.newAdjustmentLayer.curves`), red-channel s-curve. layered
  psd kept.
- build record: _______________________________

## 2. black futsu

japanese heirloom, _c. moschata_. squat and blocky, 3-5 lb, heavy
ribbing with bumpy, sometimes warted skin; deep black-green young,
curing toward warm orange-buff.

- overrides: lobes 10, groove 0.20, scale (1.0, 0.92, 0.65), radius
  0.22. rind `#2a3a26`, groove `#101a10`, buff crest `#8a7a4a` at low
  mix. carved: no (warts and carving fight). ink only.
- blender feature: voronoi displacement + matching bump — warts as
  real geometry over subdivision. docs: displace modifier, voronoi
  texture. fallback (if the rim tears): bump only, recorded here.
- photocraft feature: threshold (`image.adjustments.threshold`) —
  a one-bit woodcut version beside the color render.
- build record: _______________________________

## 3. sugar pie

new england pie standard, _c. pepo_. small (15-18 cm), round and
slightly flattened, smooth bright orange with shallow light ridging
and a thick ridged green-brown stem.

- overrides: lobes 10, groove 0.07, scale (1.0, 0.94, 0.85), radius
  0.18. rind `#f58a1e`, groove `#a85a10`. carved: yes, small classic
  face scaled to the body.
- blender feature: array modifier — three linked pies at descending
  scale on one ground shadow-catcher; scale storytelling. docs:
  array modifier.
- photocraft feature: hue/saturation
  (`image.adjustments.hueSaturation`), warm shift +8/+10: pie
  orange to porch orange.
- build record: _______________________________

## 4. baby boo

miniature, _c. pepo_. 3 in wide, 2 in tall, flattened, deeply ribbed
for its size, creamy ghost white, thin strong stems. always a
cluster, never a soloist.

- overrides: lobes 12, groove 0.09, scale (1.0, 0.94, 0.70), radius
  0.045. rind `#e8e4da`, groove `#b8b0a0`. carved: no, ink only.
- blender feature: geometry nodes scatter — ground plane with a
  scatter of instanced boos (count ~14, seeded random rotation and
  scale). docs: geometry nodes introduction.
- photocraft feature: invert (`image.adjustments.invert`) — the
  ghost-negative graphic beside the color render.
- build record: _______________________________

## 5. porcelain doll

_c. maxima_ hybrid. large, squared and blocky, deeply ribbed,
pale-to-rich salmon pink rind, glossy for a pumpkin, 10-25 lb.

- overrides: lobes 12, groove 0.13, scale (1.02, 0.94, 0.62),
  radius 0.32. rind `#e8a0a8`, groove `#b07078`, crest `#f4c4c8`.
  carved: yes, soft round-eye face (16-gon outlines).
- blender feature: principled bsdf clearcoat — coat 0.6 over a
  soft pink base with light subsurface; modern layered shading vs
  the generic's toon stack. docs: principled bsdf.
- photocraft feature: outer glow layer style
  (`layer.layerStyle.outerGlow`), low-opacity pink halo, kept live
  in the layered psd.
- build record: _______________________________

## 6. jarrahdale

australian heirloom, _c. maxima_. slate blue-grey and dusty,
flattened drum, deep ribs, 6-12 lb. orange flesh inside (the glow
quotes it).

- overrides: lobes 12, groove 0.15, scale (1.0, 0.94, 0.58), radius
  0.33. rind `#7a8a94`, groove `#4a5a64`, crest `#a8bcc4`. carved:
  yes — blue-grey rind with orange glow, strongest complement in
  the set.
- blender feature: screw modifier lathe — a 2d drum profile
  (concave crown, straight wall, flat base) spun 360. docs: screw
  modifier.
- photocraft feature: gradient map
  (`layer.newAdjustmentLayer.gradientMap`), slate-to-amber
  duotone check beside the color version.
- build record: _______________________________

## 7. lumina

_c. maxima_. ivory white, smooth and matte, shallow-to-medium
ribbing, globular to slightly squat, 10-12 lb. the painter's
canvas of the family.

- overrides: lobes 11, groove 0.08, scale (1.0, 0.94, 0.78), radius
  0.30. rind `#dfe6ea`, groove `#aebac0`. carved: yes — white rind
  with deep orange glow; the set's carving close-up subject.
- blender feature: subsurface scattering plus fresnel edge tint in
  principled bsdf (subsurface 0.25 warm radius). docs: principled
  bsdf, subsurface section.
- photocraft feature: photo filter, cooling
  (`image.adjustments.photoFilter`, `#bfd9e8` at 15%) — moonlit
  white, opposite the generic's warm grade.
- build record: _______________________________

## 8. long island cheese

pre-civil-war american heirloom, _c. moschata_. the flattest of the
ten: a buff-tan wheel, smooth skin, medium ribs, slender woody
stem, 6-10 lb.

- overrides: lobes 14, groove 0.10, scale (1.0, 0.94, 0.48), radius
  0.34. rind `#c8a878`, groove `#8a6f4a`. carved: no — kept as the
  still-life wheel, thin ink pass.
- blender feature: edit-mode spin profile plus a bezier stem with a
  taper-curve object — two classic profile tools the generic build
  never touches. docs: spin tool, curve bevel/taper.
- photocraft feature: color balance
  (`image.adjustments.colorBalance`) — warm midtones, held
  shadows.
- build record: _______________________________

## 9. harvest moon

hybrid carving standard. round, smooth, uniform dark orange, 8-12
lb; bred for an even carve and a strong stem handle. the generic's
polished sibling.

- overrides: lobes 13, groove 0.12, scale (1.0, 0.94, 0.72), radius
  0.30. rind `#e06a10`, groove `#5e2806` (deliberately darker than
  generic for contrast banding). carved: yes, full classic face.
- blender feature: freestyle line rendering instead of grease
  pencil line art — silhouette + crease linesets, compared with
  line art on the same model. docs: freestyle introduction.
- photocraft feature: levels (`image.adjustments.levels`) — black
  point in, gamma 0.95; crushes the night while holding rind
  detail. paired with cinderella's curves, the two teach the
  difference.
- build record: _______________________________

## 10. kabocha

japanese winter squash. squat and round with a flat top and corky
stalk, dull dark green and bumpy, light green-grey striping and
speckling, 2-5 lb.

- overrides: lobes 10, groove 0.14, scale (1.0, 0.94, 0.68), radius
  0.20. rind base `#2e4a2a`, groove `#1a2e1a`, speckle `#c8b060`
  sparse. carved: no — still-life green, face would fight the
  striping.
- blender feature: speckle via thresholded noise — broad mottling
  plus a hard color-ramp speckle over a matte principled base;
  procedural pattern work, distinct from futsu's geometric warts.
  docs: noise texture.
- photocraft feature: channel mixer
  (`image.adjustments.channelMixer`) — green channel remap toward
  earth for botanical color problems.
- build record: _______________________________

## record-as-you-go protocol

every variant render fills its build record the same day:

```
variant: <name>   date: <utc>   cmd: blender -b ... -- --preview --variant=<name>
output: <path>   sha256: <first12>   viewed: pass/fail vs the four checks
fix applied (if any): <parameter change only>
```

photocraft passes log the same: command ids, params, psd layer
check via `photocraft-cli info` (layer tree present = pass).
round notes and review files stay out of the repo; the tutorial
sections are the only record readers see.
