"""Generate cursive handwriting practice sheets as A4 PDFs.

Visual style matches the classic dotted-letter cursive practice worksheet:
- 3-line ruled groups (solid top, dashed middle, solid bottom) in dark gray
- Round-dotted letter outlines for tracing
- Page border, header with Name/Date fields, bold title banner
"""

import os
import subprocess
import sys
from datetime import date

from reportlab.lib.colors import white
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .constants import (
    BORDER_COLOR,
    BORDER_MARGIN,
    CONTENT_LEFT,
    CONTENT_MARGIN_BOTTOM,
    CONTENT_MARGIN_TOP,
    CONTENT_RIGHT,
    CONTENT_WIDTH,
    CURSIVE_FONT_SIZE,
    DOT_COLOR,
    DOT_DASH_OFF,
    DOT_DASH_ON,
    DOT_LINE_WIDTH,
    HEADER_COLOR,
    HEADER_FONT,
    HEADER_FONT_BOLD,
    HEADER_FONT_SIZE,
    LINE_COLOR,
    LINE_COLOR_DASHED,
    LINE_GROUP_HEIGHT,
    LINE_SPACING,
    PAGE_HEIGHT,
    PAGE_WIDTH,
    ROWS_PER_PAGE,
    TITLE_BG,
    TITLE_FONT_SIZE,
)

_registered_fonts: set[str] = set()


def _ensure_font(font_path: str, font_name: str):
    """Register a TTF font if not already registered."""
    if font_name not in _registered_fonts:
        pdfmetrics.registerFont(TTFont(font_name, font_path))
        _registered_fonts.add(font_name)


def _fit_font_size(sentence: str, font_name: str) -> float:
    """Return the largest font size (up to CURSIVE_FONT_SIZE) that fits the sentence."""
    text_width = pdfmetrics.stringWidth(sentence, font_name, CURSIVE_FONT_SIZE)
    max_width = CONTENT_WIDTH - 20
    if text_width <= max_width:
        return CURSIVE_FONT_SIZE
    return CURSIVE_FONT_SIZE * (max_width / text_width)


def _draw_border(c: canvas.Canvas):
    """Draw a rectangular border around the page content area."""
    c.setStrokeColor(BORDER_COLOR)
    c.setLineWidth(1.5)
    c.setDash([])
    c.rect(
        BORDER_MARGIN, BORDER_MARGIN,
        PAGE_WIDTH - 2 * BORDER_MARGIN,
        PAGE_HEIGHT - 2 * BORDER_MARGIN,
    )


