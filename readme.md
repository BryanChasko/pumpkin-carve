# pumpkin-carve: build a jack-o-lantern in blender, step by step

a beginner-friendly tutorial project. you will model a stylized
jack-o-lantern in blender 4.4 — by hand in the interface, in python, or
mixed — ink it with grease pencil, and grade the render in photocraft.
every step has a working example file you can open and take apart.

![the finished pumpkin, slowly turning](assets/pumpkin-turntable-480x320.webp)

## what you will make

follow along and adjust as you go. by the end you will have:

- a ribbed pumpkin body with a bent bark stem, built two ways
- a carved, glowing face (eyes and grin you can redesign freely)
- flat cartoon shading with a warm rim light
- bold grease pencil outlines over the 3d forms
- a graded final image, plus a printable inked drawing

![shaded render](assets/pumpkin-hero-960x640.webp)

## how this tutorial is organized

each step in [the tutorial](tutorial/tutorial.md) comes two ways, and
you can switch between them mid-step:

| track   | best for                     | you will use                           |
| ------- | ---------------------------- | -------------------------------------- |
| by hand | learning the interface       | modifiers, shader nodes, grease pencil |
| in code | rebuilding and tweaking fast | `blender/build_pumpkin.py`, annotated  |

example scenes for every stage live in `tutorial/examples/`:
`01-body`, `02-stem`, `03-carved-face`, `04-inked-final` (each as
`.blend` + `.png`). open them, orbit around, steal the node setups.

## the walkthrough

### 1. the ribbed body

a squashed sphere with 15 grooves and real rind thickness, so carved
holes show a pale flesh edge. by hand that is edge loops and a solidify
modifier; in code it is one polar-grid function with the groove weight
stored per vertex for later shading.

![body stage](tutorial/examples/01-body.png)

### 2. stem, twig, leaves

a bezier-curve stem with bark ridges (or a profile swept along a path),
a broken hollow tip, one thin twig, four small leaves.

![stem stage](tutorial/examples/02-stem.png)

### 3. carve the face

draw two triangles and a jagged grin, boolean-cut them for real, then
line each hole with a pale funnel and an amber glow cap. a small point
light inside the body is the candle. new face? any closed outline works.

![carved face stage](tutorial/examples/03-carved-face.png)

### 4. shading layers

toon diffuse for flat color, groove shading from the step-1 vertex
weight, painterly noise streaks, and an emission rim that only fires on
the silhouette. the shader tree is annotated node by node in the tutorial.

### 5. ink it with grease pencil

a line art modifier over the pumpkin collection draws contour, crease,
and intersection lines in near-black brown. render on white with thicker
lines and you get a coloring-page drawing of your own pumpkin.

![inked final stage](tutorial/examples/04-inked-final.png)

![the inked drawing](assets/pumpkin-ink-960x640.webp)

### 6. grade it in photocraft

photocraft is an open-source image editor written in rust: layers,
masks, adjustment layers, real psd files, fully offline. open your
render, add vibrance and contrast, warm it with a photo filter, then
bloom the highlights with a blurred screen-blend copy. the same five
steps run headlessly in `post/post.sh`, and the layered result is in
`post/render_post.psd` if you want to keep editing.

![graded render with brand frame](assets/pumpkin-framed-978x658.webp)

## try it now

you need blender 4.4. then either open `blender/scene.blend` and explore,
or rebuild everything from the script:

```
blender -b --factory-startup --python-exit-code 1 -P blender/build_pumpkin.py            # shaded final
blender -b --factory-startup --python-exit-code 1 -P blender/build_pumpkin.py -- --toon  # inked drawing
blender -b --factory-startup --python-exit-code 1 -P blender/build_pumpkin.py -- --stage=2
```

outputs land in `blender/exports/`. `--preview` renders small while you
iterate; `--stage=1` to `--stage=4` rebuilds the example scenes.
prefer clicking? the tutorial's by-hand track builds the same pumpkin
with no code at all.

## files

- `blender/build_pumpkin.py` — one annotated script that builds everything
- `blender/scene.blend` — the finished scene, saved from the final build
- `tutorial/tutorial.md` — the step-by-step walkthrough (start here)
- `tutorial/examples/` — a scene and render per stage
- `post/` — the photocraft grade chain (`post.sh`) and its outputs
- `assets/` — readme art: turntable and still webps, flicker svg,
  ascii text, and a small art helper (`make_art.py`)
