from pathlib import Path
from jobfit.extract.skills import load_skills_seed, extract_skills
from jobfit.preprocess.normalize import normalize_text

def test_extract_skills_simple():
    seed = load_skills_seed(Path("src/data/skills_seed.json"))
    text = normalize_text("Skills: Python, SQL, pandas")
    found = extract_skills(text, seed["skills"], seed["synonyms"])
    assert found == {"python", "sql", "pandas"}
