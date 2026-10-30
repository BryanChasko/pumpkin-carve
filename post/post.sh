#!/bin/bash
# post.sh - spooky grade for the pumpkin render, headless photocraft engine.
# needs: photocraft-cli 0.17+ (this box: ~/.local/opt/artcraft/*/bin)
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PC=/home/bryanchasko/.local/opt/artcraft/photocraft-0.17.0-linux-x86_64/bin
export PATH="$PC:$PATH"

# grade: vibrance + contrast + warm photo filter
photocraft-cli run "$ROOT/blender/exports/render.png" \
	--cmd image.adjustments.vibrance --params '{"vibrance":35,"saturation":12}' \
	--cmd image.adjustments.brightnessContrast --params '{"brightness":-6,"contrast":22}' \
	--cmd image.adjustments.photoFilter --params '{"color":"#ff9a30","density":18}' \
	--out "$ROOT/post/render_post.png"

# glow: blurred screen-blend copy on top, then flatten for web
photocraft-cli run "$ROOT/post/render_post.png" \
	--cmd layer.duplicate \
	--cmd filter.blur.gaussianBlur --params '{"radius":8}' \
	--cmd layer.setProps --params '{"blendMode":"screen","opacity":0.6}' \
	--cmd layer.flattenImage \
	--out "$ROOT/post/render_post_glow.png"

# same stack unflattened, as a real layered psd for the live demo
photocraft-cli run "$ROOT/post/render_post.png" \
	--cmd layer.duplicate \
	--cmd filter.blur.gaussianBlur --params '{"radius":8}' \
	--cmd layer.setProps --params '{"blendMode":"screen","opacity":0.6}' \
	--out "$ROOT/post/render_post.psd"

ls -la "$ROOT/post/"
