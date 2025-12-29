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


def detect_degree_level(text: str) -> str | None:
    """
    Regex-based degree detection to avoid false positives.

    Looks for common degree tokens using word boundaries.
    """
    t = text.lower()

    # bachelors
    if re.search(r"\b(bachelor|b\.?s\.?|b\.?a\.?)\b", t):
        return "bachelors"

    # masters
    if re.search(r"\b(master|m\.?s\.?|m\.?a\.?|mba)\b", t):
        return "masters"

    # phd
    if re.search(r"\b(phd|ph\.?d\.?|doctorate)\b", t):
        return "phd"

    return None


def detect_major_keywords(text: str, major_keywords: list[str]) -> set[str]:
    t = text.lower()
    found = set()
    for kw in major_keywords:
        if kw in t:
            found.add(kw)
    return found
