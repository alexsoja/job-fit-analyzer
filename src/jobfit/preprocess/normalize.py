from __future__ import annotations

import re

def normalize_text(text: str) -> str:
    text = text.lower()
    text = text.strip()
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = re.sub(r"\s+", " ", text)
    return text
