from __future__ import annotations

def extract_requirement_lines(jd_text: str) -> list[str]:
    cues = [
        "required",
        "requirements",
        "must",
        "experience",
        "proficient",
        "proficiency",
        "familiar",
        "knowledge of",
        "ability to",
        "years",
    ]

    lines = [line.strip() for line in jd_text.splitlines()]
    lines = [line for line in lines if line]

    req_lines = []
    for line in lines:
        low = line.lower()
        if any(cue in low for cue in cues):
            req_lines.append(line)
    return req_lines
