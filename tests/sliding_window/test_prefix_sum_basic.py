from tests.loader import load_exercise

NumArray = load_exercise("sliding_window/prefix_sum_basic.py", "NumArray")

def test_num_array():
    na = NumArray([-2, 0, 3, -5, 2, -1])
    assert na.sum_range(0, 2) == 1
    assert na.sum_range(2, 5) == -1
    assert na.sum_range(0, 5) == -3
