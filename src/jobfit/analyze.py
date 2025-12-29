from __future__ import annotations

from pathlib import Path

from jobfit.preprocess.normalize import normalize_text
from jobfit.extract.skills import load_skills_seed, extract_skills
from jobfit.extract.requirements import extract_requirement_lines
from jobfit.score.scoring import score_skills


def analyze(resume_text: str, jd_text: str) -> dict:
    resume_norm = normalize_text(resume_text)
    jd_norm = normalize_text(jd_text)

    seed = load_skills_seed(Path("src/data/skills_seed.json"))

    resume_skills = extract_skills(resume_norm, seed["skills"], seed["synonyms"])
    jd_skills = extract_skills(jd_norm, seed["skills"], seed["synonyms"])

    matched_skills = sorted(resume_skills & jd_skills)
    missing_skills = sorted(jd_skills - resume_skills)

    skills_points = score_skills(jd_skills, resume_skills, max_points=50)

    req_lines = extract_requirement_lines(jd_text)
    coverage = []
    for line in req_lines:
        low = line.lower()
        matched_in_line = [s for s in matched_skills if s in low]
        missing_in_line = [s for s in missing_skills if s in low]
        if matched_in_line or missing_in_line:
            coverage.append({"line": line, "matched": matched_in_line, "missing": missing_in_line})

    return {
        "score": {
            "skills_points": skills_points,
            "skills_max": 50,
            "total_points": skills_points,
            "total_max": 100,
            "note": "Total score is skills-only for now. Add education/experience later.",
        },
        "skills": {
            "resume_skills": sorted(resume_skills),
            "jd_skills": sorted(jd_skills),
            "matched": matched_skills,
            "missing": missing_skills,
        },
        "previews": {
            "resume_before": resume_text[:120],
            "jd_before": jd_text[:120],
            "resume_after": resume_norm[:120],
            "jd_after": jd_norm[:120],
        },
        "requirements": {"lines": req_lines, "coverage": coverage},
    }
