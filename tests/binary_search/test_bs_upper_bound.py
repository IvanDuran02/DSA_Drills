from tests.loader import load_exercise

upper_bound = load_exercise("binary_search/bs_upper_bound.py", "upper_bound")

def test_ub():
    nums = [1, 2, 4, 4, 5, 6]
    assert upper_bound(nums, 4) == 4
    assert upper_bound(nums, 6) == 6
