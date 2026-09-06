#!/usr/bin/env python3
"""Convert cover images in assets/images/ to web-sized WebP.

Cover images render at most ~1050px wide (a post hero at --measure); 1600px
keeps a retina buffer. Source PNG/JPEG files are left in place — delete them
once the posts point at the .webp versions.

Setup:  python3 -m venv .venv && .venv/bin/pip install Pillow
Run:    .venv/bin/python script/to-webp.py
"""
from pathlib import Path
from PIL import Image

MAX_WIDTH = 1600
QUALITY = 80
IMAGE_DIR = Path(__file__).resolve().parent.parent / "assets" / "images"

before = after = 0
for src in sorted(p for p in IMAGE_DIR.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg"}):
    im = Image.open(src)
    if im.mode in ("RGBA", "P", "LA"):
        im = im.convert("RGB")
    w, h = im.size
    if w > MAX_WIDTH:
        im = im.resize((MAX_WIDTH, round(h * MAX_WIDTH / w)), Image.LANCZOS)
    dst = src.with_suffix(".webp")
    im.save(dst, "WEBP", quality=QUALITY, method=6)
    before += src.stat().st_size
    after += dst.stat().st_size
    print(f"{src.name:<46} {w}x{h} {src.stat().st_size/1024:>7.0f} KB  ->  "
          f"{dst.name:<46} {im.size[0]}x{im.size[1]} {dst.stat().st_size/1024:>6.0f} KB")

if before:
    print(f"\ntotal  {before/1024/1024:.1f} MB  ->  {after/1024:.0f} KB  ({100*after/before:.1f}%)")
