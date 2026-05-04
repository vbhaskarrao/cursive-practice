import random

# Organized by theme for variety across sessions
_SENTENCES = {
    "Nature": [
        "Bright butterflies danced gracefully through the meadow.",
        "Gentle snowflakes blanketed the quiet mountain village.",
        "Colorful parrots chirped melodious tunes every morning.",
        "Mighty rivers carved deep valleys through ancient rocks.",
        "Golden sunflowers swayed gently beneath the summer sky.",
        "Playful otters splashed joyfully along the riverbank.",
        "Crimson leaves tumbled softly from towering maple trees.",
    ],
    "Adventure": [
        "Brave explorers discovered hidden treasures underground.",
        "Clever foxes navigated through misty enchanted forests.",
        "Fearless astronauts journeyed beyond distant shimmering stars.",
        "Daring pirates searched for legendary sunken galleons.",
        "Curious travelers mapped uncharted jungle pathways carefully.",
    ],
    "Science": [
        "Brilliant scientists invented remarkable devices yesterday.",
        "Powerful telescopes revealed spectacular distant galaxies.",
        "Tiny molecules combined together creating amazing compounds.",
        "Clever engineers designed incredible bridges spanning rivers.",
        "Talented researchers decoded mysterious ancient manuscripts.",
    ],
    "Animals": [
        "Curious dolphins leaped joyfully above sparkling waves.",
        "Magnificent elephants marched slowly across golden plains.",
        "Playful kittens tumbled happily across the garden.",
        "Graceful flamingos gathered near the shimmering lagoon.",
        "Clever chimpanzees crafted simple tools from branches.",
    ],
    "Arts": [
        "Talented musicians performed beautiful melodies together.",
        "Creative painters captured breathtaking sunset landscapes.",
        "Skilled dancers twirled elegantly across the grand stage.",
        "Young poets composed heartfelt verses about friendship.",
        "Gifted sculptors shaped magnificent figures from marble.",
    ],
}


def get_choices(count: int = 5) -> list[tuple[str, str]]:
    """Return a list of (sentence, theme) tuples, sampling across different themes.

    Picks from as many distinct themes as possible so the student sees variety.
    """
    themes = list(_SENTENCES.keys())
    random.shuffle(themes)

    choices: list[tuple[str, str]] = []
    theme_idx = 0
    while len(choices) < count:
        theme = themes[theme_idx % len(themes)]
        pool = _SENTENCES[theme]
        pick = random.choice(pool)
        # Avoid duplicates
        if pick not in [c[0] for c in choices]:
            choices.append((pick, theme))
        theme_idx += 1
        # Safety: break if we've exhausted everything
        if theme_idx > count * 3:
            break

    return choices
