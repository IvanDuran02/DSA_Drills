from tests.loader import load_exercise

find_target_sum_ways = load_exercise("dynamic_programming/target_sum_memo.py", "find_target_sum_ways")

def test_target_sum():
    assert find_target_sum_ways([1, 1, 1, 1, 1], 3) == 5
    assert find_target_sum_ways([1], 1) == 1
