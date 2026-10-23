from tests.loader import load_exercise

max_sum_subarray = load_exercise("sliding_window/fixed_window.py", "max_sum_subarray")

def test_fixed():
    assert max_sum_subarray([2, 1, 5, 1, 3, 2], 3) == 9
    assert max_sum_subarray([1, 2], 3) == 0
