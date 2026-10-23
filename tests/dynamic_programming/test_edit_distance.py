from tests.loader import load_exercise

min_distance = load_exercise("dynamic_programming/edit_distance.py", "min_distance")

def test_edit_dist():
    assert min_distance("horse", "ros") == 3
    assert min_distance("intention", "execution") == 5
