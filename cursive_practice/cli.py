"""Interactive CLI for the cursive practice sheet generator."""

import os
import sys
from datetime import date

from .pdf_generator import generate_practice_sheet
from .suggestions import get_suggestion
from .validator import validate_sentence

DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "Downloads")


def _ask_name() -> str:
    while True:
        name = input("\nStudent's name: ").strip()
        if name:
            return name
        print("  Please enter the student's name.")


def _ask_sentence(student_name: str) -> str:
    print(f"\nGreat! Now enter a practice sentence for {student_name}.")
    print("(At least 5 words, with no more than 3 filler words like 'and', 'the', 'is'...)")
    print("Press Enter without typing to get a suggestion.\n")

    while True:
        raw = input("Sentence: ").strip()

        # Empty — offer a suggestion
        if not raw:
            suggestion = get_suggestion()
            print(f'\n  Suggested: "{suggestion}"')
            choice = input("  Use this sentence? (y/n): ").strip().lower()
            if choice in ("y", "yes", ""):
                print(f'  Using: "{suggestion}"')
                return suggestion
            print("  Okay, try entering your own sentence.\n")
            continue

        # Validate
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
            sentence = _ask_sentence(student_name)

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
