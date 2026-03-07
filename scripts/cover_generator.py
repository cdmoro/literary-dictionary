"""Cover generator for Story Atlas reading companions.

Generates cover images for reading companion EPUBs.  When Pillow (PIL) is
available and a base cover image exists the cover is composed by overlaying
dynamic text on top of that image.  Otherwise a self-contained SVG is
produced so that the generator never fails, even in environments without
image-processing libraries.

Cover layout (matching the reference design):
::

    ┌─────────────────────────┐
    │                         │
    │                         │
    │         [Title]         │  ← gold serif, large, centred in upper area
    │                         │
    │                         │
    │   ─────────────────     │  ← thin gold horizontal rule
    │                         │
    │   [Reading Companion]   │  ← translated, muted colour, smaller
    │         [LANG]          │  ← language code, muted, small
    │                         │
    │                         │
    │   [Created by] Author   │  ← translated label + author, bottom
    └─────────────────────────┘
"""

import html
import os

# Optional – Pillow is not required.  If it is missing we fall back to SVG.
try:
    from PIL import Image, ImageDraw, ImageFont

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

_FONT_PATHS_BOLD = [
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


# ---------------------------------------------------------------------------
# Colour palette (matches the reference image)
# ---------------------------------------------------------------------------
_BG_COLOUR = "#1c2e42"          # dark navy blue
_BORDER_COLOUR = "#8a9bb0"      # muted steel-blue border
_TITLE_COLOUR = "#c8a96e"       # warm gold
_SUBTITLE_COLOUR = "#8a9bb0"    # muted blue-grey (Reading Companion + LANG)
_FOOTER_COLOUR = "#8a9bb0"      # same muted colour for "Created by …"
_RULE_COLOUR = "#8a9bb0"        # divider line


def _hex_to_rgb(hex_colour: str) -> tuple:
    """Convert a CSS hex colour string to an ``(R, G, B)`` tuple."""
    h = hex_colour.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def _find_font(paths, size):
    """Return the first available TTF font at the given size, or default."""
    if not PIL_AVAILABLE:
        return None
    for path in paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except (IOError, OSError):
                continue
    return ImageFont.load_default()


def _wrap_text_svg(text: str, max_chars: int = 20) -> list:
    """Split *text* into lines of at most *max_chars* characters."""
    words = text.split()
    lines: list = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def generate_cover_svg(
    title: str,
    companion_label: str = "Reading Companion",
    lang_label: str = "EN",
    created_by_label: str = "Created by",
    author: str = "Carlos Bonadeo",
    base_cover_path: str = None,
) -> str:
    """Generate an SVG cover that matches the reference design.

    When *base_cover_path* points to an existing image it is referenced as an
    ``<image>`` element so that readers that support embedded images will show
    it as the background.  Without a background image a flat solid fill is used
    (matching the "generic" variant in the reference).
    """
    safe_title = html.escape(title)
    safe_companion = html.escape(companion_label)
    safe_lang = html.escape(lang_label.upper())
    safe_created = html.escape(f"{created_by_label} {author}")

    # --- background image (optional) ---
    image_element = ""
    if base_cover_path and os.path.exists(base_cover_path):
        safe_path = html.escape(base_cover_path)
        image_element = (
            f'<image href="{safe_path}" width="600" height="900" x="0" y="0"'
            ' preserveAspectRatio="xMidYMid slice" opacity="0.35"/>'
        )

    # --- title: wrapped, centred in upper ~55 % of the card ---
    title_lines = _wrap_text_svg(safe_title, max_chars=20)
    line_height_px = 54
    title_block_h = len(title_lines) * line_height_px
    title_center_y = 320  # vertical centre of the title block
    title_start_y = title_center_y - title_block_h // 2 + line_height_px // 2

    title_elements = "\n  ".join(
        f'<text x="300" y="{title_start_y + i * line_height_px}" '
        f'font-family="Georgia, \'Times New Roman\', serif" font-size="48" '
        f'font-weight="normal" fill="{_TITLE_COLOUR}" text-anchor="middle">'
        f"{line}</text>"
        for i, line in enumerate(title_lines)
    )

    # --- rule Y position: just below title block ---
    rule_y = title_center_y + title_block_h // 2 + 50

    # --- companion label and lang label below rule ---
    companion_y = rule_y + 48
    lang_y = companion_y + 38

    return f"""<?xml version="1.0" encoding="utf-8"?>
<svg viewBox="0 0 600 900" xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"
     width="600" height="900">
  <!-- Solid background -->
  <rect width="600" height="900" fill="{_BG_COLOUR}"/>
  {image_element}
  <!-- Border -->
  <rect x="24" y="24" width="552" height="852" fill="none"
        stroke="{_BORDER_COLOUR}" stroke-width="1.5" rx="2"/>
  <!-- Title -->
  {title_elements}
  <!-- Horizontal rule -->
  <line x1="80" y1="{rule_y}" x2="520" y2="{rule_y}"
        stroke="{_RULE_COLOUR}" stroke-width="1"/>
  <!-- Reading Companion label -->
  <text x="300" y="{companion_y}"
        font-family="Georgia, 'Times New Roman', serif" font-size="22"
        font-weight="normal" fill="{_SUBTITLE_COLOUR}" text-anchor="middle"
        letter-spacing="1">{safe_companion}</text>
  <!-- Language -->
  <text x="300" y="{lang_y}"
        font-family="Georgia, 'Times New Roman', serif" font-size="16"
        fill="{_SUBTITLE_COLOUR}" text-anchor="middle"
        letter-spacing="2">{safe_lang}</text>
  <!-- Created-by footer -->
  <text x="300" y="855"
        font-family="Georgia, 'Times New Roman', serif" font-size="15"
        fill="{_FOOTER_COLOUR}" text-anchor="middle">{safe_created}</text>
</svg>"""


# ---------------------------------------------------------------------------
# Pillow path
# ---------------------------------------------------------------------------


def _pil_draw_wrapped(draw, text, font, fill, cx, cy_centre, max_width):
    """Draw *text* centred at *cy_centre*, wrapping at *max_width* pixels."""
    words = text.split()
    lines: list = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        try:
            w = draw.textlength(candidate, font=font)
        except AttributeError:
            w = len(candidate) * 14
        if w <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)

    line_h = 56
    start_y = cy_centre - (len(lines) * line_h) // 2
    for i, line in enumerate(lines):
        draw.text(
            (cx, start_y + i * line_h),
            line,
            font=font,
            fill=fill,
            anchor="mm",
        )
    return len(lines) * line_h  # return actual block height


