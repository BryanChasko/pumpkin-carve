#!/usr/bin/env python3
"""strip panels for the readme header: one size, brand finish.

left  = graded render, center-cropped, navy vignette + ben-day dots
right = ascii pumpkin rendered as an image (dejavu sans mono)
center panel is the animated webp, already 480x320.
brand: ~/writing/BRAND.md - navy #0F141C, lavender dots, webp out.
"""
import hashlib
import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
W, H = 480, 320
NAVY = (15, 20, 28)
LAV = (215, 199, 238)


def vignette(img, feather=28):
    """linear edge-distance fade into house navy."""
    px = img.load()
    out = Image.new("RGB", img.size, NAVY)
    op = out.load()
    w, h = img.size
    for y in range(h):
        dy = min(y, h - 1 - y)
        for x in range(w):
            d = min(min(x, w - 1 - x), dy)
            t = min(d / feather, 1.0) if feather else 1.0
            r, g, b = px[x, y][:3]
            op[x, y] = (int(r * t + NAVY[0] * (1 - t)),
                        int(g * t + NAVY[1] * (1 - t)),
                        int(b * t + NAVY[2] * (1 - t)))
    return out


def ben_day(img, spacing=12, r=2, alpha=36):
    """lavender dots, alpha ~14%, never over the outer 12px seam."""
    dots = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(dots)
    w, h = img.size
    for y in range(12 + spacing // 2, h - 12, spacing):
        for x in range(12 + spacing // 2, w - 12, spacing):
            d.ellipse([x - r, y - r, x + r, y + r],
                      fill=LAV + (alpha,))
    return Image.alpha_composite(img.convert("RGBA"), dots)


def sidecar(path, note):
    data = open(path, "rb").read()
    meta = {"source": os.path.basename(path),
            "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data), "tool": "PIL 12.2 / make_strips.py",
            "note": note}
    with open(path + ".sidecar.json", "w") as f:
        json.dump(meta, f, indent=1)


def left_panel():
    src = os.path.join(ROOT, "post", "render_post_glow.png")
    img = Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS)
    img = ben_day(vignette(img))
    out = os.path.join(HERE, "strip-render-480x320.webp")
    img.convert("RGB").save(out, "WEBP", quality=85, method=6)
    sidecar(out, "graded render, navy vignette, ben-day dots")


def right_panel():
    import sys
    sys.path.insert(0, HERE)
    from make_art import ascii_art
    txt = ascii_art(os.path.join(ROOT, "blender", "exports", "render.png"),
                    cols=62, rows=24)
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 11)
    tw = d.textlength(txt.splitlines()[0], font=font)
    d.multiline_text(((W - tw) / 2, 4), txt, font=font, fill=LAV, spacing=0)
    img = ben_day(img.convert("RGBA")).convert("RGB")
    out = os.path.join(HERE, "strip-ascii-480x320.webp")
    img.save(out, "WEBP", lossless=True, method=6)
    sidecar(out, "ascii pumpkin, dejavu sans mono 12, lavender on navy")


if __name__ == "__main__":
    left_panel()
    right_panel()
    print("wrote strip-render + strip-ascii (480x320)")
