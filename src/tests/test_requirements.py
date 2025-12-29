from jobfit.extract.requirements import extract_requirement_lines

def test_extract_requirement_lines_basic():
    jd = "Requirements: Python\nNice to have: Tableau\nOther: blah"
    lines = extract_requirement_lines(jd)
    assert any("Requirements" in l for l in lines)
