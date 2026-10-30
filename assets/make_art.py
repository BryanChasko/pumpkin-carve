#!/usr/bin/env python3
"""repo art helpers: ascii pumpkin + brand-framed hero. deterministic."""
import os
from PIL import Image, ImageOps

OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(OUT)

RAMP = "@%#*+=-:. "[::-1]  # dark -> light... we invert below for dark bg


def ascii_art(src, cols=76, rows=38):
    img = Image.open(src).convert("L")
    img = ImageOps.fit(img, (cols, rows), Image.LANCZOS)
    px = img.load()
    lines = []
    for y in range(rows):
        row = "".join(RAMP[min(px[x, y] * len(RAMP) // 256, len(RAMP) - 1)]
                      for x in range(cols))
        lines.append(row.rstrip())
    return "\n".join(lines) + "\n"


def framed_hero(src, dst):
    """brand in-post figure: 6px navy frame + 3px orange keyline."""
    img = Image.open(src).convert("RGB")
    img = ImageOps.expand(img, border=3, fill="#ff9900")
    img = ImageOps.expand(img, border=6, fill="#00002a")
    img.save(dst, "WEBP", quality=85, method=6)


if __name__ == "__main__":
    txt = ascii_art(os.path.join(ROOT, "blender", "exports", "render.png"))
    with open(os.path.join(OUT, "pumpkin.txt"), "w") as f:
        f.write(txt)
    framed_hero(os.path.join(ROOT, "post", "render_post_glow.png"),
                os.path.join(OUT, "pumpkin-framed-978x658.webp"))
    print("wrote pumpkin.txt + pumpkin-framed-978x658.webp")
