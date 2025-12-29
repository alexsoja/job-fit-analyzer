from jobfit.extract.experience import extract_years_required, estimate_resume_years
from jobfit.score.experience_scoring import score_experience


def test_extract_years_required_single():
    jd = "We require 2+ years of experience."
    assert extract_years_required(jd) == 2


def test_extract_years_required_range():
    jd = "Looking for 3-5 years in analytics."
    assert extract_years_required(jd) == 3


def test_estimate_resume_years_simple_range():
    resume = "Data Analyst Intern 2023-2024"
    years = estimate_resume_years(resume)
    assert years >= 2


def test_score_experience_no_requirement():
    out = score_experience(None, 0.0, max_points=35)
    assert out["experience_total"] == 35


def test_score_experience_partial():
    out = score_experience(4, 2.0, max_points=35)
    assert out["experience_total"] == round(35 * 0.5)
