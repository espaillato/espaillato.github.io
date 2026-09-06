#!/usr/bin/env python3
"""Generate Open Graph share images (1200x630 JPEG) into assets/og/.

LinkedIn/Facebook/Slack need an absolute JPEG or PNG og:image and are
unreliable with WebP, so these are separate from the on-page .webp covers.

  - assets/og/default.jpg        branded card, used for the home page and
                                 any page without its own cover
  - assets/og/<cover-name>.jpg   one per post cover, centre-cropped to 1200x630

Setup:  python3 -m venv .venv && .venv/bin/pip install Pillow
Run:    .venv/bin/python script/og-images.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "images"
OUT = ROOT / "assets" / "og"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1200, 630
BG = (250, 248, 243)
INK = (31, 28, 25)
MUTED = (107, 101, 92)
ACCENT = (138, 43, 31)
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

TITLE = "Field Notes"
TAGLINE = "Working notes on building small, durable personal systems."


def cover_crop(src: Path, dst: Path) -> None:
    im = Image.open(src).convert("RGB")
    scale = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left = (im.width - W) // 2
    top = (im.height - H) // 2
    im.crop((left, top, left + W, top + H)).save(dst, "JPEG", quality=86, optimize=True)


def branded_card(dst: Path) -> None:
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    x = 96

    # mark: two overlapping squares, echoing the site wordmark
    d.rounded_rectangle([x, 96, x + 46, 142], radius=9, outline=ACCENT, width=4)
    d.rounded_rectangle([x + 18, 114, x + 64, 160], radius=9, outline=ACCENT, width=4, fill=BG)
    d.rounded_rectangle([x + 18, 114, x + 64, 160], radius=9, outline=ACCENT, width=4)

    d.text((x, 214), TITLE, font=ImageFont.truetype(SERIF_BOLD, 116), fill=INK)
    d.line([x + 3, 360, x + 123, 360], fill=ACCENT, width=3)

    font_tag = ImageFont.truetype(SANS, 34)
    words, line, y = TAGLINE.split(), "", 398
    for w in words:
        trial = f"{line} {w}".strip()
        if d.textlength(trial, font=font_tag) > W - x - 96:
            d.text((x, y), line, font=font_tag, fill=MUTED)
            line, y = w, y + 46
        else:
            line = trial
    d.text((x, y), line, font=font_tag, fill=MUTED)

    im.save(dst, "JPEG", quality=90, optimize=True)


branded_card(OUT / "default.jpg")
print(f"default.jpg  {(OUT / 'default.jpg').stat().st_size // 1024} KB")
for src in sorted(SRC.glob("*.webp")):
    dst = OUT / (src.stem + ".jpg")
    cover_crop(src, dst)
    print(f"{dst.name:<46} {dst.stat().st_size // 1024} KB")
