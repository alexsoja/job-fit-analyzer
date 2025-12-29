# src/jobfit/analyze.py

from __future__ import annotations

import json
from pathlib import Path

from jobfit.preprocess.normalize import normalize_text
from jobfit.extract.skills import load_skills_seed, extract_skills
from jobfit.extract.requirements import extract_requirement_lines
from jobfit.extract.education import (
    extract_education_block,
    detect_degree_level,
    detect_major_keywords,
)
from jobfit.extract.experience import extract_years_required, estimate_resume_years
from jobfit.score.scoring import score_skills
from jobfit.score.education_scoring import score_education
from jobfit.score.experience_scoring import score_experience


def analyze(resume_text: str, jd_text: str) -> dict:
    """
    Shared analysis function used by both CLI and Streamlit.

    Returns a dict with:
    - score breakdown (skills + education + experience)
    - skills matched/missing
    - education signals
    - experience signals
    - previews (before/after normalize)
    - requirement coverage (skills-based)
    """
    # Normalize text so matching is consistent
    resume_norm = normalize_text(resume_text)
    jd_norm = normalize_text(jd_text)

    # -------- Skills --------
    seed = load_skills_seed(Path("src/data/skills_seed.json"))

    resume_skills = extract_skills(resume_norm, seed["skills"], seed["synonyms"])
    jd_skills = extract_skills(jd_norm, seed["skills"], seed["synonyms"])

    matched_skills = sorted(resume_skills & jd_skills)
    missing_skills = sorted(jd_skills - resume_skills)

    # Skills score (50 points)
    skills_points = score_skills(jd_skills, resume_skills, max_points=50)

    # -------- Education --------
    majors_seed = json.loads(Path("src/data/majors_seed.json").read_text(encoding="utf-8"))
    majors_list = majors_seed["majors"]

    jd_degree = detect_degree_level(jd_text)
    jd_majors = detect_major_keywords(jd_text, majors_list)

    resume_edu_block = extract_education_block(resume_text)
    resume_degree = detect_degree_level(resume_edu_block)
    resume_majors = detect_major_keywords(resume_edu_block, majors_list)

    edu = score_education(
        jd_degree=jd_degree,
        resume_degree=resume_degree,
        jd_majors=jd_majors,
        resume_majors=resume_majors,
        max_points=15,
    )

    # -------- Experience --------
    jd_years_required = extract_years_required(jd_text)
    resume_years_estimate = estimate_resume_years(resume_text)

    exp = score_experience(
        jd_years_required=jd_years_required,
        resume_years_estimate=resume_years_estimate,
        max_points=35,
    )

    # -------- Requirement coverage (skills-based) --------
    req_lines = extract_requirement_lines(jd_text)
    coverage: list[dict] = []
    for line in req_lines:
        low = normalize_text(line)  # normalize line too
        matched_in_line = [s for s in matched_skills if s in low]
        missing_in_line = [s for s in missing_skills if s in low]
        if matched_in_line or missing_in_line:
            coverage.append(
                {
                    "line": line,
                    "matched": matched_in_line,
                    "missing": missing_in_line,
                }
            )

    # -------- Total --------
    total_points = skills_points + edu["education_total"] + exp["experience_total"]

    return {
        "score": {
            "skills_points": skills_points,
            "skills_max": 50,
            "education_points": edu["education_total"],
            "education_max": 15,
            "experience_points": exp["experience_total"],
            "experience_max": 35,
            "total_points": total_points,
            "total_max": 100,
            "note": "Total score includes skills + education + experience.",
        },
        "skills": {
            "resume_skills": sorted(resume_skills),
            "jd_skills": sorted(jd_skills),
            "matched": matched_skills,
            "missing": missing_skills,
        },
        "education": edu,
        "experience": exp,
        "previews": {
            "resume_before": resume_text[:120],
            "jd_before": jd_text[:120],
            "resume_after": resume_norm[:120],
            "jd_after": jd_norm[:120],
            "resume_edu_block": resume_edu_block[:400],
        },
        "requirements": {
            "lines": req_lines,
            "coverage": coverage,
        },
    }
