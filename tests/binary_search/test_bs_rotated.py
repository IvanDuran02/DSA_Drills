from tests.loader import load_exercise

search_rotated = load_exercise("binary_search/bs_rotated.py", "search_rotated")

def test_rotated():
    nums = [4, 5, 6, 7, 0, 1, 2]
    assert search_rotated(nums, 0) == 4
    assert search_rotated(nums, 3) == -1
