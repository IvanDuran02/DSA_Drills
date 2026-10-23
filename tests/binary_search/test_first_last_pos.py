from tests.loader import load_exercise

search_range = load_exercise("binary_search/first_last_pos.py", "search_range")

def test_range():
    nums = [5, 7, 7, 8, 8, 10]
    assert search_range(nums, 8) == [3, 4]
    assert search_range(nums, 6) == [-1, -1]
    assert search_range([], 0) == [-1, -1]