- `refs/` — the two look-target drawings the build was shaped against
- `review/` — round-by-round review notes from the build process

art notes: stills ship as webp with a sha256 sidecar each; the turning
pumpkin above is 24 frames at a slow 6 fps. the little candlelit header
below is a hand-drawn svg — open `assets/pumpkin-flicker.svg` in a
browser and watch it flicker.

![flickering jack-o-lantern](assets/pumpkin-flicker.svg)

built for a community halloween build-along (ne3d, oct 2026) and kept
public so anyone can learn from it. carve something, shade something,
show someone.

```
                                   .:===.
                                   .====
                          .:..:-. .-----:: .-:..:.
                       .-+==+**=-=*#*-:+*#*-=**+==+=.
                     :=*+-=**+-:+=**+--+**+*--***=-**=:.
                   :=**=.=#*+=:=+=**+--+**+**:=**#=:+**=:
                 .-+**=.=#**+:-+=+**+--++*++*=:+**#=:=**+=.
                :=+*+=:-#**+-:=+=***+--++**+*+:-+**#=:=**++:
               :=+*+=:-***+=:-=+=#**+--=+**+**-:+**#*=:+*#++-
              -=+*+=::+#**+-:-+++#**+--=+**+**+:=+**#*--+*#++-
             :==**+-:=#***+::=+=*#**+--=++*++*+--+***#+-=**#++-
            .+=**+=:-*#**+=:-=+-+#**+--=++**+*+=-++**#*=--**#+*.
            +=+*+=-:=****+-:-+=*==**+--=++**+**=:=+***#==*=*#*++
           -+=**+=:-+***+=-:===%%-=*+--=+++*+**+-=+***+*#*=**#+*-
          .+=+*+=-:-****+=::=-#%%#-=*--==++*+**+--+*++#%%*++*#*=*.
          -+=*++=::=***++-:--+%%%%#-==:==++*+**+==+=*%%%%*+=**#+*=
          +=+++=-:-+***+=-:--%%%%%%#----=++*++*+=-=#%%%%%#*=+***+*
         :+=+++=-:-****+=--:*%%%%%%%*::-=++*++**=+%%##*++==-+**#=*:
         -+=++==-:=***++=-:=%%%%%%%%%*:-=+++++*-=+===-====--+**#+*=
         ==+++==::=***+=-::*##%###**++==-+++++*==--=++**#+=-+****++
         +=++==-:-=++++=-::-------==-----+++++**+--==+++*+=:++***++
         +=++==-:-=++++=-:-==+=***++=:::==+++=**+-:==+++*+=:=+***++
         +=+===-:-=++++=-::=++=****+=::--=+++=**+-:-==++*+=:=++**++
         +=+===-:-=+++=-:.:=++=****+=:::-=++==**+-:--==+*+=:=++**++
         ==+==--:-=++==-:.:=++=***++-:::-=++==**+-:--===++=:=+++*++
         -====--:--====-:.:-=+=***++-:.:-==+==*++::---==++=:=++++==
         :====--::-===--:.:-=+=+*++=-:.:-==+==*+=:::---===-:==++:=-
         .====--::--==-::.:-=+=++++=-:.:-=====*+=:.::---==::===-:=.
          -===--::-::--::.:-=+=++++=:..:-===-=*+-:.::-----::--*+:-
          :-==--::-:=--::..-=+-=++=-:..:-===-=+=-:.:::---:.:-*%--:
           --=--:.::=*:::..:=+--++=-:..:--==-=+=:...::---:.-#%+::
           .-=--:::-:##-...:-+=-=---:..:--==-==-=-...::::.+##*:..
            :----:.::=%#=..:-=-:-++-. .:--==---*%%#+-:::.=%##- .
             :---:.:::###=..:-=*%%%%#+:::----+%%%%%@%+=.-%##+
              :--::.::+##*+**+#**%%%%%%#=--+#%%%%%#*+**..:::
               :-::..:-###**:.-**+*%%%##*===+#%%#++##=:
                :-::..:##*: .-::+#*+**+=---::=+*+##=. .  .
                 :::...==  ..:=- -*#*=:.:---  .=*=....
```
