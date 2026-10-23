from tests.loader import load_exercise

find_kth_largest = load_exercise("heaps/kth_largest.py", "find_kth_largest")

def test_kth():
    assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
