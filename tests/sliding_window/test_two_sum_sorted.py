from tests.loader import load_exercise

two_sum_sorted = load_exercise("sliding_window/two_sum_sorted.py", "two_sum_sorted")

def test_two_sum():
    assert two_sum_sorted([2, 7, 11, 15], 9) == [1, 2]
    assert two_sum_sorted([2, 3, 4], 6) == [1, 3]
