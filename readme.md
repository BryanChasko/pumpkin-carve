# 🎃 pumpkin-carve — a headless haunted blender pipeline 👻

> built live for the ne3d virtual pumpkin carving jam, oct 31 2026.
> part one: carve a jack-o-lantern without touching the mouse.
> part two: grade it in photocraft and talk rust all night. 🦇

![spinning jack-o-lantern](assets/pumpkin-turntable-480x320.webp)

![blender](https://img.shields.io/badge/blender-4.4-orange?style=flat-square)
![photocraft](https://img.shields.io/badge/photocraft-0.17-rust?style=flat-square)
![render](https://img.shields.io/badge/render-cycles_cpu-darkgreen?style=flat-square)
![vibes](https://img.shields.io/badge/vibes-haunted-purple?style=flat-square)

## the pumpkin, four ways 🕷️

| shaded                                                      | inked drawing                                          |
| ----------------------------------------------------------- | ------------------------------------------------------ |
| ![shaded pumpkin](assets/pumpkin-hero-960x640.webp)         | ![inked pumpkin](assets/pumpkin-ink-960x640.webp)      |
| `render.png` — toon rind, glow cuts, grease pencil line art | `render_toon.png` — white bg, bold 6px ink, zero bloom |

| graded + glow                                              | living svg                                        |
| ---------------------------------------------------------- | ------------------------------------------------- |
| ![graded pumpkin](assets/pumpkin-framed-978x658.webp)      | ![flickering pumpkin](assets/pumpkin-flicker.svg) |
| photocraft grade: vibrance, warm filter, screen-blend glow | hand-drawn svg, the candlelight flickers forever  |

## absolutely no mice were used 🖱️🚫

everything below runs headless. one script builds the pumpkin, carves the
face, inks the outlines, lights the candle, and renders — then a second
script grades it. the pipeline survived 4 blind-critic review rounds and
kept every single one.

```
blender -b --factory-startup --python-exit-code 1 -P build_pumpkin.py            # shaded
blender -b --factory-startup --python-exit-code 1 -P build_pumpkin.py -- --toon  # inked
./post/post.sh                                                                   # spooky grade
```

## the ascii pumpkin, for terminal goblins 🧛

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

regenerate: `python3 assets/make_art.py` (also builds the framed hero).

## repo map 🗺️

- `build_pumpkin.py` — the whole haunted pipeline in one script
- `scene.blend` — saved from the final build, poke it in the gui
- `render.png` / `render_toon.png` — shaded final + inked variant
- `post/` — `post.sh` grade chain, graded pngs, layered `render_post.psd`
- `assets/` — turntable webp + frames, hero/ink webps, flicker svg,
  ascii txt, sidecars with sha256 for every shipped file
- `guide.md` — the 2-hour jam script: gui reproduce steps, adapt menu,
  photocraft talking points
- `visual-plan/refs/` + `critic/` — look targets and all 4 review rounds

## house rules 🏚️

- cpu renders only while the shared box is busy. check `pgrep blender`
  first, never stop another session's process.
- ship webp; sidecar or it did not happen. brand: house navy `#0f141c`,
  one orange accent, deja vu sans for code-drawn type.
- seed of the jam: carve something, shade something, show something.

happy halloween. do not feed the render farm after midnight. 🎃
