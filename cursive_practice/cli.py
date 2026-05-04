"""Interactive CLI for the cursive practice sheet generator."""

import os
from datetime import date

from .pdf_generator import generate_practice_sheet
from .suggestions import get_choices
from .validator import validate_sentence

DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "Downloads")


def _ask_name() -> str:
    while True:
        name = input("\nStudent's name: ").strip()
        if name:
            return name
        print("  Please enter the student's name.")


def _choose_sentence(student_name: str) -> str:
    """Present phrase options for the student to choose from, or let them type their own."""

    while True:
        choices = get_choices(5)

        print(f"\nChoose a practice sentence for {student_name}:\n")
        for i, (sentence, theme) in enumerate(choices, 1):
            print(f"  {i}. [{theme}] {sentence}")
        print(f"\n  6. Type my own sentence")
        print(f"  7. Shuffle — show new options\n")

        raw = input("Pick a number (1-7): ").strip()

        # Shuffle
        if raw == "7":
            continue

        # Type their own
        if raw == "6":
            return _custom_sentence()

        # Pick from list
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
        while True:
            student_name = _ask_name()
            sentence = _choose_sentence(student_name)

            # Build output path
            safe_name = student_name.replace(" ", "_")
            today = date.today().isoformat()
            filename = f"{safe_name}_CursivePractice_{today}.pdf"
            output_path = os.path.join(DOWNLOADS_DIR, filename)

            print("\nGenerating practice sheet...")
            generate_practice_sheet(student_name, sentence, output_path)
            print(f"\nDone! Saved to:\n  {output_path}")

            again = input("\nGenerate another sheet? (y/n): ").strip().lower()
            if again not in ("y", "yes"):
                break

    except (KeyboardInterrupt, EOFError):
        pass

    print("\nHappy practicing!")
