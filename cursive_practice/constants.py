import os
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor

# Page geometry
PAGE_WIDTH, PAGE_HEIGHT = A4  # 595.28, 841.89 pt
BORDER_MARGIN = 28           # pt — outer border inset from page edge
CONTENT_MARGIN_TOP = 100     # pt — below top border (room for header + title)
CONTENT_MARGIN_BOTTOM = 10   # pt — above bottom border
CONTENT_LEFT = BORDER_MARGIN + 10
CONTENT_RIGHT = PAGE_WIDTH - BORDER_MARGIN - 10
CONTENT_WIDTH = CONTENT_RIGHT - CONTENT_LEFT

# 3-line group geometry (matching the reference image)
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
LINE_COLOR = HexColor("#555555")
LINE_COLOR_DASHED = HexColor("#888888")
BORDER_COLOR = HexColor("#333333")
DOT_COLOR = HexColor("#444444")
HEADER_COLOR = HexColor("#222222")
TITLE_BG = HexColor("#333333")

# Dot rendering parameters for the traced text
DOT_DASH_ON = 0.5
DOT_DASH_OFF = 2.8
DOT_LINE_WIDTH = 1.5

# Validation
FILLER_WORDS = frozenset({
    "and", "but", "or", "the", "a", "an", "is", "was",
    "are", "were", "be", "been", "being", "so", "yet",
    "for", "nor", "at", "in", "on", "to", "it",
})
MIN_WORDS = 5
MAX_FILLER = 3


# ---------------------------------------------------------------------------
# Font discovery — find ALL available cursive fonts so the user can choose
# ---------------------------------------------------------------------------

def discover_fonts() -> list[tuple[str, str]]:
    """Return a list of (font_path, display_name) for every usable cursive font.

    Checks bundled fonts first, then system fonts. Skips files < 1KB (bad downloads).
    """
    found: list[tuple[str, str]] = []
    seen_names: set[str] = set()

    def _add(path: str, display_name: str):
        if display_name not in seen_names and os.path.isfile(path) and os.path.getsize(path) > 1000:
            found.append((os.path.abspath(path), display_name))
            seen_names.add(display_name)

    # 1. CURSIVE_FONT env var
    env_path = os.environ.get("CURSIVE_FONT")
    if env_path and os.path.isfile(env_path):
        name = os.path.splitext(os.path.basename(env_path))[0]
        _add(env_path, name)

    # 2. Bundled fonts (fonts/ directory next to the package)
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    bundled_dir = os.path.abspath(os.path.join(pkg_dir, os.pardir, "fonts"))
    bundled = [
        ("DancingScript.ttf", "Dancing Script"),
        ("DancingScript-Regular.ttf", "Dancing Script"),
        ("Sacramento-Regular.ttf", "Sacramento"),
        ("GreatVibes-Regular.ttf", "Great Vibes"),
        ("EduNSWACTFoundation.ttf", "Edu NSW Foundation"),
        ("EduQLDBeginner.ttf", "Edu QLD Beginner"),
        ("EduSABeginner.ttf", "Edu SA Beginner"),
        ("EduTASBeginner.ttf", "Edu TAS Beginner"),
        ("EduVICWANTBeginner.ttf", "Edu VIC Beginner"),
    ]
    for filename, display in bundled:
        _add(os.path.join(bundled_dir, filename), display)

    # 3. Platform system fonts
    if sys.platform == "win32":
        sys_fonts_dir = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
        for filename, display in [
            ("MISTRAL.TTF", "Mistral"),
            ("FRSCRIPT.TTF", "French Script"),
            ("BRUSHSCI.TTF", "Brush Script"),
            ("LHANDW.TTF", "Lucida Handwriting"),
            ("Inkfree.ttf", "Ink Free"),
        ]:
            _add(os.path.join(sys_fonts_dir, filename), display)
    elif sys.platform == "darwin":
        for path, display in [
            ("/Library/Fonts/Brush Script.ttf", "Brush Script"),
            ("/System/Library/Fonts/Supplemental/Brush Script.ttf", "Brush Script"),
            ("/Library/Fonts/Snell Roundhand.ttf", "Snell Roundhand"),
        ]:
            _add(path, display)
    else:
        for search_dir in [
            "/usr/share/fonts", "/usr/local/share/fonts",
            os.path.expanduser("~/.local/share/fonts"),
            os.path.expanduser("~/.fonts"),
        ]:
            if not os.path.isdir(search_dir):
                continue
            for root, _dirs, files in os.walk(search_dir):
                for f in files:
                    if f.lower().endswith(".ttf") and any(
                        kw in f.lower()
                        for kw in ("cursive", "script", "dancing", "pacifico", "sacramento")
                    ):
                        display = os.path.splitext(f)[0]
                        _add(os.path.join(root, f), display)

    if not found:
        raise FileNotFoundError(
            "No cursive font found. See README.md for font setup instructions."
        )

    return found