def _draw_header(c: canvas.Canvas, student_name: str, page_num: int):
    """Draw the header: Name ___, Date ___, title banner, subtitle."""
    x_left = CONTENT_LEFT
    x_right = CONTENT_RIGHT
    y_top = PAGE_HEIGHT - BORDER_MARGIN - 18

    c.setFont(HEADER_FONT, HEADER_FONT_SIZE)
    c.setFillColor(HEADER_COLOR)

    # Name + underline
    c.drawString(x_left, y_top, "Name")
    name_lw = pdfmetrics.stringWidth("Name ", HEADER_FONT, HEADER_FONT_SIZE)
    name_start = x_left + name_lw
    name_end = x_left + CONTENT_WIDTH * 0.52
    c.drawString(name_start + 4, y_top, student_name)
    c.setStrokeColor(HEADER_COLOR)
    c.setLineWidth(0.5)
    c.setDash([])
    c.line(name_start, y_top - 2, name_end, y_top - 2)

    # Date + underline
    date_x = x_left + CONTENT_WIDTH * 0.58
    today = date.today().strftime("%B %d, %Y")
    c.drawString(date_x, y_top, "Date")
    date_lw = pdfmetrics.stringWidth("Date ", HEADER_FONT, HEADER_FONT_SIZE)
    date_start = date_x + date_lw
    c.drawString(date_start + 4, y_top, today)
    c.line(date_start, y_top - 2, x_right, y_top - 2)

    # Title banner
    banner_h, banner_y = 28, y_top - 38
    banner_x, banner_w = PAGE_WIDTH / 2 - 130, 260
    c.setFillColor(TITLE_BG)
    c.roundRect(banner_x, banner_y, banner_w, banner_h, 4, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont(HEADER_FONT_BOLD, TITLE_FONT_SIZE)
    c.drawCentredString(PAGE_WIDTH / 2, banner_y + 7, "CURSIVE PRACTICE")

    # Subtitle
    c.setFillColor(HEADER_COLOR)
    c.setFont(HEADER_FONT, 9)
    c.drawCentredString(PAGE_WIDTH / 2, banner_y - 14, "Trace the sentence below!")

    # Page number
    c.setFont(HEADER_FONT, 8)
    c.drawRightString(x_right, BORDER_MARGIN + 8, f"Page {page_num} / 2")


def _compute_row_positions() -> list[float]:
    """Return y_top positions for each 3-line group on a page."""
    top_start = PAGE_HEIGHT - CONTENT_MARGIN_TOP - BORDER_MARGIN
    bottom_limit = BORDER_MARGIN + CONTENT_MARGIN_BOTTOM + 20
    usable = top_start - bottom_limit
    row_slot = usable / ROWS_PER_PAGE
    positions = []
    for i in range(ROWS_PER_PAGE):
        slot_top = top_start - i * row_slot
        pad = (row_slot - LINE_GROUP_HEIGHT) / 2
        positions.append(slot_top - pad)
    return positions


def _draw_line_group(c: canvas.Canvas, y_top: float):
    """Draw a 3-line ruled group: solid top, dashed middle, solid bottom."""
    x_start, x_end = CONTENT_LEFT, CONTENT_RIGHT

    # Top — solid
    c.setStrokeColor(LINE_COLOR)
    c.setLineWidth(0.75)
    c.setDash([])
    c.line(x_start, y_top, x_end, y_top)

    # Middle — dashed
    y_mid = y_top - LINE_SPACING
    c.setStrokeColor(LINE_COLOR_DASHED)
    c.setLineWidth(0.5)
    c.setDash(6, 4)
    c.line(x_start, y_mid, x_end, y_mid)

    # Bottom — solid
    y_bottom = y_top - 2 * LINE_SPACING
    c.setStrokeColor(LINE_COLOR)
    c.setLineWidth(0.75)
    c.setDash([])
    c.line(x_start, y_bottom, x_end, y_bottom)


def _draw_traced_sentence(c: canvas.Canvas, sentence: str, y_top: float,
                          font_name: str, font_size: float):
    """Draw the sentence as round-dotted letter outlines for tracing."""
    y_baseline = y_top - 2 * LINE_SPACING
    c.saveState()
    c.setLineCap(1)  # round cap — tiny dashes become round dots
    c.setDash(DOT_DASH_ON, DOT_DASH_OFF)
    c.setLineWidth(DOT_LINE_WIDTH)
    c.setStrokeColor(DOT_COLOR)
    text_obj = c.beginText(CONTENT_LEFT + 8, y_baseline)
    text_obj.setTextRenderMode(1)  # stroke only
    text_obj.setFont(font_name, font_size)
    text_obj.textLine(sentence)
    c.drawText(text_obj)
    c.restoreState()


# ---------------------------------------------------------------------------
# Font sampler — generates a PDF showing every available font for user to pick
# ---------------------------------------------------------------------------

def generate_font_sampler(fonts: list[tuple[str, str]], output_path: str) -> str:
    """Create a PDF showing each font with sample text on ruled lines.

    Args:
        fonts: list of (font_path, display_name) tuples.
        output_path: where to save the PDF.

    Returns the output_path.
    """
    sample_letters = "Aa Bb Cc Dd Ee Ff Gg"
    sample_sentence = "Quick brown fox jumped over lazy dogs"

    c = canvas.Canvas(output_path, pagesize=A4)
    c.setTitle("Cursive Font Sampler")

    y = PAGE_HEIGHT - 50

    # Title
    c.setFont(HEADER_FONT_BOLD, 16)
    c.setFillColor(HEADER_COLOR)
    c.drawCentredString(PAGE_WIDTH / 2, y, "Choose Your Cursive Style")
    y -= 22
    c.setFont(HEADER_FONT, 10)
    c.drawCentredString(PAGE_WIDTH / 2, y, "Review each font below and pick the number that best matches your preference.")
    y -= 30

    for idx, (font_path, display_name) in enumerate(fonts):
        # Register the font
        reg_name = display_name.replace(" ", "")
        try:
            _ensure_font(font_path, reg_name)
        except Exception:
            continue

        # Check if we need a new page
        if y < 130:
            c.showPage()
            y = PAGE_HEIGHT - 50

        # Font label with number
        c.setFont(HEADER_FONT_BOLD, 11)
        c.setFillColor(HEADER_COLOR)
        c.drawString(CONTENT_LEFT, y, f"{idx + 1}.  {display_name}")
        y -= 18

        # --- Row 1: alphabet sample ---
        top1 = y
        mid1 = y - LINE_SPACING
        bot1 = y - 2 * LINE_SPACING

        # Draw 3-line group
        c.setStrokeColor(LINE_COLOR)
        c.setLineWidth(0.75)
        c.setDash([])
        c.line(CONTENT_LEFT, top1, CONTENT_RIGHT, top1)
        c.setStrokeColor(LINE_COLOR_DASHED)
        c.setLineWidth(0.5)
        c.setDash(6, 4)
        c.line(CONTENT_LEFT, mid1, CONTENT_RIGHT, mid1)
        c.setStrokeColor(LINE_COLOR)
        c.setLineWidth(0.75)
        c.setDash([])
        c.line(CONTENT_LEFT, bot1, CONTENT_RIGHT, bot1)

        # Dotted text — alphabet
        c.saveState()
        c.setLineCap(1)
        c.setDash(DOT_DASH_ON, DOT_DASH_OFF)
        c.setLineWidth(DOT_LINE_WIDTH)
        c.setStrokeColor(DOT_COLOR)
        txt = c.beginText(CONTENT_LEFT + 8, bot1)
        txt.setTextRenderMode(1)
        size = _fit_font_size_raw(sample_letters, reg_name, 36)
        txt.setFont(reg_name, size)
        txt.textLine(sample_letters)
        c.drawText(txt)
        c.restoreState()

        y = bot1 - 10

        # --- Row 2: sentence sample ---
        top2 = y
        mid2 = y - LINE_SPACING
        bot2 = y - 2 * LINE_SPACING

        c.setStrokeColor(LINE_COLOR)
        c.setLineWidth(0.75)
        c.setDash([])
        c.line(CONTENT_LEFT, top2, CONTENT_RIGHT, top2)
        c.setStrokeColor(LINE_COLOR_DASHED)
        c.setLineWidth(0.5)
        c.setDash(6, 4)
        c.line(CONTENT_LEFT, mid2, CONTENT_RIGHT, mid2)
        c.setStrokeColor(LINE_COLOR)
        c.setLineWidth(0.75)
        c.setDash([])
        c.line(CONTENT_LEFT, bot2, CONTENT_RIGHT, bot2)

        # Dotted text — sentence
        c.saveState()
        c.setLineCap(1)
        c.setDash(DOT_DASH_ON, DOT_DASH_OFF)
        c.setLineWidth(DOT_LINE_WIDTH)
        c.setStrokeColor(DOT_COLOR)
        txt = c.beginText(CONTENT_LEFT + 8, bot2)
        txt.setTextRenderMode(1)
        size = _fit_font_size_raw(sample_sentence, reg_name, 30)
        txt.setFont(reg_name, size)
        txt.textLine(sample_sentence)
        c.drawText(txt)
        c.restoreState()

        y = bot2 - 25

    c.save()
    return output_path


def _fit_font_size_raw(text: str, font_name: str, max_size: float) -> float:
    """Scale font to fit text within CONTENT_WIDTH."""
    w = pdfmetrics.stringWidth(text, font_name, max_size)
    max_w = CONTENT_WIDTH - 20
    if w <= max_w:
        return max_size
    return max_size * (max_w / w)


# ---------------------------------------------------------------------------
# Practice sheet generator
# ---------------------------------------------------------------------------

def generate_practice_sheet(student_name: str, sentence: str, output_path: str,
                            font_path: str, font_display_name: str) -> str:
    """Create a 2-page A4 cursive practice PDF.

    Page 1: traced example (row 0) + remaining blank ruled rows.
    Page 2: all blank ruled rows.
    """
    font_name = font_display_name.replace(" ", "")
    _ensure_font(font_path, font_name)
    font_size = _fit_font_size(sentence, font_name)

    c = canvas.Canvas(output_path, pagesize=A4)
    c.setTitle(f"Cursive Practice — {student_name}")

    row_positions = _compute_row_positions()

    for page in range(2):
        _draw_border(c)
        _draw_header(c, student_name, page + 1)

        for i, y_top in enumerate(row_positions):
            _draw_line_group(c, y_top)
            if page == 0 and i == 0:
                _draw_traced_sentence(c, sentence, y_top, font_name, font_size)

        c.showPage()

    c.save()
    return output_path


def open_pdf(path: str):
    """Open a PDF in the system's default viewer."""
    if sys.platform == "win32":
        os.startfile(path)
    elif sys.platform == "darwin":
        subprocess.run(["open", path], check=False)
    else:
        subprocess.run(["xdg-open", path], check=False)
