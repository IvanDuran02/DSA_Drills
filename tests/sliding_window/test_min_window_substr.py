from tests.loader import load_exercise

min_window = load_exercise("sliding_window/min_window_substr.py", "min_window")

def test_min_window():
    assert min_window("ADOBECODEBANC", "ABC") == "BANC"
    assert min_window("a", "a") == "a"
    assert min_window("a", "aa") == ""
