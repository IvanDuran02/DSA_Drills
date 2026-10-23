from tests.loader import load_exercise

can_partition_sum = load_exercise("dynamic_programming/take_or_skip.py", "can_partition_sum")

def test_take_or_skip():
    assert can_partition_sum([1, 5, 11, 5], 11) is True
    assert can_partition_sum([1, 2, 3, 5], 50) is False
