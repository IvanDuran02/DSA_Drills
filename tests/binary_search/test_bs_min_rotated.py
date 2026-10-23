from tests.loader import load_exercise

find_min = load_exercise("binary_search/bs_min_rotated.py", "find_min")

def test_min_rotated():
    assert find_min([3, 4, 5, 1, 2]) == 1
    assert find_min([4, 5, 6, 7, 0, 1, 2]) == 0
    assert find_min([11, 13, 15, 17]) == 11
