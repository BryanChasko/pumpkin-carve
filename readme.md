# ne3d virtual pumpkin carving - headless blender build

built for the oct 31 2026 ne3d meetup: part one carves a stylized
jack-o-lantern in blender, part two grades it in photocraft (artcraft
studio) with first-impression talking points.

## contents

- build_pumpkin.py - one rebuildable script: ribbed body, carved glowing
  face, stem + twig + leaves, toon shading layers, grease pencil line art
  ink pass, lights, camera, compositor bloom. cpu cycles only.
- scene.blend - saved from the final build.
- render.png - shaded final (960x640).
- render_toon.png - inked drawing variant: white bg, bold lines, no bloom.
- post/render_post.png - photocraft grade (vibrance, contrast, warm filter).
- post/render_post_glow.png - plus blurred screen-blend glow, flattened.
- post/render_post.psd - same stack unflattened, real layered psd.
- post/post.sh - the exact headless photocraft-cli post chain, re-runnable.
- guide.md - manual gui reproduce + adapt menu + live demo script.
- visual-plan/refs/ - hero.jpg + side.png look targets (generated: the
  meetup drive links need login, so no drive art is used here).
- critic/ - observation sheet + 4 blind-critic rounds, all kept.

## rebuild

blender -b --factory-startup --python-exit-code 1 -P build_pumpkin.py
blender -b --factory-startup --python-exit-code 1 -P build_pumpkin.py -- --toon
blender -b --factory-startup --python-exit-code 1 -P build_pumpkin.py -- --preview
./post/post.sh

one blender at a time on the shared box: check pgrep blender first, never
stop another session's process. cpu device is forced in-script.

## versions

blender 4.4.0, photocraft-cli 0.17.0, ubuntu 24.04.

## known gaps

- blind grader left lighting/texture low: bevel interiors lack carved
  texture strokes, left shadow flank runs dark vs the ref.
- right eye slightly short of the ref ideal; leaflets small at output size.
- round files use the workflow's own format, so critic.py check does not
  parse them; rounds + diffs live in critic/round_*.md and stand as the
  review record.
