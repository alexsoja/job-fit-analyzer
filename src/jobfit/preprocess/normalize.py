from __future__ import annotations

import re


def normalize_text(text: str) -> str:
    text = text.lower()

    # Turn anything that is NOT a letter/number into a space
    # This removes commas, bullets, smart quotes, weird unicode dashes, etc.
    text = re.sub(r"[^a-z0-9]+", " ", text)

    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text
