# Cursive Practice

A command-line tool that generates cursive handwriting practice sheets as printable A4 PDFs. Built for teachers and parents helping students (especially 4th graders) develop their cursive writing skills.

## What It Does

1. Asks for the student's name
2. Asks for a practice sentence (or suggests one at 4th-grade reading level)
3. Validates the sentence — at least 5 words, no more than 3 filler/conjunction words
4. Generates a **2-page A4 PDF** (print double-sided on one sheet):
   - **Page 1**: Dotted/traceable cursive sentence on the first row + 3 blank practice rows
   - **Page 2**: 4 blank practice rows
   - Total: **7 practice repetitions** per sheet
   - Header with student name, date, and page number
   - Professional 4-line ruled groups (blue ascender/descender lines, red dashed midline, red solid baseline)

## Sample Output

Each row is a 4-line ruled group matching standard cursive practice paper:

```
──────────────────────────────────  (blue — ascender line)
- - - - - - - - - - - - - - - - -  (red dashed — midline)
──────────────────────────────────  (red solid — baseline)
──────────────────────────────────  (blue — descender line)
```

The first row on page 1 has the sentence rendered in dotted cursive for the student to trace.

## Installation

### Prerequisites

- Python 3.10 or later
- A cursive TTF font (see [Font Setup](#font-setup) below)

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

## Font Setup

The tool needs a cursive-style TrueType font (.ttf). It searches for fonts in this order:

1. **`CURSIVE_FONT` environment variable** — set this to the full path of any cursive `.ttf` file
2. **Bundled font** — place a font file at `fonts/DancingScript-Regular.ttf` in the project directory
3. **System fonts** (auto-detected per platform):
   - **Windows**: Mistral, French Script MT, or Brush Script (pre-installed on most systems)
   - **macOS**: Brush Script or Snell Roundhand
   - **Linux**: any `.ttf` with "cursive", "script", "dancing", or "pacifico" in the name under `/usr/share/fonts`

### Recommended free font

Download [Dancing Script](https://fonts.google.com/specimen/Dancing+Script) from Google Fonts (OFL license) and either:

- Place `DancingScript-Regular.ttf` in the `fonts/` directory, **or**
- Set the environment variable:

```bash
# Linux / macOS
export CURSIVE_FONT="$HOME/.local/share/fonts/DancingScript-Regular.ttf"

# Windows (PowerShell)
$env:CURSIVE_FONT = "C:\Users\YourName\Fonts\DancingScript-Regular.ttf"
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

Student's name: Aarav

Great! Now enter a practice sentence for Aarav.
(At least 5 words, with no more than 3 filler words like 'and', 'the', 'is'...)
Press Enter without typing to get a suggestion.

Sentence: Bright butterflies danced gracefully through the meadow.

Generating practice sheet...

Done! Saved to:
  C:\Users\you\Downloads\Aarav_CursivePractice_2026-04-29.pdf

Generate another sheet? (y/n): n

Happy practicing!
```

The PDF is saved to your Downloads folder, ready to print double-sided on one A4 sheet.

## Project Structure

```
cursive-practice/
    cursive_practice/
        __init__.py          # Package version
        __main__.py          # Entry point (python -m cursive_practice)
        cli.py               # Interactive CLI flow
        constants.py         # Page layout, colors, font config, validation rules
        pdf_generator.py     # Core PDF creation engine
        suggestions.py       # Bank of grade-appropriate fallback sentences
        validator.py         # Sentence validation logic
    fonts/                   # Place bundled TTF fonts here (optional)
    pyproject.toml           # Package metadata and dependencies
    requirements.txt         # Pip dependencies
    LICENSE                  # MIT
    README.md
```

## Sentence Rules

To encourage meaningful practice:

- **Minimum 5 words** — short sentences don't build muscle memory
- **Maximum 3 filler words** — words like *and, the, is, a, was, but, or, in, on, to, it, at* are limited so students practice a wider variety of letter combinations

If the student can't think of a sentence, the tool offers grade-appropriate suggestions like:
- *"Brave explorers discovered hidden treasures underground."*
- *"Curious dolphins leaped joyfully above sparkling waves."*
- *"Talented musicians performed beautiful melodies together."*

## Roadmap

- **Scan feedback** — upload a photo/scan of the completed sheet and get AI-powered feedback on letter formation, spacing, and consistency from a virtual cursive writing coach
- **Multi-language support** — practice cursive in other languages
- **Custom templates** — adjustable line spacing for different grade levels
- **Letter-by-letter practice mode** — individual letter sheets before full sentences

## Contributing

Contributions are welcome! Some ideas:

- Add more grade-appropriate suggestion sentences
- Support additional font formats
- Add line spacing presets for different grade levels (K-2 wide, 3-4 narrow, 5+ compact)
- Build the scan feedback feature
- Create a web UI

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
