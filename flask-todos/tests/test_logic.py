from app.logic import normalize_title

def test_normalize_title_trims_and_limits():
    assert normalize_title("  Hello  ") == "Hello"
    assert normalize_title("") == "Untitled"
    assert len(normalize_title("x" * 200)) == 100
