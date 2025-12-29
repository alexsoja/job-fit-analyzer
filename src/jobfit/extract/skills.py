from __future__ import annotations

import json
from pathlib import Path

def load_skills_seed(seed_path: Path) -> dict:
    raw_text = seed_path.read_text(encoding="utf-8")
    return json.loads(raw_text)

def extract_skills(text: str, skills: list[str], synonyms: dict[str, str]) -> set[str]:
    found = set()
    for skill in skills:
        if skill in text:
            found.add(skill)
    for alias, canonical in synonyms.items():
        if alias in text:
            found.add(canonical)
    return found
