from tests.loader import load_exercise

subarray_sum = load_exercise("sliding_window/prefix_sum_hashmap.py", "subarray_sum")

def test_sub_sum():
    assert subarray_sum([1, 1, 1], 2) == 2
    assert subarray_sum([1, 2, 3], 3) == 2
    assert subarray_sum([1, -1, 0], 0) == 3
