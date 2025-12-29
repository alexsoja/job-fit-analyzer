from jobfit.score.scoring import score_skills

def test_score_skills_half():
    jd = {"python", "sql"}
    resume = {"python"}
    assert score_skills(jd, resume, max_points=50) == 25

def test_score_skills_empty_jd():
    assert score_skills(set(), {"python"}, max_points=50) == 0
