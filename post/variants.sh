#!/bin/bash
# variants.sh - one photocraft feature per cultivar.
# usage: ./post/variants.sh (repo root; needs photocraft-cli 0.17+)
# magnitudes use 0..1 (opacity 0.6 = 60%). psds keep live layers/styles.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PC=/home/bryanchasko/.local/opt/artcraft/photocraft-0.17.0-linux-x86_64/bin
export PATH="$PC:$PATH"
V="$ROOT/tutorial/variants"
O="$ROOT/post/variants"
mkdir -p "$O"

# 1. cinderella - curves adjustment layer, red-channel s-curve
photocraft-cli run "$V/cinderella.png" \
	--cmd layer.newAdjustmentLayer.curves \
	--cmd layer.setAdjustment \
	--params '{"red":[[0,0],[64,48],[192,208],[255,255]]}' \
	--out "$O/cinderella.psd"
photocraft-cli run "$O/cinderella.psd" \
	--cmd layer.flattenImage \
	--out "$O/cinderella.png"

# 2. black futsu - threshold ink (graphic variant beside the color render)
photocraft-cli run "$V/black-futsu.png" \
	--cmd image.adjustments.threshold --params '{"threshold":128}' \
	--out "$O/black-futsu.png"

# 3. sugar pie - hue/saturation warm shift
photocraft-cli run "$V/sugar-pie.png" \
	--cmd image.adjustments.hueSaturation \
	--params '{"hue":8,"saturation":10}' \
	--out "$O/sugar-pie.png"

# 4. baby boo - invert ghost negative
photocraft-cli run "$V/baby-boo.png" \
	--cmd image.adjustments.invert \
	--out "$O/baby-boo.png"

# 5. porcelain doll - outer glow layer style, kept live in the psd
photocraft-cli run "$V/porcelain-doll.png" \
	--cmd layer.layerStyle.replace \
	--params '{"effects":[{"kind":"outerGlow","params":{"color":"#ff9ac0","opacity":0.5,"size":12}}]}' \
	--out "$O/porcelain-doll.psd"
photocraft-cli run "$O/porcelain-doll.psd" \
	--cmd layer.flattenImage \
	--out "$O/porcelain-doll.png"

# 6. jarrahdale - gradient map duotone, kept live in the psd
photocraft-cli run "$V/jarrahdale.png" \
	--cmd layer.newAdjustmentLayer.gradientMap \
	--cmd layer.setAdjustment \
	--params '{"shadows":"#4a5a64","highlights":"#e88a30"}' \
	--out "$O/jarrahdale.psd"
photocraft-cli run "$O/jarrahdale.psd" \
	--cmd layer.flattenImage \
	--out "$O/jarrahdale.png"

# 7. lumina - cooling photo filter (opposite of the generic warm grade)
photocraft-cli run "$V/lumina.png" \
	--cmd image.adjustments.photoFilter \
	--params '{"color":"#bfd9e8","density":15}' \
	--out "$O/lumina.png"

# 8. long island cheese - warm midtone color balance
photocraft-cli run "$V/long-island-cheese.png" \
	--cmd image.adjustments.colorBalance \
	--params '{"midtones":[12,6,-4]}' \
	--out "$O/long-island-cheese.png"

# 9. harvest moon - levels black point (night contrast hold)
photocraft-cli run "$V/harvest-moon.png" \
	--cmd image.adjustments.levels \
	--params '{"shadowInput":18,"gamma":0.95}' \
	--out "$O/harvest-moon.png"

# 10. kabocha - channel mixer rows are 4 numbers (r,g,b,constant)
photocraft-cli run "$V/kabocha.png" \
	--cmd image.adjustments.channelMixer \
	--params '{"red":[100,20,0,0],"green":[0,80,20,0],"blue":[0,0,100,0]}' \
	--out "$O/kabocha.png"

ls -la "$O"
