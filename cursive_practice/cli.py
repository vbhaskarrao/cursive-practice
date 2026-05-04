"""Interactive CLI for the cursive practice sheet generator."""

import os
from datetime import date

from .constants import discover_fonts
from .pdf_generator import generate_font_sampler, generate_practice_sheet, open_pdf
from .suggestions import get_choices
from .validator import validate_sentence

DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "Downloads")


def _ask_name() -> str:
    while True:
        name = input("\nStudent's name: ").strip()
        if name:
            return name
        print("  Please enter the student's name.")


def _choose_font() -> tuple[str, str]:
    """Generate a font sampler PDF, open it, and ask user to pick a font.

    Returns (font_path, display_name).
    """
    print("\nDiscovering available cursive fonts...")
    fonts = discover_fonts()

    if len(fonts) == 1:
        print(f"  Using: {fonts[0][1]}")
        return fonts[0]

    # Generate sampler PDF
    sampler_path = os.path.join(DOWNLOADS_DIR, "CursiveFontSampler.pdf")
    generate_font_sampler(fonts, sampler_path)
    print(f"\n  Font sampler saved and opened: {sampler_path}")
    print("  Review the PDF to compare each cursive style.\n")
    open_pdf(sampler_path)

    # List fonts in terminal too
    print("  Available fonts:\n")
    for i, (_path, display) in enumerate(fonts, 1):
        print(f"    {i}. {display}")
    print()

    while True:
        raw = input(f"  Pick a font (1-{len(fonts)}): ").strip()
        if raw.isdigit():
            choice = int(raw)
            if 1 <= choice <= len(fonts):
                selected = fonts[choice - 1]
                print(f'\n  Selected: {selected[1]}')
                return selected
        print(f"  Please enter a number between 1 and {len(fonts)}.")


def _choose_sentence(student_name: str) -> str:
    """Present phrase options for the student to choose from."""

    while True:
        choices = get_choices(5)

        print(f"\nChoose a practice sentence for {student_name}:\n")
        for i, (sentence, theme) in enumerate(choices, 1):
            print(f"  {i}. [{theme}] {sentence}")
        print(f"\n  6. Type my own sentence")
        print(f"  7. Shuffle — show new options\n")

        raw = input("Pick a number (1-7): ").strip()

        if raw == "7":
            continue

        if raw == "6":
            return _custom_sentence()

        if raw in ("1", "2", "3", "4", "5"):
            idx = int(raw) - 1
            chosen = choices[idx][0]
            print(f'\n  Selected: "{chosen}"')
            return chosen

        print("  Please enter a number between 1 and 7.")


def _custom_sentence() -> str:
    """Let the student type their own sentence with validation."""
    print("\n  Type your sentence below.")
    print("  (At least 5 words, max 3 filler words like 'and', 'the', 'is'...)\n")

    while True:
        raw = input("  Sentence: ").strip()
        if not raw:
            print("  Sentence cannot be empty.\n")
            continue
        valid, error = validate_sentence(raw)
        if valid:
            return raw
        print(f"  {error}\n")


def main():
    print("=" * 52)
    print("   Cursive Writing Practice Sheet Generator")
    print("=" * 52)

    try:
        # Step 1: Choose font (generates sampler PDF)
        font_path, font_name = _choose_font()

        while True:
            # Step 2: Student name
            student_name = _ask_name()

            # Step 3: Choose sentence
            sentence = _choose_sentence(student_name)

            # Step 4: Generate practice sheet
            safe_name = student_name.replace(" ", "_")
            today = date.today().isoformat()
            filename = f"{safe_name}_CursivePractice_{today}.pdf"
            output_path = os.path.join(DOWNLOADS_DIR, filename)

            print("\nGenerating practice sheet...")
            generate_practice_sheet(student_name, sentence, output_path, font_path, font_name)
            print(f"\nDone! Saved to:\n  {output_path}")
            open_pdf(output_path)

            again = input("\nGenerate another sheet? (y/n): ").strip().lower()
            if again not in ("y", "yes"):
                break

    except (KeyboardInterrupt, EOFError):
        pass

    print("\nHappy practicing!")
