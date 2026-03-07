"""Cover generator for Story Atlas reading companions.

Generates cover images for reading companion EPUBs.  When Pillow (PIL) is
available and a base cover image exists the cover is composed by overlaying
dynamic text on top of that image.  Otherwise a self-contained SVG placeholder
is produced so that the generator never fails, even in environments without
image-processing libraries.
"""

import html
import os

# Optional – Pillow is not required.  If it is missing we fall back to SVG.
try:
    from PIL import Image, ImageDraw, ImageFont

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

_FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]

_FONT_PATHS_REGULAR = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]

_FONT_PATHS_ITALIC = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
]


def _find_font(paths, size):
    """Return the first available TTF font at the given size."""
    if not PIL_AVAILABLE:
        return None
    for path in paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except (IOError, OSError):
                continue
    return ImageFont.load_default()


def generate_cover_svg(
    title: str,
    companion_type: str = "Reading Companion",
    lang: str = "EN",
    author: str = "Carlos Bonadeo",
    base_cover_path: str = None,
) -> str:
    """Generate an SVG cover placeholder.

    The SVG is fully self-contained: it uses a dark gradient background,
    decorative borders, and overlaid text.  If *base_cover_path* points to an
    existing image it is referenced as an ``<image>`` element so that readers
    that support embedded images will display it as the background.
    """
    safe_title = html.escape(title)
    safe_author = html.escape(author)
    safe_type = html.escape(companion_type)
    safe_lang = html.escape(lang.upper())

    image_element = ""
    if base_cover_path and os.path.exists(base_cover_path):
        safe_path = html.escape(base_cover_path)
        image_element = (
            f'<image href="{safe_path}" width="600" height="900" x="0" y="0"'
            ' preserveAspectRatio="xMidYMid slice"/>'
        )

    # Wrap long titles across multiple SVG text elements (≤ 20 chars per line).
    words = safe_title.split()
    lines: list = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= 22:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)

    line_height = 46
    title_start_y = 420 - ((len(lines) - 1) * line_height) // 2
    title_elements = "\n".join(
        f'  <text x="300" y="{title_start_y + i * line_height}" '
        'font-family="Georgia, serif" font-size="36" font-weight="bold" '
        f'fill="#ffffff" text-anchor="middle">{line}</text>'
        for i, line in enumerate(lines)
    )

    return f"""<?xml version="1.0" encoding="utf-8"?>
<svg viewBox="0 0 600 900" xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"
     width="600" height="900">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1a2a3a"/>
      <stop offset="100%" stop-color="#0d1520"/>
    </linearGradient>
    <linearGradient id="overlay" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="rgba(0,0,0,0.3)"/>
      <stop offset="100%" stop-color="rgba(0,0,0,0.8)"/>
    </linearGradient>
  </defs>
  <!-- Background -->
  <rect width="600" height="900" fill="url(#bg)"/>
  {image_element}
  <rect width="600" height="900" fill="url(#overlay)"/>
  <!-- Border decoration -->
  <rect x="20" y="20" width="560" height="860" fill="none"
        stroke="#c8a96e" stroke-width="2" rx="4"/>
  <rect x="28" y="28" width="544" height="844" fill="none"
        stroke="#c8a96e" stroke-width="0.5" rx="2"/>
  <!-- Language badge -->
  <rect x="470" y="40" width="90" height="30" fill="#c8a96e" rx="4"/>
  <text x="515" y="60" font-family="Georgia, serif" font-size="16"
        font-weight="bold" fill="#1a2a3a" text-anchor="middle">{safe_lang}</text>
  <!-- Title lines -->
  {title_elements}
  <!-- Companion type -->
  <text x="300" y="{title_start_y + len(lines) * line_height + 30}"
        font-family="Georgia, serif" font-size="22"
        fill="#c8a96e" text-anchor="middle" font-style="italic">{safe_type}</text>
  <!-- Divider -->
  <line x1="100" y1="{title_start_y + len(lines) * line_height + 70}"
        x2="500" y2="{title_start_y + len(lines) * line_height + 70}"
        stroke="#c8a96e" stroke-width="1"/>
  <!-- Author -->
  <text x="300" y="850" font-family="Georgia, serif" font-size="16"
        fill="#c8a96e" text-anchor="middle">{safe_author}</text>
</svg>"""


