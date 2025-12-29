from __future__ import annotations

import re


def extract_years_required(jd_text: str) -> int | None:
    """
    Pull a minimum years of experience requirement from the JD.

    Examples it catches:
    - "2+ years"
    - "3 years of experience"
    - "3-5 years" (returns 3)
    - "3 to 5 years" (returns 3)

    Returns:
    - int years if found
    - None if no years requirement detected
    """
    t = jd_text.lower()

    # Range like 3-5 years or 3 to 5 years -> take the minimum
    range_pat = re.compile(r"\b(\d+)\s*(?:-|–|to)\s*(\d+)\s*(?:years|yrs)\b")
    m = range_pat.search(t)
    if m:
        return int(m.group(1))

    # Single number like 2+ years or 2 years
    single_pat = re.compile(r"\b(\d+)\s*\+?\s*(?:years|yrs)\b")
    matches = single_pat.findall(t)
    if matches:
        # If multiple appear, take the highest minimum requirement mentioned
        return max(int(x) for x in matches)

    return None


def estimate_resume_years(resume_text: str) -> float:
    """
    Very simple estimate based on year ranges in the resume.

    Looks for patterns like:
    - 2023-2024
    - 2023–Present
    - 2022 to 2023

    We sum durations across all detected ranges.
    We do NOT dedupe overlapping jobs (simple on purpose).
    """
    t = resume_text.lower()

    year_range_pat = re.compile(r"\b(20\d{2})\s*(?:-|–|to)\s*(20\d{2}|present|current)\b")
    ranges = year_range_pat.findall(t)

    total_years = 0.0

    for start_str, end_str in ranges:
        start = int(start_str)

        if end_str in ("present", "current"):
            # Simple default: assume current year is 2025
            # You can upgrade later to use datetime.now().year
            end = 2025
        else:
            end = int(end_str)

        if end < start:
            continue

        # If someone writes 2023-2023, count as 1 year, not 0
        duration = max(1, end - start + 1)
        total_years += duration

    # If we found nothing, return 0 years
    return total_years
