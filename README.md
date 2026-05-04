# Cursive Practice

A command-line tool that generates cursive handwriting practice sheets as printable A4 PDFs. Built for teachers and parents helping students (especially 4th graders) develop their cursive writing skills.

## What It Does

The tool walks you through three simple steps:

1. **Pick a cursive font** -- a visual sampler PDF opens showing all 13 available cursive styles with alphabet and sentence previews on ruled lines. Pick the one you want your students to practice.
2. **Enter the student's name** -- appears on every page header alongside the date.
3. **Choose a practice sentence** -- pick from 5 themed options (Nature, Adventure, Science, Animals, Arts), shuffle for new ones, or type your own. Sentences are validated: at least 5 words, no more than 3 filler/conjunction words.

It then generates a **2-page A4 PDF** (print double-sided on one sheet):

- **Page 1**: Round-dotted traceable cursive sentence on the first row + 6 blank practice rows
- **Page 2**: 7 blank practice rows
- Total: **14 ruled rows** across both pages for repeated practice
- Header with student name, date, and page number
- Page border and title banner
- 3-line ruled groups (solid top line, dashed midline, solid baseline) in dark gray

## Sample Output

Each row is a 3-line ruled group matching standard cursive practice paper:

```
______________________________________  (solid — ascender/top line)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _   (dashed — midline)
______________________________________  (solid — baseline)
```

The first row on page 1 has the sentence rendered as round-dotted letter outlines for the student to trace.

## Installation

### Prerequisites

- Python 3.10 or later

### Install from source

```bash
git clone https://github.com/vbhaskarrao/cursive-practice.git
cd cursive-practice
pip install .
```

### Install in development mode

```bash
pip install -e .
```

## Fonts

The tool ships with **8 bundled cursive fonts** (all open-source, OFL-licensed) and auto-detects up to **5 additional system fonts** on Windows/macOS. No manual font setup required.

### Bundled fonts (included in `fonts/`)

| Font | Style |
|------|-------|
| Dancing Script | Popular connected school cursive |
| Sacramento | Flowing thin cursive |
| Great Vibes | Formal elegant cursive |
| Edu NSW Foundation | Australian educational handwriting |
| Edu QLD Beginner | Australian educational handwriting |
| Edu SA Beginner | Australian educational handwriting |
| Edu TAS Beginner | Australian educational handwriting |
| Edu VIC Beginner | Australian educational handwriting |

### System fonts (auto-detected)

- **Windows**: Mistral, French Script, Brush Script, Lucida Handwriting, Ink Free
- **macOS**: Brush Script, Snell Roundhand

### Custom font

Set the `CURSIVE_FONT` environment variable to the path of any `.ttf` file to add your own:

```bash
# Linux / macOS
export CURSIVE_FONT="$HOME/.local/share/fonts/MyFont.ttf"

# Windows (PowerShell)
$env:CURSIVE_FONT = "C:\Users\YourName\Fonts\MyFont.ttf"
```

## Usage

### As a command

```bash
cursive-practice
```

### As a Python module

```bash
python -m cursive_practice
```

### Interactive session

```
====================================================
   Cursive Writing Practice Sheet Generator
====================================================

Discovering available cursive fonts...

  Font sampler saved and opened: ~\Downloads\CursiveFontSampler.pdf
  Review the PDF to compare each cursive style.

  Available fonts:

    1. Dancing Script
    2. Sacramento
    3. Great Vibes
    4. Edu NSW Foundation
    ...
    13. Ink Free

  Pick a font (1-13): 1

  Selected: Dancing Script

Student's name: Aarav

Choose a practice sentence for Aarav:

  1. [Nature] Golden sunflowers swayed gently beneath the summer sky.
  2. [Adventure] Brave explorers discovered hidden treasures underground.
  3. [Science] Powerful telescopes revealed spectacular distant galaxies.
  4. [Animals] Graceful flamingos gathered near the shimmering lagoon.
  5. [Arts] Skilled dancers twirled elegantly across the grand stage.

  6. Type my own sentence
  7. Shuffle — show new options

Pick a number (1-7): 2

  Selected: "Brave explorers discovered hidden treasures underground."

Generating practice sheet...

Done! Saved to:
  ~\Downloads\Aarav_CursivePractice_2026-04-29.pdf

Generate another sheet? (y/n): n

Happy practicing!
```

The PDF is saved to your Downloads folder and opens automatically, ready to print double-sided on one A4 sheet.

## Project Structure

```
cursive-practice/
    cursive_practice/
        __init__.py          # Package version
        __main__.py          # Entry point (python -m cursive_practice)
        cli.py               # Interactive CLI: font selection, name, sentence menu
        constants.py         # Page layout, colors, font discovery, validation rules
        pdf_generator.py     # Font sampler + practice sheet PDF generation
        suggestions.py       # 27 themed sentences across 5 categories
        validator.py         # Sentence validation logic
    fonts/                   # 8 bundled OFL-licensed cursive fonts
    pyproject.toml           # Package metadata and dependencies
    requirements.txt         # Pip dependencies
    LICENSE                  # MIT
    README.md
```

## Sentence Options

The tool presents 5 themed sentence choices each time, drawn from a bank of 27 sentences across these categories:

| Theme | Example |
|-------|---------|
| Nature | *"Golden sunflowers swayed gently beneath the summer sky."* |
| Adventure | *"Brave explorers discovered hidden treasures underground."* |
| Science | *"Powerful telescopes revealed spectacular distant galaxies."* |
| Animals | *"Graceful flamingos gathered near the shimmering lagoon."* |
| Arts | *"Skilled dancers twirled elegantly across the grand stage."* |

Pick option **7** to shuffle for a fresh set, or option **6** to type your own sentence.

### Sentence rules

To encourage meaningful practice:

- **Minimum 5 words** -- short sentences don't build muscle memory
- **Maximum 3 filler words** -- words like *and, the, is, a, was, but, or* are limited so students practice a wider variety of letter combinations

## Roadmap

- **Scan feedback** -- upload a photo/scan of the completed sheet and get AI-powered feedback on letter formation, spacing, and consistency from a virtual cursive writing coach
- **Multi-language support** -- practice cursive in other languages
- **Custom templates** -- adjustable line spacing for different grade levels (K-2 wide, 3-4 narrow, 5+ compact)
- **Letter-by-letter practice mode** -- individual letter sheets before full sentences
- **Web UI** -- browser-based version for easier access

## Contributing

Contributions are welcome! Some ideas:

- Add more themed sentence categories and grade-appropriate sentences
- Add new bundled fonts (must be OFL or similarly licensed)
- Build the scan feedback feature
- Create a web UI
- Add line spacing presets for different grade levels

```bash
# Clone and set up for development
git clone https://github.com/vbhaskarrao/cursive-practice.git
cd cursive-practice
pip install -e .

# Run
cursive-practice
```

## License

MIT License. See [LICENSE](LICENSE) for details.