def _pil_draw_wrapped(draw, text, font, fill, cx, cy, max_width):
    """Draw *text* centred at (*cx*, *cy*), wrapping at *max_width* pixels."""
    words = text.split()
    lines: list = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        try:
            w = draw.textlength(candidate, font=font)
        except AttributeError:
            w = len(candidate) * 12
        if w <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)

    line_height = 44
    total_h = len(lines) * line_height
    start_y = cy - total_h // 2
    for i, line in enumerate(lines):
        draw.text((cx, start_y + i * line_height), line, font=font, fill=fill, anchor="mm")


def _create_pil_cover(
    output_dir: str,
    title: str,
    companion_type: str,
    lang: str,
    author: str,
    base_cover_path: str = None,
) -> str:
    """Create a cover using Pillow and return the filename."""
    width, height = 600, 900
    img = Image.new("RGB", (width, height), color=(26, 42, 58))

    if base_cover_path and os.path.exists(base_cover_path):
        bg = Image.open(base_cover_path).convert("RGB").resize((width, height))
        img.paste(bg)
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 150))
        img = img.convert("RGBA")
        img = Image.alpha_composite(img, overlay).convert("RGB")

    draw = ImageDraw.Draw(img)
    gold = (200, 169, 110)
    white = (255, 255, 255)
    dark = (26, 42, 58)

    title_font = _find_font(_FONT_PATHS, 36)
    subtitle_font = _find_font(_FONT_PATHS_ITALIC, 22)
    footer_font = _find_font(_FONT_PATHS_REGULAR, 16)

    # Borders
    draw.rectangle([20, 20, 579, 879], outline=gold, width=2)

    # Language badge
    draw.rectangle([470, 40, 560, 70], fill=gold)
    draw.text((515, 55), lang.upper(), font=footer_font, fill=dark, anchor="mm")

    # Title
    _pil_draw_wrapped(draw, title, title_font, white, width // 2, 400, width - 80)

    # Companion type
    draw.text((width // 2, 490), companion_type, font=subtitle_font, fill=gold, anchor="mm")

    # Divider
    draw.line([(100, 540), (500, 540)], fill=gold, width=1)

    # Author
    draw.text((width // 2, 850), author, font=footer_font, fill=gold, anchor="mm")

    cover_filename = "cover.jpg"
    img.save(os.path.join(output_dir, cover_filename), "JPEG", quality=90)
    return cover_filename


def create_cover(
    output_dir: str,
    title: str,
    companion_type: str = "Reading Companion",
    lang: str = "en",
    author: str = "Carlos Bonadeo",
    base_cover_path: str = None,
) -> str:
    """Create a cover image for the companion EPUB.

    Tries Pillow first; falls back to an SVG placeholder when Pillow is
    unavailable or the image creation fails for any reason.

    Returns the filename (not the full path) of the generated cover asset.
    """
    os.makedirs(output_dir, exist_ok=True)

    if PIL_AVAILABLE:
        try:
            return _create_pil_cover(
                output_dir, title, companion_type, lang, author, base_cover_path
            )
        except Exception as exc:  # noqa: BLE001
            # Log degraded-mode notice; fall through to SVG
            print(f"  ℹ️  Cover image generation skipped ({exc}); using SVG placeholder.")

    svg_content = generate_cover_svg(
        title, companion_type, lang.upper(), author, base_cover_path
    )
    cover_filename = "cover.svg"
    with open(os.path.join(output_dir, cover_filename), "w", encoding="utf-8") as f:
        f.write(svg_content)
    return cover_filename
