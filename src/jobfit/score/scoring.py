from __future__ import annotations

def score_skills(jd_skills: set[str], resume_skills: set[str], max_points: int = 50) -> int:
    if not jd_skills:
        return 0
    matched = jd_skills & resume_skills
    coverage = len(matched) / len(jd_skills)
    return round(max_points * coverage)