def _create_pil_cover(
    output_dir: str,
    title: str,
    companion_label: str,
    lang_label: str,
    created_by_label: str,
    author: str,
    base_cover_path: str = None,
) -> str:
    """Create a JPEG cover using Pillow, matching the reference design."""
    width, height = 600, 900
    bg_rgb = _hex_to_rgb(_BG_COLOUR)
    img = Image.new("RGB", (width, height), color=bg_rgb)

    if base_cover_path and os.path.exists(base_cover_path):
        bg = Image.open(base_cover_path).convert("RGB").resize((width, height))
        overlay = Image.new("RGBA", (width, height), (*bg_rgb, 180))
        bg_rgba = bg.convert("RGBA")
        img = Image.alpha_composite(bg_rgba, overlay).convert("RGB")

    draw = ImageDraw.Draw(img)

    border_col = _hex_to_rgb(_BORDER_COLOUR)
    title_col = _hex_to_rgb(_TITLE_COLOUR)
    muted_col = _hex_to_rgb(_SUBTITLE_COLOUR)

    title_font = _find_font(_FONT_PATHS_BOLD, 48)
    label_font = _find_font(_FONT_PATHS_REGULAR, 22)
    small_font = _find_font(_FONT_PATHS_REGULAR, 16)
    footer_font = _find_font(_FONT_PATHS_REGULAR, 15)

    # Border
    draw.rectangle([24, 24, 575, 875], outline=border_col, width=2)

    # Title block centred in upper 55 % of the image
    title_block_h = _pil_draw_wrapped(
        draw, title, title_font, title_col, width // 2, 310, width - 100
    )

    rule_y = 310 + title_block_h // 2 + 50
    companion_y = rule_y + 48
    lang_y = companion_y + 42

    # Horizontal rule
    draw.line([(80, rule_y), (520, rule_y)], fill=muted_col, width=1)

    # Companion label
    draw.text(
        (width // 2, companion_y), companion_label, font=label_font,
        fill=muted_col, anchor="mm",
    )

    # Language code
    draw.text(
        (width // 2, lang_y), lang_label.upper(), font=small_font,
        fill=muted_col, anchor="mm",
    )

    # Footer
    footer_text = f"{created_by_label} {author}"
    draw.text(
        (width // 2, 855), footer_text, font=footer_font,
        fill=muted_col, anchor="mm",
    )

    cover_filename = "cover.jpg"
    img.save(os.path.join(output_dir, cover_filename), "JPEG", quality=90)
    return cover_filename


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def create_cover(
    output_dir: str,
    title: str,
    lang: str = "en",
    companion_label: str = "Reading Companion",
    lang_label: str = None,
    created_by_label: str = "Created by",
    author: str = "Carlos Bonadeo",
    base_cover_path: str = None,
) -> str:
    """Create a cover image for a companion EPUB.

    Args:
        output_dir:        Directory where the cover file is written.
        title:             Book or saga title.
        lang:              Language code (e.g. ``'en'``).
        companion_label:   Translated "Reading Companion" string.
        lang_label:        Language display label shown on the cover (e.g.
                           ``"EN"``, ``"ES"``).  When ``None`` (the default),
                           *lang* uppercased is used.
        created_by_label:  Translated "Created by" label.
        author:            Author name (appears after *created_by_label*).
        base_cover_path:   Optional path to a base/background image for
                           image-composite covers.  Pass ``None`` for a flat
                           colour background.

    Returns:
        Filename (not full path) of the generated cover asset.
    """
    resolved_lang_label = lang_label if lang_label is not None else lang.upper()
    os.makedirs(output_dir, exist_ok=True)

    if PIL_AVAILABLE:
        try:
            return _create_pil_cover(
                output_dir,
                title,
                companion_label,
                resolved_lang_label,
                created_by_label,
                author,
                base_cover_path,
            )
        except Exception as exc:  # noqa: BLE001
            print(f"  ℹ️  Cover image generation skipped ({exc}); using SVG.")

    svg_content = generate_cover_svg(
        title,
        companion_label,
        resolved_lang_label,
        created_by_label,
        author,
        base_cover_path,
    )
    cover_filename = "cover.svg"
    with open(os.path.join(output_dir, cover_filename), "w", encoding="utf-8") as fh:
        fh.write(svg_content)
    return cover_filename

