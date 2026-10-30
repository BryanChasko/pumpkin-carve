# pumpkin-carve: build a jack-o-lantern in blender, step by step

a tutorial for building a stylized jack-o-lantern in blender 4.4 and
finishing it in photocraft. each step comes two ways — by hand in the
interface, or in annotated python — and ends with a working example
scene you can open and take apart. start to finish is an afternoon;
each step stands on its own if you only want one technique.

![the finished pumpkin, slowly turning](assets/pumpkin-turntable-480x320.webp)

## what you will make

- a ribbed pumpkin body with a bent, bark-ridged stem
- a carved glowing face you can redesign freely
- flat cartoon shading with a warm rim light
- bold grease pencil outlines over the 3d forms
- a graded final image, plus a printable inked drawing

![the finished render](assets/pumpkin-hero-960x640.webp)

## the walkthrough

full instructions, both tracks, in [the tutorial](tutorial/tutorial.md).
the short version:

**1. the ribbed body** — a squashed sphere with 15 grooves and real
rind thickness. edge loops and solidify by hand; a polar grid with a
per-vertex groove mask in code.
[example scene](tutorial/examples/01-body.blend)

![body stage](tutorial/examples/01-body.png)

**2. stem, twig, leaves** — a bezier stem with bark ridges, a broken
hollow tip, and leaves lying along a thin twig.
[example scene](tutorial/examples/02-stem.blend)

![stem stage](tutorial/examples/02-stem.png)

**3. carve the face** — triangular eyes and a jagged grin, cut through
the rind with booleans, lined with pale funnels and amber glow caps,
lit from inside.
[example scene](tutorial/examples/03-carved-face.blend)

![carved face stage](tutorial/examples/03-carved-face.png)

**4. shading layers** — toon color for flatness, the groove mask for
form, noise streaks so large areas never look like plastic, and an
emission rim that only fires on the silhouette. the tutorial lists
the node tree socket by socket.

**5. ink it with grease pencil** — a line art modifier traces contour,
crease, and intersection lines over the model. render on white with
thicker lines for a coloring-page drawing of your own pumpkin.
[example scene](tutorial/examples/04-inked-final.blend)

![inked final stage](tutorial/examples/04-inked-final.png)

![the inked drawing](assets/pumpkin-ink-960x640.webp)

**6. grade it in photocraft** — photocraft is an open-source image
editor written in rust: layers, masks, adjustment layers, real psd
files, works offline. open the render, add vibrance and contrast,
warm it with a photo filter, then bloom the highlights with a
blurred screen-blend copy. `post/post.sh` runs the identical steps
from the terminal, and `post/render_post.psd` keeps the grade as
editable layers.

![the graded render](assets/pumpkin-framed-978x658.webp)

## try it now

install blender 4.4 and photocraft 0.17, clone this repo, then either
open `blender/scene.blend` and explore, or rebuild everything:

```
blender -b --factory-startup --python-exit-code 1 -P blender/build_pumpkin.py
```

outputs land in `blender/exports/`. useful variations: `-- --toon`
for the inked drawing, `-- --preview` for a small fast render while
you iterate, `-- --stage=1` through `-- --stage=4` to regenerate
the example scenes. prefer clicking? the tutorial's by-hand track
builds the same pumpkin with no code at all.

## files

- `blender/build_pumpkin.py` — the full build as one annotated script
- `blender/scene.blend` — the finished scene
- `tutorial/tutorial.md` — the step-by-step walkthrough
- `tutorial/examples/` — one scene and render per stage
- `post/` — the photocraft grade: script, graded images, layered psd
- `assets/` — the images on this page and the script that makes them
- `refs/` — the look-target drawings the pumpkin was shaped against

the svg below is hand-drawn vector — open
`assets/pumpkin-flicker.svg` in a browser and watch the candlelight.

![flickering jack-o-lantern](assets/pumpkin-flicker.svg)

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
