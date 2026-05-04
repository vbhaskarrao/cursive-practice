"""Generate cursive handwriting practice sheets as A4 PDFs."""

from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .constants import (
    BLUE_LINE,
    BOTTOM_MARGIN,
    CURSIVE_FONT_NAME,
    CURSIVE_FONT_PATH,
    CURSIVE_FONT_SIZE,
    DOTTED_TEXT_COLOR,
    HEADER_COLOR,
    HEADER_FONT,
    HEADER_FONT_SIZE,
    LEFT_MARGIN,
    LINE_GROUP_HEIGHT,
    PAGE_HEIGHT,
    PAGE_WIDTH,
    RED_LINE,
    RIGHT_MARGIN,
    ROW_SLOT_HEIGHT,
    ROWS_PER_PAGE,
    TOP_MARGIN,
    USABLE_HEIGHT,
    USABLE_WIDTH,
    ZONE_HEIGHT,
)

_font_registered = False


def _register_fonts():
    """Register the cursive TTF font."""
    global _font_registered
    if _font_registered:
        return
    pdfmetrics.registerFont(TTFont(CURSIVE_FONT_NAME, CURSIVE_FONT_PATH))
    _font_registered = True


def _fit_font_size(sentence: str) -> float:
    """Return the largest font size (up to CURSIVE_FONT_SIZE) that fits the sentence
    within the usable page width."""
    _register_fonts()
    text_width = pdfmetrics.stringWidth(sentence, CURSIVE_FONT_NAME, CURSIVE_FONT_SIZE)
    max_width = USABLE_WIDTH - 10  # 5pt padding on each side
    if text_width <= max_width:
        return CURSIVE_FONT_SIZE
    return CURSIVE_FONT_SIZE * (max_width / text_width)


def _compute_row_positions() -> list[float]:
    """Return the y_top positions for each of the ROWS_PER_PAGE rows on a page.

    y_top is the ReportLab y-coordinate of the ascender (topmost) line in each group.
    Rows are vertically centered within their slot.
    """
    positions = []
    for i in range(ROWS_PER_PAGE):
        slot_top = PAGE_HEIGHT - TOP_MARGIN - i * ROW_SLOT_HEIGHT
        # Center the 4-line group vertically within the slot
        pad = (ROW_SLOT_HEIGHT - LINE_GROUP_HEIGHT) / 2
        y_top = slot_top - pad
        positions.append(y_top)
    return positions


def _draw_header(c: canvas.Canvas, student_name: str, page_num: int):
    """Draw the header bar at the top of the page."""
    c.setFont(HEADER_FONT, HEADER_FONT_SIZE)
    c.setFillColor(HEADER_COLOR)

    today = date.today().strftime("%B %d, %Y")
    left_text = f"Student: {student_name}"
    center_text = f"Date: {today}"
    right_text = f"Page {page_num} / 2"

    y = PAGE_HEIGHT - TOP_MARGIN + 20  # slightly above the top margin

    c.drawString(LEFT_MARGIN, y, left_text)
    c.drawCentredString(PAGE_WIDTH / 2, y, center_text)
    c.drawRightString(PAGE_WIDTH - RIGHT_MARGIN, y, right_text)

    # Thin separator line below header
    sep_y = y - 8
    c.setStrokeColor(HEADER_COLOR)
    c.setLineWidth(0.5)
    c.line(LEFT_MARGIN, sep_y, PAGE_WIDTH - RIGHT_MARGIN, sep_y)


def _draw_line_group(c: canvas.Canvas, y_top: float):
    """Draw one set of 4 ruled lines at the given y_top position."""
    x_start = LEFT_MARGIN
    x_end = PAGE_WIDTH - RIGHT_MARGIN

    # Line 1 — ascender line (blue, solid)
    c.setStrokeColor(BLUE_LINE)
    c.setLineWidth(0.5)
    c.setDash([])  # solid
    c.line(x_start, y_top, x_end, y_top)

    # Line 2 — midline (red, dashed)
    y_mid = y_top - ZONE_HEIGHT
    c.setStrokeColor(RED_LINE)
    c.setLineWidth(0.5)
    c.setDash(3, 3)
    c.line(x_start, y_mid, x_end, y_mid)

    # Line 3 — baseline (red, solid, slightly heavier)
    y_base = y_top - 2 * ZONE_HEIGHT
    c.setStrokeColor(RED_LINE)
    c.setLineWidth(0.75)
    c.setDash([])  # solid
    c.line(x_start, y_base, x_end, y_base)

    # Line 4 — descender line (blue, solid)
    y_desc = y_top - 3 * ZONE_HEIGHT
    c.setStrokeColor(BLUE_LINE)
    c.setLineWidth(0.5)
    c.setDash([])  # solid
    c.line(x_start, y_desc, x_end, y_desc)


def _draw_traced_sentence(c: canvas.Canvas, sentence: str, y_top: float, font_size: float):
    """Draw the sentence in dotted cursive on the baseline of a line group."""
    # The baseline is 2 zones below y_top
    y_baseline = y_top - 2 * ZONE_HEIGHT

    c.saveState()

    # Dotted stroke effect for traceable text
    c.setDash(1, 2)  # 1pt on, 2pt off — fine dots
    c.setLineWidth(0.5)
    c.setStrokeColor(DOTTED_TEXT_COLOR)

    text_obj = c.beginText(LEFT_MARGIN + 5, y_baseline)
    text_obj.setTextRenderMode(1)  # stroke only — no fill
    text_obj.setFont(CURSIVE_FONT_NAME, font_size)
    text_obj.textLine(sentence)
    c.drawText(text_obj)

    c.restoreState()


def generate_practice_sheet(student_name: str, sentence: str, output_path: str) -> str:
    """Create a 2-page A4 cursive practice PDF.

    Page 1: traced example (row 0) + 3 blank ruled rows.
    Page 2: 3 blank ruled rows.
    Total practice opportunities: 1 traced + 6 blank = 7.
    """
    _register_fonts()
    font_size = _fit_font_size(sentence)

    c = canvas.Canvas(output_path, pagesize=A4)
    c.setTitle(f"Cursive Practice — {student_name}")

    row_positions = _compute_row_positions()

    for page in range(2):
        _draw_header(c, student_name, page + 1)

        for i, y_top in enumerate(row_positions):
            _draw_line_group(c, y_top)

            # First row of first page: traced sentence
            if page == 0 and i == 0:
                _draw_traced_sentence(c, sentence, y_top, font_size)

        c.showPage()

    c.save()
    return output_path
