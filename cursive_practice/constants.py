import os
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor

# Page geometry
PAGE_WIDTH, PAGE_HEIGHT = A4  # 595.28, 841.89 pt
TOP_MARGIN = 72      # pt — room for header
BOTTOM_MARGIN = 50   # pt
LEFT_MARGIN = 50     # pt
RIGHT_MARGIN = 40    # pt
USABLE_HEIGHT = PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
USABLE_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN

# Row layout
ROWS_PER_PAGE = 4
ROW_SLOT_HEIGHT = USABLE_HEIGHT / ROWS_PER_PAGE

# 4-line group geometry (3 zones of equal height)
ZONE_HEIGHT = 18     # pt per zone (ascender, x-height, descender)
LINE_GROUP_HEIGHT = ZONE_HEIGHT * 3  # 54pt total


# Font — auto-detect a cursive TTF by platform, or override via CURSIVE_FONT env var
def _find_cursive_font() -> tuple[str, str]:
    """Return (font_path, font_name) for the best available cursive font."""
    env_path = os.environ.get("CURSIVE_FONT")
    if env_path and os.path.isfile(env_path):
        name = os.path.splitext(os.path.basename(env_path))[0]
        return env_path, name

    # Bundled font shipped with the repo (fonts/ directory next to the package)
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    bundled = os.path.join(pkg_dir, os.pardir, "fonts", "DancingScript-Regular.ttf")
    if os.path.isfile(bundled):
        return os.path.abspath(bundled), "DancingScript"

    # Platform-specific system font search
    candidates: list[tuple[str, str]] = []
    if sys.platform == "win32":
        fonts_dir = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
        candidates = [
            (os.path.join(fonts_dir, "MISTRAL.TTF"), "Mistral"),
            (os.path.join(fonts_dir, "FRSCRIPT.TTF"), "FrenchScript"),
            (os.path.join(fonts_dir, "BRUSHSCI.TTF"), "BrushScript"),
        ]
    elif sys.platform == "darwin":
        candidates = [
            ("/Library/Fonts/Brush Script.ttf", "BrushScript"),
            ("/System/Library/Fonts/Supplemental/Brush Script.ttf", "BrushScript"),
            ("/Library/Fonts/Snell Roundhand.ttf", "SnellRoundhand"),
        ]
    else:  # Linux / other
        for fonts_dir in [
            "/usr/share/fonts", "/usr/local/share/fonts",
            os.path.expanduser("~/.local/share/fonts"),
            os.path.expanduser("~/.fonts"),
        ]:
            for root, _dirs, files in os.walk(fonts_dir):
                for f in files:
                    if f.lower().endswith(".ttf") and any(
                        kw in f.lower() for kw in ("cursive", "script", "dancing", "pacifico")
                    ):
                        candidates.append((os.path.join(root, f), os.path.splitext(f)[0]))
                if candidates:
                    break

    for path, name in candidates:
        if os.path.isfile(path):
            return path, name

    raise FileNotFoundError(
        "No cursive font found. Install a cursive TTF font and set the CURSIVE_FONT "
        "environment variable to its path, or place DancingScript-Regular.ttf in the "
        "fonts/ directory. See README.md for details."
    )


CURSIVE_FONT_PATH, CURSIVE_FONT_NAME = _find_cursive_font()
CURSIVE_FONT_SIZE = 28  # base size — auto-scaled down if text overflows
HEADER_FONT = "Helvetica"
HEADER_FONT_SIZE = 11

# Colors
BLUE_LINE = HexColor("#4A90D9")
RED_LINE = HexColor("#D94A4A")
DOTTED_TEXT_COLOR = HexColor("#999999")
HEADER_COLOR = HexColor("#333333")

# Validation
FILLER_WORDS = frozenset({
    "and", "but", "or", "the", "a", "an", "is", "was",
    "are", "were", "be", "been", "being", "so", "yet",
    "for", "nor", "at", "in", "on", "to", "it",
})
MIN_WORDS = 5
MAX_FILLER = 3
