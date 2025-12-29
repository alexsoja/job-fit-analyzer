from __future__ import annotations


def score_experience(
    jd_years_required: int | None,
    resume_years_estimate: float,
    max_points: int = 35,
) -> dict:
    """
    Score experience out of max_points.

    Rules:
    - If JD does not specify years, do not penalize (full points).
    - Otherwise score proportional coverage, capped at 1.0.

    Returns a dict with points and an explanation payload.
    """
    if jd_years_required is None:
        return {
            "experience_total": max_points,
            "jd_years_required": None,
            "resume_years_estimate": resume_years_estimate,
            "coverage": 1.0,
            "note": "JD did not specify years of experience, no penalty applied.",
        }

    if jd_years_required <= 0:
        return {
            "experience_total": max_points,
            "jd_years_required": jd_years_required,
            "resume_years_estimate": resume_years_estimate,
            "coverage": 1.0,
            "note": "JD years requirement looked invalid, no penalty applied.",
        }

    coverage = min(1.0, resume_years_estimate / jd_years_required)
    points = round(max_points * coverage)

    note = "Meets or exceeds JD years requirement." if coverage >= 1.0 else "Below JD years requirement."

    return {
        "experience_total": points,
        "jd_years_required": jd_years_required,
        "resume_years_estimate": resume_years_estimate,
        "coverage": coverage,
        "note": note,
    }
