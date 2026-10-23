from tests.loader import load_exercise

can_partition = load_exercise("dynamic_programming/partition_subset_sum.py", "can_partition")

def test_partition():
    assert can_partition([1, 5, 11, 5]) is True
    assert can_partition([1, 2, 3, 5]) is False
