# src/jobfit/extract/skills.py

from __future__ import annotations

import json
import re
from pathlib import Path


def load_skills_seed(seed_path: Path) -> dict:
    return json.loads(seed_path.read_text(encoding="utf-8"))


def _contains(text: str, phrase: str) -> bool:
    p = phrase.lower()

    # Single word skills: word boundary regex
    if (" " not in p) and ("-" not in p):
        pattern = rf"\b{re.escape(p)}\b"   # IMPORTANT: single backslash
        return re.search(pattern, text) is not None

    # Multiword or hyphenated: substring match
    return p in text


def extract_skills(text: str, skills: list[str], synonyms: dict[str, str]) -> set[str]:
    found: set[str] = set()

    for skill in skills:
        if _contains(text, skill):
            found.add(skill)

    for alias, canonical in synonyms.items():
        if _contains(text, alias):
            found.add(canonical)

    return found
