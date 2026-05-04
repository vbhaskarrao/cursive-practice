"""Generate cursive handwriting practice sheets as A4 PDFs.

Visual style matches the classic dotted-letter cursive practice worksheet:
- 3-line ruled groups (solid top, dashed middle, solid bottom) in dark gray
- Round-dotted letter outlines for tracing
- Page border, header with Name/Date fields, bold title banner
"""

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
    CURSIVE_FONT_NAME,
    CURSIVE_FONT_PATH,
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

_font_registered = False


def _register_fonts():
    """Register the cursive TTF font."""
    global _font_registered
    if _font_registered:
        return
    pdfmetrics.registerFont(TTFont(CURSIVE_FONT_NAME, CURSIVE_FONT_PATH))
    _font_registered = True


def _fit_font_size(sentence: str) -> float:
    """Return the largest font size (up to CURSIVE_FONT_SIZE) that fits the sentence."""
    _register_fonts()
    text_width = pdfmetrics.stringWidth(sentence, CURSIVE_FONT_NAME, CURSIVE_FONT_SIZE)
    max_width = CONTENT_WIDTH - 20  # 10pt padding each side
    if text_width <= max_width:
        return CURSIVE_FONT_SIZE
    return CURSIVE_FONT_SIZE * (max_width / text_width)


def _draw_border(c: canvas.Canvas):
    """Draw a rectangular border around the page content area."""
    c.setStrokeColor(BORDER_COLOR)
    c.setLineWidth(1.5)
    c.setDash([])
    c.rect(
        BORDER_MARGIN,
        BORDER_MARGIN,
        PAGE_WIDTH - 2 * BORDER_MARGIN,
        PAGE_HEIGHT - 2 * BORDER_MARGIN,
    )


def _draw_header(c: canvas.Canvas, student_name: str, page_num: int):
    """Draw the header matching the reference image style.

    Layout:
      Name ________________________    Date __________________
                   CURSIVE PRACTICE  (banner)
                  Trace the sentence below!
    """
    x_left = CONTENT_LEFT
    x_right = CONTENT_RIGHT

    # --- Row 1: Name ___ and Date ___ ---
    y_top = PAGE_HEIGHT - BORDER_MARGIN - 18
    c.setFont(HEADER_FONT, HEADER_FONT_SIZE)
    c.setFillColor(HEADER_COLOR)

    # "Name" label + underline
    c.drawString(x_left, y_top, "Name")
    name_label_w = pdfmetrics.stringWidth("Name ", HEADER_FONT, HEADER_FONT_SIZE)
    name_line_start = x_left + name_label_w
    name_line_end = x_left + CONTENT_WIDTH * 0.52

    # Write the student name on the line
    c.drawString(name_line_start + 4, y_top, student_name)

    c.setStrokeColor(HEADER_COLOR)
    c.setLineWidth(0.5)
    c.setDash([])
    c.line(name_line_start, y_top - 2, name_line_end, y_top - 2)

    # "Date" label + underline
    date_x = x_left + CONTENT_WIDTH * 0.58
    today = date.today().strftime("%B %d, %Y")
    c.drawString(date_x, y_top, "Date")
    date_label_w = pdfmetrics.stringWidth("Date ", HEADER_FONT, HEADER_FONT_SIZE)
    date_line_start = date_x + date_label_w

    c.drawString(date_line_start + 4, y_top, today)
    c.line(date_line_start, y_top - 2, x_right, y_top - 2)

    # --- Row 2: Title banner ---
    banner_h = 28
    banner_y = y_top - 38
    banner_x = PAGE_WIDTH / 2 - 130
    banner_w = 260

    c.setFillColor(TITLE_BG)
    c.roundRect(banner_x, banner_y, banner_w, banner_h, 4, fill=1, stroke=0)

    c.setFillColor(white)
    c.setFont(HEADER_FONT_BOLD, TITLE_FONT_SIZE)
    c.drawCentredString(PAGE_WIDTH / 2, banner_y + 7, "CURSIVE PRACTICE")

    # --- Row 3: Subtitle ---
    c.setFillColor(HEADER_COLOR)
    c.setFont(HEADER_FONT, 9)
    c.drawCentredString(PAGE_WIDTH / 2, banner_y - 14, "Trace the sentence below!")

    # --- Page number (small, bottom-right) ---
    c.setFont(HEADER_FONT, 8)
    c.setFillColor(HEADER_COLOR)
    c.drawRightString(x_right, BORDER_MARGIN + 8, f"Page {page_num} / 2")


