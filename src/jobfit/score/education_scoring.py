from __future__ import annotations


def score_education(
    jd_degree: str | None,
    resume_degree: str | None,
    jd_majors: set[str],
    resume_majors: set[str],
    max_points: int = 15,
) -> dict:
    degree_points = 0
    major_points = 0

    # Degree: if JD doesn't specify, don't penalize
    if jd_degree is None:
        degree_points = 10
    elif resume_degree == jd_degree:
        degree_points = 10

    # Major: if JD doesn't specify, don't penalize
    if not jd_majors:
        major_points = 5
    elif jd_majors & resume_majors:
        major_points = 5

    total = min(degree_points + major_points, max_points)

    return {
        "education_total": total,
        "degree_points": degree_points,
        "major_points": major_points,
        "jd_degree": jd_degree,
        "resume_degree": resume_degree,
        "matched_majors": sorted(jd_majors & resume_majors),
        "missing_majors": sorted(jd_majors - resume_majors),
    }
