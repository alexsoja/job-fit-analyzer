from pathlib import Path
from jobfit.extract.skills import load_skills_seed, extract_skills
from jobfit.preprocess.normalize import normalize_text


def test_jd_skills_detect_python_tensorflow():
    seed = load_skills_seed(Path("src/data/skills_seed.json"))
    jd = normalize_text("Requirements: Tensorflow scikit python")
    found = extract_skills(jd, seed["skills"], seed["synonyms"])
    assert "python" in found
    assert "tensorflow" in found
