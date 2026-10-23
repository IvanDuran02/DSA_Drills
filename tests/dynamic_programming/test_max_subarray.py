from tests.loader import load_exercise

max_sub_array = load_exercise("dynamic_programming/max_subarray.py", "max_sub_array")

def test_kadane():
    assert max_sub_array([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert max_sub_array([1]) == 1
    assert max_sub_array([5, 4, -1, 7, 8]) == 23
