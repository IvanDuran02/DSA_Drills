from tests.loader import load_exercise

max_sliding_window = load_exercise("sliding_window/sliding_window_max.py", "max_sliding_window")

def test_window_max():
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    assert max_sliding_window(nums, 3) == [3, 3, 5, 5, 6, 7]
