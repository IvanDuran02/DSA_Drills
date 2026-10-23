from tests.loader import load_exercise

lower_bound = load_exercise("binary_search/bs_lower_bound.py", "lower_bound")

def test_lb():
    nums = [1, 2, 4, 4, 5, 6]
    assert lower_bound(nums, 4) == 2
    assert lower_bound(nums, 3) == 2
    assert lower_bound(nums, 7) == 6
