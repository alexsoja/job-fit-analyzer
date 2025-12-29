from jobfit.preprocess.normalize import normalize_text

def test_normalize_text_basic():
    raw = "Hello\n\tWorld   "
    out = normalize_text(raw)
    assert out == "hello world"
