import os
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, black

# Page geometry
PAGE_WIDTH, PAGE_HEIGHT = A4  # 595.28, 841.89 pt
BORDER_MARGIN = 28           # pt — outer border inset from page edge
CONTENT_MARGIN_TOP = 100     # pt — below top border (room for header + title)
CONTENT_MARGIN_BOTTOM = 10   # pt — above bottom border
CONTENT_LEFT = BORDER_MARGIN + 10
CONTENT_RIGHT = PAGE_WIDTH - BORDER_MARGIN - 10
CONTENT_WIDTH = CONTENT_RIGHT - CONTENT_LEFT

# 3-line group geometry (matching the reference image)
#   Top line (solid) — where ascenders reach
#   Middle line (dashed) — x-height / midline
#   Bottom line (solid) — baseline where you write
# Space between lines within a group
LINE_SPACING = 22            # pt between each of the 3 lines
LINE_GROUP_HEIGHT = LINE_SPACING * 2  # top-to-bottom = 44pt

# Number of ruled rows per page
ROWS_PER_PAGE = 7

# Font
CURSIVE_FONT_SIZE = 38       # base size — auto-scaled down if text overflows
HEADER_FONT = "Helvetica"
HEADER_FONT_BOLD = "Helvetica-Bold"
HEADER_FONT_SIZE = 10
TITLE_FONT_SIZE = 20

# Colors — all gray/black like the reference image
LINE_COLOR = HexColor("#555555")       # dark gray ruled lines
LINE_COLOR_DASHED = HexColor("#888888")  # slightly lighter dashed midline
BORDER_COLOR = HexColor("#333333")     # page border
DOT_COLOR = HexColor("#444444")        # dark dots for traceable text
HEADER_COLOR = HexColor("#222222")     # header text
TITLE_BG = HexColor("#333333")         # title banner background

# Dot rendering parameters for the traced text
DOT_DASH_ON = 0.5    # very short "on" segment — appears as a round dot
DOT_DASH_OFF = 2.8   # gap between dots
DOT_LINE_WIDTH = 1.5  # controls dot diameter

# Validation
FILLER_WORDS = frozenset({
    "and", "but", "or", "the", "a", "an", "is", "was",
    "are", "were", "be", "been", "being", "so", "yet",
    "for", "nor", "at", "in", "on", "to", "it",
})
MIN_WORDS = 5
MAX_FILLER = 3


# Font — auto-detect a cursive TTF by platform, or override via CURSIVE_FONT env var
def _find_cursive_font() -> tuple[str, str]:
    """Return (font_path, font_name) for the best available cursive font."""
    env_path = os.environ.get("CURSIVE_FONT")
    if env_path and os.path.isfile(env_path):
        name = os.path.splitext(os.path.basename(env_path))[0]
        return env_path, name

    # Bundled fonts shipped with the repo (fonts/ directory next to the package)
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    fonts_dir = os.path.join(pkg_dir, os.pardir, "fonts")
    bundled_candidates = [
        ("DancingScript.ttf", "DancingScript"),
        ("DancingScript-Regular.ttf", "DancingScript"),
        ("Sacramento-Regular.ttf", "Sacramento"),
        ("GreatVibes-Regular.ttf", "GreatVibes"),
    ]
    for filename, name in bundled_candidates:
        path = os.path.join(fonts_dir, filename)
        if os.path.isfile(path) and os.path.getsize(path) > 1000:
            return os.path.abspath(path), name

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
