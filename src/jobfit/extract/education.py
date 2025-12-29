# src/jobfit/extract/education.py

from __future__ import annotations

import re


def extract_education_block(text: str) -> str:
    """
    Try to isolate the education block from a resume.
    Very simple: find a line containing 'education' and take the next ~12 lines.
    If not found, fall back to the first 800 characters.
    """
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if "education" in line.lower():
            block = "\n".join(lines[i : i + 12])
            return block
    return text[:800]


import re


def detect_degree_level(text: str) -> str | None:
    """
    Detect the highest degree level mentioned in text.
    Returns: 'phd', 'masters', 'bachelors', or None
    """
    t = text.lower()

    # ---- PhD (highest first) ----
    if re.search(
        r"\b(ph\.?d\.?|phd|doctorate|doctoral)\b",
        t,
    ):
        return "phd"

    # ---- Masters ----
    if re.search(
        r"\b(master|masters|m\.?s\.?|m\.?a\.?|mba|m\.?eng\.?)\b",
        t,
    ):
        return "masters"

    # ---- Bachelors ----
    if re.search(
        r"\b(bachelor|bachelors|b\.?s\.?|b\.?a\.?|b\.?eng\.?)\b",
        t,
    ):
        return "bachelors"

    return None



def detect_major_keywords(text: str, major_keywords: list[str]) -> set[str]:
    t = text.lower()
    found = set()
    for kw in major_keywords:
        if kw in t:
            found.add(kw)
    return found
