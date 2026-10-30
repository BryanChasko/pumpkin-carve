# pumpkin-carve: build a jack-o-lantern in blender, step by step

model a stylized jack-o-lantern in blender 4.4 and finish it in
photocraft. this page is the map; [the tutorial](tutorial/tutorial.md)
is the walk. each step below matches one tutorial step, in order, with
the same name — finish a step here, open the same step there for the
full instructions, open its example scene to compare as you go.

![the finished pumpkin, slowly turning](assets/pumpkin-turntable-480x320.webp)

## start here

1. install blender 4.4 and photocraft 0.17 (links and scene setup are
   step 0 of the tutorial).
2. open [the tutorial](tutorial/tutorial.md) and keep it beside blender.
3. work through the steps in order. each one offers two tracks — by
   hand in the interface, or in annotated python — and they produce
   the same pumpkin, so switch whenever one clicks better.
4. stuck? every step ends with what your result should look like and
   what to fix when it doesn't. there's an index at the end.

![the finished render](assets/pumpkin-hero-960x640.webp)

## the six steps

**step 1 — the ribbed body.** a squashed sphere with 15 grooves and
real rind thickness, plus a groove mask the shading will reuse.
→ [tutorial step 1](tutorial/tutorial.md) ·
[example scene](tutorial/examples/01-body.blend)

![after step 1](tutorial/examples/01-body.png)

**step 2 — stem, twig, leaves.** a bent stem with bark ridges, a
broken hollow tip, leaves lying along a thin twig.
→ [tutorial step 2](tutorial/tutorial.md) ·
[example scene](tutorial/examples/02-stem.blend)

![after step 2](tutorial/examples/02-stem.png)

**step 3 — carve the face.** triangular eyes and a jagged grin cut
through the rind, lined with pale funnels and amber glow, lit from
inside.
→ [tutorial step 3](tutorial/tutorial.md) ·
[example scene](tutorial/examples/03-carved-face.blend)

![after step 3](tutorial/examples/03-carved-face.png)

**step 4 — shading layers.** toon color, groove shading from the
step-1 mask, painterly streaks, and a rim that only fires on the
silhouette. the tutorial lists the node tree socket by socket.
→ [tutorial step 4](tutorial/tutorial.md)

**step 5 — ink it with grease pencil.** line art outlines over the
model, then a white-background drawing variant of your own pumpkin.
→ [tutorial step 5](tutorial/tutorial.md) ·
[example scene](tutorial/examples/04-inked-final.blend)

![after step 5](tutorial/examples/04-inked-final.png)

![the inked drawing](assets/pumpkin-ink-960x640.webp)

**step 6 — grade it in photocraft.** vibrance and contrast, a warm
filter, and a blurred screen-blend glow — in the app, or with the
identical terminal commands in `post/post.sh`.
→ [tutorial step 6](tutorial/tutorial.md)

![after step 6](assets/pumpkin-framed-978x658.webp)

## prefer starting from a finished pumpkin?

open `blender/scene.blend` and take it apart, or rebuild it all:

```
blender -b --factory-startup --python-exit-code 1 -P blender/build_pumpkin.py
```

variations (`-- --toon`, `-- --preview`, `-- --stage=1` … `4`) are in
the tutorial's "run the whole build" section. outputs land in
`blender/exports/`.

## files

- `tutorial/tutorial.md` — the walkthrough (start there)
- `tutorial/examples/` — one scene and render per stage
- `blender/build_pumpkin.py` — the full build as one annotated script
- `blender/scene.blend` — the finished scene
- `post/` — the step-6 grade: script, graded images, layered psd
- `assets/` — the images on this page
- `refs/` — the look-target drawings from tutorial step 3

one last piece: `assets/pumpkin-flicker.svg` is a hand-drawn vector
of the same pumpkin. open it in a browser and watch the candlelight.

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
