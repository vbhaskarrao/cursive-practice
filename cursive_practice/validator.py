import string

from .constants import FILLER_WORDS, MAX_FILLER, MIN_WORDS


def validate_sentence(sentence: str) -> tuple[bool, str]:
    """Validate a practice sentence.

    Returns (is_valid, error_message). error_message is empty when valid.
    """
    words = sentence.strip().split()
    if len(words) < MIN_WORDS:
        return False, f"Sentence must have at least {MIN_WORDS} words (you entered {len(words)})."

    filler_count = sum(
        1
        for w in words
        if w.lower().strip(string.punctuation) in FILLER_WORDS
    )
    if filler_count > MAX_FILLER:
        return False, (
            f"Too many filler/conjunction words ({filler_count}). "
            f"Maximum allowed is {MAX_FILLER}. Try a more descriptive sentence."
        )

    return True, ""