def _compute_row_positions(page_index: int) -> list[float]:
    """Return the y_top positions for each 3-line group on a page.

    y_top is the y-coordinate of the top (ascender) line in each group.
    """
    top_start = PAGE_HEIGHT - CONTENT_MARGIN_TOP - BORDER_MARGIN
    bottom_limit = BORDER_MARGIN + CONTENT_MARGIN_BOTTOM + 20

    usable = top_start - bottom_limit
    # Space each row slot evenly
    row_slot = usable / ROWS_PER_PAGE

    positions = []
    for i in range(ROWS_PER_PAGE):
        # Top of the 3-line group, vertically centered in the slot
        slot_top = top_start - i * row_slot
        pad = (row_slot - LINE_GROUP_HEIGHT) / 2
        y_top = slot_top - pad
        positions.append(y_top)
    return positions


def _draw_line_group(c: canvas.Canvas, y_top: float):
    """Draw a 3-line ruled group: solid top, dashed middle, solid bottom."""
    x_start = CONTENT_LEFT
    x_end = CONTENT_RIGHT

    # Top line — solid dark gray (ascender line)
    c.setStrokeColor(LINE_COLOR)
    c.setLineWidth(0.75)
    c.setDash([])
    c.line(x_start, y_top, x_end, y_top)

    # Middle line — dashed (midline / x-height guide)
    y_mid = y_top - LINE_SPACING
    c.setStrokeColor(LINE_COLOR_DASHED)
    c.setLineWidth(0.5)
    c.setDash(6, 4)  # longer dashes like the reference
    c.line(x_start, y_mid, x_end, y_mid)

    # Bottom line — solid dark gray (baseline)
    y_bottom = y_top - 2 * LINE_SPACING
    c.setStrokeColor(LINE_COLOR)
    c.setLineWidth(0.75)
    c.setDash([])
    c.line(x_start, y_bottom, x_end, y_bottom)


def _draw_traced_sentence(c: canvas.Canvas, sentence: str, y_top: float, font_size: float):
    """Draw the sentence as round-dotted letter outlines for tracing.

    Uses the PDF round line-cap trick: setLineCap(1) with a very short dash
    segment produces circular dots along the stroke path.
    """
    # Baseline is the bottom line of the 3-line group
    y_baseline = y_top - 2 * LINE_SPACING

    c.saveState()

    # Round line cap — makes tiny dash segments appear as round dots
    c.setLineCap(1)
    c.setDash(DOT_DASH_ON, DOT_DASH_OFF)
    c.setLineWidth(DOT_LINE_WIDTH)
    c.setStrokeColor(DOT_COLOR)

    text_obj = c.beginText(CONTENT_LEFT + 8, y_baseline)
    text_obj.setTextRenderMode(1)  # stroke only — dots trace the letter outlines
    text_obj.setFont(CURSIVE_FONT_NAME, font_size)
    text_obj.textLine(sentence)
    c.drawText(text_obj)

    c.restoreState()


def generate_practice_sheet(student_name: str, sentence: str, output_path: str) -> str:
    """Create a 2-page A4 cursive practice PDF.

    Page 1: traced example (row 0) + remaining blank ruled rows.
    Page 2: all blank ruled rows.
    Total practice opportunities: 1 traced + (ROWS_PER_PAGE * 2 - 1) blank.
    """
    _register_fonts()
    font_size = _fit_font_size(sentence)

    c = canvas.Canvas(output_path, pagesize=A4)
    c.setTitle(f"Cursive Practice — {student_name}")

    for page in range(2):
        _draw_border(c)
        _draw_header(c, student_name, page + 1)

        row_positions = _compute_row_positions(page)
        for i, y_top in enumerate(row_positions):
            _draw_line_group(c, y_top)

            # First row of first page: traced sentence
            if page == 0 and i == 0:
                _draw_traced_sentence(c, sentence, y_top, font_size)

        c.showPage()

    c.save()
    return output_path
