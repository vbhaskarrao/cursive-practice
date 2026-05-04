import random

SUGGESTIONS = [
    "Bright butterflies danced gracefully through the meadow.",
    "Curious dolphins leaped joyfully above sparkling waves.",
    "Gentle snowflakes blanketed the quiet mountain village.",
    "Brave explorers discovered hidden treasures underground.",
    "Colorful parrots chirped melodious tunes every morning.",
    "Magnificent elephants marched slowly across golden plains.",
    "Talented musicians performed beautiful melodies together.",
    "Clever foxes navigated through misty enchanted forests.",
    "Playful kittens tumbled happily across the garden.",
    "Brilliant scientists invented remarkable devices yesterday.",
]


def get_suggestion() -> str:
    """Return a random 4th-grade-appropriate practice sentence."""
    return random.choice(SUGGESTIONS)
